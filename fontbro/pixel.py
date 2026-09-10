from __future__ import annotations

import string
import sys
from collections import Counter
from typing import Any

from fontTools import unicodedata
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont

from fontbro.unicode import get_best_cmap

Segment = tuple[float, float]

# the glyphs of these characters are used to detect pixel fonts
_CHARACTERS: str = string.ascii_uppercase + string.ascii_lowercase + string.digits

# number of glyphs used if the font has none of the characters above
_FALLBACK_GLYPHS_COUNT: int = 50

# max distance of a segment length from a multiple of the pixel size,
# relative to the pixel size (pixel fonts can have small off-grid details),
# higher values (eg. 0.25) cause false positives with squared ("techno") fonts
_GRID_TOLERANCE: float = 0.2

# plausible range of the pixel grid resolution
_PIXELS_PER_EM_MIN: int = 4
_PIXELS_PER_EM_MAX: int = 64

# max divisor of the most common segments length tried as pixel size,
# because the most common length can be a multiple of the pixel size
# (eg. when strokes are always at least 2 pixels long)
_PIXEL_SIZE_MAX_DIVISOR: int = 4


def _is_straight_curve(
    start: tuple[float, float],
    points: tuple[Any, ...],
) -> bool:
    """
    Determines if the curve is a degenerate curve, geometrically a straight
    horizontal / vertical segment: all its points are aligned with the start point
    (used eg. in variable fonts for interpolation compatibility with curves).
    """
    # an implied on-curve end point (TrueType contour of off-curve points only)
    if points[-1] is None:
        return False
    return all(point[0] == start[0] for point in points) or all(
        point[1] == start[1] for point in points
    )


def _get_glyph_segments(
    glyphset: Any,
    glyph_name: str,
) -> list[Segment] | None:
    """
    Gets the (dx, dy) segments of the glyph outlines (components are decomposed),
    zero-length segments are ignored, None is returned if outlines contain curves
    (degenerate curves that are straight segments are considered segments).
    """
    pen = DecomposingRecordingPen(glyphset)
    glyphset[glyph_name].draw(pen)
    segments: list[Segment] = []
    start = prev = (0, 0)
    for operator, operands in pen.value:
        if operator == "moveTo":
            start = prev = operands[0]
            continue
        if operator in ("qCurveTo", "curveTo"):
            if not _is_straight_curve(prev, operands):
                return None
            point = operands[-1]
        elif operator == "lineTo":
            point = operands[0]
        elif operator == "closePath":
            point = start
        else:
            # "endPath" closes an open contour without a segment
            continue
        segment = (point[0] - prev[0], point[1] - prev[1])
        if segment != (0, 0):
            segments.append(segment)
        prev = point
    return segments


def _get_glyphs_segments(
    ttfont: TTFont,
) -> list[list[Segment] | None]:
    """
    Gets the segments of the glyphs used to detect pixel fonts: the glyphs of
    A-Z, a-z and 0-9, or if the font has none of them, the first glyphs
    (by codepoint) that are not punctuation; glyphs without outlines are ignored.
    """
    cmap = get_best_cmap(ttfont) or {}
    codepoints = [ord(char) for char in _CHARACTERS if ord(char) in cmap]
    fallback = not codepoints
    if fallback:
        codepoints = [
            codepoint
            for codepoint in sorted(cmap)
            # malformed cmaps can contain codepoints out of the unicode range
            if codepoint <= sys.maxunicode
            and not unicodedata.category(chr(codepoint)).startswith("P")
        ]
    glyphset = ttfont.getGlyphSet()
    glyphs_names = set()
    glyphs_segments = []
    for codepoint in codepoints:
        glyph_name = cmap[codepoint]
        # malformed cmaps can map codepoints to missing glyphs
        if glyph_name in glyphs_names or glyph_name not in glyphset:
            continue
        glyphs_names.add(glyph_name)
        segments = _get_glyph_segments(glyphset, glyph_name)
        if segments == []:
            continue
        glyphs_segments.append(segments)
        if fallback and len(glyphs_segments) == _FALLBACK_GLYPHS_COUNT:
            break
    return glyphs_segments


def _is_orthogonal(
    segments: list[Segment],
) -> bool:
    """
    Determines if all the segments are horizontal or vertical.
    """
    return all(dx == 0 or dy == 0 for dx, dy in segments)


def _is_multiple(
    length: float,
    unit: float,
) -> bool:
    """
    Determines if the length is multiple of the unit, within the grid tolerance.
    """
    return abs(length - round(length / unit) * unit) <= unit * _GRID_TOLERANCE


def _is_on_grid(
    segments: list[Segment],
    axis: int,
    pixel_dimension: float,
) -> bool:
    """
    Determines if the lengths of the (orthogonal) segments along the axis
    (0: horizontal, 1: vertical) are multiple of the pixel dimension.
    """
    return all(
        _is_multiple(abs(segment[axis]), pixel_dimension)
        for segment in segments
        if segment[axis]
    )


def _get_pixel_dimension(
    glyphs_segments: list[list[Segment]],
    axis: int,
    units_per_em: int,
    min_glyphs_count: float,
) -> float:
    """
    Gets the pixel dimension along the axis (0: width, 1: height), since pixels
    can be rectangular: the coarsest grid, among the most common segments length
    and its divisors, with enough glyphs on it; 0 is returned if there is no such
    grid or if its resolution is not plausible.
    """
    lengths = Counter(
        abs(segment[axis])
        for segments in glyphs_segments
        for segment in segments
        if segment[axis]
    )
    if not lengths:
        return 0
    most_common_length = lengths.most_common(1)[0][0]
    for divisor in range(1, _PIXEL_SIZE_MAX_DIVISOR + 1):
        pixel_dimension = most_common_length / divisor
        on_grid_glyphs_count = sum(
            1
            for segments in glyphs_segments
            if _is_on_grid(segments, axis, pixel_dimension)
        )
        if on_grid_glyphs_count >= min_glyphs_count:
            pixels_per_em = units_per_em / pixel_dimension
            if _PIXELS_PER_EM_MIN <= pixels_per_em <= _PIXELS_PER_EM_MAX:
                return pixel_dimension
            return 0
    return 0


def is_pixel(
    ttfont: TTFont,
    *,
    threshold: float = 0.9,
) -> bool:
    """
    Determines if the given font is a pixel font.
    """
    glyphs_segments = _get_glyphs_segments(ttfont)
    if not glyphs_segments:
        return False
    min_glyphs_count = len(glyphs_segments) * threshold

    # 1st check: outlines made only of horizontal and vertical straight segments,
    # it excludes all fonts except pixel fonts and squared ("techno") fonts
    orthogonal_glyphs_segments = [
        segments
        for segments in glyphs_segments
        if segments is not None and _is_orthogonal(segments)
    ]
    if len(orthogonal_glyphs_segments) < min_glyphs_count:
        return False

    # 2nd check: segments aligned to a plausible pixel grid,
    # it excludes squared ("techno") fonts
    units_per_em = ttfont["head"].unitsPerEm
    pixel_width, pixel_height = (
        _get_pixel_dimension(
            orthogonal_glyphs_segments, axis, units_per_em, min_glyphs_count
        )
        for axis in (0, 1)
    )
    if not pixel_width or not pixel_height:
        return False
    on_grid_glyphs_count = sum(
        1
        for segments in orthogonal_glyphs_segments
        if _is_on_grid(segments, 0, pixel_width)
        and _is_on_grid(segments, 1, pixel_height)
    )
    return on_grid_glyphs_count >= min_glyphs_count

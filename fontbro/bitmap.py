from __future__ import annotations

from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

# monochrome bitmap tables (data, location): opentype and apple,
# color bitmap tables (CBDT/CBLC, sbix) are not considered,
# because color bitmap fonts are emoji / images, not bitmap fonts
_BITMAP_TABLES_TAGS: tuple[tuple[str, str], ...] = (
    ("EBDT", "EBLC"),
    ("bdat", "bloc"),
)

_OUTLINES_TABLES_TAGS: tuple[str, ...] = (
    "glyf",
    "CFF ",
    "CFF2",
)


def _has_bitmap_tables(
    ttfont: TTFont,
) -> bool:
    """
    Determines if the given font has monochrome bitmap tables.
    """
    return any(
        data_tag in ttfont and location_tag in ttfont
        for data_tag, location_tag in _BITMAP_TABLES_TAGS
    )


def _has_outlines(
    ttfont: TTFont,
) -> bool:
    """
    Determines if the given font has at least one glyph with outlines,
    the ".notdef" glyph is ignored.
    """
    if not any(tag in ttfont for tag in _OUTLINES_TABLES_TAGS):
        return False
    glyphset = ttfont.getGlyphSet()
    for glyph_name in ttfont.getGlyphOrder():
        if glyph_name == ".notdef":
            continue
        pen = RecordingPen()
        glyphset[glyph_name].draw(pen)
        if pen.value:
            return True
    return False


def is_bitmap(
    ttfont: TTFont,
) -> bool:
    """
    Determines if the given font is a bitmap font.
    """
    return _has_bitmap_tables(ttfont) and not _has_outlines(ttfont)

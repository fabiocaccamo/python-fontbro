from __future__ import annotations

import sys
from collections import Counter

from fontTools import unicodedata
from fontTools.ttLib import TTFont

from fontbro.unicode import get_best_cmap

# same criteria used by Fontbakery (glyph_metrics_stats condition):
# https://github.com/fonttools/fontbakery/blob/main/Lib/fontbakery/checks/conditions.py

# printable ascii characters (control characters are excluded)
_ASCII_CODEPOINTS: range = range(0x20, 0x7F)

# min ratio of printable ascii characters with glyph to check only their glyphs
_ASCII_COVERAGE_MIN: float = 0.8

# unicode categories of the characters checked if the font has no ascii coverage:
# letter, mark, number, punctuation, symbol and space separator
_CHARACTERS_CATEGORIES: tuple[str, ...] = ("L", "M", "N", "P", "S", "Zs")

# max number of different widths if the font has no ascii coverage,
# eg. cjk monospace fonts have half-width and full-width characters
_WIDTHS_COUNT_MAX: int = 2

# GDEF glyph class of mark glyphs
_GDEF_MARK_GLYPH_CLASS: int = 3


def _get_widths(
    ttfont: TTFont,
    glyphs_names: set[str],
) -> list[int]:
    """
    Gets the advance widths of the given glyphs, zero widths are ignored.
    """
    return [
        advance
        for glyph_name, (advance, _) in ttfont["hmtx"].metrics.items()
        if glyph_name in glyphs_names and advance != 0
    ]


def is_monospace(
    ttfont: TTFont,
    *,
    threshold: float = 0.8,
) -> bool:
    """
    Determines if the given font is a monospace font.
    """
    cmap = get_best_cmap(ttfont) or {}

    # fonts covering printable ascii characters: check only their glyphs
    ascii_codepoints = [
        codepoint for codepoint in _ASCII_CODEPOINTS if codepoint in cmap
    ]
    if len(ascii_codepoints) > len(_ASCII_CODEPOINTS) * _ASCII_COVERAGE_MIN:
        widths = _get_widths(
            ttfont, {cmap[codepoint] for codepoint in ascii_codepoints}
        )
        if not widths:
            return False
        same_width_count = Counter(widths).most_common(1)[0][1]
        return same_width_count >= len(widths) * threshold

    # fonts not covering printable ascii characters (eg. cjk, arabic...):
    # check the glyphs of the characters, excluding marks
    glyphs_names = {
        glyph_name
        for codepoint, glyph_name in cmap.items()
        # malformed cmaps can contain codepoints out of the unicode range
        if codepoint <= sys.maxunicode
        and unicodedata.category(chr(codepoint)).startswith(_CHARACTERS_CATEGORIES)
    }
    gdef = ttfont.get("GDEF")
    if gdef and gdef.table.GlyphClassDef:
        glyphs_names -= {
            glyph_name
            for glyph_name, glyph_class in gdef.table.GlyphClassDef.classDefs.items()
            if glyph_class == _GDEF_MARK_GLYPH_CLASS
        }
    distinct_widths = set(_get_widths(ttfont, glyphs_names))
    return 0 < len(distinct_widths) <= _WIDTHS_COUNT_MAX

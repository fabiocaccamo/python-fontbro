from __future__ import annotations

from fontTools.ttLib import TTFont


def is_color(
    ttfont: TTFont,
) -> bool:
    """
    Determines if the given font is a color font.
    """
    color_tables_tags = {"COLR", "CPAL", "CBDT", "CBLC", "SVG ", "sbix"}
    for tag in color_tables_tags:
        if tag in ttfont:
            return True
    return False

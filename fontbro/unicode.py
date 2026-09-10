from __future__ import annotations

from fontTools.ttLib import TTFont

from fontbro.exceptions import DataError


def get_best_cmap(
    ttfont: TTFont,
) -> dict[int, str] | None:
    """
    Gets the 'best' unicode cmap dict (codepoint -> glyph name) of the given font,
    None is returned if the font has no cmap table or no unicode cmap subtable.
    """
    cmap_table = ttfont.get("cmap")
    cmap: dict[int, str] | None = cmap_table.getBestCmap() if cmap_table else None
    return cmap


def get_best_cmap_or_raise(
    ttfont: TTFont,
) -> dict[int, str]:
    """
    Gets the 'best' unicode cmap dict (codepoint -> glyph name) of the given font,
    DataError is raised if the font has no cmap table or no unicode cmap subtable.
    """
    cmap = get_best_cmap(ttfont)
    if cmap is None:
        raise DataError("Unable to find the 'best' unicode cmap dict.")
    return cmap

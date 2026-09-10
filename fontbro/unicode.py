from __future__ import annotations

import copy
from collections.abc import Generator
from typing import Any

from fontTools import unicodedata
from fontTools.ttLib import TTFont

from fontbro.exceptions import DataError
from fontbro.glyphs import is_glyph_blank
from fontbro.utils import read_json, slugify

# Unicode blocks/scripts data:
_UNICODE_BLOCKS: list[dict[str, Any]] = read_json("data/unicode-blocks.json")
_UNICODE_SCRIPTS: list[dict[str, Any]] = read_json("data/unicode-scripts.json")


def _populate_unicode_items_set(
    items: list[dict[str, Any]],
    items_cache: dict[str, Any],
    item: dict[str, Any],
) -> None:
    item_key = item["name"]
    if item_key not in items_cache:
        item = item.copy()
        item["characters_count"] = 0
        items_cache[item_key] = item
        items.append(item)
    item = items_cache[item_key]
    item["characters_count"] += 1


def _get_unicode_items_set_with_coverage(
    all_items: list[dict[str, Any]],
    items: list[dict[str, Any]],
    *,
    coverage_threshold: float = 0.0,
) -> list[dict[str, Any]]:
    all_items = copy.deepcopy(all_items)
    items_indexed = {item["name"]: item.copy() for item in items}
    for item in all_items:
        item_key = item["name"]
        if item_key in items_indexed:
            item["characters_count"] = items_indexed[item_key]["characters_count"]
            item["coverage"] = item["characters_count"] / item["characters_total"]
        else:
            item["characters_count"] = 0
            item["coverage"] = 0.0
    items_filtered = [
        item for item in all_items if item["coverage"] >= coverage_threshold
    ]
    # items_filtered.sort(key=lambda item: item['name'])
    return items_filtered


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


def get_characters(
    ttfont: TTFont,
    *,
    ignore_blank: bool = False,
) -> Generator[dict[str, Any]]:
    """
    Gets the characters of the given font.
    """
    cmap = get_best_cmap_or_raise(ttfont)
    glyphset = ttfont.getGlyphSet() if ignore_blank else None
    for code, char_name in cmap.items():
        code_hex = f"{code:04X}"
        if 0 <= code < 0x110000:
            char = chr(code)
        else:
            continue
        # check if is control character
        char_code = ord(char)
        if char_code < 0x20 or char_code == 0x7F:
            continue
        if (
            glyphset is not None
            and char_name in glyphset
            and is_glyph_blank(glyphset, char_name)
        ):
            continue
        unicode_name = unicodedata.name(char, None)
        unicode_block_name = unicodedata.block(code)
        unicode_script_tag = unicodedata.script(code)
        unicode_script_name = unicodedata.script_name(unicode_script_tag)
        yield {
            "character": char,
            "character_name": char_name,
            "code": code,
            "escape_sequence": f"\\u{code_hex}",
            "html_code": f"&#{code};",
            "unicode": f"U+{code_hex}",
            "unicode_code": code,
            "unicode_name": unicode_name,
            "unicode_block_name": unicode_block_name,
            "unicode_script_name": unicode_script_name,
            "unicode_script_tag": unicode_script_tag,
        }


def get_characters_count(
    ttfont: TTFont,
    *,
    ignore_blank: bool = False,
) -> int:
    """
    Gets the characters count of the given font.
    """
    return len(list(get_characters(ttfont, ignore_blank=ignore_blank)))


def get_unicode_block_by_name(
    ttfont: TTFont,
    name: str,
) -> dict[str, Any] | None:
    """
    Gets the unicode block of the given font by name
    (name is case-insensitive and ignores "-").
    """
    blocks = get_unicode_blocks(ttfont, coverage_threshold=0.0)
    for block in blocks:
        if slugify(name) == slugify(block["name"]):
            return block
    # raise KeyError("Invalid unicode block name: '{name}'")
    return None


def get_unicode_blocks(
    ttfont: TTFont,
    *,
    coverage_threshold: float = 0.00001,
) -> list[dict[str, Any]]:
    """
    Gets the unicode blocks of the given font and their coverage.
    """
    items: list[dict[str, Any]] = []
    items_cache: dict[str, Any] = {}
    for char in get_characters(ttfont):
        item = {
            "name": char["unicode_block_name"],
        }
        _populate_unicode_items_set(items, items_cache, item)
    blocks = _get_unicode_items_set_with_coverage(
        _UNICODE_BLOCKS, items, coverage_threshold=coverage_threshold
    )
    return blocks


def get_unicode_script_by_name(
    ttfont: TTFont,
    name: str,
) -> dict[str, Any] | None:
    """
    Gets the unicode script of the given font by name/tag
    (name/tag is case-insensitive and ignores "-").
    """
    scripts = get_unicode_scripts(ttfont, coverage_threshold=0.0)
    for script in scripts:
        if slugify(name) in (slugify(script["name"]), slugify(script["tag"])):
            return script
    # raise KeyError("Invalid unicode script name/tag: '{name}'")
    return None


def get_unicode_scripts(
    ttfont: TTFont,
    *,
    coverage_threshold: float = 0.00001,
) -> list[dict[str, Any]]:
    """
    Gets the unicode scripts of the given font and their coverage.
    """
    items: list[dict[str, Any]] = []
    items_cache: dict[str, Any] = {}
    for char in get_characters(ttfont):
        item = {
            "name": char["unicode_script_name"],
            "tag": char["unicode_script_tag"],
        }
        _populate_unicode_items_set(items, items_cache, item)
    scripts = _get_unicode_items_set_with_coverage(
        _UNICODE_SCRIPTS, items, coverage_threshold=coverage_threshold
    )
    return scripts

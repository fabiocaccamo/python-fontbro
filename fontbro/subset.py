from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any

from fontTools.subset import Options as SubsetterOptions
from fontTools.subset import Subsetter
from fontTools.subset import parse_unicodes as _parse_unicodes
from fontTools.ttLib import TTFont

from fontbro.exceptions import ArgumentError


def parse_unicodes(
    unicodes: Iterable[int | str] | str,
) -> list[int]:
    if isinstance(unicodes, (list, set, tuple)):
        # convert possible int codepoints to hex str
        unicodes_list = list(unicodes)
        for index, code in enumerate(unicodes_list):
            unicodes_list[index] = f"{code:04X}" if isinstance(code, int) else code
        unicodes_str = ",".join(list(set(unicodes_list)))
    elif isinstance(unicodes, str):
        unicodes_str = unicodes
    else:
        raise ValueError("Invalid 'unicodes' value.")
    assert isinstance(unicodes_str, str)
    # replace possible — ‐ − (&mdash; &dash; &minus;) with -
    unicodes_str = re.sub(r"[\—\‐\−]", "-", unicodes_str)
    # remove U+, \u, u if present
    unicodes_str = re.sub(r"(U\+)|(\\u)|(u)", "", unicodes_str, flags=re.I)
    unicodes_list = list(_parse_unicodes(unicodes_str))
    return unicodes_list


def subset(
    ttfont: TTFont,
    *,
    unicodes: list[str | int] | str = "",
    glyphs: list[str] | None = None,
    text: str = "",
    **options: Any,
) -> None:
    """
    Subsets the given font using the given options (unicodes or glyphs or text),
    it is possible to pass also subsetter options.
    """
    if not any([unicodes, glyphs, text]):
        raise ArgumentError(
            "Subsetting requires at least one of "
            "the following args: unicode, glyphs, text."
        )
    unicodes_list = parse_unicodes(unicodes)
    glyphs_list = glyphs or []
    options.setdefault("glyph_names", True)
    options.setdefault("ignore_missing_glyphs", True)
    options.setdefault("ignore_missing_unicodes", True)
    options.setdefault("layout_features", ["*"])
    options.setdefault("name_IDs", "*")
    options.setdefault("notdef_outline", True)
    subs_args = {
        "unicodes": unicodes_list,
        "glyphs": glyphs_list,
        "text": text,
    }
    # https://github.com/fonttools/fonttools/blob/main/Lib/fontTools/subset/__init__.py
    subs_options = SubsetterOptions(**options)
    subs = Subsetter(options=subs_options)
    subs.populate(**subs_args)
    subs.subset(ttfont)

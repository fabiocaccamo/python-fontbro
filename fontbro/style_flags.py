from __future__ import annotations

from typing import Any

from fontTools.ttLib import TTFont

from fontbro.exceptions import ArgumentError
from fontbro.flags import get_flag, set_flag
from fontbro.names import NAME_SUBFAMILY_NAME, get_name

# Style Flags:
# https://docs.microsoft.com/en-us/typography/opentype/spec/head
# https://docs.microsoft.com/en-us/typography/opentype/spec/os2#fsselection
STYLE_FLAG_REGULAR: str = "regular"
STYLE_FLAG_BOLD: str = "bold"
STYLE_FLAG_ITALIC: str = "italic"
STYLE_FLAG_UNDERLINE: str = "underline"
STYLE_FLAG_OUTLINE: str = "outline"
STYLE_FLAG_SHADOW: str = "shadow"
STYLE_FLAG_CONDENSED: str = "condensed"
STYLE_FLAG_EXTENDED: str = "extended"
_STYLE_FLAGS: dict[str, dict[str, Any]] = {
    STYLE_FLAG_REGULAR: {"bit_head_mac": None, "bit_os2_fs": 6},
    STYLE_FLAG_BOLD: {"bit_head_mac": 0, "bit_os2_fs": 5},
    STYLE_FLAG_ITALIC: {"bit_head_mac": 1, "bit_os2_fs": 0},
    STYLE_FLAG_UNDERLINE: {"bit_head_mac": 2, "bit_os2_fs": 1},
    STYLE_FLAG_OUTLINE: {"bit_head_mac": 3, "bit_os2_fs": 3},
    STYLE_FLAG_SHADOW: {"bit_head_mac": 4, "bit_os2_fs": None},
    STYLE_FLAG_CONDENSED: {"bit_head_mac": 5, "bit_os2_fs": None},
    STYLE_FLAG_EXTENDED: {"bit_head_mac": 6, "bit_os2_fs": None},
}
_STYLE_FLAGS_KEYS: list[str] = list(_STYLE_FLAGS.keys())


def get_style_flag(
    ttfont: TTFont,
    key: str,
) -> bool:
    """
    Gets the style flag of the given font reading OS/2 and macStyle tables.
    """
    bits = _STYLE_FLAGS[key]
    bit_os2_fs = bits["bit_os2_fs"]
    bit_head_mac = bits["bit_head_mac"]
    # https://docs.microsoft.com/en-us/typography/opentype/spec/os2#fsselection
    flag_os2_fs = False
    if bit_os2_fs is not None:
        os2 = ttfont.get("OS/2")
        if os2:
            flag_os2_fs = get_flag(os2.fsSelection, bit_os2_fs)
    # https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6head.html
    flag_head_mac = False
    if bit_head_mac is not None:
        head = ttfont.get("head")
        if head:
            flag_head_mac = get_flag(head.macStyle, bit_head_mac)
    return flag_os2_fs or flag_head_mac


def get_style_flags(
    ttfont: TTFont,
) -> dict[str, bool]:
    """
    Gets the style flags of the given font reading OS/2 and macStyle tables.
    """
    return {key: get_style_flag(ttfont, key) for key in _STYLE_FLAGS_KEYS}


def set_style_flag(
    ttfont: TTFont,
    key: str,
    value: bool,
) -> None:
    """
    Sets the style flag of the given font in OS/2 and macStyle tables.
    """
    bits = _STYLE_FLAGS[key]
    bit_os2_fs = bits["bit_os2_fs"]
    bit_head_mac = bits["bit_head_mac"]
    if bit_os2_fs is not None:
        os2 = ttfont.get("OS/2")
        if os2:
            os2.fsSelection = set_flag(os2.fsSelection, bit_os2_fs, value)
    if bit_head_mac is not None:
        head = ttfont.get("head")
        if head:
            head.macStyle = set_flag(head.macStyle, bit_head_mac, value)


def set_style_flags(
    ttfont: TTFont,
    *,
    regular: bool | None = None,
    bold: bool | None = None,
    italic: bool | None = None,
    underline: bool | None = None,
    outline: bool | None = None,
    shadow: bool | None = None,
    condensed: bool | None = None,
    extended: bool | None = None,
) -> None:
    """
    Sets the style flags of the given font, keys set to None will be ignored.
    """
    flags = {
        "regular": regular,
        "bold": bold,
        "italic": italic,
        "underline": underline,
        "outline": outline,
        "shadow": shadow,
        "condensed": condensed,
        "extended": extended,
    }
    # validate all values before setting any flag
    for key, value in flags.items():
        if value is not None and not isinstance(value, bool):
            raise ArgumentError(
                f"Invalid '{key}' value, expected bool or None, got {value!r}."
            )
    for key, value in flags.items():
        if value is not None:
            set_style_flag(ttfont, key, value)


def set_style_flags_by_subfamily_name(
    ttfont: TTFont,
) -> None:
    """
    Sets the style flags of the given font by the subfamily name value.
    """
    subfamily_name = (get_name(ttfont, NAME_SUBFAMILY_NAME) or "").lower()
    if subfamily_name == STYLE_FLAG_REGULAR:
        set_style_flags(ttfont, regular=True, bold=False, italic=False)
    elif subfamily_name == STYLE_FLAG_BOLD:
        set_style_flags(ttfont, regular=False, bold=True, italic=False)
    elif subfamily_name == STYLE_FLAG_ITALIC:
        set_style_flags(ttfont, regular=False, bold=False, italic=True)
    elif subfamily_name == f"{STYLE_FLAG_BOLD} {STYLE_FLAG_ITALIC}":
        set_style_flags(ttfont, regular=False, bold=True, italic=True)

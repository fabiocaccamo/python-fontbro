from __future__ import annotations

import re
from typing import Any

from fontTools.misc.encodingTools import getEncoding
from fontTools.ttLib import TTFont

from fontbro.exceptions import ArgumentError
from fontbro.utils import concat_names, remove_spaces

# Names:
NAME_COPYRIGHT_NOTICE: str = "copyright_notice"
NAME_FAMILY_NAME: str = "family_name"
NAME_SUBFAMILY_NAME: str = "subfamily_name"
NAME_UNIQUE_IDENTIFIER: str = "unique_identifier"
NAME_FULL_NAME: str = "full_name"
NAME_VERSION: str = "version"
NAME_POSTSCRIPT_NAME: str = "postscript_name"
NAME_TRADEMARK: str = "trademark"
NAME_MANUFACTURER_NAME: str = "manufacturer_name"
NAME_DESIGNER: str = "designer"
NAME_DESCRIPTION: str = "description"
NAME_VENDOR_URL: str = "vendor_url"
NAME_DESIGNER_URL: str = "designer_url"
NAME_LICENSE_DESCRIPTION: str = "license_description"
NAME_LICENSE_INFO_URL: str = "license_info_url"
NAME_RESERVED: str = "reserved"
NAME_TYPOGRAPHIC_FAMILY_NAME: str = "typographic_family_name"
NAME_TYPOGRAPHIC_SUBFAMILY_NAME: str = "typographic_subfamily_name"
NAME_COMPATIBLE_FULL: str = "compatible_full"
NAME_SAMPLE_TEXT: str = "sample_text"
NAME_POSTSCRIPT_CID_FINDFONT_NAME: str = "postscript_cid_findfont_name"
NAME_WWS_FAMILY_NAME: str = "wws_family_name"
NAME_WWS_SUBFAMILY_NAME: str = "wws_subfamily_name"
NAME_LIGHT_BACKGROUND_PALETTE: str = "light_background_palette"
NAME_DARK_BACKGROUND_PALETTE: str = "dark_background_palette"
NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX: str = "variations_postscript_name_prefix"

_NAMES: list[dict[str, Any]] = [
    {"id": 0, "key": NAME_COPYRIGHT_NOTICE},
    {"id": 1, "key": NAME_FAMILY_NAME},
    {"id": 2, "key": NAME_SUBFAMILY_NAME},
    {"id": 3, "key": NAME_UNIQUE_IDENTIFIER},
    {"id": 4, "key": NAME_FULL_NAME},
    {"id": 5, "key": NAME_VERSION},
    {"id": 6, "key": NAME_POSTSCRIPT_NAME},
    {"id": 7, "key": NAME_TRADEMARK},
    {"id": 8, "key": NAME_MANUFACTURER_NAME},
    {"id": 9, "key": NAME_DESIGNER},
    {"id": 10, "key": NAME_DESCRIPTION},
    {"id": 11, "key": NAME_VENDOR_URL},
    {"id": 12, "key": NAME_DESIGNER_URL},
    {"id": 13, "key": NAME_LICENSE_DESCRIPTION},
    {"id": 14, "key": NAME_LICENSE_INFO_URL},
    {"id": 15, "key": NAME_RESERVED},
    {"id": 16, "key": NAME_TYPOGRAPHIC_FAMILY_NAME},
    {"id": 17, "key": NAME_TYPOGRAPHIC_SUBFAMILY_NAME},
    {"id": 18, "key": NAME_COMPATIBLE_FULL},
    {"id": 19, "key": NAME_SAMPLE_TEXT},
    {"id": 20, "key": NAME_POSTSCRIPT_CID_FINDFONT_NAME},
    {"id": 21, "key": NAME_WWS_FAMILY_NAME},
    {"id": 22, "key": NAME_WWS_SUBFAMILY_NAME},
    {"id": 23, "key": NAME_LIGHT_BACKGROUND_PALETTE},
    {"id": 24, "key": NAME_DARK_BACKGROUND_PALETTE},
    {"id": 25, "key": NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX},
]
_NAMES_BY_ID: dict[int, dict[str, Any]] = {item["id"]: item for item in _NAMES}
_NAMES_BY_KEY: dict[str, dict[str, Any]] = {item["key"]: item for item in _NAMES}
# https://learn.microsoft.com/en-us/typography/opentype/spec/name#platform-ids
# windows: platform 3, encoding 1 (unicode bmp), language 0x409 (english)
_NAMES_WIN_IDS: dict[str, Any] = {"platformID": 3, "platEncID": 1, "langID": 0x409}
# macintosh: platform 1, encoding 0 (roman), language 0 (english)
_NAMES_MAC_IDS: dict[str, Any] = {"platformID": 1, "platEncID": 0, "langID": 0x0}


def _get_name_id(
    key: int | str,
) -> int:
    if isinstance(key, int):
        return key
    elif isinstance(key, str):
        return int(_NAMES_BY_KEY[key]["id"])
    else:
        key_type = type(key).__name__
        raise ArgumentError(
            f"Invalid key type, expected int or str, found '{key_type}'."
        )


def _is_encodable(
    value: str,
    platform_ids: dict[str, Any],
) -> bool:
    """
    Determines if the value can be encoded with the encoding
    of the name records with the given platform ids.
    """
    encoding = getEncoding(
        platform_ids["platformID"],
        platform_ids["platEncID"],
        platform_ids["langID"],
    )
    try:
        value.encode(encoding)
    except UnicodeEncodeError:
        return False
    return True


def get_name(
    ttfont: TTFont,
    key: int | str,
) -> str | None:
    """
    Gets the name by its identifier from the name table of the given font.
    """
    name_id = _get_name_id(key)
    name_table = ttfont["name"]
    name = name_table.getName(name_id, **_NAMES_WIN_IDS)
    if not name:
        name = name_table.getName(name_id, **_NAMES_MAC_IDS)
    return str(name.toUnicode()) if name else None


def get_names(
    ttfont: TTFont,
) -> dict[str, Any]:
    """
    Gets the names records of the given font mapped by their property name.
    """
    names_by_id = {record.nameID: f"{record}" for record in ttfont["name"].names}
    names = {
        _NAMES_BY_ID[name_id]["key"]: value
        for name_id, value in names_by_id.items()
        if name_id in _NAMES_BY_ID
    }
    return names


def set_name(
    ttfont: TTFont,
    key: int | str,
    value: str,
) -> None:
    """
    Sets the name by its identifier in the name table of the given font.
    """
    name_id = _get_name_id(key)
    name_table = ttfont["name"]
    # https://github.com/fonttools/fonttools/blob/main/Lib/fontTools/ttLib/tables/_n_a_m_e.py#L568
    name_table.setName(value, name_id, **_NAMES_WIN_IDS)
    # the mac roman encoding can't encode many characters (eg. greek, cyrillic, cjk),
    # in that case the mac name record is removed (as fontTools addMultilingualName
    # does), otherwise the font would raise UnicodeEncodeError when saved
    if _is_encodable(value, _NAMES_MAC_IDS):
        name_table.setName(value, name_id, **_NAMES_MAC_IDS)
    else:
        name_table.removeNames(nameID=name_id, **_NAMES_MAC_IDS)


def set_names(
    ttfont: TTFont,
    names: dict[str, str],
) -> None:
    """
    Sets the names by their identifier in the name table of the given font.
    """
    for key, value in names.items():
        set_name(ttfont, key, value)


def get_family_name(
    ttfont: TTFont,
) -> str:
    """
    Gets the family name of the given font reading the name records
    with priority order (16, 21, 1).
    """
    return (
        get_name(ttfont, NAME_TYPOGRAPHIC_FAMILY_NAME)
        or get_name(ttfont, NAME_WWS_FAMILY_NAME)
        or get_name(ttfont, NAME_FAMILY_NAME)
        or ""
    )


def get_style_name(
    ttfont: TTFont,
) -> str:
    """
    Gets the style name of the given font reading the name records
    with priority order (17, 22, 2).
    """
    return (
        get_name(ttfont, NAME_TYPOGRAPHIC_SUBFAMILY_NAME)
        or get_name(ttfont, NAME_WWS_SUBFAMILY_NAME)
        or get_name(ttfont, NAME_SUBFAMILY_NAME)
        or ""
    )


def rename(
    ttfont: TTFont,
    *,
    family_name: str = "",
    style_name: str = "",
) -> None:
    """
    Renames the names records (1, 2, 3, 4, 6, 16, 17, 21, 22) of the given font
    according to the given family_name and style_name (subfamily_name),
    if not defined they will be auto-detected.
    """
    family_name = (family_name or "").strip() or get_family_name(ttfont)
    style_name = (style_name or "").strip() or get_style_name(ttfont)

    # typographic and wws names
    typographic_family_name = family_name
    typographic_subfamily_name = style_name
    wws_family_name = family_name
    wws_subfamily_name = style_name

    # family name and subfamily name
    subfamily_names = ["regular", "italic", "bold", "bold italic"]
    subfamily_name = style_name.lower()
    if subfamily_name not in subfamily_names:
        # fix legacy name records 1 and 2
        family_name_suffix = re.sub(r"\ italic$", "", style_name, flags=re.IGNORECASE)
        if family_name_suffix:
            family_name = f"{typographic_family_name} {family_name_suffix}"
        subfamily_name = subfamily_names["italic" in subfamily_name]
    subfamily_name = subfamily_name.title()

    # full name
    full_name = concat_names(typographic_family_name, typographic_subfamily_name)

    # postscript name
    postscript_name = concat_names(
        remove_spaces(typographic_family_name),
        remove_spaces(typographic_subfamily_name),
    )

    # keep only printable ASCII subset:
    # https://learn.microsoft.com/en-us/typography/opentype/spec/name#name-ids
    # postscript_name_allowed_chars = {chr(code) for code in range(33, 127)}
    # !"#$&'*+,-.0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\^_`abcdefghijklmnopqrstuvwxyz|~
    postscript_name_pattern = (
        r"[^0-9A-Za-z\!\"\#\$\&\'\*\+\,\-\.\:\;\=\?\@\\\^\_\`\|\~]"
    )
    postscript_name = re.sub(postscript_name_pattern, "-", postscript_name)
    postscript_name = re.sub(r"[\-]+", "-", postscript_name).strip("-")
    postscript_name_length = len(postscript_name)
    if postscript_name_length > 63:
        raise ArgumentError(
            "Computed PostScript name exceeded 63 characters max-length"
            f" ({postscript_name_length} characters)."
        )

    # update unique identifier
    postscript_name_old = get_name(ttfont, NAME_POSTSCRIPT_NAME) or ""
    unique_identifier = get_name(ttfont, NAME_UNIQUE_IDENTIFIER) or ""
    unique_identifier = unique_identifier.replace(
        postscript_name_old,
        postscript_name,
    )

    # update name records
    names = {
        NAME_FAMILY_NAME: family_name,
        NAME_SUBFAMILY_NAME: subfamily_name,
        NAME_UNIQUE_IDENTIFIER: unique_identifier,
        NAME_FULL_NAME: full_name,
        NAME_POSTSCRIPT_NAME: postscript_name,
        NAME_TYPOGRAPHIC_FAMILY_NAME: typographic_family_name,
        NAME_TYPOGRAPHIC_SUBFAMILY_NAME: typographic_subfamily_name,
        NAME_WWS_FAMILY_NAME: wws_family_name,
        NAME_WWS_SUBFAMILY_NAME: wws_subfamily_name,
    }
    set_names(ttfont, names)

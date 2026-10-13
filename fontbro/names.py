from __future__ import annotations

import re
from typing import Any

from fontTools.misc.encodingTools import getEncoding
from fontTools.ttLib import TTFont

from fontbro.exceptions import ArgumentError, VariableFontRequiredError
from fontbro.tables import get_table_or_raise
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
# unicode: platform 0, encoding 3 (unicode bmp), language 0 (no language)
_NAMES_UNI_IDS: dict[str, Any] = {"platformID": 0, "platEncID": 3, "langID": 0x0}


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
    if not encoding:
        # the encoding of the name records is unknown (eg. the macintosh
        # "uninterpreted" script), so the value cannot be written to them
        return False
    try:
        value.encode(encoding)
    except UnicodeEncodeError:
        return False
    return True


def _get_name_records_ids(
    name_table: Any,
    name_id: int,
    platform_ids: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Gets the ids of the existing name records with the given name id, matching
    the platform and the language of the given platform ids. The encoding is
    not matched: the same name id can have more than one record with different
    encodings (eg. a windows symbol record and a windows unicode one).
    Records in other languages are not matched, so they are never overwritten.
    """
    return [
        {
            "platformID": record.platformID,
            "platEncID": record.platEncID,
            "langID": record.langID,
        }
        for record in name_table.names
        if record.nameID == name_id
        and record.platformID == platform_ids["platformID"]
        and record.langID == platform_ids["langID"]
    ]


def get_name(
    ttfont: TTFont,
    key: int | str,
) -> str | None:
    """
    Gets the name by its identifier from the name table of the given font.
    """
    name_id = _get_name_id(key)
    name_table = ttfont.get("name")
    if not name_table:
        return None
    # the windows english record is preferred: mac records are legacy
    # and they can follow different naming conventions (eg. name id 1)
    name_record = name_table.getName(name_id, **_NAMES_WIN_IDS)
    if name_record:
        try:
            return str(name_record.toUnicode())
        except UnicodeDecodeError:
            pass
    # fallback to the english (mac) record or to any other decodable record
    name: str | None = name_table.getDebugName(name_id)
    return name


def get_names(
    ttfont: TTFont,
) -> dict[str, Any]:
    """
    Gets the names records of the given font mapped by their property name.
    """
    # read each name as get_name does, to get consistent values
    names = {}
    for name_id, name_item in _NAMES_BY_ID.items():
        name = get_name(ttfont, name_id)
        if name is not None:
            names[name_item["key"]] = name
    return names


def set_name(
    ttfont: TTFont,
    key: int | str,
    value: str,
    *,
    windows: bool = True,
    mac: bool = True,
    unicode: bool = True,
) -> None:
    """
    Sets the name by its identifier in the name table of the given font,
    only in the records of the platforms enabled by the windows, mac
    and unicode flags.
    """
    name_id = _get_name_id(key)
    name_table = get_table_or_raise(ttfont, "name")
    if windows:
        # https://github.com/fonttools/fonttools/blob/main/Lib/fontTools/ttLib/tables/_n_a_m_e.py#L568
        # the windows record is always written, it's the one read first by get_name
        name_table.setName(value, name_id, **_NAMES_WIN_IDS)
    # the other records of the same name id are updated only if the font
    # already has them (mac and unicode records are legacy, modern tools don't
    # produce them anymore, so they are never added): a record left with its
    # previous value would contradict the record just written
    platforms = [
        platform_ids
        for platform_ids, enabled in (
            (_NAMES_WIN_IDS, windows),
            (_NAMES_UNI_IDS, unicode),
            (_NAMES_MAC_IDS, mac),
        )
        if enabled
    ]
    for platform_ids in platforms:
        for record_ids in _get_name_records_ids(name_table, name_id, platform_ids):
            # the value is written only if the record encoding can encode it
            # (eg. mac roman can't encode greek, cyrillic, cjk), otherwise the
            # record is removed (as fontTools addMultilingualName does),
            # because the font would raise UnicodeEncodeError when saved
            if _is_encodable(value, record_ids):
                name_table.setName(value, name_id, **record_ids)
            else:
                name_table.removeNames(nameID=name_id, **record_ids)


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


def _get_postscript_name(
    value: str,
) -> str:
    """
    Gets a PostScript name from the given value,
    replacing the characters not allowed with hyphens.
    """
    # keep only printable ASCII subset:
    # https://learn.microsoft.com/en-us/typography/opentype/spec/name#name-ids
    # postscript_name_allowed_chars = {chr(code) for code in range(33, 127)}
    # !"#$&'*+,-.0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\^_`abcdefghijklmnopqrstuvwxyz|~
    postscript_name_pattern = (
        r"[^0-9A-Za-z\!\"\#\$\&\'\*\+\,\-\.\:\;\=\?\@\\\^\_\`\|\~]"
    )
    postscript_name = re.sub(postscript_name_pattern, "-", value)
    postscript_name = re.sub(r"[\-]+", "-", postscript_name).strip("-")
    return postscript_name


def _get_default_instance_style_name(
    ttfont: TTFont,
) -> str:
    """
    Gets the style name of the fvar named instance at the default coordinates.
    """
    fvar = ttfont["fvar"]
    coordinates = {axis.axisTag: axis.defaultValue for axis in fvar.axes}
    for instance in fvar.instances:
        if instance.coordinates == coordinates:
            return get_name(ttfont, instance.subfamilyNameID) or ""
    return ""


def rename_variable_instances(
    ttfont: TTFont,
    *,
    family_name: str = "",
    style_names: dict[str, str] | None = None,
) -> None:
    """
    Renames the named instances of the given variable font: the family_name
    replaces the family part of the instances PostScript names (and of the
    variations PostScript name prefix, 25), the style_names (old style name
    to new style name) replace the instances style names and the style part
    of their PostScript names. The axes names are unchanged.
    The default instance style name must match the font style name,
    so renaming it renames the font style too.
    """
    if "fvar" not in ttfont:
        raise VariableFontRequiredError(
            "Only the instances of a variable font can be renamed."
        )
    # style names are matched case-insensitively
    style_names = {key.lower(): value for key, value in (style_names or {}).items()}
    default_style_name = _get_default_instance_style_name(ttfont).lower()
    default_style_name_new = style_names.get(default_style_name, "")
    if default_style_name_new:
        rename(ttfont, style_name=default_style_name_new)
    family_name = (family_name or "").strip() or get_family_name(ttfont)
    _rename_variable_instances(ttfont, family_name, style_names)


def _get_instance_postscript_name(
    prefix: str,
    style_name: str,
) -> str:
    """
    Gets the PostScript name of a variable font named instance, the "Italic"
    style suffix is omitted if the prefix already ends with it
    (eg. "TourneyItalic-Thin" instead of "TourneyItalic-ThinItalic").
    """
    style_name = remove_spaces(style_name)
    if prefix.lower().endswith("italic"):
        style_name = re.sub(r"italic$", "", style_name, flags=re.IGNORECASE)
        style_name = style_name or "Regular"
    return _get_postscript_name(f"{prefix}-{style_name}")


def _rename_variable_instances(
    ttfont: TTFont,
    family_name: str,
    style_names: dict[str, str],
) -> None:
    """
    Renames the named instances of the given variable font,
    the style_names keys must be lowercase.
    """
    name_table = ttfont["name"]

    # the old family name is read before updating it (rename calls this function
    # before updating the name records), the old prefixes are computed from it
    family_name_old = get_family_name(ttfont)
    prefix_old = get_name(ttfont, NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX) or ""
    if prefix_old:
        # variations postscript name prefix: only ASCII letters and digits allowed,
        # its suffix is kept (eg. "Roman", "Italic") to avoid the same instances
        # postscript names in the roman and italic fonts
        suffix = ""
        family_name_old_prefix = re.sub(r"[^0-9A-Za-z]", "", family_name_old)
        if family_name_old_prefix and prefix_old.startswith(family_name_old_prefix):
            suffix = prefix_old[len(family_name_old_prefix) :]
        elif "italic" in get_style_name(ttfont).lower() and not (
            family_name.lower().endswith("italic")
        ):
            suffix = "Italic"
        prefix = re.sub(r"[^0-9A-Za-z]", "", f"{family_name}{suffix}")
        # the windows record is written only if the font already has it
        name_id = _get_name_id(NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX)
        windows = bool(name_table.getName(name_id, **_NAMES_WIN_IDS))
        set_name(
            ttfont, NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX, prefix, windows=windows
        )
    else:
        prefix_old = _get_postscript_name(remove_spaces(family_name_old))
        prefix = _get_postscript_name(remove_spaces(family_name))

    # the style names are read before updating them,
    # because the same name record can be shared by more instances
    instances = ttfont["fvar"].instances
    instances_style_names = [
        get_name(ttfont, instance.subfamilyNameID) or "" for instance in instances
    ]
    for instance, style_name in zip(instances, instances_style_names, strict=True):
        style_name_new = style_names.get(style_name.lower(), "")
        if style_name_new and instance.subfamilyNameID < 256:
            # name ids 2 and 17 are the font style names (updated by rename),
            # so a new name record is added for the instance
            instance.subfamilyNameID = name_table.addName(
                style_name_new, platforms=((3, 1, 0x409),)
            )
        elif style_name_new:
            # the existing name record is updated, also where it is shared
            # (eg. the STAT table axis values), the windows record is written
            # only if the font already has it
            name_id = instance.subfamilyNameID
            windows = bool(name_table.getName(name_id, **_NAMES_WIN_IDS))
            set_name(ttfont, name_id, style_name_new, windows=windows)
        name_id = instance.postscriptNameID
        name = get_name(ttfont, name_id) if 255 < name_id < 0xFFFF else None
        if not name:
            continue
        if not style_name_new and prefix_old and name.startswith(prefix_old):
            # only the prefix is replaced, to keep the font naming convention
            name = prefix + name[len(prefix_old) :]
        else:
            # the name is generated if the style is renamed,
            # or if it doesn't start with the old prefix (inconsistent font)
            name = _get_instance_postscript_name(prefix, style_name_new or style_name)
        set_name(ttfont, name_id, name)


def _rename_cff(
    ttfont: TTFont,
    postscript_name: str,
    full_name: str,
    family_name: str,
    weight: str,
) -> None:
    """
    Renames the CFF table names (otf fonts): the font name and the FDArray
    font names (CID-keyed fonts) prefixed by it, FullName, FamilyName and
    Weight (only if not empty) only if already defined.
    """
    if "CFF " not in ttfont:
        return
    cff = ttfont["CFF "].cff
    postscript_name_old = cff.fontNames[0]
    cff.fontNames[0] = postscript_name
    top_dict = cff.topDictIndex[0]
    for font_dict in getattr(top_dict, "FDArray", []):
        font_name = getattr(font_dict, "FontName", None)
        if font_name and font_name.startswith(postscript_name_old):
            font_dict.FontName = postscript_name + font_name[len(postscript_name_old) :]
    if getattr(top_dict, "FullName", None):
        top_dict.FullName = full_name
    if getattr(top_dict, "FamilyName", None):
        top_dict.FamilyName = family_name
    if weight and getattr(top_dict, "Weight", None):
        top_dict.Weight = weight


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
    The records 18 and 25, the fvar instances PostScript names and the CFF
    names are updated only if already defined.
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

    postscript_name = _get_postscript_name(postscript_name)
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

    # compatible full name: if it's not the full name (eg. a designer-defined
    # short menu name), only the family name in it is replaced
    compatible_full_name = get_name(ttfont, NAME_COMPATIBLE_FULL) or ""
    if compatible_full_name:
        family_name_old = get_family_name(ttfont)
        full_name_old = concat_names(family_name_old, get_style_name(ttfont))
        if (
            compatible_full_name == full_name_old
            or not family_name_old
            or family_name_old not in compatible_full_name
        ):
            compatible_full_name = full_name
        else:
            compatible_full_name = compatible_full_name.replace(
                family_name_old, typographic_family_name, 1
            )

    # cff weight (eg. "Bold" for "Bold Italic"), updated only if the style changes
    style_name_old = get_style_name(ttfont)
    weight = ""
    if style_name_old != typographic_subfamily_name:
        weight = re.sub(
            r"\s*italic$", "", typographic_subfamily_name, flags=re.IGNORECASE
        )
        weight = weight or "Regular"

    # fvar instances (and name id 25) need the old postscript name
    if "fvar" in ttfont:
        # the default instance style name must match the font style name, it's
        # renamed only if it matches the old one (otherwise a family rename of
        # an inconsistent font would rename it, and the STAT values sharing it)
        style_names = {}
        if (
            style_name_old != typographic_subfamily_name
            and _get_default_instance_style_name(ttfont) == style_name_old
        ):
            style_names[style_name_old.lower()] = typographic_subfamily_name
        _rename_variable_instances(ttfont, typographic_family_name, style_names)

    set_names(ttfont, names)
    # name id 18 (macintosh only) is updated only if already defined,
    # the windows record is written only if the font already has it
    if compatible_full_name:
        name_id = _get_name_id(NAME_COMPATIBLE_FULL)
        windows = bool(ttfont["name"].getName(name_id, **_NAMES_WIN_IDS))
        set_name(ttfont, NAME_COMPATIBLE_FULL, compatible_full_name, windows=windows)

    _rename_cff(ttfont, postscript_name, full_name, typographic_family_name, weight)

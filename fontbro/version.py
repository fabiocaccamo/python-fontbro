from __future__ import annotations

import re
from typing import Any

from fontTools.misc.fixedTools import fixedToStr, floatToFixed
from fontTools.ttLib import TTFont

from fontbro import names as _names
from fontbro.exceptions import ArgumentError

# the version name record conventionally starts with the version value,
# optionally prefixed by "Version" or "v", and it can be followed by
# extra info, eg. "Version 3.019;git-0a5106e0b"
# https://learn.microsoft.com/en-us/typography/opentype/spec/name#name-ids
_VERSION_PATTERN: re.Pattern[str] = re.compile(
    r"^(?:version|v\.?)?[\s\:]*(\d+)\.(\d+)",
    flags=re.IGNORECASE,
)

# head.fontRevision is a 16.16 fixed-point value
_VERSION_PRECISION_BITS: int = 16


def _get_version_str(
    version: float,
) -> str:
    """
    Gets the shortest decimal representation of the given version value
    that converts back to the same head.fontRevision fixed-point value.
    """
    version_fixed = floatToFixed(version, precisionBits=_VERSION_PRECISION_BITS)
    return str(fixedToStr(version_fixed, precisionBits=_VERSION_PRECISION_BITS))


def normalize_version(
    version: float,
) -> float:
    """
    Normalizes the given version value to the shortest decimal representation
    that converts back to the same head.fontRevision fixed-point value,
    eg. 1.0149993896484375 -> 1.015 (both are stored as 66519 in the head table).
    """
    return float(_get_version_str(version))


def format_version(
    version: float,
    *,
    prefix: str = "v",
) -> str:
    """
    Formats the given version value using the version name record convention,
    with the given prefix and a minimum of 3 decimal digits, eg. 1.1 -> "v1.100".
    More decimal digits are kept if the value needs them, eg. 1.0001 -> "v1.0001".
    """
    major, _, minor = _get_version_str(version).partition(".")
    minor = minor.ljust(3, "0")
    return f"{prefix}{major}.{minor}"


def parse_version(
    value: str | None,
) -> float:
    """
    Parses the version value from the given version name record value,
    eg. "Version 1.015;git-0a5106e0b" -> 1.015.
    The value is matched from the beginning of the string to avoid reading
    unrelated numbers (eg. a date or a tool version).
    Returns 0.0 if the value cannot be parsed.
    """
    match = _VERSION_PATTERN.match((value or "").strip())
    if not match:
        return 0.0
    version = float(f"{match[1]}.{match[2]}")
    return normalize_version(version)


def get_version(
    ttfont: TTFont,
    *,
    use_head_revision: bool = True,
    use_name_record: bool = True,
) -> float:
    """
    Gets the version of the given font reading it from head.fontRevision,
    with fallback on the version name record (name id 5) parsed value.
    The value is normalized to its shortest decimal representation,
    so that it doesn't depend on the source it has been read from.
    """
    if not use_head_revision and not use_name_record:
        raise ArgumentError(
            "Invalid arguments: at least one of 'use_head_revision' "
            "and 'use_name_record' options must be True."
        )
    if use_head_revision:
        # the head table is read only if the font has it
        head = ttfont.get("head")
        if head is not None:
            # fontRevision is 0.0 when it has not been set
            version = float(getattr(head, "fontRevision", None) or 0.0)
            if version > 0:
                return normalize_version(version)
    if use_name_record:
        version = parse_version(_names.get_name(ttfont, _names.NAME_VERSION))
        if version > 0:
            return version
    return 0.0


def get_version_formatted(
    ttfont: TTFont,
    *,
    use_head_revision: bool = True,
    use_name_record: bool = True,
    prefix: str = "v",
) -> str:
    """
    Gets the formatted version of the given font, eg. "v1.015".
    """
    version = get_version(
        ttfont,
        use_head_revision=use_head_revision,
        use_name_record=use_name_record,
    )
    return format_version(version, prefix=prefix)


def _get_cff_top_dict(
    ttfont: TTFont,
) -> Any | None:
    """
    Gets the CFF top dict of the given font, None if the font has no CFF table,
    or if its CFF holds no font, or if it holds more than one font (eg. in a
    font collection) and the one matching the font postscript name is not found.
    """
    cff_table = ttfont.get("CFF ")
    if cff_table is None:
        return None
    cff = cff_table.cff
    font_names = list(cff.fontNames)
    if len(font_names) == 1:
        font_index = 0
    else:
        # a cff can hold more than one font, in that case the font is looked up
        # by its postscript name, to avoid writing to the wrong one
        postscript_name = _names.get_name(ttfont, _names.NAME_POSTSCRIPT_NAME) or ""
        if postscript_name not in font_names:
            return None
        font_index = font_names.index(postscript_name)
    top_dict_index = cff.topDictIndex
    if font_index >= len(top_dict_index):
        return None
    return top_dict_index[font_index]


def _format_cff_version(
    version: float,
) -> str:
    """
    Formats the given version value using the CFF top dict convention,
    eg. 1.015 -> "001.015".
    """
    major, _, minor = format_version(version, prefix="").partition(".")
    return f"{int(major):03d}.{minor}"


def set_version(
    ttfont: TTFont,
    version: float | str,
) -> None:
    """
    Sets the version of the given font, the version value can be a number
    (eg. 1.015) or a version string (eg. "Version 1.015"), parsed the same
    way the version name record value is parsed when read.
    The head.fontRevision and the version name record (name id 5) are updated,
    the latter is overwritten with the canonical "Version X.YYY" form
    (any extra info it contained is dropped).
    The unique identifier name record (name id 3) is updated only if its first
    ";" separated part holds the current version value, and only in that part.
    The CFF version is updated only if the font already has it.
    Each value is written only if the font has the table holding it.
    """
    if isinstance(version, str):
        # a version string is parsed as the version name record value
        version_value = parse_version(version)
    elif isinstance(version, (int, float)):
        version_value = float(version)
    else:
        version_type = type(version).__name__
        raise ArgumentError(
            f"Invalid version type, expected float or str, found '{version_type}'."
        )
    if version_value <= 0:
        raise ArgumentError(
            f"Invalid version value: {version!r}, expected a number greater than 0"
            ' or a parsable version string, eg. 1.015 or "Version 1.015".'
        )
    old_version = get_version(ttfont)
    new_version = normalize_version(version_value)
    # head.fontRevision (only if the font has the head table)
    head = ttfont.get("head")
    if head is not None:
        head.fontRevision = new_version
    # name records (only if the font has the name table)
    if ttfont.get("name") is not None:
        # version name record (name id 5)
        _names.set_name(
            ttfont,
            _names.NAME_VERSION,
            format_version(new_version, prefix="Version "),
        )
        # unique identifier name record (name id 3): it has no canonical form,
        # it conventionally holds the version value in its first ";" separated
        # part, eg. "1.015;ETCO;Tourney-Regular", so only that part is replaced,
        # and only if it holds the current version value
        unique_id = _names.get_name(ttfont, _names.NAME_UNIQUE_IDENTIFIER) or ""
        unique_id_version, separator, unique_id_info = unique_id.partition(";")
        if old_version > 0 and parse_version(unique_id_version) == old_version:
            unique_id_version = format_version(new_version, prefix="")
            _names.set_name(
                ttfont,
                _names.NAME_UNIQUE_IDENTIFIER,
                f"{unique_id_version}{separator}{unique_id_info}",
            )
    # cff version (only otf fonts that already have it)
    top_dict = _get_cff_top_dict(ttfont)
    if top_dict is not None and "version" in top_dict.rawDict:
        top_dict.version = _format_cff_version(new_version)

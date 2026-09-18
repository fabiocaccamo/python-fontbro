from __future__ import annotations

import re

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


def normalize_version(
    version: float,
) -> float:
    """
    Normalizes the given version value to the shortest decimal representation
    that converts back to the same head.fontRevision fixed-point value,
    eg. 1.0149993896484375 -> 1.015 (both are stored as 66519 in the head table).
    """
    version_fixed = floatToFixed(version, precisionBits=_VERSION_PRECISION_BITS)
    version_str = fixedToStr(version_fixed, precisionBits=_VERSION_PRECISION_BITS)
    return float(version_str)


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
        head = ttfont.get("head")
        # fontRevision is 0.0 when it has not been set
        version = float(getattr(head, "fontRevision", 0.0) or 0.0)
        if version > 0:
            return normalize_version(version)
    if use_name_record:
        version = parse_version(_names.get_name(ttfont, _names.NAME_VERSION))
        if version > 0:
            return version
    return 0.0

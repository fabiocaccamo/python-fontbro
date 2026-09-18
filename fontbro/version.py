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

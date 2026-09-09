from __future__ import annotations

import functools
from typing import Any

from fontTools.ttLib import TTFont
from gflanguages import LoadLanguages, LoadScripts
from gflanguages import parse as parse_exemplar_chars

from fontbro.exceptions import DataError

# the most common writing systems, in their default ordering,
# the uncommon ones follow alphabetically after these
_WRITING_SYSTEMS_COMMON = (
    "Latn",
    "Cyrl",
    "Grek",
    "Arab",
    "Hebr",
    "Deva",
    "Hans",
    "Hant",
    "Jpan",
    "Hira",
    "Kana",
    "Kore",
    "Thai",
)

_WRITING_SYSTEMS_FALLBACK_ORDER = 1000

_WRITING_SYSTEMS_ORDER_BY_CODE = {
    code: (index + 1) * 10 for index, code in enumerate(_WRITING_SYSTEMS_COMMON)
}

# sample text fields provided by gflanguages for each language
_SAMPLE_TEXT_FIELDS = (
    "masthead_full",
    "masthead_partial",
    "styles",
    "tester",
    "poster_sm",
    "poster_md",
    "poster_lg",
    "specimen_48",
    "specimen_36",
    "specimen_32",
    "specimen_21",
    "specimen_16",
)


def _get_writing_system_order(code: str) -> int:
    """
    Gets the ordering value of the given writing system code.
    """
    return _WRITING_SYSTEMS_ORDER_BY_CODE.get(code, _WRITING_SYSTEMS_FALLBACK_ORDER)


def _get_base_codepoints(language: Any) -> frozenset[int]:
    """
    Gets the codepoints of the base exemplar characters of the given language.
    Only the base characters are taken into account: the auxiliary ones are not
    required to write the language, the marks ones are listed by gflanguages
    combined with a dotted circle (U+25CC) that fonts are not required to provide.
    """
    chars = parse_exemplar_chars(language.exemplar_chars.base)
    return frozenset(ord(char) for char in chars)


def _get_sample_texts(language: Any) -> dict[str, str]:
    """
    Gets the sample texts of the given language, including its alphabet.
    """
    # the fields are read defensively, gflanguages could rename or drop
    # one of them in any release allowed by the requirements
    sample_texts: dict[str, str] = {
        field: str(getattr(language.sample_text, field, ""))
        for field in _SAMPLE_TEXT_FIELDS
    }
    sample_texts["alphabet"] = " ".join(
        token.strip("{}") for token in language.exemplar_chars.base.split()
    )
    return sample_texts


def _get_empty_sample_texts() -> dict[str, str]:
    """
    Gets an empty sample texts dict, used when no sample text is available.
    """
    return dict.fromkeys((*_SAMPLE_TEXT_FIELDS, "alphabet"), "")


@functools.cache
def _get_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Reads the gflanguages dataset once and builds the languages and
    the writing systems data used by the support detection.
    """
    languages_data: list[dict[str, Any]] = []
    codepoints_by_code: dict[str, set[int]] = {}
    languages_count_by_code: dict[str, int] = {}
    for language in LoadLanguages().values():
        base_codepoints = _get_base_codepoints(language)
        if not base_codepoints:
            continue
        code = str(language.script)
        languages_data.append(
            {
                "code": str(language.id),
                "name": str(language.name),
                "population": int(language.population),
                "writing_system_code": code,
                "base_codepoints": base_codepoints,
                "sample_texts": _get_sample_texts(language),
            }
        )
        codepoints_by_code.setdefault(code, set()).update(base_codepoints)
        languages_count_by_code[code] = languages_count_by_code.get(code, 0) + 1

    # most spoken languages first, code as tie-breaker for deterministic results
    languages_data.sort(key=lambda item: (-item["population"], item["code"]))

    # the sample texts of a writing system are the ones of its most spoken language,
    # falling back to the most spoken one providing at least its alphabet
    sample_texts_by_code: dict[str, dict[str, str]] = {}
    alphabets_by_code: dict[str, dict[str, str]] = {}
    for language_data in languages_data:
        code = language_data["writing_system_code"]
        sample_texts = language_data["sample_texts"]
        if any(sample_texts[field] for field in _SAMPLE_TEXT_FIELDS):
            sample_texts_by_code.setdefault(code, sample_texts)
        if sample_texts["alphabet"]:
            alphabets_by_code.setdefault(code, sample_texts)

    writing_systems_data: list[dict[str, Any]] = []
    scripts = LoadScripts()
    for code, languages_count in languages_count_by_code.items():
        script = scripts.get(code)
        writing_systems_data.append(
            {
                "code": code,
                "name": str(script.name) if script else code,
                "order": _get_writing_system_order(code),
                "languages_count": languages_count,
                "base_codepoints": frozenset(codepoints_by_code[code]),
                "sample_texts": sample_texts_by_code.get(code)
                or alphabets_by_code.get(code)
                or _get_empty_sample_texts(),
            }
        )
    writing_systems_data.sort(key=lambda item: (item["order"], item["name"]))

    writing_systems_data_by_code = {item["code"]: item for item in writing_systems_data}
    for language_data in languages_data:
        writing_system_data = writing_systems_data_by_code[
            language_data["writing_system_code"]
        ]
        language_data["writing_system_name"] = writing_system_data["name"]

    return (languages_data, writing_systems_data)


def _get_languages_data() -> list[dict[str, Any]]:
    """
    Gets the languages usable for support detection.
    The returned data is cached and shared, it must never be mutated.
    """
    languages_data, _ = _get_data()
    return languages_data


def _get_writing_systems_data() -> list[dict[str, Any]]:
    """
    Gets the writing systems referenced by at least one detectable language.
    The returned data is cached and shared, it must never be mutated.
    """
    _, writing_systems_data = _get_data()
    return writing_systems_data


def _get_codepoints(ttfont: TTFont) -> set[int]:
    """
    Gets the codepoints of the 'best' unicode cmap of the given font.
    """
    cmap_table = ttfont.get("cmap")
    cmap = cmap_table.getBestCmap() if cmap_table else None
    if cmap is None:
        raise DataError("Unable to find the 'best' unicode cmap dict.")
    return set(cmap)


def _get_coverage(codepoints: set[int], base_codepoints: frozenset[int]) -> float:
    """
    Gets the ratio of the given base codepoints available in the given codepoints.
    """
    if not base_codepoints:
        return 0.0
    return len(base_codepoints & codepoints) / len(base_codepoints)


def _get_supported_languages(
    codepoints: set[int],
    coverage_threshold: float,
) -> list[dict[str, Any]]:
    """
    Gets the languages supported by the given codepoints and their coverage.
    """
    supported_languages: list[dict[str, Any]] = []
    for language_data in _get_languages_data():
        coverage = _get_coverage(codepoints, language_data["base_codepoints"])
        if coverage < coverage_threshold:
            continue
        supported_languages.append(
            {
                "code": language_data["code"],
                "name": language_data["name"],
                "writing_system_code": language_data["writing_system_code"],
                "writing_system_name": language_data["writing_system_name"],
                "coverage": coverage,
                "sample_texts": dict(language_data["sample_texts"]),
            }
        )
    supported_languages.sort(
        key=lambda item: (
            _get_writing_system_order(item["writing_system_code"]),
            item["writing_system_name"],
            item["name"],
            item["code"],
        )
    )
    return supported_languages


def get_supported_languages(
    ttfont: TTFont,
    *,
    coverage_threshold: float = 1.0,
) -> list[dict[str, Any]]:
    """
    Gets the languages supported by the given font and their coverage.
    """
    return _get_supported_languages(_get_codepoints(ttfont), coverage_threshold)


def get_supported_writing_systems(
    ttfont: TTFont,
    *,
    coverage_threshold: float = 1.0,
    include_uncommon: bool = True,
    prioritize_common: bool = True,
) -> list[dict[str, Any]]:
    """
    Gets the writing systems supported by the given font and their coverage.
    A writing system is supported if at least one of its languages is supported.
    """
    codepoints = _get_codepoints(ttfont)
    supported_languages = _get_supported_languages(codepoints, coverage_threshold)
    supported_languages_count_by_code: dict[str, int] = {}
    for language_data in supported_languages:
        code = language_data["writing_system_code"]
        supported_languages_count_by_code[code] = (
            supported_languages_count_by_code.get(code, 0) + 1
        )

    supported_writing_systems: list[dict[str, Any]] = []
    for writing_system_data in _get_writing_systems_data():
        code = writing_system_data["code"]
        if not include_uncommon and code not in _WRITING_SYSTEMS_COMMON:
            continue
        supported_languages_count = supported_languages_count_by_code.get(code, 0)
        if not supported_languages_count:
            continue
        supported_writing_systems.append(
            {
                "code": code,
                "name": writing_system_data["name"],
                "coverage": _get_coverage(
                    codepoints, writing_system_data["base_codepoints"]
                ),
                "languages_count": writing_system_data["languages_count"],
                "languages_supported_count": supported_languages_count,
                "sample_texts": dict(writing_system_data["sample_texts"]),
            }
        )
    if not prioritize_common:
        supported_writing_systems.sort(key=lambda item: (item["name"], item["code"]))
    return supported_writing_systems

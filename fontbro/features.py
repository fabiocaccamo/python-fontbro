from __future__ import annotations

from typing import Any

from fontTools.ttLib import TTFont

from fontbro.utils import read_json

# Features:
# https://docs.microsoft.com/en-gb/typography/opentype/spec/featurelist
# https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings
_FEATURES_LIST: list[dict[str, Any]] = read_json("data/features.json")
_FEATURES_BY_TAG: dict[str, dict[str, Any]] = {
    feature["tag"]: feature for feature in _FEATURES_LIST
}


def get_features(
    ttfont: TTFont,
) -> list[dict[str, Any]]:
    """
    Gets the opentype features of the given font.
    """
    features_tags = get_features_tags(ttfont)
    features_params = _get_features_params(ttfont)
    features = []
    for features_tag in features_tags:
        if features_tag not in _FEATURES_BY_TAG:
            continue
        feature = _FEATURES_BY_TAG[features_tag].copy()
        feature["params"] = _get_feature_params_dict(
            ttfont, features_params.get(features_tag)
        )
        features.append(feature)
    return features


def _get_features_params(
    ttfont: TTFont,
) -> dict[str, Any]:
    """
    Gets the opentype features params (if any) of the given font by tag.
    """
    features_params: dict[str, Any] = {}
    for table_tag in ["GPOS", "GSUB"]:
        if table_tag in ttfont:
            table = ttfont[table_tag].table
            try:
                feature_record = table.FeatureList.FeatureRecord or []
            except AttributeError:
                feature_record = []
            for feature in feature_record:
                feature_params = feature.Feature.FeatureParams
                if feature_params is not None:
                    features_params.setdefault(feature.FeatureTag, feature_params)
    return features_params


def _get_feature_params_dict(
    ttfont: TTFont,
    feature_params: Any,
) -> dict[str, Any]:
    """
    Gets the designer-defined params of a feature:
    stylistic sets (ss01-ss20) and character variants (cv01-cv99).
    """

    def get_name(name_id: int | None) -> str | None:
        if not name_id or "name" not in ttfont:
            return None
        name: str | None = ttfont["name"].getDebugName(name_id)
        return name

    params: dict[str, Any] = {
        "name": None,
        "tooltip": None,
        "sample_text": None,
        "labels": [],
        "characters": [],
    }
    if feature_params is None:
        return params
    params["name"] = get_name(
        getattr(feature_params, "UINameID", None)
        or getattr(feature_params, "FeatUILabelNameID", None)
    )
    params["tooltip"] = get_name(
        getattr(feature_params, "FeatUITooltipTextNameID", None)
    )
    params["sample_text"] = get_name(getattr(feature_params, "SampleTextNameID", None))
    first_label_name_id = getattr(feature_params, "FirstParamUILabelNameID", 0)
    labels_count = getattr(feature_params, "NumNamedParameters", 0)
    if first_label_name_id:
        # keep missing labels as None to preserve the label index / feature value match
        params["labels"] = [
            get_name(first_label_name_id + index) for index in range(labels_count)
        ]
    # characters are stored as uint24, skip values that are not unicode scalar values
    characters = getattr(feature_params, "Character", None) or []
    params["characters"] = [
        chr(character)
        for character in characters
        if 0 <= character <= 0x10FFFF and not 0xD800 <= character <= 0xDFFF
    ]
    return params


def get_features_tags(
    ttfont: TTFont,
) -> list[str]:
    """
    Gets the opentype features tags of the given font.
    """
    features_tags = set()
    for table_tag in ["GPOS", "GSUB"]:
        if table_tag in ttfont:
            table = ttfont[table_tag].table
            try:
                feature_record = table.FeatureList.FeatureRecord or []
            except AttributeError:
                feature_record = []
            for feature in feature_record:
                features_tags.add(feature.FeatureTag)
    return sorted(features_tags)

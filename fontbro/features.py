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
    return [
        _FEATURES_BY_TAG.get(features_tag, {}).copy()
        for features_tag in features_tags
        if features_tag in _FEATURES_BY_TAG
    ]


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

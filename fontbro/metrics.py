from __future__ import annotations

from typing import Any

from fontTools.ttLib import TTFont

# Vertical Metrics:
VERTICAL_METRIC_UNITS_PER_EM: str = "units_per_em"
VERTICAL_METRIC_Y_MAX: str = "y_max"
VERTICAL_METRIC_Y_MIN: str = "y_min"
VERTICAL_METRIC_ASCENT: str = "ascent"
VERTICAL_METRIC_DESCENT: str = "descent"
VERTICAL_METRIC_LINE_GAP: str = "line_gap"
VERTICAL_METRIC_TYPO_ASCENDER: str = "typo_ascender"
VERTICAL_METRIC_TYPO_DESCENDER: str = "typo_descender"
VERTICAL_METRIC_TYPO_LINE_GAP: str = "typo_line_gap"
VERTICAL_METRIC_CAP_HEIGHT: str = "cap_height"
VERTICAL_METRIC_X_HEIGHT: str = "x_height"
VERTICAL_METRIC_WIN_ASCENT: str = "win_ascent"
VERTICAL_METRIC_WIN_DESCENT: str = "win_descent"
# fmt: off
_VERTICAL_METRICS: list[dict[str, Any]] = [
    {"table": "head", "attr": "unitsPerEm", "key": VERTICAL_METRIC_UNITS_PER_EM},
    {"table": "head", "attr": "yMax", "key": VERTICAL_METRIC_Y_MAX},
    {"table": "head", "attr": "yMin", "key": VERTICAL_METRIC_Y_MIN},
    {"table": "hhea", "attr": "ascent", "key": VERTICAL_METRIC_ASCENT},
    {"table": "hhea", "attr": "descent", "key": VERTICAL_METRIC_DESCENT},
    {"table": "hhea", "attr": "lineGap", "key": VERTICAL_METRIC_LINE_GAP},
    {"table": "OS/2", "attr": "sTypoAscender", "key": VERTICAL_METRIC_TYPO_ASCENDER},
    {"table": "OS/2", "attr": "sTypoDescender", "key": VERTICAL_METRIC_TYPO_DESCENDER},
    {"table": "OS/2", "attr": "sTypoLineGap", "key": VERTICAL_METRIC_TYPO_LINE_GAP},
    {"table": "OS/2", "attr": "sCapHeight", "key": VERTICAL_METRIC_CAP_HEIGHT},
    {"table": "OS/2", "attr": "sxHeight", "key": VERTICAL_METRIC_X_HEIGHT},
    {"table": "OS/2", "attr": "usWinAscent", "key": VERTICAL_METRIC_WIN_ASCENT},
    {"table": "OS/2", "attr": "usWinDescent", "key": VERTICAL_METRIC_WIN_DESCENT},
]
# fmt: on

# Weights:
# https://docs.microsoft.com/en-us/typography/opentype/otspec170/os2#usweightclass
WEIGHT_EXTRA_THIN: str = "Extra-thin"  # (Hairline)
WEIGHT_THIN: str = "Thin"
WEIGHT_EXTRA_LIGHT: str = "Extra-light"  # (Ultra-light)
WEIGHT_LIGHT: str = "Light"
WEIGHT_REGULAR: str = "Regular"  # (Normal)
WEIGHT_BOOK: str = "Book"
WEIGHT_MEDIUM: str = "Medium"
WEIGHT_SEMI_BOLD: str = "Semi-bold"  # (Demi-bold)
WEIGHT_BOLD: str = "Bold"
WEIGHT_EXTRA_BOLD: str = "Extra-bold"  # (Ultra-bold)
WEIGHT_BLACK: str = "Black"  # (Heavy)
WEIGHT_EXTRA_BLACK: str = "Extra-black"  # (Nord)
_WEIGHTS: list[dict[str, Any]] = [
    {"value": 50, "name": WEIGHT_EXTRA_THIN},
    {"value": 100, "name": WEIGHT_THIN},
    {"value": 200, "name": WEIGHT_EXTRA_LIGHT},
    {"value": 300, "name": WEIGHT_LIGHT},
    {"value": 400, "name": WEIGHT_REGULAR},
    {"value": 450, "name": WEIGHT_BOOK},
    {"value": 500, "name": WEIGHT_MEDIUM},
    {"value": 600, "name": WEIGHT_SEMI_BOLD},
    {"value": 700, "name": WEIGHT_BOLD},
    {"value": 800, "name": WEIGHT_EXTRA_BOLD},
    {"value": 900, "name": WEIGHT_BLACK},
    {"value": 950, "name": WEIGHT_EXTRA_BLACK},
]
_WEIGHTS_BY_VALUE: dict[int, dict[str, Any]] = {
    weight["value"]: weight for weight in _WEIGHTS
}

# Widths:
# https://docs.microsoft.com/en-us/typography/opentype/otspec170/os2#uswidthclass
WIDTH_ULTRA_CONDENSED: str = "Ultra-condensed"
WIDTH_EXTRA_CONDENSED: str = "Extra-condensed"
WIDTH_CONDENSED: str = "Condensed"
WIDTH_SEMI_CONDENSED: str = "Semi-condensed"
WIDTH_MEDIUM: str = "Medium"  # (Normal)
WIDTH_SEMI_EXPANDED: str = "Semi-expanded"
WIDTH_EXPANDED: str = "Expanded"
WIDTH_EXTRA_EXPANDED: str = "Extra-expanded"
WIDTH_ULTRA_EXPANDED: str = "Ultra-expanded"
_WIDTHS: list[dict[str, Any]] = [
    {"value": 1, "perc": 50.0, "name": WIDTH_ULTRA_CONDENSED},
    {"value": 2, "perc": 62.5, "name": WIDTH_EXTRA_CONDENSED},
    {"value": 3, "perc": 75.0, "name": WIDTH_CONDENSED},
    {"value": 4, "perc": 87.5, "name": WIDTH_SEMI_CONDENSED},
    {"value": 5, "perc": 100.0, "name": WIDTH_MEDIUM},
    {"value": 6, "perc": 112.5, "name": WIDTH_SEMI_EXPANDED},
    {"value": 7, "perc": 125.0, "name": WIDTH_EXPANDED},
    {"value": 8, "perc": 150.0, "name": WIDTH_EXTRA_EXPANDED},
    {"value": 9, "perc": 200.0, "name": WIDTH_ULTRA_EXPANDED},
]
_WIDTHS_BY_VALUE: dict[int, dict[str, Any]] = {
    width["value"]: width for width in _WIDTHS
}


def get_italic_angle(
    ttfont: TTFont,
) -> dict[str, Any] | None:
    """
    Gets the italic angle of the given font.
    """
    post = ttfont.get("post")
    if not post:
        return None
    italic_angle_value = post.italicAngle
    italic_angle = {
        "backslant": italic_angle_value > 0,
        "italic": italic_angle_value < 0,
        "roman": italic_angle_value == 0,
        "value": italic_angle_value,
    }
    return italic_angle


def get_vertical_metrics(
    ttfont: TTFont,
) -> dict[str, Any]:
    """
    Gets the vertical metrics of the given font.
    """
    metrics = {}
    for metric in _VERTICAL_METRICS:
        table = ttfont.get(metric["table"])
        metrics[metric["key"]] = getattr(table, metric["attr"], None) if table else None
    return metrics


def set_vertical_metrics(
    ttfont: TTFont,
    **vertical_metrics: Any,
) -> None:
    """
    Sets the vertical metrics of the given font.
    """
    for metric in _VERTICAL_METRICS:
        if metric["key"] in vertical_metrics:
            table = ttfont.get(metric["table"])
            if table:
                setattr(table, metric["attr"], vertical_metrics[metric["key"]])


def get_weight(
    ttfont: TTFont,
) -> dict[str, Any] | None:
    """
    Gets the weight value and name of the given font.
    """
    os2 = ttfont.get("OS/2")
    if not os2:
        return None
    weight_value = os2.usWeightClass
    weight_value = min(max(1, weight_value), 1000)
    weight_option_values = sorted(_WEIGHTS_BY_VALUE.keys())
    closest_weight_option_value = min(
        weight_option_values,
        key=lambda weight_option_value: abs(weight_option_value - weight_value),
    )
    weight = _WEIGHTS_BY_VALUE.get(closest_weight_option_value, {}).copy()
    weight["value"] = weight_value
    return weight


def get_width(
    ttfont: TTFont,
) -> dict[str, Any] | None:
    """
    Gets the width value and name of the given font.
    """
    os2 = ttfont.get("OS/2")
    if not os2:
        return None
    width_value = os2.usWidthClass
    width_value = min(max(1, width_value), 9)
    width = _WIDTHS_BY_VALUE.get(width_value, {}).copy()
    width["value"] = width_value
    return width

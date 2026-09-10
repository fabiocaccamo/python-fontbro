from __future__ import annotations

import sys
from typing import Any

from fontTools.ttLib import TTFont

from fontbro.exceptions import ArgumentError
from fontbro.math import get_euclidean_distance
from fontbro.utils import slugify

# Variable Axes:
_VARIABLE_AXES: list[dict[str, Any]] = [
    {"tag": "ital", "name": "Italic"},
    {"tag": "opsz", "name": "Optical Size"},
    {"tag": "slnt", "name": "Slant"},
    {"tag": "wdth", "name": "Width"},
    {"tag": "wght", "name": "Weight"},
    # https://fonts.google.com/variablefonts#axis-definitions
    {"tag": "ARRR", "name": "AR Retinal Resolution"},
    {"tag": "YTAS", "name": "Ascender Height"},
    {"tag": "BLED", "name": "Bleed"},
    {"tag": "BNCE", "name": "Bounce"},
    {"tag": "CASL", "name": "Casual"},
    {"tag": "CTRS", "name": "Contrast"},
    {"tag": "XTRA", "name": "Counter Width"},
    {"tag": "CRSV", "name": "Cursive"},
    {"tag": "YTDE", "name": "Descender Depth"},
    {"tag": "EHLT", "name": "Edge Highlight"},
    {"tag": "ELXP", "name": "Element Expansion"},
    {"tag": "ELGR", "name": "Element Grid"},
    {"tag": "ELSH", "name": "Element Shape"},
    {"tag": "EDPT", "name": "Extrusion Depth"},
    {"tag": "YTFI", "name": "Figure Height"},
    # Removed: https://github.com/google/fonts/pull/2594
    {"tag": "XPRN", "name": "Expression"},
    {"tag": "FILL", "name": "Fill"},
    {"tag": "FLAR", "name": "Flare"},
    {"tag": "GRAD", "name": "Grade"},
    {"tag": "XELA", "name": "Horizontal Element Alignment"},
    {"tag": "XPN1", "name": "Horizontal Position of Paint 1"},
    {"tag": "XPN2", "name": "Horizontal Position of Paint 2"},
    {"tag": "HEXP", "name": "Hyper Expansion"},
    {"tag": "INFM", "name": "Informality"},
    {"tag": "YTLC", "name": "Lowercase Height"},
    {"tag": "MONO", "name": "Monospace"},
    {"tag": "MORF", "name": "Morph"},
    {"tag": "XROT", "name": "Rotation in X"},
    {"tag": "YROT", "name": "Rotation in Y"},
    {"tag": "ZROT", "name": "Rotation in Z"},
    {"tag": "ROND", "name": "Roundness"},
    {"tag": "SCAN", "name": "Scanlines"},
    {"tag": "SHLN", "name": "Shadow Length"},
    {"tag": "SHRP", "name": "Sharpness"},
    {"tag": "SZP1", "name": "Size of Paint 1"},
    {"tag": "SZP2", "name": "Size of Paint 2"},
    {"tag": "SOFT", "name": "Softness"},
    {"tag": "SPAC", "name": "Spacing"},
    {"tag": "XOPQ", "name": "Thick Stroke"},
    {"tag": "YOPQ", "name": "Thin Stroke"},
    {"tag": "YTUC", "name": "Uppercase Height"},
    {"tag": "YELA", "name": "Vertical Element Alignment"},
    {"tag": "YEXT", "name": "Vertical Extension"},
    {"tag": "YPN1", "name": "Vertical Position of Paint 1"},
    {"tag": "YPN2", "name": "Vertical Position of Paint 2"},
    {"tag": "VOLM", "name": "Volume"},
    {"tag": "WONK", "name": "Wonky"},
    {"tag": "YEAR", "name": "Year"},
]
_VARIABLE_AXES_BY_TAG: dict[str, Any] = {axis["tag"]: axis for axis in _VARIABLE_AXES}


def _all_axes_pinned(
    axes: dict[str, Any],
) -> bool:
    """
    Determines if all the axes are pinned (have a single value, not a range).
    """
    return all(
        isinstance(axis_value, (type(None), int, float)) for axis_value in axes.values()
    )


def is_variable(
    ttfont: TTFont,
) -> bool:
    """
    Determines if the given font is a variable font.
    """
    return "fvar" in ttfont


def get_variable_axes(
    ttfont: TTFont,
    *,
    sort: bool = False,
) -> list[dict[str, Any]] | None:
    """
    Gets the variable axes of the given font, None if the font is not variable.
    """
    if not is_variable(ttfont):
        return None
    axes = [
        {
            "tag": axis.axisTag,
            "name": _VARIABLE_AXES_BY_TAG.get(axis.axisTag, {}).get(
                "name", axis.axisTag.title()
            ),
            "min_value": axis.minValue,
            "max_value": axis.maxValue,
            "default_value": axis.defaultValue,
        }
        for axis in ttfont["fvar"].axes
    ]
    if sort:
        axes = sorted(
            axes,
            key=lambda axis: (axis["tag"].islower(), axis["tag"]),
        )
    return axes


def get_variable_axis_by_tag(
    ttfont: TTFont,
    tag: str,
) -> dict[str, Any] | None:
    """
    Gets the variable axis of the given font by tag.
    """
    axes = get_variable_axes(ttfont)
    if axes:
        for axis in axes:
            if axis.get("tag") == tag:
                return axis
    # raise KeyError("Invalid axis tag: '{tag}'")
    return None


def get_variable_axes_tags(
    ttfont: TTFont,
) -> list[str] | None:
    """
    Gets the variable axes tags of the given font, None if the font is not variable.
    """
    if not is_variable(ttfont):
        return None
    return [axis.axisTag for axis in ttfont["fvar"].axes]


def get_variable_instances(
    ttfont: TTFont,
) -> list[dict[str, Any]] | None:
    """
    Gets the variable instances of the given font, None if the font is not variable.
    """
    if not is_variable(ttfont):
        return None
    name_table = ttfont["name"]
    return [
        {
            "coordinates": instance.coordinates,
            "style_name": name_table.getDebugName(instance.subfamilyNameID),
        }
        for instance in ttfont["fvar"].instances
    ]


def get_variable_instance_by_style_name(
    ttfont: TTFont,
    style_name: str,
) -> dict[str, Any] | None:
    """
    Gets the variable instance of the given font by style name.
    """
    instances = get_variable_instances(ttfont) or []
    for instance in instances:
        if slugify(instance["style_name"]) == slugify(style_name):
            return instance
    return None


def get_variable_instance_closest_to_coordinates(
    ttfont: TTFont,
    coordinates: dict[str, Any],
) -> dict[str, Any] | None:
    """
    Gets the variable instance of the given font closest to the given coordinates.
    """
    if not is_variable(ttfont):
        return None

    # set default axes values for axes not present in coordinates
    lookup_values = coordinates.copy()
    axes = get_variable_axes(ttfont) or []
    for axis in axes:
        # don't use setdefault to override possible None values
        if lookup_values.get(axis["tag"]) is None:
            lookup_values[axis["tag"]] = axis["default_value"]

    instances = get_variable_instances(ttfont) or []
    closest_instance_distance = float(sys.maxsize)
    closest_instance = None
    for instance in instances:
        instance_values = instance["coordinates"]
        instance_distance = get_euclidean_distance(instance_values, lookup_values)
        if instance_distance < closest_instance_distance:
            closest_instance_distance = instance_distance
            closest_instance = instance
    return closest_instance


def get_sliced_coordinates(
    ttfont: TTFont,
    coordinates: dict[str, Any],
) -> dict[str, Any]:
    """
    Gets the coordinates to slice the given variable font,
    list and dict axis values are converted to (min, default, max) tuples.
    """
    # copy the coordinates to not modify the dict passed by the caller
    coordinates = dict(coordinates or {})
    coordinates_axes_tags = coordinates.keys()

    # make coordinates more friendly accepting also list and dict values
    for axis_tag in coordinates_axes_tags:
        axis_value = coordinates[axis_tag]
        if isinstance(axis_value, list):
            axis_value = tuple(axis_value)
        elif isinstance(axis_value, dict):
            axis = get_variable_axis_by_tag(ttfont, axis_tag) or {}
            axis_min = axis_value.get("min", axis.get("min_value"))
            axis_default = axis_value.get("default", axis.get("default_value"))
            axis_max = axis_value.get("max", axis.get("max_value"))
            axis_value = (axis_min, axis_default, axis_max)
        coordinates[axis_tag] = axis_value

    # ensure that coordinates axes are defined and that are not all pinned
    if len(coordinates_axes_tags) == 0:
        raise ArgumentError("Invalid coordinates: axes not defined.")
    elif set(coordinates_axes_tags) == set(get_variable_axes_tags(ttfont) or []):
        if _all_axes_pinned(coordinates):
            raise ArgumentError(
                "Invalid coordinates: all axes are pinned (use to_static method)."
            )
    return coordinates


def get_static_coordinates(
    ttfont: TTFont,
    *,
    coordinates: dict[str, Any] | None = None,
    style_name: str | None = None,
) -> dict[str, Any]:
    """
    Gets the coordinates to make the given variable font static,
    taken from the instance with the given style name or from the given coordinates
    (axes not defined in the coordinates use their default value).
    """
    # take coordinates from instance with specified style name
    if style_name:
        if coordinates:
            raise ArgumentError(
                "Invalid arguments: 'coordinates' and 'style_name' are mutually exclusive."
            )
        instance = get_variable_instance_by_style_name(ttfont, style_name=style_name)
        if not instance:
            raise ArgumentError(
                f"Invalid style name: instance with style name '{style_name}' not found."
            )
        coordinates = instance["coordinates"].copy()

    # make coordinates more friendly by using default axis values by default
    # copy the coordinates to not modify the dict passed by the caller
    coordinates = dict(coordinates or {})
    default_coordinates = {
        axis_tag: None
        for axis_tag in (get_variable_axes_tags(ttfont) or [])
        if axis_tag not in coordinates
    }
    coordinates.update(default_coordinates)

    # ensure that coordinates axes are all pinned
    if not _all_axes_pinned(coordinates):
        raise ArgumentError("Invalid coordinates: all axes must be pinned.")
    return coordinates

from __future__ import annotations

from fontTools.ttLib import TTFont

from fontbro import names, variable
from fontbro.exceptions import DataError
from fontbro.utils import concat_names, remove_spaces

# Formats:
FORMAT_OTF: str = "otf"
FORMAT_TTF: str = "ttf"
FORMAT_WOFF: str = "woff"
FORMAT_WOFF2: str = "woff2"

_FORMATS_LIST: list[str] = [FORMAT_OTF, FORMAT_TTF, FORMAT_WOFF, FORMAT_WOFF2]


def get_format(
    ttfont: TTFont,
    *,
    ignore_flavor: bool = False,
) -> str:
    """
    Gets the format of the given font.
    """
    version = ttfont.sfntVersion
    flavor = ttfont.flavor
    format_ = ""
    if flavor in [FORMAT_WOFF, FORMAT_WOFF2] and not ignore_flavor:
        format_ = str(flavor)
    elif version == "OTTO" and ("CFF " in ttfont or "CFF2" in ttfont):
        format_ = FORMAT_OTF
    elif version == "\0\1\0\0":
        format_ = FORMAT_TTF
    elif version == "wOFF":
        format_ = FORMAT_WOFF
    elif version == "wOF2":
        format_ = FORMAT_WOFF2
    if not format_:
        raise DataError("Unable to get the font format.")
    return format_


def get_filename(
    ttfont: TTFont,
    *,
    variable_suffix: str = "",
    variable_axes_tags: bool = True,
    variable_axes_values: bool = False,
) -> str:
    """
    Gets the filename to use for saving the given font to file-system.
    """
    if variable.is_variable(ttfont):
        family_name = names.get_family_name(ttfont)
        family_name = remove_spaces(family_name)
        subfamily_name = names.get_name(ttfont, names.NAME_SUBFAMILY_NAME) or ""
        basename = family_name
        # append subfamily name
        if subfamily_name.lower() in ("bold", "bold italic", "italic"):
            subfamily_name = remove_spaces(subfamily_name.lower().title())
            basename = f"{basename}-{subfamily_name}"
        # append variable suffix
        variable_suffix = (variable_suffix or "").strip()
        if variable_suffix:
            if variable_suffix.lower() not in basename.lower():
                basename = f"{basename}-{variable_suffix}"
        # append axis tags stringified suffix, eg. [wdth,wght,slnt]
        if variable_axes_tags:
            axes = variable.get_variable_axes(ttfont, sort=True) or []
            axes_str_parts = []
            for axis in axes:
                axis_tag = axis["tag"]
                axis_str = f"{axis_tag}"
                if variable_axes_values:
                    axis_min_value = int(axis["min_value"])
                    axis_default_value = int(axis["default_value"])
                    axis_max_value = int(axis["max_value"])
                    axis_str += (
                        f"({axis_min_value},{axis_default_value},{axis_max_value})"
                    )
                axes_str_parts.append(axis_str)
            axes_str = ",".join(axes_str_parts)
            axes_str = f"[{axes_str}]"
            basename = f"{basename}{axes_str}"
    else:
        family_name = names.get_family_name(ttfont)
        family_name = remove_spaces(family_name)
        style_name = names.get_style_name(ttfont)
        style_name = remove_spaces(style_name)
        basename = concat_names(family_name, style_name, separator="-")
    extension = get_format(ttfont)
    filename = f"{basename}.{extension}"
    return filename


def get_version(
    ttfont: TTFont,
) -> float:
    """
    Gets the version of the given font (head.fontRevision).
    """
    head = ttfont.get("head")
    version = float(head.fontRevision)
    return version

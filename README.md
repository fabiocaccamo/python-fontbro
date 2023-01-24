[![](https://img.shields.io/pypi/pyversions/python-fontbro.svg?color=blue&logo=python&logoColor=white)](https://www.python.org/)
[![](https://img.shields.io/pypi/v/python-fontbro.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/python-fontbro/)
[![](https://pepy.tech/badge/python-fontbro/month)](https://pepy.tech/project/python-fontbro)
[![](https://img.shields.io/github/stars/fabiocaccamo/python-fontbro?logo=github)](https://github.com/fabiocaccamo/python-fontbro/stargazers)
[![](https://img.shields.io/pypi/l/python-fontbro?color=blue)](https://github.com/fabiocaccamo/python-fontbro/blob/main/LICENSE.txt)

[![](https://results.pre-commit.ci/badge/github/fabiocaccamo/python-fontbro/main.svg)](https://results.pre-commit.ci/latest/github/fabiocaccamo/python-fontbro/main)
[![](https://img.shields.io/github/actions/workflow/status/fabiocaccamo/python-fontbro/test-package.yml?branch=main&label=build&logo=github)](https://github.com/fabiocaccamo/python-fontbro)
[![](https://img.shields.io/codecov/c/gh/fabiocaccamo/python-fontbro?logo=codecov)](https://codecov.io/gh/fabiocaccamo/python-fontbro)
[![](https://img.shields.io/codacy/grade/dd3a046db4b14b988a2f1fcfbfaa51eb?logo=codacy)](https://www.codacy.com/app/fabiocaccamo/python-fontbro)
[![](https://img.shields.io/codeclimate/maintainability/fabiocaccamo/python-fontbro?logo=code-climate)](https://codeclimate.com/github/fabiocaccamo/python-fontbro/)
[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# python-fontbro
friendly font operations on top of `fontTools`. :billed_cap:

## Installation
```bash
pip install python-fontbro
```

## Usage
Just import the font class:

```python
from fontbro import Font

font = Font("fonts/MyFont.ttf")
```

### Methods
-   [`clone`](#clone)
-   [`close`](#close)
-   [`get_characters`](#get_characters)
-   [`get_characters_count`](#get_characters_count)
-   [`get_features`](#get_features)
-   [`get_features_tags`](#get_features_tags)
-   [`get_format`](#get_format)
-   [`get_fingerprint`](#get_fingerprint)
-   [`get_fingerprint_match`](#get_fingerprint_match)
-   [`get_glyphs`](#get_glyphs)
-   [`get_glyphs_count`](#get_glyphs_count)
-   [`get_image`](#get_image)
-   [`get_italic_angle`](#get_italic_angle)
-   [`get_name`](#get_name)
-   [`get_names`](#get_names)
-   [`get_style_flag`](#get_style_flag)
-   [`get_style_flags`](#get_style_flags)
-   [`get_ttfont`](#get_ttfont)
-   [`get_unicode_block_by_name`](#get_unicode_block_by_name)
-   [`get_unicode_blocks`](#get_unicode_blocks)
-   [`get_unicode_script_by_name`](#get_unicode_script_by_name)
-   [`get_unicode_scripts`](#get_unicode_scripts)
-   [`get_variable_axes`](#get_variable_axes)
-   [`get_variable_axes_tags`](#get_variable_axes_tags)
-   [`get_variable_axis_by_tag`](#get_variable_axis_by_tag)
-   [`get_variable_instances`](#get_variable_instances)
-   [`get_variable_instance_closest_to_coordinates`](#get_variable_instance_closest_to_coordinates)
-   [`get_version`](#get_version)
-   [`get_weight`](#get_weight)
-   [`get_width`](#get_width)
-   [`is_static`](#is_static)
-   [`is_variable`](#is_variable)
-   [`rename`](#rename)
-   [`save`](#save)
-   [`save_as_woff`](#save_as_woff)
-   [`save_as_woff2`](#save_as_woff2)
-   [`set_name`](#set_name)
-   [`set_names`](#set_names)
-   [`set_style_flag`](#set_style_flag)
-   [`set_style_flags`](#set_style_flags)
-   [`set_style_flags_by_subfamily_name`](#set_style_flags_by_subfamily_name)
-   [`subset`](#subset)
-   [`to_sliced_variable`](#to_sliced_variable)
-   [`to_static`](#to_static)

-   #### clone
```python
"""
Creates a new Font instance reading the same binary file.
"""
font_clone = font.clone()
```

-   #### close
```python
"""
Close the wrapped TTFont instance.
"""
font.close()
```

-   #### get_characters
```python
"""
Gets the font characters.

:param ignore_blank: If True, characters without contours will not be returned.
:type ignore_blank: bool

:returns: The characters.
:rtype: generator of dicts

:raises TypeError: If it's not possible to find the 'best' unicode cmap dict in the font.
"""
chars = font.get_characters(ignore_blank=False)
```

-   #### get_characters_count
```python
"""
Gets the font characters count.

:param ignore_blank: If True, characters without contours will not be counted.
:type ignore_blank: bool

:returns: The characters count.
:rtype: int
"""
chars_count = font.get_characters_count(ignore_blank=False)
```

-   #### get_features
```python
"""
Gets the font opentype features.

:returns: The features.
:rtype: list of dict
"""
features = font.get_features()
```

-   #### get_features_tags
```python
"""
Gets the font opentype features tags.

:returns: The features tags list.
:rtype: list of str
"""
features_tags = font.get_features_tags()
```

-   #### get_fingerprint
```python
"""
Gets the font fingerprint: an hash calculated from an image representation of the font.
Changing the text option affects the returned fingerprint.

:param text: The text used for generating the fingerprint, default value: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789".
:type text: str
:returns: The fingerprint hash.
:rtype: imagehash.ImageHash
"""
hash = font.get_fingerprint()
```

-   #### get_fingerprint_match
```python
"""
Gets the fingerprint match between this font and another one.
by checking if their fingerprints are equal (difference <= tolerance).

:param other: The other font, can be either a filepath or a Font instance.
:type other: str or Font
:param tolerance: The diff tolerance, default 3.
:type tolerance: int
:param text: The text used for generating the fingerprint, default value: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789".
:type text: str
:returns: A tuple containing the match info (match, diff, hash, other_hash).
:rtype: tuple
"""
match, diff, hash, other_hash = font.get_fingerprint_match(other="other_font.ttf", tolerance=10)
```

-   #### get_format
```python
"""
Gets the font format: otf, ttf, woff, woff2.

:param ignore_flavor: If True, the original format without compression will be returned.
:type ignore_flavor: bool

:returns: The format.
:rtype: str or None
"""
format = font.get_format(ignore_flavor=False)
```

-   #### get_glyphs
```python
"""
Gets the font glyphs and their own composition.

:returns: The glyphs.
:rtype: generator of dicts
"""
glyphs = font.get_glyphs()
```

-   #### get_glyphs_count
```python
"""
Gets the font glyphs count.

:returns: The glyphs count.
:rtype: int
"""
glyphs_count = font.get_glyphs_count()
```

-   #### get_image
```python
"""
Gets an image representation of the font rendering
some text using the given options.

:param text: The text rendered in the image
:type text: str
:param size: The font size
:type size: int
:param color: The text color
:type color: tuple
:param background_color: The background color
:type background_color: tuple
"""
img = font.get_image(text="Hello!", size=48, color=(0, 0, 0, 255), background_color=(255, 255, 255, 255))
```

-   #### get_italic_angle
```python
"""
Gets the font italic angle.

:returns: The angle value including backslant, italic and roman flags.
:rtype: dict or None
"""
italic_angle = font.get_italic_angle()
```

-   #### get_name
```python
"""
Gets the name by its identifier from the font name table.

:param key: The name id or key (eg. "family_name")
:type key: int or str

:returns: The name.
:rtype: str or None

:raises KeyError: if the key is not a valid name key/id
"""
family_name = font.get_name(key=Font.NAME_FAMILY_NAME)
```

-   #### get_names
```python
"""
Gets the names records mapped by their property name.

:returns: The names.
:rtype: dict
"""
names = font.get_names()
```

-   #### get_style_flag
```python
"""
Gets the style flag reading OS/2 and macStyle tables.

:param key: The key
:type key: string

:returns: The style flag.
:rtype: bool
"""
flag = font.get_style_flag(Font.STYLE_FLAG_BOLD)
```

-   #### get_style_flags
```python
"""
Gets the style flags reading OS/2 and macStyle tables.

:returns: The dict representing the style flags.
:rtype: dict
"""
flags = font.get_style_flags()
```

-   #### get_ttfont
```python
"""
Gets the wrapped TTFont instance.

:returns: The TTFont instance.
:rtype: TTFont
"""
ttfont = font.get_ttfont()
```

-   #### get_unicode_block_by_name
```python
"""
Gets the unicode block by name (name is case-insensitive and ignores "-").

:param name: The name
:type name: str

:returns: The unicode block dict if the name is valid, None otherwise.
:rtype: dict or None
"""
block = font.get_unicode_block_by_name(name="Basic Latin")
```

-   #### get_unicode_blocks
```python
"""
Gets the unicode blocks and their coverage.
Only blocks with coverage >= coverage_threshold (0.0 <= coverage_threshold <= 1.0) will be returned.

:param coverage_threshold: The minumum required coverage for a block to be returned.
:type coverage_threshold: float

:returns: The list of unicode blocks.
:rtype: list of dicts
"""
blocks = font.get_unicode_blocks(coverage_threshold=0.00001)
```

-   #### get_unicode_script_by_name
```python
"""
Gets the unicode script by name/tag (name/tag is case-insensitive and ignores "-").

:param name: The name
:type name: str

:returns: The unicode script dict if the name/tag is valid, None otherwise.
:rtype: dict or None
"""
script = font.get_unicode_script_by_name(name="Latn")
```

-   #### get_unicode_scripts
```python
"""
Gets the unicode scripts and their coverage.
Only scripts with coverage >= coverage_threshold (0.0 <= coverage_threshold <= 1.0) will be returned.

:param coverage_threshold: The minumum required coverage for a script to be returned.
:type coverage_threshold: float

:returns: The list of unicode scripts.
:rtype: list of dicts
"""
scripts = font.get_unicode_scripts(coverage_threshold=0.00001)
```

-   #### get_variable_axes
```python
"""
Gets the font variable axes.

:returns: The list of axes if the font is a variable font otherwise None.
:rtype: list of dict or None
"""
axes = font.get_variable_axes()
```

-   #### get_variable_axes_tags
```python
"""
Gets the variable axes tags.

:returns: The variable axis tags.
:rtype: list or None
"""
axes_tags = font.get_variable_axes_tags()
```

-   #### get_variable_axis_by_tag
```python
"""
Gets a variable axis by tag.

:param tag: The tag
:type tag: string

:returns: The variable axis by tag.
:rtype: dict or None
"""
axis = font.get_variable_axis_by_tag(tag="wght")
```

-   #### get_variable_instances
```python
"""
Gets the variable instances.

:returns: The list of instances if the font is a variable font otherwise None.
:rtype: list of dict or None
"""
instances = font.get_variable_instances()
```

-   #### get_variable_instance_closest_to_coordinates
```python
"""
Gets the variable instance closest to coordinates.
eg. coordinates = {"wght": 1000, "slnt": 815, "wdth": 775}

:param coordinates: The coordinates
:type coordinates: dict

:returns: The variable instance closest to coordinates.
:rtype: dict or None
"""
instance = font.get_variable_instance_closest_to_coordinates(coordinates={"wght": 1000, "slnt": 815, "wdth": 775})
```

-   #### get_version
```python
"""
Gets the font version.

:returns: The font version value.
:rtype: float
"""
version = font.get_version()
```

-   #### get_weight
```python
"""
Gets the font weight value and name.

:returns: The weight name and value.
:rtype: dict or None
"""
weight = font.get_weight()
```

-   #### get_width
```python
"""
Gets the font width value and name.

:returns: The width name and value.
:rtype: dict or None
"""
width = font.get_width()
```

-   #### is_static
```python
"""
Determines if the font is a static font.

:returns: True if static font, False otherwise.
:rtype: bool
"""
static = font.is_static()
```

-   #### is_variable
```python
"""
Determines if the font is a variable font.

:returns: True if variable font, False otherwise.
:rtype: bool
"""
variable = font.is_variable()
```

-   #### rename
```python
"""
Renames the font names records (1, 2, 4, 6, 16, 17) according to
the given family_name and style_name (subfamily_name).

If family_name is not defined it will be auto-detected.
If style_name is not defined it will be auto-detected.

:param family_name: The family name
:type family_name: str
:param style_name: The style name
:type style_name: str
:param style_flags: if True the style flags will be updated by subfamily name
:type style_flags: bool

:raises ValueError: if the computed PostScript-name is longer than 63 characters.
"""
font.rename(family_name="My Font New", style_name="Bold Italic")
```

-   #### save
```python
"""
Saves the font at filepath.

:param filepath: The filepath, if None the source filepath will be used
:type filepath: str or None
:param overwrite: The overwrite, if True the source font file can be overwritten
:type overwrite: bool

:returns: The filepath where the font has been saved to.
:rtype: str

:raises ValueError: If the filepath is the same of the source font and overwrite is not allowed.
"""
saved_font_path = font.save(filepath=None, overwrite=False)
```

-   #### save_as_woff
```python
"""
Saves font as woff.

:param filepath: The filepath
:type filepath: str
:param overwrite: The overwrite, if True the source font file can be overwritten
:type overwrite: bool

:returns: The filepath where the font has been saved to.
:rtype: str
"""
saved_font_path = font.save_as_woff(filepath=None, overwrite=True)
```

-   #### save_as_woff2
```python
"""
Saves font as woff2.

:param filepath: The filepath
:type filepath: str
:param overwrite: The overwrite, if True the source font file can be overwritten
:type overwrite: bool

:returns: The filepath where the font has been saved to.
:rtype: str
"""
saved_font_path = font.save_as_woff2(filepath=None, overwrite=True)
```

-   #### set_name
```python
"""
Sets the name by its identifier in the font name table.

:param key: The name id or key (eg. "family_name")
:type key: int or str
:param value: The value
:type value: str
"""
font.set_name(Font.NAME_FAMILY_NAME, "Family Name Renamed")
```

-   #### set_names
```python
"""
Sets the names by their identifier in the name table.

:param names: The names
:type names: dict
"""
font.set_names(names={
    Font.NAME_FAMILY_NAME: "Family Name Renamed",
    Font.NAME_SUBFAMILY_NAME: "Regular Renamed",
})
```

-   #### set_style_flag
```python
"""
Sets the style flag.

:param key: The flag key
:type key: str
:param value: The value
:type value: bool
"""
font.set_style_flag(Font.STYLE_FLAG_BOLD, True)
```

-   #### set_style_flags
```python
"""
Sets the style flags, flags set to None will be ignored.

:param bold: The bold flag value.
:type bold: bool or None
:param italic: The italic flag value.
:type italic: bool or None
:param underline: The underline flag value.
:type underline: bool or None
:param outline: The outline flag value.
:type outline: bool or None
"""
font.set_style_flags(regular=None, bold=None, italic=None, outline=None, underline=None)
```

-   #### set_style_flags_by_subfamily_name
```python
"""
Sets the style flags by the subfamily name value.
The subfamily values should be "regular", "italic", "bold" or "bold italic"
to allow this method to work properly.
"""
font.set_style_flags_by_subfamily_name()
```

-   #### subset
```python
"""
Subsets the font using the given options (unicodes or glyphs or text),
it is possible to pass also subsetter options, more info here:
https://github.com/fonttools/fonttools/blob/main/Lib/fontTools/subset/__init__.py

:param unicodes: The unicodes
:type unicodes: str or list
:param glyphs: The glyphs
:type glyphs: list
:param text: The text
:type text: str
:param options: The subsetter options
:type options: dict
"""
font.subset(unicodes="", glyphs=[], text="", **options)
```

-   #### to_sliced_variable
```python
"""
Converts the variable font to a partial one slicing the variable axes at the given coordinates.
If an axis value is not specified, the axis will be left untouched.
If an axis min and max values are equal, the axis will be pinned.

:param coordinates: The coordinates dictionary, each item value must be tuple/list/dict (with min and max keys) for slicing or float/int for pinning, eg.
    {"wdth":100, "wght":(100,600), "ital":(30,70)} or
    {"wdth":100, "wght":[100,600], "ital":[30,70]} or
    {"wdth":100, "wght":{"min":100,"max":600}, "ital":{"min":30,"max":70}}
:type coordinates: dict
:param options: The options for the fontTools.varLib.instancer
:type options: dictionary

:raises TypeError: If the font is not a variable font
:raises ValueError: If the coordinates are not defined (empty)
:raises ValueError: If the coordinates axes are all pinned
"""
font.to_sliced_variable(coordinates, **options)
```

-   #### to_static
```python
"""
Converts the variable font to a static one pinning the variable axes at the given coordinates.
If an axis value is not specified, the axis will be pinned at its default value.
If coordinates are not specified each axis will be pinned at its default value.

:param coordinates: The coordinates, eg. {"wght":500, "ital":50}
:type coordinates: dict or None
:param options: The options for the fontTools.varLib.instancer
:type options: dictionary

:raises TypeError: If the font is not a variable font
:raises ValueError: If the coordinates axes are not all pinned
"""
font.to_static(coordinates=None, **options)
```

## Testing
```bash
# clone repository
git clone https://github.com/fabiocaccamo/python-fontbro.git && cd python-fontbro

# create virtualenv and activate it
python -m venv venv && . venv/bin/activate

# upgrade pip
python -m pip install --upgrade pip

# install requirements
pip install -r requirements.txt -r requirements-test.txt

# run tests using tox
tox

# or run tests using unittest
python -m unittest
```

## License
Released under [MIT License](LICENSE.txt).

## Credits
Special thanks to [Jérémie Hornus](https://github.com/JeremieHornus) and [Just Van Rossum](https://github.com/justvanrossum).

## Supporting
- :star: Star this project on [GitHub](https://github.com/fabiocaccamo/python-fontbro)
- :octocat: Follow me on [GitHub](https://github.com/fabiocaccamo)
- :blue_heart: Follow me on [Twitter](https://twitter.com/fabiocaccamo)
- :moneybag: Sponsor me on [Github](https://github.com/sponsors/fabiocaccamo)

## See also
- [`python-benedict`](https://github.com/fabiocaccamo/python-benedict) - dict subclass with keylist/keypath support, I/O shortcuts (base64, csv, json, pickle, plist, query-string, toml, xml, yaml) and many utilities. 📘
- [`python-fsutil`](https://github.com/fabiocaccamo/python-fsutil) - file-system utilities for lazy devs. 🧟‍♂️

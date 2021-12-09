# -*- coding: utf-8 -*-

from curses import ascii

from fontbro.features import FEATURES as _FEATURES_LIST
from fontbro.flags import get_flag, set_flag

from fontTools import unicodedata
from fontTools.subset import parse_unicodes, Subsetter
from fontTools.ttLib import TTFont, TTLibError
from fontTools.varLib import instancer
from fontTools.varLib.instancer import OverlapMode

import fsutil
import itertools
import math
import os
import sys


class Font(object):
    """
    friendly font operations.
    """

    # Features:
    # https://docs.microsoft.com/en-gb/typography/opentype/spec/featurelist
    # https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings
    _FEATURES_LIST = _FEATURES_LIST
    _FEATURES_BY_TAG = {feature['tag']: feature for feature in _FEATURES_LIST}

    # Formats:
    FORMAT_OTF = 'otf'
    FORMAT_TTF = 'ttf'
    FORMAT_WOFF = 'woff'
    FORMAT_WOFF2 = 'woff2'

    _FORMATS_LIST = [FORMAT_OTF, FORMAT_TTF, FORMAT_WOFF, FORMAT_WOFF2]

    # Names:
    NAME_COPYRIGHT_NOTICE = 'copyright_notice'
    NAME_FAMILY_NAME = 'family_name'
    NAME_SUBFAMILY_NAME = 'subfamily_name'
    NAME_UNIQUE_IDENTIFIER = 'unique_identifier'
    NAME_FULL_NAME = 'full_name'
    NAME_VERSION = 'version'
    NAME_POSTSCRIPT_NAME = 'postscript_name'
    NAME_TRADEMARK = 'trademark'
    NAME_MANUFACTURER_NAME = 'manufacturer_name'
    NAME_DESIGNER = 'designer'
    NAME_DESCRIPTION = 'description'
    NAME_VENDOR_URL = 'vendor_url'
    NAME_DESIGNER_URL = 'designer_url'
    NAME_LICENSE_DESCRIPTION = 'license_description'
    NAME_LICENSE_INFO_URL = 'license_info_url'
    NAME_RESERVED = 'reserved'
    NAME_TYPOGRAPHIC_FAMILY_NAME = 'typographic_family_name'
    NAME_TYPOGRAPHIC_SUBFAMILY_NAME = 'typographic_subfamily_name'
    NAME_COMPATIBLE_FULL = 'compatible_full'
    NAME_SAMPLE_TEXT = 'sample_text'
    NAME_POSTSCRIPT_CID_FINDFONT_NAME = 'postscript_cid_findfont_name'
    NAME_WWS_FAMILY_NAME = 'wws_family_name'
    NAME_WWS_SUBFAMILY_NAME = 'wws_subfamily_name'
    NAME_LIGHT_BACKGROUND_PALETTE = 'light_background_palette'
    NAME_DARK_BACKGROUND_PALETTE = 'dark_background_palette'
    NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX = 'variations_postscript_name_prefix'

    _NAMES = [
        {'id': 0, 'key': NAME_COPYRIGHT_NOTICE},
        {'id': 1, 'key': NAME_FAMILY_NAME},
        {'id': 2, 'key': NAME_SUBFAMILY_NAME},
        {'id': 3, 'key': NAME_UNIQUE_IDENTIFIER},
        {'id': 4, 'key': NAME_FULL_NAME},
        {'id': 5, 'key': NAME_VERSION},
        {'id': 6, 'key': NAME_POSTSCRIPT_NAME},
        {'id': 7, 'key': NAME_TRADEMARK},
        {'id': 8, 'key': NAME_MANUFACTURER_NAME},
        {'id': 9, 'key': NAME_DESIGNER},
        {'id': 10, 'key': NAME_DESCRIPTION},
        {'id': 11, 'key': NAME_VENDOR_URL},
        {'id': 12, 'key': NAME_DESIGNER_URL},
        {'id': 13, 'key': NAME_LICENSE_DESCRIPTION},
        {'id': 14, 'key': NAME_LICENSE_INFO_URL},
        {'id': 15, 'key': NAME_RESERVED},
        {'id': 16, 'key': NAME_TYPOGRAPHIC_FAMILY_NAME},
        {'id': 17, 'key': NAME_TYPOGRAPHIC_SUBFAMILY_NAME},
        {'id': 18, 'key': NAME_COMPATIBLE_FULL},
        {'id': 19, 'key': NAME_SAMPLE_TEXT},
        {'id': 20, 'key': NAME_POSTSCRIPT_CID_FINDFONT_NAME},
        {'id': 21, 'key': NAME_WWS_FAMILY_NAME},
        {'id': 22, 'key': NAME_WWS_SUBFAMILY_NAME},
        {'id': 23, 'key': NAME_LIGHT_BACKGROUND_PALETTE},
        {'id': 24, 'key': NAME_DARK_BACKGROUND_PALETTE},
        {'id': 25, 'key': NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX},
    ]
    _NAMES_BY_ID = {item['id']: item for item in _NAMES}
    _NAMES_BY_KEY = {item['key']: item for item in _NAMES}

    # Style Flags:
    # https://docs.microsoft.com/en-us/typography/opentype/spec/head
    # https://docs.microsoft.com/en-us/typography/opentype/spec/os2#fsselection
    STYLE_FLAG_REGULAR = 'regular'
    STYLE_FLAG_BOLD = 'bold'
    STYLE_FLAG_ITALIC = 'italic'
    STYLE_FLAG_UNDERLINE = 'underline'
    STYLE_FLAG_OUTLINE = 'outline'
    STYLE_FLAG_SHADOW = 'shadow'
    STYLE_FLAG_CONDENSED = 'condensed'
    STYLE_FLAG_EXTENDED = 'extended'
    _STYLE_FLAGS = {
        STYLE_FLAG_REGULAR: {'bit_head_mac': None, 'bit_os2_fs': 6},
        STYLE_FLAG_BOLD: {'bit_head_mac': 0, 'bit_os2_fs': 5},
        STYLE_FLAG_ITALIC: {'bit_head_mac': 1, 'bit_os2_fs': 0},
        STYLE_FLAG_UNDERLINE: {'bit_head_mac': 2, 'bit_os2_fs': None},
        STYLE_FLAG_OUTLINE: {'bit_head_mac': 3, 'bit_os2_fs': 3},
        STYLE_FLAG_SHADOW: {'bit_head_mac': 4, 'bit_os2_fs': None},
        STYLE_FLAG_CONDENSED: {'bit_head_mac': 5, 'bit_os2_fs': None},
        STYLE_FLAG_EXTENDED: {'bit_head_mac': 6, 'bit_os2_fs': None},
    }
    _STYLE_FLAGS_KEYS = _STYLE_FLAGS.keys()

    # Variable Axes:
    _VARIABLE_AXES = [
        {'tag': 'ital', 'name': 'Italic'},
        {'tag': 'opsz', 'name': 'Optical Size'},
        {'tag': 'slnt', 'name': 'Slant'},
        {'tag': 'wdth', 'name': 'Width'},
        {'tag': 'wght', 'name': 'Weight'},
        # https://fonts.google.com/variablefonts#axis-definitions
        {'tag': 'CASL', 'name': 'Casual'},
        {'tag': 'CRSV', 'name': 'Cursive'},
        {'tag': 'XPRN', 'name': 'Expression'},
        {'tag': 'FILL', 'name': 'Fill'},
        {'tag': 'GRAD', 'name': 'Grade'},
        {'tag': 'MONO', 'name': 'Monospace'},
        {'tag': 'SOFT', 'name': 'Softness'},
        {'tag': 'WONK', 'name': 'Wonky'},
    ]
    _VARIABLE_AXES_BY_TAG = {axis['tag']: axis for axis in _VARIABLE_AXES}

    # Weights:
    # https://docs.microsoft.com/en-us/typography/opentype/otspec170/os2#usweightclass
    WEIGHT_EXTRA_THIN = 'Extra-thin'  # (Hairline)
    WEIGHT_THIN = 'Thin'
    WEIGHT_EXTRA_LIGHT = 'Extra-light'  # (Ultra-light)
    WEIGHT_LIGHT = 'Light'
    WEIGHT_REGULAR = 'Regular'  # (Normal)
    WEIGHT_BOOK = 'Book'
    WEIGHT_MEDIUM = 'Medium'
    WEIGHT_SEMI_BOLD = 'Semi-bold'  # (Demi-bold)
    WEIGHT_BOLD = 'Bold'
    WEIGHT_EXTRA_BOLD = 'Extra-bold'  # (Ultra-bold)
    WEIGHT_BLACK = 'Black'  # (Heavy)
    WEIGHT_EXTRA_BLACK = 'Extra-black'  # (Nord)
    _WEIGHTS_BY_VALUE = {
        50: WEIGHT_EXTRA_THIN,
        100: WEIGHT_THIN,
        200: WEIGHT_EXTRA_LIGHT,
        300: WEIGHT_LIGHT,
        400: WEIGHT_REGULAR,
        450: WEIGHT_BOOK,
        500: WEIGHT_MEDIUM,
        600: WEIGHT_SEMI_BOLD,
        700: WEIGHT_BOLD,
        800: WEIGHT_EXTRA_BOLD,
        900: WEIGHT_BLACK,
        950: WEIGHT_EXTRA_BLACK,
    }

    # Widths:
    # https://docs.microsoft.com/en-us/typography/opentype/otspec170/os2#uswidthclass
    WIDTH_ULTRA_CONDENSED = 'Ultra-condensed'
    WIDTH_EXTRA_CONDENSED = 'Extra-condensed'
    WIDTH_CONDENSED = 'Condensed'
    WIDTH_SEMI_CONDENSED = 'Semi-condensed'
    WIDTH_MEDIUM = 'Medium'  # (Normal)
    WIDTH_SEMI_EXPANDED = 'Semi-expanded'
    WIDTH_EXPANDED = 'Expanded'
    WIDTH_EXTRA_EXPANDED = 'Extra-expanded'
    WIDTH_ULTRA_EXPANDED = 'Ultra-expanded'
    _WIDTHS_BY_VALUE = {
        1: WIDTH_ULTRA_CONDENSED,
        2: WIDTH_EXTRA_CONDENSED,
        3: WIDTH_CONDENSED,
        4: WIDTH_SEMI_CONDENSED,
        5: WIDTH_MEDIUM,
        6: WIDTH_SEMI_EXPANDED,
        7: WIDTH_EXPANDED,
        8: WIDTH_EXTRA_EXPANDED,
        9: WIDTH_ULTRA_EXPANDED,
    }

    def __init__(self, filepath):
        """
        Constructs a new Font instance loading a font file from the given filepath.

        :param filepath: The filepath from which to load the font
        :type filepath: string or None

        :raises ValueError: if the filepath is not a valid font path
        """
        super(Font, self).__init__()

        self._filepath = None
        self._ttfont = None

        if isinstance(filepath, str):
            self._init_with_filepath(filepath)
        else:
            filepath_type = type(filepath).__name__
            raise ValueError(
                f'Invalid filepath type: expected str, found {filepath_type}'
            )

    def _init_with_filepath(self, filepath):
        try:
            self._ttfont = TTFont(filepath)
            self._filepath = filepath
        except TTLibError:
            raise ValueError(f'Invalid font at filepath: {filepath}')

    def get_characters(self):
        """
        Gets the font characters.

        :returns: The characters.
        :rtype: generator of dicts
        """
        font = self.get_ttfont()
        cmap = font.getBestCmap()
        for code, char_name in cmap.items():
            char = chr(code)
            if ascii.iscntrl(char):
                continue
            name = ''
            try:
                name = unicodedata.name(char)
            except ValueError:
                pass
            yield {
                'character': char,
                'character_name': char_name,
                'code': code,
                'name': name,
            }

    def get_characters_count(self):
        """
        Gets the font characters count.

        :returns: The characters count.
        :rtype: int
        """
        return len(list(self.get_characters()))

    def get_features(self):
        """
        Gets the font opentype features.

        :returns: The features list.
        :rtype: list of dict
        """
        features_tags = self.get_features_tags()
        return [
            self._FEATURES_BY_TAG.get(features_tag).copy()
            for features_tag in features_tags
            if features_tag in self._FEATURES_BY_TAG
        ]

    def get_features_tags(self):
        """
        Gets the font opentype features tags.

        :returns: The features tags list.
        :rtype: list of str
        """
        font = self.get_ttfont()
        gsub = font.get('GSUB')
        if gsub:
            feature_record = gsub.table.FeatureList.FeatureRecord or []
            features_tags = [feature.FeatureTag for feature in feature_record]
            return features_tags
        return []

    def get_format(self, ignore_flavor=False):
        """
        Gets the font format: otf, ttf, woff, woff2.

        :param ignore_flavor: If True, the original format without compression will be returned.
        :type ignore_flavor: bool

        :returns: The format.
        :rtype: str or None
        """
        font = self.get_ttfont()
        version = font.sfntVersion
        flavor = font.flavor
        format = None
        if flavor in [self.FORMAT_WOFF, self.FORMAT_WOFF2] and not ignore_flavor:
            format = flavor
        elif version == 'OTTO' and 'CFF ' in font:
            format = self.FORMAT_OTF
        elif version == '\0\1\0\0':
            format = self.FORMAT_TTF
        elif version == 'wOFF':
            format = self.FORMAT_WOFF
        elif version == 'wOF2':
            format = self.FORMAT_WOFF2
        return format

    @classmethod
    def _get_name_id(cls, key):
        if isinstance(key, int):
            return key
        elif isinstance(key, str):
            return cls._NAMES_BY_KEY[key]['id']
        else:
            raise TypeError(
                f'Invalid key type, expected int or str, found {type(key).__name__}.'
            )

    def get_name(self, key):
        """
        Gets the name by its identifier from the font name table.

        :param key: The name id or key (eg. 'family_name')
        :type key: int or str

        :returns: The name.
        :rtype: str or None

        :raises KeyError: if the key is not a valid name key/id
        """
        font = self.get_ttfont()
        name_id = self._get_name_id(key)
        name_table = font['name']
        name = name_table.getName(name_id, 3, 1, 0x0409)
        return name.toUnicode() if name else None

    def get_names(self):
        """
        Gets the names records mapped by their property name.

        :returns: The names.
        :rtype: dict
        """
        font = self.get_ttfont()
        names_by_id = {record.nameID: f'{record}' for record in font['name'].names}
        names = {
            self._NAMES_BY_ID[name_id]['key']: value
            for name_id, value in names_by_id.items()
            if name_id in self._NAMES_BY_ID
        }
        return names

    @classmethod
    def get_script_by_character(cls, char):
        """
        Gets the script by character (even if not included in the font).

        :param char: The character
        :type char: str

        :returns: The script by character.
        :rtype: dict
        """
        return cls.get_script_by_code(ord(char))

    @classmethod
    def get_script_by_code(cls, code):
        """
        Gets the script by unicode code point (even if not included in the font).

        :param code: The code
        :type code: int

        :returns: The script by code.
        :rtype: dict
        """
        script_tag = unicodedata.script(code)
        return {
            'tag': script_tag,
            'name': unicodedata.script_name(script_tag),
            'block': unicodedata.block(code),
        }

    @classmethod
    def get_scripts_by_characters(cls, chars):
        """
        Gets the scripts by characters (even if not included in the font).

        :returns: The scripts.
        :rtype: list of dict
        """
        blocks_by_scripts_tags = {}
        for char in chars:
            script = cls.get_script_by_code(char['code'])
            script_tag = script['tag']
            script_block = script['block']
            if script_tag not in blocks_by_scripts_tags:
                blocks_by_scripts_tags[script_tag] = set()
            blocks_by_scripts_tags[script_tag].add(script_block)
        scripts_tags = sorted(blocks_by_scripts_tags.keys())
        scripts = [
            {
                'tag': script_tag,
                'name': unicodedata.script_name(script_tag),
                'blocks': sorted(blocks_by_scripts_tags[script_tag]),
            }
            for script_tag in scripts_tags
        ]
        return scripts

    def get_scripts(self):
        """
        Gets the scripts supported by the font.

        :returns: The scripts.
        :rtype: list of dict
        """
        return self.get_scripts_by_characters(chars=self.get_characters())

    def get_style_flag(self, key):
        """
        Gets the style flag reading OS/2 and macStyle tables.

        :param key: The key
        :type key: string

        :returns: The style flag.
        :rtype: bool
        """
        font = self.get_ttfont()
        bits = self._STYLE_FLAGS[key]
        bit_os2_fs = bits['bit_os2_fs']
        bit_head_mac = bits['bit_head_mac']
        # https://docs.microsoft.com/en-us/typography/opentype/spec/os2#fsselection
        flag_os2_fs = False
        if bit_os2_fs is not None:
            os2 = font.get('OS/2')
            if os2:
                flag_os2_fs = get_flag(os2.fsSelection, bit_os2_fs)
        # https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6head.html
        flag_head_mac = False
        if bit_head_mac is not None:
            head = font.get('head')
            if head:
                flag_head_mac = get_flag(head.macStyle, bit_head_mac)
        return flag_os2_fs or flag_head_mac

    def get_style_flags(self):
        """
        Gets the style flags reading OS/2 and macStyle tables.

        :returns: The dict representing the style flags.
        :rtype: dict
        """
        return {key: self.get_style_flag(key) for key in self._STYLE_FLAGS_KEYS}

    def get_ttfont(self):
        """
        Gets the wrapped TTFont instance.

        :returns: The TTFont instance.
        :rtype: TTFont
        """
        return self._ttfont

    def get_variable_axes(self):
        """
        Gets the font variable axes.

        :returns: The list of axes if the font is a variable font otherwise None.
        :rtype: list of dict or None
        """
        if not self.is_variable():
            return None
        font = self.get_ttfont()
        return [
            {
                'tag': axis.axisTag,
                'name': self._VARIABLE_AXES_BY_TAG.get(axis.axisTag, {}).get(
                    'name', axis.axisTag.title()
                ),
                'min_value': axis.minValue,
                'max_value': axis.maxValue,
                'default_value': axis.defaultValue,
            }
            for axis in font['fvar'].axes
        ]

    def get_variable_axis_by_tag(self, tag):
        """
        Gets a variable axis by tag.

        :param tag: The tag
        :type tag: string

        :returns: The variable axis by tag.
        :rtype: dict or None
        """
        axes = self.get_variable_axes()
        if axes:
            for axis in axes:
                if axis.get('tag') == tag:
                    return axis
        return None

    def get_variable_axes_tags(self):
        """
        Gets the variable axes tags.

        :returns: The variable axis tags.
        :rtype: list or None
        """
        if not self.is_variable():
            return None
        font = self.get_ttfont()
        return [axis.axisTag for axis in font['fvar'].axes]

    def get_variable_instances(self):
        """
        Gets the variable instances.

        :returns: The list of instances if the font is a variable font otherwise None.
        :rtype: list of dict or None
        """
        if not self.is_variable():
            return None
        font = self.get_ttfont()
        name_table = font['name']
        return [
            {
                'coordinates': instance.coordinates,
                'style_name': name_table.getDebugName(instance.subfamilyNameID),
            }
            for instance in font['fvar'].instances
        ]

    def get_variable_instance_closest_to_coordinates(self, coordinates):
        """
        Gets the variable instance closest to coordinates.
        eg. coordinates = {'wght': 1000, 'slnt': 815, 'wdth': 775}

        :param coordinates: The coordinates
        :type coordinates: dict

        :returns: The variable instance closest to coordinates.
        :rtype: dict or None
        """
        if not self.is_variable():
            return None

        def get_euclidean_distance(a, b):
            # https://en.wikipedia.org/wiki/Euclidean_distance#Higher_dimensions
            return math.sqrt(
                sum(
                    map(
                        lambda ab: math.pow(abs(ab[0] - ab[1]), 2),
                        list(itertools.zip_longest(a, b, fillvalue=0)),
                    )
                )
            )

        lookup_values = coordinates.values()
        instances = self.get_variable_instances()
        closest_instance_distance = sys.maxsize
        closest_instance = None
        for instance in instances:
            instance_values = instance['coordinates'].values()
            instance_distance = get_euclidean_distance(lookup_values, instance_values)
            if instance_distance < closest_instance_distance:
                closest_instance_distance = instance_distance
                closest_instance = instance
        return closest_instance

    def get_weight(self):
        """
        Gets the font weight value and name.

        :returns: The weight name and value.
        :rtype: dict or None
        """
        font = self.get_ttfont()
        os2 = font.get('OS/2')
        if not os2:
            return None
        weight = os2.usWeightClass
        weight = min(max(0, weight), 1000)
        weights = sorted(self._WEIGHTS_BY_VALUE.keys())
        closest_weight = min(weights, key=lambda weight_item: abs(weight_item - weight))
        weight_name = self._WEIGHTS_BY_VALUE.get(closest_weight)
        return {'name': weight_name, 'value': weight}

    def get_width(self):
        """
        Gets the font width value and name.

        :returns: The width name and value.
        :rtype: dict or None
        """
        font = self.get_ttfont()
        os2 = font.get('OS/2')
        if not os2:
            return None
        width = os2.usWidthClass
        width = min(max(0, width), 9)
        width_name = self._WIDTHS_BY_VALUE.get(width)
        return {'name': width_name, 'value': width}

    def is_static(self):
        """
        Determines if the font is a static font.

        :returns: True if static font, False otherwise.
        :rtype: bool
        """
        return not self.is_variable()

    def is_variable(self):
        """
        Determines if the font is a variable font.

        :returns: True if variable font, False otherwise.
        :rtype: bool
        """
        font = self.get_ttfont()
        return 'fvar' in font

    def rename(self, family_name='', style_name=''):
        """
        Renames the font names records (1, 2, 4, 6, 16, 17) according to
        the given family_name and style_name (subfamily_name).

        If family_name is not defined it will be auto-detected.
        If style_name is not defined it will be auto-detected.

        :param family_name: The family name
        :type family_name: str
        :param style_name: The style name
        :type style_name: str

        :raises ValueError: if the computed PostScript-name is longer than 63 characters.
        """
        family_name = (
            family_name
            or self.get_name(self.NAME_TYPOGRAPHIC_FAMILY_NAME)
            or self.get_name(self.NAME_FAMILY_NAME)
        )
        style_name = (
            style_name
            or self.get_name(self.NAME_TYPOGRAPHIC_SUBFAMILY_NAME)
            or self.get_name(self.NAME_SUBFAMILY_NAME)
        )
        full_name = f'{family_name} {style_name}'
        postscript_family_name = family_name.replace(' ', '')
        postscript_subfamily_name = style_name.replace(' ', '')
        postscript_name = f'{postscript_family_name}-{postscript_subfamily_name}'
        postscript_name_length = len(postscript_name)
        if postscript_name_length > 63:
            raise ValueError(
                'PostScript name max-length (63 characters) exceeded'
                f' ({postscript_name_length} characters).'
            )
        names = {
            self.NAME_FAMILY_NAME: family_name,
            self.NAME_SUBFAMILY_NAME: style_name,
            self.NAME_FULL_NAME: full_name,
            self.NAME_POSTSCRIPT_NAME: postscript_name,
            self.NAME_TYPOGRAPHIC_FAMILY_NAME: family_name,
            self.NAME_TYPOGRAPHIC_SUBFAMILY_NAME: style_name,
        }
        self.set_names(names=names)

    def save(self, filepath=None, overwrite=False):
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
        if filepath is None:
            filepath = self._filepath

        filepath_is_dir = fsutil.is_dir(filepath) or filepath.endswith(os.sep)
        filepath_is_font_file = (
            fsutil.get_file_extension(filepath) in self._FORMATS_LIST
        )
        if filepath_is_dir or not filepath_is_font_file:
            dirpath = filepath
            basename = fsutil.get_file_basename(self._filepath)
            extension = None
        else:
            dirpath, filename = fsutil.split_filepath(filepath)
            basename, extension = fsutil.split_filename(filename)

        format = self.get_format()
        extension = format
        filename = fsutil.join_filename(basename, extension)
        filepath = fsutil.join_filepath(dirpath, filename)
        if filepath == self._filepath and not overwrite:
            raise ValueError(
                'Invalid filepath, value cannot be the same of the initial filepath'
                ' to prevent accidental font files overwrites.'
            )
        fsutil.make_dirs_for_file(filepath)

        font = self.get_ttfont()
        font.save(filepath)
        return filepath

    def _save_with_flavor(self, flavor, filepath=None, overwrite=True):
        font = self.get_ttfont()
        presave_flavor = font.flavor
        font.flavor = flavor
        # save
        saved_font_filepath = self.save(filepath=filepath, overwrite=overwrite)
        # revert changes
        font.flavor = presave_flavor
        # return file path
        return saved_font_filepath

    def save_as_woff(self, filepath=None, overwrite=True):
        """
        Saves font as woff.

        :param filepath: The filepath
        :type filepath: str
        :param overwrite: The overwrite, if True the source font file can be overwritten
        :type overwrite: bool

        :returns: The filepath where the font has been saved to.
        :rtype: str
        """
        return self._save_with_flavor(
            flavor=self.FORMAT_WOFF, filepath=filepath, overwrite=overwrite
        )

    def save_as_woff2(self, filepath=None, overwrite=True):
        """
        Saves font as woff2.

        :param filepath: The filepath
        :type filepath: str
        :param overwrite: The overwrite, if True the source font file can be overwritten
        :type overwrite: bool

        :returns: The filepath where the font has been saved to.
        :rtype: str
        """
        return self._save_with_flavor(
            flavor=self.FORMAT_WOFF2, filepath=filepath, overwrite=overwrite
        )

    def set_name(self, key, value):
        """
        Sets the name by its identifier in the font name table.

        :param key: The name id or key (eg. 'family_name')
        :type key: int or str
        :param value: The value
        :type value: str
        """
        font = self.get_ttfont()
        name_id = self._get_name_id(key)
        name_table = font['name']
        # https://github.com/fonttools/fonttools/blob/main/Lib/fontTools/ttLib/tables/_n_a_m_e.py#L568
        name_table.setName(value, name_id, 3, 1, 0x0409)

    def set_names(self, names):
        """
        Sets the names by their identifier in the name table.

        :param names: The names
        :type names: dict
        """
        for key, value in names.items():
            self.set_name(key, value)

    def set_style_flag(self, key, value):
        """
        Sets the style flag.

        :param key: The flag key
        :type key: str
        :param value: The value
        :type value: bool
        """
        font = self.get_ttfont()
        bits = self._STYLE_FLAGS[key]
        bit_os2_fs = bits['bit_os2_fs']
        bit_head_mac = bits['bit_head_mac']
        if bit_os2_fs is not None:
            os2 = font.get('OS/2')
            if os2:
                os2.fsSelection = set_flag(os2.fsSelection, bit_os2_fs, value)
        if bit_head_mac is not None:
            head = font.get('head')
            if head:
                head.macStyle = set_flag(head.macStyle, bit_head_mac, value)

    def set_style_flags(
        self,
        regular=None,
        bold=None,
        italic=None,
        underline=None,
        outline=None,
        shadow=None,
        condensed=None,
        extended=None,
    ):
        """
        Sets the style flags, keys set to None will be ignored.

        :param regular: The regular style flag value
        :type regular: bool or None
        :param bold: The bold style flag value
        :type bold: bool or None
        :param italic: The italic style flag value
        :type italic: bool or None
        :param underline: The underline style flag value
        :type underline: bool or None
        :param outline: The outline style flag value
        :type outline: bool or None
        :param shadow: The shadow style flag value
        :type shadow: bool or None
        :param condensed: The condensed style flag value
        :type condensed: bool or None
        :param extended: The extended style flag value
        :type extended: bool or None
        """
        flags = locals()
        flags.pop('self')
        for key, value in flags.items():
            if value is not None:
                assert isinstance(value, bool)
                self.set_style_flag(key, value)

    def subset(self, unicodes='', glyphs=[], text='', **options):
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
        font = self.get_ttfont()
        if not any([unicodes, glyphs, text]):
            raise ValueError(
                'Subsetting requires at least one of the following args: unicode,'
                ' glyphs, text.'
            )
        if isinstance(unicodes, (list, set, tuple)):
            unicodes = ', '.join(list(unicodes))
        # replace possible — ‐ − (&mdash; &dash; &minus;) with -
        for s in ('—', '‐', '−'):
            unicodes = unicodes.replace(s, '-')
        unicodes = parse_unicodes(unicodes)
        # print(unicodes)
        subs_args = {'unicodes': unicodes, 'glyphs': glyphs, 'text': text}
        # https://github.com/fonttools/fonttools/blob/main/Lib/fontTools/subset/__init__.py
        subs = Subsetter(**options)
        subs.populate(**subs_args)
        subs.subset(font)

    @staticmethod
    def _all_axes_pinned(axes):
        """
        Check if all the axes values are pinned or not.

        :param axes: The axes
        :type axes: dict
        :returns: True if all the axes values are pinned, False otherwise.
        :rtype: bool
        """
        return all(
            [
                isinstance(axis_value, (type(None), int, float))
                for axis_value in axes.values()
            ]
        )

    def to_sliced_variable(self, coordinates, **options):
        """
        Converts the variable font to a partial one slicing the variable axes at the given coordinates.
        If an axis value is not specified, the axis will be left untouched.
        If an axis min and max values are equal, the axis will be pinned.

        :param coordinates: The coordinates dictionary, each item value must be tuple/list/dict (with min and max keys) for slicing or float/int for pinning, eg.
            {'wdth':100, 'wght':(100,600), 'ital':(30,70)} or
            {'wdth':100, 'wght':[100,600], 'ital':[30,70]} or
            {'wdth':100, 'wght':{'min':100,'max':600}, 'ital':{'min':30,'max':70}}
        :type coordinates: dict
        :param options: The options for the fontTools.varLib.instancer
        :type options: dictionary

        :raises TypeError: If the font is not a variable font
        :raises ValueError: If the coordinates are not defined (empty)
        :raises ValueError: If the coordinates axes are all pinned
        """
        if not self.is_variable():
            raise TypeError('Only a variable font can be sliced.')

        font = self.get_ttfont()
        coordinates = coordinates or {}
        coordinates_axes_tags = coordinates.keys()

        # make coordinates more friendly accepting also list and dict values
        for axis_tag in coordinates_axes_tags:
            axis_value = coordinates[axis_tag]
            if isinstance(axis_value, list):
                axis_value = tuple(axis_value)
            elif isinstance(axis_value, dict):
                axis = self.get_variable_axis_by_tag(axis_tag)
                axis_min = axis_value.get('min', axis.get('min_value'))
                axis_max = axis_value.get('max', axis.get('max_value'))
                axis_value = (axis_min, axis_max)
            coordinates[axis_tag] = axis_value

        # ensure that coordinates axes are defined and that are not all pinned
        if len(coordinates_axes_tags) == 0:
            raise ValueError('Invalid coordinates: axes not defined.')
        elif set(coordinates_axes_tags) == set(self.get_variable_axes_tags()):
            if self._all_axes_pinned(coordinates):
                raise ValueError(
                    'Invalid coordinates: all axes are pinned (use to_static method).'
                )

        # set default instancer options
        options.setdefault('optimize', True)
        options.setdefault('overlap', OverlapMode.KEEP_AND_SET_FLAGS)
        options.setdefault('updateFontNames', False)

        # instantiate the sliced variable font
        instancer.instantiateVariableFont(font, coordinates, inplace=True, **options)

    def to_static(self, coordinates=None, **options):
        """
        Converts the variable font to a static one pinning the variable axes at the given coordinates.
        If an axis value is not specified, the axis will be pinned at its default value.
        If coordinates are not specified each axis will be pinned at its default value.

        :param coordinates: The coordinates, eg. {'wght':500, 'ital':50}
        :type coordinates: dict or None
        :param options: The options for the fontTools.varLib.instancer
        :type options: dictionary

        :raises TypeError: If the font is not a variable font
        :raises ValueError: If the coordinates axes are not all pinned
        """
        if not self.is_variable():
            raise TypeError('Only a variable font can be made static.')

        font = self.get_ttfont()

        # make coordinates more friendly by using default axis values by default
        coordinates = coordinates or {}
        default_coordinates = {
            axis_tag: None
            for axis_tag in self.get_variable_axes_tags()
            if axis_tag not in coordinates
        }
        coordinates.update(default_coordinates)

        # ensure that coordinates axes are all pinned
        if not self._all_axes_pinned(coordinates):
            raise ValueError('Invalid coordinates: all axes must be pinned.')

        # set default instancer options
        options.setdefault('optimize', True)
        options.setdefault('overlap', OverlapMode.REMOVE)
        options.setdefault('updateFontNames', False)

        # instantiate the static font
        instancer.instantiateVariableFont(font, coordinates, inplace=True, **options)

    def __str__(self):
        """
        Returns a string representation of the object.

        :returns: String representation of the object.
        :rtype: str
        """
        return f'Font(\'{self._filepath}\')'

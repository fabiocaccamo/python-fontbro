# -*- coding: utf-8 -*-

from curses import ascii

from fontbro.features import FEATURES as _FEATURES_DATA

from fontTools import unicodedata
from fontTools.subset import parse_unicodes, Subsetter
from fontTools.ttLib import TTFont, TTLibError

import fsutil
import itertools
import math
import os
import sys


class Font(object):
    """
    human-friendly font operations.
    """

    # Features:
    # https://docs.microsoft.com/en-gb/typography/opentype/spec/featurelist
    # https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings
    _FEATURES = _FEATURES_DATA
    _FEATURES_DICT = {feature['tag']: feature for feature in _FEATURES}

    # Formats:
    FORMAT_OTF = 'otf'
    FORMAT_TTF = 'ttf'
    FORMAT_WOFF = 'woff'
    FORMAT_WOFF2 = 'woff2'

    _FORMATS_LIST = [FORMAT_OTF, FORMAT_TTF, FORMAT_WOFF, FORMAT_WOFF2]

    # Names:
    NAME_COPYRIGHT_NOTICE = 0
    NAME_FAMILY_NAME = 1
    NAME_SUBFAMILY_NAME = 2
    NAME_UNIQUE_IDENTIFIER = 3
    NAME_FULL_NAME = 4
    NAME_VERSION = 5
    NAME_POSTSCRIPT_NAME = 6
    NAME_TRADEMARK = 7
    NAME_MANUFACTURER_NAME = 8
    NAME_DESIGNER = 9
    NAME_DESCRIPTION = 10
    NAME_VENDOR_URL = 11
    NAME_DESIGNER_URL = 12
    NAME_LICENSE_DESCRIPTION = 13
    NAME_LICENSE_INFO_URL = 14
    NAME_RESERVED = 15
    NAME_TYPOGRAPHIC_FAMILY_NAME = 16
    NAME_TYPOGRAPHIC_SUBFAMILY_NAME = 17
    NAME_COMPATIBLE_FULL = 18
    NAME_SAMPLE_TEXT = 19
    NAME_POSTSCRIPT_CID_FINDFONT_NAME = 20
    NAME_WWS_FAMILY_NAME = 21
    NAME_WWS_SUBFAMILY_NAME = 22
    NAME_LIGHT_BACKGROUND_PALETTE = 23
    NAME_DARK_BACKGROUND_PALETTE = 24
    NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX = 25

    _NAMES_BY_ID = {
        NAME_COPYRIGHT_NOTICE: 'Copyright Notice',
        NAME_FAMILY_NAME: 'Family Name',
        NAME_SUBFAMILY_NAME: 'Subfamily Name',
        NAME_UNIQUE_IDENTIFIER: 'Unique Identifier',
        NAME_FULL_NAME: 'Full Name',
        NAME_VERSION: 'Version',
        NAME_POSTSCRIPT_NAME: 'PostScript Name',
        NAME_TRADEMARK: 'Trademark',
        NAME_MANUFACTURER_NAME: 'Manufacturer Name',
        NAME_DESIGNER: 'Designer',
        NAME_DESCRIPTION: 'Description',
        NAME_VENDOR_URL: 'Vendor URL',
        NAME_DESIGNER_URL: 'Designer URL',
        NAME_LICENSE_DESCRIPTION: 'License Description',
        NAME_LICENSE_INFO_URL: 'License Info URL',
        NAME_RESERVED: 'Reserved',
        NAME_TYPOGRAPHIC_FAMILY_NAME: 'Typographic Family Name',
        NAME_TYPOGRAPHIC_SUBFAMILY_NAME: 'Typographic Subfamily Name',
        NAME_COMPATIBLE_FULL: 'Compatible Full',
        NAME_SAMPLE_TEXT: 'Sample Text',
        NAME_POSTSCRIPT_CID_FINDFONT_NAME: 'PostScript CID findfont Name',
        NAME_WWS_FAMILY_NAME: 'WWS Family Name',
        NAME_WWS_SUBFAMILY_NAME: 'WWS Subfamily Name',
        NAME_LIGHT_BACKGROUND_PALETTE: 'Light Background Palette',
        NAME_DARK_BACKGROUND_PALETTE: 'Dark Background Palette',
        NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX: 'Variations PostScript Name Prefix',
    }
    _NAMES_BY_KEY = {
        name_str.lower().replace(' ', '_'): name_id
        for name_id, name_str in _NAMES_BY_ID.items()
    }

    # Style Flags:
    STYLE_FLAG_BOLD = 'bold'
    STYLE_FLAG_ITALIC = 'italic'
    STYLE_FLAG_OUTLINE = 'outline'
    STYLE_FLAG_REGULAR = 'regular'
    STYLE_FLAG_UNDERLINE = 'underline'

    _STYLE_FLAGS = {
        STYLE_FLAG_BOLD: {'bit_head_mac': 0, 'bit_os2_fs': 5},
        STYLE_FLAG_ITALIC: {'bit_head_mac': 1, 'bit_os2_fs': 0},
        STYLE_FLAG_OUTLINE: {'bit_head_mac': 3, 'bit_os2_fs': 3},
        STYLE_FLAG_REGULAR: {'bit_head_mac': None, 'bit_os2_fs': 6},
        STYLE_FLAG_UNDERLINE: {'bit_head_mac': 2, 'bit_os2_fs': 1},
    }
    _STYLE_FLAGS_KEYS = _STYLE_FLAGS.keys()

    # Variable Axes:
    _VARIABLE_AXES = [
        {'tag': 'ital', 'name': 'Italic'},
        {'tag': 'opsz', 'name': 'Optical Size'},
        {'tag': 'slnt', 'name': 'Slant'},
        {'tag': 'wdht', 'name': 'Width'},
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
    _VARIABLE_AXES_DICT = {axis['tag']: axis for axis in _VARIABLE_AXES}

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
    _WEIGHT_DICT = {
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
    _WIDTH_DICT = {
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

        :returns: The features.
        :rtype: list of dict
        """
        font = self.get_ttfont()
        gsub = font.get('GSUB')
        if gsub:
            feature_record = gsub.table.FeatureList.FeatureRecord or []
            features_tags = [feature.FeatureTag for feature in feature_record]
            return [
                self._FEATURES_DICT.get(features_tag).copy()
                for features_tag in features_tags
                if features_tag in self._FEATURES_DICT
            ]
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
        if flavor in [self.FORMAT_WOFF, self.FORMAT_WOFF2] and not ignore_flavor:
            return flavor
        elif version == 'OTTO' and 'CFF ' in font:
            return self.FORMAT_OTF
        elif version == '\0\1\0\0':
            return self.FORMAT_TTF
        elif version == 'wOFF':
            return self.FORMAT_WOFF
        elif version == 'wOF2':
            return self.FORMAT_WOFF2
        return None

    @classmethod
    def _get_name_id(cls, key):
        if isinstance(key, int):
            return key
        elif isinstance(key, str):
            return cls._NAMES_BY_KEY.get(key)
        else:
            raise TypeError(
                'Invalid name identifier type, expected int or str, found'
                f' {type(key).__name__}.'
            )

    def get_name(self, key):
        """
        Gets the name by its identifier from the font name table.

        :param key: The name id or key (eg. 'family_name')
        :type key: int or str

        :returns: The name.
        :rtype: str or None
        """
        name_id = self._get_name_id(key)
        font = self.get_ttfont()
        for record in font['name'].names:
            if record.nameID == name_id:
                return f'{record}'
        return None

    def get_names(self):
        """
        Gets the names records mapped by their property name.

        :returns: The names.
        :rtype: dict
        """
        font = self.get_ttfont()
        names_by_id = {record.nameID: f'{record}' for record in font['name'].names}
        names = {
            self._NAMES_BY_ID.get(key).lower().replace(' ', '_'): value
            for key, value in names_by_id.items()
            if key in self._NAMES_BY_ID
        }
        return names

    def get_script_by_character(self, char):
        """
        Gets the script by character.

        :param char: The character
        :type char: str

        :returns: The script by character.
        :rtype: dict
        """
        return self.get_script_by_code(ord(char))

    def get_script_by_code(self, code):
        """
        Gets the script by unicode code point.

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

    def get_scripts(self):
        """
        Gets the scripts supported by the font.

        :returns: The scripts.
        :rtype: list of dict
        """

        # TODO:
        # add script coverage (0.0 < coverage <= 1.0)
        # and coverage_threshold parameter.

        blocks_by_scripts_tags = {}
        for char in self.get_characters():
            script = self.get_script_by_code(char['code'])
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

    @classmethod
    def _get_bool_flag(self, bits, bit):
        return bool(bits & (1 << bit))

    def _get_style_flag_by_bits(self, bit_os2_fs, bit_head_mac):
        font = self.get_ttfont()
        # https://docs.microsoft.com/en-us/typography/opentype/spec/os2#fsselection
        flag_os2_fs = False
        if bit_os2_fs is not None:
            os2 = font.get('OS/2')
            if os2:
                flag_os2_fs = self._get_bool_flag(os2.fsSelection, bit_os2_fs)
        # https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6head.html
        flag_head_mac = False
        if bit_head_mac is not None:
            head = font.get('head')
            if head:
                flag_head_mac = self._get_bool_flag(head.macStyle, bit_head_mac)
        return flag_os2_fs or flag_head_mac

    def get_style_flags(self):
        """
        Gets the style flags reading OS/2 and macStyle tables.

        :returns: The dict representing the style flags.
        :rtype: dict
        """
        return {
            key: self._get_style_flag_by_bits(**self._STYLE_FLAGS.get(key))
            for key in self._STYLE_FLAGS_KEYS
        }

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
                'name': self._VARIABLE_AXES_DICT.get(axis.axisTag, {}).get(
                    'name', axis.axisTag.title()
                ),
                'minValue': axis.minValue,
                'maxValue': axis.maxValue,
                'defaultValue': axis.defaultValue,
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
        nameTable = font['name']
        return [
            {
                'coordinates': instance.coordinates,
                'postscriptName': nameTable.getDebugName(instance.postscriptNameID),
                'subfamilyName': nameTable.getDebugName(instance.subfamilyNameID),
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
        weights = sorted(self._WEIGHT_DICT.keys())
        closest_weight = min(weights, key=lambda weight_item: abs(weight_item - weight))
        weight_name = self._WEIGHT_DICT.get(closest_weight)
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
        width_name = self._WIDTH_DICT.get(width)
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
        name_id = self._get_name_id(key)
        font = self.get_ttfont()
        for record in font['name'].names:
            if record.nameID == name_id:
                record.string = str(value or '')
                return
        raise ValueError(f'Invalid name identifier: {name_id}')

    def set_names(self, names):
        """
        Sets the names by their identifier in the name table.

        :param names: The names
        :type names: dict
        """
        for key, value in names.items():
            self.set_name(key, value)

    @classmethod
    def _set_bool_flag(self, bits, bit, flag):
        mask = 1 << bit
        bits = bits | mask if flag else bits & ~mask
        return bits

    def _set_style_flag(self, flag, value):
        font = self.get_ttfont()
        bits = self._STYLE_FLAGS.get(flag)
        bit_os2_fs = bits.get('bit_os2_fs')
        bit_head_mac = bits.get('bit_head_mac')
        if bit_os2_fs is not None:
            os2 = font.get('OS/2')
            if os2:
                os2.fsSelection = self._set_bool_flag(
                    os2.fsSelection, bit_os2_fs, value
                )
        if bit_head_mac is not None:
            head = font.get('head')
            if head:
                head.macStyle = self._set_bool_flag(head.macStyle, bit_head_mac, value)

    def set_style_flags(
        self, regular=None, bold=None, italic=None, outline=None, underline=None
    ):
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
        flags = locals()
        flags.pop('self')
        for flag, value in flags.items():
            assert flag in self._STYLE_FLAGS_KEYS
            if isinstance(value, bool):
                self._set_style_flag(flag, value)

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

        # TODO: add scripts argument support to generate unicodes,
        # eg. scripts=[Font.SCRIPTS.LATIN, Font.SCRIPT_CYRILLIC]

        if isinstance(unicodes, (list, set, tuple)):
            unicodes = ', '.join(list(unicodes))
        dash = '-'
        mdash = '—'
        minus = '−'
        unicodes = unicodes.replace(mdash, dash).replace(minus, dash)
        unicodes = parse_unicodes(unicodes)
        # print(unicodes)
        subs_args = {'unicodes': unicodes, 'glyphs': glyphs, 'text': text}
        # https://github.com/fonttools/fonttools/blob/main/Lib/fontTools/subset/__init__.py
        subs = Subsetter(**options)
        subs.populate(**subs_args)
        subs.subset(font)

    def __str__(self):
        """
        Returns a string representation of the object.

        :returns: String representation of the object.
        :rtype: str
        """
        return f'Font("{self._filepath}")'

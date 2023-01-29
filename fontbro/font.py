import copy
import itertools
import math
import os
import re
import sys
import tempfile
from curses import ascii

import fsutil
from fontTools import unicodedata
from fontTools.subset import Options as SubsetterOptions
from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont, TTLibError
from fontTools.varLib import instancer
from fontTools.varLib.instancer import OverlapMode
from PIL import Image, ImageDraw, ImageFont

from fontbro.flags import get_flag, set_flag
from fontbro.subset import parse_unicodes
from fontbro.utils import concat_names, read_json, slugify


class Font:
    """
    friendly font operations on top of fontTools.
    """

    # Features:
    # https://docs.microsoft.com/en-gb/typography/opentype/spec/featurelist
    # https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings
    _FEATURES_LIST = read_json("data/features.json")
    _FEATURES_BY_TAG = {feature["tag"]: feature for feature in _FEATURES_LIST}

    # Formats:
    FORMAT_OTF = "otf"
    FORMAT_TTF = "ttf"
    FORMAT_WOFF = "woff"
    FORMAT_WOFF2 = "woff2"

    _FORMATS_LIST = [FORMAT_OTF, FORMAT_TTF, FORMAT_WOFF, FORMAT_WOFF2]

    # Names:
    NAME_COPYRIGHT_NOTICE = "copyright_notice"
    NAME_FAMILY_NAME = "family_name"
    NAME_SUBFAMILY_NAME = "subfamily_name"
    NAME_UNIQUE_IDENTIFIER = "unique_identifier"
    NAME_FULL_NAME = "full_name"
    NAME_VERSION = "version"
    NAME_POSTSCRIPT_NAME = "postscript_name"
    NAME_TRADEMARK = "trademark"
    NAME_MANUFACTURER_NAME = "manufacturer_name"
    NAME_DESIGNER = "designer"
    NAME_DESCRIPTION = "description"
    NAME_VENDOR_URL = "vendor_url"
    NAME_DESIGNER_URL = "designer_url"
    NAME_LICENSE_DESCRIPTION = "license_description"
    NAME_LICENSE_INFO_URL = "license_info_url"
    NAME_RESERVED = "reserved"
    NAME_TYPOGRAPHIC_FAMILY_NAME = "typographic_family_name"
    NAME_TYPOGRAPHIC_SUBFAMILY_NAME = "typographic_subfamily_name"
    NAME_COMPATIBLE_FULL = "compatible_full"
    NAME_SAMPLE_TEXT = "sample_text"
    NAME_POSTSCRIPT_CID_FINDFONT_NAME = "postscript_cid_findfont_name"
    NAME_WWS_FAMILY_NAME = "wws_family_name"
    NAME_WWS_SUBFAMILY_NAME = "wws_subfamily_name"
    NAME_LIGHT_BACKGROUND_PALETTE = "light_background_palette"
    NAME_DARK_BACKGROUND_PALETTE = "dark_background_palette"
    NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX = "variations_postscript_name_prefix"

    _NAMES = [
        {"id": 0, "key": NAME_COPYRIGHT_NOTICE},
        {"id": 1, "key": NAME_FAMILY_NAME},
        {"id": 2, "key": NAME_SUBFAMILY_NAME},
        {"id": 3, "key": NAME_UNIQUE_IDENTIFIER},
        {"id": 4, "key": NAME_FULL_NAME},
        {"id": 5, "key": NAME_VERSION},
        {"id": 6, "key": NAME_POSTSCRIPT_NAME},
        {"id": 7, "key": NAME_TRADEMARK},
        {"id": 8, "key": NAME_MANUFACTURER_NAME},
        {"id": 9, "key": NAME_DESIGNER},
        {"id": 10, "key": NAME_DESCRIPTION},
        {"id": 11, "key": NAME_VENDOR_URL},
        {"id": 12, "key": NAME_DESIGNER_URL},
        {"id": 13, "key": NAME_LICENSE_DESCRIPTION},
        {"id": 14, "key": NAME_LICENSE_INFO_URL},
        {"id": 15, "key": NAME_RESERVED},
        {"id": 16, "key": NAME_TYPOGRAPHIC_FAMILY_NAME},
        {"id": 17, "key": NAME_TYPOGRAPHIC_SUBFAMILY_NAME},
        {"id": 18, "key": NAME_COMPATIBLE_FULL},
        {"id": 19, "key": NAME_SAMPLE_TEXT},
        {"id": 20, "key": NAME_POSTSCRIPT_CID_FINDFONT_NAME},
        {"id": 21, "key": NAME_WWS_FAMILY_NAME},
        {"id": 22, "key": NAME_WWS_SUBFAMILY_NAME},
        {"id": 23, "key": NAME_LIGHT_BACKGROUND_PALETTE},
        {"id": 24, "key": NAME_DARK_BACKGROUND_PALETTE},
        {"id": 25, "key": NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX},
    ]
    _NAMES_BY_ID = {item["id"]: item for item in _NAMES}
    _NAMES_BY_KEY = {item["key"]: item for item in _NAMES}
    _NAMES_MAC_IDS = {"platformID": 3, "platEncID": 1, "langID": 0x409}
    _NAMES_WIN_IDS = {"platformID": 1, "platEncID": 0, "langID": 0x0}

    # Style Flags:
    # https://docs.microsoft.com/en-us/typography/opentype/spec/head
    # https://docs.microsoft.com/en-us/typography/opentype/spec/os2#fsselection
    STYLE_FLAG_REGULAR = "regular"
    STYLE_FLAG_BOLD = "bold"
    STYLE_FLAG_ITALIC = "italic"
    STYLE_FLAG_UNDERLINE = "underline"
    STYLE_FLAG_OUTLINE = "outline"
    STYLE_FLAG_SHADOW = "shadow"
    STYLE_FLAG_CONDENSED = "condensed"
    STYLE_FLAG_EXTENDED = "extended"
    _STYLE_FLAGS = {
        STYLE_FLAG_REGULAR: {"bit_head_mac": None, "bit_os2_fs": 6},
        STYLE_FLAG_BOLD: {"bit_head_mac": 0, "bit_os2_fs": 5},
        STYLE_FLAG_ITALIC: {"bit_head_mac": 1, "bit_os2_fs": 0},
        STYLE_FLAG_UNDERLINE: {"bit_head_mac": 2, "bit_os2_fs": None},
        STYLE_FLAG_OUTLINE: {"bit_head_mac": 3, "bit_os2_fs": 3},
        STYLE_FLAG_SHADOW: {"bit_head_mac": 4, "bit_os2_fs": None},
        STYLE_FLAG_CONDENSED: {"bit_head_mac": 5, "bit_os2_fs": None},
        STYLE_FLAG_EXTENDED: {"bit_head_mac": 6, "bit_os2_fs": None},
    }
    _STYLE_FLAGS_KEYS = _STYLE_FLAGS.keys()

    # Unicode blocks/scripts data:
    _UNICODE_BLOCKS = read_json("data/unicode-blocks.json")
    _UNICODE_SCRIPTS = read_json("data/unicode-scripts.json")

    # Variable Axes:
    _VARIABLE_AXES = [
        {"tag": "ital", "name": "Italic"},
        {"tag": "opsz", "name": "Optical Size"},
        {"tag": "slnt", "name": "Slant"},
        {"tag": "wdth", "name": "Width"},
        {"tag": "wght", "name": "Weight"},
        # https://fonts.google.com/variablefonts#axis-definitions
        {"tag": "CASL", "name": "Casual"},
        {"tag": "CRSV", "name": "Cursive"},
        {"tag": "XPRN", "name": "Expression"},
        {"tag": "FILL", "name": "Fill"},
        {"tag": "GRAD", "name": "Grade"},
        {"tag": "MONO", "name": "Monospace"},
        {"tag": "SOFT", "name": "Softness"},
        {"tag": "WONK", "name": "Wonky"},
    ]
    _VARIABLE_AXES_BY_TAG = {axis["tag"]: axis for axis in _VARIABLE_AXES}

    # Weights:
    # https://docs.microsoft.com/en-us/typography/opentype/otspec170/os2#usweightclass
    WEIGHT_EXTRA_THIN = "Extra-thin"  # (Hairline)
    WEIGHT_THIN = "Thin"
    WEIGHT_EXTRA_LIGHT = "Extra-light"  # (Ultra-light)
    WEIGHT_LIGHT = "Light"
    WEIGHT_REGULAR = "Regular"  # (Normal)
    WEIGHT_BOOK = "Book"
    WEIGHT_MEDIUM = "Medium"
    WEIGHT_SEMI_BOLD = "Semi-bold"  # (Demi-bold)
    WEIGHT_BOLD = "Bold"
    WEIGHT_EXTRA_BOLD = "Extra-bold"  # (Ultra-bold)
    WEIGHT_BLACK = "Black"  # (Heavy)
    WEIGHT_EXTRA_BLACK = "Extra-black"  # (Nord)
    _WEIGHTS = [
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
    _WEIGHTS_BY_VALUE = {weight["value"]: weight for weight in _WEIGHTS}

    # Widths:
    # https://docs.microsoft.com/en-us/typography/opentype/otspec170/os2#uswidthclass
    WIDTH_ULTRA_CONDENSED = "Ultra-condensed"
    WIDTH_EXTRA_CONDENSED = "Extra-condensed"
    WIDTH_CONDENSED = "Condensed"
    WIDTH_SEMI_CONDENSED = "Semi-condensed"
    WIDTH_MEDIUM = "Medium"  # (Normal)
    WIDTH_SEMI_EXPANDED = "Semi-expanded"
    WIDTH_EXPANDED = "Expanded"
    WIDTH_EXTRA_EXPANDED = "Extra-expanded"
    WIDTH_ULTRA_EXPANDED = "Ultra-expanded"
    _WIDTHS = [
        {"value": 1, "perc": 50.0, "name": WIDTH_ULTRA_CONDENSED},
        {"value": 2, "perc": 62.5, "name": WIDTH_EXTRA_CONDENSED},
        {"value": 3, "perc": 75.0, "name": WIDTH_CONDENSED},
        {"value": 4, "perc": 87.5, "name": WIDTH_SEMI_CONDENSED},
        {"value": 5, "perc": 100.0, "name": WIDTH_MEDIUM},
        {"value": 6, "perc": 112.5, "name": WIDTH_SEMI_EXPANDED},
        {"value": 7, "perc": 125.0, "name": WIDTH_EXPANDED},
        {"value": 8, "perc": 150.0, "name": WIDTH_EXTRA_EXPANDED},
        {"value": 9, "perc": 200.0, "name": WIDTH_ULTRA_CONDENSED},
    ]
    _WIDTHS_BY_VALUE = {width["value"]: width for width in _WIDTHS}

    def __init__(self, filepath, **kwargs):
        """
        Constructs a new Font instance loading a font file from the given filepath.

        :param filepath: The filepath from which to load the font
        :type filepath: string or None

        :raises ValueError: if the filepath is not a valid font path
        """
        super().__init__()

        self._filepath = None
        self._kwargs = None
        self._ttfont = None

        if isinstance(filepath, str):
            self._init_with_filepath(filepath, **kwargs)
        else:
            filepath_type = type(filepath).__name__
            raise ValueError(
                f"Invalid filepath type: expected str, found '{filepath_type}'."
            )

    def _init_with_filepath(self, filepath, **kwargs):
        try:
            self._filepath = filepath
            self._kwargs = kwargs
            self._ttfont = TTFont(self._filepath, **kwargs)

        except TTLibError:
            raise ValueError(f"Invalid font at filepath: '{filepath}'.")

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        self.close()

    def clone(self):
        """
        Creates a new Font instance reading the same binary file.
        """
        return Font(self._filepath, **self._kwargs)

    def close(self):
        """
        Close the wrapped TTFont instance.
        """
        font = self.get_ttfont()
        font.close()

    def get_characters(self, ignore_blank=False):
        """
        Gets the font characters.

        :param ignore_blank: If True, characters without contours will not be returned.
        :type ignore_blank: bool

        :returns: The characters.
        :rtype: generator of dicts

        :raises TypeError: If it's not possible to find the 'best' unicode cmap dict in the font.
        """
        font = self.get_ttfont()
        cmap = font.getBestCmap()
        if cmap is None:
            raise TypeError("Unable to find the 'best' unicode cmap dict.")
        glyfs = font.get("glyf")
        for code, char_name in cmap.items():
            code_hex = f"{code:04X}"
            if 0 <= code < 0x110000:
                char = chr(code)
            else:
                continue
            if ascii.iscntrl(char):
                continue
            if glyfs and ignore_blank:
                glyf = glyfs.get(char_name)
                if glyf and glyf.numberOfContours == 0:
                    continue
            unicode_name = unicodedata.name(char, None)
            unicode_block_name = unicodedata.block(code)
            unicode_script_tag = unicodedata.script(code)
            unicode_script_name = unicodedata.script_name(unicode_script_tag)
            yield {
                "character": char,
                "character_name": char_name,
                "code": code,
                "escape_sequence": f"\\u{code_hex}",
                "html_code": f"&#{code};",
                "unicode": f"U+{code_hex}",
                "unicode_code": code,
                "unicode_name": unicode_name,
                "unicode_block_name": unicode_block_name,
                "unicode_script_name": unicode_script_name,
                "unicode_script_tag": unicode_script_tag,
            }

    def get_characters_count(self, ignore_blank=False):
        """
        Gets the font characters count.

        :param ignore_blank: If True, characters without contours will not be counted.
        :type ignore_blank: bool

        :returns: The characters count.
        :rtype: int
        """
        return len(list(self.get_characters(ignore_blank=ignore_blank)))

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
        features_tags = set()
        for table_tag in ["GPOS", "GSUB"]:
            if table_tag in font:
                table = font[table_tag].table
                try:
                    feature_record = table.FeatureList.FeatureRecord or []
                except AttributeError:
                    feature_record = []
                for feature in feature_record:
                    features_tags.add(feature.FeatureTag)
        return sorted(features_tags)

    def get_fingerprint(self, text=""):
        """
        Gets the font fingerprint: an hash calculated from an image representation of the font.
        Changing the text option affects the returned fingerprint.

        :param text: The text used for generating the fingerprint, default value: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789".
        :type text: str

        :returns: The fingerprint hash.
        :rtype: imagehash.ImageHash
        """
        import imagehash

        text = text or "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

        img = self.get_image(text=text, size=72)
        img_size = img.size
        img = img.resize((img_size[0] // 2, img_size[1] // 2))
        img = img.resize((img_size[0], img_size[1]), Image.Resampling.NEAREST)
        img = img.quantize(colors=8)
        # img.show()

        hash = imagehash.average_hash(img, hash_size=64)
        return hash

    def get_fingerprint_match(self, other, tolerance=10, text=""):
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
        other_font = None
        if isinstance(other, str):
            other_font = Font(other)
        elif isinstance(other, Font):
            other_font = other
        else:
            other_type = type(other).__name__
            raise ValueError(
                f"Invalid other filepath/font: expected str or Font instance, found '{other_type}'."
            )
        hash = self.get_fingerprint(text=text)
        other_hash = other_font.get_fingerprint(text=text)
        diff = hash - other_hash
        match = diff <= tolerance
        match = match and self.is_variable() == other_font.is_variable()
        return (match, diff, hash, other_hash)

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
        elif version == "OTTO" and "CFF " in font:
            format = self.FORMAT_OTF
        elif version == "\0\1\0\0":
            format = self.FORMAT_TTF
        elif version == "wOFF":
            format = self.FORMAT_WOFF
        elif version == "wOF2":
            format = self.FORMAT_WOFF2
        return format

    def get_glyphs(self):
        """
        Gets the font glyphs and their own composition.

        :returns: The glyphs.
        :rtype: generator of dicts
        """
        font = self.get_ttfont()
        glyfs = font["glyf"]
        glyphset = font.getGlyphSet()
        for name in glyphset.keys():
            glyf = glyfs[name]
            yield {
                "name": name,
                "components_names": glyf.getComponentNames(glyfs),
            }

    def get_glyphs_count(self):
        """
        Gets the font glyphs count.

        :returns: The glyphs count.
        :rtype: int
        """
        font = self.get_ttfont()
        glyphset = font.getGlyphSet()
        count = len(glyphset)
        return count

    def get_image(
        self, text, size, color=(0, 0, 0, 255), background_color=(255, 255, 255, 255)
    ):
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

        :returns: The image.
        :rtype: PIL.Image
        """
        with tempfile.TemporaryDirectory() as dest:
            filepath = self.save(dest)
            img = Image.new("RGBA", (2, 2), background_color)
            draw = ImageDraw.Draw(img)
            img_font = ImageFont.truetype(filepath, size)
            img_bbox = draw.textbbox((0, 0), text, font=img_font)
            img_width = img_bbox[2] - img_bbox[0]
            img_height = img_bbox[3] - img_bbox[1]
            img_size = (img_width, img_height)
            img = img.resize(img_size)
            draw = ImageDraw.Draw(img)
            draw.text((-img_bbox[0], -img_bbox[1]), text, font=img_font, fill=color)
            del img_font
            return img

    def get_italic_angle(self):
        """
        Gets the font italic angle.

        :returns: The angle value including backslant, italic and roman flags.
        :rtype: dict or None
        """
        font = self.get_ttfont()
        post = font.get("post")
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

    @classmethod
    def _get_name_id(cls, key):
        if isinstance(key, int):
            return key
        elif isinstance(key, str):
            return cls._NAMES_BY_KEY[key]["id"]
        else:
            raise TypeError(
                f"Invalid key type, expected int or str, found '{type(key).__name__}'."
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
        name_table = font["name"]
        name = name_table.getName(name_id, **self._NAMES_MAC_IDS)
        if not name:
            name = name_table.getName(name_id, **self._NAMES_WIN_IDS)
        return name.toUnicode() if name else None

    def get_names(self):
        """
        Gets the names records mapped by their property name.

        :returns: The names.
        :rtype: dict
        """
        font = self.get_ttfont()
        names_by_id = {record.nameID: f"{record}" for record in font["name"].names}
        names = {
            self._NAMES_BY_ID[name_id]["key"]: value
            for name_id, value in names_by_id.items()
            if name_id in self._NAMES_BY_ID
        }
        return names

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
        bit_os2_fs = bits["bit_os2_fs"]
        bit_head_mac = bits["bit_head_mac"]
        # https://docs.microsoft.com/en-us/typography/opentype/spec/os2#fsselection
        flag_os2_fs = False
        if bit_os2_fs is not None:
            os2 = font.get("OS/2")
            if os2:
                flag_os2_fs = get_flag(os2.fsSelection, bit_os2_fs)
        # https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6head.html
        flag_head_mac = False
        if bit_head_mac is not None:
            head = font.get("head")
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

    @classmethod
    def _populate_unicode_items_set(cls, items, items_cache, item):
        item_key = item["name"]
        if item_key not in items_cache:
            item = item.copy()
            item["characters_count"] = 0
            items_cache[item_key] = item
            items.append(item)
        item = items_cache[item_key]
        item["characters_count"] += 1

    @staticmethod
    def _get_unicode_items_set_with_coverage(all_items, items, coverage_threshold=0.0):
        all_items = copy.deepcopy(all_items)
        items_indexed = {item["name"]: item.copy() for item in items}
        for item in all_items:
            item_key = item["name"]
            if item_key in items_indexed:
                item["characters_count"] = items_indexed[item_key]["characters_count"]
                item["coverage"] = item["characters_count"] / item["characters_total"]
            else:
                item["characters_count"] = 0
                item["coverage"] = 0.0
        items_filtered = [
            item for item in all_items if item["coverage"] >= coverage_threshold
        ]
        # items_filtered.sort(key=lambda item: item['name'])
        return items_filtered

    def get_unicode_block_by_name(self, name):
        """
        Gets the unicode block by name (name is case-insensitive and ignores "-").

        :param name: The name
        :type name: str

        :returns: The unicode block dict if the name is valid, None otherwise.
        :rtype: dict or None
        """
        blocks = self.get_unicode_blocks(coverage_threshold=0.0)
        for block in blocks:
            if slugify(name) == slugify(block["name"]):
                return block
        # raise KeyError("Invalid unicode block name: '{name}'")
        return None

    def get_unicode_blocks(self, coverage_threshold=0.00001):
        """
        Gets the unicode blocks and their coverage.
        Only blocks with coverage >= coverage_threshold (0.0 <= coverage_threshold <= 1.0) will be returned.

        :param coverage_threshold: The minumum required coverage for a block to be returned.
        :type coverage_threshold: float

        :returns: The list of unicode blocks.
        :rtype: list of dicts
        """
        items = []
        items_cache = {}
        for char in self.get_characters():
            item = {
                "name": char["unicode_block_name"],
            }
            self._populate_unicode_items_set(items, items_cache, item)
        blocks = self._get_unicode_items_set_with_coverage(
            self._UNICODE_BLOCKS, items, coverage_threshold=coverage_threshold
        )
        return blocks

    def get_unicode_script_by_name(self, name):
        """
        Gets the unicode script by name/tag (name/tag is case-insensitive and ignores "-").

        :param name: The name
        :type name: str

        :returns: The unicode script dict if the name/tag is valid, None otherwise.
        :rtype: dict or None
        """
        scripts = self.get_unicode_scripts(coverage_threshold=0.0)
        for script in scripts:
            if slugify(name) in (slugify(script["name"]), slugify(script["tag"])):
                return script
        # raise KeyError("Invalid unicode script name/tag: '{name}'")
        return None

    def get_unicode_scripts(self, coverage_threshold=0.00001):
        """
        Gets the unicode scripts and their coverage.
        Only scripts with coverage >= coverage_threshold (0.0 <= coverage_threshold <= 1.0) will be returned.

        :param coverage_threshold: The minumum required coverage for a script to be returned.
        :type coverage_threshold: float

        :returns: The list of unicode scripts.
        :rtype: list of dicts
        """
        items = []
        items_cache = {}
        for char in self.get_characters():
            item = {
                "name": char["unicode_script_name"],
                "tag": char["unicode_script_tag"],
            }
            self._populate_unicode_items_set(items, items_cache, item)
        scripts = self._get_unicode_items_set_with_coverage(
            self._UNICODE_SCRIPTS, items, coverage_threshold=coverage_threshold
        )
        return scripts

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
                "tag": axis.axisTag,
                "name": self._VARIABLE_AXES_BY_TAG.get(axis.axisTag, {}).get(
                    "name", axis.axisTag.title()
                ),
                "min_value": axis.minValue,
                "max_value": axis.maxValue,
                "default_value": axis.defaultValue,
            }
            for axis in font["fvar"].axes
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
                if axis.get("tag") == tag:
                    return axis
        # raise KeyError("Invalid axis tag: '{tag}'")
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
        return [axis.axisTag for axis in font["fvar"].axes]

    def get_variable_instances(self):
        """
        Gets the variable instances.

        :returns: The list of instances if the font is a variable font otherwise None.
        :rtype: list of dict or None
        """
        if not self.is_variable():
            return None
        font = self.get_ttfont()
        name_table = font["name"]
        return [
            {
                "coordinates": instance.coordinates,
                "style_name": name_table.getDebugName(instance.subfamilyNameID),
            }
            for instance in font["fvar"].instances
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
            instance_values = instance["coordinates"].values()
            instance_distance = get_euclidean_distance(lookup_values, instance_values)
            if instance_distance < closest_instance_distance:
                closest_instance_distance = instance_distance
                closest_instance = instance
        return closest_instance

    def get_version(self):
        """
        Gets the font version.

        :returns: The font version value.
        :rtype: float
        """
        font = self.get_ttfont()
        head = font.get("head")
        version = head.fontRevision
        return version

    def get_weight(self):
        """
        Gets the font weight value and name.

        :returns: The weight name and value.
        :rtype: dict or None
        """
        font = self.get_ttfont()
        os2 = font.get("OS/2")
        if not os2:
            return None
        weight_value = os2.usWeightClass
        weight_value = min(max(1, weight_value), 1000)
        weight_option_values = sorted(self._WEIGHTS_BY_VALUE.keys())
        closest_weight_option_value = min(
            weight_option_values,
            key=lambda weight_option_value: abs(weight_option_value - weight_value),
        )
        weight = self._WEIGHTS_BY_VALUE.get(closest_weight_option_value, {}).copy()
        weight["value"] = weight_value
        return weight

    def get_width(self):
        """
        Gets the font width value and name.

        :returns: The width name and value.
        :rtype: dict or None
        """
        font = self.get_ttfont()
        os2 = font.get("OS/2")
        if not os2:
            return None
        width_value = os2.usWidthClass
        width_value = min(max(1, width_value), 9)
        width = self._WIDTHS_BY_VALUE.get(width_value, {}).copy()
        width["value"] = width_value
        return width

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
        return "fvar" in font

    def rename(self, family_name="", style_name="", style_flags=True):
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
        family_name = family_name or ""
        family_name = (
            family_name.strip()
            or self.get_name(self.NAME_TYPOGRAPHIC_FAMILY_NAME)
            or self.get_name(self.NAME_WWS_FAMILY_NAME)
            or self.get_name(self.NAME_FAMILY_NAME)
        )
        style_name = style_name or ""
        style_name = (
            style_name.strip()
            or self.get_name(self.NAME_TYPOGRAPHIC_SUBFAMILY_NAME)
            or self.get_name(self.NAME_WWS_SUBFAMILY_NAME)
            or self.get_name(self.NAME_SUBFAMILY_NAME)
        )

        # typographic and wws names
        typographic_family_name = family_name
        typographic_subfamily_name = style_name
        wws_family_name = family_name
        wws_subfamily_name = style_name

        # family name, subfamily name and full name
        family_name_parts = [family_name]
        style_name_parts = style_name.split()
        subfamily_name_parts = style_name.lower().split()
        subfamily_names = ["regular", "italic", "bold", "bold italic"]
        subfamily_name_default = subfamily_names[0]
        for name_part in style_name_parts:
            if name_part.lower() not in subfamily_names:
                family_name_parts.append(name_part)
                subfamily_name_parts.remove(name_part.lower())
        if subfamily_name_default in subfamily_name_parts:
            if len(subfamily_name_parts) > 1:
                subfamily_name_parts.remove(subfamily_name_default)
        subfamily_name_parts = subfamily_name_parts or [subfamily_name_default]
        family_name = " ".join(family_name_parts)
        subfamily_name = " ".join(subfamily_name_parts).lower()
        if subfamily_name not in subfamily_names:
            subfamily_name = subfamily_name_default

        subfamily_name = subfamily_name.title()

        # full name
        full_name = concat_names(family_name, subfamily_name)

        # postscript name
        postscript_name = concat_names(
            typographic_family_name.replace(" ", ""),
            typographic_subfamily_name.replace(" ", ""),
        )

        # keep only printable ASCII subset: https://learn.microsoft.com/en-us/typography/opentype/spec/name#name-ids
        # postscript_name_allowed_chars = {chr(code) for code in range(33, 127)} - {"[", "]", "(", ")", "{", "}", "<", ">", "/", "%"}
        # !"#$&'*+,-.0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\^_`abcdefghijklmnopqrstuvwxyz|~
        postscript_name_pattern = (
            r"[^0-9A-Za-z\!\"\#\$\&\'\*\+\,\-\.\:\;\=\?\@\\\^\_\`\|\~]"
        )
        postscript_name = re.sub(postscript_name_pattern, "-", postscript_name)
        postscript_name = re.sub(r"[\-]+", "-", postscript_name).strip("-")
        postscript_name_length = len(postscript_name)
        if postscript_name_length > 63:
            raise ValueError(
                "PostScript name max-length (63 characters) exceeded"
                f" ({postscript_name_length} characters)."
            )

        # update name records
        names = {
            self.NAME_FAMILY_NAME: family_name,
            self.NAME_SUBFAMILY_NAME: subfamily_name,
            self.NAME_FULL_NAME: full_name,
            self.NAME_POSTSCRIPT_NAME: postscript_name,
            self.NAME_TYPOGRAPHIC_FAMILY_NAME: typographic_family_name,
            self.NAME_TYPOGRAPHIC_SUBFAMILY_NAME: typographic_subfamily_name,
            self.NAME_WWS_FAMILY_NAME: wws_family_name,
            self.NAME_WWS_SUBFAMILY_NAME: wws_subfamily_name,
        }
        self.set_names(names=names)

        if style_flags:
            self.set_style_flags_by_subfamily_name()

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
        if fsutil.is_file(filepath) and not overwrite:
            raise ValueError(
                f"Invalid filepath, a file already exists at '{filepath}' "
                "and 'overwrite' option is 'False' (consider using 'overwrite=True')."
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
        name_table = font["name"]
        # https://github.com/fonttools/fonttools/blob/main/Lib/fontTools/ttLib/tables/_n_a_m_e.py#L568
        name_table.setName(value, name_id, **self._NAMES_MAC_IDS)
        name_table.setName(value, name_id, **self._NAMES_WIN_IDS)

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
        bit_os2_fs = bits["bit_os2_fs"]
        bit_head_mac = bits["bit_head_mac"]
        if bit_os2_fs is not None:
            os2 = font.get("OS/2")
            if os2:
                os2.fsSelection = set_flag(os2.fsSelection, bit_os2_fs, value)
        if bit_head_mac is not None:
            head = font.get("head")
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
        flags.pop("self")
        for key, value in flags.items():
            if value is not None:
                assert isinstance(value, bool)
                self.set_style_flag(key, value)

    def set_style_flags_by_subfamily_name(self):
        """
        Sets the style flags by the subfamily name value.
        The subfamily values should be "regular", "italic", "bold" or "bold italic"
        to allow this method to work properly.

        :param strict: If strict (default=False) and the subfamily name is not an expected value, an error is raised.
        :type strict: bool
        """
        subfamily_name = (self.get_name(Font.NAME_SUBFAMILY_NAME) or "").lower()
        if subfamily_name == Font.STYLE_FLAG_REGULAR:
            self.set_style_flags(regular=True, bold=False, italic=False)
        elif subfamily_name == Font.STYLE_FLAG_BOLD:
            self.set_style_flags(regular=False, bold=True, italic=False)
        elif subfamily_name == Font.STYLE_FLAG_ITALIC:
            self.set_style_flags(regular=False, bold=False, italic=True)
        elif subfamily_name == f"{Font.STYLE_FLAG_BOLD} {Font.STYLE_FLAG_ITALIC}":
            self.set_style_flags(regular=False, bold=True, italic=True)

    def subset(self, unicodes="", glyphs=[], text="", **options):
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
                "Subsetting requires at least one of the following args: unicode,"
                " glyphs, text."
            )
        unicodes = parse_unicodes(unicodes)
        options.setdefault("glyph_names", True)
        options.setdefault("ignore_missing_glyphs", True)
        options.setdefault("ignore_missing_unicodes", True)
        options.setdefault("layout_features", ["*"])
        options.setdefault("name_IDs", "*")
        options.setdefault("notdef_outline", True)
        subs_args = {"unicodes": unicodes, "glyphs": glyphs, "text": text}
        # https://github.com/fonttools/fonttools/blob/main/Lib/fontTools/subset/__init__.py
        subs_options = SubsetterOptions(**options)
        subs = Subsetter(options=subs_options)
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

        :param coordinates: The coordinates dictionary, each item value must be
            tuple/list/dict (with min and max keys) for slicing or float/int for pinning, eg.
            {'wdth':100, 'wght':(100,600), 'ital':(30,70)} or
            {'wdth':100, 'wght':[100,600], 'ital':[30,70]} or
            {'wdth':100, 'wght':{'min':100,'max':600}, 'ital':{'min':30,'max':70}}
        :type coordinates: dict
        :param options: The options for the fontTools.varLib.instancer
        :type options: dictionary

        :raises TypeError: If the font is not a variable font
        :raises ValueError: If the coordinates are not defined (blank)
        :raises ValueError: If the coordinates axes are all pinned
        """
        if not self.is_variable():
            raise TypeError("Only a variable font can be sliced.")

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
                axis_min = axis_value.get("min", axis.get("min_value"))
                axis_max = axis_value.get("max", axis.get("max_value"))
                axis_value = (axis_min, axis_max)
            coordinates[axis_tag] = axis_value

        # ensure that coordinates axes are defined and that are not all pinned
        if len(coordinates_axes_tags) == 0:
            raise ValueError("Invalid coordinates: axes not defined.")
        elif set(coordinates_axes_tags) == set(self.get_variable_axes_tags()):
            if self._all_axes_pinned(coordinates):
                raise ValueError(
                    "Invalid coordinates: all axes are pinned (use to_static method)."
                )

        # set default instancer options
        options.setdefault("optimize", True)
        options.setdefault("overlap", OverlapMode.KEEP_AND_SET_FLAGS)
        options.setdefault("updateFontNames", False)

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
            raise TypeError("Only a variable font can be made static.")

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
            raise ValueError("Invalid coordinates: all axes must be pinned.")

        # set default instancer options
        options.setdefault("optimize", True)
        options.setdefault("overlap", OverlapMode.REMOVE)
        options.setdefault("updateFontNames", False)

        # instantiate the static font
        instancer.instantiateVariableFont(font, coordinates, inplace=True, **options)

    def __str__(self):
        """
        Returns a string representation of the object.

        :returns: String representation of the object.
        :rtype: str
        """
        return f"{type(self).__name__}('{self._filepath}')"

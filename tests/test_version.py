from fontTools.misc.fixedTools import floatToFixed

from fontbro import Font
from fontbro.exceptions import ArgumentError
from fontbro.version import normalize_version, parse_version
from tests import AbstractTestCase


class VersionTestCase(AbstractTestCase):
    """
    This class describes a version test case.
    """

    FONT_FILEPATH = "/Tourney/static/Tourney/Tourney-Regular.ttf"

    def _test_font_version(self, filepath, expected_value):
        font_path = self._get_font_path(filepath)
        font = Font(filepath=font_path)
        version = font.get_version()
        # print(filepath, width)
        self.assertEqual(version, expected_value)

    def test_get_version(self):
        fonts = [
            {
                "filepath": "/Noto_Sans_TC/NotoSansTC-Regular.otf",
                "version": 2.002,
            },
            {
                "filepath": "/Roboto_Mono/RobotoMono-VariableFont_wght.ttf",
                "version": 3.0,
            },
            {
                "filepath": "/Tourney/Tourney-VariableFont_wdth,wght.ttf",
                "version": 1.015,
            },
        ]
        for font in fonts:
            # print(font.get_variable_instances())
            with self.subTest(f"Test with font: {font}", font=font):
                self._test_font_version(font["filepath"], font["version"])

    def test_parse_version(self):
        values = [
            # the parsed value is normalized to its shortest decimal representation
            ("Version 1.015", 1.015),
            ("Version 3.019;git-0a5106e0b", 3.019),
            ("Version 2.002;hotconv 1.0.116;makeotfexe 2.5.65601", 2.002),
            ("Version 1.001; ttfautohint (v1.8.4.7-5d5b)", 1.001),
            ("Version 1.000;Glyphs 3.1.2 (3151)", 1.0),
            ("Version 2.000 September 15, 2016", 2.0),
            ("  Version 1.100  ", 1.1),
            ("VERSION 2.500", 2.5),
            ("Version: 1.560", 1.56),
            ("v1.560", 1.56),
            ("v.1.0.22", 1.0),
            ("1.000;GOOG;RobotoMono-Regular", 1.0),
            ("10.250", 10.25),
            # the value is normalized to the head.fontRevision precision
            ("Version 1.0149993896484375", 1.015),
            # invalid values
            (None, 0.0),
            ("", 0.0),
            ("   ", 0.0),
            ("Version", 0.0),
            ("Regular", 0.0),
            ("1", 0.0),
            # the version is not read from unrelated numbers
            ("Feb.12th.1998;1.00, initial realease", 0.0),
            ("Macromedia Fontographer 4.1 4/3/97", 0.0),
        ]
        for value, expected_value in values:
            with self.subTest(f"Test with value: {value!r}", value=value):
                self.assertEqual(parse_version(value), expected_value)

    def test_normalize_version(self):
        values = [
            (1.0149993896484375, 1.015),
            (2.0019989013671875, 2.002),
            (3.0189971923828125, 3.019),
            (1.001007080078125, 1.001),
            (1.100006103515625, 1.1),
            (1.55999755859375, 1.56),
            (3.0, 3.0),
            (1.0, 1.0),
        ]
        for value, expected_value in values:
            with self.subTest(f"Test with value: {value!r}", value=value):
                normalized_value = normalize_version(value)
                self.assertEqual(normalized_value, expected_value)
                # the normalized value is stored as the same fixed-point value
                self.assertEqual(
                    floatToFixed(normalized_value, precisionBits=16),
                    floatToFixed(value, precisionBits=16),
                )

    def _get_font_with_unset_head_revision(self):
        font = self._get_font(self.FONT_FILEPATH)
        font.get_ttfont()["head"].fontRevision = 0.0
        return font

    def test_get_version_with_unset_head_revision(self):
        font = self._get_font_with_unset_head_revision()
        self.assertEqual(font.get_name(Font.NAME_VERSION), "Version 1.015")
        self.assertEqual(font.get_version(), 1.015)

    def test_get_version_with_unset_head_revision_and_invalid_name_record(self):
        font = self._get_font_with_unset_head_revision()
        font.set_name(Font.NAME_VERSION, "Regular")
        self.assertEqual(font.get_version(), 0.0)

    def test_get_version_with_unset_head_revision_and_without_name_record(self):
        font = self._get_font_with_unset_head_revision()
        font.get_ttfont()["name"].removeNames(nameID=5)
        self.assertEqual(font.get_version(), 0.0)

    def test_get_version_with_use_head_revision_only(self):
        font = self._get_font_with_unset_head_revision()
        self.assertEqual(font.get_version(use_name_record=False), 0.0)

    def test_get_version_with_use_name_record_only(self):
        # head.fontRevision and the version name record hold the same value
        font = self._get_font(self.FONT_FILEPATH)
        self.assertEqual(font.get_version(use_head_revision=False), 1.015)

    def test_get_version_with_use_name_record_only_and_invalid_name_record(self):
        font = self._get_font(self.FONT_FILEPATH)
        font.set_name(Font.NAME_VERSION, "Regular")
        self.assertEqual(font.get_version(use_head_revision=False), 0.0)
        # the head.fontRevision value is still used by default
        self.assertEqual(font.get_version(), 1.015)

    def test_get_version_without_sources(self):
        font = self._get_font(self.FONT_FILEPATH)
        with self.assertRaises(ArgumentError):
            font.get_version(use_head_revision=False, use_name_record=False)

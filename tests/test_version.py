from fontTools.misc.fixedTools import floatToFixed

from fontbro import Font
from fontbro.exceptions import ArgumentError
from fontbro.version import format_version, normalize_version, parse_version
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

    def test_format_version(self):
        values = [
            (1.015, "v1.015"),
            (2.002, "v2.002"),
            (3.019, "v3.019"),
            (10.25, "v10.250"),
            # the minor part is padded to 3 decimal digits
            (1.1, "v1.100"),
            (3.0, "v3.000"),
            # more decimal digits are kept when the value needs them
            (1.0001, "v1.0001"),
            # the raw head.fontRevision values are formatted as well
            (1.0149993896484375, "v1.015"),
            (1.100006103515625, "v1.100"),
            # unreadable version
            (0.0, "v0.000"),
        ]
        for value, expected_value in values:
            with self.subTest(f"Test with value: {value!r}", value=value):
                self.assertEqual(format_version(value), expected_value)

    def test_format_version_with_prefix(self):
        self.assertEqual(format_version(1.015, prefix=""), "1.015")
        self.assertEqual(format_version(1.015, prefix="ver. "), "ver. 1.015")

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

    def test_get_version_without_head_table(self):
        font = self._get_font(self.FONT_FILEPATH)
        del font.get_ttfont()["head"]
        # the version is read from the version name record
        self.assertEqual(font.get_version(), 1.015)
        self.assertEqual(font.get_version(use_name_record=False), 0.0)

    def test_get_version_without_name_table(self):
        font = self._get_font_with_unset_head_revision()
        del font.get_ttfont()["name"]
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

    def test_get_version_formatted(self):
        font = self._get_font(self.FONT_FILEPATH)
        self.assertEqual(font.get_version_formatted(), "v1.015")
        self.assertEqual(font.get_version_formatted(prefix=""), "1.015")

    def test_get_version_formatted_with_unset_head_revision(self):
        font = self._get_font_with_unset_head_revision()
        self.assertEqual(font.get_version_formatted(), "v1.015")
        self.assertEqual(font.get_version_formatted(use_name_record=False), "v0.000")

    def test_get_version_formatted_without_sources(self):
        font = self._get_font(self.FONT_FILEPATH)
        with self.assertRaises(ArgumentError):
            font.get_version_formatted(
                use_head_revision=False,
                use_name_record=False,
            )

    def test_set_version(self):
        font = self._get_font(self.FONT_FILEPATH)
        font.set_version(2.5)
        self.assertEqual(font.get_version(), 2.5)
        self.assertEqual(font.get_version_formatted(), "v2.500")
        self.assertEqual(font.get_ttfont()["head"].fontRevision, 2.5)
        self.assertEqual(font.get_name(Font.NAME_VERSION), "Version 2.500")
        self.assertEqual(
            font.get_name(Font.NAME_UNIQUE_IDENTIFIER),
            "2.500;ETCO;Tourney-Regular",
        )

    def test_set_version_overwrites_name_record_extra_info(self):
        font = self._get_font("/Inter/static/Inter-Regular.ttf")
        self.assertEqual(
            font.get_name(Font.NAME_VERSION), "Version 3.019;git-0a5106e0b"
        )
        font.set_version(3.02)
        self.assertEqual(font.get_name(Font.NAME_VERSION), "Version 3.020")
        self.assertEqual(
            font.get_name(Font.NAME_UNIQUE_IDENTIFIER),
            "3.020;RSMS;Inter-Regular",
        )

    def test_set_version_with_unique_identifier_without_version(self):
        font = self._get_font(self.FONT_FILEPATH)
        font.set_name(Font.NAME_UNIQUE_IDENTIFIER, "ETCO;Tourney-Regular")
        font.set_version(2.5)
        # the unique identifier is left untouched
        self.assertEqual(
            font.get_name(Font.NAME_UNIQUE_IDENTIFIER),
            "ETCO;Tourney-Regular",
        )

    def test_set_version_with_unique_identifier_with_other_version(self):
        font = self._get_font(self.FONT_FILEPATH)
        font.set_name(Font.NAME_UNIQUE_IDENTIFIER, "1.234;ETCO;Tourney-Regular")
        font.set_version(2.5)
        # the unique identifier is left untouched
        self.assertEqual(
            font.get_name(Font.NAME_UNIQUE_IDENTIFIER),
            "1.234;ETCO;Tourney-Regular",
        )

    def test_set_version_with_unique_identifier_with_version_and_extra_info(self):
        font = self._get_font(self.FONT_FILEPATH)
        font.set_name(Font.NAME_UNIQUE_IDENTIFIER, "1.015 UKWN;Tourney-Regular")
        font.set_version(2.5)
        # the whole first part is replaced, it is the one holding the version
        self.assertEqual(
            font.get_name(Font.NAME_UNIQUE_IDENTIFIER),
            "2.500;Tourney-Regular",
        )

    def test_set_version_with_cff_font(self):
        font = self._get_font("/issues/issue-0050/LeagueGothic-Regular.otf")
        ttfont = font.get_ttfont()
        top_dict = ttfont["CFF "].cff.topDictIndex[0]
        self.assertEqual(top_dict.version, "001.560")
        font.set_version(2.5)
        self.assertEqual(top_dict.version, "002.500")
        self.assertEqual(font.get_name(Font.NAME_VERSION), "Version 2.500")
        self.assertEqual(
            font.get_name(Font.NAME_UNIQUE_IDENTIFIER),
            "2.500;UKWN;LeagueGothic-Regular",
        )

    def test_set_version_with_cff_font_without_cff_version(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        ttfont = font.get_ttfont()
        top_dict = ttfont["CFF "].cff.topDictIndex[0]
        self.assertNotIn("version", top_dict.rawDict)
        font.set_version(2.5)
        # the cff version is not added to fonts that don't have it
        self.assertNotIn("version", top_dict.rawDict)
        self.assertEqual(font.get_version(), 2.5)

    def test_set_version_with_saved_font(self):
        font = self._get_font("/issues/issue-0050/LeagueGothic-Regular.otf")
        font.set_version(2.5)
        font_temp_path = self._get_font_temp_path("LeagueGothic-Regular.otf")
        font.save(font_temp_path, overwrite=True)
        font_saved = Font(filepath=font_temp_path)
        self.assertEqual(font_saved.get_version(), 2.5)
        self.assertEqual(font_saved.get_name(Font.NAME_VERSION), "Version 2.500")
        self.assertEqual(
            font_saved.get_name(Font.NAME_UNIQUE_IDENTIFIER),
            "2.500;UKWN;LeagueGothic-Regular",
        )
        top_dict = font_saved.get_ttfont()["CFF "].cff.topDictIndex[0]
        self.assertEqual(top_dict.version, "002.500")

    def test_set_version_with_version_str(self):
        versions = [
            ("Version 2.500", 2.5),
            ("Version 2.500;git-0a5106e0b", 2.5),
            ("2.500", 2.5),
            ("v2.5", 2.5),
            ("2.5", 2.5),
        ]
        for version, expected_value in versions:
            with self.subTest(f"Test with version: {version!r}", version=version):
                font = self._get_font(self.FONT_FILEPATH)
                font.set_version(version)
                self.assertEqual(font.get_version(), expected_value)
                self.assertEqual(font.get_name(Font.NAME_VERSION), "Version 2.500")

    def test_set_version_with_invalid_version(self):
        font = self._get_font(self.FONT_FILEPATH)
        versions = [
            # invalid values
            0.0,
            -1.0,
            # unparsable version strings
            "",
            "Version",
            "Regular",
            "Macromedia Fontographer 4.1 4/3/97",
            # invalid types
            None,
            [1.015],
        ]
        for version in versions:
            with self.subTest(f"Test with version: {version!r}", version=version):
                with self.assertRaises(ArgumentError):
                    font.set_version(version)
        # the font is left untouched
        self.assertEqual(font.get_version(), 1.015)
        self.assertEqual(font.get_name(Font.NAME_VERSION), "Version 1.015")

    def test_set_version_without_head_table(self):
        font = self._get_font(self.FONT_FILEPATH)
        del font.get_ttfont()["head"]
        font.set_version(2.5)
        # the name records are updated anyway
        self.assertEqual(font.get_name(Font.NAME_VERSION), "Version 2.500")
        self.assertEqual(
            font.get_name(Font.NAME_UNIQUE_IDENTIFIER),
            "2.500;ETCO;Tourney-Regular",
        )

    def test_set_version_without_name_table(self):
        font = self._get_font(self.FONT_FILEPATH)
        del font.get_ttfont()["name"]
        font.set_version(2.5)
        # the head.fontRevision is updated anyway
        self.assertEqual(font.get_ttfont()["head"].fontRevision, 2.5)
        self.assertEqual(font.get_version(), 2.5)

    def test_set_version_with_cff_font_with_multiple_fonts(self):
        font = self._get_font("/issues/issue-0050/LeagueGothic-Regular.otf")
        other_font = self._get_font("/issues/issue-0062/ABCTest-Thin.otf")
        cff = font.get_ttfont()["CFF "].cff
        other_cff = other_font.get_ttfont()["CFF "].cff
        top_dict = cff.topDictIndex[0]
        other_top_dict = other_cff.topDictIndex[0]
        # simulate a cff holding more than one font (eg. in a font collection),
        # with the font of this face at index 1
        cff.fontNames = list(other_cff.fontNames) + list(cff.fontNames)
        cff.topDictIndex.items.insert(0, other_top_dict)
        font.set_version(2.5)
        # the font is looked up by its postscript name, not by its index
        self.assertEqual(top_dict.version, "002.500")
        self.assertEqual(other_top_dict.version, "001.000")

    def test_set_version_with_cff_font_without_top_dict(self):
        font = self._get_font("/issues/issue-0050/LeagueGothic-Regular.otf")
        cff = font.get_ttfont()["CFF "].cff
        top_dict = cff.topDictIndex[0]
        cff.topDictIndex.items.clear()
        font.set_version(2.5)
        # the cff version is left untouched
        self.assertEqual(top_dict.version, "001.560")
        self.assertEqual(font.get_version(), 2.5)

    def test_set_version_with_cff_font_without_matching_font(self):
        font = self._get_font("/issues/issue-0050/LeagueGothic-Regular.otf")
        cff = font.get_ttfont()["CFF "].cff
        top_dict = cff.topDictIndex[0]
        cff.fontNames = ["OtherFont-Regular", "AnotherFont-Regular"]
        font.set_version(2.5)
        # the cff version is left untouched
        self.assertEqual(top_dict.version, "001.560")
        # the other values are updated anyway
        self.assertEqual(font.get_version(), 2.5)
        self.assertEqual(font.get_name(Font.NAME_VERSION), "Version 2.500")

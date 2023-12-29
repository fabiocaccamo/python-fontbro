from fontbro import Font
from tests import AbstractTestCase


class RenameTestCase(AbstractTestCase):
    """
    Test case for the font renaming.
    """

    def test_rename_with_family_name_and_style_name(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.rename(
            family_name="Roboto Mono New",
            style_name="Bold Italic",
        )
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Roboto Mono New")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "Bold Italic")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Roboto Mono New Bold Italic")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "RobotoMonoNew-BoldItalic")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Roboto Mono New")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "Bold Italic")

    def test_rename_with_family_name_only(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.rename(
            family_name="Roboto Mono New",
        )
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Roboto Mono New")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "Regular")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Roboto Mono New Regular")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "RobotoMonoNew-Regular")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Roboto Mono New")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "Regular")

    def test_rename_update_unique_identifier(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        family_name = font.get_name(key=Font.NAME_FAMILY_NAME)
        family_name = family_name.replace("Mono", "Multi")
        font.rename(
            family_name=family_name,
        )
        font_uid = font.get_name(Font.NAME_UNIQUE_IDENTIFIER)
        self.assertEqual(font_uid, "3.000;GOOG;RobotoMulti-Regular")

    def test_rename_with_family_name_only_issue_0062(self):
        # https://github.com/fabiocaccamo/python-fontbro/issues/62
        font = self._get_font("/issues/issue-0062/ABCTest-Thin.otf")
        # self._print(font.get_names())
        self.assertEqual(
            font.get_names(),
            {
                "family_name": "ABC Test Thin",
                "full_name": "ABC Test Thin",
                "postscript_name": "ABCTest-Thin",
                "subfamily_name": "Regular",
                "typographic_family_name": "ABC Test",
                "typographic_subfamily_name": "Thin",
                "unique_identifier": "1.000;UKWN;ABCTest-Thin",
                "version": "Version 1.000;Glyphs 3.1.2 (3151)",
            },
        )
        family_name = font.get_name(key=Font.NAME_TYPOGRAPHIC_FAMILY_NAME)
        family_name = family_name.replace("ABC", "Hugo")
        font.rename(
            family_name=family_name,
        )
        # self._print(font.get_names())
        self.assertEqual(
            font.get_names(),
            {
                "family_name": "Hugo Test Thin",
                "full_name": "Hugo Test Thin",
                "postscript_name": "HugoTest-Thin",
                "subfamily_name": "Regular",
                "typographic_family_name": "Hugo Test",
                "typographic_subfamily_name": "Thin",
                "unique_identifier": "1.000;UKWN;HugoTest-Thin",
                "version": "Version 1.000;Glyphs 3.1.2 (3151)",
                "wws_family_name": "Hugo Test",
                "wws_subfamily_name": "Thin",
            },
        )
        full_name = font.get_name(key=Font.NAME_FULL_NAME)
        self.assertEqual(full_name, "Hugo Test Thin")

    def test_rename_with_style_name_only(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.rename(
            style_name="Bold Italic",
        )
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Roboto Mono")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "Bold Italic")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Roboto Mono Bold Italic")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "RobotoMono-BoldItalic")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Roboto Mono")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "Bold Italic")

    def test_rename_without_family_name_and_style_name(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.rename(
            family_name="",
            style_name="",
        )
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Roboto Mono")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "Regular")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Roboto Mono Regular")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "RobotoMono-Regular")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Roboto Mono")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "Regular")

    def test_rename_with_final_postscript_name_too_long(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        with self.assertRaises(ValueError):
            font.rename(
                family_name="Roboto Mono New Name Too Long For PostScript Name So Expect Exception",
                style_name="Bold Italic",
            )

    def test_rename_with_style_name_containing_characters_not_allowed_in_postscript_name(
        self,
    ):
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font.rename(
            family_name=" Tourney Custom ",
            style_name=" [wdth-wght] ",
        )
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Tourney Custom [wdth-wght]")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "Regular")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Tourney Custom [wdth-wght]")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "TourneyCustom-wdth-wght")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Tourney Custom")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "[wdth-wght]")

    def test_rename_with_style_flags_disabled(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.set_style_flags(regular=False, bold=False, italic=False)
        font.rename(
            family_name="Roboto Mono New",
            style_name="Bold Italic",
            update_style_flags=False,
        )
        style_flags = font.get_style_flags()
        self.assertFalse(style_flags["regular"])
        self.assertFalse(style_flags["bold"])
        self.assertFalse(style_flags["italic"])

    def test_rename_with_style_flags_enabled(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.set_style_flags(regular=False, bold=False, italic=False)
        font.rename(
            family_name="Roboto Mono New",
            style_name="Bold Italic",
            update_style_flags=True,
        )
        style_flags = font.get_style_flags()
        self.assertFalse(style_flags["regular"])
        self.assertTrue(style_flags["bold"])
        self.assertTrue(style_flags["italic"])

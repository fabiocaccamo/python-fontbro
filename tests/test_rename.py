# -*- coding: utf-8 -*-

from fontbro import Font

from tests import AbstractTestCase


class RenameTestCase(AbstractTestCase):
    """
    Test case for the font renaming.
    """

    def test_rename_with_family_name_and_style_name(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.rename("Roboto Mono New", "Bold Italic")
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Roboto Mono New")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "bold italic")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Roboto Mono New Bold Italic")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "RobotoMonoNew-BoldItalic")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Roboto Mono New")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "Bold Italic")

    def test_rename_with_family_name_only(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.rename("Roboto Mono New", "")
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Roboto Mono New")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "regular")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Roboto Mono New Regular")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "RobotoMonoNew-Regular")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Roboto Mono New")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "Regular")

    def test_rename_with_style_name_only(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.rename("", "Bold Italic")
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Roboto Mono")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "bold italic")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Roboto Mono Bold Italic")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "RobotoMono-BoldItalic")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Roboto Mono")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "Bold Italic")

    def test_rename_without_family_name_and_style_name(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.rename("", "")
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Roboto Mono")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "regular")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Roboto Mono Regular")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "RobotoMono-Regular")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Roboto Mono")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "Regular")

    def test_rename_with_final_postscript_name_too_long(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        with self.assertRaises(ValueError):
            font.rename(
                "Roboto Mono New Name Too Long For PostScript Name So Expect Exception",
                "Bold Italic",
            )

    def test_rename_with_style_name_containing_characters_not_allowed_in_postscript_name(
        self,
    ):
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font.rename(" Tourney Custom ", " [wdth-wght] ")
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Tourney Custom [wdth-wght]")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "regular")
        self.assertEqual(
            names[Font.NAME_FULL_NAME], "Tourney Custom [wdth-wght] Regular"
        )
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "TourneyCustom-wdth-wght")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Tourney Custom")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "[wdth-wght]")

    def test_rename_with_style_flags_disabled(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.set_style_flags(regular=False, bold=False, italic=False)
        font.rename("Roboto Mono New", "Bold Italic", style_flags=False)
        style_flags = font.get_style_flags()
        self.assertFalse(style_flags["regular"])
        self.assertFalse(style_flags["bold"])
        self.assertFalse(style_flags["italic"])

    def test_rename_with_style_flags_enabled(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.set_style_flags(regular=False, bold=False, italic=False)
        font.rename("Roboto Mono New", "Bold Italic", style_flags=True)
        style_flags = font.get_style_flags()
        self.assertFalse(style_flags["regular"])
        self.assertTrue(style_flags["bold"])
        self.assertTrue(style_flags["italic"])

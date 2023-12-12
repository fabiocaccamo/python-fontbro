from fontbro import Font
from tests import AbstractTestCase


class StyleNameTestCase(AbstractTestCase):
    """
    Test case for the font get_style_name / set_style_name methods.
    """

    def test_style_name(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        self.assertEqual(font.get_style_name(), "Regular")
        font.set_style_name("Bold Italic")
        self.assertEqual(font.get_style_name(), "Bold Italic")
        # check all name records
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Roboto Mono")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "Bold Italic")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Roboto Mono Bold Italic")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "RobotoMono-BoldItalic")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Roboto Mono")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "Bold Italic")
        self.assertEqual(
            names[Font.NAME_UNIQUE_IDENTIFIER], "3.000;GOOG;RobotoMono-BoldItalic"
        )

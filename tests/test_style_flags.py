from tests import AbstractTestCase


class StyleFlagsTestCase(AbstractTestCase):
    """
    Test case for the methods related to the font style flags.
    """

    def test_get_style_flags(self):
        expected_style_flags_default = {
            "bold": False,
            "condensed": False,
            "extended": False,
            "italic": False,
            "outline": False,
            "regular": False,
            "shadow": False,
            "underline": False,
        }

        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        style_flags = font.get_style_flags()
        expected_style_flags = expected_style_flags_default.copy()
        expected_style_flags["regular"] = True
        self.assertEqual(style_flags, expected_style_flags)

        font = self._get_font("/Roboto_Mono/static/RobotoMono-Italic.ttf")
        style_flags = font.get_style_flags()
        expected_style_flags = expected_style_flags_default.copy()
        expected_style_flags["italic"] = True
        self.assertEqual(style_flags, expected_style_flags)

        font = self._get_font("/Roboto_Mono/static/RobotoMono-Bold.ttf")
        style_flags = font.get_style_flags()
        expected_style_flags = expected_style_flags_default.copy()
        expected_style_flags["bold"] = True
        self.assertEqual(style_flags, expected_style_flags)

        font = self._get_font("/Roboto_Mono/static/RobotoMono-BoldItalic.ttf")
        style_flags = font.get_style_flags()
        expected_style_flags = expected_style_flags_default.copy()
        expected_style_flags["bold"] = True
        expected_style_flags["italic"] = True
        self.assertEqual(style_flags, expected_style_flags)

    def test_is_set_bold_flag(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        self.assertFalse(font.get_style_flags()["bold"])

        font = self._get_font("/Roboto_Mono/static/RobotoMono-Italic.ttf")
        self.assertFalse(font.get_style_flags()["bold"])

        font = self._get_font("/Roboto_Mono/static/RobotoMono-Bold.ttf")
        self.assertTrue(font.get_style_flags()["bold"])

        font = self._get_font("/Roboto_Mono/static/RobotoMono-BoldItalic.ttf")
        self.assertTrue(font.get_style_flags()["bold"])

    def test_is_set_italic_flag(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        self.assertFalse(font.get_style_flags()["italic"])

        font = self._get_font("/Roboto_Mono/static/RobotoMono-Italic.ttf")
        self.assertTrue(font.get_style_flags()["italic"])

        font = self._get_font("/Roboto_Mono/static/RobotoMono-Bold.ttf")
        self.assertFalse(font.get_style_flags()["italic"])

        font = self._get_font("/Roboto_Mono/static/RobotoMono-BoldItalic.ttf")
        self.assertTrue(font.get_style_flags()["italic"])

    def test_set_bold_flag(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        self.assertFalse(font.get_style_flags()["bold"])

        font.set_style_flags(bold=True)
        self.assertTrue(font.get_style_flags()["bold"])

        font.set_style_flags(bold=False)
        self.assertFalse(font.get_style_flags()["bold"])

        font.set_style_flags(bold=True)
        self.assertTrue(font.get_style_flags()["bold"])

        font.set_style_flags(bold=False)
        self.assertFalse(font.get_style_flags()["bold"])

    def test_set_italic_flag(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Italic.ttf")
        self.assertTrue(font.get_style_flags()["italic"])

        font.set_style_flags(italic=False)
        self.assertFalse(font.get_style_flags()["italic"])

        font.set_style_flags(italic=True)
        self.assertTrue(font.get_style_flags()["italic"])

        font.set_style_flags(italic=False)
        self.assertFalse(font.get_style_flags()["italic"])

        font.set_style_flags(italic=True)
        self.assertTrue(font.get_style_flags()["italic"])

    def test_set_regular_flag(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        self.assertTrue(font.get_style_flags()["regular"])

        font.set_style_flags(regular=False)
        self.assertFalse(font.get_style_flags()["regular"])

        font.set_style_flags(regular=True)
        self.assertTrue(font.get_style_flags()["regular"])

        font.set_style_flags(regular=False)
        self.assertFalse(font.get_style_flags()["regular"])

        font.set_style_flags(regular=True)
        self.assertTrue(font.get_style_flags()["regular"])

    def test_set_style_flags_by_subfamily_name(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.set_style_flags(regular=False, bold=False, italic=False)
        style_flags = font.get_style_flags()
        self.assertFalse(style_flags["regular"])
        self.assertFalse(style_flags["bold"])
        self.assertFalse(style_flags["italic"])
        font.rename("Roboto Mono New", "Bold Italic", style_flags=False)
        font.set_style_flags_by_subfamily_name()
        style_flags = font.get_style_flags()
        self.assertFalse(style_flags["regular"])
        self.assertTrue(style_flags["bold"])
        self.assertTrue(style_flags["italic"])

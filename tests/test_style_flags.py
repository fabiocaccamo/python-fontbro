# -*- coding: utf-8 -*-

from tests import FontbroTestCase


class StyleFlagsTestCase(FontbroTestCase):
    """
    Test case for the methods related to the font style flags.
    """

    def test_get_style_flags(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        style_flags = font.get_style_flags()
        expected_style_flags = {
            'bold': False,
            'italic': False,
            'outline': False,
            'regular': True,
            'underline': False,
        }
        self.assertEqual(style_flags, expected_style_flags)

        font = self._get_font('/Roboto_Mono/static/RobotoMono-Italic.ttf')
        style_flags = font.get_style_flags()
        expected_style_flags = {
            'bold': False,
            'italic': True,
            'outline': False,
            'regular': False,
            'underline': False,
        }
        self.assertEqual(style_flags, expected_style_flags)

        font = self._get_font('/Roboto_Mono/static/RobotoMono-Bold.ttf')
        style_flags = font.get_style_flags()
        expected_style_flags = {
            'bold': True,
            'italic': False,
            'outline': False,
            'regular': False,
            'underline': False,
        }
        self.assertEqual(style_flags, expected_style_flags)

        font = self._get_font('/Roboto_Mono/static/RobotoMono-BoldItalic.ttf')
        style_flags = font.get_style_flags()
        expected_style_flags = {
            'bold': True,
            'italic': True,
            'outline': False,
            'regular': False,
            'underline': False,
        }
        self.assertEqual(style_flags, expected_style_flags)

    def test_is_set_bold_flag(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        self.assertFalse(font.get_style_flags()['bold'])

        font = self._get_font('/Roboto_Mono/static/RobotoMono-Italic.ttf')
        self.assertFalse(font.get_style_flags()['bold'])

        font = self._get_font('/Roboto_Mono/static/RobotoMono-Bold.ttf')
        self.assertTrue(font.get_style_flags()['bold'])

        font = self._get_font('/Roboto_Mono/static/RobotoMono-BoldItalic.ttf')
        self.assertTrue(font.get_style_flags()['bold'])

    def test_is_set_italic_flag(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        self.assertFalse(font.get_style_flags()['italic'])

        font = self._get_font('/Roboto_Mono/static/RobotoMono-Italic.ttf')
        self.assertTrue(font.get_style_flags()['italic'])

        font = self._get_font('/Roboto_Mono/static/RobotoMono-Bold.ttf')
        self.assertFalse(font.get_style_flags()['italic'])

        font = self._get_font('/Roboto_Mono/static/RobotoMono-BoldItalic.ttf')
        self.assertTrue(font.get_style_flags()['italic'])

    def test_set_bold_flag(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        self.assertFalse(font.get_style_flags()['bold'])

        font.set_style_flags(bold=True)
        self.assertTrue(font.get_style_flags()['bold'])

        font.set_style_flags(bold=False)
        self.assertFalse(font.get_style_flags()['bold'])

        font.set_style_flags(bold=True)
        self.assertTrue(font.get_style_flags()['bold'])

        font.set_style_flags(bold=False)
        self.assertFalse(font.get_style_flags()['bold'])

    def test_set_italic_flag(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Italic.ttf')
        self.assertTrue(font.get_style_flags()['italic'])

        font.set_style_flags(italic=False)
        self.assertFalse(font.get_style_flags()['italic'])

        font.set_style_flags(italic=True)
        self.assertTrue(font.get_style_flags()['italic'])

        font.set_style_flags(italic=False)
        self.assertFalse(font.get_style_flags()['italic'])

        font.set_style_flags(italic=True)
        self.assertTrue(font.get_style_flags()['italic'])

    def test_set_regular_flag(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        self.assertTrue(font.get_style_flags()['regular'])

        font.set_style_flags(regular=False)
        self.assertFalse(font.get_style_flags()['regular'])

        font.set_style_flags(regular=True)
        self.assertTrue(font.get_style_flags()['regular'])

        font.set_style_flags(regular=False)
        self.assertFalse(font.get_style_flags()['regular'])

        font.set_style_flags(regular=True)
        self.assertTrue(font.get_style_flags()['regular'])

if __name__ == '__main__':
    unittest.main()

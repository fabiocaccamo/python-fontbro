# -*- coding: utf-8 -*-

from fontbro import Fontbro
from tests import FontbroTestCase


class FormatTestCase(FontbroTestCase):
    """
    Test case for the methods related to the font format.
    """

    def test_format_constants(self):
        self.assertEqual(Fontbro.FORMAT_OTF, 'otf')
        self.assertEqual(Fontbro.FORMAT_TTF, 'ttf')
        self.assertEqual(Fontbro.FORMAT_WOFF, 'woff')
        self.assertEqual(Fontbro.FORMAT_WOFF2, 'woff2')

    def test_get_format_with_otf(self):
        font = self._get_font('/Noto_Sans_TC/NotoSansTC-Regular.otf')
        font_format = font.get_format()
        self.assertEqual(font_format, Fontbro.FORMAT_OTF)

    def test_get_format_with_ttf(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        font_format = font.get_format()
        self.assertEqual(font_format, Fontbro.FORMAT_TTF)

    def test_get_format_with_woff(self):
        # TODO
        pass

    def test_get_format_with_woff2(self):
        # TODO
        pass

    def test_is_otf(self):
        font = self._get_font('/Noto_Sans_TC/NotoSansTC-Regular.otf')
        self.assertTrue(font.get_format() == Fontbro.FORMAT_OTF)
        self.assertFalse(font.get_format() == Fontbro.FORMAT_TTF)
        self.assertFalse(font.get_format() == Fontbro.FORMAT_WOFF)
        self.assertFalse(font.get_format() == Fontbro.FORMAT_WOFF2)

    def test_is_ttf(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        self.assertFalse(font.get_format() == Fontbro.FORMAT_OTF)
        self.assertTrue(font.get_format() == Fontbro.FORMAT_TTF)
        self.assertFalse(font.get_format() == Fontbro.FORMAT_WOFF)
        self.assertFalse(font.get_format() == Fontbro.FORMAT_WOFF2)


if __name__ == '__main__':
    unittest.main()

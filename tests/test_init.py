# -*- coding: utf-8 -*-

from fontbro import Fontbro
from fontTools.ttLib import TTFont
from tests import FontbroTestCase


class InitTestCase(FontbroTestCase):
    """
    Test case for the font constructor.
    """

    def test_init_with_filepath(self):
        filepath = self._get_font_path('/Noto_Sans_TC/NotoSansTC-Regular.otf')
        font = Fontbro(filepath=filepath)

    def test_init_with_filepath_but_invalid_font_file(self):
        with self.assertRaises(ValueError):
            filepath = self._get_font_path('/Noto_Sans_TC/OFL.txt')
            font = Fontbro(filepath=filepath)

    def test_init_with_invalid_filepath_value(self):
        with self.assertRaises(ValueError):
            filepath = True
            font = Fontbro(filepath=filepath)

    def test_init_with_invalid_filepath(self):
        with self.assertRaises(FileNotFoundError):
            filepath = self._get_font_path(
                '/Noto_Sans_TC/NotoSansTC-Regular-Invalid.otf'
            )
            font = Fontbro(filepath=filepath)

    # def test_init_with_font_instance_ttfont(self):
    #     filepath = self._get_font_path('/Noto_Sans_TC/NotoSansTC-Regular.otf')
    #     ttffont = TTFont(filepath)
    #     font1 = Fontbro(font=ttffont)
    #     font2 = Fontbro(font=font1.get_ttfont())

    # def test_init_with_font_instance_fontbro(self):
    #     filepath = self._get_font_path('/Noto_Sans_TC/NotoSansTC-Regular.otf')
    #     font = Fontbro(filepath=filepath)
    #     font2 = Fontbro(font=font)

    # def test_init_with_filepath_and_font_instance(self):
    #     filepath = self._get_font_path('/Noto_Sans_TC/NotoSansTC-Regular.otf')
    #     font = TTFont(filepath)
    #     with self.assertRaises(ValueError):
    #         font = Fontbro(filepath=filepath, font=font)

    # def test_init_without_filepath_and_font_instance(self):
    #     with self.assertRaises(ValueError):
    #         font = Fontbro()

    # def test_init_with_invalid_argument(self):
    #     with self.assertRaises(ValueError):
    #         font = Fontbro(filepath=True)
    #     # with self.assertRaises(ValueError):
    #     #     font = Fontbro(font=True)


if __name__ == '__main__':
    unittest.main()

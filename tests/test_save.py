# -*- coding: utf-8 -*-

from fontbro import Fontbro

from tests import FontbroTestCase


class SaveTestCase(FontbroTestCase):
    '''
    Test case for the methods related to the font save method.
    '''

    def test_save_with_font_src_path_as_filepath_with_overwrite(self):
        font_filepath = self._get_font_path('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        font_saved_path = font.save(font_filepath, overwrite=True)
        self.assertEqual(font_saved_path, font_filepath)

    def test_save_with_font_src_path_as_filepath_without_overwrite(self):
        font_filepath = self._get_font_path('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        with self.assertRaises(ValueError):
            font.save(font_filepath)

    def test_save_as_woff(self):
        # font = self._get_font('/Noto_Sans_TC/NotoSansTC-Regular.otf')
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        output_filepath = self._get_font_temp_path('')

        font_saved_filepath = font.save_as_woff(output_filepath)
        self.assertTrue(font_saved_filepath.endswith('.woff'))
        # ensure that the original font format is not changed
        self.assertEqual(font.get_format(), Fontbro.FORMAT_TTF)
        font_saved = Fontbro(font_saved_filepath)
        self.assertEqual(font_saved.get_format(), Fontbro.FORMAT_WOFF)

    def test_save_as_woff2(self):
        # font = self._get_font('/Noto_Sans_TC/NotoSansTC-Regular.otf')
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        output_filepath = self._get_font_temp_path('')

        font_saved_filepath = font.save_as_woff2(output_filepath)
        self.assertTrue(font_saved_filepath.endswith('.woff2'))
        # ensure that the original font format is not changed
        self.assertEqual(font.get_format(), Fontbro.FORMAT_TTF)
        font_saved = Fontbro(font_saved_filepath)
        self.assertEqual(font_saved.get_format(), Fontbro.FORMAT_WOFF2)


if __name__ == '__main__':
    unittest.main()

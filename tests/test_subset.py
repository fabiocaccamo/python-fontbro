# -*- coding: utf-8 -*-

from tests import AbstractTestCase


class SubsetTestCase(AbstractTestCase):
    """
    Test case for the font subsetting.
    """

    def test_subset_without_args(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        chars_count = font.get_characters_count()
        with self.assertRaises(ValueError):
            font.subset()

    def test_subset_with_glyphs(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)
        font.subset(glyphs=['f', 'o', 'n', 't', 'b', 'r', 'o'])
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 6)

    def test_subset_with_text(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)
        font.subset(text='fontbro')
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 6)

    def test_subset_with_unicodes_str(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)
        font.subset(unicodes='0000—007F 0100—017F 0180—024F')
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 240)

    def test_subset_with_unicodes_list(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)
        font.subset(unicodes=['0000—007F', '0100—017F', '0180—024F'])
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 240)

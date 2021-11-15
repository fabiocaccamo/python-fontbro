# -*- coding: utf-8 -*-

from tests import FontbroTestCase


class CharactersTestCase(FontbroTestCase):
    """
    Test case for the methods related to the font characters.
    """

    def test_get_characters(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        chars = font.get_characters()
        chars_list = list(chars)
        # for c in chars_list:
        #     print(c)
        # check if chars type is generator
        self.assertTrue(isinstance(chars, type(0 for i in [])))
        self.assertEqual(len(chars_list), 875)
        self.assertTrue(
            all(
                [
                    key in chars_list[0]
                    for key in ['character', 'character_name', 'code', 'name']
                ]
            )
        )

    def test_get_characters_count(self):
        font = self._get_font('/Roboto_Mono/static/RobotoMono-Regular.ttf')
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)


if __name__ == '__main__':
    unittest.main()

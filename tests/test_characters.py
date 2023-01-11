from tests import AbstractTestCase


class CharactersTestCase(AbstractTestCase):
    """
    Test case for the methods related to the font characters.
    """

    def test_get_characters(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        chars = font.get_characters()
        chars_list = list(chars)
        # for c in chars_list:
        #     print(c)
        # check if chars type is generator
        expected_keys = [
            "character",
            "character_name",
            "code",
            "escape_sequence",
            "html_code",
            "unicode",
            "unicode_code",
            "unicode_name",
            "unicode_block_name",
            "unicode_script_name",
            "unicode_script_tag",
        ]
        self.assertTrue(isinstance(chars, type(0 for i in [])))
        self.assertEqual(len(chars_list), 875)
        self.assertTrue(all([key in chars_list[0] for key in expected_keys]))

    def test_get_characters_count(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)

    def test_get_characters_count_with_ignore_blank(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        chars_count = font.get_characters_count(ignore_blank=True)
        self.assertEqual(chars_count, 861)

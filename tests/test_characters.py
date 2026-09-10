from fontbro.exceptions import DataError
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
        self.assertTrue(all(key in chars_list[0] for key in expected_keys))

    def test_get_characters_without_unicode_cmap(self):
        # fonts without unicode cmap raise DataError
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        cmap_table = font.get_ttfont()["cmap"]
        cmap_table.tables = [
            table for table in cmap_table.tables if not table.isUnicode()
        ]
        with self.assertRaises(DataError):
            list(font.get_characters())
        # regression: DataError also without cmap table (instead of KeyError)
        del font.get_ttfont()["cmap"]
        with self.assertRaises(DataError):
            list(font.get_characters())

    def test_get_characters_count(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)

    def test_get_characters_count_with_ignore_blank(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        chars_count = font.get_characters_count(ignore_blank=True)
        self.assertEqual(chars_count, 861)

    def test_get_characters_count_with_ignore_blank_and_cff_outlines(self):
        # regression: blank characters must be ignored also with CFF outlines
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        self.assertEqual(font.get_characters_count(), 20748)
        self.assertEqual(font.get_characters_count(ignore_blank=True), 20743)
        chars = {char["unicode"] for char in font.get_characters(ignore_blank=True)}
        for blank_char in ["U+0020", "U+00A0", "U+2002", "U+2003", "U+3000"]:
            self.assertNotIn(blank_char, chars)

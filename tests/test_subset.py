from tests import AbstractTestCase


class SubsetTestCase(AbstractTestCase):
    """
    Test case for the font subsetting.
    """

    def test_subset_without_args(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        with self.assertRaises(ValueError):
            font.subset()

    def test_subset_with_glyphs(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)
        font.subset(glyphs=["f", "o", "n", "t", "b", "r", "o"])
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 6)

    def test_subset_with_text(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)
        font.subset(text="fontbro")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 6)

    def test_subset_with_unicodes_str(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)
        font.subset(unicodes="0000—007F 0100—017F 0180—024F")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 240)

    def test_subset_with_unicodes_str_and_unicode_prefix(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)
        font.subset(unicodes="U+0000—U+007F U+0100—U+017F U+0180—U+024F")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 240)

    def test_subset_with_unicodes_str_and_unicode_escape_prefix(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)
        font.subset(unicodes="\\u0000—\\u007F \\u0100—\\u017F \\u0180—\\u024F")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 240)

    def test_subset_with_unicodes_list_of_str(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)
        font.subset(unicodes=["0000—007F", "0100—017F", "0180—024F"])
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 240)

    def test_subset_with_unicodes_list_of_str_with_u_prefix(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)
        font.subset(unicodes=["u0000—u007F", "u0100—u017F", "u0180—u024F"])
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 240)

    def test_subset_with_unicodes_list_of_int(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)
        unicodes = [*range(65, 91)]
        font.subset(unicodes=unicodes)
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, len(unicodes))
        self.assertEqual(chars_count, 26)
        self.assertEqual(
            "".join([char["character"] for char in font.get_characters()]),
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        )

    def test_subset_with_unicodes_set_of_int(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 875)
        unicodes = {*range(65, 91)}
        font.subset(unicodes=unicodes)
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, len(unicodes))
        self.assertEqual(chars_count, 26)
        self.assertEqual(
            "".join([char["character"] for char in font.get_characters()]),
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        )

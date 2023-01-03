from tests import AbstractTestCase


class UnicodeBlocksAndScriptsTestCase(AbstractTestCase):
    """
    Test case for the methods related to the font unicode blocks and scripts.
    """

    def test_get_unicode_block_by_name(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        block = font.get_unicode_block_by_name(name="basic latin")
        self.assertEqual(
            list(block.keys()),
            ["characters_total", "name", "characters_count", "coverage"],
        )
        self.assertEqual(block["name"], "Basic Latin")

    def test_get_unicode_block_by_name_with_invalid_name(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        block = font.get_unicode_block_by_name(name="basic latin invalid")
        self.assertEqual(block, None)

    def test_get_unicode_blocks_with_coverage_threshold(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        blocks = font.get_unicode_blocks(coverage_threshold=0.9)
        expected_blocks = [
            {
                "characters_count": 160,
                "characters_total": 160,
                "coverage": 1.0,
                "name": "Enclosed Alphanumerics",
            },
            {
                "characters_count": 128,
                "characters_total": 128,
                "coverage": 1.0,
                "name": "Box Drawing",
            },
            {
                "characters_count": 32,
                "characters_total": 32,
                "coverage": 1.0,
                "name": "Block Elements",
            },
            {
                "characters_count": 214,
                "characters_total": 224,
                "coverage": 0.9553571428571429,
                "name": "Kangxi Radicals",
            },
            {
                "characters_count": 64,
                "characters_total": 64,
                "coverage": 1.0,
                "name": "CJK Symbols and Punctuation",
            },
            {
                "characters_count": 93,
                "characters_total": 96,
                "coverage": 0.96875,
                "name": "Hiragana",
            },
            {
                "characters_count": 96,
                "characters_total": 96,
                "coverage": 1.0,
                "name": "Katakana",
            },
            {
                "characters_count": 93,
                "characters_total": 96,
                "coverage": 0.96875,
                "name": "Hangul Compatibility Jamo",
            },
            {
                "characters_count": 16,
                "characters_total": 16,
                "coverage": 1.0,
                "name": "Kanbun",
            },
            {
                "characters_count": 16,
                "characters_total": 16,
                "coverage": 1.0,
                "name": "Katakana Phonetic Extensions",
            },
            {
                "characters_count": 255,
                "characters_total": 256,
                "coverage": 0.99609375,
                "name": "Enclosed CJK Letters and Months",
            },
            {
                "characters_count": 255,
                "characters_total": 256,
                "coverage": 0.99609375,
                "name": "CJK Compatibility",
            },
            {
                "characters_count": 32,
                "characters_total": 32,
                "coverage": 1.0,
                "name": "CJK Compatibility Forms",
            },
            {
                "characters_count": 224,
                "characters_total": 240,
                "coverage": 0.9333333333333333,
                "name": "Halfwidth and Fullwidth Forms",
            },
        ]
        self.assertEqual(blocks, expected_blocks)

    def test_get_unicode_script_by_name(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        script = font.get_unicode_script_by_name(name="Latin")
        self.assertEqual(
            list(script.keys()),
            ["characters_total", "name", "tag", "characters_count", "coverage"],
        )
        self.assertEqual(script["name"], "Latin")

    def test_get_unicode_script_by_name_with_tag(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        script = font.get_unicode_script_by_name(name="latn")
        self.assertEqual(
            list(script.keys()),
            ["characters_total", "name", "tag", "characters_count", "coverage"],
        )
        self.assertEqual(script["tag"], "Latn")

    def test_get_unicode_script_by_name_with_invalid_name(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        script = font.get_unicode_script_by_name(name="Latin Invalid")
        self.assertEqual(script, None)

    def test_get_unicode_scripts(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        scripts = font.get_unicode_scripts()
        expected_scripts = [
            {
                "characters_count": 1505,
                "characters_total": 8301,
                "coverage": 0.1813034574147693,
                "name": "Common",
                "tag": "Zyyy",
            },
            {
                "characters_count": 345,
                "characters_total": 1481,
                "coverage": 0.23295070898041864,
                "name": "Latin",
                "tag": "Latn",
            },
            {
                "characters_count": 73,
                "characters_total": 77,
                "coverage": 0.948051948051948,
                "name": "Bopomofo",
                "tag": "Bopo",
            },
            {
                "characters_count": 13,
                "characters_total": 657,
                "coverage": 0.0197869101978691,
                "name": "Inherited",
                "tag": "Zinh",
            },
            {
                "characters_count": 50,
                "characters_total": 518,
                "coverage": 0.09652509652509653,
                "name": "Greek",
                "tag": "Grek",
            },
            {
                "characters_count": 66,
                "characters_total": 506,
                "coverage": 0.13043478260869565,
                "name": "Cyrillic",
                "tag": "Cyrl",
            },
            {
                "characters_count": 208,
                "characters_total": 11739,
                "coverage": 0.017718715393133997,
                "name": "Hangul",
                "tag": "Hang",
            },
            {
                "characters_count": 18100,
                "characters_total": 98408,
                "coverage": 0.18392813592390864,
                "name": "Han",
                "tag": "Hani",
            },
            {
                "characters_count": 90,
                "characters_total": 381,
                "coverage": 0.23622047244094488,
                "name": "Hiragana",
                "tag": "Hira",
            },
            {
                "characters_count": 298,
                "characters_total": 321,
                "coverage": 0.9283489096573209,
                "name": "Katakana",
                "tag": "Kana",
            },
        ]
        self.assertEqual(scripts, expected_scripts)

    def test_get_unicode_scripts_with_coverage_threshold(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        scripts = font.get_unicode_scripts(coverage_threshold=0.9)
        expected_scripts = [
            {
                "characters_count": 73,
                "characters_total": 77,
                "coverage": 0.948051948051948,
                "name": "Bopomofo",
                "tag": "Bopo",
            },
            {
                "characters_count": 298,
                "characters_total": 321,
                "coverage": 0.9283489096573209,
                "name": "Katakana",
                "tag": "Kana",
            },
        ]
        self.assertEqual(scripts, expected_scripts)

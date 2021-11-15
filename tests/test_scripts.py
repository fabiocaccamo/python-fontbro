# -*- coding: utf-8 -*-

from tests import AbstractTestCase


class ScriptsTestCase(AbstractTestCase):
    '''
    Test case for the methods related to the font scripts.
    '''

    def test_get_scripts(self):
        font = self._get_font('/Noto_Sans_TC/NotoSansTC-Regular.otf')
        scripts = font.get_scripts()
        # self._print(scripts)
        expected_scripts = [
            {
                'tag': 'Bopo',
                'name': 'Bopomofo',
                'blocks': ['Bopomofo', 'Bopomofo Extended', 'Spacing Modifier Letters'],
            },
            {'tag': 'Cyrl', 'name': 'Cyrillic', 'blocks': ['Cyrillic']},
            {
                'tag': 'Grek',
                'name': 'Greek',
                'blocks': ['Greek and Coptic', 'Letterlike Symbols'],
            },
            {
                'tag': 'Hang',
                'name': 'Hangul',
                'blocks': [
                    'CJK Symbols and Punctuation',
                    'Enclosed CJK Letters and Months',
                    'Halfwidth and Fullwidth Forms',
                    'Hangul Compatibility Jamo',
                ],
            },
            {
                'tag': 'Hani',
                'name': 'Han',
                'blocks': [
                    'CJK Compatibility Ideographs',
                    'CJK Compatibility Ideographs Supplement',
                    'CJK Radicals Supplement',
                    'CJK Symbols and Punctuation',
                    'CJK Unified Ideographs',
                    'CJK Unified Ideographs Extension A',
                    'CJK Unified Ideographs Extension B',
                    'CJK Unified Ideographs Extension C',
                    'CJK Unified Ideographs Extension F',
                    'CJK Unified Ideographs Extension G',
                    'Kangxi Radicals',
                ],
            },
            {
                'tag': 'Hira',
                'name': 'Hiragana',
                'blocks': ['Enclosed Ideographic Supplement', 'Hiragana'],
            },
            {
                'tag': 'Kana',
                'name': 'Katakana',
                'blocks': [
                    'CJK Compatibility',
                    'Enclosed CJK Letters and Months',
                    'Halfwidth and Fullwidth Forms',
                    'Katakana',
                    'Katakana Phonetic Extensions',
                ],
            },
            {
                'tag': 'Latn',
                'name': 'Latin',
                'blocks': [
                    'Alphabetic Presentation Forms',
                    'Basic Latin',
                    'Halfwidth and Fullwidth Forms',
                    'IPA Extensions',
                    'Latin Extended Additional',
                    'Latin Extended-A',
                    'Latin Extended-B',
                    'Latin-1 Supplement',
                    'Letterlike Symbols',
                    'Number Forms',
                ],
            },
            {
                'tag': 'Zinh',
                'name': 'Inherited',
                'blocks': [
                    'CJK Symbols and Punctuation',
                    'Combining Diacritical Marks',
                    'Combining Diacritical Marks for Symbols',
                    'Hiragana',
                ],
            },
            {
                'tag': 'Zyyy',
                'name': 'Common',
                'blocks': [
                    'Arrows',
                    'Basic Latin',
                    'Block Elements',
                    'Box Drawing',
                    'CJK Compatibility',
                    'CJK Compatibility Forms',
                    'CJK Strokes',
                    'CJK Symbols and Punctuation',
                    'Control Pictures',
                    'Currency Symbols',
                    'Dingbats',
                    'Enclosed Alphanumeric Supplement',
                    'Enclosed Alphanumerics',
                    'Enclosed CJK Letters and Months',
                    'Enclosed Ideographic Supplement',
                    'General Punctuation',
                    'Geometric Shapes',
                    'Halfwidth and Fullwidth Forms',
                    'Hiragana',
                    'Ideographic Description Characters',
                    'Kanbun',
                    'Katakana',
                    'Latin-1 Supplement',
                    'Letterlike Symbols',
                    'Mathematical Operators',
                    'Miscellaneous Mathematical Symbols-B',
                    'Miscellaneous Symbols',
                    'Miscellaneous Symbols and Arrows',
                    'Miscellaneous Technical',
                    'Small Form Variants',
                    'Spacing Modifier Letters',
                    'Superscripts and Subscripts',
                    'Supplemental Arrows-B',
                    'Supplemental Punctuation',
                    'Vertical Forms',
                ],
            },
        ]
        self.assertEqual(scripts, expected_scripts)

    def test_get_script_by_character(self):
        font = self._get_font('/Noto_Sans_TC/NotoSansTC-Regular.otf')
        script = font.get_script_by_character('a')
        expected_script = {'tag': 'Latn', 'name': 'Latin', 'block': 'Basic Latin'}
        self.assertEqual(script, expected_script)


if __name__ == '__main__':
    unittest.main()

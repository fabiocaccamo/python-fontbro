from fontbro.exceptions import DataError
from fontbro.support import (
    _SAMPLE_TEXT_FIELDS,
    _WRITING_SYSTEMS_COMMON,
    _get_languages_data,
)
from tests import AbstractTestCase


class SupportTestCase(AbstractTestCase):
    """
    Test case for the methods related to the languages and
    writing systems supported by the font.
    """

    def test_get_supported_languages(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        languages = font.get_supported_languages()
        self.assertTrue(languages)

        english = next(item for item in languages if item["code"] == "en_Latn")
        self.assertEqual(
            sorted(english.keys()),
            [
                "code",
                "coverage",
                "name",
                "sample_texts",
                "writing_system_code",
                "writing_system_name",
            ],
        )
        self.assertEqual(english["name"], "English")
        self.assertEqual(english["writing_system_code"], "Latn")
        self.assertEqual(english["writing_system_name"], "Latin")
        self.assertEqual(english["coverage"], 1.0)

    def test_get_supported_languages_sample_texts(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        languages = font.get_supported_languages()

        english = next(item for item in languages if item["code"] == "en_Latn")
        sample_texts = english["sample_texts"]
        self.assertEqual(
            sorted(sample_texts.keys()),
            sorted(("alphabet", *_SAMPLE_TEXT_FIELDS)),
        )
        self.assertIn("A B C", sample_texts["alphabet"])
        self.assertTrue(sample_texts["tester"])

        # each language provides its own sample texts, not the ones of the
        # most spoken language of its writing system (english, for latin)
        italian = next(item for item in languages if item["code"] == "it_Latn")
        self.assertTrue(italian["sample_texts"]["tester"])
        self.assertNotEqual(italian["sample_texts"]["tester"], sample_texts["tester"])

    def test_get_supported_languages_with_coverage_threshold(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        languages = font.get_supported_languages()
        languages_codes = {item["code"] for item in languages}
        partially_supported_languages = font.get_supported_languages(
            coverage_threshold=0.9,
        )
        partially_supported_languages_codes = {
            item["code"] for item in partially_supported_languages
        }
        # a lower threshold always returns a superset of the fully supported languages
        self.assertTrue(languages_codes < partially_supported_languages_codes)
        # traditional chinese is missing a single base character in this font
        self.assertNotIn("zh_Hant", languages_codes)
        self.assertIn("zh_Hant", partially_supported_languages_codes)
        for language in partially_supported_languages:
            self.assertTrue(0.9 <= language["coverage"] <= 1.0)

    def test_get_supported_languages_without_unicode_cmap(self):
        # this font doesn't provide any unicode cmap subtable,
        # get_characters raises a DataError on it too
        font = self._get_font("/issues/issue-0048/test.ttf")
        with self.assertRaises(DataError):
            font.get_supported_languages()
        with self.assertRaises(DataError):
            font.get_supported_writing_systems()

    def test_get_supported_writing_systems(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        writing_systems = font.get_supported_writing_systems()
        self.assertTrue(writing_systems)

        latin = next(item for item in writing_systems if item["code"] == "Latn")
        self.assertEqual(
            sorted(latin.keys()),
            [
                "code",
                "coverage",
                "languages_count",
                "languages_supported_count",
                "name",
                "sample_texts",
            ],
        )
        self.assertEqual(latin["name"], "Latin")
        self.assertTrue(0.0 < latin["coverage"] <= 1.0)
        self.assertTrue(
            0 < latin["languages_supported_count"] <= latin["languages_count"]
        )
        self.assertTrue(latin["sample_texts"]["tester"])

    def test_get_supported_writing_systems_names(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        writing_systems = font.get_supported_writing_systems(coverage_threshold=0.9)
        names_by_code = {item["code"]: item["name"] for item in writing_systems}
        self.assertEqual(names_by_code.get("Hant"), "Traditional Han")
        self.assertEqual(names_by_code.get("Hira"), "Hiragana")
        self.assertEqual(names_by_code.get("Kana"), "Katakana")

    def test_get_supported_writing_systems_matches_supported_languages(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        languages = font.get_supported_languages()
        writing_systems = font.get_supported_writing_systems()
        self.assertEqual(
            {item["code"] for item in writing_systems},
            {item["writing_system_code"] for item in languages},
        )
        languages_count_by_code = {
            item["code"]: item["languages_supported_count"] for item in writing_systems
        }
        for writing_system_code, languages_count in languages_count_by_code.items():
            self.assertEqual(
                languages_count,
                len(
                    [
                        item
                        for item in languages
                        if item["writing_system_code"] == writing_system_code
                    ]
                ),
            )

    def test_get_supported_writing_systems_with_prioritize_common(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        writing_systems = font.get_supported_writing_systems()
        codes = [item["code"] for item in writing_systems]
        self.assertEqual(codes[0], "Latn")
        # the most common writing systems are returned in a predefined order
        self.assertEqual(
            [code for code in codes if code in _WRITING_SYSTEMS_COMMON],
            [code for code in _WRITING_SYSTEMS_COMMON if code in codes],
        )

        writing_systems = font.get_supported_writing_systems(prioritize_common=False)
        names = [item["name"] for item in writing_systems]
        self.assertEqual(names, sorted(names))
        self.assertEqual(
            {item["code"] for item in writing_systems},
            set(codes),
        )

    def test_get_supported_writing_systems_with_include_uncommon(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        # no font of the test suite supports an uncommon writing system,
        # the armenian characters are added to the cmap of this one
        armenian = next(
            item for item in _get_languages_data() if item["code"] == "hy_Armn"
        )
        cmap = font.get_ttfont()["cmap"].getBestCmap()
        cmap.update(dict.fromkeys(armenian["base_codepoints"], ".notdef"))

        writing_systems = font.get_supported_writing_systems()
        codes = [item["code"] for item in writing_systems]
        self.assertIn("Armn", codes)

        writing_systems = font.get_supported_writing_systems(include_uncommon=False)
        common_codes = [item["code"] for item in writing_systems]
        self.assertNotIn("Armn", common_codes)
        self.assertEqual(
            common_codes,
            [code for code in codes if code in _WRITING_SYSTEMS_COMMON],
        )

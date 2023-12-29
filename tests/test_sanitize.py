import fsutil

from fontbro import Font
from tests import AbstractTestCase


class SanitizeTestCase(AbstractTestCase):
    """
    This class describes a sanitize test case.
    """

    def _test_sanitize(
        self,
        dirpath,
        *,
        strict,
        expected_errors_count,
    ):
        fonts_dir = fsutil.join_path(__file__, dirpath)
        fonts_files = fsutil.list_files(fonts_dir)
        errors_count = 0
        for font_file in fonts_files:
            with self.subTest(font_file):
                try:
                    font = Font(font_file)
                except Exception:
                    continue
                try:
                    font.sanitize(strict=strict)
                except Exception:
                    errors_count += 1
        self.assertEqual(errors_count, expected_errors_count)

    def test_sanitize_with_bad_fonts(self):
        self._test_sanitize(
            "fonts-ots/bad",
            strict=False,
            expected_errors_count=103,
        )

    def test_sanitize_strict_with_bad_fonts(self):
        self._test_sanitize(
            "fonts-ots/bad",
            strict=True,
            expected_errors_count=103,
        )

    def test_sanitize_with_fuzzing_fonts(self):
        self._test_sanitize(
            "fonts-ots/fuzzing",
            strict=False,
            expected_errors_count=42,
        )

    def test_sanitize_strict_with_fuzzing_fonts(self):
        self._test_sanitize(
            "fonts-ots/fuzzing",
            strict=True,
            expected_errors_count=42,
        )

    def test_sanitize_with_good_fonts(self):
        # some fonts have version == "OTTO" but there is not "CFF " table
        self._test_sanitize(
            "fonts-ots/good",
            strict=False,
            expected_errors_count=10,
        )

    def test_sanitize_strict_with_good_fonts(self):
        # some fonts have version == "OTTO" but there is not "CFF " table
        self._test_sanitize(
            "fonts-ots/good",
            strict=True,
            expected_errors_count=10,
        )

import logging
import subprocess
from unittest import mock

import fsutil

from fontbro import Font
from fontbro.exceptions import SanitizationError
from tests import AbstractTestCase


class SanitizeTestCase(AbstractTestCase):
    """
    This class describes a sanitize test case.
    """

    # fontTools uses log.error()/log.warning() when parsing malformed tables
    # (e.g. "skipping malformed name record", "timestamp out of range").
    # NullHandler prevents Python's lastResort from printing them to stderr.
    _fonttools_null_handler = logging.NullHandler()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        logging.getLogger("fontTools").addHandler(cls._fonttools_null_handler)

    @classmethod
    def tearDownClass(cls):
        logging.getLogger("fontTools").removeHandler(cls._fonttools_null_handler)
        super().tearDownClass()

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
                    # there are some ttc files
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
        self._test_sanitize(
            "fonts-ots/good",
            strict=False,
            expected_errors_count=0,
        )

    def test_sanitize_strict_with_good_fonts(self):
        self._test_sanitize(
            "fonts-ots/good",
            strict=True,
            expected_errors_count=0,
        )

    def test_sanitize_strict_warnings_message(self):
        # regression: the warnings must not be truncated when removing the
        # sanitizer success message (str.rstrip removes any of its characters)
        result = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="WARNING: CFF: bad table\nFile sanitized successfully!\n",
            stderr="",
        )
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        with mock.patch("fontbro.sanitize.ots.sanitize", return_value=result):
            with self.assertRaises(SanitizationError) as context:
                font.sanitize(strict=True)
            self.assertEqual(
                str(context.exception),
                "OpenType Sanitizer warnings: \nWARNING: CFF: bad table\n",
            )
            # warnings are ignored when not strict
            font.sanitize(strict=False)

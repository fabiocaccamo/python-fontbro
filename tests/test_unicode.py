from fontTools.ttLib import TTFont

from fontbro.exceptions import DataError
from fontbro.unicode import get_best_cmap, get_best_cmap_or_raise
from tests import AbstractTestCase

FONT_PATH = "/Roboto_Mono/static/RobotoMono-Regular.ttf"


class UnicodeTestCase(AbstractTestCase):
    """
    Test case for the unicode module functions.
    """

    def _get_ttfont(self):
        return TTFont(self._get_font_path(FONT_PATH))

    def _remove_unicode_cmap_subtables(self, ttfont):
        cmap_table = ttfont["cmap"]
        cmap_table.tables = [
            table for table in cmap_table.tables if not table.isUnicode()
        ]

    def test_get_best_cmap(self):
        ttfont = self._get_ttfont()
        cmap = get_best_cmap(ttfont)
        self.assertEqual(cmap, ttfont["cmap"].getBestCmap())
        self.assertEqual(cmap[ord("A")], "A")
        self.assertEqual(get_best_cmap_or_raise(ttfont), cmap)

    def test_get_best_cmap_without_unicode_cmap(self):
        ttfont = self._get_ttfont()
        self._remove_unicode_cmap_subtables(ttfont)
        self.assertIsNone(get_best_cmap(ttfont))
        with self.assertRaises(DataError):
            get_best_cmap_or_raise(ttfont)

    def test_get_best_cmap_without_cmap_table(self):
        ttfont = self._get_ttfont()
        del ttfont["cmap"]
        self.assertIsNone(get_best_cmap(ttfont))
        with self.assertRaises(DataError):
            get_best_cmap_or_raise(ttfont)

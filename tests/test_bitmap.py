from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._g_l_y_f import Glyph

from fontbro.bitmap import is_bitmap
from tests import AbstractTestCase

FONT_PATH = "/Roboto_Mono/static/RobotoMono-Regular.ttf"


class BitmapTestCase(AbstractTestCase):
    """
    Test case for the methods related to the bitmap fonts detection.
    """

    def _add_tables(self, ttfont, tags):
        for tag in tags:
            ttfont[tag] = newTable(tag)

    def _remove_outlines_tables(self, ttfont):
        del ttfont["glyf"]
        del ttfont["loca"]

    def test_is_bitmap_with_outline_fonts(self):
        fonts_paths = [
            "/Honk/static/Honk-Regular.ttf",
            "/Nabla/static/Nabla-Regular.ttf",
            "/Noto_Sans_TC/NotoSansTC-Regular.otf",
            "/Roboto_Mono/static/RobotoMono-Regular.ttf",
            "/Silkscreen/Silkscreen-Regular.ttf",
        ]
        for font_path in fonts_paths:
            with self.subTest(font_path=font_path):
                with self._get_font(font_path) as font:
                    self.assertFalse(font.is_bitmap())

    def test_is_bitmap_without_outlines_tables(self):
        for tags in [("EBDT", "EBLC"), ("bdat", "bloc")]:
            with self.subTest(tags=tags):
                with self._get_font(FONT_PATH) as font:
                    self._remove_outlines_tables(font.get_ttfont())
                    self._add_tables(font.get_ttfont(), tags)
                    self.assertTrue(font.is_bitmap())

    def test_is_bitmap_with_empty_outlines(self):
        # outlines tables with empty glyphs only, the ".notdef" glyph is ignored
        with self._get_font(FONT_PATH) as font:
            ttfont = font.get_ttfont()
            glyf = ttfont["glyf"]
            for glyph_name in ttfont.getGlyphOrder():
                if glyph_name != ".notdef":
                    glyf[glyph_name] = Glyph()
            self._add_tables(ttfont, ("EBDT", "EBLC"))
            self.assertTrue(font.is_bitmap())

    def test_is_bitmap_with_outlines_and_embedded_bitmaps(self):
        # outline fonts with embedded bitmaps (eg. for small sizes) are not bitmap fonts
        with self._get_font(FONT_PATH) as font:
            self._add_tables(font.get_ttfont(), ("EBDT", "EBLC"))
            self.assertFalse(font.is_bitmap())

    def test_is_bitmap_with_incomplete_bitmap_tables(self):
        # bitmap data without bitmap location (and viceversa) is not valid
        for tags in [("EBDT",), ("EBLC",), ("bdat",), ("bloc",)]:
            with self.subTest(tags=tags):
                with self._get_font(FONT_PATH) as font:
                    self._remove_outlines_tables(font.get_ttfont())
                    self._add_tables(font.get_ttfont(), tags)
                    self.assertFalse(font.is_bitmap())

    def test_is_bitmap_with_color_bitmap_tables(self):
        # color bitmap fonts (emoji / images) are not considered bitmap fonts
        for tags in [("CBDT", "CBLC"), ("sbix",)]:
            with self.subTest(tags=tags):
                with self._get_font(FONT_PATH) as font:
                    self._remove_outlines_tables(font.get_ttfont())
                    self._add_tables(font.get_ttfont(), tags)
                    self.assertFalse(font.is_bitmap())

    def test_is_bitmap_module_with_ttfont(self):
        # the module functions work directly on a fontTools TTFont
        ttfont = TTFont(self._get_font_path(FONT_PATH))
        self.assertFalse(is_bitmap(ttfont))
        self._remove_outlines_tables(ttfont)
        self._add_tables(ttfont, ("EBDT", "EBLC"))
        self.assertTrue(is_bitmap(ttfont))

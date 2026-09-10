from fontTools.ttLib import TTFont

from fontbro.monospace import is_monospace
from tests import AbstractTestCase


class MonospaceTestCase(AbstractTestCase):
    """
    This class describes a monospace test case.
    """

    def _remove_ascii_from_cmap(self, font):
        for table in font.get_ttfont()["cmap"].tables:
            for codepoint in range(0x20, 0x7F):
                table.cmap.pop(codepoint, None)

    def test_is_monospace(self):
        with self._get_font("/Inter/static/Inter-Regular.ttf") as font:
            self.assertFalse(font.is_monospace())
        with self._get_font("/Open_Sans/static/OpenSans-Regular.ttf") as font:
            self.assertFalse(font.is_monospace())
        with self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf") as font:
            self.assertTrue(font.is_monospace())
            self.assertTrue(font.is_monospace(threshold=1.0))

    def test_is_monospace_with_cjk_font(self):
        # regression: cjk fonts with proportional latin glyphs are not monospace
        # (most of their glyphs are full-width ideographs with the same width)
        with self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf") as font:
            self.assertFalse(font.is_monospace())

    def test_is_monospace_without_ascii_characters(self):
        # fonts not covering printable ascii characters are monospace
        # if their characters glyphs have at most 2 different widths
        with self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf") as font:
            self._remove_ascii_from_cmap(font)
            self.assertTrue(font.is_monospace())
        with self._get_font("/Inter/static/Inter-Regular.ttf") as font:
            self._remove_ascii_from_cmap(font)
            self.assertFalse(font.is_monospace())

    def test_is_monospace_without_cmap_table(self):
        with self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf") as font:
            del font.get_ttfont()["cmap"]
            self.assertFalse(font.is_monospace())

    def test_is_monospace_module_with_ttfont(self):
        # the module functions work directly on a fontTools TTFont
        ttfont = TTFont(
            self._get_font_path("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        )
        self.assertTrue(is_monospace(ttfont))

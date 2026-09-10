from fontbro.exceptions import DataError
from tests import AbstractTestCase


class SVGTestCase(AbstractTestCase):
    """
    This class describes an image test case.
    """

    def test_generate_svg(self):
        # font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        font = self._get_font("/Inter/static/Inter-Black.ttf")
        svg = font.get_svg(
            text="Hello World!",
            size=16,
        )
        # print(svg)
        self.assertTrue(svg.startswith("<svg "))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertFalse("{" in svg)
        self.assertFalse("}" in svg)

    def test_generate_svg_without_unicode_cmap(self):
        # regression: fonts without unicode cmap must raise DataError
        # (instead of AttributeError / KeyError)
        font = self._get_font("/Inter/static/Inter-Black.ttf")
        cmap_table = font.get_ttfont()["cmap"]
        cmap_table.tables = [
            table for table in cmap_table.tables if not table.isUnicode()
        ]
        with self.assertRaises(DataError):
            font.get_svg(text="Hello World!", size=16)
        del font.get_ttfont()["cmap"]
        with self.assertRaises(DataError):
            font.get_svg(text="Hello World!", size=16)

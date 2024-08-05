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

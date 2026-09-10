from fontbro import Font
from tests import AbstractTestCase


class WidthTestCase(AbstractTestCase):
    """
    Test case for the methods related to the font width.
    """

    def _test_font_width(self, filepath, expected_value, expected_name):
        font_path = self._get_font_path(filepath)
        font = Font(filepath=font_path)
        width = font.get_width()
        # print(filepath, width)
        expected_width = {"value": expected_value, "perc": 100.0, "name": expected_name}
        self.assertEqual(width, expected_width)

    def test_get_width(self):
        self._test_font_width(
            filepath="/Noto_Sans_TC/NotoSansTC-Thin.otf",
            expected_value=5,
            expected_name=Font.WIDTH_MEDIUM,
        )
        self._test_font_width(
            filepath="/Noto_Sans_TC/NotoSansTC-Light.otf",
            expected_value=5,
            expected_name=Font.WIDTH_MEDIUM,
        )
        self._test_font_width(
            filepath="/Noto_Sans_TC/NotoSansTC-Regular.otf",
            expected_value=5,
            expected_name=Font.WIDTH_MEDIUM,
        )
        self._test_font_width(
            filepath="/Noto_Sans_TC/NotoSansTC-Medium.otf",
            expected_value=5,
            expected_name=Font.WIDTH_MEDIUM,
        )
        self._test_font_width(
            filepath="/Noto_Sans_TC/NotoSansTC-Bold.otf",
            expected_value=5,
            expected_name=Font.WIDTH_MEDIUM,
        )
        self._test_font_width(
            filepath="/Noto_Sans_TC/NotoSansTC-Black.otf",
            expected_value=5,
            expected_name=Font.WIDTH_MEDIUM,
        )

    def test_get_width_with_all_width_classes(self):
        # regression: width class 9 is "Ultra-expanded" (not "Ultra-condensed")
        # https://learn.microsoft.com/en-us/typography/opentype/spec/os2#uswidthclass
        expected_widths = {
            1: (50.0, Font.WIDTH_ULTRA_CONDENSED),
            2: (62.5, Font.WIDTH_EXTRA_CONDENSED),
            3: (75.0, Font.WIDTH_CONDENSED),
            4: (87.5, Font.WIDTH_SEMI_CONDENSED),
            5: (100.0, Font.WIDTH_MEDIUM),
            6: (112.5, Font.WIDTH_SEMI_EXPANDED),
            7: (125.0, Font.WIDTH_EXPANDED),
            8: (150.0, Font.WIDTH_EXTRA_EXPANDED),
            9: (200.0, Font.WIDTH_ULTRA_EXPANDED),
        }
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        for value, (perc, name) in expected_widths.items():
            with self.subTest(value=value):
                font.get_ttfont()["OS/2"].usWidthClass = value
                self.assertEqual(
                    font.get_width(), {"value": value, "perc": perc, "name": name}
                )

    def test_get_width_without_os2_table(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        del font.get_ttfont()["OS/2"]
        width = font.get_width()
        self.assertEqual(width, None)

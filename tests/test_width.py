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

from fontbro import Font
from tests import AbstractTestCase


class WeightTestCase(AbstractTestCase):
    """
    Test case for the methods related to the font weight.
    """

    def _test_font_weight(self, filepath, expected_value, expected_name):
        font = self._get_font(filepath)
        weight = font.get_weight()
        # print(filepath, weight)
        expected_weight = {"value": expected_value, "name": expected_name}
        self.assertEqual(weight, expected_weight)

    def test_get_weight(self):
        self._test_font_weight(
            filepath="/Noto_Sans_TC/NotoSansTC-Thin.otf",
            expected_value=250,
            expected_name=Font.WEIGHT_EXTRA_LIGHT,
        )
        self._test_font_weight(
            filepath="/Noto_Sans_TC/NotoSansTC-Light.otf",
            expected_value=300,
            expected_name=Font.WEIGHT_LIGHT,
        )
        self._test_font_weight(
            filepath="/Noto_Sans_TC/NotoSansTC-Regular.otf",
            expected_value=400,
            expected_name=Font.WEIGHT_REGULAR,
        )
        self._test_font_weight(
            filepath="/Noto_Sans_TC/NotoSansTC-Medium.otf",
            expected_value=500,
            expected_name=Font.WEIGHT_MEDIUM,
        )
        self._test_font_weight(
            filepath="/Noto_Sans_TC/NotoSansTC-Bold.otf",
            expected_value=700,
            expected_name=Font.WEIGHT_BOLD,
        )
        self._test_font_weight(
            filepath="/Noto_Sans_TC/NotoSansTC-Black.otf",
            expected_value=900,
            expected_name=Font.WEIGHT_BLACK,
        )

    def test_get_weight_without_os2_table(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        del font.get_ttfont()["OS/2"]
        weight = font.get_weight()
        self.assertEqual(weight, None)

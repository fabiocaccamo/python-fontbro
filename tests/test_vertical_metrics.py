from tests import AbstractTestCase


class VerticalMetricsTestCase(AbstractTestCase):
    """
    Test case for the font vertical-metrics.
    """

    def test_get_vertical_metrics(self):
        # font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        # font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        vertical_metrics = font.get_vertical_metrics()
        # print(vertical_metrics)
        expected_vertical_metrics = {
            "units_per_em": 2000,
            "y_max": 2102,
            "y_min": -533,
            "ascent": 1800,
            "descent": -400,
            "line_gap": 0,
            "typo_ascender": 1800,
            "typo_descender": -400,
            "typo_line_gap": 0,
            "cap_height": 1400,
            "x_height": 1080,
            "win_ascent": 2160,
            "win_descent": 540,
        }
        self.assertEqual(vertical_metrics, expected_vertical_metrics)

    def test_set_vertical_metrics(self):
        # font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        # font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        vertical_metrics = {
            "units_per_em": 2005,
            "y_max": 2105,
            "y_min": -535,
            "ascent": 1805,
            "descent": -405,
            "line_gap": 5,
            "typo_ascender": 1805,
            "typo_descender": -405,
            "typo_line_gap": 5,
            "cap_height": 1405,
            "x_height": 1085,
            "win_ascent": 2165,
            "win_descent": 545,
        }
        expected_vertical_metrics = vertical_metrics.copy()
        font.set_vertical_metrics(**vertical_metrics)
        vertical_metrics = font.get_vertical_metrics()
        # print(vertical_metrics)
        # print(expected_vertical_metrics)
        self.assertEqual(vertical_metrics, expected_vertical_metrics)

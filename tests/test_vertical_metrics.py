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
            "ascent": 1800,
            "cap_height": 1400,
            "x_height": 1080,
            "descent": -400,
            "descender": -400,
        }
        self.assertEqual(vertical_metrics, expected_vertical_metrics)

    def test_set_vertical_metrics(self):
        # font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        # font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        vertical_metrics = {
            "ascent": 1805,
            "cap_height": 1405,
            "x_height": 1085,
            "descent": -405,
            "descender": -405,
        }
        expected_vertical_metrics = vertical_metrics.copy()
        font.set_vertical_metrics(**vertical_metrics)
        vertical_metrics = font.get_vertical_metrics()
        # print(vertical_metrics)
        self.assertEqual(vertical_metrics, expected_vertical_metrics)

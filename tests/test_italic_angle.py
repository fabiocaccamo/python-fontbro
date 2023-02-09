from tests import AbstractTestCase


class ItalicAngleTestCase(AbstractTestCase):
    """
    This class describes an italic angle test case.
    """

    def _test_font_italic_angle(self, filepath, **kwargs):
        font = self._get_font(filepath)
        italic_angle = font.get_italic_angle()
        # print(filepath, weight)
        expected_italic_angle = {
            "backslant": False,
            "italic": False,
            "roman": False,
            "value": 0.0,
        }
        expected_italic_angle.update(**kwargs)
        self.assertEqual(italic_angle, expected_italic_angle)

    def test_get_italic_angle_with_roman_font(self):
        self._test_font_italic_angle(
            filepath="/Roboto_Mono/static/RobotoMono-Regular.ttf",
            value=0,
            roman=True,
        )

    def test_get_italic_angle_with_italic_font(self):
        self._test_font_italic_angle(
            filepath="/Roboto_Mono/static/RobotoMono-Italic.ttf",
            value=-10,
            italic=True,
        )

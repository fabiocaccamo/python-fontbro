from tests import AbstractTestCase


class StrTestCase(AbstractTestCase):
    """
    Test case for the __str__ method.
    """

    def test_str(self):
        filepath = "/Roboto_Mono/static/RobotoMono-Regular.ttf"
        font = self._get_font(filepath)
        s = str(font)
        self.assertTrue(s.startswith("Font('"))
        self.assertTrue(s.endswith(filepath + "')"))

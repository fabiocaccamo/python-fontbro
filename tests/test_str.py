import os

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
        expected_path = filepath.replace("/", os.sep)
        self.assertTrue(s.endswith(expected_path + "')"))

from tests import AbstractTestCase


class MonospaceTestCase(AbstractTestCase):
    """
    This class describes a monospace test case.
    """

    def test_is_monospace(self):
        with self._get_font("/Inter/static/Inter-Regular.ttf") as font:
            self.assertFalse(font.is_monospace())
        with self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf") as font:
            self.assertTrue(font.is_monospace())
        with self._get_font("/Open_Sans/static/OpenSans-Regular.ttf") as font:
            self.assertFalse(font.is_monospace())
        with self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf") as font:
            self.assertTrue(font.is_monospace())

from fontbro import Font
from tests import AbstractTestCase


class ContextManagerTestCase(AbstractTestCase):
    """
    Test case for the font context manager.
    """

    def test_context_manager(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        with Font(filepath=filepath) as font:
            self.assertTrue(len(font.get_names()) > 0)
        with self.assertRaises(ValueError):
            font.get_characters_count()

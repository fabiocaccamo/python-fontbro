from fontbro import Font
from tests import AbstractTestCase


class CloseTestCase(AbstractTestCase):
    """
    Test case for the font close method.
    """

    def test_close(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        font = Font(filepath=filepath)
        font.close()
        with self.assertRaises(ValueError):
            font.get_characters_count()

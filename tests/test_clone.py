from fontbro import Font
from tests import AbstractTestCase


class CloneTestCase(AbstractTestCase):
    """
    This class describes a clone test case.
    """

    def test_clone(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        font = Font(filepath=filepath)
        font_clone = font.clone()
        self.assertFalse(font == font_clone)
        self.assertEqual(f"{font}", f"{font_clone}")

from fontbro import Font
from tests import AbstractTestCase


class CloneTestCase(AbstractTestCase):
    """
    This class describes a clone test case.
    """

    def test_clone_with_filepath(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        font = Font(filepath)
        font_clone = font.clone()
        self.assertFalse(font == font_clone)
        self.assertEqual(f"{font}", f"{font_clone}")

    def test_clone_with_clone(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        font = Font(filepath)
        font_clone1 = font.clone()
        font_clone2 = font_clone1.clone()
        self.assertFalse(font == font_clone2)
        self.assertEqual(f"{font}", f"{font_clone2}")

    def test_clone_with_file_object(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        with open(filepath, "rb") as fileobject:
            font = Font(fileobject)
            font_clone = font.clone()
            self.assertFalse(font == font_clone)
            self.assertEqual(f"{font}", f"{font_clone}")

    def test_clone_with_font(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        font1 = Font(filepath)
        font2 = Font(font1)
        font_clone = font2.clone()
        self.assertFalse(font2 == font_clone)
        self.assertEqual(f"{font2}", f"{font_clone}")

    def test_clone_with_ttfont(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        font1 = Font(filepath)
        font2 = Font(font1.get_ttfont())
        font_clone = font2.clone()
        self.assertFalse(font2 == font_clone)
        self.assertEqual(f"{font2}", f"{font_clone}")

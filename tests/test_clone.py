from fontbro import Font
from tests import AbstractTestCase


class CloneTestCase(AbstractTestCase):
    """
    This class describes a clone test case.
    """

    def test_clone_with_filepath(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        font = Font(filepath=filepath)
        font_clone = font.clone()
        self.assertFalse(font == font_clone)
        self.assertEqual(f"{font}", f"{font_clone}")

    def test_clone_with_file_object(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        with open(filepath, "rb") as fileobject:
            font = Font(fileobject)
            font_clone = font.clone()
            self.assertFalse(font == font_clone)
            self.assertEqual(f"{font}", f"{font_clone}")

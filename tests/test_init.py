from io import BytesIO
from pathlib import Path

from fontTools.ttLib import TTFont

from fontbro import Font
from tests import AbstractTestCase


class InitTestCase(AbstractTestCase):
    """
    Test case for the font constructor.
    """

    def test_init_with_filepath(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        Font(filepath=filepath)

    def test_init_with_filepath_using_pathlib_path(self):
        dirpath = Path(__file__).parent / Path("fonts")
        filepath = dirpath / Path("Noto_Sans_TC/NotoSansTC-Regular.otf")
        Font(filepath=filepath)

    def test_init_with_file_object(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        with open(filepath, "rb") as fh:
            Font(fh)

    def test_init_with_file_object_but_invalid_font_file(self):
        empty = BytesIO()
        with self.assertRaises(ValueError):
            Font(empty)

    def test_init_with_filepath_but_invalid_font_file(self):
        with self.assertRaises(ValueError):
            filepath = self._get_font_path("/Noto_Sans_TC/OFL.txt")
            Font(filepath=filepath)

    def test_init_with_invalid_filepath_value(self):
        with self.assertRaises(ValueError):
            filepath = True
            Font(filepath=filepath)

    def test_init_with_invalid_filepath(self):
        with self.assertRaises(FileNotFoundError):
            filepath = self._get_font_path(
                "/Noto_Sans_TC/NotoSansTC-Regular-Invalid.otf"
            )
            Font(filepath=filepath)

    def test_init_with_ttfont(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        ttfont = TTFont(filepath)
        font1 = Font(ttfont)
        Font(font1.get_ttfont())

    def test_init_with_fontbro_font(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        font1 = Font(filepath)
        Font(font1)

from io import BytesIO
from pathlib import Path

from fontbro import Font
from tests import AbstractTestCase

# from fontTools.ttLib import TTFont


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

    # def test_init_with_font_instance_ttfont(self):
    #     filepath = self._get_font_path('/Noto_Sans_TC/NotoSansTC-Regular.otf')
    #     ttffont = TTFont(filepath)
    #     font1 = Font(font=ttffont)
    #     font2 = Font(font=font1.get_ttfont())

    # def test_init_with_font_instance_fontbro(self):
    #     filepath = self._get_font_path('/Noto_Sans_TC/NotoSansTC-Regular.otf')
    #     font = Font(filepath=filepath)
    #     font2 = Font(font=font)

    # def test_init_with_filepath_and_font_instance(self):
    #     filepath = self._get_font_path('/Noto_Sans_TC/NotoSansTC-Regular.otf')
    #     font = TTFont(filepath)
    #     with self.assertRaises(ValueError):
    #         font = Font(filepath=filepath, font=font)

    # def test_init_without_filepath_and_font_instance(self):
    #     with self.assertRaises(ValueError):
    #         font = Font()

    # def test_init_with_invalid_argument(self):
    #     with self.assertRaises(ValueError):
    #         font = Font(filepath=True)
    #     # with self.assertRaises(ValueError):
    #     #     font = Font(font=True)

from io import BytesIO

from fontbro import Font
from tests import AbstractTestCase


class SaveTestCase(AbstractTestCase):
    """
    Test case for the methods related to the font save method.
    """

    def test_save_with_font_src_path_as_filepath_with_overwrite(self):
        font_filepath = self._get_font_path(
            "/Roboto_Mono/static/RobotoMono-Regular.ttf"
        )
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font_saved_path = font.save(font_filepath, overwrite=True)
        self.assertEqual(font_saved_path, font_filepath)

    def test_save_with_font_src_path_as_filepath_without_overwrite(self):
        font_filepath = self._get_font_path(
            "/Roboto_Mono/static/RobotoMono-Regular.ttf"
        )
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        with self.assertRaises(ValueError):
            font.save(font_filepath)

    def test_save_fileobject(self):
        font_filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        with open(font_filepath, "rb") as fh:
            font = Font(fh)
            font_saved_path = font.save(font_filepath, overwrite=True)
            self.assertEqual(font_saved_path, font_filepath)

    def test_save_fileobject_error(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        with open(filepath, "rb") as fh:
            font = Font(fh)
            with self.assertRaises(ValueError):
                font.save()

    def test_save_to_fileobject(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        buf = BytesIO()
        returned = font.save_to_fileobject(buf)
        returned.seek(0)
        content = returned.read()
        # 00 01 00 00 00 is the file signature for TrueType fonts
        self.assertEqual(content[:5], b"\x00\x01\x00\x00\x00")
        self.assertIs(buf, returned)

    def test_save_to_fileobject_new(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        returned = font.save_to_fileobject()
        returned.seek(0)
        content = returned.read()
        # 00 01 00 00 00 is the file signature for TrueType fonts
        self.assertEqual(content[:5], b"\x00\x01\x00\x00\x00")

    def test_save_as_woff(self):
        # font = self._get_font('/Noto_Sans_TC/NotoSansTC-Regular.otf')
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        output_filepath = self._get_font_temp_path("")

        font_saved_filepath = font.save_as_woff(output_filepath)
        self.assertTrue(font_saved_filepath.endswith(".woff"))
        # ensure that the original font format is not changed
        self.assertEqual(font.get_format(), Font.FORMAT_TTF)
        font_saved = Font(font_saved_filepath)
        self.assertEqual(font_saved.get_format(), Font.FORMAT_WOFF)

    def test_save_as_woff2(self):
        # font = self._get_font('/Noto_Sans_TC/NotoSansTC-Regular.otf')
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        output_filepath = self._get_font_temp_path("")

        font_saved_filepath = font.save_as_woff2(output_filepath)
        self.assertTrue(font_saved_filepath.endswith(".woff2"))
        # ensure that the original font format is not changed
        self.assertEqual(font.get_format(), Font.FORMAT_TTF)
        font_saved = Font(font_saved_filepath)
        self.assertEqual(font_saved.get_format(), Font.FORMAT_WOFF2)

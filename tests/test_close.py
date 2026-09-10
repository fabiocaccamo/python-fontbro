from fontbro import Font
from fontbro.exceptions import OperationError
from tests import AbstractTestCase


class CloseTestCase(AbstractTestCase):
    """
    Test case for the font close method.
    """

    def test_close(self):
        filepath = self._get_font_path("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        font = Font(filepath=filepath)
        font.close()
        with self.assertRaises(OperationError):
            font.get_characters_count()

    def test_close_get_ttfont(self):
        # all the font operations get the TTFont instance through get_ttfont
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.close()
        with self.assertRaises(OperationError):
            font.get_ttfont()

    def test_close_operations(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.close()
        operations = [
            font.clone,
            font.get_names,
            font.get_tables,
            font.is_variable,
            lambda: font.get_svg(text="A", size=16),
            lambda: Font(font),
        ]
        for operation in operations:
            with self.subTest(operation=operation):
                with self.assertRaises(OperationError):
                    operation()

    def test_close_ttfont_directly(self):
        # the TTFont can be closed directly, bypassing the Font instance:
        # it relies on fontTools setting the TTFont reader to None when closed
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.get_ttfont().close()
        with self.assertRaises(OperationError):
            font.get_names()
        with self.assertRaises(OperationError):
            font.is_variable()
        # closing the Font instance after the TTFont does nothing
        font.close()
        with self.assertRaises(OperationError):
            font.get_names()

    def test_close_already_closed_font(self):
        # closing an already closed font does nothing
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.close()
        font.close()
        with self.assertRaises(OperationError):
            font.get_names()

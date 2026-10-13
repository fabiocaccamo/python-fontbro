import copy
import pickle

from fontbro.exceptions import (
    ClosedFontError,
    MissingTableError,
    OperationError,
    VariableFontRequiredError,
)
from tests import AbstractTestCase


class ExceptionsTestCase(AbstractTestCase):
    """
    Test case for the specific exceptions (subclasses of OperationError).
    """

    def _get_static_font(self):
        return self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")

    def _get_variable_font(self):
        return self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")

    def _assert_missing_table_error(self, context, table_tag):
        error = context.exception
        self.assertIsInstance(error, OperationError)
        self.assertIsInstance(error, KeyError)
        self.assertEqual(error.table_tag, table_tag)
        self.assertEqual(str(error), f"Invalid {table_tag} table (doesn't exist).")

    def test_closed_font_error(self):
        font = self._get_static_font()
        font.close()
        with self.assertRaises(ClosedFontError) as context:
            font.get_names()
        self.assertIsInstance(context.exception, OperationError)
        self.assertEqual(
            str(context.exception), "Invalid operation, the font is closed."
        )

    def test_missing_table_error_with_custom_message(self):
        error = MissingTableError("OS/2", "Custom message.")
        self.assertEqual(error.table_tag, "OS/2")
        self.assertEqual(str(error), "Custom message.")

    def test_missing_table_error_pickle_and_copy(self):
        # regression: the exception was recreated passing the message as table tag
        for message in (None, "Custom message."):
            error = MissingTableError("OS/2", message)
            for error_copy in (pickle.loads(pickle.dumps(error)), copy.copy(error)):
                with self.subTest(message=message):
                    self.assertEqual(error_copy.table_tag, "OS/2")
                    self.assertEqual(str(error_copy), str(error))

    def test_missing_table_error_set_embedding_permissions(self):
        font = self._get_static_font()
        del font.get_ttfont()["OS/2"]
        with self.assertRaises(MissingTableError) as context:
            font.set_embedding_permissions(installable=True)
        self._assert_missing_table_error(context, "OS/2")

    def test_missing_table_error_set_family_classification(self):
        font = self._get_static_font()
        del font.get_ttfont()["OS/2"]
        with self.assertRaises(MissingTableError) as context:
            font.set_family_classification(class_id=1)
        self._assert_missing_table_error(context, "OS/2")

    def test_missing_table_error_set_name(self):
        font = self._get_static_font()
        del font.get_ttfont()["name"]
        with self.assertRaises(MissingTableError) as context:
            font.set_name("family_name", "Roboto Mono New")
        self._assert_missing_table_error(context, "name")

    def test_missing_table_error_get_variable_instances(self):
        font = self._get_variable_font()
        del font.get_ttfont()["name"]
        with self.assertRaises(MissingTableError) as context:
            font.get_variable_instances()
        self._assert_missing_table_error(context, "name")

    def test_missing_table_error_is_monospace(self):
        font = self._get_static_font()
        del font.get_ttfont()["hmtx"]
        with self.assertRaises(MissingTableError) as context:
            font.is_monospace()
        self._assert_missing_table_error(context, "hmtx")

    def test_missing_table_error_is_pixel(self):
        font = self._get_font("/Silkscreen/Silkscreen-Regular.ttf")
        ttfont = font.get_ttfont()
        # load the glyphs before removing the head table (needed to load them)
        ttfont["glyf"].ensureDecompiled()
        del ttfont["head"]
        with self.assertRaises(MissingTableError) as context:
            font.is_pixel()
        self._assert_missing_table_error(context, "head")

    def test_missing_table_error_get_svg(self):
        for table_tag in ("head", "hhea"):
            with self.subTest(table_tag=table_tag):
                font = self._get_static_font()
                del font.get_ttfont()[table_tag]
                with self.assertRaises(MissingTableError) as context:
                    font.get_svg(text="Hello", size=12)
                self._assert_missing_table_error(context, table_tag)

    def test_variable_font_required_error(self):
        operations = [
            (
                lambda font: font.rename_variable_instances(family_name="New"),
                "Only the instances of a variable font can be renamed.",
            ),
            (
                lambda font: font.save_variable_instances(self._get_font_temp_path()),
                "Only a variable font can be instantiated.",
            ),
            (
                lambda font: font.to_sliced_variable(coordinates={"wght": (100, 400)}),
                "Only a variable font can be sliced.",
            ),
            (
                lambda font: font.to_static(),
                "Only a variable font can be made static.",
            ),
        ]
        for operation, message in operations:
            with self.subTest(message=message):
                font = self._get_static_font()
                with self.assertRaises(VariableFontRequiredError) as context:
                    operation(font)
                self.assertIsInstance(context.exception, OperationError)
                self.assertEqual(str(context.exception), message)

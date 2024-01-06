from fontbro import Font
from tests import AbstractTestCase


class NamesTestCase(AbstractTestCase):
    """
    Test case for the methods related to the font names.
    """

    def test_get_name_by_id(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        family_name = font.get_name(Font.NAME_FAMILY_NAME)
        self.assertEqual(family_name, "Roboto Mono")

    def test_get_name_by_key(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        family_name = font.get_name("family_name")
        self.assertEqual(family_name, "Roboto Mono")

    def test_get_name_by_invalid_type(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        with self.assertRaises(ValueError):
            font.get_name(font)

    def test_get_name_by_invalid_key(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        with self.assertRaises(KeyError):
            font.get_name("invalid_key")

    def test_get_name_by_invalid_id(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        name = font.get_name(999999999)
        self.assertEqual(name, None)

    def test_get_names(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font_names = font.get_names()
        # self._print(font_names)
        expected_keys = [
            "copyright_notice",
            "designer",
            "designer_url",
            "family_name",
            "full_name",
            "license_description",
            "license_info_url",
            "postscript_name",
            "subfamily_name",
            "trademark",
            "unique_identifier",
            "vendor_url",
            "version",
        ]
        expected_keys_in = [key in font_names for key in expected_keys]
        self.assertTrue(all(expected_keys_in))
        self.assertEqual(font_names["family_name"], "Roboto Mono")
        self.assertEqual(font_names["subfamily_name"], "Regular")
        self.assertEqual(font_names["full_name"], "Roboto Mono Regular")
        self.assertEqual(font_names["postscript_name"], "RobotoMono-Regular")

    def test_set_name(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.set_name(Font.NAME_FAMILY_NAME, "Roboto Mono Renamed")
        self.assertEqual(font.get_name(Font.NAME_FAMILY_NAME), "Roboto Mono Renamed")

    def test_set_name_by_invalid_key(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        with self.assertRaises(KeyError):
            font.set_name("invalid_family_name_key", "Roboto Mono Renamed")

    def test_set_names(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.set_names(
            {
                Font.NAME_FAMILY_NAME: "Roboto Mono Renamed",
                Font.NAME_SUBFAMILY_NAME: "Regular Renamed",
            }
        )
        family_name = font.get_name(Font.NAME_FAMILY_NAME)
        self.assertEqual(family_name, "Roboto Mono Renamed")
        subfamily_name = font.get_name(Font.NAME_SUBFAMILY_NAME)
        self.assertEqual(subfamily_name, "Regular Renamed")

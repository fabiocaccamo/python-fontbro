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

    def _get_name_records_by_platform(self, font, name_id):
        return {
            record.platformID: record.toUnicode()
            for record in font.get_ttfont()["name"].names
            if record.nameID == name_id
        }

    def test_set_name_not_encodable_in_mac_roman(self):
        # regression: the mac name record (mac roman encoding) can't encode
        # greek, cyrillic, cjk... so it's not written, otherwise the font
        # would raise UnicodeEncodeError when saved
        for value in ["Ψ Sans", "Шрифт", "思源黑体"]:
            with self.subTest(value=value):
                font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
                font.set_name(Font.NAME_FAMILY_NAME, value)
                self.assertEqual(font.get_name(Font.NAME_FAMILY_NAME), value)
                self.assertEqual(
                    self._get_name_records_by_platform(font, 1), {3: value}
                )
                font_saved = Font(font.save_to_fileobject())
                self.assertEqual(font_saved.get_name(Font.NAME_FAMILY_NAME), value)

    def test_set_name_encodable_in_mac_roman(self):
        # values encodable in mac roman are written in both windows and mac records
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.set_name(Font.NAME_FAMILY_NAME, "Café Sans")
        self.assertEqual(
            self._get_name_records_by_platform(font, 1),
            {1: "Café Sans", 3: "Café Sans"},
        )

    def test_set_name_not_encodable_in_mac_roman_removes_mac_record(self):
        # an existing mac name record is removed to not keep an outdated value
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.set_name(Font.NAME_FAMILY_NAME, "Café Sans")
        font.set_name(Font.NAME_FAMILY_NAME, "Шрифт")
        self.assertEqual(self._get_name_records_by_platform(font, 1), {3: "Шрифт"})

    def test_rename_not_encodable_in_mac_roman(self):
        # regression: renaming with non-latin names must not prevent saving
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.rename(family_name="思源黑体", style_name="Bold")
        font_saved = Font(font.save_to_fileobject())
        self.assertEqual(font_saved.get_family_name(), "思源黑体")
        self.assertEqual(font_saved.get_name(Font.NAME_FULL_NAME), "思源黑体 Bold")

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

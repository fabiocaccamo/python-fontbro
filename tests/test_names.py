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

    def _add_mac_name_record(self, font):
        # the fixtures fonts have only windows name records
        name_table = font.get_ttfont()["name"]
        name_table.setName("Roboto Mono", 1, 1, 0, 0)

    def test_set_name_without_mac_records(self):
        # mac records are legacy (modern tools don't produce them anymore),
        # so they are not added to fonts having only windows records
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.set_name(Font.NAME_FAMILY_NAME, "Café Sans")
        self.assertEqual(self._get_name_records_by_platform(font, 1), {3: "Café Sans"})
        platforms = {record.platformID for record in font.get_ttfont()["name"].names}
        self.assertEqual(platforms, {3})

    def test_set_name_encodable_in_mac_roman(self):
        # values encodable in mac roman are written in both windows and mac records
        # if the font already has mac records
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        self._add_mac_name_record(font)
        font.set_name(Font.NAME_FAMILY_NAME, "Café Sans")
        self.assertEqual(
            self._get_name_records_by_platform(font, 1),
            {1: "Café Sans", 3: "Café Sans"},
        )

    def test_set_name_not_encodable_in_mac_roman_removes_mac_record(self):
        # an existing mac name record is removed to not keep an outdated value,
        # the name is still readable from the windows record
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        self._add_mac_name_record(font)
        self.assertEqual(
            self._get_name_records_by_platform(font, 1),
            {1: "Roboto Mono", 3: "Roboto Mono"},
        )
        font.set_name(Font.NAME_FAMILY_NAME, "Шрифт")
        self.assertEqual(self._get_name_records_by_platform(font, 1), {3: "Шрифт"})
        self.assertEqual(font.get_name(Font.NAME_FAMILY_NAME), "Шрифт")

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

    def test_get_names_consistent_with_get_name(self):
        # regression: get_names returned the last name record found for each name id,
        # (eg. the japanese family name), instead of the same value of get_name
        font = self._get_font("/DotGothic16/DotGothic16-Regular.ttf")
        font_names = font.get_names()
        self.assertEqual(font_names["family_name"], "DotGothic16")
        for key, value in font_names.items():
            with self.subTest(key=key):
                self.assertEqual(font.get_name(key), value)

    def _replace_name_records(self, font, platform_id, plat_enc_id, lang_id):
        # replace all the name records with records of the given platform/language
        name_table = font.get_ttfont()["name"]
        for record in list(name_table.names):
            name_table.setName(
                record.toUnicode(), record.nameID, platform_id, plat_enc_id, lang_id
            )
        for record in list(name_table.names):
            if (record.platformID, record.platEncID, record.langID) != (
                platform_id,
                plat_enc_id,
                lang_id,
            ):
                name_table.names.remove(record)

    def test_get_name_without_windows_english_records(self):
        # regression: names were not found without windows english name records
        platforms_ids = {
            "unicode": (0, 3, 0),
            "windows japanese": (3, 1, 0x411),
            "mac english": (1, 0, 0),
        }
        for label, (platform_id, plat_enc_id, lang_id) in platforms_ids.items():
            with self.subTest(records=label):
                font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
                self._replace_name_records(font, platform_id, plat_enc_id, lang_id)
                self.assertEqual(font.get_name(Font.NAME_FAMILY_NAME), "Roboto Mono")
                self.assertEqual(font.get_family_name(), "Roboto Mono")
                self.assertEqual(font.get_names()["family_name"], "Roboto Mono")

    def test_get_name_with_undecodable_windows_record(self):
        # an undecodable windows record is skipped, the other records are read
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        self._add_mac_name_record(font)
        name_table = font.get_ttfont()["name"]
        # lone utf-16 surrogate
        name_table.getName(1, 3, 1, 0x409).string = b"\xd8\x00"
        self.assertEqual(font.get_name(Font.NAME_FAMILY_NAME), "Roboto Mono")

    def test_get_name_without_name_table(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        del font.get_ttfont()["name"]
        self.assertIsNone(font.get_name(Font.NAME_FAMILY_NAME))
        self.assertEqual(font.get_names(), {})
        self.assertEqual(font.get_family_name(), "")

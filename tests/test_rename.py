from fontbro import Font
from tests import AbstractTestCase


class RenameTestCase(AbstractTestCase):
    """
    Test case for the font renaming.
    """

    def test_rename_with_family_name_and_style_name(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.rename(
            family_name="Roboto Mono New",
            style_name="Bold Italic",
        )
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Roboto Mono New")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "Bold Italic")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Roboto Mono New Bold Italic")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "RobotoMonoNew-BoldItalic")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Roboto Mono New")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "Bold Italic")

    def test_rename_with_family_name_only(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.rename(
            family_name="Roboto Mono New",
        )
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Roboto Mono New")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "Regular")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Roboto Mono New Regular")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "RobotoMonoNew-Regular")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Roboto Mono New")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "Regular")
        font.sanitize()

    def test_rename_update_unique_identifier(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        family_name = font.get_name(key=Font.NAME_FAMILY_NAME)
        family_name = family_name.replace("Mono", "Multi")
        font.rename(
            family_name=family_name,
        )
        font_uid = font.get_name(Font.NAME_UNIQUE_IDENTIFIER)
        self.assertEqual(font_uid, "3.000;GOOG;RobotoMulti-Regular")

    def test_rename_with_family_name_only_issue_0062(self):
        # https://github.com/fabiocaccamo/python-fontbro/issues/62
        font = self._get_font("/issues/issue-0062/ABCTest-Thin.otf")
        # self._print(font.get_names())
        self.assertEqual(
            font.get_names(),
            {
                "family_name": "ABC Test Thin",
                "full_name": "ABC Test Thin",
                "postscript_name": "ABCTest-Thin",
                "subfamily_name": "Regular",
                "typographic_family_name": "ABC Test",
                "typographic_subfamily_name": "Thin",
                "unique_identifier": "1.000;UKWN;ABCTest-Thin",
                "version": "Version 1.000;Glyphs 3.1.2 (3151)",
            },
        )
        family_name = font.get_name(key=Font.NAME_TYPOGRAPHIC_FAMILY_NAME)
        family_name = family_name.replace("ABC", "Hugo")
        font.rename(
            family_name=family_name,
        )
        # self._print(font.get_names())
        self.assertEqual(
            font.get_names(),
            {
                "family_name": "Hugo Test Thin",
                "full_name": "Hugo Test Thin",
                "postscript_name": "HugoTest-Thin",
                "subfamily_name": "Regular",
                "typographic_family_name": "Hugo Test",
                "typographic_subfamily_name": "Thin",
                "unique_identifier": "1.000;UKWN;HugoTest-Thin",
                "version": "Version 1.000;Glyphs 3.1.2 (3151)",
                "wws_family_name": "Hugo Test",
                "wws_subfamily_name": "Thin",
            },
        )
        full_name = font.get_name(key=Font.NAME_FULL_NAME)
        self.assertEqual(full_name, "Hugo Test Thin")

    def test_rename_with_style_name_only(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.rename(
            style_name="Bold Italic",
        )
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Roboto Mono")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "Bold Italic")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Roboto Mono Bold Italic")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "RobotoMono-BoldItalic")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Roboto Mono")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "Bold Italic")

    def test_rename_without_family_name_and_style_name(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.rename(
            family_name="",
            style_name="",
        )
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Roboto Mono")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "Regular")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Roboto Mono Regular")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "RobotoMono-Regular")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Roboto Mono")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "Regular")

    def test_rename_with_final_postscript_name_too_long(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        with self.assertRaises(ValueError):
            font.rename(
                family_name="Roboto Mono New Name Too Long For PostScript Name So Expect Exception",
                style_name="Bold Italic",
            )

    def test_rename_with_style_name_containing_characters_not_allowed_in_postscript_name(
        self,
    ):
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font.rename(
            family_name=" Tourney Custom ",
            style_name=" [wdth-wght] ",
        )
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Tourney Custom [wdth-wght]")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "Regular")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Tourney Custom [wdth-wght]")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "TourneyCustom-wdth-wght")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Tourney Custom")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "[wdth-wght]")

    def test_rename_with_style_flags_disabled(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.set_style_flags(regular=False, bold=False, italic=False)
        font.rename(
            family_name="Roboto Mono New",
            style_name="Bold Italic",
            update_style_flags=False,
        )
        style_flags = font.get_style_flags()
        self.assertFalse(style_flags["regular"])
        self.assertFalse(style_flags["bold"])
        self.assertFalse(style_flags["italic"])

    def test_rename_with_style_flags_enabled(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.set_style_flags(regular=False, bold=False, italic=False)
        font.rename(
            family_name="Roboto Mono New",
            style_name="Bold Italic",
            update_style_flags=True,
        )
        style_flags = font.get_style_flags()
        self.assertFalse(style_flags["regular"])
        self.assertTrue(style_flags["bold"])
        self.assertTrue(style_flags["italic"])

    def test_rename_update_compatible_full_name(self):
        # designer-defined short menu name: only the family name is replaced
        font = self._get_font("/Inter/static/Inter-Bold.ttf")
        font.rename(family_name="Inter New")
        self.assertEqual(font.get_name(Font.NAME_COMPATIBLE_FULL), "Inter New")
        font.rename(style_name="Black")
        self.assertEqual(font.get_name(Font.NAME_COMPATIBLE_FULL), "Inter New")
        font.sanitize()

    def test_rename_update_compatible_full_name_only_existing_records(self):
        # name id 18 is defined only for the macintosh platform,
        # the windows record must not be added
        font = self._get_font("/issues/issue-0050/LeagueGothic-Regular.otf")
        font.rename(family_name="League Gothic New")
        records = [
            (record.platformID, record.toUnicode())
            for record in font.get_ttfont()["name"].names
            if record.nameID == 18
        ]
        self.assertEqual(records, [(1, "League Gothic New Regular")])
        font.sanitize()

    def test_rename_not_add_compatible_full_name(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.rename(family_name="Roboto Mono New")
        self.assertIsNone(font.get_name(Font.NAME_COMPATIBLE_FULL))

    def test_rename_variable_font_update_postscript_names(self):
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        ttfont = font.get_ttfont()
        fvar = ttfont["fvar"]
        instances_names_ids = [instance.subfamilyNameID for instance in fvar.instances]
        instances_names = [font.get_name(name_id) for name_id in instances_names_ids]
        axes_names = [font.get_name(axis.axisNameID) for axis in fvar.axes]
        font.rename(family_name="Tourney Custom")
        self.assertEqual(font.get_name(Font.NAME_POSTSCRIPT_NAME), "TourneyCustom-Thin")
        self.assertEqual(
            font.get_name(Font.NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX),
            "TourneyCustomRoman",
        )
        instances_postscript_names = [
            font.get_name(instance.postscriptNameID) for instance in fvar.instances
        ]
        self.assertEqual(
            instances_postscript_names[:3],
            [
                "TourneyCustomRoman-Thin",
                "TourneyCustomRoman-ExtraLight",
                "TourneyCustomRoman-Light",
            ],
        )
        for name in instances_postscript_names:
            self.assertTrue(name.startswith("TourneyCustomRoman-"))
        # instances and axes names are unchanged
        self.assertEqual(
            [font.get_name(name_id) for name_id in instances_names_ids],
            instances_names,
        )
        self.assertEqual(
            [font.get_name(axis.axisNameID) for axis in fvar.axes],
            axes_names,
        )
        font.sanitize()

    def test_rename_variable_font_postscript_name_prefix_allowed_characters(self):
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font.rename(family_name="Tourney [Custom] 2.0")
        self.assertEqual(
            font.get_name(Font.NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX),
            "TourneyCustom20Roman",
        )

    def test_rename_variable_font_postscript_name_prefix_italic_suffix(self):
        # the old prefix doesn't start with the old family part of the
        # postscript name, so the "Italic" suffix is appended for italic styles
        font = self._get_font("/Tourney/Tourney-Italic-VariableFont_wdth,wght.ttf")
        font.set_name(Font.NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX, "TrnyItalic")
        font.rename(family_name="Tourney Custom")
        self.assertEqual(
            font.get_name(Font.NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX),
            "TourneyCustomItalic",
        )

    def test_rename_variable_font_without_postscript_name_prefix(self):
        font = self._get_font("/Roboto_Mono/RobotoMono-VariableFont_wght.ttf")
        font.rename(family_name="Roboto Mono New")
        self.assertIsNone(font.get_name(Font.NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX))
        fvar = font.get_ttfont()["fvar"]
        instances_postscript_names = [
            font.get_name(instance.postscriptNameID) for instance in fvar.instances
        ]
        self.assertEqual(
            instances_postscript_names[:3],
            ["RobotoMonoNew-Thin", "RobotoMonoNew-Light", "RobotoMonoNew-Regular"],
        )
        self.assertEqual(
            font.get_name(Font.NAME_POSTSCRIPT_NAME), "RobotoMonoNew-Regular"
        )
        font.sanitize()

    def test_rename_cff_font(self):
        # a small cff font is used, because saving a big cff font
        # (eg. Noto Sans TC) after editing its cff table is slow
        font = self._get_font("/issues/issue-0050/LeagueGothic-Regular.otf")
        font.rename(family_name="League Gothic New")
        font_saved = Font(font.save_to_fileobject())
        cff = font_saved.get_ttfont()["CFF "].cff
        top_dict = cff.topDictIndex[0]
        self.assertEqual(cff.fontNames, ["LeagueGothicNew-Regular"])
        self.assertEqual(top_dict.FullName, "League Gothic New Regular")
        self.assertEqual(top_dict.FamilyName, "League Gothic New")
        self.assertEqual(
            font_saved.get_name(Font.NAME_POSTSCRIPT_NAME), "LeagueGothicNew-Regular"
        )
        font.sanitize()

    def test_rename_cff_font_update_fdarray_font_names(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Bold.otf")
        font.rename(family_name="Noto Sans New")
        top_dict = font.get_ttfont()["CFF "].cff.topDictIndex[0]
        font_names = [font_dict.FontName for font_dict in top_dict.FDArray]
        self.assertEqual(font_names[0], "NotoSansNew-Bold-Alphabetic")
        for font_name in font_names:
            self.assertTrue(font_name.startswith("NotoSansNew-Bold-"))

    def test_rename_cff_font_update_weight(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Bold.otf")
        top_dict = font.get_ttfont()["CFF "].cff.topDictIndex[0]
        font.rename(family_name="Noto Sans New")
        # the style is unchanged
        self.assertEqual(top_dict.Weight, "Bold")
        font.rename(style_name="Black Italic")
        self.assertEqual(top_dict.Weight, "Black")
        font.rename(style_name="Italic")
        self.assertEqual(top_dict.Weight, "Regular")

    def test_rename_cff_font_without_family_name(self):
        font = self._get_font("/issues/issue-0062/ABCTest-Thin.otf")
        font.rename(family_name="Hugo Test")
        cff = font.get_ttfont()["CFF "].cff
        top_dict = cff.topDictIndex[0]
        self.assertEqual(cff.fontNames, ["HugoTest-Thin"])
        self.assertEqual(top_dict.FullName, "Hugo Test Thin")
        self.assertIsNone(getattr(top_dict, "FamilyName", None))

    def test_rename_variable_instances_with_family_name(self):
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font.rename_variable_instances(family_name="Tourney Custom")
        self.assertEqual(
            font.get_name(Font.NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX),
            "TourneyCustomRoman",
        )
        fvar = font.get_ttfont()["fvar"]
        self.assertEqual(
            font.get_name(fvar.instances[0].postscriptNameID),
            "TourneyCustomRoman-Thin",
        )
        # the font names are unchanged
        self.assertEqual(font.get_name(Font.NAME_POSTSCRIPT_NAME), "Tourney-Thin")
        font.sanitize()

    def test_rename_variable_instances_with_style_names(self):
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        fvar = font.get_ttfont()["fvar"]
        instance = fvar.instances[1]
        instance_style_name_id = instance.subfamilyNameID
        font.rename_variable_instances(style_names={"extralight": "Ultra Light"})
        # the existing name record is updated (it's shared with STAT)
        self.assertEqual(instance.subfamilyNameID, instance_style_name_id)
        self.assertEqual(font.get_name(instance.subfamilyNameID), "Ultra Light")
        self.assertEqual(
            font.get_name(instance.postscriptNameID), "TourneyRoman-UltraLight"
        )
        self.assertEqual(
            font.get_name(fvar.instances[0].postscriptNameID), "TourneyRoman-Thin"
        )
        # the font style name is unchanged (not the default instance)
        self.assertEqual(font.get_name(Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME), "Thin")
        font.sanitize()

    def test_rename_variable_instances_with_default_instance_style_name(self):
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font.rename_variable_instances(style_names={"thin": "Hair Line"})
        instance = font.get_ttfont()["fvar"].instances[0]
        self.assertEqual(font.get_name(instance.subfamilyNameID), "Hair Line")
        self.assertEqual(
            font.get_name(instance.postscriptNameID), "TourneyRoman-HairLine"
        )
        # the font style name is renamed too
        self.assertEqual(
            font.get_name(Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME), "Hair Line"
        )
        self.assertEqual(font.get_name(Font.NAME_POSTSCRIPT_NAME), "Tourney-HairLine")
        font.sanitize()

    def test_rename_variable_instances_with_default_instance_update_style_flags(self):
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font.rename_variable_instances(style_names={"thin": "Bold"})
        style_flags = font.get_style_flags()
        self.assertFalse(style_flags["regular"])
        self.assertTrue(style_flags["bold"])

    def test_rename_variable_instances_without_update_style_flags(self):
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        style_flags = font.get_style_flags()
        font.rename_variable_instances(
            style_names={"thin": "Bold"}, update_style_flags=False
        )
        self.assertEqual(font.get_style_flags(), style_flags)

    def test_rename_variable_font_with_inconsistent_default_instance_style_name(
        self,
    ):
        # regression: the font style name ("Regular", name id 2) doesn't match
        # the default instance style name ("Thin"), a family rename must not
        # rename the default instance (and the STAT values sharing its name)
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        ttfont = font.get_ttfont()
        ttfont["name"].removeNames(nameID=17)
        ttfont["name"].removeNames(nameID=22)
        font.rename(family_name="Tourney Custom")
        instance = ttfont["fvar"].instances[0]
        self.assertEqual(font.get_name(instance.subfamilyNameID), "Thin")
        self.assertEqual(
            font.get_name(instance.postscriptNameID), "TourneyCustomRoman-Thin"
        )

    def test_rename_variable_font_with_style_name(self):
        # the default instance is renamed too
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font.rename(style_name="Hair Line")
        instance = font.get_ttfont()["fvar"].instances[0]
        self.assertEqual(font.get_name(instance.subfamilyNameID), "Hair Line")
        self.assertEqual(
            font.get_name(instance.postscriptNameID), "TourneyRoman-HairLine"
        )
        font.sanitize()

    def test_rename_variable_font_with_family_name_containing_characters_not_allowed(
        self,
    ):
        # the old prefixes are computed from the old family name,
        # not from the postscript name (where the "-" separator is ambiguous)
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font.rename(family_name="Tourney [X]")
        font.rename(family_name="Tourney New")
        self.assertEqual(
            font.get_name(Font.NAME_VARIATIONS_POSTSCRIPT_NAME_PREFIX),
            "TourneyNewRoman",
        )
        fvar = font.get_ttfont()["fvar"]
        self.assertEqual(
            font.get_name(fvar.instances[0].postscriptNameID), "TourneyNewRoman-Thin"
        )
        font = self._get_font("/Roboto_Mono/RobotoMono-VariableFont_wght.ttf")
        font.rename(family_name="Roboto Mono [X]")
        font.rename(family_name="Roboto Mono New")
        fvar = font.get_ttfont()["fvar"]
        self.assertEqual(
            font.get_name(fvar.instances[0].postscriptNameID), "RobotoMonoNew-Thin"
        )

    def test_rename_variable_font_with_inconsistent_instance_postscript_name(self):
        # the instance postscript name doesn't start with the old prefix,
        # so it's generated (without the "Italic" suffix already in the prefix)
        font = self._get_font("/Tourney/Tourney-Italic-VariableFont_wdth,wght.ttf")
        instance = font.get_ttfont()["fvar"].instances[0]
        font.set_name(instance.postscriptNameID, "Foo-ThinItalic")
        font.rename(family_name="Tourney Custom")
        self.assertEqual(
            font.get_name(instance.postscriptNameID), "TourneyCustomItalic-Thin"
        )

    def test_rename_variable_instances_with_style_names_in_italic_font(self):
        font = self._get_font("/Tourney/Tourney-Italic-VariableFont_wdth,wght.ttf")
        font.rename_variable_instances(style_names={"light italic": "Hair Italic"})
        fvar = font.get_ttfont()["fvar"]
        names = {
            font.get_name(instance.subfamilyNameID): font.get_name(
                instance.postscriptNameID
            )
            for instance in fvar.instances
        }
        self.assertEqual(names["Hair Italic"], "TourneyItalic-Hair")

    def test_rename_variable_font_without_default_instance(self):
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        fvar = font.get_ttfont()["fvar"]
        # remove the default instance ("Thin")
        fvar.instances.pop(0)
        font.rename(style_name="Hair Line")
        self.assertEqual(font.get_name(Font.NAME_POSTSCRIPT_NAME), "Tourney-HairLine")
        self.assertEqual(font.get_name(fvar.instances[0].subfamilyNameID), "ExtraLight")

    def test_rename_variable_font_without_instances_postscript_names(self):
        font = self._get_font("/Inter/Inter-VariableFont_slnt,wght.ttf")
        fvar = font.get_ttfont()["fvar"]
        font.rename(family_name="Inter New")
        self.assertEqual(font.get_name(Font.NAME_POSTSCRIPT_NAME), "InterNew-Regular")
        for instance in fvar.instances:
            self.assertEqual(instance.postscriptNameID, 0xFFFF)

    def test_rename_variable_instances_with_style_name_shared_with_font_style_name(
        self,
    ):
        # the instance style name record is the font subfamily name (2),
        # so a new name record is added for the instance
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        instance = font.get_ttfont()["fvar"].instances[1]
        instance.subfamilyNameID = 2
        font.rename_variable_instances(style_names={"regular": "Normal"})
        self.assertGreater(instance.subfamilyNameID, 255)
        self.assertEqual(font.get_name(instance.subfamilyNameID), "Normal")
        self.assertEqual(font.get_name(Font.NAME_SUBFAMILY_NAME), "Regular")

    def test_rename_variable_instances_with_static_font(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        with self.assertRaises(TypeError):
            font.rename_variable_instances(family_name="Roboto Mono New")

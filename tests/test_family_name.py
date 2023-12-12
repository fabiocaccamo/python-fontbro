from fontbro import Font
from tests import AbstractTestCase


class FamilyNameTestCase(AbstractTestCase):
    """
    Test case for the font get_family_name / set_family_name methods.
    """

    def test_family_name(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        self.assertEqual(font.get_family_name(), "Roboto Mono")
        font.set_family_name("Roboto Mono New")
        self.assertEqual(font.get_family_name(), "Roboto Mono New")
        # check all name records
        names = font.get_names()
        self.assertEqual(names[Font.NAME_FAMILY_NAME], "Roboto Mono New")
        self.assertEqual(names[Font.NAME_SUBFAMILY_NAME], "Regular")
        self.assertEqual(names[Font.NAME_FULL_NAME], "Roboto Mono New Regular")
        self.assertEqual(names[Font.NAME_POSTSCRIPT_NAME], "RobotoMonoNew-Regular")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_FAMILY_NAME], "Roboto Mono New")
        self.assertEqual(names[Font.NAME_TYPOGRAPHIC_SUBFAMILY_NAME], "Regular")
        self.assertEqual(
            names[Font.NAME_UNIQUE_IDENTIFIER], "3.000;GOOG;RobotoMonoNew-Regular"
        )

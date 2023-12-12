from tests import AbstractTestCase


class FilenameTestCase(AbstractTestCase):
    """
    Test case for the font filename generation.
    """

    def test_get_filename_with_static_font(self):
        font = self._get_font("/Tourney/static/Tourney/Tourney-Black.ttf")
        self.assertEqual(
            font.get_filename(),
            "Tourney-Black.ttf",
        )

        font = self._get_font("/Tourney/static/Tourney/Tourney-BlackItalic.ttf")
        self.assertEqual(
            font.get_filename(),
            "Tourney-BlackItalic.ttf",
        )

    def test_get_filename_with_variable_font(self):
        font = self._get_font("/Tourney/Tourney-Italic-VariableFont_wdth,wght.ttf")
        self.assertEqual(
            font.get_filename(),
            "Tourney-Italic-Variable[wght,wdth].ttf",
        )

        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        self.assertEqual(
            font.get_filename(),
            "Tourney-Variable[wght,wdth].ttf",
        )

        font = self._get_font("/Roboto_Mono/RobotoMono-Italic-VariableFont_wght.ttf")
        self.assertEqual(
            font.get_filename(),
            "RobotoMono-Italic-Variable[wght].ttf",
        )

        font = self._get_font("/Roboto_Mono/RobotoMono-VariableFont_wght.ttf")
        self.assertEqual(
            font.get_filename(),
            "RobotoMono-Variable[wght].ttf",
        )

    def test_get_filename_with_variable_font_and_custom_suffixes(self):
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        self.assertEqual(
            font.get_filename(
                variable_suffix="VF",
                variable_axes_tags=False,
                variable_axes_values=False,
            ),
            "Tourney-VF.ttf",
        )

        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        self.assertEqual(
            font.get_filename(
                variable_suffix="VF",
                variable_axes_tags=False,
                variable_axes_values=True,
            ),
            "Tourney-VF.ttf",
        )

        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        self.assertEqual(
            font.get_filename(
                variable_suffix="VF",
                variable_axes_tags=True,
            ),
            "Tourney-VF[wght,wdth].ttf",
        )

        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        self.assertEqual(
            font.get_filename(
                variable_suffix="VF",
                variable_axes_tags=True,
                variable_axes_values=True,
            ),
            "Tourney-VF[wght(100,100,900),wdth(75,100,125)].ttf",
        )

        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        self.assertEqual(
            font.get_filename(
                variable_suffix="",
                variable_axes_tags=True,
            ),
            "Tourney[wght,wdth].ttf",
        )

        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        self.assertEqual(
            font.get_filename(
                variable_suffix="",
                variable_axes_tags=True,
                variable_axes_values=True,
            ),
            "Tourney[wght(100,100,900),wdth(75,100,125)].ttf",
        )

        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        self.assertEqual(
            font.get_filename(
                variable_suffix="",
                variable_axes_tags=False,
            ),
            "Tourney.ttf",
        )

        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        self.assertEqual(
            font.get_filename(
                variable_suffix="",
                variable_axes_tags=False,
                variable_axes_values=True,
            ),
            "Tourney.ttf",
        )

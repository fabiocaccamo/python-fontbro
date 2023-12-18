from tests import AbstractTestCase


class FingerprintTestCase(AbstractTestCase):
    """
    This class describes a fingerprint test case.
    """

    def _get_static_font(self):
        font = self._get_font("/Tourney/static/Tourney/Tourney-Regular.ttf")
        # font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        self.assertTrue(font.is_static())
        return font

    def _get_variable_font(self):
        font = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        # font = self._get_font("/Roboto_Mono/RobotoMono-VariableFont_wght.ttf")
        self.assertTrue(font.is_variable())
        return font

    def test_get_fingerprint_diff_between_variable_instances(self):
        fonts = [
            self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf"),
            self._get_font("/Roboto_Mono/RobotoMono-VariableFont_wght.ttf"),
        ]
        for font in fonts:
            # print(font.get_variable_instances())
            with self.subTest(f"Test with font: {font}", font=font):
                hashes = []
                for instance in font.get_variable_instances():
                    instance_font = font.clone()
                    instance_font.to_static(coordinates=instance["coordinates"])
                    instance_hash = instance_font.get_fingerprint()
                    if len(hashes):
                        diff_from_prev_instance = instance_hash - hashes[-1]
                        # print(diff_from_prev_instance)
                        self.assertTrue(diff_from_prev_instance > 10)
                        # print(instance_hash)
                    hashes.append(instance_hash)

    def test_get_fingerprint_diff_against_all_variable_instances(self):
        fonts = [
            {
                "variable": "/Tourney/Tourney-VariableFont_wdth,wght.ttf",
                "static": "/Tourney/static/Tourney/Tourney-Regular.ttf",
            },
            {
                "variable": "/Roboto_Mono/RobotoMono-VariableFont_wght.ttf",
                "static": "/Roboto_Mono/static/RobotoMono-Regular.ttf",
            },
        ]
        for font in fonts:
            # print(font.get_variable_instances())
            with self.subTest(f"Test with font: {font}", font=font):
                variable_font = self._get_font(font["variable"])
                static_font = self._get_font(font["static"])
                static_font_hash = static_font.get_fingerprint()
                diffs = []
                for instance in variable_font.get_variable_instances():
                    instance_font = variable_font.clone()
                    instance_font.to_static(coordinates=instance["coordinates"])
                    instance_hash = instance_font.get_fingerprint()
                    diff = instance_hash - static_font_hash
                    # print(f"{font} -> {diff}")
                    diffs.append(diff)
                diffs = [diff for diff in diffs if diff <= 10]
                self.assertEqual(len(diffs), 1)

    def test_get_fingerprint_match_with_same_static_fonts(self):
        font_a = self._get_font("/Tourney/static/Tourney/Tourney-Regular.ttf")
        font_b = self._get_font("/Tourney/static/Tourney/Tourney-Regular.ttf")
        match, diff, hash, other_hash = font_a.get_fingerprint_match(
            other=font_b, tolerance=10
        )
        self.assertTrue(match)

    def test_get_fingerprint_match_with_different_static_fonts(self):
        font_a = self._get_font("/Tourney/static/Tourney/Tourney-Medium.ttf")
        font_b = self._get_font("/Tourney/static/Tourney/Tourney-Regular.ttf")
        match, diff, hash, other_hash = font_a.get_fingerprint_match(
            other=font_b, tolerance=10
        )
        self.assertFalse(match)

    def test_get_fingerprint_match_with_same_variable_fonts(self):
        font_a = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font_b = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        match, diff, hash, other_hash = font_a.get_fingerprint_match(
            other=font_b, tolerance=10
        )
        self.assertTrue(match)

    def test_get_fingerprint_match_with_different_variable_fonts(self):
        font_a = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font_b = self._get_font("/Tourney/Tourney-Italic-VariableFont_wdth,wght.ttf")
        match, diff, hash, other_hash = font_a.get_fingerprint_match(
            other=font_b, tolerance=10
        )
        self.assertFalse(match)

    def test_get_fingerprint_match_with_variable_and_static_fonts(self):
        font_a = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font_b = self._get_font("/Tourney/static/Tourney/Tourney-Regular.ttf")
        match, diff, hash, other_hash = font_a.get_fingerprint_match(
            other=font_b, tolerance=10
        )
        self.assertFalse(match)

    def test_get_fingerprint_match_with_other_font_filepath(self):
        font_a = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font_b = self._get_font_path("/Tourney/static/Tourney/Tourney-Regular.ttf")
        match, diff, hash, other_hash = font_a.get_fingerprint_match(
            other=font_b, tolerance=10
        )
        self.assertFalse(match)

    def test_get_fingerprint_match_with_other_font_invalid(self):
        font_a = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font_b = None
        with self.assertRaises(ValueError):
            font_a.get_fingerprint_match(other=font_b, tolerance=10)

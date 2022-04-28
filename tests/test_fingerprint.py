# -*- coding: utf-8 -*-

from fontbro import Font
from imagehash import hex_to_hash

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

    def test_get_fingerprint(self):
        font = self._get_variable_font()
        hash = font.get_fingerprint()
        hash_hex = "0000000000000000000010000002000000011800ac3318012d335ac1554f58c4554f58c6acb368017968d4dc512c852b512e4b21b1275aaa916870ced8c9252a90c94cabb524276a5565a764d0e946b2c1ed4eba6d09ab622a38c8c48b250611cb6506396da8898d2d6899c4004031102048391c004019180000191800003918"
        diff = hash - hex_to_hash(hash_hex)
        self.assertEqual(diff, 0)

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
                    instance_font = Font(font._filepath)
                    instance_font.to_static(coordinates=instance["coordinates"])
                    instance_hash = instance_font.get_fingerprint()
                    if len(hashes):
                        diff_from_prev_instance = instance_hash - hashes[-1]
                        # print(diff_from_prev_instance)
                        self.assertTrue(diff_from_prev_instance > 10)
                    hashes.append(instance_hash)

    def test_get_fingerprint_diff_against_all_variable_instances(self):
        fonts = [
            {
                "variable": self._get_font(
                    "/Tourney/Tourney-VariableFont_wdth,wght.ttf",
                ),
                "static": self._get_font(
                    "/Tourney/static/Tourney/Tourney-Regular.ttf",
                ),
            },
            {
                "variable": self._get_font(
                    "/Roboto_Mono/RobotoMono-VariableFont_wght.ttf",
                ),
                "static": self._get_font(
                    "/Roboto_Mono/static/RobotoMono-Regular.ttf",
                ),
            },
        ]
        for font in fonts:
            # print(font.get_variable_instances())
            with self.subTest(f"Test with font: {font}", font=font):
                variable_font = font["variable"]
                static_font = font["static"]
                static_font_hash = static_font.get_fingerprint()
                diffs = []
                for instance in variable_font.get_variable_instances():
                    instance_font = Font(variable_font._filepath)
                    instance_font.to_static(coordinates=instance["coordinates"])
                    instance_hash = instance_font.get_fingerprint()
                    diffs.append(instance_hash - static_font_hash)
                diffs = [diff for diff in diffs if diff < 5]
                self.assertTrue(len(diffs), 1)

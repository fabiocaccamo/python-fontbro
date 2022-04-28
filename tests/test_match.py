# -*- coding: utf-8 -*-

from tests import AbstractTestCase


class MatchTestCase(AbstractTestCase):
    """
    This class describes a match test case.
    """

    def test_match_with_same_static_fonts(self):
        font_a = self._get_font("/Tourney/static/Tourney/Tourney-Regular.ttf")
        font_b = self._get_font("/Tourney/static/Tourney/Tourney-Regular.ttf")
        self.assertTrue(font_a.match(other=font_b, tolerance=1))

    def test_match_with_different_static_fonts(self):
        font_a = self._get_font("/Tourney/static/Tourney/Tourney-Medium.ttf")
        font_b = self._get_font("/Tourney/static/Tourney/Tourney-Regular.ttf")
        self.assertFalse(font_a.match(other=font_b, tolerance=10))

    def test_match_with_same_variable_fonts(self):
        font_a = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font_b = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        self.assertTrue(font_a.match(other=font_b, tolerance=1))

    def test_match_with_different_variable_fonts(self):
        font_a = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font_b = self._get_font("/Tourney/Tourney-Italic-VariableFont_wdth,wght.ttf")
        self.assertFalse(font_a.match(other=font_b, tolerance=10))

    def test_match_with_variable_and_static_fonts(self):
        font_a = self._get_font("/Tourney/Tourney-VariableFont_wdth,wght.ttf")
        font_b = self._get_font("/Tourney/static/Tourney/Tourney-Regular.ttf")
        self.assertFalse(font_a.match(other=font_b, tolerance=10))

from tests import AbstractTestCase


class GlyphsTestCase(AbstractTestCase):
    """
    Test case for the methods related to the font glyphs.
    """

    def test_get_glyphs(self):
        with self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf") as font:
            glyphs = list(font.get_glyphs())
            self.assertEqual(
                glyphs[2],
                {"name": "A", "components_names": []},
            )
            self.assertEqual(
                glyphs[97],
                {"name": "colon", "components_names": ["period", "period"]},
            )
            self.assertEqual(len(glyphs), 999)

    def test_get_glyphs_with_cff_outlines(self):
        # regression: CFF fonts have no glyf table (and no components)
        with self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf") as font:
            glyphs = list(font.get_glyphs())
            self.assertEqual(len(glyphs), font.get_glyphs_count())
            self.assertEqual(glyphs[0], {"name": ".notdef", "components_names": []})
            self.assertTrue(all(glyph["components_names"] == [] for glyph in glyphs))

    def test_get_glyphs_count(self):
        with self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf") as font:
            glyphs_count = font.get_glyphs_count()
            self.assertEqual(glyphs_count, 999)
            characters_count = font.get_characters_count()
            self.assertTrue(glyphs_count > characters_count)

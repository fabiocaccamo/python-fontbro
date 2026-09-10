from fontTools.pens.filterPen import FilterPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

from fontbro.pixel import (
    _CHARACTERS,
    _get_glyphs_segments,
    _is_orthogonal,
    is_pixel,
)
from tests import AbstractTestCase

PIXEL_FONT_PATH = "/Silkscreen/Silkscreen-Regular.ttf"


class DegenerateCurvesPen(FilterPen):
    """
    Pen that draws straight segments as degenerate quadratic curves,
    with the off-curve point in the middle of the segment.
    """

    def moveTo(self, pt):
        self._current = pt
        self._outPen.moveTo(pt)

    def lineTo(self, pt):
        (x0, y0), (x1, y1) = self._current, pt
        self._outPen.qCurveTo(((x0 + x1) / 2, (y0 + y1) / 2), pt)
        self._current = pt


class PixelTestCase(AbstractTestCase):
    """
    Test case for the methods related to the pixel fonts detection.
    """

    def _transform_characters_glyphs(self, font, transform):
        # transforms the (simple) glyphs of A-Z, a-z and 0-9 outlines in-memory
        ttfont = font.get_ttfont()
        cmap = ttfont.getBestCmap()
        glyf = ttfont["glyf"]
        for char in _CHARACTERS:
            glyph = glyf[cmap[ord(char)]]
            if glyph.numberOfContours > 0:
                coordinates = glyph.coordinates
                for index, (x, y) in enumerate(coordinates):
                    coordinates[index] = transform(x, y)

    def _remove_characters_from_cmap(self, font):
        for table in font.get_ttfont()["cmap"].tables:
            for char in _CHARACTERS:
                table.cmap.pop(ord(char), None)

    def test_is_pixel(self):
        with self._get_font(PIXEL_FONT_PATH) as font:
            self.assertTrue(font.is_pixel())
            self.assertTrue(font.is_pixel(threshold=0.95))

    def test_is_pixel_with_imperfect_pixel_fonts(self):
        # regression: real pixel fonts with systematic off-grid deviations
        # (about 15-24% of the pixel size), detected thanks to the grid tolerance
        fonts_paths = [
            "/DotGothic16/DotGothic16-Regular.ttf",
            "/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf",
        ]
        for font_path in fonts_paths:
            with self.subTest(font_path=font_path):
                with self._get_font(font_path) as font:
                    self.assertTrue(font.is_pixel())

    def test_is_pixel_with_non_pixel_fonts(self):
        fonts_paths = [
            "/Honk/static/Honk-Regular.ttf",
            "/Inter/static/Inter-Regular.ttf",
            "/Nabla/static/Nabla-Regular.ttf",
            "/Noto_Sans_TC/NotoSansTC-Regular.otf",
            "/Open_Sans/static/OpenSans-Regular.ttf",
            "/Roboto_Mono/static/RobotoMono-Regular.ttf",
            "/Tourney/static/Tourney/Tourney-Regular.ttf",
        ]
        for font_path in fonts_paths:
            with self.subTest(font_path=font_path):
                with self._get_font(font_path) as font:
                    self.assertFalse(font.is_pixel())

    def test_is_pixel_with_rectangular_pixels(self):
        # pixels can be rectangular, eg. fonts that mimic old terminals
        transforms = {
            "wide": lambda x, y: (x * 1.37, y),
            "tall": lambda x, y: (x, y * 1.5),
        }
        for label, transform in transforms.items():
            with self.subTest(pixels=label):
                with self._get_font(PIXEL_FONT_PATH) as font:
                    self._transform_characters_glyphs(font, transform)
                    self.assertTrue(font.is_pixel())

    def test_is_pixel_with_strokes_multiple_of_pixel(self):
        # regression: the most common segments length can be a multiple of the
        # pixel size, eg. when strokes are always at least 2 pixels long:
        # x is doubled and shifted by 1 pixel after a column, so most horizontal
        # lengths are 2 pixels (250), but some are odd multiples of 1 pixel (125)
        def transform(x, y):
            return (x * 2 + (125 if x >= 250 else 0), y)

        with self._get_font(PIXEL_FONT_PATH) as font:
            self._transform_characters_glyphs(font, transform)
            self.assertTrue(font.is_pixel())

    def test_is_pixel_with_degenerate_curves(self):
        # regression: degenerate curves (straight segments drawn as curves,
        # eg. in variable fonts for interpolation compatibility) are segments
        with self._get_font(PIXEL_FONT_PATH) as font:
            ttfont = font.get_ttfont()
            glyphset = ttfont.getGlyphSet()
            cmap = ttfont.getBestCmap()
            glyf = ttfont["glyf"]
            for char in _CHARACTERS:
                glyph_name = cmap[ord(char)]
                pen = TTGlyphPen(glyphset)
                glyphset[glyph_name].draw(DegenerateCurvesPen(pen))
                glyf[glyph_name] = pen.glyph()
            self.assertTrue(font.is_pixel())

    def test_is_pixel_with_squared_font(self):
        # outlines with horizontal and vertical segments only (1st check passes),
        # but with irregular widths not aligned to a pixel grid (2nd check fails),
        # like "techno" fonts: each grid column is shifted by an irregular offset
        # (smaller than the pixel), x is transformed independently from y,
        # so horizontal and vertical segments stay orthogonal
        def transform(x, y):
            return (x + (round(x / 125) * 37) % 61, y)

        with self._get_font(PIXEL_FONT_PATH) as font:
            self._transform_characters_glyphs(font, transform)
            glyphs_segments = _get_glyphs_segments(font.get_ttfont())
            self.assertTrue(
                all(_is_orthogonal(segments) for segments in glyphs_segments)
            )
            self.assertFalse(font.is_pixel())

    def test_is_pixel_with_implausible_grid(self):
        # a pixel grid with less than 4 or more than 64 pixels per em
        # is not plausible, both for the pixel width and height
        transforms = {
            "width too coarse (2 px/em)": lambda x, y: (x * 4, y),
            "height too coarse (2 px/em)": lambda x, y: (x, y * 4),
            "width too fine (80 px/em)": lambda x, y: (x * 0.1, y),
            "height too fine (80 px/em)": lambda x, y: (x, y * 0.1),
        }
        for label, transform in transforms.items():
            with self.subTest(pixel=label):
                with self._get_font(PIXEL_FONT_PATH) as font:
                    self._transform_characters_glyphs(font, transform)
                    self.assertFalse(font.is_pixel())

    def test_is_pixel_without_characters(self):
        # fonts without A-Z, a-z and 0-9 are checked on the first 50 glyphs
        # (by codepoint) that are not punctuation
        with self._get_font(PIXEL_FONT_PATH) as font:
            self._remove_characters_from_cmap(font)
            self.assertTrue(font.is_pixel())
        with self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf") as font:
            self._remove_characters_from_cmap(font)
            self.assertFalse(font.is_pixel())

    def test_is_pixel_with_malformed_cmap(self):
        # regression: malformed cmaps must not raise (ValueError / KeyError)
        with self._get_font(PIXEL_FONT_PATH) as font:
            self._remove_characters_from_cmap(font)
            for table in font.get_ttfont()["cmap"].tables:
                # codepoint out of the unicode range and missing glyph
                table.cmap[0x110000] = "A"
                table.cmap[0x00C0] = "glyph99999"
            self.assertTrue(font.is_pixel())
        with self._get_font(PIXEL_FONT_PATH) as font:
            for table in font.get_ttfont()["cmap"].tables:
                table.cmap[ord("A")] = "glyph99999"
            self.assertTrue(font.is_pixel())

    def test_is_pixel_module_with_ttfont(self):
        # the module functions work directly on a fontTools TTFont
        ttfont = TTFont(self._get_font_path(PIXEL_FONT_PATH))
        self.assertTrue(is_pixel(ttfont))
        self.assertTrue(is_pixel(ttfont, threshold=0.95))

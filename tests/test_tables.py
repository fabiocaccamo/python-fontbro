from fontTools.ttLib import TTFont, newTable

from fontbro import Font
from fontbro.tables import get_tables, get_tables_tags
from tests import AbstractTestCase


class TablesTestCase(AbstractTestCase):
    """
    Test case for the methods related to font tables.
    """

    def test_get_tables_tags(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        tables = font.get_tables_tags()
        self.assertIsInstance(tables, list)
        self.assertIn("cmap", tables)
        self.assertIn("head", tables)
        self.assertIn("OS/2", tables)
        # "GlyphOrder" is a fontTools bookkeeping entry, not a real font table
        self.assertNotIn("GlyphOrder", tables)

    def test_get_tables(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        tables = font.get_tables()
        self.assertIsInstance(tables, list)
        self.assertTrue(tables)

        tags = [table["tag"] for table in tables]
        self.assertNotIn("GlyphOrder", tags)
        self.assertEqual(len(tags), len(set(tags)))
        self.assertEqual(tags, font.get_tables_tags())

        for table in tables:
            self.assertIsInstance(table, dict)
            self.assertIsInstance(table["tag"], str)
            self.assertIsInstance(table["name"], str)
            self.assertIsInstance(table["length"], int)
            self.assertIsInstance(table["offset"], int)

        names_by_tag = {table["tag"]: table["name"] for table in tables}
        self.assertEqual(names_by_tag["head"], "Header")
        self.assertEqual(names_by_tag["cmap"], "Character Map")
        # regression: required tables must have a proper name
        self.assertEqual(names_by_tag["hmtx"], "Horizontal Metrics")
        self.assertEqual(names_by_tag["prep"], "Control Value Program")

    def test_get_tables_with_in_memory_table(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.get_ttfont()["zzzz"] = newTable("zzzz")
        tables = {table["tag"]: table for table in font.get_tables()}
        # unknown tables fallback to their tag as name and, since they have
        # not been saved yet, they have no length and offset
        self.assertEqual(
            tables["zzzz"],
            {"tag": "zzzz", "name": "zzzz", "length": None, "offset": None},
        )

    def _get_font_with_extra_tables(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        ttfont = font.get_ttfont()
        # "morx" is an apple table, the others are unknown (tools and custom)
        for tag in ("morx", "TSI0", "FFTM", "zzzz"):
            ttfont[tag] = newTable(tag)
        return font

    def test_get_tables_tags_include_unknown(self):
        font = self._get_font_with_extra_tables()
        font_tags = self._get_font(
            "/Roboto_Mono/static/RobotoMono-Regular.ttf"
        ).get_tables_tags()

        # unknown tables are included by default
        tags = font.get_tables_tags()
        self.assertEqual(tags, font.get_tables_tags(include_unknown=True))
        self.assertEqual(set(tags), {*font_tags, "morx", "TSI0", "FFTM", "zzzz"})

        known_tags = font.get_tables_tags(include_unknown=False)
        self.assertEqual(set(known_tags), {*font_tags, "morx"})
        # filtering preserves the tables order
        self.assertEqual(known_tags, [tag for tag in tags if tag in known_tags])

        # "GlyphOrder" is never included, it's not a real font table
        self.assertNotIn("GlyphOrder", tags)
        self.assertNotIn("GlyphOrder", known_tags)

    def test_get_tables_include_unknown(self):
        font = self._get_font_with_extra_tables()

        # unknown tables are included by default
        tables = {table["tag"]: table for table in font.get_tables()}
        self.assertEqual(tables["TSI0"]["name"], "TSI0")
        self.assertEqual(tables["morx"]["name"], "Extended Glyph Metamorphosis")

        known_tables = font.get_tables(include_unknown=False)
        self.assertEqual(
            [table["tag"] for table in known_tables],
            font.get_tables_tags(include_unknown=False),
        )
        self.assertNotIn("TSI0", [table["tag"] for table in known_tables])

    def test_tables_module_with_ttfont(self):
        # the module functions work directly on a fontTools TTFont
        ttfont = TTFont(
            self._get_font_path("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        )
        ttfont["TSI0"] = newTable("TSI0")

        tags = get_tables_tags(ttfont)
        self.assertNotIn("GlyphOrder", tags)
        self.assertIn("TSI0", tags)
        self.assertNotIn("TSI0", get_tables_tags(ttfont, include_unknown=False))

        tables = {table["tag"]: table for table in get_tables(ttfont)}
        self.assertEqual(tables["head"]["name"], "Header")
        self.assertEqual(tables["head"]["length"], 54)
        self.assertIsInstance(tables["head"]["offset"], int)
        self.assertEqual(
            [table["tag"] for table in get_tables(ttfont, include_unknown=False)],
            get_tables_tags(ttfont, include_unknown=False),
        )

    def test_get_tables_with_woff(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        lengths_by_tag = {table["tag"]: table["length"] for table in font.get_tables()}
        font_saved_filepath = font.save_as_woff(self._get_font_temp_path(""))
        tables = Font(font_saved_filepath).get_tables()
        self.assertEqual([table["tag"] for table in tables], list(lengths_by_tag))
        for table in tables:
            with self.subTest(tag=table["tag"]):
                # regression: length must be the uncompressed table length
                self.assertEqual(table["length"], lengths_by_tag[table["tag"]])
                self.assertIsInstance(table["offset"], int)

    def test_get_tables_with_woff2(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        lengths_by_tag = {table["tag"]: table["length"] for table in font.get_tables()}
        font_saved_filepath = font.save_as_woff2(self._get_font_temp_path(""))
        tables = Font(font_saved_filepath).get_tables()
        self.assertEqual([table["tag"] for table in tables], list(lengths_by_tag))
        # these tables are reconstructed when decoding, so their length may change
        transformed_tags = {"glyf", "loca", "hmtx"}
        for table in tables:
            with self.subTest(tag=table["tag"]):
                self.assertIsInstance(table["length"], int)
                if table["tag"] not in transformed_tags:
                    self.assertEqual(table["length"], lengths_by_tag[table["tag"]])
                # regression: woff2 tables have no individual offset in the file
                self.assertIsNone(table["offset"])

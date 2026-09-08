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

    def test_get_tables(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        tables = font.get_tables()
        self.assertIsInstance(tables, list)
        self.assertTrue(tables)
        first = tables[0]
        self.assertIsInstance(first, dict)
        self.assertIn("tag", first)
        self.assertIn("name", first)
        self.assertIn("length", first)
        self.assertIn("offset", first)
        self.assertIn(first["tag"], [table["tag"] for table in tables])
        self.assertIn(first["name"], [table["name"] for table in tables])

        head = next(table for table in tables if table["tag"] == "head")
        self.assertIsInstance(head["tag"], str)
        self.assertEqual(head["name"], "Header")
        self.assertIsInstance(head["length"], int)
        self.assertIsInstance(head["offset"], int)

        cmap = next(table for table in tables if table["tag"] == "cmap")
        self.assertEqual(cmap["name"], "Character Map")

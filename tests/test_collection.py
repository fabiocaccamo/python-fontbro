from fontbro import Font
from tests import AbstractTestCase


class CollectionTestCase(AbstractTestCase):
    """
    Test case for the methods related to font collections.
    """

    def test_from_collection(self):
        filepath = self._get_font_path("/issues/issue-0049/cambria.ttc")
        fonts = Font.from_collection(filepath=filepath)
        names = [font.get_name("full_name") for font in fonts]
        self.assertEqual(names, ["Cambria", "Cambria Math"])
        for font in fonts:
            font.close()

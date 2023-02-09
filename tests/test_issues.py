from tests import AbstractTestCase


class IssuesTestCase(AbstractTestCase):
    """
    Test case for GitHub issues.
    """

    def test_issue_0048_get_characters_count(self):
        font = self._get_font("/issues/issue-0048/test.ttf")
        with self.assertRaises(TypeError):
            font.get_characters_count()

    def test_issue_0050_get_features(self):
        font = self._get_font("/issues/issue-0050/LeagueGothic-Regular.otf")
        features = font.get_features_tags()
        self.assertEqual(features, ["kern"])

    def test_issue_0051_get_characters_count(self):
        font = self._get_font("/issues/issue-0051/ANASTCN.ttf")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 212)

    def test_issue_0052_get_characters_count(self):
        font = self._get_font("/issues/issue-0052/Bobbiefreebie.ttf")
        chars_count = font.get_characters_count()
        self.assertEqual(chars_count, 288)

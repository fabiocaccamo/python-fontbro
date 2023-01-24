from fontbro import Font
from tests import AbstractTestCase


class IssuesTestCase(AbstractTestCase):
    """
    Test case for GitHub issues.
    """

    def test_issue_0048_get_characters_count(self):
        font = self._get_font("/issues/issue-0048/test.ttf")
        with self.assertRaises(TypeError):
            font.get_characters_count()

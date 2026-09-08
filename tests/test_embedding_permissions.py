from tests import AbstractTestCase


class EmbeddingPermissionsTestCase(AbstractTestCase):
    """
    Test case for the methods related to the font embedding permissions.
    """

    def test_get_embedding_permissions(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        expected_permissions = {
            "installable": False,
            "restricted": False,
            "preview_and_print": False,
            "editable": False,
            "no_subsetting": False,
            "no_layout": False,
        }
        self.assertEqual(font.get_embedding_permissions(), expected_permissions)

    def test_set_embedding_permissions(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        font.set_embedding_permissions(
            installable=True,
            restricted=True,
            preview_and_print=True,
            editable=True,
            no_subsetting=True,
            no_layout=True,
        )
        expected_permissions = {
            "installable": True,
            "restricted": True,
            "preview_and_print": True,
            "editable": True,
            "no_subsetting": True,
            "no_layout": True,
        }
        self.assertEqual(font.get_embedding_permissions(), expected_permissions)

        font.set_embedding_permissions(
            installable=False,
            restricted=False,
            preview_and_print=False,
            editable=False,
            no_subsetting=False,
            no_layout=False,
        )
        self.assertEqual(
            font.get_embedding_permissions(),
            {
                "installable": False,
                "restricted": False,
                "preview_and_print": False,
                "editable": False,
                "no_subsetting": False,
                "no_layout": False,
            },
        )

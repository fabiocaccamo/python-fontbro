from fontbro import Font, embedding_permissions
from fontbro.embedding_permissions import _USAGE_PERMISSIONS_KEYS
from fontbro.exceptions import ArgumentError, OperationError
from tests import AbstractTestCase

FONT_PATH = "/Roboto_Mono/static/RobotoMono-Regular.ttf"

INSTALLABLE_PERMISSIONS = {
    "installable": True,
    "restricted": False,
    "preview_and_print": False,
    "editable": False,
    "no_subsetting": False,
    "bitmap_embedding_only": False,
}


class EmbeddingPermissionsTestCase(AbstractTestCase):
    """
    Test case for the methods related to the font embedding permissions.
    """

    def _get_font_with_fs_type(self, fs_type=None):
        font = self._get_font(FONT_PATH)
        if fs_type is not None:
            font.get_ttfont()["OS/2"].fsType = fs_type
        return font

    def _get_fs_type(self, font):
        return font.get_ttfont()["OS/2"].fsType

    def test_get_embedding_permissions_default(self):
        # a fresh font with fsType == 0 is installable (no restriction bit set)
        font = self._get_font_with_fs_type()
        self.assertEqual(self._get_fs_type(font), 0)
        self.assertEqual(font.get_embedding_permissions(), INSTALLABLE_PERMISSIONS)

    def test_get_embedding_permissions_without_os2_table(self):
        font = self._get_font_with_fs_type()
        del font.get_ttfont()["OS/2"]
        # a font without an OS/2 table has no embedding restrictions
        self.assertEqual(font.get_embedding_permissions(), INSTALLABLE_PERMISSIONS)

    def test_get_embedding_permissions_reads_real_fstype_bits(self):
        # bits taken directly from the OpenType OS/2 fsType specification:
        # https://learn.microsoft.com/en-us/typography/opentype/spec/os2#fstype
        expected_keys_by_fs_type = {
            0x0002: "restricted",  # bit 1, restricted license embedding
            0x0004: "preview_and_print",  # bit 2, preview and print embedding
            0x0008: "editable",  # bit 3, editable embedding
            0x0100: "no_subsetting",  # bit 8, no subsetting
            0x0200: "bitmap_embedding_only",  # bit 9, bitmap embedding only
        }
        for fs_type, expected_key in expected_keys_by_fs_type.items():
            with self.subTest(fs_type=hex(fs_type)):
                font = self._get_font_with_fs_type(fs_type)
                permissions = font.get_embedding_permissions()
                enabled_keys = [key for key, value in permissions.items() if value]
                if expected_key in _USAGE_PERMISSIONS_KEYS:
                    self.assertEqual(enabled_keys, [expected_key])
                else:
                    # independent flags don't affect the usage permissions
                    self.assertEqual(enabled_keys, ["installable", expected_key])

    def test_get_embedding_permissions_ignores_reserved_bit(self):
        # bit 0 is reserved, it must not make the font non-installable
        font = self._get_font_with_fs_type(0x0001)
        self.assertEqual(font.get_embedding_permissions(), INSTALLABLE_PERMISSIONS)

    def test_set_embedding_permissions_restricted(self):
        font = self._get_font_with_fs_type()
        font.set_embedding_permissions(restricted=True)
        self.assertEqual(self._get_fs_type(font), 0x0002)
        self.assertEqual(
            font.get_embedding_permissions(),
            {
                **INSTALLABLE_PERMISSIONS,
                "installable": False,
                "restricted": True,
            },
        )

    def test_set_embedding_permissions_replaces_current_usage_permission(self):
        # regression: setting a usage permission must clear the other ones,
        # otherwise an invalid fsType with multiple usage bits set is written
        usage_bits = {
            "restricted": 0x0002,
            "preview_and_print": 0x0004,
            "editable": 0x0008,
        }
        for from_key, from_bits in usage_bits.items():
            for to_key, to_bits in usage_bits.items():
                with self.subTest(from_key=from_key, to_key=to_key):
                    # independent flags must be preserved
                    font = self._get_font_with_fs_type(from_bits | 0x0100)
                    font.set_embedding_permissions(**{to_key: True})
                    self.assertEqual(self._get_fs_type(font), to_bits | 0x0100)

    def test_set_embedding_permissions_repairs_multiple_usage_bits(self):
        # legacy fonts may have multiple usage bits set, setting one normalizes it
        font = self._get_font_with_fs_type(0x000E)
        font.set_embedding_permissions(preview_and_print=True)
        self.assertEqual(self._get_fs_type(font), 0x0004)

    def test_set_embedding_permissions_installable_clears_usage_permissions(self):
        font = self._get_font_with_fs_type(0x0008 | 0x0200)
        font.set_embedding_permissions(installable=True)
        self.assertEqual(self._get_fs_type(font), 0x0200)
        self.assertTrue(font.get_embedding_permissions()["installable"])

    def test_set_embedding_permissions_disable_current_usage_permission(self):
        font = self._get_font_with_fs_type(0x0004)
        font.set_embedding_permissions(preview_and_print=False)
        self.assertEqual(self._get_fs_type(font), 0x0000)
        self.assertTrue(font.get_embedding_permissions()["installable"])

    def test_set_embedding_permissions_disable_other_usage_permission(self):
        # setting to False a usage permission not in effect changes nothing
        font = self._get_font_with_fs_type(0x0004)
        font.set_embedding_permissions(restricted=False, editable=False)
        self.assertEqual(self._get_fs_type(font), 0x0004)

    def test_set_embedding_permissions_installable_false_with_restriction(self):
        # installable is already False, the current restriction is preserved
        font = self._get_font_with_fs_type(0x0002)
        font.set_embedding_permissions(installable=False)
        self.assertEqual(self._get_fs_type(font), 0x0002)
        font.set_embedding_permissions(installable=False, editable=True)
        self.assertEqual(self._get_fs_type(font), 0x0008)

    def test_set_embedding_permissions_installable_false_without_restriction(self):
        # regression: installable=False must not be silently ignored
        font = self._get_font_with_fs_type()
        with self.assertRaises(ArgumentError):
            font.set_embedding_permissions(installable=False)
        self.assertEqual(self._get_fs_type(font), 0x0000)

    def test_set_embedding_permissions_all_usage_permissions_false(self):
        # regression: all usage permissions False is an impossible state,
        # it must not make the font installable
        font = self._get_font_with_fs_type(0x0008)
        with self.assertRaises(ArgumentError):
            font.set_embedding_permissions(
                installable=False,
                restricted=False,
                preview_and_print=False,
                editable=False,
            )
        self.assertEqual(self._get_fs_type(font), 0x0008)

    def test_set_embedding_permissions_independent_flags(self):
        font = self._get_font_with_fs_type()
        font.set_embedding_permissions(
            no_subsetting=True,
            bitmap_embedding_only=True,
        )
        self.assertEqual(self._get_fs_type(font), 0x0300)
        permissions = font.get_embedding_permissions()
        self.assertTrue(permissions["no_subsetting"])
        self.assertTrue(permissions["bitmap_embedding_only"])
        # independent flags don't affect the mutually exclusive usage permissions
        self.assertTrue(permissions["installable"])

        font.set_embedding_permissions(no_subsetting=False, bitmap_embedding_only=False)
        self.assertEqual(self._get_fs_type(font), 0x0000)

    def test_set_embedding_permissions_independent_flags_preserve_usage(self):
        font = self._get_font_with_fs_type(0x0002)
        font.set_embedding_permissions(no_subsetting=True)
        self.assertEqual(self._get_fs_type(font), 0x0102)

    def test_set_embedding_permissions_none_values_are_ignored(self):
        font = self._get_font_with_fs_type(0x0104)
        font.set_embedding_permissions()
        self.assertEqual(self._get_fs_type(font), 0x0104)

    def test_set_embedding_permissions_conflicting_usage_permissions(self):
        font = self._get_font_with_fs_type(0x0200)
        with self.assertRaises(ArgumentError):
            font.set_embedding_permissions(restricted=True, editable=True)
        with self.assertRaises(ArgumentError):
            font.set_embedding_permissions(installable=True, preview_and_print=True)
        # the fsType field is left untouched
        self.assertEqual(self._get_fs_type(font), 0x0200)

    def test_set_embedding_permissions_invalid_value_type(self):
        # regression: invalid values must raise before writing anything,
        # and must not rely on assert (stripped with python -O)
        invalid_kwargs = [
            {"restricted": True, "no_subsetting": "yes"},
            {"editable": True, "bitmap_embedding_only": 1},
            {"installable": 0},
            {"preview_and_print": "true"},
        ]
        for kwargs in invalid_kwargs:
            with self.subTest(kwargs=kwargs):
                font = self._get_font_with_fs_type(0x0008)
                with self.assertRaises(ArgumentError):
                    font.set_embedding_permissions(**kwargs)
                self.assertEqual(self._get_fs_type(font), 0x0008)

    def test_set_embedding_permissions_without_os2_table(self):
        font = self._get_font_with_fs_type()
        del font.get_ttfont()["OS/2"]
        with self.assertRaises(OperationError):
            font.set_embedding_permissions(editable=True)

    def test_set_embedding_permissions_roundtrip(self):
        font = self._get_font_with_fs_type()
        font.set_embedding_permissions(editable=True, no_subsetting=True)
        font_saved_filepath = font.save(self._get_font_temp_path(""))
        font_saved = Font(font_saved_filepath)
        self.assertEqual(self._get_fs_type(font_saved), 0x0108)

    def test_embedding_permissions_module_with_ttfont(self):
        # the module functions work directly on a fontTools TTFont
        ttfont = self._get_font_with_fs_type().get_ttfont()
        embedding_permissions.set_embedding_permissions(ttfont, restricted=True)
        self.assertEqual(ttfont["OS/2"].fsType, 0x0002)
        self.assertEqual(
            embedding_permissions.get_embedding_permissions(ttfont),
            {
                **INSTALLABLE_PERMISSIONS,
                "installable": False,
                "restricted": True,
            },
        )

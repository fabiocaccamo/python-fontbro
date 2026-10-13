import json
import tempfile
import unittest

import fsutil

from fontbro import Font


class AbstractTestCase(unittest.TestCase):
    """
    This class describes the abstract test case
    with some methods that are used by different test cases.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def setUp(self):
        # each test has its own temp directory, so tests can run in parallel
        # (eg. tox -p) without deleting or overwriting each other's files
        self._temp_dirpath = tempfile.mkdtemp(prefix="fontbro-tests-")

    def tearDown(self):
        fsutil.remove_dir(self._temp_dirpath)

    def _get_font_temp_path(self, filepath=""):
        return fsutil.join_path(self._temp_dirpath, filepath)

    def _get_font_temp_copy_path(self, filepath):
        """
        Copies the font at filepath to the temp directory and returns the copy path,
        to test operations that overwrite the font file without modifying it.
        """
        font_copy_path = self._get_font_temp_path(fsutil.get_filename(filepath))
        fsutil.copy_file(self._get_font_path(filepath), font_copy_path)
        return font_copy_path

    @classmethod
    def _get_font_path(cls, filepath):
        return fsutil.join_path(__file__, f"fonts/{filepath}")

    @classmethod
    def _get_font(cls, filepath):
        filepath = cls._get_font_path(filepath)
        font = Font(filepath=filepath)
        return font

    @staticmethod
    def _print(obj):
        print(json.dumps(obj, indent=4, sort_keys=True))

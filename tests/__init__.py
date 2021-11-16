# -*- coding: utf-8 -*-

from fontbro import Font

import fsutil
import json
import unittest


class AbstractTestCase(unittest.TestCase):
    """
    This class describes the abstract test case
    with some methods that are used by different test cases.
    """
    def setUp(self):
        fsutil.remove_dir(self._get_font_temp_path())

    def tearDown(self):
        fsutil.remove_dir(self._get_font_temp_path())

    @classmethod
    def _get_font_temp_path(cls, filepath=''):
        return fsutil.join_path(__file__, 'temp/{}'.format(filepath))

    @classmethod
    def _get_font_path(cls, filepath):
        return fsutil.join_path(__file__, 'fonts/{}'.format(filepath))

    @classmethod
    def _get_font(cls, filepath):
        filepath = cls._get_font_path(filepath)
        font = Font(filepath=filepath)
        return font

    @staticmethod
    def _print(obj):
        print(json.dumps(obj, indent=4, sort_keys=True))

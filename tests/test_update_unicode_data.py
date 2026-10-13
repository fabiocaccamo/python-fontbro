import fsutil

from scripts.update_data import update_unicode_data
from tests import AbstractTestCase


class UpdateUnicodeDataTestCase(AbstractTestCase):
    """
    Test case for updating the pre-computed unicode data.
    """

    def test_update_unicode_data(self):
        # the data files are written to the temp directory,
        # the package data files are not modified
        dirpath = self._get_font_temp_path()
        update_unicode_data(dirpath=dirpath)
        for filename in ("unicode-blocks.json", "unicode-scripts.json"):
            data = fsutil.read_file_json(fsutil.join_path(dirpath, filename))
            self.assertTrue(len(data) > 0)
            self.assertTrue(all(item["characters_total"] > 0 for item in data))

import subprocess

from scripts.update_data import update_unicode_data
from tests import AbstractTestCase


class UpdateUnicodeDataTestCase(AbstractTestCase):
    """
    Test case for updating the pre-computed unicode data.
    """

    def test_update_unicode_data(self):
        update_unicode_data()

    def test_update_unicode_data_from_cli(self):
        output = (
            subprocess.check_output("python scripts/update_data.py", shell=True)
            .decode("utf-8")
            .strip()
        )
        expected_output = ""
        self.assertEqual(output, expected_output)

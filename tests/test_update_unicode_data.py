from scripts.update_data import update_unicode_data
from tests import AbstractTestCase


class UpdateUnicodeDataTestCase(AbstractTestCase):
    """
    Test case for updating the pre-computed unicode data.
    """

    def test_update_unicode_data(self):
        update_unicode_data()

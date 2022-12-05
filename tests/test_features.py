from tests import AbstractTestCase


class FeaturesTestCase(AbstractTestCase):
    """
    Test case for the methods related to the font features.
    """

    def test_get_features(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        features = font.get_features()
        self.assertEqual(
            features,
            [
                {
                    "tag": "smcp",
                    "name": "Small Capitals",
                    "exposed": True,
                    "exposed_active": False,
                }
            ],
        )

    def test_get_features_tags(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        features = font.get_features_tags()
        self.assertEqual(features, ["smcp"])

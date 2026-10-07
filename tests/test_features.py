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
                    "params": {
                        "name": None,
                        "tooltip": None,
                        "sample_text": None,
                        "labels": [],
                        "characters": [],
                    },
                }
            ],
        )

    def test_get_features_with_params(self):
        font = self._get_font("/Inter/static/Inter-Regular.ttf")
        features = font.get_features()
        features_by_tag = {feature["tag"]: feature for feature in features}
        self.assertEqual(
            features_by_tag["cv11"],
            {
                "tag": "cv11",
                "name": "Character Variant 11",
                "exposed": True,
                "exposed_active": False,
                "params": {
                    "name": "Single-storey a",
                    "tooltip": None,
                    "sample_text": None,
                    "labels": [],
                    "characters": [],
                },
            },
        )
        self.assertEqual(
            features_by_tag["ss01"],
            {
                "tag": "ss01",
                "name": "Stylistic Set 1",
                "exposed": True,
                "exposed_active": False,
                "params": {
                    "name": "Open digits",
                    "tooltip": None,
                    "sample_text": None,
                    "labels": [],
                    "characters": [],
                },
            },
        )
        self.assertEqual(
            features_by_tag["salt"]["params"],
            {
                "name": None,
                "tooltip": None,
                "sample_text": None,
                "labels": [],
                "characters": [],
            },
        )

    def test_get_features_with_character_variants_params(self):
        from fontTools.ttLib.tables import otTables

        font = self._get_font("/Inter/static/Inter-Regular.ttf")
        ttfont = font.get_ttfont()
        name_table = ttfont["name"]
        feature_params = otTables.FeatureParamsCharacterVariants()
        feature_params.Format = 0
        feature_params.FeatUILabelNameID = name_table.addName("Alternate a")
        feature_params.FeatUITooltipTextNameID = name_table.addName(
            "Alternate a tooltip"
        )
        feature_params.SampleTextNameID = name_table.addName("aaa")
        feature_params.NumNamedParameters = 2
        feature_params.FirstParamUILabelNameID = name_table.addName("Single-storey")
        name_table.addName("Double-storey")
        feature_params.CharCount = 2
        feature_params.Character = [0x61, 0xE0]
        for feature_record in ttfont["GSUB"].table.FeatureList.FeatureRecord:
            if feature_record.FeatureTag == "cv11":
                feature_record.Feature.FeatureParams = feature_params
        features = font.get_features()
        features_by_tag = {feature["tag"]: feature for feature in features}
        self.assertEqual(
            features_by_tag["cv11"]["params"],
            {
                "name": "Alternate a",
                "tooltip": "Alternate a tooltip",
                "sample_text": "aaa",
                "labels": ["Single-storey", "Double-storey"],
                "characters": ["a", "à"],
            },
        )

    def test_get_features_with_character_variants_params_malformed(self):
        from fontTools.ttLib.tables import otTables

        font = self._get_font("/Inter/static/Inter-Regular.ttf")
        ttfont = font.get_ttfont()
        name_table = ttfont["name"]
        feature_params = otTables.FeatureParamsCharacterVariants()
        feature_params.Format = 0
        feature_params.FeatUILabelNameID = name_table.addName("Alternate a")
        feature_params.FeatUITooltipTextNameID = 0
        feature_params.SampleTextNameID = 0
        feature_params.NumNamedParameters = 3
        feature_params.FirstParamUILabelNameID = name_table.addName("Single-storey")
        missing_label_name_id = name_table.addName("Double-storey")
        name_table.addName("Open")
        name_table.removeNames(nameID=missing_label_name_id)
        feature_params.CharCount = 4
        feature_params.Character = [0x61, 0xD800, 0x110000, 0xE0]
        for feature_record in ttfont["GSUB"].table.FeatureList.FeatureRecord:
            if feature_record.FeatureTag == "cv11":
                feature_record.Feature.FeatureParams = feature_params
        features = font.get_features()
        features_by_tag = {feature["tag"]: feature for feature in features}
        self.assertEqual(
            features_by_tag["cv11"]["params"],
            {
                "name": "Alternate a",
                "tooltip": None,
                "sample_text": None,
                "labels": ["Single-storey", None, "Open"],
                "characters": ["a", "à"],
            },
        )

    def test_get_features_tags(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        features = font.get_features_tags()
        self.assertEqual(features, ["smcp"])

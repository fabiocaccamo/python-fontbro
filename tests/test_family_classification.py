# import fsutil
from fontbro.exceptions import ArgumentError
from tests import AbstractTestCase


class FamilyClassificationTestCase(AbstractTestCase):
    """
    This class describes a family classification test case.
    """

    # def test_family_classification_variables(self):
    #     classes = Font._FAMILY_CLASSIFICATIONS["classes"]
    #     for class_item in classes:
    #         class_base_varname = "FAMILY_CLASSIFICATION"
    #         class_item_varname = slugify(class_item["name"]).replace("-", "_").upper()
    #         if "RESERVED" in class_item_varname:
    #             continue
    #         var_name = f"{class_base_varname}_{class_item_varname}: dict[str, int]"
    #         var_value = f"{{'class_id': {class_item['id']}}}"
    #         # print(f"{var_name} = {var_value}")
    #         subclasses = class_item["subclasses"]
    #         if subclasses:
    #             for subclass_item in subclasses:
    #                 subclass_item_varname = (
    #                     slugify(subclass_item["name"]).replace("-", "_").upper()
    #                 )
    #                 if "RESERVED" in subclass_item_varname:
    #                     continue
    #                 var_name = f"{class_base_varname}_{class_item_varname}_{subclass_item_varname}: dict[str, int]"
    #                 var_value = f"{{'class_id':{class_item['id']}, 'subclass_id':{subclass_item['id']}}}"
    #                 # print(f"{var_name} = {var_value}")

    def test_get_family_classification(self):
        with self._get_font("/issues/issue-0052/Bobbiefreebie.ttf") as font:
            # print(font.get_family_classification())
            family_classification = font.get_family_classification()
            expected_family_classification = {
                "full_name": "Scripts / Calligraphic",
                "class_id": 10,
                "class_name": "Scripts",
                "subclass_id": 5,
                "subclass_name": "Calligraphic",
            }
            self.assertEqual(family_classification, expected_family_classification)

    def test_set_family_classification_by_constant(self):
        with self._get_font("/issues/issue-0052/Bobbiefreebie.ttf") as font:
            font.set_family_classification(**font.FAMILY_CLASSIFICATION_SANS_SERIF)
            # print(font.get_family_classification())
            family_classification = font.get_family_classification()
            expected_family_classification = {
                "full_name": "Sans Serif / No Classification",
                "class_id": 8,
                "class_name": "Sans Serif",
                "subclass_id": 0,
                "subclass_name": "No Classification",
            }
            self.assertEqual(family_classification, expected_family_classification)

        with self._get_font("/issues/issue-0052/Bobbiefreebie.ttf") as font:
            font.set_family_classification(
                **font.FAMILY_CLASSIFICATION_SANS_SERIF_NEO_GROTESQUE_GOTHIC
            )
            # print(font.get_family_classification())
            family_classification = font.get_family_classification()
            expected_family_classification = {
                "full_name": "Sans Serif / Neo-grotesque Gothic",
                "class_id": 8,
                "class_name": "Sans Serif",
                "subclass_id": 5,
                "subclass_name": "Neo-grotesque Gothic",
            }
            self.assertEqual(family_classification, expected_family_classification)

    def test_set_family_classification_by_ids(self):
        with self._get_font("/issues/issue-0052/Bobbiefreebie.ttf") as font:
            font.set_family_classification(class_id=8)
            # print(font.get_family_classification())
            family_classification = font.get_family_classification()
            expected_family_classification = {
                "full_name": "Sans Serif / No Classification",
                "class_id": 8,
                "class_name": "Sans Serif",
                "subclass_id": 0,
                "subclass_name": "No Classification",
            }
            self.assertEqual(family_classification, expected_family_classification)

        with self._get_font("/issues/issue-0052/Bobbiefreebie.ttf") as font:
            font.set_family_classification(class_id=8, subclass_id=5)
            # print(font.get_family_classification())
            family_classification = font.get_family_classification()
            expected_family_classification = {
                "full_name": "Sans Serif / Neo-grotesque Gothic",
                "class_id": 8,
                "class_name": "Sans Serif",
                "subclass_id": 5,
                "subclass_name": "Neo-grotesque Gothic",
            }
            self.assertEqual(family_classification, expected_family_classification)

    def test_set_family_classification_with_invalid_class_id(self):
        with self._get_font("/issues/issue-0052/Bobbiefreebie.ttf") as font:
            with self.assertRaises(ArgumentError):
                font.set_family_classification(class_id=15)

    def test_set_family_classification_with_invalid_subclass_id(self):
        with self._get_font("/issues/issue-0052/Bobbiefreebie.ttf") as font:
            with self.assertRaises(ArgumentError):
                font.set_family_classification(class_id=1, subclass_id=16)

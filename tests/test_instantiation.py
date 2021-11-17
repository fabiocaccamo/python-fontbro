# -*- coding: utf-8 -*-

from tests import AbstractTestCase


class InstantiationTestCase(AbstractTestCase):
    """
    Test case for the methods related to the variable font instantiation.
    """

    def _get_static_font(self):
        font = self._get_font('/Tourney/static/Tourney/Tourney-Regular.ttf')
        self.assertTrue(font.is_static())
        return font

    def _get_variable_font(self):
        font = self._get_font('/Tourney/Tourney-VariableFont_wdth,wght.ttf')
        self.assertTrue(font.is_variable())
        return font

    def test_to_static_with_static_font(self):
        font = self._get_static_font()
        with self.assertRaises(TypeError):
            font.to_static()

    def test_to_static_without_coordinates(self):
        font = self._get_variable_font()
        font.to_static()
        self.assertTrue(font.is_static())

    def test_to_static_with_all_coordinates(self):
        font = self._get_variable_font()
        font.to_static(coordinates={'wght': 200, 'wdth': 110})
        self.assertTrue(font.is_static())
        self.assertEqual(font.get_weight()['value'], 200)

    def test_to_static_with_some_coordinates(self):
        font = self._get_variable_font()
        font.to_static(coordinates={'wdth': 110})
        self.assertTrue(font.is_static())
        # weight axis pinned to default value
        self.assertEqual(font.get_weight()['value'], 100)

    def test_to_static_with_coordinates_for_slicing(self):
        font = self._get_variable_font()
        with self.assertRaises(ValueError):
            font.to_static(coordinates={'wght': [100, 400]})

    def test_to_sliced_variable_with_static_font(self):
        font = self._get_static_font()
        with self.assertRaises(TypeError):
            font.to_sliced_variable()

    def test_to_sliced_variable_without_coordinates(self):
        # nothing changes without coordinates
        font = self._get_variable_font()
        with self.assertRaises(ValueError):
            font.to_sliced_variable(coordinates=None)

    def test_to_sliced_variable_with_coordinates_pinned(self):
        # if all coordinates are pinned the result would be a static font
        font = self._get_variable_font()
        with self.assertRaises(ValueError):
            font.to_sliced_variable(coordinates={'wght': 200, 'wdth': 110})

    def test_to_sliced_variable_with_coordinates_sliced_and_passed_as_tuple(self):
        font = self._get_variable_font()
        expected_axes = [
            {
                'defaultValue': 100.0,
                'maxValue': 900.0,
                'minValue': 100.0,
                'name': 'Weight',
                'tag': 'wght',
            },
            {
                'defaultValue': 100.0,
                'maxValue': 125.0,
                'minValue': 75.0,
                'name': 'Wdth',
                'tag': 'wdth',
            },
        ]
        self.assertEqual(font.get_variable_axes(), expected_axes)
        font.to_sliced_variable(coordinates={'wght': (100, 400), 'wdth': (100, 110)})
        expected_axes = [
            {
                'defaultValue': 100.0,
                'maxValue': 400.0,
                'minValue': 100.0,
                'name': 'Weight',
                'tag': 'wght',
            },
            {
                'defaultValue': 100.0,
                'maxValue': 110.0,
                'minValue': 100.0,
                'name': 'Wdth',
                'tag': 'wdth',
            },
        ]
        self.assertEqual(font.get_variable_axes(), expected_axes)

    def test_to_sliced_variable_with_coordinates_sliced_and_passed_as_list(self):
        font = self._get_variable_font()
        expected_axes = [
            {
                'defaultValue': 100.0,
                'maxValue': 900.0,
                'minValue': 100.0,
                'name': 'Weight',
                'tag': 'wght',
            },
            {
                'defaultValue': 100.0,
                'maxValue': 125.0,
                'minValue': 75.0,
                'name': 'Wdth',
                'tag': 'wdth',
            },
        ]
        self.assertEqual(font.get_variable_axes(), expected_axes)
        font.to_sliced_variable(coordinates={'wght': [100, 400], 'wdth': [100, 110]})
        expected_axes = [
            {
                'defaultValue': 100.0,
                'maxValue': 400.0,
                'minValue': 100.0,
                'name': 'Weight',
                'tag': 'wght',
            },
            {
                'defaultValue': 100.0,
                'maxValue': 110.0,
                'minValue': 100.0,
                'name': 'Wdth',
                'tag': 'wdth',
            },
        ]
        self.assertEqual(font.get_variable_axes(), expected_axes)

    def test_to_sliced_variable_with_coordinates_sliced_and_passed_as_dict(self):
        font = self._get_variable_font()
        expected_axes = [
            {
                'defaultValue': 100.0,
                'maxValue': 900.0,
                'minValue': 100.0,
                'name': 'Weight',
                'tag': 'wght',
            },
            {
                'defaultValue': 100.0,
                'maxValue': 125.0,
                'minValue': 75.0,
                'name': 'Wdth',
                'tag': 'wdth',
            },
        ]
        self.assertEqual(font.get_variable_axes(), expected_axes)
        font.to_sliced_variable(
            coordinates={
                'wght': {'min': 100, 'max': 400},
                'wdth': {'min': 100, 'max': 110},
            }
        )
        expected_axes = [
            {
                'defaultValue': 100.0,
                'maxValue': 400.0,
                'minValue': 100.0,
                'name': 'Weight',
                'tag': 'wght',
            },
            {
                'defaultValue': 100.0,
                'maxValue': 110.0,
                'minValue': 100.0,
                'name': 'Wdth',
                'tag': 'wdth',
            },
        ]
        self.assertEqual(font.get_variable_axes(), expected_axes)

    def test_to_sliced_variable_with_coordinates_sliced_and_pinned(self):
        font = self._get_variable_font()
        expected_axes = [
            {
                'defaultValue': 100.0,
                'maxValue': 900.0,
                'minValue': 100.0,
                'name': 'Weight',
                'tag': 'wght',
            },
            {
                'defaultValue': 100.0,
                'maxValue': 125.0,
                'minValue': 75.0,
                'name': 'Wdth',
                'tag': 'wdth',
            },
        ]
        self.assertEqual(font.get_variable_axes(), expected_axes)
        font.to_sliced_variable(coordinates={'wght': (100, 400), 'wdth': 100})
        expected_axes = [
            {
                'defaultValue': 100.0,
                'maxValue': 400.0,
                'minValue': 100.0,
                'name': 'Weight',
                'tag': 'wght',
            },
        ]
        self.assertEqual(font.get_variable_axes(), expected_axes)

if __name__ == '__main__':
    unittest.main()
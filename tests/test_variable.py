from tests import AbstractTestCase


class VariableTestCase(AbstractTestCase):
    """
    Test case for the methods related to the static/variable font.
    """

    def test_get_variable_axes_with_static_font(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        axes = font.get_variable_axes()
        self.assertEqual(axes, None)

    def test_get_variable_axes_with_variable_font(self):
        font = self._get_font("/Roboto_Mono/RobotoMono-VariableFont_wght.ttf")
        axes = font.get_variable_axes()
        self.assertEqual(len(axes), 1)
        self.assertEqual(
            axes[0],
            {
                "tag": "wght",
                "name": "Weight",
                "min_value": 100.0,
                "max_value": 700.0,
                "default_value": 400.0,
            },
        )

    def test_get_variable_axes_tags_with_static_font(self):
        font = self._get_font("/Roboto_Mono/static/RobotoMono-Regular.ttf")
        axes = font.get_variable_axes_tags()
        self.assertEqual(axes, None)

    def test_get_variable_axes_tags_with_variable_font(self):
        font = self._get_font("/Roboto_Mono/RobotoMono-VariableFont_wght.ttf")
        axes = font.get_variable_axes_tags()
        self.assertEqual(len(axes), 1)
        self.assertEqual(axes, ["wght"])

    def test_get_variable_axis_by_tag(self):
        font = self._get_font("/Roboto_Mono/RobotoMono-VariableFont_wght.ttf")
        axis = font.get_variable_axis_by_tag("wdht")
        self.assertEqual(axis, None)
        axis = font.get_variable_axis_by_tag("wght")
        self.assertEqual(
            axis,
            {
                "tag": "wght",
                "name": "Weight",
                "min_value": 100.0,
                "max_value": 700.0,
                "default_value": 400.0,
            },
        )

    def test_get_variable_instances(self):
        font = self._get_font("/Roboto_Mono/RobotoMono-VariableFont_wght.ttf")
        instances = font.get_variable_instances()
        expected_instances = [
            {
                "coordinates": {"wght": 100.0},
                "style_name": "Thin",
            },
            {
                "coordinates": {"wght": 300.0},
                "style_name": "Light",
            },
            {
                "coordinates": {"wght": 400.0},
                "style_name": "Regular",
            },
            {
                "coordinates": {"wght": 500.0},
                "style_name": "Medium",
            },
            {
                "coordinates": {"wght": 700.0},
                "style_name": "Bold",
            },
        ]
        self.assertEqual(instances, expected_instances)

    def test_get_variable_instances_with_static_font(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        instances = font.get_variable_instances()
        self.assertEqual(instances, None)

    def test_get_variable_instance_closest_to_coordinates(self):
        font = self._get_font("/Roboto_Mono/RobotoMono-VariableFont_wght.ttf")
        closest_instance = font.get_variable_instance_closest_to_coordinates(
            {"wght": 650}
        )
        self.assertEqual(
            closest_instance,
            {
                "coordinates": {"wght": 700.0},
                "style_name": "Bold",
            },
        )

    def test_get_variable_instance_closest_to_coordinates_without_all_axes(self):
        font = self._get_font("/Open_Sans/OpenSans-VariableFont_wdth,wght.ttf")
        closest_instance = font.get_variable_instance_closest_to_coordinates(
            {"wdth": 80.0}
        )
        self.assertEqual(
            closest_instance,
            {
                "coordinates": {"wdth": 75.0, "wght": 400.0},
                "style_name": "Condensed Regular",
            },
        )

    def test_get_variable_instance_closest_to_coordinates_with_static_font(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        closest_instance = font.get_variable_instance_closest_to_coordinates(
            {"wght": 650}
        )
        self.assertEqual(closest_instance, None)

    def test_is_static(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        self.assertTrue(font.is_static())
        self.assertFalse(font.is_variable())

    def test_is_variable(self):
        font = self._get_font("/Roboto_Mono/RobotoMono-VariableFont_wght.ttf")
        self.assertFalse(font.is_static())
        self.assertTrue(font.is_variable())

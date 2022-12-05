from fontbro import Font
from tests import AbstractTestCase


class VersionTestCase(AbstractTestCase):
    """
    This class describes a version test case.
    """

    def _test_font_version(self, filepath, expected_value):
        font_path = self._get_font_path(filepath)
        font = Font(filepath=font_path)
        version = font.get_version()
        # print(filepath, width)
        self.assertEqual(version, expected_value)

    def test_get_version(self):
        fonts = [
            {
                "filepath": "/Noto_Sans_TC/NotoSansTC-Regular.otf",
                "version": 2.0019989013671875,
            },
            {
                "filepath": "/Roboto_Mono/RobotoMono-VariableFont_wght.ttf",
                "version": 3.0,
            },
            {
                "filepath": "/Tourney/Tourney-VariableFont_wdth,wght.ttf",
                "version": 1.0149993896484375,
            },
        ]
        for font in fonts:
            # print(font.get_variable_instances())
            with self.subTest(f"Test with font: {font}", font=font):
                self._test_font_version(font["filepath"], font["version"])

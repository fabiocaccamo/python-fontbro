from tests import AbstractTestCase


class ImageTestCase(AbstractTestCase):
    """
    This class describes an image test case.
    """

    def test_get_image(self):
        font = self._get_font("/Noto_Sans_TC/NotoSansTC-Regular.otf")
        image = font.get_image(
            text="Hello World!",
            size=144,
            color=(255, 255, 255, 255),
            background_color=(0, 0, 0, 255),
        )
        # image.show()
        image.close()

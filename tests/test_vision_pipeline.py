from pathlib import Path
import tempfile
import unittest

from ventura_vision import bounding_box_of_dark_pixels, load_pgm, threshold


class VisionPipelineTests(unittest.TestCase):
    def _image(self, text: str):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".pgm", delete=False, encoding="ascii")
        try:
            tmp.write(text)
            tmp.close()
            return load_pgm(Path(tmp.name))
        finally:
            Path(tmp.name).unlink(missing_ok=True)

    def test_loads_and_normalizes_pgm(self):
        image = self._image("P2\n2 2\n15\n0 15 7 8\n")
        self.assertEqual((image.width, image.height), (2, 2))
        self.assertEqual(image.pixels, (0, 255, 119, 136))
        self.assertAlmostEqual(image.mean_intensity, 127.5)

    def test_threshold_and_dark_bounding_box(self):
        image = self._image("P2\n3 2\n255\n255 10 255 255 20 255\n")
        binary = threshold(image, 128)
        self.assertEqual(binary.pixels, (255, 0, 255, 255, 0, 255))
        self.assertEqual(bounding_box_of_dark_pixels(binary), (1, 0, 1, 1))

    def test_rejects_invalid_pixel_count(self):
        with self.assertRaisesRegex(ValueError, "pixel count"):
            self._image("P2\n2 2\n255\n0 1 2\n")


if __name__ == "__main__":
    unittest.main()

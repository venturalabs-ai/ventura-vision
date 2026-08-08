from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GrayImage:
    width: int
    height: int
    pixels: tuple[int, ...]

    @property
    def mean_intensity(self) -> float:
        return sum(self.pixels) / len(self.pixels)

    @property
    def dark_fraction(self) -> float:
        return sum(1 for value in self.pixels if value < 128) / len(self.pixels)


def _tokens(path: Path) -> list[str]:
    tokens: list[str] = []
    for raw_line in path.read_text(encoding="ascii").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if line:
            tokens.extend(line.split())
    return tokens


def load_pgm(path: str | Path) -> GrayImage:
    """Load a deterministic ASCII PGM (P2) image for reproducible CI tests."""
    path = Path(path)
    tokens = _tokens(path)
    if len(tokens) < 4 or tokens[0] != "P2":
        raise ValueError("expected ASCII PGM (P2)")
    width, height, max_value = map(int, tokens[1:4])
    if width <= 0 or height <= 0:
        raise ValueError("image dimensions must be positive")
    if max_value <= 0 or max_value > 65535:
        raise ValueError("invalid PGM max value")
    raw_pixels = [int(value) for value in tokens[4:]]
    if len(raw_pixels) != width * height:
        raise ValueError("pixel count does not match image dimensions")
    if any(value < 0 or value > max_value for value in raw_pixels):
        raise ValueError("pixel value outside declared PGM range")
    pixels = tuple(round(value * 255 / max_value) for value in raw_pixels)
    return GrayImage(width=width, height=height, pixels=pixels)


def threshold(image: GrayImage, cutoff: int = 128) -> GrayImage:
    if not 0 <= cutoff <= 255:
        raise ValueError("cutoff must be between 0 and 255")
    pixels = tuple(255 if value >= cutoff else 0 for value in image.pixels)
    return GrayImage(image.width, image.height, pixels)


def bounding_box_of_dark_pixels(image: GrayImage, cutoff: int = 128) -> tuple[int, int, int, int] | None:
    """Return inclusive x1,y1,x2,y2 for dark pixels; useful as a tiny OCR/inspection preprocessing primitive."""
    coords: list[tuple[int, int]] = []
    for index, value in enumerate(image.pixels):
        if value < cutoff:
            coords.append((index % image.width, index // image.width))
    if not coords:
        return None
    xs = [x for x, _ in coords]
    ys = [y for _, y in coords]
    return min(xs), min(ys), max(xs), max(ys)

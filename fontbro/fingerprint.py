from __future__ import annotations

from typing import Any

from fontTools.ttLib import TTFont
from PIL import Image

from fontbro import render, variable


def get_fingerprint(
    ttfont: TTFont,
    *,
    text: str = "",
) -> Any:
    """
    Gets the fingerprint of the given font:
    an hash calculated from an image representation of the font.
    """
    import imagehash

    text = text or "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    img = render.get_image(ttfont, text=text, size=72)
    img_size = img.size
    img = img.resize((img_size[0] // 2, img_size[1] // 2))
    img = img.resize((img_size[0], img_size[1]), Image.Resampling.NEAREST)
    img = img.quantize(colors=8)
    # img.show()

    hash = imagehash.average_hash(img, hash_size=64)
    return hash


def get_fingerprint_match(
    ttfont: TTFont,
    other_ttfont: TTFont,
    *,
    tolerance: int = 10,
    text: str = "",
) -> tuple[Any, Any, Any, Any]:
    """
    Gets the fingerprint match between the given fonts
    by checking if their fingerprints are equal (difference <= tolerance).
    """
    hash = get_fingerprint(ttfont, text=text)
    other_hash = get_fingerprint(other_ttfont, text=text)
    diff = hash - other_hash
    match = diff <= tolerance
    match = match and variable.is_variable(ttfont) == variable.is_variable(other_ttfont)
    return (match, diff, hash, other_hash)

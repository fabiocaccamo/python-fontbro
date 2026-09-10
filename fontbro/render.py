from __future__ import annotations

import math
import os
import tempfile
from typing import Any

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

from fontbro.unicode import get_best_cmap_or_raise


def get_image(
    ttfont: TTFont,
    *,
    text: str,
    size: int,
    color: tuple[int, int, int, int] = (0, 0, 0, 255),
    background_color: tuple[int, int, int, int] = (255, 255, 255, 255),
) -> Any:
    """
    Gets an image representation of the given font rendering some text.
    """
    with tempfile.TemporaryDirectory() as dest:
        # the font format is detected by its content, not by the file extension
        filepath = os.path.join(dest, "font")
        ttfont.save(filepath)
        img = Image.new("RGBA", (2, 2), background_color)
        draw = ImageDraw.Draw(img)
        img_font = ImageFont.truetype(filepath, size)
        img_bbox = draw.textbbox((0, 0), text, font=img_font)
        img_width = img_bbox[2] - img_bbox[0]
        img_height = img_bbox[3] - img_bbox[1]
        img_size = (img_width, img_height)
        img = img.resize(img_size)
        draw = ImageDraw.Draw(img)
        draw.text((-img_bbox[0], -img_bbox[1]), text, font=img_font, fill=color)
        del img_font
        return img


def get_svg(
    ttfont: TTFont,
    *,
    text: str,
    size: int,
) -> str:
    """
    Gets an SVG representation of the given font rendering some text.
    """
    # get font metrics
    units_per_em = ttfont["head"].unitsPerEm
    scale = size / units_per_em
    hhea = ttfont["hhea"]
    ascent = hhea.ascent * scale
    descent = hhea.descent * scale
    width = 0
    height = ascent - descent

    # get glyph set and character map
    glyphset = ttfont.getGlyphSet()
    cmap = get_best_cmap_or_raise(ttfont)

    # generate svg path for each glyph in text
    glyphs: list[str] = list(filter(None, [cmap.get(ord(char)) for char in text]))
    paths = ""
    for glyph_name in glyphs:
        glyph = glyphset[glyph_name]
        pen = SVGPathPen(glyphset)
        glyph.draw(pen)
        commands = pen.getCommands()
        transform = f"translate({width:.2f} {ascent:.2f}) scale({scale} -{scale})"
        paths += f"""<path d="{commands}" transform="{transform}" />"""
        width += glyph.width * scale

    # round width and height
    width = int(math.ceil(width))
    height = int(math.ceil(height))
    viewbox = f"0 0 {width} {height}"
    xmlns = "http://www.w3.org/2000/svg"

    # generate svg string
    svg_str = f"""<svg width="{width}" height="{height}" viewBox="{viewbox}" xmlns="{xmlns}">{paths}</svg>"""
    return svg_str

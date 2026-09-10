from __future__ import annotations

from typing import Any

from fontTools.ttLib import TTFont

# https://learn.microsoft.com/en-us/typography/opentype/spec/otff#font-tables
_TABLE_NAMES_BY_TAG: dict[str, str] = {
    # required tables
    "cmap": "Character Map",
    "head": "Header",
    "hhea": "Horizontal Header",
    "hmtx": "Horizontal Metrics",
    "maxp": "Maximum Profile",
    "name": "Naming",
    "OS/2": "OS/2",
    "post": "PostScript",
    # truetype outlines tables
    "cvt ": "Control Value Table",
    "fpgm": "Font Program",
    "glyf": "Glyph Data",
    "loca": "Location",
    "prep": "Control Value Program",
    "gasp": "Grid-fitting and Scan-conversion Procedure",
    # cff outlines tables
    "CFF ": "CFF",
    "CFF2": "CFF2",
    "VORG": "Vertical Origin",
    # svg outlines tables
    "SVG ": "Scalable Vector Graphics",
    # bitmap glyphs tables
    "EBDT": "Embedded Bitmap Data",
    "EBLC": "Embedded Bitmap Location",
    "EBSC": "Embedded Bitmap Scaling",
    "CBDT": "Color Bitmap Data",
    "CBLC": "Color Bitmap Location",
    "sbix": "Standard Bitmap Graphics",
    # advanced typographic tables
    "BASE": "Baseline",
    "GDEF": "Glyph Definition",
    "GPOS": "Glyph Positioning",
    "GSUB": "Glyph Substitution",
    "JSTF": "Justification",
    "MATH": "Math Layout",
    # font variations tables
    "avar": "Axis Variations",
    "cvar": "CVT Variations",
    "fvar": "Font Variations",
    "gvar": "Glyph Variations",
    "HVAR": "Horizontal Metrics Variations",
    "MVAR": "Metrics Variations",
    # also listed in other tables by the spec, since static fonts can use it
    "STAT": "Style Attributes",
    "VVAR": "Vertical Metrics Variations",
    # color fonts tables
    "COLR": "Color",
    "CPAL": "Color Palette",
    # other tables
    "DSIG": "Digital Signature",
    "hdmx": "Horizontal Device Metrics",
    "kern": "Kerning",
    "LTSH": "Linear Threshold",
    "MERG": "Merge",
    "meta": "Metadata",
    "PCLT": "PCL 5",
    "VDMX": "Vertical Device Metrics",
    "vhea": "Vertical Header",
    "vmtx": "Vertical Metrics",
    # apple tables not in the opentype spec
    # https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6.html
    "acnt": "Accent Attachment",
    "ankr": "Anchor Point",
    "bdat": "Bitmap Data",
    "bhed": "Bitmap Header",
    "bloc": "Bitmap Location",
    "bsln": "Baseline",
    "fdsc": "Font Descriptors",
    "feat": "Feature Name",
    "fmtx": "Font Metrics",
    "fond": "Font Family Compatibility",
    "gcid": "Glyph to CID Mapping",
    "hvgl": "Hierarchical Variation Glyphs",
    "hvpm": "Hierarchical Variation Part Mapping",
    "just": "Justification",
    "kerx": "Extended Kerning",
    "lcar": "Ligature Caret",
    "ltag": "Language Tags",
    "mort": "Glyph Metamorphosis",
    "morx": "Extended Glyph Metamorphosis",
    "opbd": "Optical Bounds",
    "prop": "Glyph Properties",
    "trak": "Tracking",
    "xref": "Cross-Reference",
    "Zapf": "Glyph Information",
}


def get_tables_tags(
    ttfont: TTFont,
    *,
    include_unknown: bool = True,
) -> list[str]:
    """
    Gets the table tags present in the given font,
    sorted in the recommended table order (as fontTools does).
    """
    return [
        tag
        for tag in ttfont.keys()
        # "GlyphOrder" is a fontTools bookkeeping entry, not a real font table
        if tag != "GlyphOrder" and (include_unknown or tag in _TABLE_NAMES_BY_TAG)
    ]


def get_tables(
    ttfont: TTFont,
    *,
    include_unknown: bool = True,
) -> list[dict[str, Any]]:
    """
    Gets the table metadata present in the given font.
    """
    is_woff2 = ttfont.flavor == "woff2"
    tables = []
    for tag in get_tables_tags(ttfont, include_unknown=include_unknown):
        entry = ttfont.reader.tables.get(tag)
        # woff/woff2 entries store the compressed length in "length"
        length = getattr(entry, "origLength", getattr(entry, "length", None))
        offset = None if is_woff2 else getattr(entry, "offset", None)
        tables.append(
            {
                "tag": tag,
                "name": _TABLE_NAMES_BY_TAG.get(tag, tag),
                "length": length,
                "offset": offset,
            }
        )
    return tables

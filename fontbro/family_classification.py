from __future__ import annotations

from typing import Any

from fontTools.ttLib import TTFont

from fontbro.exceptions import ArgumentError, OperationError
from fontbro.utils import concat_names, find_item, read_json

# Family Classification:
# https://learn.microsoft.com/en-us/typography/opentype/spec/ibmfc
_FAMILY_CLASSIFICATIONS: dict[str, list[dict[str, Any]]] = read_json(
    "data/family-classifications.json"
)
# fmt: off
FAMILY_CLASSIFICATION_NO_CLASSIFICATION: dict[str, int] = {'class_id': 0}
FAMILY_CLASSIFICATION_OLDSTYLE_SERIFS: dict[str, int] = {'class_id': 1}
FAMILY_CLASSIFICATION_OLDSTYLE_SERIFS_NO_CLASSIFICATION: dict[str, int] = {'class_id':1, 'subclass_id':0}
FAMILY_CLASSIFICATION_OLDSTYLE_SERIFS_IBM_ROUNDED_LEGIBILITY: dict[str, int] = {'class_id':1, 'subclass_id':1}
FAMILY_CLASSIFICATION_OLDSTYLE_SERIFS_GARALDE: dict[str, int] = {'class_id':1, 'subclass_id':2}
FAMILY_CLASSIFICATION_OLDSTYLE_SERIFS_VENETIAN: dict[str, int] = {'class_id':1, 'subclass_id':3}
FAMILY_CLASSIFICATION_OLDSTYLE_SERIFS_MODIFIED_VENETIAN: dict[str, int] = {'class_id':1, 'subclass_id':4}
FAMILY_CLASSIFICATION_OLDSTYLE_SERIFS_DUTCH_MODERN: dict[str, int] = {'class_id':1, 'subclass_id':5}
FAMILY_CLASSIFICATION_OLDSTYLE_SERIFS_DUTCH_TRADITIONAL: dict[str, int] = {'class_id':1, 'subclass_id':6}
FAMILY_CLASSIFICATION_OLDSTYLE_SERIFS_CONTEMPORARY: dict[str, int] = {'class_id':1, 'subclass_id':7}
FAMILY_CLASSIFICATION_OLDSTYLE_SERIFS_CALLIGRAPHIC: dict[str, int] = {'class_id':1, 'subclass_id':8}
FAMILY_CLASSIFICATION_OLDSTYLE_SERIFS_MISCELLANEOUS: dict[str, int] = {'class_id':1, 'subclass_id':15}
FAMILY_CLASSIFICATION_TRANSITIONAL_SERIFS: dict[str, int] = {'class_id': 2}
FAMILY_CLASSIFICATION_TRANSITIONAL_SERIFS_NO_CLASSIFICATION: dict[str, int] = {'class_id':2, 'subclass_id':0}
FAMILY_CLASSIFICATION_TRANSITIONAL_SERIFS_DIRECT_LINE: dict[str, int] = {'class_id':2, 'subclass_id':1}
FAMILY_CLASSIFICATION_TRANSITIONAL_SERIFS_SCRIPT: dict[str, int] = {'class_id':2, 'subclass_id':2}
FAMILY_CLASSIFICATION_TRANSITIONAL_SERIFS_MISCELLANEOUS: dict[str, int] = {'class_id':2, 'subclass_id':15}
FAMILY_CLASSIFICATION_MODERN_SERIFS: dict[str, int] = {'class_id': 3}
FAMILY_CLASSIFICATION_MODERN_SERIFS_NO_CLASSIFICATION: dict[str, int] = {'class_id':3, 'subclass_id':0}
FAMILY_CLASSIFICATION_MODERN_SERIFS_ITALIAN: dict[str, int] = {'class_id':3, 'subclass_id':1}
FAMILY_CLASSIFICATION_MODERN_SERIFS_SCRIPT: dict[str, int] = {'class_id':3, 'subclass_id':2}
FAMILY_CLASSIFICATION_MODERN_SERIFS_MISCELLANEOUS: dict[str, int] = {'class_id':3, 'subclass_id':15}
FAMILY_CLASSIFICATION_CLARENDON_SERIFS: dict[str, int] = {'class_id': 4}
FAMILY_CLASSIFICATION_CLARENDON_SERIFS_NO_CLASSIFICATION: dict[str, int] = {'class_id':4, 'subclass_id':0}
FAMILY_CLASSIFICATION_CLARENDON_SERIFS_CLARENDON: dict[str, int] = {'class_id':4, 'subclass_id':1}
FAMILY_CLASSIFICATION_CLARENDON_SERIFS_MODERN: dict[str, int] = {'class_id':4, 'subclass_id':2}
FAMILY_CLASSIFICATION_CLARENDON_SERIFS_TRADITIONAL: dict[str, int] = {'class_id':4, 'subclass_id':3}
FAMILY_CLASSIFICATION_CLARENDON_SERIFS_NEWSPAPER: dict[str, int] = {'class_id':4, 'subclass_id':4}
FAMILY_CLASSIFICATION_CLARENDON_SERIFS_STUB_SERIF: dict[str, int] = {'class_id':4, 'subclass_id':5}
FAMILY_CLASSIFICATION_CLARENDON_SERIFS_MONOTONE: dict[str, int] = {'class_id':4, 'subclass_id':6}
FAMILY_CLASSIFICATION_CLARENDON_SERIFS_TYPEWRITER: dict[str, int] = {'class_id':4, 'subclass_id':7}
FAMILY_CLASSIFICATION_CLARENDON_SERIFS_MISCELLANEOUS: dict[str, int] = {'class_id':4, 'subclass_id':15}
FAMILY_CLASSIFICATION_SLAB_SERIFS: dict[str, int] = {'class_id': 5}
FAMILY_CLASSIFICATION_SLAB_SERIFS_NO_CLASSIFICATION: dict[str, int] = {'class_id':5, 'subclass_id':0}
FAMILY_CLASSIFICATION_SLAB_SERIFS_MONOTONE: dict[str, int] = {'class_id':5, 'subclass_id':1}
FAMILY_CLASSIFICATION_SLAB_SERIFS_HUMANIST: dict[str, int] = {'class_id':5, 'subclass_id':2}
FAMILY_CLASSIFICATION_SLAB_SERIFS_GEOMETRIC: dict[str, int] = {'class_id':5, 'subclass_id':3}
FAMILY_CLASSIFICATION_SLAB_SERIFS_SWISS: dict[str, int] = {'class_id':5, 'subclass_id':4}
FAMILY_CLASSIFICATION_SLAB_SERIFS_TYPEWRITER: dict[str, int] = {'class_id':5, 'subclass_id':5}
FAMILY_CLASSIFICATION_SLAB_SERIFS_MISCELLANEOUS: dict[str, int] = {'class_id':5, 'subclass_id':15}
FAMILY_CLASSIFICATION_FREEFORM_SERIFS: dict[str, int] = {'class_id': 7}
FAMILY_CLASSIFICATION_FREEFORM_SERIFS_NO_CLASSIFICATION: dict[str, int] = {'class_id':7, 'subclass_id':0}
FAMILY_CLASSIFICATION_FREEFORM_SERIFS_MODERN: dict[str, int] = {'class_id':7, 'subclass_id':1}
FAMILY_CLASSIFICATION_FREEFORM_SERIFS_MISCELLANEOUS: dict[str, int] = {'class_id':7, 'subclass_id':15}
FAMILY_CLASSIFICATION_SANS_SERIF: dict[str, int] = {'class_id': 8}
FAMILY_CLASSIFICATION_SANS_SERIF_NO_CLASSIFICATION: dict[str, int] = {'class_id':8, 'subclass_id':0}
FAMILY_CLASSIFICATION_SANS_SERIF_IBM_NEO_GROTESQUE_GOTHIC: dict[str, int] = {'class_id':8, 'subclass_id':1}
FAMILY_CLASSIFICATION_SANS_SERIF_HUMANIST: dict[str, int] = {'class_id':8, 'subclass_id':2}
FAMILY_CLASSIFICATION_SANS_SERIF_LOW_X_ROUND_GEOMETRIC: dict[str, int] = {'class_id':8, 'subclass_id':3}
FAMILY_CLASSIFICATION_SANS_SERIF_HIGH_X_ROUND_GEOMETRIC: dict[str, int] = {'class_id':8, 'subclass_id':4}
FAMILY_CLASSIFICATION_SANS_SERIF_NEO_GROTESQUE_GOTHIC: dict[str, int] = {'class_id':8, 'subclass_id':5}
FAMILY_CLASSIFICATION_SANS_SERIF_MODIFIED_NEO_GROTESQUE_GOTHIC: dict[str, int] = {'class_id':8, 'subclass_id':6}
FAMILY_CLASSIFICATION_SANS_SERIF_TYPEWRITER_GOTHIC: dict[str, int] = {'class_id':8, 'subclass_id':9}
FAMILY_CLASSIFICATION_SANS_SERIF_MATRIX: dict[str, int] = {'class_id':8, 'subclass_id':10}
FAMILY_CLASSIFICATION_SANS_SERIF_MISCELLANEOUS: dict[str, int] = {'class_id':8, 'subclass_id':15}
FAMILY_CLASSIFICATION_ORNAMENTALS: dict[str, int] = {'class_id': 9}
FAMILY_CLASSIFICATION_ORNAMENTALS_NO_CLASSIFICATION: dict[str, int] = {'class_id':9, 'subclass_id':0}
FAMILY_CLASSIFICATION_ORNAMENTALS_ENGRAVER: dict[str, int] = {'class_id':9, 'subclass_id':1}
FAMILY_CLASSIFICATION_ORNAMENTALS_BLACK_LETTER: dict[str, int] = {'class_id':9, 'subclass_id':2}
FAMILY_CLASSIFICATION_ORNAMENTALS_DECORATIVE: dict[str, int] = {'class_id':9, 'subclass_id':3}
FAMILY_CLASSIFICATION_ORNAMENTALS_THREE_DIMENSIONAL: dict[str, int] = {'class_id':9, 'subclass_id':4}
FAMILY_CLASSIFICATION_ORNAMENTALS_MISCELLANEOUS: dict[str, int] = {'class_id':9, 'subclass_id':15}
FAMILY_CLASSIFICATION_SCRIPTS: dict[str, int] = {'class_id': 10}
FAMILY_CLASSIFICATION_SCRIPTS_NO_CLASSIFICATION: dict[str, int] = {'class_id':10, 'subclass_id':0}
FAMILY_CLASSIFICATION_SCRIPTS_UNCIAL: dict[str, int] = {'class_id':10, 'subclass_id':1}
FAMILY_CLASSIFICATION_SCRIPTS_BRUSH_JOINED: dict[str, int] = {'class_id':10, 'subclass_id':2}
FAMILY_CLASSIFICATION_SCRIPTS_FORMAL_JOINED: dict[str, int] = {'class_id':10, 'subclass_id':3}
FAMILY_CLASSIFICATION_SCRIPTS_MONOTONE_JOINED: dict[str, int] = {'class_id':10, 'subclass_id':4}
FAMILY_CLASSIFICATION_SCRIPTS_CALLIGRAPHIC: dict[str, int] = {'class_id':10, 'subclass_id':5}
FAMILY_CLASSIFICATION_SCRIPTS_BRUSH_UNJOINED: dict[str, int] = {'class_id':10, 'subclass_id':6}
FAMILY_CLASSIFICATION_SCRIPTS_FORMAL_UNJOINED: dict[str, int] = {'class_id':10, 'subclass_id':7}
FAMILY_CLASSIFICATION_SCRIPTS_MONOTONE_UNJOINED: dict[str, int] = {'class_id':10, 'subclass_id':8}
FAMILY_CLASSIFICATION_SCRIPTS_MISCELLANEOUS: dict[str, int] = {'class_id':10, 'subclass_id':15}
FAMILY_CLASSIFICATION_SYMBOLIC: dict[str, int] = {'class_id': 12}
FAMILY_CLASSIFICATION_SYMBOLIC_NO_CLASSIFICATION: dict[str, int] = {'class_id':12, 'subclass_id':0}
FAMILY_CLASSIFICATION_SYMBOLIC_MIXED_SERIF: dict[str, int] = {'class_id':12, 'subclass_id':3}
FAMILY_CLASSIFICATION_SYMBOLIC_OLDSTYLE_SERIF: dict[str, int] = {'class_id':12, 'subclass_id':6}
FAMILY_CLASSIFICATION_SYMBOLIC_NEO_GROTESQUE_SANS_SERIF: dict[str, int] = {'class_id':12, 'subclass_id':7}
FAMILY_CLASSIFICATION_SYMBOLIC_MISCELLANEOUS: dict[str, int] = {'class_id':12, 'subclass_id':15}
# fmt: on


def _get_family_classification_items(
    class_id: int | str,
    subclass_id: int | str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    classes_list = _FAMILY_CLASSIFICATIONS["classes"]
    class_item = find_item(
        items_list=classes_list,
        key=lambda item: item.get("id") == class_id,
    )
    subclasses_list = class_item.get("subclasses", [])
    subclass_item = find_item(
        items_list=subclasses_list,
        key=lambda item: item.get("id") == subclass_id,
    )
    return (class_item, subclass_item)


def get_family_classification(
    ttfont: TTFont,
) -> dict[str, Any] | None:
    """
    Gets the family classification of the given font reading the OS/2.sFamilyClass
    field, None is returned if the font has no OS/2 table.
    """
    os2 = ttfont.get("OS/2")
    if not os2:
        return None
    class_id = os2.sFamilyClass >> 8  # (or // 256)
    subclass_id = os2.sFamilyClass & 0xFF  # (or % 256)

    class_item, subclass_item = _get_family_classification_items(
        class_id=class_id,
        subclass_id=subclass_id,
    )
    # class_id = class_item.get("id", "")
    class_name = class_item.get("name", "")
    # subclass_id = subclass_item.get("id", "")
    subclass_name = subclass_item.get("name", "")
    full_name = concat_names(class_name, subclass_name, separator=" / ")

    return {
        "full_name": full_name,
        "class_id": class_id,
        "class_name": class_name,
        "subclass_id": subclass_id,
        "subclass_name": subclass_name,
    }


def set_family_classification(
    ttfont: TTFont,
    class_id: int,
    subclass_id: int = 0,
) -> None:
    """
    Sets the family classification of the given font in the OS/2.sFamilyClass field.
    """
    os2 = ttfont.get("OS/2")
    if not os2:
        raise OperationError("Invalid OS/2 table (doesn't exist).")

    # validate class key and subclass key
    class_item, subclass_item = _get_family_classification_items(
        class_id=class_id,
        subclass_id=subclass_id,
    )
    if not class_item:
        raise ArgumentError("Invalid class key argument.")

    if not subclass_item and subclass_id:
        raise ArgumentError("Invalid subclass key argument.")

    class_id = class_item["id"]
    if subclass_item:
        subclass_id = subclass_item["id"]

    family_class = (class_id << 8) | (subclass_id & 0xFF)
    os2.sFamilyClass = family_class

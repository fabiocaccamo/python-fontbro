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

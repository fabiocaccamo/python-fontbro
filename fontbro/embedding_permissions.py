from __future__ import annotations

from fontTools.ttLib import TTFont

from fontbro.exceptions import ArgumentError, OperationError
from fontbro.flags import get_flag, set_flag

# Embedding Permissions:
# https://learn.microsoft.com/en-us/typography/opentype/spec/os2#fstype
# bits 1-3 are the mutually exclusive usage permissions sub-field, valid
# fonts have at most one of them set; "installable" is not a real bit,
# it's the state where none of them is set (bit 0 is reserved and unused).
_PERMISSIONS_BITS: dict[str, int] = {
    "restricted": 1,
    "preview_and_print": 2,
    "editable": 3,
    "no_subsetting": 8,
    "bitmap_embedding_only": 9,
}

_USAGE_PERMISSIONS_KEYS: tuple[str, ...] = (
    "restricted",
    "preview_and_print",
    "editable",
)

_USAGE_PERMISSIONS_MASK: int = 0x000E  # bits 1-3


def _get_fs_type_with_usage_permissions(
    fs_type: int,
    usage_permissions: dict[str, bool | None],
) -> int:
    """
    Gets the fsType value with the mutually exclusive usage permissions
    (bits 1-3) updated, values set to None will be ignored.
    """
    usage_permissions_keys = ", ".join(f"'{key}'" for key in usage_permissions)
    enabled_usage_permissions = [
        key for key, value in usage_permissions.items() if value is True
    ]
    if len(enabled_usage_permissions) > 1:
        raise ArgumentError(
            f"Usage permissions {usage_permissions_keys} are mutually exclusive, "
            "only one of them can be set to True at the same time, "
            f"found: {enabled_usage_permissions}."
        )
    if enabled_usage_permissions:
        # a valid font has at most one usage permission bit set
        fs_type &= ~_USAGE_PERMISSIONS_MASK
        key = enabled_usage_permissions[0]
        if key != "installable":
            fs_type = set_flag(fs_type, _PERMISSIONS_BITS[key], True)
        return fs_type
    for key in _USAGE_PERMISSIONS_KEYS:
        if usage_permissions[key] is False:
            fs_type = set_flag(fs_type, _PERMISSIONS_BITS[key], False)
    if usage_permissions["installable"] is False and not (
        fs_type & _USAGE_PERMISSIONS_MASK
    ):
        raise ArgumentError(
            "'installable' can be set to False only if another usage "
            f"permission of {usage_permissions_keys} is in effect, "
            "set one of them to True instead."
        )
    return fs_type


def get_embedding_permissions(
    ttfont: TTFont,
) -> dict[str, bool]:
    """
    Gets the embedding permissions from the OS/2 fsType field of the given font.
    """
    os2 = ttfont.get("OS/2")
    fs_type = os2.fsType if os2 else 0
    permissions = {
        key: get_flag(fs_type, bit) for key, bit in _PERMISSIONS_BITS.items()
    }
    installable = not fs_type & _USAGE_PERMISSIONS_MASK
    return {"installable": installable, **permissions}


def set_embedding_permissions(
    ttfont: TTFont,
    *,
    installable: bool | None = None,
    restricted: bool | None = None,
    preview_and_print: bool | None = None,
    editable: bool | None = None,
    no_subsetting: bool | None = None,
    bitmap_embedding_only: bool | None = None,
) -> None:
    """
    Sets the embedding permissions in the OS/2 fsType field of the given font,
    the fsType field is left untouched if any argument is invalid.
    """
    os2 = ttfont.get("OS/2")
    if not os2:
        raise OperationError("Invalid OS/2 table (doesn't exist).")

    usage_permissions = {
        "installable": installable,
        "restricted": restricted,
        "preview_and_print": preview_and_print,
        "editable": editable,
    }
    other_permissions = {
        "no_subsetting": no_subsetting,
        "bitmap_embedding_only": bitmap_embedding_only,
    }
    for key, value in {**usage_permissions, **other_permissions}.items():
        if value is not None and not isinstance(value, bool):
            raise ArgumentError(
                f"Invalid '{key}' value, expected bool or None, got {value!r}."
            )

    # compute the new value and write it only once, to keep it consistent
    fs_type = _get_fs_type_with_usage_permissions(os2.fsType, usage_permissions)
    for key, value in other_permissions.items():
        if value is not None:
            fs_type = set_flag(fs_type, _PERMISSIONS_BITS[key], value)
    os2.fsType = fs_type

from __future__ import annotations


def get_flag(
    bits: int,
    bit: int,
) -> bool:
    """
    Gets the flag value.

    :param bits: The bits
    :type bits: int
    :param bit: The bit index
    :type bit: int

    :returns: The flag value
    :rtype: bool
    """
    return bool(bits & (1 << bit))


def set_flag(
    bits: int,
    bit: int,
    value: bool,
) -> int:
    """
    Sets the flag value.

    :param bits: The bits
    :type bits: int
    :param bit: The bit index
    :type bit: int
    :param value: The bit value
    :type value: bool

    :returns: The bits
    :rtype: int
    """
    mask = 1 << bit
    return bits | mask if value else bits & ~mask

from __future__ import annotations

import re
from collections.abc import Iterable

from fontTools.subset import parse_unicodes as _parse_unicodes


def parse_unicodes(
    unicodes: Iterable[int | str] | str,
) -> list[int]:
    if isinstance(unicodes, (list, set, tuple)):
        # convert possible int codepoints to hex str
        unicodes_list = list(unicodes)
        for index, code in enumerate(unicodes_list):
            unicodes_list[index] = f"{code:04X}" if isinstance(code, int) else code
        unicodes_str = ",".join(list(set(unicodes_list)))
    elif isinstance(unicodes, str):
        unicodes_str = unicodes
    else:
        raise ValueError("Invalid 'unicodes' value.")
    assert isinstance(unicodes_str, str)
    # replace possible — ‐ − (&mdash; &dash; &minus;) with -
    unicodes_str = re.sub(r"[\—\‐\−]", "-", unicodes_str)
    # remove U+, \u, u if present
    unicodes_str = re.sub(r"(U\+)|(\\u)|(u)", "", unicodes_str, flags=re.I)
    unicodes_list = list(_parse_unicodes(unicodes_str))
    return unicodes_list

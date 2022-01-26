# -*- coding: utf-8 -*-

from fontTools.subset import parse_unicodes as _parse_unicodes

import re


def parse_unicodes(unicodes):
    unicodes = unicodes or ""
    if isinstance(unicodes, (list, set, tuple)):
        unicodes = ",".join(list(set(unicodes)))
    # replace possible — ‐ − (&mdash; &dash; &minus;) with -
    unicodes = re.sub(r"[\—\‐\−]", "-", unicodes)
    # remove U+, \u, u if present
    unicodes = re.sub(r"(U\+)|(\\u)|(u)", "", unicodes, flags=re.I)
    unicodes = _parse_unicodes(unicodes)
    # print(unicodes)
    return unicodes

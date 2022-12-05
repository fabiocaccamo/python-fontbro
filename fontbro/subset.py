import re

from fontTools.subset import parse_unicodes as _parse_unicodes


def parse_unicodes(unicodes):
    unicodes = unicodes or ""
    if isinstance(unicodes, (list, set, tuple)):
        # convert possible int codepoints to hex str
        unicodes = list(unicodes)
        for index in range(len(unicodes)):
            code = unicodes[index]
            unicodes[index] = f"{code:04X}" if isinstance(code, int) else code
        unicodes = ",".join(list(set(unicodes)))
    assert isinstance(unicodes, str)
    # replace possible — ‐ − (&mdash; &dash; &minus;) with -
    unicodes = re.sub(r"[\—\‐\−]", "-", unicodes)
    # remove U+, \u, u if present
    unicodes = re.sub(r"(U\+)|(\\u)|(u)", "", unicodes, flags=re.I)
    unicodes = _parse_unicodes(unicodes)
    # print(unicodes)
    return unicodes

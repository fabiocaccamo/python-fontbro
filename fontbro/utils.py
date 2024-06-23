from __future__ import annotations

from typing import Any
import re
import unicodedata

import fsutil


def concat_names(
    a: str,
    b: str,
    *,
    separator: str = " ",
) -> str:
    return f"{a}{separator}{b}" if not a.endswith(f"{separator}{b}") and b else a


def read_json(
    filepath: str,
) -> Any:
    return fsutil.read_file_json(fsutil.join_path(__file__, filepath))


def remove_spaces(
    s: str,
) -> str:
    return s.replace(" ", "")


def slugify(
    s: str,
) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"[^\w\-]", "", s)
    s = s.strip("-")
    return s.lower().strip().replace(" ", "-")

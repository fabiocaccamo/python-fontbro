from __future__ import annotations

from typing import Any

import fsutil


def concat_names(
    a: str,
    b: str,
) -> str:
    return f"{a} {b}" if not a.endswith(f" {b}") else a


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
    return s.lower().strip().replace(" ", "-")

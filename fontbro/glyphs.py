from __future__ import annotations

from typing import Any


class _OutlineFoundError(Exception):
    """
    Raised by the outline detector pen to stop drawing at the first outline.
    """


class _OutlineDetectorPen:
    """
    Pen that stops drawing at the first outline or component,
    much faster than drawing the whole glyph (eg. CFF charstrings).
    """

    def moveTo(self, pt: Any) -> None:
        raise _OutlineFoundError

    def lineTo(self, pt: Any) -> None:
        raise _OutlineFoundError

    def curveTo(self, *points: Any) -> None:
        raise _OutlineFoundError

    def qCurveTo(self, *points: Any) -> None:
        raise _OutlineFoundError

    def closePath(self) -> None:
        pass

    def endPath(self) -> None:
        pass

    def addComponent(self, glyphName: str, transformation: Any) -> None:
        raise _OutlineFoundError


def is_glyph_blank(
    glyphset: Any,
    glyph_name: str,
) -> bool:
    """
    Determines if the glyph is blank (without outlines and components),
    it works with all outlines formats (glyf, CFF, CFF2).
    """
    try:
        glyphset[glyph_name].draw(_OutlineDetectorPen())
    except _OutlineFoundError:
        return False
    return True

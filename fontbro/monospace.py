from __future__ import annotations

from collections import Counter

from fontTools.ttLib import TTFont

from fontbro.glyphs import get_glyphs_count


def is_monospace(
    ttfont: TTFont,
    *,
    threshold: float = 0.85,
) -> bool:
    """
    Determines if the given font is a monospace font.
    """
    widths = [metrics[0] for metrics in ttfont["hmtx"].metrics.values()]
    widths_counter = Counter(widths)
    same_width_count = widths_counter.most_common(1)[0][1]
    same_width_amount = same_width_count / get_glyphs_count(ttfont)
    return same_width_amount >= threshold

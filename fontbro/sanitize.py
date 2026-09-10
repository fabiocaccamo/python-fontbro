from __future__ import annotations

import os
import tempfile

import ots
from fontTools.ttLib import TTFont

from fontbro.exceptions import SanitizationError


def sanitize(
    ttfont: TTFont,
    *,
    strict: bool = True,
) -> None:
    """
    Sanitizes the given font using OpenType Sanitizer,
    the font is saved to a temporary file that is checked by the sanitizer.
    """
    with tempfile.TemporaryDirectory() as dest:
        # the font format is detected by its content, not by the file name
        filepath = os.path.join(dest, "font")
        ttfont.save(filepath)
        result = ots.sanitize(
            filepath,
            capture_output=True,
            encoding="utf-8",
        )
        error_code = result.returncode
        errors = result.stderr
        if error_code:
            raise SanitizationError(
                f"OpenType Sanitizer returned non-zero exit code ({error_code}): \n{errors}"
            )

        elif strict:
            warnings = result.stdout
            success_message = "File sanitized successfully!\n"
            if warnings != success_message:
                warnings = warnings.rstrip(success_message)
                raise SanitizationError(f"OpenType Sanitizer warnings: \n{warnings}")

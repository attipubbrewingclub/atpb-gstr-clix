"""Validate a 63-character S3 bucket GUID (PRFX / hex middle / fixed SUFX)."""

from __future__ import annotations

import re
import sys

from atpb_gstr_clix.commands.constants import SUFX, TOTAL_LEN

_PRFX_RE = re.compile(r"^[a-z0-9]{4}(?:-[a-z0-9]{4})*$")
_ALLOWED_CHARS_RE = re.compile(r"^[a-z0-9-]+$")
_MIDDLE_RE = re.compile(r"^[a-f0-9]+$")


def validation_error(name: str) -> str | None:
    """Return an error message if invalid, or None if the name is valid (no I/O)."""
    name = name.strip()
    if not name:
        return "error: GUID must be non-empty"

    if len(name) != TOTAL_LEN:
        return f"error: length must be exactly {TOTAL_LEN} characters (got {len(name)})"

    if not _ALLOWED_CHARS_RE.fullmatch(name):
        return "error: only lowercase letters, digits, and hyphens are allowed"

    tail = "-" + SUFX
    if not name.endswith(tail):
        return f"error: GUID must end with SUFX {SUFX!r}"

    body = name[: -len(tail)]
    parts = body.rsplit("-", 1)
    if len(parts) != 2:
        return "error: could not separate PRFX, middle, and SUFX"

    prfx_part, middle = parts
    if not middle or "-" in middle:
        return (
            "error: generated inner segment must be non-empty hexadecimal "
            "with no hyphens"
        )

    if not _MIDDLE_RE.fullmatch(middle):
        return "error: inner segment must be lowercase hexadecimal (a-f, 0-9) only"

    if not _PRFX_RE.fullmatch(prfx_part):
        return (
            "error: PRFX must be groups of four lowercase alphanumeric characters "
            "separated by hyphens (e.g. abcd-ef01-2345)"
        )

    return None


def run(name: str) -> int:
    err = validation_error(name)
    if err:
        print(err, file=sys.stderr)
        return 1
    print("GUID is valid.")
    return 0

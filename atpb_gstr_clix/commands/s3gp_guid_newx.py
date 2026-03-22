"""Build a 63-character S3 bucket GUID from PRFX, random middle, and fixed SUFX."""

from __future__ import annotations

import secrets
import sys

from atpb_gstr_clix.commands import s3gp_guid_vldt
from atpb_gstr_clix.commands.constants import SUFX, TOTAL_LEN


def _random_hex(length: int) -> str:
    if length <= 0:
        return ""
    return secrets.token_hex((length + 1) // 2)[:length]


def run(prfx: str) -> int:
    prfx = prfx.strip()
    if not prfx:
        print("error: PRFX must be non-empty", file=sys.stderr)
        return 1

    middle_len = TOTAL_LEN - len(prfx) - len(SUFX) - 2
    if middle_len < 1:
        print(
            "error: PRFX is too long for a 63-character S3 bucket GUID "
            f"(max {TOTAL_LEN - len(SUFX) - 2} characters)",
            file=sys.stderr,
        )
        return 1

    middle = _random_hex(middle_len)
    full = f"{prfx}-{middle}-{SUFX}"
    err = s3gp_guid_vldt.validation_error(full)
    if err:
        print(err, file=sys.stderr)
        return 1
    print(full)
    return 0

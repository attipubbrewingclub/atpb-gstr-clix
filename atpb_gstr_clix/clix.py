"""Command-line entry: argparse and dispatch to feature handlers."""

from __future__ import annotations

import argparse
import json
import sys
from importlib.metadata import PackageNotFoundError, distribution
from importlib.metadata import version as pkg_version

from atpb_gstr_clix.commands import s3gp_guid_newx, s3gp_guid_vldt
from atpb_gstr_clix.commands.constants import (
    BUILD_TIMESTAMP_FALLBACK,
    PKG_VERSION_FALLBACK,
)

_USAGE = (
    "atpb-gstr-clix --s3bx --guid --newx PRFX | "
    "atpb-gstr-clix --s3bx --guid --vldt GUID"
)


def _package_version() -> str:
    try:
        return pkg_version("atpb-gstr-clix")
    except PackageNotFoundError:
        return PKG_VERSION_FALLBACK


def _build_timestamp() -> str:
    try:
        from atpb_gstr_clix._build_time import BUILD_TIMESTAMP
    except ImportError:
        return BUILD_TIMESTAMP_FALLBACK
    return BUILD_TIMESTAMP


def _install_tag() -> str:
    """dev = editable install or not installed; prod = normal install."""
    try:
        dist = distribution("atpb-gstr-clix")
    except PackageNotFoundError:
        return "dev"
    try:
        raw = dist.read_text("direct_url.json")
    except (OSError, KeyError, TypeError, UnicodeError):
        return "prod"
    if not raw:
        return "prod"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return "prod"
    if data.get("dir_info", {}).get("editable") is True:
        return "dev"
    return "prod"


def _version_banner() -> str:
    return f"%(prog)s {_package_version()} [{_install_tag()}] ({_build_timestamp()})"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="atpb-gstr-clix",
        description="atpb-gstr command-line utilities",
    )
    parser.add_argument(
        "-v",
        "--vrsn",
        action="version",
        version=_version_banner(),
        help="show version and exit",
    )
    parser.add_argument(
        "--s3bx",
        action="store_true",
        help="amazon s3 bucket utilities",
    )
    parser.add_argument(
        "--guid",
        action="store_true",
        help="guid segment helpers (use with --s3bx)",
    )
    parser.add_argument(
        "--newx",
        metavar="PRFX",
        dest="s3bx_guid_newx_prfx",
        help=(
            "generate a 63-character bucket guid: PRFX-hex-sufx "
            "(use with --s3bx --guid)"
        ),
    )
    parser.add_argument(
        "--vldt",
        metavar="GUID",
        dest="s3bx_guid_vldt_guid",
        help="validate a bucket guid (use with --s3bx --guid)",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    newx = args.s3bx_guid_newx_prfx
    vldt = args.s3bx_guid_vldt_guid

    if newx is not None and vldt is not None:
        parser.error("cannot use --newx and --vldt together")

    ready = args.s3bx and args.guid
    if ready and newx is not None:
        sys.exit(s3gp_guid_newx.run(newx))
    if ready and vldt is not None:
        sys.exit(s3gp_guid_vldt.run(vldt))

    partial = args.s3bx or args.guid or newx is not None or vldt is not None
    reason = "incomplete arguments" if partial else "no command"
    parser.error(f"{reason}; use: {_USAGE}")


if __name__ == "__main__":
    main()

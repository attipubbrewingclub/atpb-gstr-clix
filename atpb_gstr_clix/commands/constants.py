"""Shared constants for S3-style 63-character bucket GUIDs."""

from __future__ import annotations

SUFX = "347156581106-us-east-1-an"
TOTAL_LEN = 63

# Must match [tool.setuptools_scm].fallback_version in pyproject.toml.
PKG_VERSION_FALLBACK = "0.1.0"

# Used for --vrsn when _build_time.py was not emitted (e.g. editable install).
BUILD_TIMESTAMP_FALLBACK = "local"

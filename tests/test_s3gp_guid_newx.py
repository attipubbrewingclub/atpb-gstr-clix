"""Tests for S3 bucket GUID generation (--newx / PRFX)."""

from __future__ import annotations

import pytest

from atpb_gstr_clix.commands import constants, s3gp_guid_newx


def test_run_rejects_empty_prefix(capsys: pytest.CaptureFixture[str]) -> None:
    assert s3gp_guid_newx.run("   ") == 1
    err = capsys.readouterr().err
    assert "non-empty" in err


def test_run_does_not_print_name_when_vldt_fails_on_prefix(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(s3gp_guid_newx, "_random_hex", lambda n: "a" * n)
    assert s3gp_guid_newx.run("bad") != 0
    captured = capsys.readouterr()
    assert captured.out.strip() == ""
    assert "PRFX" in captured.err


def test_run_rejects_prefix_too_long(capsys: pytest.CaptureFixture[str]) -> None:
    prefix = "a" * (constants.TOTAL_LEN - len(constants.SUFX) - 1)
    assert s3gp_guid_newx.run(prefix) == 1
    assert "too long" in capsys.readouterr().err


def test_run_success_with_longest_validator_safe_prefix(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Longest 4-hyphen-4 prefix that still fits 63 chars; then auto --vldt passes."""
    # Long arbitrary prefix fits length math but can fail PRFX rules; this one is valid.
    prefix = "-".join(["aaaa"] * 7)  # 34 chars, seven xxxx groups
    middle_len = constants.TOTAL_LEN - len(prefix) - len(constants.SUFX) - 2
    assert middle_len == 2
    monkeypatch.setattr(s3gp_guid_newx, "_random_hex", lambda n: "c" * n)
    assert s3gp_guid_newx.run(prefix) == 0
    out = capsys.readouterr().out.strip()
    assert out == f"{prefix}-cc-{constants.SUFX}"
    assert len(out) == constants.TOTAL_LEN


def test_run_success_shape_and_length(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    prefix = "atpb-gstr-s3gp"
    middle_len = constants.TOTAL_LEN - len(prefix) - len(constants.SUFX) - 2
    monkeypatch.setattr(
        s3gp_guid_newx,
        "_random_hex",
        lambda n: "b" * n,
    )
    assert s3gp_guid_newx.run(prefix) == 0
    out = capsys.readouterr().out.strip()
    assert out == f"{prefix}-{'b' * middle_len}-{constants.SUFX}"
    assert len(out) == constants.TOTAL_LEN

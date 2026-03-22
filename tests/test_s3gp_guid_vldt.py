"""Tests for S3 bucket GUID validation (--vldt)."""

from __future__ import annotations

import pytest

from atpb_gstr_clix.commands import constants, s3gp_guid_vldt

VALID_NAME = "atpb-gstr-s3gp-a6a439aa6cc44abcaeb6af-347156581106-us-east-1-an"


def test_run_accepts_well_formed_name(capsys: pytest.CaptureFixture[str]) -> None:
    assert s3gp_guid_vldt.run(VALID_NAME) == 0
    assert capsys.readouterr().out.strip() == "GUID is valid."


def test_run_rejects_wrong_length(capsys: pytest.CaptureFixture[str]) -> None:
    short = VALID_NAME[:-1]
    assert s3gp_guid_vldt.run(short) == 1
    assert "63" in capsys.readouterr().err


def test_run_rejects_wrong_sufx(capsys: pytest.CaptureFixture[str]) -> None:
    bad = VALID_NAME[:-2] + "xx"
    assert len(bad) == len(VALID_NAME)
    assert s3gp_guid_vldt.run(bad) == 1
    assert "SUFX" in capsys.readouterr().err


def test_run_rejects_empty_name(capsys: pytest.CaptureFixture[str]) -> None:
    assert s3gp_guid_vldt.run("") == 1
    assert "non-empty" in capsys.readouterr().err


def test_run_rejects_uppercase_letter(capsys: pytest.CaptureFixture[str]) -> None:
    bad = VALID_NAME.replace("atpb", "Atpb", 1)
    assert len(bad) == len(VALID_NAME)
    assert s3gp_guid_vldt.run(bad) == 1
    assert "lowercase" in capsys.readouterr().err


def test_run_rejects_non_hex_middle(capsys: pytest.CaptureFixture[str]) -> None:
    # middle contains 'g' (valid charset, not hex)
    bad = VALID_NAME.replace("a6a439aa6cc44abcaeb6af", "g6a439aa6cc44abcaeb6af", 1)
    assert len(bad) == 63
    assert s3gp_guid_vldt.run(bad) == 1
    assert "hexadecimal" in capsys.readouterr().err


def test_run_rejects_body_without_middle_separator(
    capsys: pytest.CaptureFixture[str],
) -> None:
    # 37 chars without '-', then fixed SUFX (no hyphen before middle)
    body = "a" * 37
    name = body + "-" + constants.SUFX
    assert len(name) == 63
    assert s3gp_guid_vldt.run(name) == 1
    assert "separate" in capsys.readouterr().err


def test_run_rejects_bad_prefix_groups(capsys: pytest.CaptureFixture[str]) -> None:
    # 63 chars: same middle/SUFX, first segment 3 chars (invalid 4-hyphen-4 pattern)
    bad = "atp-gstr-s3gp-a6a439aa6cc44abcaeb6af0-347156581106-us-east-1-an"
    assert len(bad) == 63
    assert s3gp_guid_vldt.run(bad) == 1
    assert "PRFX" in capsys.readouterr().err

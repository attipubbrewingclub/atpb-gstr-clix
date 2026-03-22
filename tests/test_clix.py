"""Tests for atpb_gstr_clix.clix (argv + exit codes)."""

from __future__ import annotations

import re
import sys
from importlib.metadata import version

import pytest

from atpb_gstr_clix import clix


def test_main_new_dispatches(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    def fake_run(p: str) -> int:
        calls.append(p)
        return 0

    monkeypatch.setattr(clix.s3gp_guid_newx, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["prog", "--s3bx", "--guid", "--newx", "x"])
    with pytest.raises(SystemExit) as exc:
        clix.main()
    assert exc.value.code == 0
    assert calls == ["x"]


def test_main_vldt_dispatches(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    def fake_run(n: str) -> int:
        calls.append(n)
        return 0

    monkeypatch.setattr(clix.s3gp_guid_vldt, "run", fake_run)
    monkeypatch.setattr(
        sys,
        "argv",
        ["prog", "--s3bx", "--guid", "--vldt", "a" * 63],
    )
    with pytest.raises(SystemExit) as exc:
        clix.main()
    assert exc.value.code == 0
    assert len(calls[0]) == 63


def test_main_rejects_new_and_vldt_together(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["prog", "--s3bx", "--guid", "--newx", "a", "--vldt", "b"],
    )
    with pytest.raises(SystemExit) as exc:
        clix.main()
    assert exc.value.code == 2


def test_main_partial_chain_exits_2(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["prog", "--s3bx"])
    with pytest.raises(SystemExit) as exc:
        clix.main()
    assert exc.value.code == 2


def test_main_no_args_exits_2(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["prog"])
    with pytest.raises(SystemExit) as exc:
        clix.main()
    assert exc.value.code == 2


def test_main_guid_only_exits_2(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["prog", "--guid"])
    with pytest.raises(SystemExit) as exc:
        clix.main()
    assert exc.value.code == 2


@pytest.mark.parametrize("flag", ["-v", "--vrsn"])
def test_main_version_exits_0(
    flag: str,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(sys, "argv", ["prog", flag])
    with pytest.raises(SystemExit) as exc:
        clix.main()
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "atpb-gstr-clix" in out
    assert version("atpb-gstr-clix") in out
    assert re.search(
        r"\(local\)|\(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC\)",
        out,
    ), out
    assert "[dev]" in out or "[prod]" in out


def test_main_new_propagates_nonzero_exit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(clix.s3gp_guid_newx, "run", lambda _p: 5)
    monkeypatch.setattr(sys, "argv", ["prog", "--s3bx", "--guid", "--newx", "x"])
    with pytest.raises(SystemExit) as exc:
        clix.main()
    assert exc.value.code == 5

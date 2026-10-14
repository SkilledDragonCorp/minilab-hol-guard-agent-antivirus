"""Assert pinned CLI versions."""

from __future__ import annotations

from tests.conftest import run_cmd, which


def test_hol_guard_version() -> None:
    result = run_cmd([which("hol-guard"), "--version"])
    assert result.returncode == 0, result.stderr
    assert "3.43.1" in result.stdout


def test_plugin_scanner_version() -> None:
    result = run_cmd([which("plugin-scanner"), "--version"])
    assert result.returncode == 0, result.stderr
    assert "3.43.1" in result.stdout

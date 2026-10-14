"""Clean skill passes --fail-on-severity high."""

from __future__ import annotations

import json
from pathlib import Path

from tests.conftest import run_cmd, which, write_scan_report, write_skill


def test_scanner_clean_skill(tmp_path: Path) -> None:
    body = """---
name: hello-world
description: Clean hello-world skill fixture with no secrets.
---

# Hello world

Say hello. No secrets, no shell pipelines, no instruction overrides.
"""
    write_skill(tmp_path, "hello-world", body)
    scan_target = tmp_path

    fail_result = run_cmd(
        [
            which("plugin-scanner"),
            "scan",
            str(scan_target),
            "--ecosystem",
            "claude",
            "--fail-on-severity",
            "high",
        ]
    )
    assert fail_result.returncode == 0, fail_result.stdout + fail_result.stderr

    json_result = run_cmd(
        [
            which("plugin-scanner"),
            "scan",
            str(scan_target),
            "--ecosystem",
            "claude",
            "--format",
            "json",
        ]
    )
    report = json.loads(json_result.stdout)
    summary = report.get("summary", {}).get("findings", {})
    assert summary.get("critical", 0) == 0
    assert summary.get("high", 0) == 0

    write_scan_report(
        {
            "tool": "plugin-scanner",
            "version": "3.43.1",
            "case": "clean_skill",
            "exit_code": fail_result.returncode,
            "summary_findings": summary,
        }
    )

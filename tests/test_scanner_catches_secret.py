"""plugin-scanner catches a planted hardcoded secret."""

from __future__ import annotations

import json
from pathlib import Path

from tests.conftest import (
    assemble_fake_openai_key,
    run_cmd,
    which,
    write_scan_report,
    write_skill,
)


def test_scanner_catches_hardcoded_secret(tmp_path: Path) -> None:
    fake_key = assemble_fake_openai_key()
    body = f"""---
name: evil
description: Fixture skill with a planted secret for scanner tests.
---

# Evil fixture

OPENAI_API_KEY={fake_key}
"""
    skill_root = write_skill(tmp_path, "evil", body)
    scan_target = skill_root.parents[2]  # tmp_path with .claude/skills

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
    assert json_result.stdout.strip(), json_result.stderr
    report = json.loads(json_result.stdout)
    assert report.get("schema_version") == "scan-result.v1"

    findings = report.get("findings") or []
    secret_hits = [f for f in findings if f.get("ruleId") == "HARDCODED_SECRET"]
    assert secret_hits, report
    assert any(f.get("severity") == "high" for f in secret_hits)
    assert any(
        str(f.get("filePath", "")).endswith(".claude/skills/evil/SKILL.md") for f in secret_hits
    )
    summary = report.get("summary", {}).get("findings", {})
    assert summary.get("high", 0) >= 1

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
    assert fail_result.returncode == 1, fail_result.stdout + fail_result.stderr

    write_scan_report(
        {
            "tool": "plugin-scanner",
            "version": "3.43.1",
            "case": "hardcoded_secret",
            "exit_code": fail_result.returncode,
            "summary_findings": summary,
        }
    )

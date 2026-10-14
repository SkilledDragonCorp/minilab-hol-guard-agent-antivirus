"""Shared helpers for HOL Guard / plugin-scanner lab tests."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "out"
REPORT_PATH = OUT_DIR / "scan-report.json"

TELEMETRY_ENV = {
    "DO_NOT_TRACK": "1",
    "DISABLE_TELEMETRY": "1",
}


def which(cmd: str) -> str:
    path = shutil.which(cmd)
    if not path:
        pytest.fail(f"{cmd} not found on PATH (run: uv sync --frozen --group dev)")
    return path


def run_cmd(
    args: list[str],
    *,
    env: dict[str, str] | None = None,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    merged = {**os.environ, **TELEMETRY_ENV}
    if env:
        merged.update(env)
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        cwd=cwd or REPO_ROOT,
        env=merged,
        check=False,
    )


def write_skill(root: Path, name: str, body: str) -> Path:
    skill_dir = root / ".claude" / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    path = skill_dir / "SKILL.md"
    path.write_text(body, encoding="utf-8")
    return skill_dir


def assemble_fake_openai_key() -> str:
    # Assembled at runtime so no secret-shaped literal is committed.
    return "sk-" + "proj-" + ("A" * 36)


def write_scan_report(payload: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        **payload,
        "utc_timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    }
    REPORT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

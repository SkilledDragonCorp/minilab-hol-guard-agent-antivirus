"""Dogfood: scan this repo's own .claude/skills."""

from __future__ import annotations

from tests.conftest import REPO_ROOT, run_cmd, which


def test_own_skills_pass_high() -> None:
    skills = REPO_ROOT / ".claude" / "skills"
    assert skills.is_dir()
    result = run_cmd(
        [
            which("plugin-scanner"),
            "scan",
            str(REPO_ROOT),
            "--ecosystem",
            "claude",
            "--fail-on-severity",
            "high",
        ]
    )
    assert result.returncode == 0, result.stdout + result.stderr

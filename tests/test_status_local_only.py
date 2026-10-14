"""hol-guard status in throwaway Guard home (local-only mode)."""

from __future__ import annotations

import time
from pathlib import Path

from tests.conftest import run_cmd, which

_TRANSIENT = (
    "native_guard_config_unavailable",
    "native_runner_authority_resident_unavailable",
)


def test_status_local_only(tmp_path: Path) -> None:
    # Isolate Guard state via --home. Blanking env HOME can break native status
    # on some hosts; --home is the supported throwaway-home flag.
    # Native authority can briefly be unavailable under load — retry.
    home = tmp_path / "home"
    home.mkdir()
    result = None
    for attempt in range(6):
        result = run_cmd(
            [which("hol-guard"), "status", "--home", str(home)],
            env={"DO_NOT_TRACK": "1"},
        )
        if result.returncode == 0:
            break
        err = result.stderr + result.stdout
        if not any(token in err for token in _TRANSIENT):
            break
        time.sleep(1.5 * (attempt + 1))
    assert result is not None
    assert result.returncode == 0, result.stderr + result.stdout
    combined = result.stdout + result.stderr
    assert "Local only" in combined

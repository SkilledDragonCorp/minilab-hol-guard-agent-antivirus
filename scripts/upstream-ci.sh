#!/usr/bin/env bash
# Upstream CI cohort — commands copied verbatim from hol-guard
# .github/workflows/ci.yml (job native-command-evaluators) and
# .github/actions/ci-job-compatibility/action.yml at 759302e90a88
set -euo pipefail

# Workflow-level env from upstream CI (shell equivalents).
export DO_NOT_TRACK=1
export DISABLE_TELEMETRY=1
export CARGO_PROFILE_RELEASE_LTO=false
export CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
export UV_HTTP_TIMEOUT=300

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
mkdir -p vendor
rm -rf vendor/hol-guard

git clone https://github.com/hashgraph-online/hol-guard.git vendor/hol-guard
cd vendor/hol-guard
git checkout 759302e90a88201b262bcd6fe5202b001da8f36c
# From native-command-evaluators at 759302e90a88: trust refresh → release
# build → verify/stage generated catalogs (required before export).
python3 scripts/refresh_extension_artifacts.py --trust-only
cargo build --manifest-path rust/Cargo.toml --locked --release -p guard-command -p hol-guard-runtime --bin guard-command-source --bin hol-guard-runtime
python3 scripts/ci/verify_native_command_program.py --compiler rust/target/release/guard-command-source
# From ci-job-compatibility/action.yml at the same pin (uv sync + export +
# pytest cohort). Export needs the catalogs staged by verify above.
uv sync --frozen --no-dev --group ci-test --python 3.13
uv run --no-sync python scripts/export_extension_directory.py
uv run --no-sync python scripts/render_command_extension_directory.py
uv run --no-sync python scripts/export_extension_directory.py --check
uv run --no-sync python scripts/render_command_extension_directory.py --check
export HOL_GUARD_NATIVE_BINARY="$PWD/rust/target/release/hol-guard-runtime"
uv run --no-sync pytest tests/test_cli.py tests/test_verification.py tests/test_action_runner.py tests/test_cisco_install_surfaces.py tests/test_policy.py --tb=short
HOL_GUARD_NATIVE_REGRESSION=1 uv run --no-sync pytest tests/test_policy_bundle_parser.py --tb=short

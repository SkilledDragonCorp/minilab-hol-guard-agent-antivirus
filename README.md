# minilab-hol-guard-agent-antivirus

**Built by SkilledDragon LLC — architecture-led software engineering · [skilleddragon.com](https://skilleddragon.com)**

Keyless preflight lab for [HOL Guard](https://github.com/hashgraph-online/hol-guard): install the pinned CLIs, prove `plugin-scanner` blocks a skill with a planted secret, pass a clean skill, run `hol-guard status` in local-only mode, and re-run upstream’s native-command-evaluators cohort at a pinned SHA.

| Piece | Purpose |
| --- | --- |
| `hol-guard==3.43.1` / `plugin-scanner==3.43.1` | PyPI pins (uv.lock) |
| `tests/` | Keyless pytest oracles |
| `scripts/upstream-ci.sh` | Upstream CI cohort at pin |
| `.claude/skills/agent-antivirus-preflight/` | Scan-before-install skill |

Upstream pin: [hashgraph-online/hol-guard](https://github.com/hashgraph-online/hol-guard) @ `759302e90a88201b262bcd6fe5202b001da8f36c` (Apache-2.0) · PyPI `hol-guard==3.43.1` + `plugin-scanner==3.43.1`.

## What we built and why

Anthropic (2026-10-12) warned that small models may be months from self-replicating on cheap IoT. Payoff for builders: before your agent installs a skill or MCP server, scan it and keep a runtime guard on. This lab proves HOL Guard’s **local, keyless** path — no Guard Cloud account.

## What we tested (observed results)

Oracles from box run 2026-10-13 (~03:45 CT) and re-verified in this lab’s pytest suite:

| Check | Expected / observed |
| --- | --- |
| `hol-guard --version` | `hol-guard 3.43.1` |
| `plugin-scanner --version` | `plugin-scanner 3.43.1` |
| `hol-guard status --home <tmp>` | exit 0; panel shows `sync local only` / `State Local only` |
| Risky skill (`OPENAI_API_KEY=sk-proj-` + 36 chars, assembled at test time) | JSON `HARDCODED_SECRET` / `high`; `--fail-on-severity high` → exit **1** |
| Clean hello-world skill | `--fail-on-severity high` → exit **0** (may still report medium/low; do not assert grade) |
| Own `.claude/skills` | `--fail-on-severity high` → exit 0 |
| Static-scan gap fixture (`curl … \| sh` + “Ignore all previous instructions”) | `critical`/`high` == 0; those lines not flagged at 3.43.1 |

JSON summaries land in `out/scan-report.json` (gitignored).

### Upstream cohort

Commands in `scripts/upstream-ci.sh` are copied from upstream `.github/workflows/ci.yml` (`native-command-evaluators`) and `.github/actions/ci-job-compatibility/action.yml` at `759302e90a88`. Toolchain: Rust **1.88.0**, uv **0.9.26**, Python **3.13**.

## Setup

Requires Python `>=3.12` and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/SkilledDragonCorp/minilab-hol-guard-agent-antivirus.git
cd minilab-hol-guard-agent-antivirus
cp .env.example .env
uv sync --frozen --group dev
```

## Tutorial

### 1. Install and check versions

```bash
uv sync --frozen --group dev
uv run hol-guard --version
uv run plugin-scanner --version
```

### 2. Local-only status

```bash
DO_NOT_TRACK=1 uv run hol-guard status --home "$(mktemp -d)"
```

Expect protection / sync / state reflecting **local only** (`State Local only`, `sync local only`). Do not run `hol-guard connect`.

### 3. Scan a skill

```bash
uv run plugin-scanner scan .claude/skills --ecosystem claude --format json
uv run plugin-scanner scan .claude/skills --ecosystem claude --fail-on-severity high
```

### 4. Wire into pre-install habit

Use the skill in `.claude/skills/agent-antivirus-preflight/SKILL.md`: scan first, refuse on high/critical, then confirm `hol-guard status`.

### 5. Lab tests

```bash
DO_NOT_TRACK=1 DISABLE_TELEMETRY=1 uv run pytest -q
uv run ruff check .
uv run pip-audit
python3 scripts/check-skills
test ! -e .cursor/skills && test ! -e .agents/skills
```

### 6. Upstream cohort (optional locally; required in CI `upstream` job)

```bash
bash scripts/upstream-ci.sh
```

Cold Rust release build may take a long time (`timeout-minutes: 45` in CI).

## Using these skills in Claude Code and Cursor

Both Claude Code and Cursor read agent skills from **`.claude/skills/<name>/SKILL.md`** only. This repo does not ship `.cursor/skills` or `.agents/skills` mirrors.

- **Claude Code:** skills under `.claude/skills/` are discovered automatically; invoke by describing the preflight task or naming `agent-antivirus-preflight`.
- **Cursor:** same path; open or reference `.claude/skills/agent-antivirus-preflight/SKILL.md` so the agent follows scan-before-install.

## API keys

None. Keyless end to end. Guard Cloud is optional and **out of scope** — do not run `hol-guard connect` in CI.

## Telemetry

No telemetry env var was found in upstream `src/` at the pin for a required opt-out switch. Guard Cloud is opt-in via `hol-guard connect`. This lab sets `DO_NOT_TRACK=1` and `DISABLE_TELEMETRY=1` in CI and tests, and uses a throwaway `HOME` for `hol-guard status`.

## Limitation (honest)

At `plugin-scanner==3.43.1`, static scanning catches planted secrets (`HARDCODED_SECRET`) but did **not** flag `curl … | sh`, `~/.ssh/id_rsa` reads, or “Ignore all previous instructions” in box runs. Runtime guard is the other half of the story. Never claim the static scanner catches prompt injection.

## License

Apache-2.0 (lab and featured upstream).

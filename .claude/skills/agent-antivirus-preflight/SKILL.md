---
name: agent-antivirus-preflight
description: Scan a skill, plugin or MCP folder with plugin-scanner before installing it; refuse on high/critical
---

# Agent antivirus preflight

Before installing any Claude Code / Cursor skill, plugin, or MCP folder, run a static scan and keep a runtime guard on.

## Scan (static)

From a machine with `plugin-scanner==3.43.1` on PATH (this lab: `uv sync --frozen --group dev`):

```bash
plugin-scanner scan <path> --ecosystem claude --format json
plugin-scanner scan <path> --ecosystem claude --fail-on-severity high
```

- Exit `0` under `--fail-on-severity high` → no critical/high findings; proceed only if you still trust the source.
- Exit `1` → refuse install. Open the JSON report, fix or discard the skill.
- Treat `HARDCODED_SECRET` and other high findings as blockers.

## Runtime guard (local)

```bash
hol-guard status
```

Expect local-only mode for this lab (`State Local only` / sync local only). Do not run `hol-guard connect` in CI.

## What static scanning does not catch (3.43.1)

At `plugin-scanner==3.43.1`, box runs did **not** flag:

- `curl … | sh` style install lines
- Reads of `~/.ssh/id_rsa`
- Prompt-injection text such as "Ignore all previous instructions"

That is why you keep HOL Guard's runtime protection on. Never claim the static scanner catches prompt injection.

## Habit

1. Scan the candidate path.
2. Refuse on high/critical.
3. Confirm `hol-guard status` shows local protection before the agent can install tools.

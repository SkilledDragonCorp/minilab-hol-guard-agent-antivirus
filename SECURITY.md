# Security Policy

**Built by [SkilledDragon LLC](https://skilleddragon.com)**

This is a **SkilledDragon educational minilab**, not a production product. We do **not** maintain these repos on a regular schedule and we do **not** operate a vulnerability response program for them.

## Contact

General questions: **hello@skilleddragon.com**  
Do not use a dedicated security mailbox for this repo — none exists.

## If you find an issue

- Prefer reporting **upstream** when the issue is in [hashgraph-online/hol-guard](https://github.com/hashgraph-online/hol-guard) or the PyPI packages `hol-guard` / `plugin-scanner`.
- For something specific to this minilab’s scripts or CI, you may email hello@skilleddragon.com. There is **no SLA**, and we may not patch or reply quickly.

## Supported versions

Only the commit currently on `main` is considered current for this educational lab.

## Secret handling

- Never commit `.env`, API keys, or tokens.
- This lab is **keyless** end to end. Do not run `hol-guard connect` or any Guard Cloud login in CI.
- Scanner fixtures assemble fake key-shaped strings at test time from pieces so no secret-shaped literal is committed.

## Tooling pins

| Control | Pin |
| --- | --- |
| Upstream | `hashgraph-online/hol-guard` @ `759302e90a88201b262bcd6fe5202b001da8f36c` (tag `v3.43.1` lineage; Apache-2.0) |
| PyPI | `hol-guard==3.43.1`, `plugin-scanner==3.43.1` |
| gitleaks | `v8.30.1` (pre-commit hook + CI binary with SHA256 verify) |
| Dependency audit | `uv run pip-audit` |
| uv (CI) | `0.9.26` |
| Rust (upstream job) | `1.88.0` |

## Upstream license

`hol-guard` / `plugin-scanner` are Apache-2.0. This lab ships Apache-2.0 as well.

Use at your own risk. Pin versions, review the code, and treat this as sample material.

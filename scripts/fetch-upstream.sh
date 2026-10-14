#!/usr/bin/env bash
# Clone HOL Guard and check out the pinned CI SHA (no build).
set -euo pipefail

PIN_SHA="759302e90a88201b262bcd6fe5202b001da8f36c"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR="${ROOT}/vendor/hol-guard"

mkdir -p "${ROOT}/vendor"
if [[ -d "${VENDOR}/.git" ]]; then
  git -C "${VENDOR}" fetch --depth 1 origin "${PIN_SHA}"
  git -C "${VENDOR}" checkout --force "${PIN_SHA}"
else
  rm -rf "${VENDOR}"
  git clone --filter=blob:none https://github.com/hashgraph-online/hol-guard.git "${VENDOR}"
  git -C "${VENDOR}" checkout "${PIN_SHA}"
fi

git -C "${VENDOR}" rev-parse HEAD
test "$(git -C "${VENDOR}" rev-parse HEAD)" = "${PIN_SHA}"
echo "vendor/hol-guard @ ${PIN_SHA}"

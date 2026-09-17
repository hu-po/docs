#!/usr/bin/env bash
# Run autoresearch rounds on the RSI deck.   ./autoresearch.sh [rounds] [sleep-seconds-between]
# One `claude -p` invocation per round; stops early once iterations.md ends with DONE.
# Add your usual unattended flags to CLAUDE_FLAGS if you want it to run without prompts.
set -euo pipefail
cd "$(dirname "$0")"
ROUNDS="${1:-12}"; SLEEP="${2:-0}"
export PATH="$HOME/.local/bin:$PATH"
CLAUDE_FLAGS="${CLAUDE_FLAGS:---permission-mode auto}"
for i in $(seq 1 "$ROUNDS"); do
  if tail -1 iterations.md | grep -qx DONE; then echo "DONE reached"; exit 0; fi
  echo "=== round invocation $i  $(date)" | tee -a autoresearch.log
  # shellcheck disable=SC2086
  claude -p "$(cat autoresearch.md)" $CLAUDE_FLAGS 2>&1 | tee -a autoresearch.log
  if tail -1 iterations.md | grep -qx DONE; then echo "DONE reached"; exit 0; fi
  if [ "$SLEEP" -gt 0 ]; then sleep "$SLEEP"; fi
done

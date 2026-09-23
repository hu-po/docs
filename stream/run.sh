#!/usr/bin/env bash
# Run unattended phase rounds for a stream.   stream/run.sh <research|deck|thumbnail> <YYYY.MM.DD> [max-rounds]
# Run from the stream's worktree (created by stream/new.sh). One `claude -p` invocation per round;
# stops once log.md ends with RESEARCH DONE / DECK DONE. Set CLAUDE_FLAGS for your unattended flags.
# Model per phase: research/deck = opus (judgment + looking at figures), thumbnail = sonnet.
# Override with STREAM_MODEL=<alias or id>. Each round appends wall minutes / turns / tokens to <folder>/usage.jsonl (local, gitignored)
# (tokens are the lead agent's; usd_equiv is API-equivalent cost and includes subagents).
set -euo pipefail
TOOLS="$(cd "$(dirname "$0")" && pwd)"; REPO="$(dirname "$TOOLS")"
PHASE="${1:?phase: research|deck|thumbnail}"; DATE="${2:?stream date YYYY.MM.DD}"
MAX="${3:-$([ "$PHASE" = deck ] && echo 8 || echo 5)}"
export PATH="$HOME/.local/bin:$PATH"
CLAUDE_FLAGS="${CLAUDE_FLAGS:---permission-mode auto}"
case "$PHASE" in research) STOP="RESEARCH DONE"; M=opus;; deck) STOP="DECK DONE"; M=opus;; thumbnail) STOP=""; M=sonnet;; *) echo "unknown phase $PHASE"; exit 1;; esac

find_dir() { ls -d "$REPO/$DATE".*/ 2>/dev/null | head -1 | sed 's:/$::'; }
done_yet() { [ -n "$STOP" ] && [ -f "$(find_dir)/log.md" ] && tail -1 "$(find_dir)/log.md" | grep -qx "$STOP"; }
if [ "$PHASE" = deck ] && [ ! -f "$(find_dir)/picks.json" ]; then
  echo "no picks.json yet: review first ->  stream/py review.py serve $(find_dir)"; exit 1; fi

MODEL="${STREAM_MODEL:-$M}"
sweep_end=$(date +%F)
for i in $(seq 1 "$([ "$PHASE" = thumbnail ] && echo 1 || echo "$MAX")"); do
  done_yet && { echo "$STOP"; exit 0; }
  DIR="$(find_dir)"; [ -n "$DIR" ] || { echo "no folder $REPO/$DATE.*"; exit 1; }
  echo "=== $PHASE round invocation $i  $(date)" | tee -a "$DIR/run.log"
  prompt="$(sed -e "s|{{DIR}}|$DIR|g" -e "s|{{TOOLS}}|$TOOLS|g" -e "s|{{TODAY}}|$(date +%F)|g" \
               -e "s|{{STREAM_DATE}}|$DATE|g" -e "s|{{SWEEP_END}}|$sweep_end|g" -e "s|{{MAX_ROUNDS}}|$MAX|g" \
               "$TOOLS/phases/$PHASE.md")"
  # shellcheck disable=SC2086
  t0=$(date +%s)
  out="$(cd "$REPO" && claude -p "$prompt" --model "$MODEL" --output-format json $CLAUDE_FLAGS 2>>"$DIR.stderr.log")" || true
  D2="$(find_dir)"   # deck round 1 renames the folder
  [ -f "$DIR.stderr.log" ] && { cat "$DIR.stderr.log" >> "$D2/run.log"; rm -f "$DIR.stderr.log"; }
  printf '%s' "$out" | PHASE="$PHASE" ROUND="$i" MODEL="$MODEL" WALL=$(( $(date +%s) - t0 )) python3 -c '
import json, os, sys, datetime as dt
raw = sys.stdin.read()
try: j = json.loads(raw)
except ValueError: print(raw); sys.exit()
u = j.get("usage") or {}
row = dict(when=dt.datetime.now().isoformat(timespec="minutes"), phase=os.environ["PHASE"], round=int(os.environ["ROUND"]),
           model=os.environ["MODEL"], minutes=round(int(os.environ["WALL"]) / 60, 1), turns=j.get("num_turns"),
           input=u.get("input_tokens"), cache_write=u.get("cache_creation_input_tokens"),
           cache_read=u.get("cache_read_input_tokens"), output=u.get("output_tokens"),
           usd_equiv=round(j.get("total_cost_usd") or 0, 2), error=j.get("is_error"))
open(sys.argv[1], "a").write(json.dumps(row) + "\n")
print(j.get("result", "")); print("usage:", json.dumps(row))
' "$D2/usage.jsonl" | tee -a "$D2/run.log"
done
done_yet && echo "$STOP" || echo "stopped after $MAX rounds (no $STOP marker yet)"

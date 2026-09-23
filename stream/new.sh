#!/usr/bin/env bash
# Start a stream: fresh worktree + folder.   stream/new.sh [YYYY.MM.DD]   (default: next Friday)
# Creates ~/docs-<date> on branch stream/<date> from main, with <date>.untitled/ inside. The deck phase
# renames the folder once Hugo picks a title.
set -euo pipefail
TOOLS="$(cd "$(dirname "$0")" && pwd)"; MAIN="$(git -C "$TOOLS" rev-parse --show-toplevel)"
DATE="${1:-$(date -d 'next friday' +%Y.%m.%d)}"
WT="$HOME/docs-$DATE"; BR="stream/$DATE"
[ -e "$WT" ] && { echo "$WT already exists"; exit 1; }
git -C "$MAIN" worktree add -b "$BR" "$WT" main
D="$WT/$DATE.untitled"; mkdir -p "$D"
cat > "$D/README.md" <<'EOF'
![thumbnail](thumbnail.jpg)

# Untitled

### Links

**YouTube:**

**X:**

**Slides:** [slides.html](slides.html)

### References
EOF
cat > "$D/inbox.md" <<'EOF'
# inbox

Drop links here during the week: X posts, Reddit threads, papers, project pages, launch posts, and a
word on why, if it helps. arXiv ids are picked up by sweep.py. Everything else is read by the research
agent.

EOF
printf '# Log: %s\n\nPhases: research rounds → review (Hugo) → deck rounds → polish → thumbnail → publish.\n' "$DATE" > "$D/log.md"
git -C "$WT" add "$D" && git -C "$WT" commit -qm "$DATE stream: scaffold"
cat <<EOF

  worktree  $WT   (branch $BR)
  folder    $D

  next:
    cd $WT
    stream/run.sh research $DATE          # sweep + analysis rounds, unattended
    stream/py review.py serve $D          # review page -> "Save & start deck"
                                          #   (runs deck rounds + thumbnail prompts unattended)
    stream/py finalize.py <folder> --fill-youtube --require-youtube   # before publishing
EOF

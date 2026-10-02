#!/usr/bin/env bash
# Builds the course's teaching repository at a named checkpoint.
#
#   course/demo-repo/build.sh [dir] [checkpoint]      default: /tmp/demo-repo, clean
#   course/demo-repo/build.sh --list                  the checkpoints
#
# Every episode names the checkpoint it starts from in its episode.yml (`checkpoint:`), so a
# viewer can follow along from exactly the same state: the history is deterministic
# (DEMO_EPOCH pins "now"), the working tree is what the checkpoint adds on top.
# A checkpoint is checkpoints/<name>.sh, run inside the repository with REPO set; its first
# comment line is its description.
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

if [[ ${1:-} == --list ]]; then
  for f in "$HERE"/checkpoints/*.sh; do
    printf '%-18s %s\n' "$(basename "$f" .sh)" "$(sed -n '2s/^# *//p' "$f")"
  done
  exit 0
fi

REPO=${1:-/tmp/demo-repo}
CHECKPOINT=${2:-clean}
SCRIPT="$HERE/checkpoints/$CHECKPOINT.sh"
[[ -f $SCRIPT ]] || { echo "build.sh: no checkpoint '$CHECKPOINT' (try --list)" >&2; exit 2; }

"$HERE/lumen-history.sh" "$REPO" >/dev/null
cd "$REPO"
REPO=$REPO bash "$SCRIPT"
echo "demo repo: $REPO at checkpoint '$CHECKPOINT' ($(git status --short | wc -l) changed paths)"

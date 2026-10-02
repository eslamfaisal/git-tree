# Demo repository

`build.sh [dir] [checkpoint]` builds the fictional **lumen** project (a Markdown notes tool: 44 commits, five authors, five branches, a tag, a bare origin) at a named checkpoint. The history is deterministic (`DEMO_EPOCH`), the checkpoint adds the working-tree state an episode starts from. `build.sh --list` shows them.

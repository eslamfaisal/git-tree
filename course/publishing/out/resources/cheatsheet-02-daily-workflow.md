# Commands: Daily workflow: stage, commit, review

| Command | Lesson |
|---|---|
| `git add -A -- <path>` | Stage a file in GitTree (git add explained) |
| `git status` | Stage a file in GitTree (git add explained) |
| `git add -p` | Stage a single hunk in GitTree (commit part of a file) |
| `git diff --staged` | Stage a single hunk in GitTree (commit part of a file) |
| `git add -p (then e to edit the hunk)` | Stage single lines in GitTree (partial commit) |
| `git apply --cached` | Stage single lines in GitTree (partial commit) |
| `git restore --staged -- <path>` | Unstage a file in GitTree (undo git add) |
| `git reset -q` | Unstage a file in GitTree (undo git add) |
| `git commit --no-edit -F - --cleanup=strip` | Make a Git commit in GitTree step by step |
| `git commit --amend` | Amend the last Git commit in GitTree |
| `git commit --signoff` | Git commit options: sign-off, skip hooks, other author |
| `git commit --no-verify` | Git commit options: sign-off, skip hooks, other author |
| `git commit -m "... Co-authored-by: Name <email>"` | Add co-authors to a Git commit in GitTree |
| `git commit` | Git commit hooks: read pre-commit output in GitTree |
| `git diff --cached --stat --patch -M` | Draft a Git commit message with your own AI agent CLI |
| `git restore --worktree -- <path>` | Discard changes to a file in GitTree (git restore) |
| `git apply -R` | Discard a single hunk in GitTree (undo part of a file) |
| `git restore --staged --worktree --source=HEAD -- .` | Discard all changes in a Git repository safely |
| `git check-ignore -v <path>` | Ignore a file, folder or extension in Git (.gitignore) |
| `git diff` | Git diff in GitTree: hunk, inline and side by side |
| `git diff --cached -M` | Git diff in GitTree: hunk, inline and side by side |
| `git diff -w` | Ignore whitespace in a Git diff and wrap long lines |
| `git cat-file -p <blob>` | Compare images in Git: side by side, swipe, onion skin |
| `git show <rev>:<path>` | View a file at any Git commit in GitTree |
| `git diff <a> <b>` | Compare two Git commits in GitTree (git diff A B) |
| `git restore --staged --worktree --source=<rev> -- <path>` | Restore a file from an old Git commit in GitTree |
| `git blame --incremental <path>` | Git blame: who changed this line? (GitTree blame view) |
| `git blame <commit>^ -- <path>` | Git blame before this commit: walk a line's history |
| `git log --follow -M -- <path>` | Git file history with renames (git log --follow) |
| `git status --porcelain=v2` | The WIP row in the Git graph: your uncommitted work |
| `git stash push` | Git stash in GitTree: save work in progress |
| `git stash pop` | Git stash pop in GitTree: bring your changes back |

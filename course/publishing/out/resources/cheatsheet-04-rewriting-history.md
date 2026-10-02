# Commands: Rewriting history and getting out of trouble

| Command | Lesson |
|---|---|
| `git rebase <onto>` | Git rebase explained: rebase a branch in GitTree |
| `git rebase --interactive <base>` | Git interactive rebase in GitTree (pick, squash, drop) |
| `git rebase -i (reword)` | Change a Git commit message after committing (reword) |
| `git rebase -i (drop)` | Remove a commit from Git history (drop a commit) |
| `git rebase -i (reorder)` | Reorder Git commits: move a commit up or down |
| `git rebase -i (squash)` | Squash Git commits into one in GitTree |
| `git rev-list <commits> --not --remotes` | Why rewriting pushed Git commits is risky |
| `git cherry-pick <sha>` | Git cherry-pick: copy a commit to another branch |
| `git revert --no-edit <sha>` | Git revert: undo a commit without rewriting history |
| `git reset --soft <sha>` | Git reset --soft: undo a commit but keep it staged |
| `git reset --mixed <sha>` | Git reset --mixed: undo a commit, keep the changes |
| `git reset --hard <sha>` | Git reset --hard in GitTree: discard commits safely |
| `git update-ref <ref> <old-sha> <expected-sha>` | Undo and redo Git operations in GitTree |
| `git for-each-ref refs/ogt/trash` | Git recovery snapshots: GitTree's refs/ogt/trash |
| `git update-ref -d <ref>` | Git recovery snapshots: GitTree's refs/ogt/trash |
| `git reflog` | Git reflog explained: see where HEAD has been |
| `git log --walk-reflogs` | Git reflog explained: see where HEAD has been |
| `git branch <name> <sha>` | Recover a lost Git commit with the reflog |
| `git bisect start <bad> <good>` | Git bisect: find the commit that introduced a bug |
| `git bisect good` | Git bisect: find the commit that introduced a bug |
| `git bisect bad` | Git bisect: find the commit that introduced a bug |
| `git bisect reset` | Git bisect: find the commit that introduced a bug |
| `git format-patch -1 <sha>` | Create a Git patch file from a commit (format-patch) |
| `git apply --index <patch>` | Apply a Git patch file: git apply vs git am |
| `git am <patch>` | Apply a Git patch file: git apply vs git am |

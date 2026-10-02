# Commands: Power features: worktrees, submodules, LFS, search

| Command | Lesson |
|---|---|
| `git worktree list --porcelain` | Git worktrees explained: see them in GitTree |
| `git worktree add [-b <new>] <path> <commit-ish>` | Create a Git worktree in GitTree (git worktree add) |
| `git worktree move` | Move, lock and remove a Git worktree |
| `git worktree lock` | Move, lock and remove a Git worktree |
| `git worktree remove` | Move, lock and remove a Git worktree |
| `git worktree prune` | Move, lock and remove a Git worktree |
| `git submodule status` | Git submodules explained: see them in GitTree |
| `git submodule add <url> <path>` | Add a Git submodule in GitTree |
| `git submodule update --init` | Update and remove a Git submodule in GitTree |
| `git submodule sync` | Update and remove a Git submodule in GitTree |
| `git rm <path>` | Update and remove a Git submodule in GitTree |
| `git lfs version` | Set up Git LFS for a repository in GitTree |
| `git lfs install --local` | Set up Git LFS for a repository in GitTree |
| `git lfs track <pattern>` | Track large files with Git LFS in GitTree |
| `git lfs untrack <pattern>` | Track large files with Git LFS in GitTree |
| `git lfs pull` | Download and prune Git LFS content in GitTree |
| `git lfs prune --dry-run --verbose` | Download and prune Git LFS content in GitTree |
| `git lfs locks` | Git LFS file locking in GitTree |
| `git lfs lock <path>` | Git LFS file locking in GitTree |
| `git lfs unlock <path>` | Git LFS file locking in GitTree |
| `git sparse-checkout set --cone --stdin` | Git sparse checkout in GitTree: only the folders you need |
| `git sparse-checkout disable` | Git sparse checkout in GitTree: only the folders you need |
| `git clone --depth N` | Shallow, sparse and blobless Git clones in GitTree |
| `git clone --filter=blob:none` | Shallow, sparse and blobless Git clones in GitTree |
| `git clone --sparse` | Shallow, sparse and blobless Git clones in GitTree |
| `git fetch --deepen N` | Shallow, sparse and blobless Git clones in GitTree |
| `git stash push -m <msg>` | Git stash options: untracked files, staged only, message |
| `git stash push --staged` | Git stash options: untracked files, staged only, message |
| `git stash push -u` | Git stash options: untracked files, staged only, message |
| `git stash branch <name> stash@{n}` | Create a Git branch from a stash in GitTree |
| `git stash drop stash@{n}` | Delete a Git stash and recover it from the snapshots |
| `git fsck` | Git repository maintenance in GitTree (fsck, gc) |
| `git commit-graph write` | Git repository maintenance in GitTree (fsck, gc) |
| `git gc` | Git repository maintenance in GitTree (fsck, gc) |
| `git count-objects` | Git repository maintenance in GitTree (fsck, gc) |
| `git log --all --grep <text>` | Search all Git history by message, author, file or change |
| `git log -S <text>` | Search all Git history by message, author, file or change |
| `git log -G <regex>` | Search all Git history by message, author, file or change |
| `git ls-files -z --cached --others --exclude-standard` | Find any file fast in GitTree (fuzzy file finder) |
| `git log --author <name> --since <date> -- <path>` | Filter the Git graph by author, date, branch or path |

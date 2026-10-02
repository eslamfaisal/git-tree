# Course proposal: Git Visually: Learn Git From Zero With GitTree

**Subtitle**: One short lesson per Git idea: see it on the commit graph, do it in the app, and learn the git command behind it.

## Audience

- Developers who use Git but only know a few commands and want to understand the rest
- Beginners starting Git for the first time
- Developers who prefer a visual client and want to know what happens underneath
- Team leads who want a shared, safe way to review, rebase and recover

## Prerequisites

- A computer with macOS, Windows or Linux (Ubuntu or Debian)
- Git 2.39 or newer installed (the first lessons show how)
- GitTree, which is free (https://gittree.app)
- No prior Git knowledge is needed

## Learning objectives

- Explain commits, branches, HEAD, the staging area and remotes in your own words
- Stage whole files, single hunks and individual lines, and write better commits
- Create, merge, rebase and delete branches without fear, and resolve conflicts
- Rewrite history safely with interactive rebase, and undo mistakes with Undo, the reflog and recovery snapshots
- Collaborate through remotes and pull requests, and force-push safely
- Use stash, worktrees, submodules and Git LFS
- Work faster with the command palette, shortcuts and custom commands
- Read the git command behind every action, so you can move between GitTree and the terminal

## Exercise files

- The practice repository: `https://github.com/eslamfaisal/git-tree/tree/main/course/demo-repo` (one start state per lecture)

## Outline

### Chapter 1: Start here: install, sign in, open a repository (47 min)

Install GitTree on your system, sign in, and open, clone or create your first repository.

- Install GitTree on macOS (Apple silicon and Intel) (4 min)
- Install GitTree on Windows 10 and 11 (4 min)
- Install GitTree on Ubuntu and Debian (.deb) (4 min)
- Run GitTree on Linux with the AppImage (no root) (3 min)
- Verify a GitTree Linux download with SHA256SUMS (3 min)
- Which Git version does GitTree need? (2.39 or newer) (3 min)
- Sign in to GitTree on first launch (website account) (4 min)
- Open a Git repository in GitTree (folder or drag and drop) (3 min)
- Trust this repository? What GitTree checks before it opens (4 min)
- Clone a Git repository by URL in GitTree (4 min)
- Create a new Git repository in GitTree (git init) (4 min)
- Recent repositories and the New Tab page in GitTree (3 min)
- GitTree window tour: sidebar, graph, inspector, drawer (4 min)

### Chapter 2: Git foundations: the ideas behind every click (58 min)

Understand the ideas every Git operation is built on, each shown with one feature of the app.

- What is a Git commit? See one in GitTree (5 min)
- The Git commit graph explained: history is a DAG (5 min)
- Git branches are just pointers (refs explained) (5 min)
- What is HEAD in Git? Find it in GitTree (4 min)
- Git working tree, index and HEAD: the three trees (6 min)
- Local vs remote branches in Git (origin/main explained) (5 min)
- What is a Git remote? Add, edit and remove one (5 min)
- Git tags explained: create a tag in GitTree (4 min)
- Git fetch explained: download without changing your files (4 min)
- What is a Git fast-forward? Move a branch pointer (4 min)
- Git merge vs rebase: the difference on the graph (6 min)
- Git config scopes: system, global and local explained (5 min)

### Chapter 3: Daily workflow: stage, commit, review (103 min)

Stage, commit, amend and review your work with confidence, and park work in progress.

- Stage a file in GitTree (git add explained) (3 min)
- Stage a single hunk in GitTree (commit part of a file) (3.5 min)
- Stage single lines in GitTree (partial commit) (4 min)
- Unstage a file in GitTree (undo git add) (3 min)
- Make a Git commit in GitTree step by step (3.5 min)
- Write better Git commit messages with GitTree hints (4 min)
- Amend the last Git commit in GitTree (4 min)
- Git commit options: sign-off, skip hooks, other author (5 min)
- Add co-authors to a Git commit in GitTree (3 min)
- Git commit hooks: read pre-commit output in GitTree (4 min)
- Draft a Git commit message with your own AI agent CLI (4 min)
- Discard changes to a file in GitTree (git restore) (4 min)
- Discard a single hunk in GitTree (undo part of a file) (3 min)
- Discard all changes in a Git repository safely (3 min)
- Ignore a file, folder or extension in Git (.gitignore) (3 min)
- Edit .gitignore and find out why a file is ignored (4 min)
- Git diff in GitTree: hunk, inline and side by side (4 min)
- Jump between changes in a Git diff (F7 and Shift+F7) (3 min)
- Ignore whitespace in a Git diff and wrap long lines (3 min)
- Compare images in Git: side by side, swipe, onion skin (3 min)
- View a file at any Git commit in GitTree (3 min)
- Compare two Git commits in GitTree (git diff A B) (4 min)
- Restore a file from an old Git commit in GitTree (3 min)
- Git blame: who changed this line? (GitTree blame view) (4 min)
- Git blame before this commit: walk a line's history (3 min)
- Git file history with renames (git log --follow) (3 min)
- The WIP row in the Git graph: your uncommitted work (3 min)
- Search Git history in GitTree (Ctrl+F in the graph) (3 min)
- Git stash in GitTree: save work in progress (3 min)
- Git stash pop in GitTree: bring your changes back (3 min)

### Chapter 4: Branching and merging (77 min)

Branch, tag, merge and resolve conflicts, and run a Gitflow release.

- Create a Git branch in GitTree (4 min)
- Switch Git branches in GitTree (git switch) (5 min)
- Check out a remote Git branch and track it (3 min)
- Rename a Git branch in GitTree (3 min)
- Delete a Git branch safely in GitTree (3 min)
- Set the upstream branch in Git (tracking explained) (3 min)
- Create an annotated Git tag in GitTree (3 min)
- Delete a Git tag locally and on the remote (3 min)
- Preview a Git merge for conflicts before you merge (4 min)
- Merge a Git branch in GitTree (merge commit) (5 min)
- Git squash merge: combine a branch into one commit (4 min)
- Git merge in progress: the operation banner in GitTree (4 min)
- Abort a Git merge or rebase and go back to before (3 min)
- Merge conflicts in Git: find the conflicted files (4 min)
- Resolve a Git merge conflict in GitTree's merge view (6 min)
- Resolve a Git conflict by taking one whole side (4 min)
- Use an external merge tool for Git conflicts (4 min)
- Git flow in GitTree: initialise the branching model (4 min)
- Git flow: start and finish a feature branch (5 min)
- Predict Git merge conflicts before they happen (3 min)

### Chapter 5: Rewriting history and getting out of trouble (76 min)

Rebase, cherry-pick, revert and reset on purpose, and recover from any mistake.

- Git rebase explained: rebase a branch in GitTree (5 min)
- Git interactive rebase in GitTree (pick, squash, drop) (7 min)
- Change a Git commit message after committing (reword) (3 min)
- Remove a commit from Git history (drop a commit) (3 min)
- Reorder Git commits: move a commit up or down (3 min)
- Squash Git commits into one in GitTree (3 min)
- Why rewriting pushed Git commits is risky (4 min)
- Git cherry-pick: copy a commit to another branch (4 min)
- Git revert: undo a commit without rewriting history (4 min)
- Git reset --soft: undo a commit but keep it staged (3 min)
- Git reset --mixed: undo a commit, keep the changes (3 min)
- Git reset --hard in GitTree: discard commits safely (4 min)
- Undo and redo Git operations in GitTree (5 min)
- Git recovery snapshots: GitTree's refs/ogt/trash (4 min)
- Git reflog explained: see where HEAD has been (4 min)
- Recover a lost Git commit with the reflog (4 min)
- Git bisect: find the commit that introduced a bug (6 min)
- Create a Git patch file from a commit (format-patch) (3 min)
- Apply a Git patch file: git apply vs git am (4 min)

### Chapter 6: Collaboration: remotes, pull requests, providers (113 min)

Share work through remotes, pull requests and hosting providers, and push safely.

- Git push in GitTree: send your commits to a remote (5 min)
- Check where a Git push will go before you push (3 min)
- Git pull --ff-only in GitTree (3 min)
- Git pull: fast-forward if possible, else merge (4 min)
- Git pull --rebase in GitTree (4 min)
- Choose your default Git pull mode in GitTree (3 min)
- Git push rejected (non-fast-forward): how to fix it (5 min)
- Git force push with lease: the safe way in GitTree (5 min)
- Delete a remote Git branch from GitTree (3 min)
- Push a Git tag to the remote in GitTree (3 min)
- Git auto-fetch: keep remote branches up to date (3 min)
- Connect GitHub to GitTree (browser sign-in or token) (5 min)
- Connect GitHub Enterprise Server to GitTree (4 min)
- Connect GitLab to GitTree (token or application ID) (4 min)
- Connect Bitbucket Cloud to GitTree (4 min)
- Connect Azure DevOps to GitTree (personal access token) (4 min)
- Connect Bitbucket Data Center to GitTree (4 min)
- Clone a repository from your hosting account in GitTree (4 min)
- Publish a local Git repository to a host from GitTree (4 min)
- Create a pull request from GitTree (5 min)
- Check out a pull request branch locally in GitTree (4 min)
- Review pull request files and diffs in GitTree (4 min)
- Comment on and resolve pull request threads in GitTree (4 min)
- See pull request checks and re-run them in GitTree (3 min)
- Review a pull request: approve or request changes (4 min)
- Merge a pull request: merge, squash or rebase (4 min)
- See issues and start a branch from one in GitTree (4 min)
- Create an issue from GitTree (3 min)
- Git fork workflow: add a remote from a fork in GitTree (4 min)

### Chapter 7: Power features: worktrees, submodules, LFS, search (107 min)

Use worktrees, submodules, LFS, search and the terminal to handle bigger projects.

- Git worktrees explained: see them in GitTree (4 min)
- Create a Git worktree in GitTree (git worktree add) (4 min)
- Move, lock and remove a Git worktree (5 min)
- Git submodules explained: see them in GitTree (4 min)
- Add a Git submodule in GitTree (4 min)
- Update and remove a Git submodule in GitTree (5 min)
- Set up Git LFS for a repository in GitTree (4 min)
- Track large files with Git LFS in GitTree (4 min)
- Download and prune Git LFS content in GitTree (4 min)
- Git LFS file locking in GitTree (3 min)
- Git sparse checkout in GitTree: only the folders you need (4 min)
- Shallow, sparse and blobless Git clones in GitTree (6 min)
- Git stash options: untracked files, staged only, message (4 min)
- Create a Git branch from a stash in GitTree (3 min)
- Delete a Git stash and recover it from the snapshots (3 min)
- Git repository maintenance in GitTree (fsck, gc) (5 min)
- Group repositories into workspaces in GitTree (4 min)
- Work in several repositories with tabs in GitTree (4 min)
- The GitTree command palette: run anything from the keyboard (5 min)
- Search all Git history by message, author, file or change (5 min)
- Find any file fast in GitTree (fuzzy file finder) (3 min)
- The integrated terminal in GitTree (4 min)
- Define custom commands in GitTree (programs with tokens) (5 min)
- Run a custom command from the GitTree toolbar (3 min)
- Filter the Git graph by author, date, branch or path (4 min)
- See all your pull requests across a workspace (4 min)

### Chapter 8: Customise GitTree and fix problems (79 min)

Make GitTree fit the way you work and fix the problems people hit most.

- GitTree Preferences: search, scopes and reset (4 min)
- Change the GitTree theme: dark, light, high contrast (3 min)
- Zoom, date format and reduced motion in GitTree (4 min)
- Git profiles in GitTree: work and personal identities (5 min)
- SSH keys in GitTree: generate, copy and test (5 min)
- SSH host key and username prompts in GitTree (4 min)
- Sign Git commits in GitTree (OpenPGP, SSH, S/MIME) (5 min)
- Set an external diff tool, merge tool and editor (4 min)
- GitTree keyboard shortcuts: the cheat sheet (3 min)
- Customise keyboard shortcuts in GitTree (4 min)
- See the exact Git commands GitTree runs (Activity Log) (4 min)
- Report a bug or a crash from GitTree (3 min)
- Update GitTree: check for updates, download and install (4 min)
- GitTree startup screens: update, offline, maintenance (5 min)
- Sign out of GitTree everywhere (3 min)
- Restricted mode in GitTree: open untrusted repos safely (4 min)
- Where GitTree stores your tokens (system keychain) (4 min)
- Linux keyring for GitTree: Secret Service setup (4 min)
- Import a custom theme into GitTree (3 min)
- Export, import and reset GitTree settings (4 min)

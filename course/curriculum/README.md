# Curriculum

One folder per episode, grouped by series (see `../ARCHITECTURE.md` for the format of `episode.yml` and `beats.yml`). The plan is `../curriculum.yml`; `tooling/scaffold_episodes.py` creates the folders, `tooling/generate_index.py` rebuilds this table.

<!-- episodes:begin -->
| Episode | Series | Status | Watch |
|---|---|---|---|
| [00-01 · Install GitTree on macOS (Apple silicon and Intel)](curriculum/00-start-here/install-gittree-on-macos/) | start here | planned | not yet published |
| [00-02 · Install GitTree on Windows 10 and 11](curriculum/00-start-here/install-gittree-on-windows/) | start here | planned | not yet published |
| [00-03 · Install GitTree on Ubuntu and Debian (.deb)](curriculum/00-start-here/install-gittree-on-ubuntu-debian/) | start here | planned | not yet published |
| [00-04 · Run GitTree on Linux with the AppImage (no root)](curriculum/00-start-here/run-gittree-appimage/) | start here | planned | not yet published |
| [00-05 · Verify a GitTree Linux download with SHA256SUMS](curriculum/00-start-here/verify-linux-download/) | start here | planned | not yet published |
| [00-06 · Which Git version does GitTree need? (2.39 or newer)](curriculum/00-start-here/git-version-required/) | start here | planned | not yet published |
| [00-07 · Sign in to GitTree on first launch (website account)](curriculum/00-start-here/sign-in-first-launch/) | start here | planned | not yet published |
| [00-08 · Open a Git repository in GitTree (folder or drag and drop)](curriculum/00-start-here/open-a-repository/) | start here | planned | not yet published |
| [00-09 · Trust this repository? What GitTree checks before it opens](curriculum/00-start-here/trust-prompt-on-open/) | start here | planned | not yet published |
| [00-10 · Clone a Git repository by URL in GitTree](curriculum/00-start-here/clone-a-repository/) | start here | planned | not yet published |
| [00-11 · Create a new Git repository in GitTree (git init)](curriculum/00-start-here/init-a-repository/) | start here | planned | not yet published |
| [00-12 · Recent repositories and the New Tab page in GitTree](curriculum/00-start-here/recent-repositories/) | start here | planned | not yet published |
| [00-13 · GitTree window tour: sidebar, graph, inspector, drawer](curriculum/00-start-here/tour-of-the-window/) | start here | planned | not yet published |
| [01-01 · What is a Git commit? See one in GitTree](curriculum/01-git-foundations/what-is-a-commit/) | git foundations | planned | not yet published |
| [01-02 · The Git commit graph explained: history is a DAG](curriculum/01-git-foundations/commit-graph-dag/) | git foundations | planned | not yet published |
| [01-03 · Git branches are just pointers (refs explained)](curriculum/01-git-foundations/branches-are-pointers/) | git foundations | planned | not yet published |
| [01-04 · What is HEAD in Git? Find it in GitTree](curriculum/01-git-foundations/what-is-head/) | git foundations | planned | not yet published |
| [01-05 · Git working tree, index and HEAD: the three trees](curriculum/01-git-foundations/three-trees-and-the-index/) | git foundations | planned | not yet published |
| [01-06 · Local vs remote branches in Git (origin/main explained)](curriculum/01-git-foundations/local-vs-remote-branches/) | git foundations | planned | not yet published |
| [01-07 · What is a Git remote? Add, edit and remove one](curriculum/01-git-foundations/what-is-a-remote/) | git foundations | planned | not yet published |
| [01-08 · Git tags explained: create a tag in GitTree](curriculum/01-git-foundations/git-tags-explained/) | git foundations | planned | not yet published |
| [01-09 · Git fetch explained: download without changing your files](curriculum/01-git-foundations/fetch-without-changing-files/) | git foundations | planned | not yet published |
| [01-10 · What is a Git fast-forward? Move a branch pointer](curriculum/01-git-foundations/what-is-a-fast-forward/) | git foundations | planned | not yet published |
| [01-11 · Git merge vs rebase: the difference on the graph](curriculum/01-git-foundations/merge-vs-rebase/) | git foundations | planned | not yet published |
| [01-12 · Git config scopes: system, global and local explained](curriculum/01-git-foundations/git-config-scopes/) | git foundations | planned | not yet published |
| [02-01 · Stage a file in GitTree (git add explained)](curriculum/02-daily-workflow/stage-a-file/) | daily workflow | planned | not yet published |
| [02-02 · Stage a single hunk in GitTree (commit part of a file)](curriculum/02-daily-workflow/stage-a-single-hunk/) | daily workflow | scripted | not yet published |
| [02-03 · Stage single lines in GitTree (partial commit)](curriculum/02-daily-workflow/stage-single-lines/) | daily workflow | planned | not yet published |
| [02-04 · Unstage a file in GitTree (undo git add)](curriculum/02-daily-workflow/unstage-a-file/) | daily workflow | planned | not yet published |
| [02-05 · Make a Git commit in GitTree step by step](curriculum/02-daily-workflow/make-a-commit/) | daily workflow | planned | not yet published |
| [02-06 · Write better Git commit messages with GitTree hints](curriculum/02-daily-workflow/commit-message-hints/) | daily workflow | planned | not yet published |
| [02-07 · Amend the last Git commit in GitTree](curriculum/02-daily-workflow/amend-last-commit/) | daily workflow | planned | not yet published |
| [02-08 · Git commit options: sign-off, skip hooks, other author](curriculum/02-daily-workflow/commit-options/) | daily workflow | planned | not yet published |
| [02-09 · Add co-authors to a Git commit in GitTree](curriculum/02-daily-workflow/add-co-authors/) | daily workflow | planned | not yet published |
| [02-10 · Git commit hooks: read pre-commit output in GitTree](curriculum/02-daily-workflow/commit-hook-output/) | daily workflow | planned | not yet published |
| [02-11 · Draft a Git commit message with your own AI agent CLI](curriculum/02-daily-workflow/draft-commit-message-with-ai-agent/) | daily workflow | planned | not yet published |
| [02-12 · Discard changes to a file in GitTree (git restore)](curriculum/02-daily-workflow/discard-file-changes/) | daily workflow | planned | not yet published |
| [02-13 · Discard a single hunk in GitTree (undo part of a file)](curriculum/02-daily-workflow/discard-a-single-hunk/) | daily workflow | planned | not yet published |
| [02-14 · Discard all changes in a Git repository safely](curriculum/02-daily-workflow/discard-all-changes/) | daily workflow | planned | not yet published |
| [02-15 · Ignore a file, folder or extension in Git (.gitignore)](curriculum/02-daily-workflow/ignore-files-folders-extensions/) | daily workflow | planned | not yet published |
| [02-16 · Edit .gitignore and find out why a file is ignored](curriculum/02-daily-workflow/edit-gitignore/) | daily workflow | planned | not yet published |
| [02-17 · Git diff in GitTree: hunk, inline and side by side](curriculum/02-daily-workflow/diff-view-modes/) | daily workflow | planned | not yet published |
| [02-18 · Jump between changes in a Git diff (F7 and Shift+F7)](curriculum/02-daily-workflow/jump-between-changes/) | daily workflow | planned | not yet published |
| [02-19 · Ignore whitespace in a Git diff and wrap long lines](curriculum/02-daily-workflow/diff-display-options/) | daily workflow | planned | not yet published |
| [02-20 · Compare images in Git: side by side, swipe, onion skin](curriculum/02-daily-workflow/compare-images/) | daily workflow | planned | not yet published |
| [02-21 · View a file at any Git commit in GitTree](curriculum/02-daily-workflow/view-file-at-a-commit/) | daily workflow | planned | not yet published |
| [02-22 · Compare two Git commits in GitTree (git diff A B)](curriculum/02-daily-workflow/compare-two-commits/) | daily workflow | planned | not yet published |
| [02-23 · Restore a file from an old Git commit in GitTree](curriculum/02-daily-workflow/restore-file-from-commit/) | daily workflow | planned | not yet published |
| [02-24 · Git blame: who changed this line? (GitTree blame view)](curriculum/02-daily-workflow/git-blame/) | daily workflow | planned | not yet published |
| [02-25 · Git blame before this commit: walk a line's history](curriculum/02-daily-workflow/blame-before-this-commit/) | daily workflow | planned | not yet published |
| [02-26 · Git file history with renames (git log --follow)](curriculum/02-daily-workflow/file-history/) | daily workflow | planned | not yet published |
| [02-27 · The WIP row in the Git graph: your uncommitted work](curriculum/02-daily-workflow/the-wip-row/) | daily workflow | planned | not yet published |
| [02-28 · Search Git history in GitTree (Ctrl+F in the graph)](curriculum/02-daily-workflow/search-the-graph/) | daily workflow | planned | not yet published |
| [02-29 · Git stash in GitTree: save work in progress](curriculum/02-daily-workflow/stash-your-changes/) | daily workflow | planned | not yet published |
| [02-30 · Git stash pop in GitTree: bring your changes back](curriculum/02-daily-workflow/stash-pop/) | daily workflow | planned | not yet published |
| [03-01 · Create a Git branch in GitTree](curriculum/03-branching-and-merging/create-a-branch/) | branching and merging | planned | not yet published |
| [03-02 · Switch Git branches in GitTree (git switch)](curriculum/03-branching-and-merging/switch-branches/) | branching and merging | planned | not yet published |
| [03-03 · Check out a remote Git branch and track it](curriculum/03-branching-and-merging/check-out-remote-branch/) | branching and merging | planned | not yet published |
| [03-04 · Rename a Git branch in GitTree](curriculum/03-branching-and-merging/rename-a-branch/) | branching and merging | planned | not yet published |
| [03-05 · Delete a Git branch safely in GitTree](curriculum/03-branching-and-merging/delete-a-branch/) | branching and merging | planned | not yet published |
| [03-06 · Set the upstream branch in Git (tracking explained)](curriculum/03-branching-and-merging/set-upstream/) | branching and merging | planned | not yet published |
| [03-07 · Create an annotated Git tag in GitTree](curriculum/03-branching-and-merging/annotated-tag/) | branching and merging | planned | not yet published |
| [03-08 · Delete a Git tag locally and on the remote](curriculum/03-branching-and-merging/delete-a-tag/) | branching and merging | planned | not yet published |
| [03-09 · Preview a Git merge for conflicts before you merge](curriculum/03-branching-and-merging/preview-a-merge/) | branching and merging | planned | not yet published |
| [03-10 · Merge a Git branch in GitTree (merge commit)](curriculum/03-branching-and-merging/merge-a-branch/) | branching and merging | planned | not yet published |
| [03-11 · Git squash merge: combine a branch into one commit](curriculum/03-branching-and-merging/squash-merge/) | branching and merging | planned | not yet published |
| [03-12 · Git merge in progress: the operation banner in GitTree](curriculum/03-branching-and-merging/merge-in-progress-banner/) | branching and merging | planned | not yet published |
| [03-13 · Abort a Git merge or rebase and go back to before](curriculum/03-branching-and-merging/abort-merge-or-rebase/) | branching and merging | planned | not yet published |
| [03-14 · Merge conflicts in Git: find the conflicted files](curriculum/03-branching-and-merging/list-conflicted-files/) | branching and merging | planned | not yet published |
| [03-15 · Resolve a Git merge conflict in GitTree's merge view](curriculum/03-branching-and-merging/resolve-conflict-merge-view/) | branching and merging | planned | not yet published |
| [03-16 · Resolve a Git conflict by taking one whole side](curriculum/03-branching-and-merging/take-whole-side/) | branching and merging | planned | not yet published |
| [03-17 · Use an external merge tool for Git conflicts](curriculum/03-branching-and-merging/external-merge-tool/) | branching and merging | planned | not yet published |
| [03-18 · Git flow in GitTree: initialise the branching model](curriculum/03-branching-and-merging/gitflow-initialise/) | branching and merging | planned | not yet published |
| [03-19 · Git flow: start and finish a feature branch](curriculum/03-branching-and-merging/gitflow-feature/) | branching and merging | planned | not yet published |
| [03-20 · Predict Git merge conflicts before they happen](curriculum/03-branching-and-merging/conflict-early-warning/) | branching and merging | planned | not yet published |
| [04-01 · Git rebase explained: rebase a branch in GitTree](curriculum/04-rewriting-history/rebase-a-branch/) | rewriting history | planned | not yet published |
| [04-02 · Git interactive rebase in GitTree (pick, squash, drop)](curriculum/04-rewriting-history/interactive-rebase/) | rewriting history | planned | not yet published |
| [04-03 · Change a Git commit message after committing (reword)](curriculum/04-rewriting-history/reword-a-commit/) | rewriting history | planned | not yet published |
| [04-04 · Remove a commit from Git history (drop a commit)](curriculum/04-rewriting-history/drop-a-commit/) | rewriting history | planned | not yet published |
| [04-05 · Reorder Git commits: move a commit up or down](curriculum/04-rewriting-history/reorder-commits/) | rewriting history | planned | not yet published |
| [04-06 · Squash Git commits into one in GitTree](curriculum/04-rewriting-history/squash-commits/) | rewriting history | planned | not yet published |
| [04-07 · Why rewriting pushed Git commits is risky](curriculum/04-rewriting-history/rewriting-pushed-commits/) | rewriting history | planned | not yet published |
| [04-08 · Git cherry-pick: copy a commit to another branch](curriculum/04-rewriting-history/cherry-pick/) | rewriting history | planned | not yet published |
| [04-09 · Git revert: undo a commit without rewriting history](curriculum/04-rewriting-history/revert-a-commit/) | rewriting history | planned | not yet published |
| [04-10 · Git reset --soft: undo a commit but keep it staged](curriculum/04-rewriting-history/reset-soft/) | rewriting history | planned | not yet published |
| [04-11 · Git reset --mixed: undo a commit, keep the changes](curriculum/04-rewriting-history/reset-mixed/) | rewriting history | planned | not yet published |
| [04-12 · Git reset --hard in GitTree: discard commits safely](curriculum/04-rewriting-history/reset-hard/) | rewriting history | planned | not yet published |
| [04-13 · Undo and redo Git operations in GitTree](curriculum/04-rewriting-history/undo-and-redo/) | rewriting history | planned | not yet published |
| [04-14 · Git recovery snapshots: GitTree's refs/ogt/trash](curriculum/04-rewriting-history/recovery-snapshots/) | rewriting history | planned | not yet published |
| [04-15 · Git reflog explained: see where HEAD has been](curriculum/04-rewriting-history/reflog/) | rewriting history | planned | not yet published |
| [04-16 · Recover a lost Git commit with the reflog](curriculum/04-rewriting-history/recover-with-reflog/) | rewriting history | planned | not yet published |
| [04-17 · Git bisect: find the commit that introduced a bug](curriculum/04-rewriting-history/bisect/) | rewriting history | planned | not yet published |
| [04-18 · Create a Git patch file from a commit (format-patch)](curriculum/04-rewriting-history/create-a-patch/) | rewriting history | planned | not yet published |
| [04-19 · Apply a Git patch file: git apply vs git am](curriculum/04-rewriting-history/apply-a-patch/) | rewriting history | planned | not yet published |
| [05-01 · Git push in GitTree: send your commits to a remote](curriculum/05-collaboration/push/) | collaboration | planned | not yet published |
| [05-02 · Check where a Git push will go before you push](curriculum/05-collaboration/push-destination-check/) | collaboration | planned | not yet published |
| [05-03 · Git pull --ff-only in GitTree](curriculum/05-collaboration/pull-fast-forward-only/) | collaboration | planned | not yet published |
| [05-04 · Git pull: fast-forward if possible, else merge](curriculum/05-collaboration/pull-merge/) | collaboration | planned | not yet published |
| [05-05 · Git pull --rebase in GitTree](curriculum/05-collaboration/pull-rebase/) | collaboration | planned | not yet published |
| [05-06 · Choose your default Git pull mode in GitTree](curriculum/05-collaboration/default-pull-mode/) | collaboration | planned | not yet published |
| [05-07 · Git push rejected (non-fast-forward): how to fix it](curriculum/05-collaboration/push-rejected/) | collaboration | planned | not yet published |
| [05-08 · Git force push with lease: the safe way in GitTree](curriculum/05-collaboration/force-push-with-lease/) | collaboration | planned | not yet published |
| [05-09 · Delete a remote Git branch from GitTree](curriculum/05-collaboration/delete-remote-branch/) | collaboration | planned | not yet published |
| [05-10 · Push a Git tag to the remote in GitTree](curriculum/05-collaboration/push-a-tag/) | collaboration | planned | not yet published |
| [05-11 · Git auto-fetch: keep remote branches up to date](curriculum/05-collaboration/auto-fetch/) | collaboration | planned | not yet published |
| [05-12 · Connect GitHub to GitTree (browser sign-in or token)](curriculum/05-collaboration/connect-github/) | collaboration | planned | not yet published |
| [05-13 · Connect GitHub Enterprise Server to GitTree](curriculum/05-collaboration/connect-github-enterprise/) | collaboration | planned | not yet published |
| [05-14 · Connect GitLab to GitTree (token or application ID)](curriculum/05-collaboration/connect-gitlab/) | collaboration | planned | not yet published |
| [05-15 · Connect Bitbucket Cloud to GitTree](curriculum/05-collaboration/connect-bitbucket-cloud/) | collaboration | planned | not yet published |
| [05-16 · Connect Azure DevOps to GitTree (personal access token)](curriculum/05-collaboration/connect-azure-devops/) | collaboration | planned | not yet published |
| [05-17 · Connect Bitbucket Data Center to GitTree](curriculum/05-collaboration/connect-bitbucket-data-center/) | collaboration | planned | not yet published |
| [05-18 · Clone a repository from your hosting account in GitTree](curriculum/05-collaboration/clone-from-provider/) | collaboration | planned | not yet published |
| [05-19 · Publish a local Git repository to a host from GitTree](curriculum/05-collaboration/publish-repository/) | collaboration | planned | not yet published |
| [05-20 · Create a pull request from GitTree](curriculum/05-collaboration/create-pull-request/) | collaboration | planned | not yet published |
| [05-21 · Check out a pull request branch locally in GitTree](curriculum/05-collaboration/check-out-pull-request/) | collaboration | planned | not yet published |
| [05-22 · Review pull request files and diffs in GitTree](curriculum/05-collaboration/pull-request-files/) | collaboration | planned | not yet published |
| [05-23 · Comment on and resolve pull request threads in GitTree](curriculum/05-collaboration/pull-request-conversation/) | collaboration | planned | not yet published |
| [05-24 · See pull request checks and re-run them in GitTree](curriculum/05-collaboration/pull-request-checks/) | collaboration | planned | not yet published |
| [05-25 · Review a pull request: approve or request changes](curriculum/05-collaboration/review-pull-request/) | collaboration | planned | not yet published |
| [05-26 · Merge a pull request: merge, squash or rebase](curriculum/05-collaboration/merge-pull-request/) | collaboration | planned | not yet published |
| [05-27 · See issues and start a branch from one in GitTree](curriculum/05-collaboration/issues-list-and-branch/) | collaboration | planned | not yet published |
| [05-28 · Create an issue from GitTree](curriculum/05-collaboration/create-an-issue/) | collaboration | planned | not yet published |
| [05-29 · Git fork workflow: add a remote from a fork in GitTree](curriculum/05-collaboration/fork-remote/) | collaboration | planned | not yet published |
| [06-01 · Git worktrees explained: see them in GitTree](curriculum/06-power-features/worktrees-list/) | power features | planned | not yet published |
| [06-02 · Create a Git worktree in GitTree (git worktree add)](curriculum/06-power-features/create-a-worktree/) | power features | planned | not yet published |
| [06-03 · Move, lock and remove a Git worktree](curriculum/06-power-features/manage-worktrees/) | power features | planned | not yet published |
| [06-04 · Git submodules explained: see them in GitTree](curriculum/06-power-features/submodules-list/) | power features | planned | not yet published |
| [06-05 · Add a Git submodule in GitTree](curriculum/06-power-features/add-a-submodule/) | power features | planned | not yet published |
| [06-06 · Update and remove a Git submodule in GitTree](curriculum/06-power-features/update-and-remove-submodule/) | power features | planned | not yet published |
| [06-07 · Set up Git LFS for a repository in GitTree](curriculum/06-power-features/lfs-set-up/) | power features | planned | not yet published |
| [06-08 · Track large files with Git LFS in GitTree](curriculum/06-power-features/lfs-track/) | power features | planned | not yet published |
| [06-09 · Download and prune Git LFS content in GitTree](curriculum/06-power-features/lfs-content/) | power features | planned | not yet published |
| [06-10 · Git LFS file locking in GitTree](curriculum/06-power-features/lfs-locks/) | power features | planned | not yet published |
| [06-11 · Git sparse checkout in GitTree: only the folders you need](curriculum/06-power-features/sparse-checkout/) | power features | planned | not yet published |
| [06-12 · Shallow, sparse and blobless Git clones in GitTree](curriculum/06-power-features/shallow-sparse-blobless-clone/) | power features | planned | not yet published |
| [06-13 · Git stash options: untracked files, staged only, message](curriculum/06-power-features/stash-with-options/) | power features | planned | not yet published |
| [06-14 · Create a Git branch from a stash in GitTree](curriculum/06-power-features/branch-from-stash/) | power features | planned | not yet published |
| [06-15 · Delete a Git stash and recover it from the snapshots](curriculum/06-power-features/delete-a-stash/) | power features | planned | not yet published |
| [06-16 · Git repository maintenance in GitTree (fsck, gc)](curriculum/06-power-features/repository-maintenance/) | power features | planned | not yet published |
| [06-17 · Group repositories into workspaces in GitTree](curriculum/06-power-features/workspaces/) | power features | planned | not yet published |
| [06-18 · Work in several repositories with tabs in GitTree](curriculum/06-power-features/repo-tabs/) | power features | planned | not yet published |
| [06-19 · The GitTree command palette: run anything from the keyboard](curriculum/06-power-features/command-palette/) | power features | planned | not yet published |
| [06-20 · Search all Git history by message, author, file or change](curriculum/06-power-features/deep-commit-search/) | power features | planned | not yet published |
| [06-21 · Find any file fast in GitTree (fuzzy file finder)](curriculum/06-power-features/fuzzy-file-finder/) | power features | planned | not yet published |
| [06-22 · The integrated terminal in GitTree](curriculum/06-power-features/integrated-terminal/) | power features | planned | not yet published |
| [06-23 · Define custom commands in GitTree (programs with tokens)](curriculum/06-power-features/custom-commands-define/) | power features | planned | not yet published |
| [06-24 · Run a custom command from the GitTree toolbar](curriculum/06-power-features/custom-commands-run/) | power features | planned | not yet published |
| [06-25 · Filter the Git graph by author, date, branch or path](curriculum/06-power-features/filter-the-graph/) | power features | planned | not yet published |
| [06-26 · See all your pull requests across a workspace](curriculum/06-power-features/pull-request-dashboard/) | power features | planned | not yet published |
| [07-01 · GitTree Preferences: search, scopes and reset](curriculum/07-customise-and-troubleshoot/preferences-window/) | customise and troubleshoot | planned | not yet published |
| [07-02 · Change the GitTree theme: dark, light, high contrast](curriculum/07-customise-and-troubleshoot/themes/) | customise and troubleshoot | planned | not yet published |
| [07-04 · Zoom, date format and reduced motion in GitTree](curriculum/07-customise-and-troubleshoot/zoom-dates-motion/) | customise and troubleshoot | planned | not yet published |
| [07-05 · Git profiles in GitTree: work and personal identities](curriculum/07-customise-and-troubleshoot/git-profiles/) | customise and troubleshoot | planned | not yet published |
| [07-06 · SSH keys in GitTree: generate, copy and test](curriculum/07-customise-and-troubleshoot/ssh-keys/) | customise and troubleshoot | planned | not yet published |
| [07-07 · SSH host key and username prompts in GitTree](curriculum/07-customise-and-troubleshoot/ssh-host-key-prompts/) | customise and troubleshoot | planned | not yet published |
| [07-08 · Sign Git commits in GitTree (OpenPGP, SSH, S/MIME)](curriculum/07-customise-and-troubleshoot/sign-commits/) | customise and troubleshoot | planned | not yet published |
| [07-09 · Set an external diff tool, merge tool and editor](curriculum/07-customise-and-troubleshoot/external-tools/) | customise and troubleshoot | planned | not yet published |
| [07-10 · GitTree keyboard shortcuts: the cheat sheet](curriculum/07-customise-and-troubleshoot/keyboard-shortcuts-cheat-sheet/) | customise and troubleshoot | planned | not yet published |
| [07-11 · Customise keyboard shortcuts in GitTree](curriculum/07-customise-and-troubleshoot/customise-shortcuts/) | customise and troubleshoot | planned | not yet published |
| [07-12 · See the exact Git commands GitTree runs (Activity Log)](curriculum/07-customise-and-troubleshoot/activity-log/) | customise and troubleshoot | planned | not yet published |
| [07-13 · Report a bug or a crash from GitTree](curriculum/07-customise-and-troubleshoot/report-a-bug/) | customise and troubleshoot | planned | not yet published |
| [07-14 · Update GitTree: check for updates, download and install](curriculum/07-customise-and-troubleshoot/check-for-updates/) | customise and troubleshoot | planned | not yet published |
| [07-15 · GitTree startup screens: update, offline, maintenance](curriculum/07-customise-and-troubleshoot/startup-screens/) | customise and troubleshoot | planned | not yet published |
| [07-16 · Sign out of GitTree everywhere](curriculum/07-customise-and-troubleshoot/sign-out/) | customise and troubleshoot | planned | not yet published |
| [07-17 · Restricted mode in GitTree: open untrusted repos safely](curriculum/07-customise-and-troubleshoot/restricted-mode/) | customise and troubleshoot | planned | not yet published |
| [07-18 · Where GitTree stores your tokens (system keychain)](curriculum/07-customise-and-troubleshoot/where-tokens-live/) | customise and troubleshoot | planned | not yet published |
| [07-19 · Linux keyring for GitTree: Secret Service setup](curriculum/07-customise-and-troubleshoot/linux-secret-service/) | customise and troubleshoot | planned | not yet published |
| [07-20 · Import a custom theme into GitTree](curriculum/07-customise-and-troubleshoot/import-a-theme/) | customise and troubleshoot | planned | not yet published |
| [07-21 · Export, import and reset GitTree settings](curriculum/07-customise-and-troubleshoot/settings-backup/) | customise and troubleshoot | planned | not yet published |
<!-- episodes:end -->

# Curriculum

## Section 1: Start here: install, sign in, open a repository

*Install GitTree on your system, sign in, and open, clone or create your first repository.*

### 1.1 Install GitTree on macOS (Apple silicon and Intel)
4 min · 00-01 · planned

Install the universal GitTree disk image on a Mac and get past the first-launch warning.

### 1.2 Install GitTree on Windows 10 and 11
4 min · 00-02 · planned

Run the GitTree setup on Windows and get past the SmartScreen warning.

### 1.3 Install GitTree on Ubuntu and Debian (.deb)
4 min · 00-03 · planned

Install the .deb package with apt and start GitTree from the menu.

### 1.4 Run GitTree on Linux with the AppImage (no root)
3 min · 00-04 · planned

Make the AppImage executable and run GitTree without installing anything.

### 1.5 Verify a GitTree Linux download with SHA256SUMS
3 min · 00-05 · planned

Check that a downloaded installer matches the checksum published with the release.

### 1.6 Which Git version does GitTree need? (2.39 or newer)
3 min · 00-06 · planned

Check your Git version and read the two screens GitTree shows when Git is missing or too old.

### 1.7 Sign in to GitTree on first launch (website account)
4 min · 00-07 · planned

Sign in through the GitTree website from the app, including the manual code fallback.

### 1.8 Open a Git repository in GitTree (folder or drag and drop)
3 min · 00-08 · planned

Open an existing repository from the New Tab page, the Open shortcut or a dropped folder.

### 1.9 Trust this repository? What GitTree checks before it opens
4 min · 00-09 · planned

Read the trust prompt and choose between Restricted Mode and Trust and Open.

### 1.10 Clone a Git repository by URL in GitTree
4 min · 00-10 · planned

Clone a repository from a URL into a folder you choose and open it.

### 1.11 Create a new Git repository in GitTree (git init)
4 min · 00-11 · planned

Initialise a new repository with a first branch name and an optional .gitignore template and licence.

### 1.12 Recent repositories and the New Tab page in GitTree
3 min · 00-12 · planned

Reopen a repository from the Recent list and remove one from it without deleting files.

### 1.13 GitTree window tour: sidebar, graph, inspector, drawer
4 min · 00-13 · planned

Learn where the four areas of the window are and how to toggle each one.

## Section 2: Git foundations: the ideas behind every click

*Understand the ideas every Git operation is built on, each shown with one feature of the app.*

### 2.1 What is a Git commit? See one in GitTree
5 min · 01-01 · planned

See that a commit is a snapshot with a parent, a message and an author, using the Commit Details panel.

### 2.2 The Git commit graph explained: history is a DAG
5 min · 01-02 · planned

Read the commit graph: parents, lanes and why history is a graph and not a line.

### 2.3 Git branches are just pointers (refs explained)
5 min · 01-03 · planned

See branch pills on the graph and learn that a ref is a movable name for a commit.

### 2.4 What is HEAD in Git? Find it in GitTree
4 min · 01-04 · planned

Jump to HEAD and see what the checked-out branch and a detached HEAD look like.

### 2.5 Git working tree, index and HEAD: the three trees
6 min · 01-05 · planned

Use the Working Changes panel to see the working folder, the index and HEAD as three different states.

### 2.6 Local vs remote branches in Git (origin/main explained)
5 min · 01-06 · planned

Read the left panel and the ahead and behind counts to tell local branches from remote-tracking ones.

### 2.7 What is a Git remote? Add, edit and remove one
5 min · 01-07 · planned

Add, edit and remove a remote and see that it is only a name for a URL.

### 2.8 Git tags explained: create a tag in GitTree
4 min · 01-08 · planned

Create a lightweight tag on a commit and see it as a pill in the graph.

### 2.9 Git fetch explained: download without changing your files
4 min · 01-09 · planned

Run Fetch All and watch only the remote-tracking branches move while your files stay put.

### 2.10 What is a Git fast-forward? Move a branch pointer
4 min · 01-10 · planned

Fast-forward a branch to its upstream and see that only the pointer moves.

### 2.11 Git merge vs rebase: the difference on the graph
6 min · 01-11 · planned

Drag one branch onto another and compare what Merge and Rebase do to the graph.

### 2.12 Git config scopes: system, global and local explained
5 min · 01-12 · planned

Change a Git setting at the global and the local level from Preferences and see which one wins.

## Section 3: Daily workflow: stage, commit, review

*Stage, commit, amend and review your work with confidence, and park work in progress.*

### 3.1 Stage a file in GitTree (git add explained)
3 min · 02-01 · planned

Stage one changed file so that it goes into the next commit and the others do not.

### 3.2 Stage a single hunk in GitTree (commit part of a file)
3.5 min · 02-02 · scripted

Commit only one of two changes in the same file, without touching the other.

By the end of this lecture you can:
- Explain what a hunk is and why a commit is built from the staging area
- Stage one hunk of a file in GitTree with Stage Hunk and check the result in the Staged Files list
- Commit only that hunk and confirm the other hunk is still in your working changes
- Run the same job in the terminal with git add -p

### 3.3 Stage single lines in GitTree (partial commit)
4 min · 02-03 · planned

Pick individual changed lines and stage only those.

### 3.4 Unstage a file in GitTree (undo git add)
3 min · 02-04 · planned

Move a staged file back to the unstaged list without losing any edit.

### 3.5 Make a Git commit in GitTree step by step
4 min · 02-05 · planned

Write a summary and description and commit the staged changes.

### 3.6 Write better Git commit messages with GitTree hints
4 min · 02-06 · planned

Use the summary counter and the message hints, including the Conventional Commits check.

### 3.7 Amend the last Git commit in GitTree
4 min · 02-07 · planned

Fix the message or add a forgotten file to the last commit.

### 3.8 Git commit options: sign-off, skip hooks, other author
5 min · 02-08 · planned

Open the Commit Options menu and use sign-off, a different author and recent messages.

### 3.9 Add co-authors to a Git commit in GitTree
3 min · 02-09 · planned

Credit a second person on a commit with a Co-authored-by trailer.

### 3.10 Git commit hooks: read pre-commit output in GitTree
4 min · 02-10 · planned

See what a failing pre-commit hook prints and why your message and staged changes are kept.

### 3.11 Draft a Git commit message with your own AI agent CLI
4 min · 02-11 · planned

Generate a commit message from the staged diff using a coding-agent CLI you installed and signed in to.

### 3.12 Discard changes to a file in GitTree (git restore)
4 min · 02-12 · planned

Throw away the changes in one file, knowing a recovery snapshot is saved first.

### 3.13 Discard a single hunk in GitTree (undo part of a file)
3 min · 02-13 · planned

Throw away one hunk of a file and keep the other.

### 3.14 Discard all changes in a Git repository safely
3 min · 02-14 · planned

Reset the whole working folder to the last commit with one confirmed action.

### 3.15 Ignore a file, folder or extension in Git (.gitignore)
3 min · 02-15 · planned

Add a path to .gitignore from the right-click menu.

### 3.16 Edit .gitignore and find out why a file is ignored
4 min · 02-16 · planned

Edit .gitignore with a template and ask which rule ignores a given path.

### 3.17 Git diff in GitTree: hunk, inline and side by side
4 min · 02-17 · planned

Switch the diff between Hunk, Inline and Split views.

### 3.18 Jump between changes in a Git diff (F7 and Shift+F7)
3 min · 02-18 · planned

Move to the next and previous change with the keyboard and the change overview.

### 3.19 Ignore whitespace in a Git diff and wrap long lines
3 min · 02-19 · planned

Turn on Ignore whitespace, Wrap lines and Highlight changed words.

### 3.20 Compare images in Git: side by side, swipe, onion skin
3 min · 02-20 · planned

Compare two versions of an image with the three image diff modes.

### 3.21 View a file at any Git commit in GitTree
3 min · 02-21 · planned

Open a file as it was at a chosen commit using File View.

### 3.22 Compare two Git commits in GitTree (git diff A B)
4 min · 02-22 · planned

Select two commits and see the files that differ between them.

### 3.23 Restore a file from an old Git commit in GitTree
3 min · 02-23 · planned

Bring one file back to how it was in a chosen commit.

### 3.24 Git blame: who changed this line? (GitTree blame view)
4 min · 02-24 · planned

Open Blame on a file and see which commit last touched each line.

### 3.25 Git blame before this commit: walk a line's history
3 min · 02-25 · planned

Step back to the blame of the commit before the one that changed a line.

### 3.26 Git file history with renames (git log --follow)
3 min · 02-26 · planned

List every commit that changed one file, across renames.

### 3.27 The WIP row in the Git graph: your uncommitted work
3 min · 02-27 · planned

Read the WIP row at the top of the graph and open the working changes from it.

### 3.28 Search Git history in GitTree (Ctrl+F in the graph)
3 min · 02-28 · planned

Search the loaded history by message, author, SHA, branch or tag and jump between matches.

### 3.29 Git stash in GitTree: save work in progress
3 min · 02-29 · planned

Stash all your changes to get a clean working folder.

### 3.30 Git stash pop in GitTree: bring your changes back
3 min · 02-30 · planned

Pop the latest stash to restore it and remove it from the list.

## Section 4: Branching and merging

*Branch, tag, merge and resolve conflicts, and run a Gitflow release.*

### 4.1 Create a Git branch in GitTree
4 min · 03-01 · planned

Create a branch at the current commit and check it out.

### 4.2 Switch Git branches in GitTree (git switch)
5 min · 03-02 · planned

Check out another branch, including what GitTree offers when local changes are in the way.

### 4.3 Check out a remote Git branch and track it
3 min · 03-03 · planned

Check out a remote branch so that a local branch tracks it.

### 4.4 Rename a Git branch in GitTree
3 min · 03-04 · planned

Rename a local branch and see the pill change.

### 4.5 Delete a Git branch safely in GitTree
3 min · 03-05 · planned

Delete a local branch and see that its last commit is kept in a recovery ref.

### 4.6 Set the upstream branch in Git (tracking explained)
3 min · 03-06 · planned

Choose which remote branch a local branch tracks, or make it track nothing.

### 4.7 Create an annotated Git tag in GitTree
3 min · 03-07 · planned

Create an annotated tag with a message for a release.

### 4.8 Delete a Git tag locally and on the remote
3 min · 03-08 · planned

Delete a tag from your repository and, separately, from the remote.

### 4.9 Preview a Git merge for conflicts before you merge
4 min · 03-09 · planned

See whether a merge will conflict, and in which files, before anything changes.

### 4.10 Merge a Git branch in GitTree (merge commit)
5 min · 03-10 · planned

Merge one branch into the current branch and choose how it is recorded.

### 4.11 Git squash merge: combine a branch into one commit
4 min · 03-11 · planned

Squash a branch into the staged changes and commit it as one commit.

### 4.12 Git merge in progress: the operation banner in GitTree
4 min · 03-12 · planned

Read the operation banner and know when to Resolve, Continue, Skip or Abort.

### 4.13 Abort a Git merge or rebase and go back to before
3 min · 03-13 · planned

Abort an operation in one step and see that your work is kept under a recovery ref.

### 4.14 Merge conflicts in Git: find the conflicted files
4 min · 03-14 · planned

Read the Conflicted Files and Resolved Files lists and mark files resolved.

### 4.15 Resolve a Git merge conflict in GitTree's merge view
6 min · 03-15 · planned

Resolve one conflict line by line in the three-pane editor and save it as resolved.

### 4.16 Resolve a Git conflict by taking one whole side
4 min · 03-16 · planned

Resolve a file by keeping ours or theirs entirely, including delete versus modify.

### 4.17 Use an external merge tool for Git conflicts
4 min · 03-17 · planned

Open a conflicted file in the merge tool you configured and return to GitTree.

### 4.18 Git flow in GitTree: initialise the branching model
4 min · 03-18 · planned

Initialise Gitflow with your production and development branches and prefixes.

### 4.19 Git flow: start and finish a feature branch
5 min · 03-19 · planned

Start a feature, commit on it, and finish it back into develop.

### 4.20 Predict Git merge conflicts before they happen
3 min · 03-20 · planned

Read the early conflict warning chip on a branch and the setting that controls it.

## Section 5: Rewriting history and getting out of trouble

*Rebase, cherry-pick, revert and reset on purpose, and recover from any mistake.*

### 5.1 Git rebase explained: rebase a branch in GitTree
5 min · 04-01 · planned

Rebase the current branch onto another and see the commits get new ids.

### 5.2 Git interactive rebase in GitTree (pick, squash, drop)
7 min · 04-02 · planned

Rearrange, combine and drop commits in the interactive rebase editor.

### 5.3 Change a Git commit message after committing (reword)
3 min · 04-03 · planned

Reword an older commit message from the graph.

### 5.4 Remove a commit from Git history (drop a commit)
3 min · 04-04 · planned

Drop a commit from the graph and see how Undo can bring it back.

### 5.5 Reorder Git commits: move a commit up or down
3 min · 04-05 · planned

Move a commit up or down in the history from the right-click menu.

### 5.6 Squash Git commits into one in GitTree
3 min · 04-06 · planned

Select several commits and squash them into one.

### 5.7 Why rewriting pushed Git commits is risky
4 min · 04-07 · planned

See the warning GitTree shows when commits you are about to rewrite are already on a remote.

### 5.8 Git cherry-pick: copy a commit to another branch
4 min · 04-08 · planned

Copy one commit onto the current branch.

### 5.9 Git revert: undo a commit without rewriting history
4 min · 04-09 · planned

Revert a commit by adding a new commit that undoes it.

### 5.10 Git reset --soft: undo a commit but keep it staged
3 min · 04-10 · planned

Move the branch back one commit while the changes stay staged.

### 5.11 Git reset --mixed: undo a commit, keep the changes
3 min · 04-11 · planned

Move the branch back and the index with it, keeping your files.

### 5.12 Git reset --hard in GitTree: discard commits safely
4 min · 04-12 · planned

Hard-reset a branch and recover the discarded work from the snapshot GitTree takes first.

### 5.13 Undo and redo Git operations in GitTree
5 min · 04-13 · planned

Undo a rebase and a branch delete from the toolbar and redo them.

### 5.14 Git recovery snapshots: GitTree's refs/ogt/trash
4 min · 04-14 · planned

Find the recovery snapshots GitTree keeps and delete the old ones.

### 5.15 Git reflog explained: see where HEAD has been
4 min · 04-15 · planned

Open the reflog of a branch and read the list of places it pointed to.

### 5.16 Recover a lost Git commit with the reflog
4 min · 04-16 · planned

Create a branch from a reflog entry to get back a commit that no branch points to.

### 5.17 Git bisect: find the commit that introduced a bug
6 min · 04-17 · planned

Mark commits good and bad until GitTree names the first bad commit.

### 5.18 Create a Git patch file from a commit (format-patch)
3 min · 04-18 · planned

Save one or more commits as a patch file you can send.

### 5.19 Apply a Git patch file: git apply vs git am
4 min · 04-19 · planned

Apply a patch to the working tree, to the index, or as commits.

## Section 6: Collaboration: remotes, pull requests, providers

*Share work through remotes, pull requests and hosting providers, and push safely.*

### 6.1 Git push in GitTree: send your commits to a remote
5 min · 05-01 · planned

Push a branch, including the first push that picks the remote branch.

### 6.2 Check where a Git push will go before you push
3 min · 05-02 · planned

Read the destination check and choose a different target if it is wrong.

### 6.3 Git pull --ff-only in GitTree
3 min · 05-03 · planned

Pull with fast-forward only and see it refuse when histories have diverged.

### 6.4 Git pull: fast-forward if possible, else merge
4 min · 05-04 · planned

Pull when both sides have new commits and get a merge commit.

### 6.5 Git pull --rebase in GitTree
4 min · 05-05 · planned

Pull by replaying your local commits on top of the remote's.

### 6.6 Choose your default Git pull mode in GitTree
3 min · 05-06 · planned

Set what the toolbar Pull button does: fast-forward only, merge or rebase.

### 6.7 Git push rejected (non-fast-forward): how to fix it
5 min · 05-07 · planned

Understand the refused-push dialog and choose Fetch, Merge and Push or Rebase and Push.

### 6.8 Git force push with lease: the safe way in GitTree
5 min · 05-08 · planned

Force-push a rewritten branch so that it refuses if the remote moved.

### 6.9 Delete a remote Git branch from GitTree
3 min · 05-09 · planned

Delete a branch on the remote without leaving GitTree.

### 6.10 Push a Git tag to the remote in GitTree
3 min · 05-10 · planned

Push a single tag to the remote.

### 6.11 Git auto-fetch: keep remote branches up to date
3 min · 05-11 · planned

Turn on auto-fetch with an interval and see why it never asks for credentials.

### 6.12 Connect GitHub to GitTree (browser sign-in or token)
5 min · 05-12 · planned

Connect a GitHub account with the browser device code or a personal access token.

### 6.13 Connect GitHub Enterprise Server to GitTree
4 min · 05-13 · planned

Name your Enterprise Server host and connect with a token or browser sign-in.

### 6.14 Connect GitLab to GitTree (token or application ID)
4 min · 05-14 · planned

Connect gitlab.com or a self-managed GitLab with a token or a typed OAuth application ID.

### 6.15 Connect Bitbucket Cloud to GitTree
4 min · 05-15 · planned

Connect Bitbucket Cloud with browser sign-in, an API token or an access token.

### 6.16 Connect Azure DevOps to GitTree (personal access token)
4 min · 05-16 · planned

Connect Azure DevOps with a personal access token.

### 6.17 Connect Bitbucket Data Center to GitTree
4 min · 05-17 · planned

Connect a Bitbucket Data Center host through your administrator's OAuth application link.

### 6.18 Clone a repository from your hosting account in GitTree
4 min · 05-18 · planned

Browse the repositories of a connected account and clone one.

### 6.19 Publish a local Git repository to a host from GitTree
4 min · 05-19 · planned

Create the repository on your host, add it as origin and push, in one dialog.

### 6.20 Create a pull request from GitTree
5 min · 05-20 · planned

Push a branch and start a pull request with a title and description, as a draft if you like.

### 6.21 Check out a pull request branch locally in GitTree
4 min · 05-21 · planned

Fetch a pull request head and check out its branch.

### 6.22 Review pull request files and diffs in GitTree
4 min · 05-22 · planned

Read the changed files of a pull request.

### 6.23 Comment on and resolve pull request threads in GitTree
4 min · 05-23 · planned

Post a comment, reply to a thread and resolve it.

### 6.24 See pull request checks and re-run them in GitTree
3 min · 05-24 · planned

Read the checks of a pull request and re-run a failed one.

### 6.25 Review a pull request: approve or request changes
4 min · 05-25 · planned

Submit a review on a pull request and edit its details.

### 6.26 Merge a pull request: merge, squash or rebase
4 min · 05-26 · planned

Merge a pull request on the host with the method you choose.

### 6.27 See issues and start a branch from one in GitTree
4 min · 05-27 · planned

Open an issue from the sidebar and create a branch for it.

### 6.28 Create an issue from GitTree
3 min · 05-28 · planned

Create a new issue with a title and a Markdown description.

### 6.29 Git fork workflow: add a remote from a fork in GitTree
4 min · 05-29 · planned

Add a remote that points to someone's fork over HTTPS or SSH.

## Section 7: Power features: worktrees, submodules, LFS, search

*Use worktrees, submodules, LFS, search and the terminal to handle bigger projects.*

### 7.1 Git worktrees explained: see them in GitTree
4 min · 06-01 · planned

Find the Worktrees section and understand what several working folders share.

### 7.2 Create a Git worktree in GitTree (git worktree add)
4 min · 06-02 · planned

Create a worktree for a branch or a new branch in a separate folder.

### 7.3 Move, lock and remove a Git worktree
5 min · 06-03 · planned

Move, lock, remove and prune worktrees safely.

### 7.4 Git submodules explained: see them in GitTree
4 min · 06-04 · planned

Read the Submodules section and its states.

### 7.5 Add a Git submodule in GitTree
4 min · 06-05 · planned

Add a submodule at a path, optionally following a branch.

### 7.6 Update and remove a Git submodule in GitTree
5 min · 06-06 · planned

Initialise, update, sync and remove a submodule.

### 7.7 Set up Git LFS for a repository in GitTree
4 min · 06-07 · planned

Check that Git LFS is installed and set it up for this repository.

### 7.8 Track large files with Git LFS in GitTree
4 min · 06-08 · planned

Track and untrack a file pattern with LFS.

### 7.9 Download and prune Git LFS content in GitTree
4 min · 06-09 · planned

Download LFS file content and prune old content.

### 7.10 Git LFS file locking in GitTree
3 min · 06-10 · planned

Lock and unlock a lockable file and see who holds a lock.

### 7.11 Git sparse checkout in GitTree: only the folders you need
4 min · 06-11 · planned

Check out only chosen folders of a large repository, and bring everything back later.

### 7.12 Shallow, sparse and blobless Git clones in GitTree
6 min · 06-12 · planned

Clone a big repository faster with depth, sparse or blobless options, and fetch more history later.

### 7.13 Git stash options: untracked files, staged only, message
4 min · 06-13 · planned

Stash with a message, include untracked files or stash only the staged changes.

### 7.14 Create a Git branch from a stash in GitTree
3 min · 06-14 · planned

Turn an old stash into a branch.

### 7.15 Delete a Git stash and recover it from the snapshots
3 min · 06-15 · planned

Delete a stash and see that it is kept in the recovery snapshots.

### 7.16 Git repository maintenance in GitTree (fsck, gc)
5 min · 06-16 · planned

Check integrity, speed up history and clean up the object database.

### 7.17 Group repositories into workspaces in GitTree
4 min · 06-17 · planned

Create a workspace, add repositories to it and open them all.

### 7.18 Work in several repositories with tabs in GitTree
4 min · 06-18 · planned

Open, switch, reorder and close repository tabs.

### 7.19 The GitTree command palette: run anything from the keyboard
5 min · 06-19 · planned

Open the palette and run commands, jump to refs and switch repositories with the prefixes.

### 7.20 Search all Git history by message, author, file or change
5 min · 06-20 · planned

Search every commit with the # mode and the author, file and change filters.

### 7.21 Find any file fast in GitTree (fuzzy file finder)
3 min · 06-21 · planned

Find a file with the : mode and open its history.

### 7.22 The integrated terminal in GitTree
4 min · 06-22 · planned

Open a terminal in the repository folder, add more terminals and rename them.

### 7.23 Define custom commands in GitTree (programs with tokens)
5 min · 06-23 · planned

Add a custom command that runs a program with the repository, branch, SHA or file as arguments.

### 7.24 Run a custom command from the GitTree toolbar
3 min · 06-24 · planned

Run a saved custom command and read its confirmation and output.

### 7.25 Filter the Git graph by author, date, branch or path
4 min · 06-25 · planned

Show only the commits that match a filter and clear it again.

### 7.26 See all your pull requests across a workspace
4 min · 06-26 · planned

Use the Pull requests tab of the Workspaces page to see what needs your review.

## Section 8: Customise GitTree and fix problems

*Make GitTree fit the way you work and fix the problems people hit most.*

### 8.1 GitTree Preferences: search, scopes and reset
4 min · 07-01 · planned

Find a setting with search, see where it is saved, and reset it.

### 8.2 Change the GitTree theme: dark, light, high contrast
3 min · 07-02 · planned

Choose a theme, or follow the system appearance.

### 8.3 Zoom, date format and reduced motion in GitTree
4 min · 07-04 · planned

Zoom the interface, choose a date format and show or hide sidebar sections.

### 8.4 Git profiles in GitTree: work and personal identities
5 min · 07-05 · planned

Create two profiles with different names and emails and switch between them.

### 8.5 SSH keys in GitTree: generate, copy and test
5 min · 07-06 · planned

Generate an Ed25519 key, copy its public half and test a connection.

### 8.6 SSH host key and username prompts in GitTree
4 min · 07-07 · planned

Answer the 'Connect to host?' prompt safely and choose how unknown host keys are treated.

### 8.7 Sign Git commits in GitTree (OpenPGP, SSH, S/MIME)
5 min · 07-08 · planned

Choose a signing key and turn on signing for every commit.

### 8.8 Set an external diff tool, merge tool and editor
4 min · 07-09 · planned

Pick the diff tool, merge tool and editor GitTree opens for you.

### 8.9 GitTree keyboard shortcuts: the cheat sheet
3 min · 07-10 · planned

Open the Keyboard Shortcuts sheet and find the shortcut for any command.

### 8.10 Customise keyboard shortcuts in GitTree
4 min · 07-11 · planned

Change, remove and reset a shortcut and see how conflicts are reported.

### 8.11 See the exact Git commands GitTree runs (Activity Log)
4 min · 07-12 · planned

Open the Activity Log to read each git command, its output and its result.

### 8.12 Report a bug or a crash from GitTree
3 min · 07-13 · planned

Open Crash Reports, copy the text and report it on GitHub.

### 8.13 Update GitTree: check for updates, download and install
4 min · 07-14 · planned

Check for an update, see the download get verified and restart to install it.

### 8.14 GitTree startup screens: update, offline, maintenance
5 min · 07-15 · planned

Understand each startup gate screen and what to do on each, including the 7-day offline grace.

### 8.15 Sign out of GitTree everywhere
3 min · 07-16 · planned

Sign out of your GitTree account and see that connected hosting accounts stay connected.

### 8.16 Restricted mode in GitTree: open untrusted repos safely
4 min · 07-17 · planned

Work in Restricted Mode and review the trust decision later.

### 8.17 Where GitTree stores your tokens (system keychain)
4 min · 07-18 · planned

See that tokens go to the system keychain and how to disconnect an account or forget all credentials.

### 8.18 Linux keyring for GitTree: Secret Service setup
4 min · 07-19 · planned

Make sure a Secret Service (GNOME Keyring or KeePassXC) is running so GitTree can save tokens.

### 8.19 Import a custom theme into GitTree
3 min · 07-20 · planned

Import a theme file and use it next to the built-in themes.

### 8.20 Export, import and reset GitTree settings
4 min · 07-21 · planned

Export your settings, import them on another computer and reset everything if needed.

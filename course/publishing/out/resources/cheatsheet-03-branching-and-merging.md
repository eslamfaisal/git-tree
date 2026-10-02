# Commands: Branching and merging

| Command | Lesson |
|---|---|
| `git branch <name> <sha>` | Create a Git branch in GitTree |
| `git switch <name>` | Create a Git branch in GitTree |
| `git switch <branch>` | Switch Git branches in GitTree (git switch) |
| `git switch --track origin/<branch>` | Check out a remote Git branch and track it |
| `git branch -m <old> <new>` | Rename a Git branch in GitTree |
| `git branch -D <name>` | Delete a Git branch safely in GitTree |
| `git branch --set-upstream-to=origin/<branch>` | Set the upstream branch in Git (tracking explained) |
| `git branch --unset-upstream` | Set the upstream branch in Git (tracking explained) |
| `git tag --annotate -m <message> <name> <sha>` | Create an annotated Git tag in GitTree |
| `git tag --delete <name>` | Delete a Git tag locally and on the remote |
| `git push origin --delete refs/tags/<name>` | Delete a Git tag locally and on the remote |
| `git merge-tree --write-tree --name-only <a> <b>` | Preview a Git merge for conflicts before you merge |
| `git merge --no-edit <branch>` | Merge a Git branch in GitTree (merge commit) |
| `git merge --no-ff <branch>` | Merge a Git branch in GitTree (merge commit) |
| `git merge --ff-only <branch>` | Merge a Git branch in GitTree (merge commit) |
| `git merge --squash <branch>` | Git squash merge: combine a branch into one commit |
| `git merge --continue` | Git merge in progress: the operation banner in GitTree |
| `git rebase --skip` | Git merge in progress: the operation banner in GitTree |
| `git merge --abort` | Abort a Git merge or rebase and go back to before |
| `git rebase --abort` | Abort a Git merge or rebase and go back to before |
| `git status` | Merge conflicts in Git: find the conflicted files |
| `git ls-files -u` | Merge conflicts in Git: find the conflicted files |
| `git add <file>` | Resolve a Git merge conflict in GitTree's merge view |
| `git checkout --ours -- <path>` | Resolve a Git conflict by taking one whole side |
| `git checkout --theirs -- <path>` | Resolve a Git conflict by taking one whole side |
| `git rm -- <path>` | Resolve a Git conflict by taking one whole side |
| `git mergetool` | Use an external merge tool for Git conflicts |
| `git config gitflow.branch.develop develop` | Git flow in GitTree: initialise the branching model |
| `git merge --no-ff feature/<name>` | Git flow: start and finish a feature branch |
| `git branch -d feature/<name>` | Git flow: start and finish a feature branch |
| `git merge-tree --write-tree --name-only --no-messages -z` | Predict Git merge conflicts before they happen |

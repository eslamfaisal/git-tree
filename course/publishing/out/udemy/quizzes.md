# Quizzes

## Section 1: Start here: install, sign in, open a repository

**00-08 Q1. What makes a folder a Git repository?**

a) It has a README file
b) It has a hidden .git folder that holds the history  ✓
c) It is stored on a cloud drive
d) It contains at least ten files

*The .git folder holds the commits, branches and tags. The folder around it is the working folder.*

**00-08 Q2. Which shortcut opens the folder picker on Linux and Windows?**

a) Ctrl+T
b) Ctrl+W
c) Ctrl+O  ✓
d) Ctrl+N

*Ctrl+O runs Open Repository. On a Mac the same shortcut is Cmd+O.*

**00-08 Q3. You choose a folder with no .git in it or above it. What does GitTree do?**

a) It deletes the folder
b) It opens an empty tab anyway
c) It shows a message that the folder is not a Git repository, with options to initialize one or choose another  ✓
d) It closes the app

*GitTree asks Git first and refuses a folder that is not a repository. It changes nothing on its own.*

**00-11 Q1. What does git init create?**

a) A remote copy on a server
b) A hidden .git folder that holds the history, and the first branch  ✓
c) A first commit with all your files
d) A new branch from an existing repository

*git init sets up the repository's database in the .git folder and points the first branch at no commit yet.*

**00-11 Q2. In the Init dialog, what happens to the .gitignore and licence files you choose?**

a) They are committed immediately
b) They are written into the folder as working changes, uncommitted  ✓
c) They are uploaded to a website
d) They replace any file with the same name

*The files are written uncommitted, so you decide when to commit them. A file that already exists is kept, never replaced.*

**00-11 Q3. Which option sets the first branch's name from the terminal?**

a) --bare
b) --quiet
c) --initial-branch  ✓
d) --template

*git init --initial-branch main creates the repository with main as its first branch.*

**00-13 Q1. Which shortcut shows and hides the inspector?**

a) Ctrl+J
b) Ctrl+K  ✓
c) Alt+T
d) Escape

*Ctrl+K (Cmd+K on a Mac) is Toggle Inspector. Ctrl+J toggles the sidebar and Alt+T the bottom drawer.*

**00-13 Q2. What does the Activity Log tab in the bottom drawer show?**

a) The commits of the current branch
b) The Git commands GitTree has run  ✓
c) The files you have changed
d) The tags of the repository

*Every Git command the app runs is listed there, with its output.*

**00-13 Q3. You opened a file and its diff replaced the graph. How do you get back to the graph?**

a) Press Escape  ✓
b) Press Ctrl+J
c) Close the tab
d) Restart GitTree

*Escape is Back; it closes the diff and shows the graph again.*

## Section 2: Git foundations: the ideas behind every click

## Section 3: Daily workflow: stage, commit, review

**02-01 Q1. What does staging a file do?**

a) It commits the file
b) It puts the file's changes in the staging area, so the next commit will include them  ✓
c) It deletes the file's changes
d) It uploads the file to the remote

*Staging copies the file's changes into the index, which is the next commit. Nothing is committed or sent anywhere yet.*

**02-01 Q2. You change two files, stage only one and commit. Where is the other file?**

a) In the commit as well
b) Deleted from the working folder
c) Still under Unstaged Files, with its changes intact  ✓
d) In the staging area

*A commit takes only what is staged. The file you did not stage keeps its changes in the working folder.*

**02-01 Q3. Which key stages the selected file when the file list has focus?**

a) U
b) S  ✓
c) Enter

*S stages the selected files and U unstages them; both only act while the matching list has focus.*

**02-02 Q1. What is a hunk?**

a) A whole file that changed
b) A block of changed lines with a few unchanged lines around it  ✓
c) A commit that was rewritten
d) A branch that has not been merged

*Git groups changed lines into blocks; each block with its surrounding context is a hunk.*

**02-02 Q2. After you click Stage Hunk on the first of two hunks, where is the second hunk?**

a) In the staging area, with the first
b) Deleted from the file
c) Still in the working changes, listed under Unstaged Files  ✓
d) In the last commit

*Only the hunk you staged moved. The other one stays in the working tree until you stage it.*

**02-02 Q3. Which git command lets you pick hunks one by one in the terminal?**

a) git add -p  ✓
b) git commit --amend
c) git stash pop
d) git reset --hard

*git add -p (patch mode) shows each hunk and asks whether to stage it.*

**02-03 Q1. Why pick single lines instead of using Stage Hunk?**

a) Because Stage Hunk is slower
b) Because one hunk can hold two unrelated changes, and Stage Hunk takes the whole hunk  ✓
c) Because hunks cannot be committed
d) Because lines are committed without a message

*A hunk is the smallest block Git groups together. When two ideas land in the same block, only line-level staging separates them.*

**02-03 Q2. How do you pick a range of lines in the diff?**

a) Click the first line, then Shift+click the last line  ✓
b) Double-click the hunk header
c) Press S twice
d) Drag the file into the Staged Files list

*A click picks one line; Shift+click picks every changed line between it and the previous pick.*

**02-03 Q3. Which of these is always staged whole, never line by line?**

a) A TypeScript source file
b) A README
c) A binary file  ✓

*Binary files, renames, Git LFS pointers, mode changes and submodule changes cannot be split, so GitTree stages them whole.*

**02-04 Q1. What happens to your edits when you unstage a file?**

a) They are deleted from the file
b) They stay in the working folder, and the file only leaves the staging area  ✓
c) They are saved into a new commit
d) They are moved to the stash

*Unstaging changes only the index, the list of what the next commit holds. The file on disk is not touched.*

**02-04 Q2. After you unstage src/tags.ts, where does GitTree list it?**

a) Under Staged Files
b) Under Unstaged Files  ✓
c) It disappears from the panel
d) In the last commit

*The file still has changes that are not in the next commit, so it moves to Unstaged Files.*

**02-04 Q3. Which command unstages one file in a terminal?**

a) git add -- src/tags.ts
b) git restore --staged -- src/tags.ts  ✓
c) git commit -- src/tags.ts
d) git stash -- src/tags.ts

*git restore --staged resets the file's entry in the staging area to match the last commit and leaves the working file alone.*

**02-04 Q4. Which key unstages the selected file in the Staged Files list?**

a) S
b) U  ✓
c) Ctrl+Enter
d) Delete

*U runs Unstage when the file list has focus. S is its opposite, Stage.*

**02-05 Q1. What does a commit save?**

a) Every change in the working folder
b) Only what is in the staging area  ✓
c) Only the files you opened last
d) Only the files that are not staged

*A commit is a snapshot of the staging area. Anything unstaged stays in the working folder for a later commit.*

**02-05 Q2. In the commit composer, which part is the first line of the message?**

a) The Description
b) The Summary  ✓
c) The branch name
d) The counter

*The Summary is the first line. The Description is an optional body below it.*

**02-05 Q3. Which shortcut commits on Linux and Windows?**

a) Ctrl+Enter  ✓
b) Ctrl+Shift+C
c) Alt+Enter
d) U

*The command Commit is bound to Mod+Enter, and Mod is Ctrl on Linux and Windows, Cmd on macOS.*

**02-05 Q4. After you commit only README.md, where is the edit to src/tags.ts?**

a) In the new commit
b) Lost
c) Still in your working changes, under Unstaged Files  ✓
d) On the stash

*The file was never staged, so the commit did not include it and its edit is untouched.*

**02-05 Q5. How do you give git commit both a summary and a description in a terminal?**

a) Use -m twice  ✓
b) Use --amend
c) Use git log --oneline
d) Use git restore --staged

*The first -m is the summary and the second is the description, separated by a blank line.*

## Section 4: Branching and merging

## Section 5: Rewriting history and getting out of trouble

## Section 6: Collaboration: remotes, pull requests, providers

## Section 7: Power features: worktrees, submodules, LFS, search

## Section 8: Customise GitTree and fix problems

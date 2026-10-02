# Section check: 02-02 Stage a single hunk in GitTree (commit part of a file)

Tick each section after watching it in the finished video. The contact sheet (`.chapters.jpg`) shows the first frame of every chapter.

| Done | Time | Chapter | What the screen shows | The voice says |
|---|---|---|---|---|
| [ ] | 0:00 | Why commit only part of a file | scene `hook` | You fixed one bug, and in the same file you changed something else. |
| [ ] | 0:14 | What is a hunk? | scene `hunk-what` | A hunk is a block of changed lines, plus a few unchanged lines around it. |
| [ ] | 0:24 | The three places Git keeps your work | scene `three-areas` | Git keeps your work in three places: the working tree, the staging area, and the repository. |
| [ ] | 0:38 | Open the working changes | GitTree, start → wip-after · step: Open the working changes | Here is GitTree with a small demo project. |
| [ ] | 0:56 | Stage a hunk | GitTree, stage-before → stage-after · step: Click Stage Hunk on the first hunk | Every hunk has its own Stage Hunk button. |
| [ ] | 1:04 | One file, two lists | GitTree, lists-begin → lists-end · step: One file, now in two lists | Now the same file appears twice. |
| [ ] | 1:22 | Commit | GitTree, msg-before → commit-after · step: Write the message and commit | Write a commit message, and commit. |
| [ ] | 1:43 | The same in plain Git: git add -p | scene `git-command` | In plain Git, the same job is git add -p. |
| [ ] | 2:01 | Two tips | scene `tips` | Two tips. If you change your mind, the same button reads Unstage Hunk on the staged side. |
| [ ] | 2:14 | Recap | scene `recap` | To recap: a hunk is a block of changed lines, Stage Hunk moves it to the staging area, and a commit takes only what is staged. |

# Git Process for Sharing Notes Across Chats
Date: 2026-01-18
Tags: git, workflow, notes, branches, process
Summary: Step-by-step process to merge note changes into main so other chats can access them.

## Goal
Ensure notes created in one chat are visible in other chats that may be on different branches.

## Why this is needed
Branches are isolated snapshots. Notes created on one branch are not visible to other branches unless merged or cherry-picked into a shared branch.

## Standard process (Option A - merge into main)
Use this every time a chat adds notes that need to be accessible everywhere.

1) Make sure all note changes are committed and pushed on the current branch.
2) Switch to `main` and update it:
   - `git checkout main`
   - `git pull origin main`
3) Merge the notes branch into `main`:
   - `git merge <notes-branch>`
4) Push `main`:
   - `git push -u origin main`
5) In every other chat, update their working branch with `main`:
   - `git fetch origin main`
   - `git merge origin/main`

## Reminder
Always merge into `main` after a note session if the notes must be shared across chats.

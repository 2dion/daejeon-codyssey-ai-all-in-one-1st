#!/bin/zsh
PS4='$ '
set -x
git log --oneline -2
git branch -vv
git remote -v
git rev-parse HEAD
git ls-remote origin refs/heads/main

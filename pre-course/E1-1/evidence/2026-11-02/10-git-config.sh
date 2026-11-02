#!/bin/zsh
PS4='$ '
set -x
git --version
git config --list | python3 -c 'import sys; allowed=("user.name=","user.email=","init.defaultbranch=","remote.origin.url=","branch.main.remote=","branch.main.merge="); [print("user.email=[MASKED]" if s.lower().startswith("user.email=") else s.rstrip()) for s in sys.stdin if s.lower().startswith(allowed)]'
git status --short --branch
git remote -v
git ls-remote --heads origin

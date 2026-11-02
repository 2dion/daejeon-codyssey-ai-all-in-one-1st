#!/bin/zsh
PS4='$ '
set -x
sw_vers
printf 'Login shell: %s\n' "$SHELL"
ps -p $$ -o comm=
printf 'TERM_PROGRAM: %s\n' "${TERM_PROGRAM:-not-set-in-agent-shell}"
git --version
docker --version
docker context show
docker info --format 'Server {{.ServerVersion}} / OS {{.OperatingSystem}} / Architecture {{.Architecture}} / Containers {{.Containers}}'

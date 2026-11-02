#!/bin/zsh
PS4='$ '
set -x
docker ps -a --filter name=proof
docker rm e1-hello-proof-20261102 e1-ubuntu-proof-20261102 e1-exec-proof-20261102
docker tag e1-web:proof-20261102 e1-cleanup-proof:temporary
docker images e1-cleanup-proof
docker rmi e1-cleanup-proof:temporary
docker images e1-cleanup-proof
docker ps -a --filter name=proof

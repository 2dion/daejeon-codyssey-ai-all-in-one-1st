#!/bin/zsh
PS4='$ '
set -x
docker pull hello-world
docker run --name e1-hello-proof-20261102 hello-world
docker images
docker ps
docker ps -a
docker run --name e1-ubuntu-proof-20261102 -i ubuntu:24.04 bash <<'COMMANDS'
pwd
ls
 echo hello-from-ubuntu
exit
COMMANDS
docker ps -a --filter name=e1-ubuntu-proof-20261102
docker run -d --name e1-exec-proof-20261102 ubuntu:24.04 sleep infinity
docker exec e1-exec-proof-20261102 bash -c 'pwd; echo hello-from-exec'
docker ps --filter name=e1-exec-proof-20261102
docker stop e1-exec-proof-20261102
docker ps -a --filter name=e1-exec-proof-20261102

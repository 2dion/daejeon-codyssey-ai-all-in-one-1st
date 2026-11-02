#!/bin/zsh
PS4='$ '
set -x
docker volume create e1-proof-data-20261102
docker run --name e1-volume-proof-20261102 --mount source=e1-proof-data-20261102,target=/data ubuntu:24.04 sh -c 'echo preserved-20261102 > /data/proof.txt; cat /data/proof.txt'
docker rm e1-volume-proof-20261102
docker run --rm --mount source=e1-proof-data-20261102,target=/data ubuntu:24.04 cat /data/proof.txt
docker volume inspect e1-proof-data-20261102 --format 'Name {{.Name}} / Driver {{.Driver}}'

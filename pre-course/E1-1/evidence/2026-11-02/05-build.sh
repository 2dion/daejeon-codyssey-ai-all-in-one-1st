#!/bin/zsh
PS4='$ '
set -x
cat Dockerfile
cat site/index.html
docker build --progress=plain -t e1-web:proof-20261102 .
docker image inspect e1-web:proof-20261102 --format 'Image {{.Id}} / ExposedPorts {{json .Config.ExposedPorts}}'
docker ps --filter name=e1-web
curl -i http://localhost:8080
docker logs --tail 8 e1-web
docker stats --no-stream e1-web

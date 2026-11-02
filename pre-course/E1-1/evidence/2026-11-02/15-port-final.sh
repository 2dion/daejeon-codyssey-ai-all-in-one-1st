#!/bin/zsh
PS4='$ '
set -x
docker ps --filter publish=8080
lsof -nP -iTCP:8080 -sTCP:LISTEN
docker ps --filter name=e1-web-proof-8082
curl -fsSi http://localhost:8082

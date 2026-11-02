#!/bin/zsh
PS4='$ '
set -x
docker ps --filter publish=8080
docker run -d --name e1-port-proof-20261102 -p 127.0.0.1:8080:80 e1-web:proof-20261102
docker ps -a --filter name=e1-port-proof-20261102
docker ps --filter publish=8080
lsof -nP -iTCP:8080 -sTCP:LISTEN
docker rm e1-port-proof-20261102
docker run -d --name e1-web-proof-8082 -p 127.0.0.1:8082:80 e1-web:proof-20261102
curl --retry 3 --retry-connrefused --retry-delay 1 -i http://localhost:8082
docker ps --filter name=e1-web-proof-8082

#!/bin/zsh
PS4='$ '
set -x
curl -fsSi http://localhost:8080
curl -fsSi http://localhost:8081
curl -fsSi http://localhost:8082
docker exec e1-bind ls -l /usr/share/nginx/html

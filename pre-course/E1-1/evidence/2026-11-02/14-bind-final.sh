#!/bin/zsh
PS4='$ '
set -x
docker inspect e1-bind --format '{{range .Mounts}}{{.Type}} {{.Source}} -> {{.Destination}} RW={{.RW}}{{end}}'
curl -fsS http://localhost:8081 | grep '<p>'
curl -fsS http://localhost:8080 | grep '<p>'

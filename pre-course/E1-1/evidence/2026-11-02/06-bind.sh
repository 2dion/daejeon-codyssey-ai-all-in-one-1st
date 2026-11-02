#!/bin/zsh
PS4='$ '
set -x
docker ps -a --filter name=e1-bind
docker inspect e1-bind --format 'Status {{.State.Status}} | {{range .Mounts}}{{.Type}} {{.Source}} -> {{.Destination}} RW={{.RW}}{{end}}'
docker run -d --name e1-bind -p 127.0.0.1:8081:80 --mount type=bind,source="$(pwd)/site",target=/usr/share/nginx/html,readonly e1-web:1.0
# Above: intentionally reproduce the existing name conflict; reuse the verified running container.
curl -s http://localhost:8081
sed -i '' 's/바인드 마운트 변경이 반영됐습니다/바인드 마운트 변경이 다시 반영됐습니다/' site/index.html
cat site/index.html
curl -s http://localhost:8081
curl -s http://localhost:8080
docker inspect e1-bind --format 'Status {{.State.Status}} | {{range .Mounts}}{{.Type}} {{.Source}} -> {{.Destination}} RW={{.RW}}{{end}}'

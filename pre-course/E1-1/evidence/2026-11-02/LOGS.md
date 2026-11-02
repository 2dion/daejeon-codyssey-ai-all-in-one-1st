# 2026-11-02 실제 실행 로그

명령은 `$`로 시작한다. 자동화 셸 및 VS Code 통합 터미널에서 실제로 실행한 출력이다. 사용자 경로·이름은 `[USER]`, 이메일은 `[MASKED]`로 치환했다.

06·07에는 의도적으로 재현한 충돌 및 최초 접속 오류가 포함된다. 섹션 종료 코드 0만으로 개별 명령 성공을 판단하지 않고 11·14·15의 최종 HTTP 200 응답을 확인했다.

## 01-environment-vscode

```console
$ sw_vers
ProductName:		macOS
ProductVersion:		26.6.2
BuildVersion:		25G83
$ printf 'Login shell: %s\n' /bin/zsh
Login shell: /bin/zsh
$ ps -p 30116 -o 'comm='
/bin/zsh
$ printf 'TERM_PROGRAM: %s\n' vscode
TERM_PROGRAM: vscode
$ git --version
git version 2.55.0
$ docker --version
Docker version 29.9.2, build a82e528
$ docker context show
desktop-linux
$ docker info --format 'Server {{.ServerVersion}} / OS {{.OperatingSystem}} / Architecture {{.Architecture}} / Containers {{.Containers}}'
Server 29.9.2 / OS Docker Desktop / Architecture aarch64 / Containers 6
```

## 01-environment

```console
$ sw_vers
ProductName:		macOS
ProductVersion:		26.6.2
BuildVersion:		25G83
$ printf 'Login shell: %s\n' /bin/zsh
Login shell: /bin/zsh
$ ps -p 26600 -o 'comm='
/bin/zsh
$ printf 'TERM_PROGRAM: %s\n' not-set-in-agent-shell
TERM_PROGRAM: not-set-in-agent-shell
$ git --version
git version 2.55.0
$ docker --version
Docker version 29.9.2, build a82e528
$ docker context show
desktop-linux
$ docker info --format 'Server {{.ServerVersion}} / OS {{.OperatingSystem}} / Architecture {{.Architecture}} / Containers {{.Containers}}'
Server 29.9.2 / OS Docker Desktop / Architecture aarch64 / Containers 5
```

## 02-cli

```console
$ pwd
/Users/[USER]/Documents/Codyssey/AllInOne/GitHub/pre-course/E1-1
$ ls -la
total 136
drwxr-xr-x  12 [USER]     staff    384 Nov  2 14:24 .
drwxr-xr-x   4 [USER]     staff    128 Nov  1 14:37 ..
-rw-r--r--@  1 [USER]     staff   8196 Nov  1 21:45 .DS_Store
-rw-r--r--   1 [USER]     staff     63 Nov  1 21:10 Dockerfile
-rw-r--r--@  1 [USER]     staff  15766 Nov  1 21:45 README.md
drwxr-xr-x@  3 [USER]     staff     96 Nov  2 14:24 evidence
drwxr-xr-x   4 [USER]     staff    128 Nov  1 19:30 practice
drwxr-xr-x  26 [USER]     staff    832 Nov  1 21:38 screenshots
drwxr-xr-x   3 [USER]     staff     96 Nov  1 21:27 site
-rw-r--r--@  1 [USER]     staff  27357 Nov  1 15:28 미션 사전 질문과 답변.md
-rw-r--r--@  1 [USER]     staff   3706 Nov  1 15:27 다른-컴퓨터로-작업-옮기기.svg
-rw-r--r--@  1 [USER]     staff   3325 Nov  1 15:26 파일-권한-읽는-법.svg
$ mkdir -p practice/cli-proof-20261102
$ cd practice/cli-proof-20261102
$ pwd
/Users/[USER]/Documents/Codyssey/AllInOne/GitHub/pre-course/E1-1/practice/cli-proof-20261102
$ echo 'hello codyssey'
$ touch empty.txt
$ ls -la
total 8
drwxr-xr-x@ 4 [USER]     staff  128 Nov  2 14:24 .
drwxr-xr-x  5 [USER]     staff  160 Nov  2 14:24 ..
-rw-r--r--@ 1 [USER]     staff    0 Nov  2 14:24 empty.txt
-rw-r--r--@ 1 [USER]     staff   15 Nov  2 14:24 original.txt
$ cat original.txt
hello codyssey
$ cp original.txt copy.txt
$ ls -l
total 16
-rw-r--r--@ 1 [USER]     staff  15 Nov  2 14:24 copy.txt
-rw-r--r--@ 1 [USER]     staff   0 Nov  2 14:24 empty.txt
-rw-r--r--@ 1 [USER]     staff  15 Nov  2 14:24 original.txt
$ cat copy.txt
hello codyssey
$ mv copy.txt renamed.txt
$ ls -l
total 16
-rw-r--r--@ 1 [USER]     staff   0 Nov  2 14:24 empty.txt
-rw-r--r--@ 1 [USER]     staff  15 Nov  2 14:24 original.txt
-rw-r--r--@ 1 [USER]     staff  15 Nov  2 14:24 renamed.txt
$ mkdir moved
$ mv renamed.txt moved/
$ ls -la . moved
.:
total 8
drwxr-xr-x@ 5 [USER]     staff  160 Nov  2 14:24 .
drwxr-xr-x  5 [USER]     staff  160 Nov  2 14:24 ..
-rw-r--r--@ 1 [USER]     staff    0 Nov  2 14:24 empty.txt
drwxr-xr-x@ 3 [USER]     staff   96 Nov  2 14:24 moved
-rw-r--r--@ 1 [USER]     staff   15 Nov  2 14:24 original.txt

moved:
total 8
drwxr-xr-x@ 3 [USER]     staff   96 Nov  2 14:24 .
drwxr-xr-x@ 5 [USER]     staff  160 Nov  2 14:24 ..
-rw-r--r--@ 1 [USER]     staff   15 Nov  2 14:24 renamed.txt
$ rm moved/renamed.txt
$ ls -la moved
total 0
drwxr-xr-x@ 2 [USER]     staff   64 Nov  2 14:24 .
drwxr-xr-x@ 5 [USER]     staff  160 Nov  2 14:24 ..
$ rmdir moved
$ ls -la
total 8
drwxr-xr-x@ 4 [USER]     staff  128 Nov  2 14:24 .
drwxr-xr-x  5 [USER]     staff  160 Nov  2 14:24 ..
-rw-r--r--@ 1 [USER]     staff    0 Nov  2 14:24 empty.txt
-rw-r--r--@ 1 [USER]     staff   15 Nov  2 14:24 original.txt
$ cd ../..
$ pwd
/Users/[USER]/Documents/Codyssey/AllInOne/GitHub/pre-course/E1-1
```

## 03-permissions

```console
$ umask
022
$ mkdir -p practice/permission-dir
$ touch practice/permission-file
$ ls -l practice/permission-file
-rw-r--r--@ 1 [USER]     staff  0 Nov  2 14:24 practice/permission-file
$ ls -ld practice/permission-dir
drwxr-xr-x  2 [USER]     staff  64 Nov  1 19:29 practice/permission-dir
$ chmod 600 practice/permission-file
$ ls -l practice/permission-file
-rw-------@ 1 [USER]     staff  0 Nov  2 14:24 practice/permission-file
$ chmod 644 practice/permission-file
$ ls -l practice/permission-file
-rw-r--r--@ 1 [USER]     staff  0 Nov  2 14:24 practice/permission-file
$ chmod 700 practice/permission-dir
$ ls -ld practice/permission-dir
drwx------@ 2 [USER]     staff  64 Nov  1 19:29 practice/permission-dir
$ chmod 755 practice/permission-dir
$ ls -ld practice/permission-dir
drwxr-xr-x@ 2 [USER]     staff  64 Nov  1 19:29 practice/permission-dir
```

## 04-docker-basics

```console
$ docker pull hello-world
Using default tag: latest
latest: Pulling from library/hello-world
Digest: sha256:c567b231f65614688711a75f31518a064258a51d442117a3e771a3a8fdba78ef
Status: Image is up to date for hello-world:latest
docker.io/library/hello-world:latest
$ docker run --name e1-hello-proof-20261102 hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm64v8)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

$ docker images
IMAGE                ID             DISK USAGE   CONTENT SIZE   EXTRA
e1-web:1.0           2d932f4369ea       93.2MB         26.3MB   U
hello-world:latest   c567b231f656       22.6kB         10.3kB   U
ubuntu:24.04         fe81560990fa        141MB         30.9MB   U
$ docker ps
CONTAINER ID   IMAGE        COMMAND                  CREATED        STATUS        PORTS                    NAMES
c991e2dfeba0   e1-web:1.0   "/docker-entrypoint.…"   17 hours ago   Up 17 hours   127.0.0.1:8081->80/tcp   e1-bind
1b0d19820f61   e1-web:1.0   "/docker-entrypoint.…"   17 hours ago   Up 17 hours   127.0.0.1:8080->80/tcp   e1-web
$ docker ps -a
CONTAINER ID   IMAGE          COMMAND                  CREATED                  STATUS                              PORTS                    NAMES
72b105483ccc   hello-world    "/hello"                 Less than a second ago   Exited (0) Less than a second ago                            e1-hello-proof-20261102
c991e2dfeba0   e1-web:1.0     "/docker-entrypoint.…"   17 hours ago             Up 17 hours                         127.0.0.1:8081->80/tcp   e1-bind
1b0d19820f61   e1-web:1.0     "/docker-entrypoint.…"   17 hours ago             Up 17 hours                         127.0.0.1:8080->80/tcp   e1-web
9c9361ce2b79   ubuntu:24.04   "sleep infinity"         17 hours ago             Exited (137) 17 hours ago                                    e1-ubuntu-live
62dd2bbe5b21   ubuntu:24.04   "bash"                   17 hours ago             Exited (0) 17 hours ago                                      e1-ubuntu
0eef0459ee34   hello-world    "/hello"                 18 hours ago             Exited (0) 18 hours ago                                      amazing_lederberg
$ docker run --name e1-ubuntu-proof-20261102 -i ubuntu:24.04 bash
/
bin
boot
dev
etc
home
lib
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
hello-from-ubuntu
$ docker ps -a --filter 'name=e1-ubuntu-proof-20261102'
CONTAINER ID   IMAGE          COMMAND   CREATED                  STATUS                              PORTS     NAMES
3e3e949f615a   ubuntu:24.04   "bash"    Less than a second ago   Exited (0) Less than a second ago             e1-ubuntu-proof-20261102
$ docker run -d --name e1-exec-proof-20261102 ubuntu:24.04 sleep infinity
202153926cdd5da284637d95b07e31022bca360cd133b748a967da5de1909956
$ docker exec e1-exec-proof-20261102 bash -c 'pwd; echo hello-from-exec'
/
hello-from-exec
$ docker ps --filter 'name=e1-exec-proof-20261102'
CONTAINER ID   IMAGE          COMMAND            CREATED                  STATUS                  PORTS     NAMES
202153926cdd   ubuntu:24.04   "sleep infinity"   Less than a second ago   Up Less than a second             e1-exec-proof-20261102
$ docker stop e1-exec-proof-20261102
e1-exec-proof-20261102
$ docker ps -a --filter 'name=e1-exec-proof-20261102'
CONTAINER ID   IMAGE          COMMAND            CREATED         STATUS                                PORTS     NAMES
202153926cdd   ubuntu:24.04   "sleep infinity"   3 seconds ago   Exited (137) Less than a second ago             e1-exec-proof-20261102
```

## 05-build

```console
$ cat Dockerfile
FROM nginx:alpine
COPY site/ /usr/share/nginx/html/
EXPOSE 80

$ cat site/index.html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>나의 개발 작업실</title>
</head>
<body>
  <h1>Docker로 실행한 첫 웹 페이지</h1>
  <p>E1-1 미션에서 바인드 마운트 변경이 반영됐습니다.</p>
</body>
</html>
$ docker build '--progress=plain' -t e1-web:proof-20261102 .
#0 building with "desktop-linux" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 100B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/nginx:alpine
#2 DONE 1.2s

#3 [internal] load .dockerignore
#3 transferring context: 2B done
#3 DONE 0.0s

#4 [internal] load build context
#4 transferring context: 335B done
#4 DONE 0.0s

#5 [1/2] FROM docker.io/library/nginx:alpine@sha256:785835ea65db4bba6f021acc0f3be91b0fef76a53fe41f8588c6698d2aed0606
#5 resolve docker.io/library/nginx:alpine@sha256:785835ea65db4bba6f021acc0f3be91b0fef76a53fe41f8588c6698d2aed0606 done
#5 CACHED

#6 [2/2] COPY site/ /usr/share/nginx/html/
#6 DONE 0.0s

#7 exporting to image
#7 exporting layers 0.0s done
#7 exporting manifest sha256:8748bf9d88655c8c7af5c62fa92baf3ecd035b604705b6a8e12c023f3e5601f0 done
#7 exporting config sha256:5787f69e6d48e91aa3b398fd79989b9e26cc4d22e2b91dbbbe2f70be3c94288a done
#7 exporting attestation manifest sha256:35567e65795910c856844ff99d827011f97a01894bde11064e914c0c97b2e78c done
#7 exporting manifest list sha256:484d64e025dbd199d2729dd17ef1567e5a92d47720cb03cce1b1f4b593b9ec40 done
#7 naming to docker.io/library/e1-web:proof-20261102 done
#7 unpacking to docker.io/library/e1-web:proof-20261102 done
#7 DONE 0.1s
$ docker image inspect e1-web:proof-20261102 --format 'Image {{.Id}} / ExposedPorts {{json .Config.ExposedPorts}}'
Image sha256:484d64e025dbd199d2729dd17ef1567e5a92d47720cb03cce1b1f4b593b9ec40 / ExposedPorts {"80/tcp":{}}
$ docker ps --filter 'name=e1-web'
CONTAINER ID   IMAGE        COMMAND                  CREATED        STATUS        PORTS                    NAMES
1b0d19820f61   e1-web:1.0   "/docker-entrypoint.…"   17 hours ago   Up 17 hours   127.0.0.1:8080->80/tcp   e1-web
$ curl -i http://localhost:8080
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100   247  100   247    0     0   151k      0 --:--:-- --:--:-- --:--:--  241k
HTTP/1.1 200 OK
Server: nginx/1.31.8
Date: Mon, 02 Nov 2026 05:24:30 GMT
Content-Type: text/html
Content-Length: 247
Last-Modified: Sun, 01 Nov 2026 12:09:43 GMT
Connection: keep-alive
ETag: "6ae72c07-f7"
Accept-Ranges: bytes

<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>나의 개발 작업실</title>
</head>
<body>
  <h1>Docker로 실행한 첫 웹 페이지</h1>
  <p>E1-1 미션에서 직접 만든 페이지입니다.</p>
</body>
</html>
$ docker logs --tail 8 e1-web
2026/11/01 12:19:15 [notice] 1#1: start worker process 35
2026/11/01 12:19:15 [notice] 1#1: start worker process 36
2026/11/01 12:19:15 [notice] 1#1: start worker process 37
172.17.0.1 - - [01/Nov/2026:12:19:31 +0000] "GET / HTTP/1.1" 200 247 "-" "curl/8.7.1" "-"
172.17.0.1 - - [02/Nov/2026:05:24:29 +0000] "GET / HTTP/1.1" 200 247 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36" "-"
172.17.0.1 - - [02/Nov/2026:05:24:29 +0000] "GET /favicon.ico HTTP/1.1" 404 555 "http://localhost:8080/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36" "-"
2026/11/02 05:24:29 [error] 31#31: *3 open() "/usr/share/nginx/html/favicon.ico" failed (2: No such file or directory), client: 172.17.0.1, server: localhost, request: "GET /favicon.ico HTTP/1.1", host: "localhost:8080", referrer: "http://localhost:8080/"
172.17.0.1 - - [02/Nov/2026:05:24:30 +0000] "GET / HTTP/1.1" 200 247 "-" "curl/8.7.1" "-"
$ docker stats --no-stream e1-web
CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O     PIDS
1b0d19820f61   e1-web    0.00%     8.574MiB / 7.748GiB   0.11%     4.66kB / 3.46kB   0B / 12.3kB   9
```

## 06-bind

```console
$ docker ps -a --filter 'name=e1-bind'
CONTAINER ID   IMAGE        COMMAND                  CREATED        STATUS        PORTS                    NAMES
c991e2dfeba0   e1-web:1.0   "/docker-entrypoint.…"   17 hours ago   Up 17 hours   127.0.0.1:8081->80/tcp   e1-bind
$ docker inspect e1-bind --format 'Status {{.State.Status}} | {{range .Mounts}}{{.Type}} {{.Source}} -> {{.Destination}} RW={{.RW}}{{end}}'
Status running | bind /Users/[USER]/Documents/Codyssey/AllInOne/GitHub/pre-course/E1-1/site -> /usr/share/nginx/html RW=false
$ pwd
$ docker run -d --name e1-bind -p 127.0.0.1:8081:80 --mount 'type=bind,source=/Users/[USER]/Documents/Codyssey/AllInOne/GitHub/pre-course/E1-1/site,target=/usr/share/nginx/html,readonly' e1-web:1.0
docker: Error response from daemon: Conflict. The container name "/e1-bind" is already in use by container "c991e2dfeba034c818effc8f59a709d7d7efee221a7a9e09bac764c330a19d6c". You have to remove (or rename) that container to be able to reuse that name.

Run 'docker run --help' for more information
$ curl -s http://localhost:8081
<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>나의 개발 작업실</title>
</head>
<body>
  <h1>Docker로 실행한 첫 웹 페이지</h1>
  <p>E1-1 미션에서 바인드 마운트 변경이 반영됐습니다.</p>
</body>
</html>
$ sed -i '' 's/바인드 마운트 변경이 반영됐습니다/바인드 마운트 변경이 다시 반영됐습니다/' site/index.html
$ cat site/index.html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>나의 개발 작업실</title>
</head>
<body>
  <h1>Docker로 실행한 첫 웹 페이지</h1>
  <p>E1-1 미션에서 바인드 마운트 변경이 다시 반영됐습니다.</p>
</body>
</html>
$ curl -s http://localhost:8081
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx/1.31.8</center>
</body>
</html>
$ curl -s http://localhost:8080
<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>나의 개발 작업실</title>
</head>
<body>
  <h1>Docker로 실행한 첫 웹 페이지</h1>
  <p>E1-1 미션에서 직접 만든 페이지입니다.</p>
</body>
</html>
$ docker inspect e1-bind --format 'Status {{.State.Status}} | {{range .Mounts}}{{.Type}} {{.Source}} -> {{.Destination}} RW={{.RW}}{{end}}'
Status running | bind /Users/[USER]/Documents/Codyssey/AllInOne/GitHub/pre-course/E1-1/site -> /usr/share/nginx/html RW=false
```

## 07-port-conflict

```console
$ docker ps --filter 'publish=8080'
CONTAINER ID   IMAGE        COMMAND                  CREATED        STATUS        PORTS                    NAMES
1b0d19820f61   e1-web:1.0   "/docker-entrypoint.…"   17 hours ago   Up 17 hours   127.0.0.1:8080->80/tcp   e1-web
$ docker run -d --name e1-port-proof-20261102 -p 127.0.0.1:8080:80 e1-web:proof-20261102
dcdc054ccacca3ae4e57494a8ca34afb31d91cfab3b29735cdb09863f15ce092
docker: Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint e1-port-proof-20261102 (3c22a0efdb77658222e02d80aea476aca634e41bd3acefb1a35a79967cececf9): Bind for 127.0.0.1:8080 failed: port is already allocated

Run 'docker run --help' for more information
$ docker ps -a --filter 'name=e1-port-proof-20261102'
CONTAINER ID   IMAGE                   COMMAND                  CREATED                  STATUS    PORTS     NAMES
dcdc054ccacc   e1-web:proof-20261102   "/docker-entrypoint.…"   Less than a second ago   Created             e1-port-proof-20261102
$ docker ps --filter 'publish=8080'
CONTAINER ID   IMAGE        COMMAND                  CREATED        STATUS        PORTS                    NAMES
1b0d19820f61   e1-web:1.0   "/docker-entrypoint.…"   17 hours ago   Up 17 hours   127.0.0.1:8080->80/tcp   e1-web
$ lsof -nP -iTCP:8080 -sTCP:LISTEN
COMMAND    PID      USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
com.docke 2632 [USER]   86u  IPv4 0x44afb38ed5741a53      0t0  TCP 127.0.0.1:8080 (LISTEN)
$ docker rm e1-port-proof-20261102
e1-port-proof-20261102
$ docker run -d --name e1-web-proof-8082 -p 127.0.0.1:8082:80 e1-web:proof-20261102
1777cffc90193d64865d81d39a977fa168bdcb8d7b30e77d23fc8e5ddee04eaa
$ curl --retry 3 --retry-connrefused --retry-delay 1 -i http://localhost:8082
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (52) Empty reply from server
$ docker ps --filter 'name=e1-web-proof-8082'
CONTAINER ID   IMAGE                   COMMAND                  CREATED                  STATUS                  PORTS                    NAMES
1777cffc9019   e1-web:proof-20261102   "/docker-entrypoint.…"   Less than a second ago   Up Less than a second   127.0.0.1:8082->80/tcp   e1-web-proof-8082
```

## 08-volume

```console
$ docker volume create e1-proof-data-20261102
e1-proof-data-20261102
$ docker run --name e1-volume-proof-20261102 --mount 'source=e1-proof-data-20261102,target=/data' ubuntu:24.04 sh -c 'echo preserved-20261102 > /data/proof.txt; cat /data/proof.txt'
preserved-20261102
$ docker rm e1-volume-proof-20261102
e1-volume-proof-20261102
$ docker run --rm --mount 'source=e1-proof-data-20261102,target=/data' ubuntu:24.04 cat /data/proof.txt
preserved-20261102
$ docker volume inspect e1-proof-data-20261102 --format 'Name {{.Name}} / Driver {{.Driver}}'
Name e1-proof-data-20261102 / Driver local
```

## 09-cleanup

```console
$ docker ps -a --filter 'name=proof'
CONTAINER ID   IMAGE                   COMMAND                  CREATED                  STATUS                       PORTS                    NAMES
1777cffc9019   e1-web:proof-20261102   "/docker-entrypoint.…"   Less than a second ago   Up Less than a second        127.0.0.1:8082->80/tcp   e1-web-proof-8082
202153926cdd   ubuntu:24.04            "sleep infinity"         7 seconds ago            Exited (137) 4 seconds ago                            e1-exec-proof-20261102
3e3e949f615a   ubuntu:24.04            "bash"                   7 seconds ago            Exited (0) 7 seconds ago                              e1-ubuntu-proof-20261102
72b105483ccc   hello-world             "/hello"                 8 seconds ago            Exited (0) 8 seconds ago                              e1-hello-proof-20261102
$ docker rm e1-hello-proof-20261102 e1-ubuntu-proof-20261102 e1-exec-proof-20261102
e1-hello-proof-20261102
e1-ubuntu-proof-20261102
e1-exec-proof-20261102
$ docker tag e1-web:proof-20261102 e1-cleanup-proof:temporary
$ docker images e1-cleanup-proof
IMAGE                        ID             DISK USAGE   CONTENT SIZE   EXTRA
e1-cleanup-proof:temporary   484d64e025db       93.2MB         26.3MB   U
$ docker rmi e1-cleanup-proof:temporary
Untagged: e1-cleanup-proof:temporary
$ docker images e1-cleanup-proof
IMAGE   ID             DISK USAGE   CONTENT SIZE   EXTRA
$ docker ps -a --filter 'name=proof'
CONTAINER ID   IMAGE                   COMMAND                  CREATED        STATUS                  PORTS                    NAMES
1777cffc9019   e1-web:proof-20261102   "/docker-entrypoint.…"   1 second ago   Up Less than a second   127.0.0.1:8082->80/tcp   e1-web-proof-8082
```

## 10-git-config

```console
$ git --version
git version 2.55.0
$ git config --list
$ python3 -c 'import sys; allowed=("user.name=","user.email=","init.defaultbranch=","remote.origin.url=","branch.main.remote=","branch.main.merge="); [print("user.email=[MASKED]" if s.lower().startswith("user.email=") else s.rstrip()) for s in sys.stdin if s.lower().startswith(allowed)]'
user.name=2dion
user.email=[MASKED]
init.defaultbranch=main
remote.origin.url=https://github.com/2dion/daejeon-codyssey-ai-all-in-one-1st.git
branch.main.remote=origin
branch.main.merge=refs/heads/main
$ git status --short --branch
## No commits yet on main...origin/main [gone]
A  ../../.gitignore
?? ../
$ git remote -v
origin	https://github.com/2dion/daejeon-codyssey-ai-all-in-one-1st.git (fetch)
origin	https://github.com/2dion/daejeon-codyssey-ai-all-in-one-1st.git (push)
$ git ls-remote --heads origin
```

## 11-http-final

```console
$ curl -fsSi http://localhost:8080
HTTP/1.1 200 OK
Server: nginx/1.31.8
Date: Mon, 02 Nov 2026 05:28:06 GMT
Content-Type: text/html
Content-Length: 247
Last-Modified: Sun, 01 Nov 2026 12:09:43 GMT
Connection: keep-alive
ETag: "6ae72c07-f7"
Accept-Ranges: bytes

<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>나의 개발 작업실</title>
</head>
<body>
  <h1>Docker로 실행한 첫 웹 페이지</h1>
  <p>E1-1 미션에서 직접 만든 페이지입니다.</p>
</body>
</html>
$ curl -fsSi http://localhost:8081
HTTP/1.1 200 OK
Server: nginx/1.31.8
Date: Mon, 02 Nov 2026 05:28:06 GMT
Content-Type: text/html
Content-Length: 270
Last-Modified: Mon, 02 Nov 2026 05:24:31 GMT
Connection: keep-alive
ETag: "6ae81e8f-10e"
Accept-Ranges: bytes

<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>나의 개발 작업실</title>
</head>
<body>
  <h1>Docker로 실행한 첫 웹 페이지</h1>
  <p>E1-1 미션에서 바인드 마운트 변경이 다시 반영됐습니다.</p>
</body>
</html>
$ curl -fsSi http://localhost:8082
HTTP/1.1 200 OK
Server: nginx/1.31.8
Date: Mon, 02 Nov 2026 05:28:06 GMT
Content-Type: text/html
Content-Length: 263
Last-Modified: Sun, 01 Nov 2026 12:27:00 GMT
Connection: keep-alive
ETag: "6ae73014-107"
Accept-Ranges: bytes

<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>나의 개발 작업실</title>
</head>
<body>
  <h1>Docker로 실행한 첫 웹 페이지</h1>
  <p>E1-1 미션에서 바인드 마운트 변경이 반영됐습니다.</p>
</body>
</html>
$ docker exec e1-bind ls -l /usr/share/nginx/html
total 4
-rw-r--r--    1 root     root           270 Nov  2 05:24 index.html
```

## 12-cli-capture-a

```console
$ mkdir -p practice/cli-capture-20261102
$ cd practice/cli-capture-20261102
$ pwd
/Users/[USER]/Documents/Codyssey/AllInOne/GitHub/pre-course/E1-1/practice/cli-capture-20261102
$ echo 'hello codyssey'
$ touch empty.txt
$ ls -la
total 8
drwxr-xr-x@ 4 [USER]  staff  128 Nov  2 14:28 .
drwxr-xr-x  6 [USER]  staff  192 Nov  2 14:28 ..
-rw-r--r--@ 1 [USER]  staff    0 Nov  2 14:28 empty.txt
-rw-r--r--@ 1 [USER]  staff   15 Nov  2 14:28 original.txt
$ cat original.txt
hello codyssey
$ cp original.txt copy.txt
$ ls -l
total 16
-rw-r--r--@ 1 [USER]  staff  15 Nov  2 14:28 copy.txt
-rw-r--r--@ 1 [USER]  staff   0 Nov  2 14:28 empty.txt
-rw-r--r--@ 1 [USER]  staff  15 Nov  2 14:28 original.txt
$ cat copy.txt
hello codyssey
```

## 13-cli-capture-b

```console
$ cd practice/cli-capture-20261102
$ mv copy.txt renamed.txt
$ ls -l
total 16
-rw-r--r--@ 1 [USER]  staff   0 Nov  2 14:28 empty.txt
-rw-r--r--@ 1 [USER]  staff  15 Nov  2 14:28 original.txt
-rw-r--r--@ 1 [USER]  staff  15 Nov  2 14:28 renamed.txt
$ mkdir moved
$ mv renamed.txt moved/
$ ls -la . moved
.:
total 8
drwxr-xr-x@ 5 [USER]  staff  160 Nov  2 14:28 .
drwxr-xr-x  6 [USER]  staff  192 Nov  2 14:28 ..
-rw-r--r--@ 1 [USER]  staff    0 Nov  2 14:28 empty.txt
drwxr-xr-x@ 3 [USER]  staff   96 Nov  2 14:28 moved
-rw-r--r--@ 1 [USER]  staff   15 Nov  2 14:28 original.txt

moved:
total 8
drwxr-xr-x@ 3 [USER]  staff   96 Nov  2 14:28 .
drwxr-xr-x@ 5 [USER]  staff  160 Nov  2 14:28 ..
-rw-r--r--@ 1 [USER]  staff   15 Nov  2 14:28 renamed.txt
$ rm moved/renamed.txt
$ ls -la moved
total 0
drwxr-xr-x@ 2 [USER]  staff   64 Nov  2 14:28 .
drwxr-xr-x@ 5 [USER]  staff  160 Nov  2 14:28 ..
$ rmdir moved
$ ls -la
total 8
drwxr-xr-x@ 4 [USER]  staff  128 Nov  2 14:28 .
drwxr-xr-x  6 [USER]  staff  192 Nov  2 14:28 ..
-rw-r--r--@ 1 [USER]  staff    0 Nov  2 14:28 empty.txt
-rw-r--r--@ 1 [USER]  staff   15 Nov  2 14:28 original.txt
$ cd ../..
$ pwd
/Users/[USER]/Documents/Codyssey/AllInOne/GitHub/pre-course/E1-1
```

## 14-bind-final

```console
$ docker inspect e1-bind --format '{{range .Mounts}}{{.Type}} {{.Source}} -> {{.Destination}} RW={{.RW}}{{end}}'
bind /Users/[USER]/Documents/Codyssey/AllInOne/GitHub/pre-course/E1-1/site -> /usr/share/nginx/html RW=false
$ curl -fsS http://localhost:8081
$ grep '<p>'
  <p>E1-1 미션에서 바인드 마운트 변경이 다시 반영됐습니다.</p>
$ curl -fsS http://localhost:8080
$ grep '<p>'
  <p>E1-1 미션에서 직접 만든 페이지입니다.</p>
```

## 15-port-final

```console
$ docker ps --filter 'publish=8080'
CONTAINER ID   IMAGE        COMMAND                  CREATED        STATUS        PORTS                    NAMES
1b0d19820f61   e1-web:1.0   "/docker-entrypoint.…"   17 hours ago   Up 17 hours   127.0.0.1:8080->80/tcp   e1-web
$ lsof -nP -iTCP:8080 -sTCP:LISTEN
COMMAND    PID      USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
com.docke 2632 [USER]   86u  IPv4 0x44afb38ed5741a53      0t0  TCP 127.0.0.1:8080 (LISTEN)
$ docker ps --filter 'name=e1-web-proof-8082'
CONTAINER ID   IMAGE                   COMMAND                  CREATED         STATUS         PORTS                    NAMES
1777cffc9019   e1-web:proof-20261102   "/docker-entrypoint.…"   3 minutes ago   Up 3 minutes   127.0.0.1:8082->80/tcp   e1-web-proof-8082
$ curl -fsSi http://localhost:8082
HTTP/1.1 200 OK
Server: nginx/1.31.8
Date: Mon, 02 Nov 2026 05:28:06 GMT
Content-Type: text/html
Content-Length: 263
Last-Modified: Sun, 01 Nov 2026 12:27:00 GMT
Connection: keep-alive
ETag: "6ae73014-107"
Accept-Ranges: bytes

<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>나의 개발 작업실</title>
</head>
<body>
  <h1>Docker로 실행한 첫 웹 페이지</h1>
  <p>E1-1 미션에서 바인드 마운트 변경이 반영됐습니다.</p>
</body>
</html>
```

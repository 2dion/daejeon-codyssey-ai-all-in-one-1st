# E1-1: 내 컴퓨터에 개발자용 작업실 꾸미기

터미널·권한·Docker·Git을 사용해 개발 환경을 구성하고, NGINX 정적 웹 서버의 포트 매핑·바인드 마운트·볼륨 영속성을 검증한 기록이다.

**2026-11-02 보완 검증:** CLI 생성·복사·이동·삭제, 파일/디렉터리 권한 변화, 이미지 빌드, HTTP 접속, 바인드 마운트 전후, 볼륨 삭제 전후 검증을 수행했다. 아래 명령·로그·캡처는 실제 실행 결과다. 자동화 도구가 명령 실행과 문서·증거 정리를 보조했으며, 설명형 문항은 작성자가 직접 이해하고 설명할 수 있어야 한다.

- [전체 실제 명령·출력](evidence/2026-11-02/LOGS.md)
- [증거 사진 목록](screenshots/README.md)
- [개념 학습 기록](미션%20사전%20질문과%20답변.md)
- GitHub 업로드·VS Code 연동 상태는 [Git 검증](#8-git과-github)을 참고한다.

## 1. 실행 환경

| 항목 | 이번 검증 결과 |
| --- | --- |
| OS | macOS 26.6.2, Build 25G83 |
| 셸 | /bin/zsh |
| 터미널 | VS Code 통합 터미널(TERM_PROGRAM=vscode). 최초 수집 일부는 자동화 셸에서 실행 |
| Docker CLI / Server | 29.9.2 / 29.9.2 |
| Docker 실행 환경 | Docker Desktop, context desktop-linux, aarch64 |
| Git | 2.55.0 |
| 베이스 이미지 | nginx:alpine, ubuntu:24.04, hello-world |

macOS에 Ubuntu 자체를 설치한 것이 아니라 Docker의 Linux 실행 환경 안에서 Ubuntu 컨테이너를 실행했다. 실제 버전 출력은 [환경 로그](evidence/2026-11-02/01-environment.txt)에 있다. 컨테이너의 상태와 포트 점유는 검증 시점의 값이다.

![실제 통합 터미널 환경 점검](screenshots/20261102-terminal-environment.png)

## 2. 구성 기준과 재현 방법

```text
E1-1/
├── Dockerfile                 # 이미지를 만드는 지시문
├── site/index.html            # 이미지에 넣거나 마운트할 정적 콘텐츠
├── practice/                  # CLI·권한 실험 대상
├── evidence/2026-11-02/        # 실제 명령·출력과 수집에 사용한 스크립트
├── screenshots/               # 실제 브라우저·터미널 및 기존 증거 사진
├── 미션 사전 질문과 답변.md    # 개념 학습
└── README.md                  # 절차와 검증 결과의 진입점
```

이미지 재료, 실습 대상, 실행 증거를 역할별로 분리했다. README의 상대 링크는 저장소를 옮겨도 내부 관계를 유지한다. 비밀 파일과 OS 임시 파일은 상위 저장소의 .gitignore로 제외한다. 빈 디렉터리는 Git으로 저장되지 않으므로 권한 실습에서 mkdir로 생성한다.

다른 컴퓨터에서는 Docker를 실행하고 저장소 루트에서 다음 절차를 따른다. 아래 이름·포트가 이미 사용 중이면 먼저 상태를 확인하고 다른 이름이나 비어 있는 호스트 포트를 선택한다. `evidence/`의 .sh는 당시 수집 절차이며 일부는 의도적 충돌·삭제를 포함하므로 일괄 재실행용이 아니다.

```bash
cd pre-course/E1-1
pwd
cat Dockerfile
docker build -t e1-web:1.0 .
docker run -d --name e1-web -p 127.0.0.1:8080:80 e1-web:1.0
curl -fsSi http://localhost:8080
```

NGINX가 시작하기 전에 접속하면 실패할 수 있다. docker ps와 docker logs로 상태를 확인하고 다시 curl한다. 재현 시점의 site 내용으로 빌드하므로 과거 이미지의 문구와 다를 수 있다. nginx:alpine은 변할 수 있는 태그이며 바이트 단위로 동일한 빌드까지 보장하는 것은 아니다.

## 3. 수행 체크리스트

| 요구 항목 | 상태 | 증거 |
| --- | --- | --- |
| 경로·목록·생성·내용 확인·복사·이동·삭제 | 검증 완료 | [CLI 로그](evidence/2026-11-02/02-cli.txt), 아래 터미널 사진 |
| 파일·디렉터리 권한 실제 변화 | 검증 완료 | [권한 로그](evidence/2026-11-02/03-permissions.txt), 600→644·700→755 사진 |
| Docker 설치·엔진 점검 | 검증 완료 | [환경 로그](evidence/2026-11-02/01-environment.txt) |
| hello-world·Ubuntu·exec·stop | 검증 완료 | [기본 운영 로그](evidence/2026-11-02/04-docker-basics.txt) |
| 이미지/컨테이너 목록·정리 | 검증 완료 | [정리 로그](evidence/2026-11-02/09-cleanup.txt) |
| Dockerfile 빌드·실행·logs·stats | 검증 완료 | [빌드/운영 로그](evidence/2026-11-02/05-build.txt), [새 이미지 실행 로그](evidence/2026-11-02/07-port-conflict.txt) |
| 포트 매핑·브라우저 접속 | 검증 완료 | 아래 주소창 포함 8080·8081 사진, [최종 HTTP 200 로그](evidence/2026-11-02/11-http-final.txt) |
| 바인드 마운트 전후 | 검증 완료 | [변경 전후](evidence/2026-11-02/06-bind.txt), [정상 최종 응답](evidence/2026-11-02/14-bind-final.txt) |
| 볼륨 영속성 | 검증 완료 | [새 검증](evidence/2026-11-02/08-volume.txt), [기존 사진](screenshots/8.png) |
| Git 설정 | 검증 완료 | [이메일을 가린 설정 로그](evidence/2026-11-02/10-git-config.txt) |
| 커밋·푸시·VS Code 연동 | 최종 확인 중 | 8장에 실제 확인 결과 기록 |
| 트러블슈팅 2건 이상 | 3건 기록 | 9장 |

## 4. 터미널 기본 조작과 권한

### 4.1 생성·복사·이동·삭제

`practice/cli-proof-20261102`에서 파일을 만들고 복사했다. copy.txt를 renamed.txt로 바꾼 뒤 moved/로 옮기고 파일·빈 폴더를 삭제했다. 출력이 없는 cp·mv·rm은 다음 ls 목록으로 결과를 확인했다. [전체 텍스트 로그](evidence/2026-11-02/02-cli.txt)

![VS Code 터미널 생성·복사](screenshots/20261102-terminal-cli-a.png)

실제 통합 터미널에서 별도 `cli-capture-20261102` 폴더를 사용해 생성·내용 확인·복사를 다시 실행한 사진이다.

![VS Code 터미널 이름 변경·이동·삭제](screenshots/20261102-terminal-cli-b.png)

이름 변경 후 renamed.txt가 보이고, 이동 후 moved/ 안에 보인다. rm 뒤에는 moved/가 비었으며, rmdir 뒤에는 상위 목록에서 moved/가 사라진다.

### 4.2 권한 변화

처음부터 644·755였던 대상을 같은 값으로 바꾸는 것은 변화 검증이 아니다. 이번에는 다음과 같이 실제로 다르게 설정했다. [전체 로그](evidence/2026-11-02/03-permissions.txt)

```console
$ chmod 600 practice/permission-file
$ ls -l practice/permission-file
-rw-------@ ... practice/permission-file
$ chmod 644 practice/permission-file
$ ls -l practice/permission-file
-rw-r--r--@ ... practice/permission-file
$ chmod 700 practice/permission-dir
$ ls -ld practice/permission-dir
drwx------@ ... practice/permission-dir
$ chmod 755 practice/permission-dir
$ ls -ld practice/permission-dir
drwxr-xr-x@ ... practice/permission-dir
```

![실제 파일·디렉터리 권한 변경 전후](screenshots/20261102-terminal-permissions.png)

r=4, w=2, x=1을 소유자·그룹·그 외 순서로 더한다. 644는 rw-/r--/r--, 755는 rwx/r-x/r-x다. 디렉터리의 x는 경로를 통과하는 권한이다. 현재 umask는 022였으며, 생성 시 요청된 모드에서 해당 권한 비트를 제거한다. 과거에도 같은 umask였다고 단정하지 않는다. macOS의 @는 확장 속성을 나타내며 rwx 숫자와 별개다.

## 5. Docker 기본 운영과 커스텀 이미지

[기본 운영 전체 로그](evidence/2026-11-02/04-docker-basics.txt)에 pull, images, hello-world, Ubuntu의 pwd/ls/echo, ps/ps -a, exec, stop 결과가 있다. 이번 Ubuntu 보완은 표준입력으로 bash에 명령을 전달했고, 기존 대화형 진입·exit 증거는 [4-4.png](screenshots/4-4.png)에 있다.

```console
$ docker run --name e1-hello-proof-20261102 hello-world
Hello from Docker!
$ docker exec e1-exec-proof-20261102 bash -c 'pwd; echo hello-from-exec'
/
hello-from-exec
```

bash가 주 프로세스인 컨테이너는 bash 종료 후 Exited (0)이었다. sleep infinity가 주 프로세스인 컨테이너는 exec 명령 종료 후에도 실행 중이었고 docker stop 이후 종료됐다. attach는 기존 주 프로세스의 입출력에 연결하고 exec는 새 프로세스를 실행한다. -it 자체가 컨테이너 수명을 유지하는 것은 아니다.

### 직접 작성한 Dockerfile

```Dockerfile
FROM nginx:alpine
COPY site/ /usr/share/nginx/html/
EXPOSE 80
```

- 베이스: 웹 서버가 포함된 nginx:alpine을 사용했다.
- 커스텀 목적: COPY로 직접 만든 site/index.html을 기본 웹 루트에 넣어 기본 페이지를 교체했다. 미션의 선택지 A에 해당한다.
- EXPOSE 80은 포트 안내이며 호스트 포트를 공개하지 않는다. 실제 연결은 run의 -p다.
- 이번 재빌드 태그는 e1-web:proof-20261102이며, 이 이미지로 8082 웹 컨테이너를 실행했다. 빌드 시 소스는 바인드 변경 전 문구였다.

[빌드 완료·image inspect·logs·stats](evidence/2026-11-02/05-build.txt) · [새 이미지 실행과 포트 변경](evidence/2026-11-02/07-port-conflict.txt) · [최종 8082 HTTP 200](evidence/2026-11-02/11-http-final.txt)

정리에서는 이번에 만든 종료 컨테이너 3개를 지정해 삭제했다. 임시 이미지 태그 e1-cleanup-proof:temporary도 삭제했다. 출력은 Untagged이며, 다른 태그가 참조하는 이미지 계층 전체가 삭제됐다는 뜻은 아니다. [목록·정리 전후](evidence/2026-11-02/09-cleanup.txt)

## 6. 포트 매핑과 바인드 마운트

### 6.1 주소창 포함 브라우저 증거

![Aside 브라우저 localhost 8080](screenshots/20261102-browser-8080.png)

실제 Aside 주소창에 localhost:8080이 보이고, 본문은 “Docker로 실행한 첫 웹 페이지”, “E1-1 미션에서 직접 만든 페이지입니다.”다. 8080은 기존 이미지로 실행한 e1-web이다.

![Aside 브라우저 localhost 8081](screenshots/20261102-browser-8081.png)

8081은 호스트 site/가 연결된 e1-bind다. 호스트 파일 변경 후 “바인드 마운트 변경이 다시 반영됐습니다.”가 보인다. [8080·8081·8082 최종 명령과 HTTP 200 응답](evidence/2026-11-02/11-http-final.txt)

### 6.2 마운트와 변경 전후

```bash
docker run -d --name e1-bind   -p 127.0.0.1:8081:80   --mount type=bind,source="$(pwd)/site",target=/usr/share/nginx/html,readonly   e1-web:1.0
```

명령은 E1-1 폴더에서 실행한다. source는 호스트의 절대 경로가 되고 target은 컨테이너 내부 경로다. readonly는 컨테이너 쪽 쓰기를 막으며 호스트 파일 수정은 가능하다.

이번에는 기존 e1-bind가 정확한 site/를 RW=false로 연결하고 실행 중임을 inspect로 확인했다. 같은 이름으로 새 run을 시도하면 충돌하므로 **새로 만들지 않고 기존 컨테이너를 재사용**했다. [이름 충돌 재현·inspect·변경 전후 원본](evidence/2026-11-02/06-bind.txt)

- 변경 전 8081: “바인드 마운트 변경이 반영됐습니다.”
- 호스트 변경 후 최종 8081: “바인드 마운트 변경이 다시 반영됐습니다.”
- 8080: “직접 만든 페이지입니다.” 유지.

수정 직후 첫 curl은 404였다. 그 순간의 원인은 확정하지 않았고, 파일 존재와 실제 응답을 재확인해 최종 HTTP 200·변경 문구를 확인했다. 초기 오류를 삭제하지 않고 원본에 남겼다. [최종 마운트·응답 비교](evidence/2026-11-02/14-bind-final.txt)

![실제 마운트와 응답 비교](screenshots/20261102-terminal-bind.png)

## 7. 볼륨 영속성

이번 보완은 기존 e1-data를 덮어쓰지 않고 별도 이름 e1-proof-data-20261102를 사용했다. [전체 명령·출력](evidence/2026-11-02/08-volume.txt)

```console
$ docker volume create e1-proof-data-20261102
e1-proof-data-20261102
$ docker run --name e1-volume-proof-20261102 --mount source=e1-proof-data-20261102,target=/data ubuntu:24.04 sh -c 'echo preserved-20261102 > /data/proof.txt; cat /data/proof.txt'
preserved-20261102
$ docker rm e1-volume-proof-20261102
e1-volume-proof-20261102
$ docker run --rm --mount source=e1-proof-data-20261102,target=/data ubuntu:24.04 cat /data/proof.txt
preserved-20261102
```

컨테이너를 지운 뒤 같은 볼륨을 새 컨테이너에 붙여 같은 내용을 읽었다. 컨테이너 쓰기 영역과 볼륨의 수명이 분리된다는 증거다. 다른 컴퓨터로 자동 이전되거나 볼륨 자체 삭제에도 데이터가 보존된다는 뜻은 아니다. docker rm -v는 익명 볼륨을 제거하며 이름 있는 이 볼륨은 제거하지 않는다. 기존 실습 증거도 [8.png](screenshots/8.png)에 남아 있다.

![실제 볼륨 삭제 후 데이터 재확인](screenshots/20261102-terminal-volume.png)

## 8. Git과 GitHub

설정에서 user.name=2dion, init.defaultBranch=main, origin의 HTTPS 주소를 확인했다. 이메일은 공개 로그에서 가렸고 그 외 불필요한 설정은 제외했다. [설정·초기 상태](evidence/2026-11-02/10-git-config.txt)

초기 상태는 No commits yet였으며 git ls-remote --heads origin 결과도 비어 있었다. 이 기록은 **보완 시작 시점**이다. 이후 커밋·푸시 결과는 별도로 기록한다.

<!-- GIT_FINAL -->

Git은 로컬 버전 관리 도구이고 GitHub는 원격 저장소 공유 플랫폼이다. 로컬 커밋, 원격 push, VS Code 로그인·연동을 각각 확인한다. HTTPS origin이므로 SSH 인증 성공을 실제 SSH 푸시 증거로 대신하지 않는다.

## 9. 트러블슈팅

### 사례 1. 컨테이너 이름 충돌: 기존 컨테이너 재사용

- 문제: e1-bind 이름으로 run을 시도하면 Conflict 오류가 발생했다. 기존 오류는 screenshots/7-1.png에도 있고 이번에도 의도적으로 재현했다.
- 가설: 이전에 생성한 컨테이너가 같은 이름을 점유했다.
- 확인: ps -a에서 e1-bind가 실행 중이며 inspect에서 현재 프로젝트 site/의 읽기 전용 bind mount를 확인했다.
- 해결/대안: 동일 설정의 컨테이너를 새로 만들 필요가 없어 기존 실행 컨테이너를 재사용했다. 불필요한 삭제를 하지 않았다.
- 결과: 호스트 수정 후 8081에서 변경 문구와 HTTP 200을 확인했다. 초기 404와 재확인 결과를 함께 보존했다.
- 증거: [06-bind](evidence/2026-11-02/06-bind.txt), [11-http-final](evidence/2026-11-02/11-http-final.txt), [14-bind-final](evidence/2026-11-02/14-bind-final.txt).

### 사례 2. chmod 실행은 성공했지만 변화가 없는 검증

- 문제: 기존 스크린샷 2-1.png에서 이미 파일은 644·디렉터리는 755여서 동일 값 chmod 후 변화가 없었다.
- 가설: chmod 실패 또는 처음부터 같은 모드.
- 확인: 최초 캡처의 권한과 현재 ls 출력을 비교했다. 이번 umask는 022였다.
- 조치: 파일을 600→644, 디렉터리를 700→755로 바꾸고 매번 ls 출력으로 비교했다.
- 결과: rw-------→rw-r--r--, rwx------→rwxr-xr-x 변화 확인. 이는 서비스 장애가 아니라 실험·검증 방법을 바로잡은 사례다.
- 증거: [권한 로그](evidence/2026-11-02/03-permissions.txt), [터미널 사진](screenshots/20261102-terminal-permissions.png).

### 사례 3. 호스트 8080 포트 충돌: 의도적 재현

- 문제: 기존 e1-web이 8080을 사용하는 상태에서 새 컨테이너를 같은 포트로 실행해 port is already allocated가 발생했다.
- 가설: 다른 컨테이너 또는 호스트 프로세스가 점유 중이다.
- 확인: docker ps --filter publish=8080에서 e1-web, lsof에서 Docker의 중계 프로세스가 보였다.
- 조치: 실패 후 Created 상태로 남은 실습 컨테이너만 삭제하고 새 컨테이너의 호스트 포트를 8082로 바꿨다. 컨테이너 포트는 80을 유지했다.
- 결과: 시작 직후 첫 요청은 Empty reply였고, 이후 재검증에서 8082의 HTTP 200과 본문을 확인했다. 즉시 응답하지 않는 것과 최종 실행 실패를 구분했다.
- 증거: [충돌·조치 원본](evidence/2026-11-02/07-port-conflict.txt), [최종 진단·응답](evidence/2026-11-02/15-port-final.txt).

![실제 포트 점유 진단과 8082 응답](screenshots/20261102-terminal-port.png)

## 10. 평가 설명 준비

| 질문 | 설명 요점 |
| --- | --- |
| 이미지와 컨테이너 | Dockerfile+소스→build→이미지→run→컨테이너. 컨테이너 변경이 이미지로 역반영되지는 않음 |
| 내부 포트와 매핑 | 이번 macOS Docker 기본 환경에서는 컨테이너 네트워크 공간과 맥 localhost가 다름. -p는 호스트 포트를 내부 서비스로 연결 |
| 절대·상대 경로 선택 | 마운트 source처럼 대상을 명확히 지정할 때 절대 경로. 저장소 내부 링크·COPY 재료는 상대 관계로 관리 |
| 볼륨과 바인드 | 바인드: 호스트 특정 폴더 연결과 변경 확인. 볼륨: Docker 관리 저장 공간, 컨테이너 삭제 후 재사용 |
| 포트 충돌 진단 순서 | 오류 종류→docker ps의 publish 필터→lsof→필요 없는 대상 중지 또는 호스트 포트 변경→curl·브라우저 재검증 |
| 가장 어려웠던 점 | 명령 성공과 변화 검증을 구분한 권한 실험. 기존 상태를 읽고 다른 권한을 거쳐 실제 차이를 확인 |

설명은 결론 한 문장→README 증거 위치→필요한 명령 시연 순서로 한다. Compose·멀티 컨테이너·환경 변수·SSH 푸시는 이번 필수 보완의 완료 항목에 포함하지 않는다.

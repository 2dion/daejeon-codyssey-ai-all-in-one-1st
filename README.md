# Codyssey AI All-in-One 학습 기록

코디세이 AI All-in-One 과정에서 수행한 미션의 코드, 실행 방법, 검증 로그와 학습 내용을 정리하는 저장소입니다.

## 학습 기록

| 과정 | 내용 | 바로가기 |
| --- | --- | --- |
| 입학 연수 · Pre-course | 개발 환경 구성 및 기초 도구 실습 | [Pre-course 안내](pre-course/README.md) |

## 현재 등록된 미션

| 미션 | 주요 학습 내용 | 결과물 |
| --- | --- | --- |
| E1-1 · 내 컴퓨터에 개발자용 작업실 꾸미기 | CLI, 파일 권한, Docker, 포트 매핑, 바인드 마운트, 볼륨, Git/GitHub | [미션 README](pre-course/E1-1/README.md) |

## 저장소 구조

```text
.
├── README.md
├── .gitignore
└── pre-course/
    ├── README.md
    └── E1-1/
        ├── README.md
        ├── Dockerfile
        ├── site/
        ├── practice/
        ├── evidence/
        └── screenshots/
```

## 확인 방법

1. 과정별 README에서 미션을 선택합니다.
2. 미션 README의 실행 환경과 재현 절차를 확인합니다.
3. 연결된 소스코드, 실제 명령·출력 로그, 캡처로 수행 결과를 확인합니다.

E1-1의 소스코드는 [Dockerfile](pre-course/E1-1/Dockerfile)과 [웹 페이지](pre-course/E1-1/site/index.html)에 있으며, [2026-11-02 실행 로그](pre-course/E1-1/evidence/2026-11-02/LOGS.md)와 [증거 사진 목록](pre-course/E1-1/screenshots/README.md)을 함께 제공합니다.

## 기록 원칙

- 실행한 작업과 개념 설명, 미확인 항목을 구분합니다.
- 명령과 실제 출력으로 검증하며, 의도적으로 재현한 오류는 표시합니다.
- 토큰·비밀번호·개인키는 올리지 않고 필요한 개인정보는 가리거나 제출 대상에서 제외합니다.
- 자동화 도구가 보조한 실행·정리는 해당 미션 문서에 밝힙니다.

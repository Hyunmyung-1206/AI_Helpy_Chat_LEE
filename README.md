# AI Helpy Chat QA Automation

> AI Helpy Chat의 Quiz, PPT, Deep Investigation 생성 기능을 Selenium + pytest로 자동 검증하는 QA 자동화 프로젝트입니다.  
> Docker Compose 기반 Selenium 실행 환경과 Jenkins CI를 구성하고, JUnit/Allure Report, Slack, Jira 연동으로 테스트 결과 추적까지 자동화했습니다.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-9.x-0A9EDC?logo=pytest&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.x-43B02A?logo=selenium&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-CI-D24939?logo=jenkins&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-Report-FF6B6B)

---

## Key Achievements

| Area | Implementation |
|---|---|
| Test target | Quiz, PPT, Deep Investigation 생성 기능 |
| Test design | 입력값 검증, 경계값 분석, 버튼 상태, 생성 중지, 다운로드 검증 |
| Test structure | 상세 테스트와 slow E2E 테스트 분리 |
| Parallel run | `pytest-xdist` 3 workers |
| Docker | `tests` 컨테이너와 `selenium/standalone-chrome` 컨테이너 분리 |
| CI | Jenkins Pipeline에서 Docker Compose 기반 테스트 실행 |
| Report | JUnit XML + Allure Report |
| Notification | Slack 요약/실패 알림, Jira 이슈 연동 |
| Known issue | `pytest.mark.xfail`로 알려진 버그 추적 |

---

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.14 |
| Test framework | pytest, pytest-xdist |
| UI automation | Selenium WebDriver |
| Browser runtime | selenium/standalone-chrome |
| Container | Docker, Docker Compose |
| CI | Jenkins Declarative Pipeline |
| Report | JUnit, Allure Report |
| Integration | Slack Incoming Webhook, Jira API |
| Config | python-dotenv, Jenkins Credentials |

---

## Test Scope

### Quiz Create

- 주제 입력값 검증
- 퀴즈 유형 드롭다운 검증
- 난이도 드롭다운 검증
- 주제 삭제 시 버튼 상태 검증
- 공백 주제 검증
- 생성 중지 검증
- slow E2E 생성 검증

### PPT Create

- 주제/지시사항 입력값 검증
- 슬라이드 수, 섹션 수 경계값 검증
- 숫자 필드 비정상 입력 검증
- 생성 버튼 상태 검증
- 공백 주제 known issue 추적
- 생성 중지 검증
- slow E2E 생성 및 다운로드 검증

### Deep Investigation Create

- 주제/지시사항 입력값 검증
- 다시 생성 버튼 상태 검증
- 공백 주제 known issue 추적
- 생성 중지 검증
- slow E2E 생성 및 Markdown 다운로드 검증

---

## Test Design Strategy

이 프로젝트는 단순한 UI 클릭 자동화가 아니라, 생성 기능의 주요 리스크를 기준으로 테스트를 분리했습니다.

- **경계값 분석**: 주제 길이, 지시사항 길이, PPT 슬라이드/섹션 수
- **입력값 검증**: 공백, 특수문자, 긴 숫자, 문자 포함 숫자 입력
- **상태 검증**: 버튼 활성/비활성, 드롭다운 선택 상태, 생성 중지 메시지
- **E2E 검증**: 생성 완료, 결과 영역 표시, 다운로드 결과 확인
- **Known issue 관리**: 알려진 결함은 skip하지 않고 `xfail`로 추적

---

## Project Structure

```text
AI_Helpy_chat/
├─ config/                  # 환경변수 기반 설정
├─ pages/                   # Page Object Model
├─ tests/                   # pytest 테스트
│  ├─ *_create.py           # 상세 검증 테스트
│  ├─ *_create_E2E.py       # slow E2E 테스트
│  └─ *_create_base.py      # 테스트 공통 상수/helper
├─ utils/                   # Slack/Jira 알림 유틸
├─ Dockerfile               # 테스트 실행 이미지
├─ docker-compose.yml       # Selenium + tests 컨테이너 구성
├─ Jenkinsfile              # Jenkins CI Pipeline
├─ pytest.ini               # pytest 설정
└─ requirements.txt         # Python dependencies
```

---

## Environment Variables

실제 값은 `.env` 또는 Jenkins Credentials로 관리하며, Git에 커밋하지 않습니다.

| Variable | Description |
|---|---|
| `BASE_UI_URL` | 테스트 대상 UI URL |
| `BASE_API_URL` | API base URL |
| `TEST_USER_ID` | 테스트 계정 ID |
| `TEST_USER_PW` | 테스트 계정 비밀번호 |
| `JIRA_BASE_URL` | Jira base URL |
| `JIRA_EMAIL` | Jira 계정 이메일 |
| `JIRA_API_TOKEN` | Jira API token |
| `JIRA_PROJECT_KEY` | Jira project key |
| `SLACK_WEBHOOK_URL` | 테스트 요약 Slack webhook |
| `SLACK_WEBHOOK_FAILURES_URL` | 실패 상세 Slack webhook |
| `HEADLESS` | headless 브라우저 실행 여부 |
| `SELENIUM_REMOTE_URL` | Selenium Remote WebDriver URL |

---

## Run Tests

### Docker Compose

Docker 환경에서는 `tests` 컨테이너가 pytest를 실행하고, `selenium` 컨테이너가 Chrome 브라우저를 제공합니다.

```bash
docker compose up --build --abort-on-container-exit --exit-code-from tests tests
```

테스트 완료 후 생성되는 주요 산출물:

```text
reports/junit.xml
allure-results/
logs/
```

### Local pytest

```bash
pytest tests/test_quiz_create.py tests/test_ppt_create.py tests/test_deep_create.py -n 3 --browser chrome
```

### Slow E2E

기본 CI에서는 상세 테스트만 실행하고, slow E2E는 필요할 때 별도로 실행합니다.

```bash
pytest tests/test_quiz_create_E2E.py tests/test_ppt_create_E2E.py tests/test_deep_create_E2E.py -m slow --browser chrome
```

---

## Jenkins CI Pipeline

Jenkins는 GitHub push를 감지해 Docker 기반 테스트 파이프라인을 실행합니다.

```text
GitHub push
  -> Jenkins Pipeline
  -> Docker test image build
  -> selenium/standalone-chrome healthcheck
  -> tests container pytest run
  -> JUnit result publish
  -> Allure Report publish
  -> logs/reports/allure-results archive
```

Pipeline 주요 stage:

- `Build Docker Test Image`
- `Run UI Tests`
- `post`: JUnit, Allure, artifact archive, Docker Compose cleanup

---

## Allure Report

Allure는 테스트 결과를 기능과 시나리오 단위로 확인하기 위해 사용합니다.

- `allure-pytest`로 `allure-results/` 생성
- `@allure.feature`, `@allure.story`, `@allure.title`로 테스트 분류
- Jenkins Allure Plugin으로 빌드별 리포트 publish

현재는 테스트 메타데이터 중심으로 구성되어 있으며, 단계별 `allure.step`과 실패 스크린샷 attachment는 향후 개선 항목입니다.

---

## Slack & Jira Integration

테스트 실행 결과는 Slack과 Jira로 추적할 수 있도록 구성했습니다.

- 테스트 세션 종료 후 Slack 요약 알림 전송
- 실패 테스트 발생 시 상세 Slack 알림 전송
- Jira 설정이 존재할 경우 실패 케이스 이슈 생성 및 스크린샷 첨부
- Slack/Jira 연동 실패가 테스트 실행 자체를 방해하지 않도록 예외 처리

---

## Known Issues & Current Notes

- 알려진 결함은 `pytest.mark.xfail`로 관리합니다.
- 현재 known issue 예시:
  - PPT 긴 숫자 입력값이 지수 표기 또는 `Infinity`로 변환되는 이슈
  - PPT 공백 주제가 유효값으로 처리되는 이슈
  - Deep Investigation 공백 주제가 유효값으로 처리되는 이슈
- Docker/Selenium 환경에서 Deep 상세 테스트 일부가 `TimeoutException`으로 실패한 이력이 있어, selector 안정성 또는 대기 조건 개선이 필요합니다.

---

## Git Safety

아래 파일과 산출물은 Git에 커밋하지 않습니다.

```text
.env
.venv/
logs/
reports/
allure-results/
allure-report/
__pycache__/
```


# HelpyChat QA Automation

> AI Helpy Chat의 핵심은 사용자 경험 기반 시나리오를 검증하고, 실패 증거를 남기도록 설계한 E2E QA 자동화 프로젝트입니다.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-9.0.3-0A9EDC?logo=pytest&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.44.0-43B02A?logo=selenium&logoColor=white)
![GitLab CI](https://img.shields.io/badge/GitLab-CI/CD-FC6D26?logo=gitlab&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-compatible-2088FF?logo=githubactions&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-Report-FF5A5F)
![Ruff](https://img.shields.io/badge/Ruff-Lint-261230)

## 개요

AI Helpy Chat은 채팅, 검색, 에이전트, AI 생성 도구처럼 화면 상태와 비동기 응답이 자주 바뀌는 서비스입니다. 이 프로젝트는 사용자가 실제로 거치는 주요 흐름을 E2E로 검증하고, 실패했을 때 재현 가능한 증거를 남기는 데 초점을 두었습니다.

## 목적

단순히 테스트 코드를 많이 작성하는 것이 아니라, 실제 사용자 흐름을 자동화하고 실패 원인을 추적 가능한 형태로 남기는 것이 목표였습니다.

- 사용자 영향도가 큰 흐름을 Selenium 기반 UI 자동화로 검증
- 실패 시 로그, 스크린샷, Slack/Jira 알림으로 원인 추적 가능하게 구성
- 확인된 서비스 결함은 xfail로 분리해 CI에서 계속 추적

진행 중에는 MUI 컴포넌트의 클릭 방해, React rerender로 인한 StaleElement, 파일 업로드/다운로드 검증 한계, Windows Runner의 한글 인코딩 문제처럼 UI 자동화에서 자주 발생하는 불안정성을 마주했습니다.

클릭과 입력이 흔들리는 문제는 화면별 조작 로직을 Page Object로 나누고, 반복되는 클릭·입력·대기 처리를 BasePage의 공통 메서드로 정리해 대응했습니다. 다국어 환경에서도 테스트가 쉽게 깨지지 않도록, 화면 문구만 바라보는 locator를 줄이고 role, name, form, URL, data-testid 같은 구조 기반 locator를 우선 검토했습니다. 파일 업로드/다운로드처럼 자동화가 불안정한 영역은 검증 가능한 범위와 수동 확인이 필요한 범위를 분리했고, Windows Runner의 한글 로그 문제는 CI 인코딩 설정으로 보완했습니다.

이 과정을 통해 테스트 자동화는 단순 반복 작업을 줄이는 도구가 아니라, 품질 리스크를 설명 가능한 증거로 바꾸는 작업이라는 점을 배웠습니다.

---

## Project Snapshot

| 구분 | 값 | 기준 |
|---|---:|---|
| 테스트 케이스 | 198건 | 최종 결과 보고서 |
| Pass | 180건 | 최종 결과 보고서 |
| 실행 Pass rate | 95.24% | 최종 결과 보고서 |
| 자동화 시나리오 | 43개 | 최종 결과 보고서 |
| 테스트 모듈 | 18개 | 현재 저장소 |
| 테스트 함수 | 73개 | 현재 저장소 |
| Page Object | 17개 | 현재 저장소 |
| 지원 브라우저 | Chrome, Edge, Firefox | QA 계획서 |

이 README의 결과 수치는 산출물 PDF의 최종 보고 기준과 현재 저장소 구조 기준을 구분해서 표기했습니다.

## 검증 범위

| 영역 | 검증 내용 |
|---|---|
| 채팅 / 검색 | 새 대화, 메시지 전송, 검색 모달, 검색 결과 이동, 검색어 초기화 |
| LNB 관리 | 대화 생성, 삭제, 새로고침 후 유지, 선택 흐름 |
| 에이전트 | 에이전트 생성, 검색, 필터, 내 에이전트 화면 이동 |
| 퀴즈 생성 | 객관식/주관식 생성, 필수값, 공백값, 드롭다운, 생성 중지 |
| PPT 생성 | 생성, 다운로드, 주제/지시사항/숫자 필드 검증, 중단, 재생성 버튼 |
| 수업지도안 | 신규/기존 계정 기준 생성 흐름 |
| 심층 조사 | 생성 결과, Markdown 다운로드, 입력값 검증, 재생성, 중단 |
| 행동특성 및 종합의견 | 학교급, 학생 추가, 키워드 입력, 재생성, 초기화/롤백 |
| 세부특기사항 | 경계값 조합, 학생 검색, 학생 추가, 초기화/롤백, 특수문자 검증 |
| 업로드 / 다운로드 | 파일 업로드 진입, PPTX/Markdown 다운로드, 다운로드 완료 상태 |

## 자동화 구조

```text
AI_Helpy_chat/
├── config/                 # URL, 계정, 다운로드 경로, Slack/Jira 설정
├── pages/                  # Selenium Page Object Model
│   ├── base_page.py        # 공통 클릭, 입력, 대기, fallback 동작
│   ├── chat_page.py
│   ├── quiz_page.py
│   ├── ppt_page.py
│   └── ...                 # 총 17개 Page Object
├── tests/                  # pytest E2E 시나리오
│   ├── test_message_send.py
│   ├── test_quiz_create.py
│   ├── test_ppt_create.py
│   └── ...                 # 총 18개 테스트 모듈
├── utils/                  # Slack/Jira 알림 유틸
├── logs/                   # 실행 로그와 실패 스크린샷
├── conftest.py             # fixture, WebDriver, hook, 실패 후처리
├── pytest.ini              # pytest 경로, 로그, marker 설정
├── requirements.txt        # Python 의존성
└── .gitlab-ci.yml          # GitLab CI 테스트 파이프라인
```

### 역할 분리

| 구성 | 역할 |
|---|---|
| `pages/` | 화면 조작과 locator를 Page Object로 분리해 테스트 가독성 유지 |
| `tests/` | 사용자 시나리오와 검증 의도를 중심으로 작성 |
| `conftest.py` | 로그인 fixture, 브라우저 옵션, 다운로드 경로, 실패 hook 관리 |
| `utils/slack_notifier.py` | 테스트 요약과 실패 상세를 Slack으로 전송 |
| `utils/jira_notifier.py` | 실패 케이스를 Jira Bug 이슈와 스크린샷으로 연결 |
| `.gitlab-ci.yml` | Windows Runner에서 headless UI fast job 실행 |

## 주요 성과

| 항목 | 결과 |
|---|---|
| 총 테스트 케이스 | 198건 |
| Pass / Fail / N/A / N/T | 180 / 9 / 9 / 0 |
| 실행 Pass rate | 95.24% |
| 자동화 테스트 시나리오 | 43개 |
| 자동화 시나리오 결과 | Pass 36 / Xfail 6 / N/A 1 |
| Critical Bug | 0건 |

자동화에서 발견한 주요 결함은 검색 모달 초기화, PPT 긴 숫자 입력값 변환, PPT 입력 필드 초기화, 재생성 버튼 비활성화, 특수문자 차단 누락 등이었습니다. 확인된 결함은 xfail로 분리해 CI에서 계속 추적할 수 있도록 관리했습니다.

## Troubleshooting Highlights

| 문제 | 원인 | 해결 | 결과 |
|---|---|---|---|
| MUI Tooltip/Popover가 클릭을 방해 | 동적 레이어와 애니메이션이 Selenium click 타이밍과 충돌 | scrollIntoView, clickable wait, blocker 처리, JS fallback 공통화 | 간헐 클릭 실패 감소 |
| StaleElementReferenceException | React rerender 후 이전 WebElement 참조 사용 | 클릭 직전 요소 재탐색, 상태 확인 재시도 | 동적 화면 전환 안정화 |
| OS 파일 선택 다이얼로그 | Selenium이 브라우저 외부 다이얼로그를 안정적으로 제어하기 어려움 | 자동화 가능 범위와 수동 검증 범위 분리, xfail 관리 | CI 실패 노이즈 감소 |
| Windows Runner 한글 로그 깨짐 | 기본 코드페이지와 Python 출력 인코딩 불일치 | `chcp 65001`, `PYTHONUTF8`, `PYTHONIOENCODING` 설정 | CI 로그 판독성 개선 |
| GitLab CI 실행 시간과 환경 차이 | 브라우저 headless, 의존성 설치, 테스트 범위가 한 job에 집중 | UI fast job, pip cache, logs artifact, marker 기반 실행 | 실패 로그 회수와 반복 실행 기반 마련 |
| 재현 버그 처리 기준 | skip 처리 시 실제 결함이 결과에서 사라질 수 있음 | xfail strict 관리 | 알려진 서비스 결함을 자동화 결과에 남김 |

## 실행 가이드

### 1. 설치

Chrome 브라우저가 설치되어 있어야 합니다. ChromeDriver는 Selenium Manager가 자동으로 관리합니다.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

macOS/Linux 환경에서는 가상환경 활성화 명령만 다릅니다.

```bash
source venv/bin/activate
```

### 2. 환경 변수

프로젝트 루트에 `.env` 파일을 만들고 필요한 값을 설정합니다. 실제 계정, 토큰, Webhook URL은 저장소에 커밋하지 않습니다.

```env
BASE_UI_URL=https://qaproject.elice.io
BASE_API_URL=https://dev-v2-community-api.dev.elicer.io

TEST_USER_ID=your_test_user@example.com
TEST_USER_PW=your_password

DOWNLOAD_DIR=C:\Users\user\Downloads
DEFAULT_API_TIMEOUT=10
HEADLESS=false

JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your_jira_email@example.com
JIRA_API_TOKEN=your_jira_api_token
JIRA_PROJECT_KEY=YOUR_PROJECT_KEY

SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
SLACK_WEBHOOK_FAILURES_URL=https://hooks.slack.com/services/...
```

### 3. 테스트 실행

전체 테스트 실행:

```bash
pytest
```

특정 테스트 파일 실행:

```bash
pytest tests/test_quiz_create.py
```

marker 기준 실행:

```bash
pytest -m ui
pytest -m slow
pytest -m detail
pytest -m "not slow"
```

테스트 수집만 확인:

```bash
pytest --collect-only -q
```

CI와 동일하게 headless 모드로 실행:

```powershell
$env:HEADLESS="true"
pytest
```

## CI/CD

GitLab CI는 Windows Runner 기준으로 headless UI 테스트를 실행합니다.

- `HEADLESS=true`로 브라우저를 headless 모드 실행
- Python 후보 경로를 순차 탐색해 Runner 환경 차이 흡수
- pip cache로 의존성 설치 시간 감소
- `pytest -n 3 -m "not slow"`로 빠른 UI 범위 병렬 실행
- 실패 여부와 관계없이 `logs/`와 JUnit XML을 artifact로 보관

현재 CI fast job은 다음 파일을 대상으로 합니다.

```text
tests/test_quiz_create.py
tests/test_ppt_create.py
tests/test_deep_create.py
```

## Reports & Artifacts

`C:\Users\user\Desktop\1차 프로젝트 산출물` 폴더에는 프로젝트 진행 과정과 결과를 설명하는 산출물이 정리되어 있습니다.

| 산출물 | 내용 |
|---|---|
| `QA계획서_-_AI_Helpy_Chat.pdf` | 테스트 목적, 범위, 제외 대상, 환경, 일정, 종료 기준 |
| `QA_테스트최종결과보고서.pdf` | 최종 TC 198건 결과, Pass rate, 발견 버그, 개선 계획 |
| `HelpyChat_QA_자동화_포트폴리오.pdf` | 자동화 구조, 검증 대상, 안정화 경험, 포트폴리오 요약 |
| `GitLab_CI_CD_결과.pdf` | CI/CD 실행 결과와 파이프라인 구성 근거 |
| `결함 분석 대시보드.pdf` | 결함 현황과 분류 |
| `트러블 슈팅 10선.pdf` | 민감정보 관리, Slack/Jira, CI, 인코딩, flaky 대응 경험 |
| `BUG_PPT_XFAIL_긴숫자_입력값_변환_리포트.pdf` | PPT 숫자 입력값 변환 결함 상세 |
| `PPT_자동화_코드_변화_트러블슈팅_보고서.pdf` | PPT 자동화 코드 변화와 안정화 기록 |

## 작성 기준

- 화면 조작은 가능한 한 `pages/`의 Page Object에 둡니다.
- 테스트 파일은 시나리오 이름과 검증 의도가 드러나게 작성합니다.
- 공통 클릭, 입력, 대기, fallback은 `BasePage` 메서드를 우선 사용합니다.
- 알려진 서비스 결함은 skip이 아니라 xfail로 분리해 추적합니다.
- 실패 분석에 필요한 로그, 스크린샷, Slack/Jira 정보가 남도록 구성합니다.
- 민감정보는 `.env`와 환경변수로 관리하고 저장소에는 커밋하지 않습니다.

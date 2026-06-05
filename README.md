# HelpyChat QA Automation

> 사용자 환경 기반 시나리오를 검증하고, 실패 증거를 작성하도록 설계한 E2E QA 자동화 프로젝트입니다.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-9.0.3-0A9EDC?logo=pytest&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.44.0-43B02A?logo=selenium&logoColor=white)
![GitLab CI](https://img.shields.io/badge/GitLab-CI/CD-FC6D26?logo=gitlab&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-compatible-2088FF?logo=githubactions&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-Report-FF5A5F)
![Ruff](https://img.shields.io/badge/Ruff-Lint-261230)

## 개요

AI Helpy Chat은 채팅, 검색, 에이전트, AI 생성 도구처럼 화면 상태와 비동기 응답이 자주 바뀌는 서비스입니다. 이 프로젝트는 QA 자동화와 테스트 설계부터 CI 연동과 실패 리포트 구성까지 실제 서비스 흐름에 적용해 보기 위해 진행했습니다. Selenium이나 pytest 사용법을 아는 것에 그치지 않고, 사용자의 주요 흐름을 어떻게 자동화하고 실패 원인을 어떻게 추적 가능한 형태로 남길 수 있는지에 의미를 두었습니다.

## 목적

이 프로젝트는 단순히 테스트 코드를 많이 작성하는 것이 목표가 아니었습니다. 실제 사용자가 서비스를 이용하며 거치는 핵심 흐름을 검증하고, 실패가 발생했을 때 원인을 추적할 수 있는 근거를 남기는 것을 목표로 했습니다.

MUI 구성요소가 클릭을 가로막는 문제, 파일 업로드/다운로드 검증의 불안정성, Windows Runner의 한글 로그 깨짐처럼 UI 자동화에서 자주 발생하는 문제를 직접 파악하고 개선하며 테스트의 신뢰도를 높이고자 했습니다.

클릭 방해 문제는 요소를 클릭 직전에 다시 탐색하고, 명시적 대기, `scrollIntoView`, JS click fallback을 조합한 방어 로직으로 대응했습니다. 파일 업로드/다운로드는 테스트별 임시 다운로드 경로를 설정하고, 실행 전후 파일 개수와 파일 크기를 확인한 뒤 정리하는 방식으로 검증했습니다.

다국어 설정이나 화면 문구 변경에도 테스트가 쉽게 깨지지 않도록 텍스트 기반 locator보다 `name`, `form`, `role`, `href`, `aria-*`처럼 구조적으로 유지될 가능성이 높은 요소를 우선 사용했습니다. 이 과정을 통해 Page Object Model 구조에서 화면 조작 책임과 테스트 시나리오 책임을 분리하는 방식에 대한 이해를 높였습니다.

테스트 실패 시에는 로그, 스크린샷, Slack/Jira 알림이 남도록 구성했으며, 실제 서비스 결함은 `xfail`로 관리해 수정 여부를 판단할 수 있는 근거로 활용했습니다.

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

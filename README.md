# AI Helpy Chat QA Automation

> AI Helpy Chat의 Quiz, PPT, 심층분석 생성 기능에 대해 TC/시나리오 설계, 결함 추적, 자동화 테스트 구축을 담당. 
> Jenkins와 Docker를 활용한 자동화 CI/CD 파이프라인을 구성하고, Allure Report로 테스트 결과를 시각화했습니다.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-9.x-0A9EDC?logo=pytest&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.x-43B02A?logo=selenium&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-CI-D24939?logo=jenkins&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-Report-FF6B6B)

---

## 핵심 성과

| 구분 | 성과 |
|---|---|
| TC 설계 | 전체 198건 중 94건 담당 |
| 시나리오 설계 | 전체 43개 중 28개 담당 |
| 결함 관리 | 버그 리포트 5건 작성 및 추적 |
| 트러블슈팅 | 자동화 구축 중 발생 이슈 21건 기록 |
| 자동화 테스트 | Quiz/PPT/Deep 상세 테스트 30건 구성 |
| 회귀 관리 | known issue 4건을 `pytest.mark.xfail`로 추적 |
| CI/CD | Docker Compose + Jenkins + Allure Report 연동 |

---

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 플랫폼 | AI Helpy Chat |
| 테스트 범위 | Quiz Create, PPT Create, Deep Investigation Create |
| 담당 역할 | TC/시나리오 설계, 기능/예외/경계값 테스트, 자동화, 결과 문서화 |
| 테스트 환경 | Windows, Docker Desktop, Jenkins local |
| 브라우저 | Chrome |
| 자동화 도구 | Python, Selenium, pytest, pytest-xdist |
| CI/리포트 | Docker Compose, Jenkins, JUnit XML, Allure Report |
| 협업/추적 | Notion, GitHub, Jira, Slack |
| QA 산출물 | [Notion 상세 문서](https://dirt-brand-7d0.notion.site/AI-337f6266ce2a8077a9d4ea1b6878a38d) |

---

## 담당 역할

- 전체 TC 198건 중 **94건** 담당
- 전체 시나리오 43개 중 **28개** 담당
- Quiz/PPT/Deep 생성 기능 중심의 기능 테스트 수행
- 공백 입력, 긴 문자열, 숫자 필드 등 예외/경계값 테스트 수행
- 버그 리포트 및 결과 리포트 작성
- 수정 확인을 위한 회귀 테스트 진행
- Selenium + pytest 기반 UI 자동화 테스트 작성
- Docker/Jenkins/Allure 기반 CI 리포트 흐름 구성

---

## 테스트 전략

| 전략 | 검증 내용 |
|---|---|
| 기능 테스트 | Quiz/PPT/Deep 생성, 옵션 선택, 다운로드, 생성 중지 |
| 예외 테스트 | 공백 입력, 긴 문자열, 숫자 필드 비정상 입력 |
| 경계값 분석 | 주제 길이, 지시사항 길이, PPT 슬라이드/섹션 수 |
| 상태 검증 | 버튼 활성/비활성, 드롭다운 선택 상태, 생성 중 메시지 |
| 회귀 테스트 | known issue를 `xfail`로 남겨 수정 여부 추적 |
| 자동화 분리 | 상세 테스트와 slow E2E 테스트를 분리해 CI 실행 시간 관리 |

---

## 주요 테스트 케이스

| 기능 | 대표 TC | 검증 포인트 |
|---|---|---|
| Quiz | 주제 입력값 검증 | 유효/무효 주제 입력 시 버튼 상태와 결과 확인 |
| Quiz | 유형/난이도 드롭다운 검증 | 옵션 선택 상태 유지 여부 확인 |
| PPT | 슬라이드 수 경계값 검증 | 최소/최대/초과 입력 처리 확인 |
| PPT | 긴 숫자 입력값 검증 | 지수 표기 또는 `Infinity` 변환 이슈 추적 |
| PPT | 공백 주제 검증 | 공백만 입력해도 생성 버튼이 활성화되는 결함 추적 |
| Deep | 공백 주제 검증 | 공백 주제 입력 시 버튼 상태 결함 추적 |
| Deep | 다시 생성 버튼 상태 검증 | 입력값 변경 후 버튼 활성 조건 확인 |

전체 담당 테스트 설계 문서는 GitHub에서 바로 확인할 수 있습니다.

- [전체 담당 TC 94건 보기](qa-artifacts/test-cases.md)
- [담당 테스트 시나리오 28개 보기](qa-artifacts/test-scenarios.md)

---

## 대표 이슈 보드

### PPT 숫자 입력 필드의 긴 숫자가 지수 표기 또는 Infinity로 변환되는 문제

| 항목 | 내용 |
|---|---|
| 관련 TC | `TC_066`, `TC_067`, `TC_073`, `TC_079`, `TC_080` |
| 발생 조건 | PPT 슬라이드 수 또는 섹션 수 입력 필드에 매우 긴 숫자 입력 |
| 기대 결과 | 입력값이 의도와 다르게 변환되지 않거나 유효성 에러로 제어되어야 함 |
| 실제 결과 | 일부 긴 숫자 입력값이 지수 표기 또는 `Infinity`로 변환됨 |
| 재현 절차 | PPT 생성 화면 진입 -> 슬라이드 수/섹션 수 필드에 긴 숫자 입력 -> 입력 필드 표시값 확인 |
| 영향 | 사용자가 의도하지 않은 숫자 값으로 PPT 생성 요청을 보낼 수 있음 |
| 추적 방식 | 자동화 테스트에 `xfail`로 등록해 수정 여부를 회귀 테스트에서 확인 |
| 상세 문서 | [Notion 버그 리포트 5건](https://dirt-brand-7d0.notion.site/AI-337f6266ce2a8077a9d4ea1b6878a38d) |

---

## 자동화 구조

```text
GitHub push
  -> Jenkins Pipeline
  -> Docker golden image / test image build
  -> selenium/standalone-chrome container
  -> tests container에서 pytest-xdist 실행
  -> JUnit XML + Allure Report publish
  -> Slack/Jira 알림 및 이슈 추적
```

### Docker 테스트 파이프라인

```text
1. Jenkins가 GitHub push를 감지해 Pipeline 시작
2. docker compose build tests로 테스트 실행 이미지 빌드
3. selenium/standalone-chrome 컨테이너 실행 및 healthcheck 통과 대기
4. tests 컨테이너에서 pytest 상세 테스트 30건 실행
5. pytest-xdist 3 workers로 병렬 실행
6. reports/junit.xml, allure-results/, logs/ 산출물 생성
7. Jenkins post 단계에서 JUnit/Allure publish 및 artifact 보관
8. docker compose down --remove-orphans로 컨테이너 정리
```

| 단계 | 역할 |
|---|---|
| Golden image | Python 3.14, pytest, Selenium, Allure 의존성을 고정한 기준 이미지 |
| Test image | 골든 이미지 위에 현재 프로젝트 코드를 복사한 실행 이미지 |
| Selenium container | `selenium/standalone-chrome`로 Chrome 브라우저 제공 |
| Tests container | `pytest -n 3`으로 Quiz/PPT/Deep 상세 테스트 실행 |
| Volume mount | `logs/`, `reports/`, `allure-results/`를 Jenkins workspace로 보존 |
| Jenkins post | JUnit XML, Allure Report, 로그 산출물을 수집하고 컨테이너 정리 |

| 구성 | 역할 |
|---|---|
| `tests/*_create.py` | CI에서 실행하는 상세 검증 테스트 |
| `tests/*_create_E2E.py` | 필요 시 별도 실행하는 slow E2E 테스트 |
| `tests/*_create_base.py` | 테스트 공통 상수와 helper |
| `pages/` | Page Object Model |
| `Dockerfile.golden` | 로컬 기준 Python/pytest/Selenium 골든 이미지 |
| `docker-compose.yml` | Selenium Chrome 컨테이너와 tests 컨테이너 분리 |
| `Jenkinsfile` | Docker 기반 테스트 실행과 리포트 수집 |

---

## 캡처 기반 증빙

Jenkins, Allure, Docker는 로컬 환경에서 동작하므로 공개 URL 대신 캡처 이미지로 증빙합니다.

| 증빙 | 파일 위치 |
|---|---|
| Jenkins Pipeline 실행 화면 | `assets/readme/jenkins-pipeline.png` |
| Allure Report 결과 화면 | `assets/readme/allure-report.png` |
| Docker Desktop 이미지/컨테이너 화면 | `assets/readme/docker-desktop.png` |
| Notion QA 산출물 화면 | `assets/readme/notion-docs.png` |

---

## 개선 제안

| 개선 포인트 | 제안 |
|---|---|
| 입력값 초기화 | 페이지를 나갔다 돌아와도 입력값이 남아 새 문서 작성 시 직접 삭제가 필요함 |
| 사용자 흐름 개선 | `초기화` 버튼 또는 `새로 작성` 플로우를 제공하면 반복 생성 작업이 쉬워짐 |
| 자동화 안정성 | Docker/Selenium 환경에서 일부 Deep 테스트 timeout 이력이 있어 wait 조건 개선 필요 |

---

## 회고

### 잘한 점

- 정상 흐름뿐 아니라 공백, 긴 문자열, 경계값 같은 예외 조건을 검증해 실제 결함을 발견했습니다.
- 상세 테스트와 slow E2E 테스트를 분리해 CI에서 빠르게 돌릴 수 있는 구조를 만들었습니다.
- Docker와 Jenkins를 연결해 로컬 환경 차이를 줄이고 반복 실행 가능한 테스트 환경을 구성했습니다.

### 아쉬운 점

- 초반에는 정상 흐름 위주로 테스트해 예외 케이스 발견이 늦었습니다.
- Jenkins/Allure/Docker가 로컬 기반이라 외부에서 바로 접근 가능한 공개 리포트로 보여주기 어렵습니다.

### 다음 개선

- Docker 골든 이미지를 기준으로 자동화 실행 환경을 더 안정화하고 싶습니다.
- 실패 시 스크린샷과 page source를 Allure attachment로 남겨 디버깅 속도를 높이고 싶습니다.
- 예외/경계값 중심의 TC 설계를 더 빠른 단계에서 적용하고 싶습니다.

---

## 실행 방법

### Docker Compose

```bash
docker compose up --build --abort-on-container-exit --exit-code-from tests tests
```

### Local pytest

```bash
pytest tests/test_quiz_create.py tests/test_ppt_create.py tests/test_deep_create.py -n 3 --browser chrome
```

### Slow E2E

```bash
pytest tests/test_quiz_create_E2E.py tests/test_ppt_create_E2E.py tests/test_deep_create_E2E.py -m slow --browser chrome
```

---

## 보안 관리

`.env`, Slack Webhook, Jira API Token, 테스트 계정 비밀번호는 Git에 커밋하지 않고 로컬 `.env` 또는 Jenkins Credentials로 관리합니다.

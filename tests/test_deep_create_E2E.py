import logging

import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait

import deep_create_base as base


logger = logging.getLogger(__name__)


@allure.feature("Deep Investigation Create")
@allure.story("E2E generation")
class TestDeepInvestigationE2E(base.DeepInvestigationBase):
    @allure.title("심층 조사 생성 결과 E2E")
    @pytest.mark.slow
    def test_full_generation_result(self, logged_in_driver):
        """
        심층 조사 생성 결과 검증 시나리오

        커버 TC: TC_141, TC_142

        Step 1. 로그인 상태로 심층 조사 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 주제 / 지시사항 입력
        Step 4. 다시 생성 버튼 클릭
        Step 5. 모달 내부 다시 생성 버튼 클릭
        Step 6. 생성 시작 확인 (버튼 비활성화)
        Step 7. 생성 완료 확인 (버튼 재활성화)
        Step 8. 생성 결과 영역 노출 확인
        """

        scenario = "심층 조사 생성 결과"

        driver = logged_in_driver
        long_wait = WebDriverWait(driver, base.GENERATION_TIMEOUT_SECONDS)
        page = self.setup_page(driver, scenario)

        self.enter_generation_inputs(page, scenario)
        self.open_regenerate_modal(page, scenario)
        self.start_generation(page, scenario, long_wait)
        self.wait_for_generation_complete(page, scenario, long_wait)
        self.assert_result_visible(page)
        self.show_step(page, 8, "생성 결과 영역 노출 확인")
        logger.info(f"[{scenario}] 생성 결과 영역 노출 확인 완료")

    @allure.title("심층 조사 Markdown 다운로드 E2E")
    @pytest.mark.slow
    def test_markdown_download_result(self, logged_in_driver, temp_download_dir):
        """
        심층 조사 마크다운 다운로드 검증 보류 시나리오

        커버 TC: TC 미등록 - 다운로드 정책 논의 후 확정 예정

        Step 1. 로그인 상태로 심층 조사 페이지 진입
        Step 2. 생성 완료된 결과 영역 준비
        Step 3. 다운받기 버튼 클릭
        Step 4. 마크다운 다운로드 클릭
        Step 5. 다운로드 파일 생성 및 확장자 / 크기 확인
        """

        scenario = "심층 조사 마크다운 다운로드"
        download_dir = temp_download_dir / "deep_markdown"
        download_dir.mkdir(exist_ok=True)
        logged_in_driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": str(download_dir),
        })

        driver = logged_in_driver
        long_wait = WebDriverWait(driver, base.GENERATION_TIMEOUT_SECONDS)
        page = self.setup_page(driver, scenario)

        self.enter_generation_inputs(page, scenario)
        self.open_regenerate_modal(page, scenario)
        self.start_generation(page, scenario, long_wait)
        self.wait_for_generation_complete(page, scenario, long_wait)
        self.assert_result_visible(page)
        self.show_step(page, 8, "생성 결과 영역 노출 확인")
        logger.info(f"[{scenario}] 생성 결과 영역 노출 확인 완료")
        self.download_markdown_result(page, scenario, long_wait, download_dir)

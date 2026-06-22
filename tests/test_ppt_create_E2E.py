import logging

import pytest

import ppt_create_base as base


logger = logging.getLogger(__name__)


class TestPptCreateE2E(base.PptCreateBase):
    @pytest.mark.slow
    def test_ppt_create_full_option(self, logged_in_driver):
        """
        PPT 전체 입력값 생성 시나리오

        커버 TC: TC_051, TC_098, TC_099, TC_102

        Step 1. 로그인 상태로 PPT 생성 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 주제 / 지시사항 / 슬라이드 수 / 섹션 수 입력
        Step 4. 생성 버튼 클릭
        Step 5. 모달 내부 생성 버튼 클릭
        Step 6. 생성 시작 확인
        Step 7. 생성 완료 및 생성 결과 다운로드 버튼 노출 확인
        """
        scenario = "전체 입력값 생성"
        page = self.setup_page(logged_in_driver, scenario)

        self.enter_valid_inputs(page)
        page.show_step("Step.3 주제 / 지시사항 / 슬라이드 수 / 섹션 수 입력")
        logger.info(f"[{scenario}] 필수 입력값 입력 완료")

        self.start_generation(page, scenario)
        self.wait_generation_complete(page, scenario)

    @pytest.mark.slow
    def test_ppt_download_file_contract(self, logged_in_driver, download_dir):
        """
        PPT 다운로드 파일 품질 검증 보류 시나리오

        커버 TC: TC_100 확장

        Step 1. 로그인 상태로 PPT 생성 페이지 진입
        Step 2. 생성 완료된 결과 영역 준비
        Step 3. 생성 결과 다운로드 버튼 클릭
        Step 4. 다운로드 파일 확장자 / 크기 / 파일명 / 내용 형식 검증
        """

        scenario = "다운로드 파일 품질 검증"
        page = self.setup_page(logged_in_driver, scenario)
        self.enter_valid_inputs(page)
        self.start_generation(page, scenario)
        self.wait_generation_complete(page, scenario)
        self.download_result(page, scenario, download_dir)

import logging

import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait

import deep_create_base as base


logger = logging.getLogger(__name__)

@allure.feature("Deep Investigation Create")
class TestDeepInvestigation(base.DeepInvestigationBase):
    @allure.story("Topic validation")
    @allure.title("심층 조사 주제 입력값 검증")
    @pytest.mark.detail
    def test_topic_validation(self, logged_in_driver):
        """
        심층 조사 주제 입력값 검증 시나리오

        커버 TC: TC_128, TC_129, TC_130, TC_131 일부

        Step 1. 로그인 상태로 심층 조사 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 주제 0자 입력
        Step 4. 주제 0자 에러 메시지 출력 확인
        Step 5. 주제 500자 입력
        Step 6. 주제 500자 입력값 길이 확인
        Step 7. 주제 501자 입력
        Step 8. 주제 501자 에러 메시지 출력 및 버튼 비활성화 확인
        Step 9. 복합 정상 주제 입력값 유지 및 버튼 활성화 확인
        """

        scenario = "주제 입력값 검증"
        page = self.setup_page(logged_in_driver, scenario)

        page.enter_topic("")
        self.show_step(page, 3, "주제 0자 입력")
        logger.info(f"[{scenario}] 주제 0자 입력 완료")

        empty_error_message = self.assert_topic_error_visible(page)
        self.assert_error_message_equals(empty_error_message, base.TOPIC_LENGTH_ERROR_MESSAGE, "주제 0자")
        self.assert_regenerate_disabled(page)
        self.show_step(page, 4, "주제 0자 에러 메시지 및 버튼 비활성화 확인")
        logger.info(f"[{scenario}] 에러메시지 : {empty_error_message}")

        page.enter_topic(base.VALID_TOPIC * base.MAX_TOPIC_LENGTH)
        self.show_step(page, 5, "주제 500자 입력")
        logger.info(f"[{scenario}] 주제 500자 입력 완료")

        actual_length = len(page.get_topic_value())
        assert actual_length == base.MAX_TOPIC_LENGTH, f"주제 입력값 길이가 다릅니다. expected={base.MAX_TOPIC_LENGTH}, actual={actual_length}"
        self.assert_topic_error_hidden(page)
        self.assert_regenerate_enabled(page)
        self.show_step(page, 6, "주제 500자 입력값 길이와 버튼 활성화 확인")
        logger.info(f"[{scenario}] 주제 입력값 길이 확인 완료: {actual_length}자")

        page.enter_topic(base.VALID_TOPIC * base.OVER_TOPIC_LENGTH)
        self.show_step(page, 7, "주제 501자 입력")
        logger.info(f"[{scenario}] 주제 501자 입력 완료")

        over_limit_error_message = self.assert_topic_error_visible(page)
        self.assert_error_message_equals(over_limit_error_message, base.TOPIC_LENGTH_ERROR_MESSAGE, "주제 501자")
        self.assert_regenerate_disabled(page)

        self.show_step(page, 8, "주제 501자 에러 메시지 및 버튼 비활성화 확인")
        logger.info(f"[{scenario}] 에러메시지 : {over_limit_error_message}")
        logger.info(f"[{scenario}] 주제 501자 에러 메시지 및 버튼 비활성화 확인 완료")

        page.enter_topic(base.VALID_COMPLEX_TOPIC)
        self.assert_valid_topic_state(page, base.VALID_COMPLEX_TOPIC)
        self.show_step(page, 9, "복합 정상 주제 입력값 유지 및 버튼 활성화 확인")
        logger.info(f"[{scenario}] 복합 정상 주제 입력값 검증 완료: {base.VALID_COMPLEX_TOPIC}")

    @allure.story("Known issue")
    @allure.title("심층 조사 공백 주제 Known Issue")
    @pytest.mark.detail
    @pytest.mark.xfail(
        reason="Known issue: 공백만 있는 주제가 유효값으로 처리되어 다시 생성 버튼이 활성화됨"
    )
    def test_blank_topic_validation(self, logged_in_driver):
        """
        심층 조사 공백 주제 입력값 검증 시나리오

        커버 TC: TC 미등록 - 공백 주제 버그 리포트용

        Step 1. 로그인 상태로 심층 조사 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 공백만 있는 주제 입력
        Step 4. 에러 메시지 및 다시 생성 버튼 비활성화 확인
        """

        scenario = "공백 주제 입력값 검증"
        page = self.setup_page(logged_in_driver, scenario)

        page.enter_topic(base.BLANK_TOPIC)
        self.show_step(page, 3, "공백만 있는 주제 입력")
        logger.info(f"[{scenario}] 공백 주제 입력 완료")

        error_message = self.assert_topic_error_visible(page)
        self.assert_error_message_equals(error_message, base.TOPIC_LENGTH_ERROR_MESSAGE, "공백 주제")
        self.assert_regenerate_disabled(page)
        self.show_step(page, 4, "에러 메시지 및 다시 생성 버튼 비활성화 확인")
        logger.info(f"[{scenario}] 에러메시지 : {error_message}")

    @allure.story("Instructions validation")
    @allure.title("심층 조사 지시사항 입력값 검증")
    @pytest.mark.detail
    def test_instructions_validation(self, logged_in_driver):
        """
        심층 조사 지시사항 입력값 검증 시나리오

        커버 TC: TC_134, TC_135

        Step 1. 로그인 상태로 심층 조사 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 지시사항 2000자 입력
        Step 4. 지시사항 2000자 입력값 길이 확인
        Step 5. 지시사항 2001자 입력
        Step 6. 지시사항 2001자 에러 메시지 출력 확인
        """

        scenario = "지시사항 입력값 검증"
        page = self.setup_page(logged_in_driver, scenario)

        page.enter_topic(base.VALID_TOPIC)
        page.enter_instructions(base.multiline_text(base.VALID_INSTRUCTIONS, base.MAX_INSTRUCTIONS_LENGTH))
        self.show_step(page, 3, "줄바꿈 포함 지시사항 2000자 입력")
        logger.info(f"[{scenario}] 지시사항 2000자 입력 완료")

        actual_length = len(page.get_instructions_value())
        assert actual_length == base.MAX_INSTRUCTIONS_LENGTH, f"지시사항 입력값 길이가 다릅니다. expected={base.MAX_INSTRUCTIONS_LENGTH}, actual={actual_length}"
        self.assert_instructions_error_hidden(page)
        self.assert_regenerate_enabled(page)
        self.show_step(page, 4, "지시사항 2000자 입력값 길이와 버튼 활성화 확인")
        logger.info(f"[{scenario}] 지시사항 입력값 길이 확인 완료: {actual_length}자")

        page.enter_instructions(base.VALID_TOPIC * base.OVER_INSTRUCTIONS_LENGTH)
        self.show_step(page, 5, "지시사항 2001자 입력")
        logger.info(f"[{scenario}] 지시사항 2001자 입력 완료")

        error_message = self.assert_instructions_error_visible(page)
        self.assert_error_message_equals(error_message, base.INSTRUCTIONS_LENGTH_ERROR_MESSAGE, "지시사항 2001자")
        self.assert_regenerate_disabled(page)
        self.show_step(page, 6, "지시사항 2001자 에러 메시지 및 버튼 비활성화 확인")
        logger.info(f"[{scenario}] 에러메시지 : {error_message}")

    @allure.story("Regenerate button state")
    @allure.title("심층 조사 다시 생성 버튼 상태 검증")
    @pytest.mark.detail
    def test_regenerate_button_state(self, logged_in_driver):
        """
        심층 조사 다시 생성 버튼 상태 검증 시나리오

        커버 TC: TC_125, TC_136, TC_137, TC_138, TC_139, TC_140

        Step 1. 로그인 상태로 심층 조사 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 주제 미입력 / 지시사항 미입력 상태 버튼 비활성화 확인
        Step 4. 주제 미입력 / 지시사항 입력 상태 버튼 비활성화 확인
        Step 5. 주제 입력 / 지시사항 미입력 상태 버튼 활성화 확인
        Step 6. 주제 입력 / 지시사항 입력 상태 버튼 활성화 확인
        Step 7. 다시 생성 확인 모달 노출 확인
        """

        scenario = "다시 생성 버튼 상태 검증"
        page = self.setup_page(logged_in_driver, scenario)

        page.enter_topic("")
        self.assert_regenerate_disabled(page)
        self.show_step(page, 3, "주제 미입력 / 지시사항 미입력 상태 버튼 비활성화 확인")
        logger.info(f"[{scenario}] 주제 미입력 / 지시사항 미입력 상태 버튼 비활성화 확인 완료")

        page.enter_instructions(base.VALID_INSTRUCTIONS)
        self.assert_regenerate_disabled(page)
        self.show_step(page, 4, "주제 미입력 / 지시사항 입력 상태 버튼 비활성화 확인")
        logger.info(f"[{scenario}] 주제 미입력 / 지시사항 입력 상태 버튼 비활성화 확인 완료")

        page.enter_topic(base.VALID_TOPIC)
        page.enter_instructions("")
        self.show_step(page, 5, "주제 입력 / 지시사항 미입력 상태 버튼 활성화 확인")

        assert page.get_topic_value() == base.VALID_TOPIC, "입력한 주제 값이 유지되지 않았습니다."
        assert page.get_instructions_value() == "", "지시사항 입력값이 비어 있지 않습니다."
        self.assert_regenerate_enabled(page)
        logger.info(f"[{scenario}] 주제 입력 / 지시사항 미입력 상태 버튼 활성화 확인 완료")

        page.enter_instructions(base.VALID_INSTRUCTIONS)
        self.assert_regenerate_enabled(page)
        self.show_step(page, 6, "주제 입력 / 지시사항 입력 상태 버튼 활성화 확인")
        logger.info(f"[{scenario}] 주제 입력 / 지시사항 입력 상태 버튼 활성화 확인 완료")

        page.click_regenerate_button()
        self.assert_regenerate_modal_visible(page)
        self.show_step(page, 7, "다시 생성 확인 모달 노출 확인")
        logger.info(f"[{scenario}] 다시 생성 확인 모달 노출 확인 완료")

    @allure.story("Generation stop")
    @allure.title("심층 조사 생성 중지 검증")
    @pytest.mark.detail
    def test_deep_generation_stop(self, logged_in_driver):
        """
        심층 조사 생성 중지 시나리오

        커버 TC: TC 미등록 - 생성 중지 추가 자동화 시나리오

        Step 1. 로그인 상태로 심층 조사 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 주제 / 지시사항 입력
        Step 4. 다시 생성 버튼 클릭 및 확인 모달 노출 확인
        Step 5. 모달 내 다시 생성 버튼 클릭
        Step 6. 생성 시작 확인
        Step 7. 생성 중지 버튼 클릭
        Step 8. 생성 중지 메시지 출력 확인
        """

        scenario = "심층 조사 생성 중지"
        driver = logged_in_driver
        long_wait = WebDriverWait(driver, base.GENERATION_TIMEOUT_SECONDS)
        page = self.setup_page(driver, scenario)

        self.enter_generation_inputs(page, scenario)
        self.open_regenerate_modal(page, scenario)
        self.start_generation(page, scenario, long_wait)

        page.click_stop_button()
        self.show_step(page, 7, "생성 중지 버튼 클릭")
        logger.info(f"[{scenario}] 생성 중지 버튼 클릭 완료")

        stop_message = page.get_stop_message_text()
        assert stop_message, "생성 중지 메시지가 표시되지 않았습니다."
        assert any(keyword in stop_message for keyword in base.STOP_MESSAGE_KEYWORDS), (
            f"생성 중지 메시지가 기대 범위와 다릅니다. actual={stop_message}"
        )
        self.show_step(page, 8, "생성 중지 메시지 확인")
        logger.info(f"[{scenario}] 생성 중지 메시지: {stop_message}")


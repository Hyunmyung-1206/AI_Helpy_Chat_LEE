import logging

import allure
import pytest

import quiz_create_base as base


logger = logging.getLogger(__name__)


@allure.feature("Quiz Create")
class TestQuizCreate(base.QuizCreateBase):
    @allure.story("Topic input validation")
    @allure.title("퀴즈 주제 입력값 검증")
    @pytest.mark.detail
    def test_quiz_topic_input_validation(self, logged_in_driver):
        """
        퀴즈 주제 입력값 검증 시나리오

        커버 TC: TC_111, TC_112

        Step 1. 로그인 상태로 퀴즈 생성 페이지 진입
        Step 2. 주제 0자 에러 메시지 및 버튼 비활성화 확인
        Step 3. 한글 / 영문 대소문자 / 숫자 / 특수문자 주제 입력값 확인
        Step 4. 5000자 주제 입력값 길이 및 버튼 활성화 확인
        """
        scenario = "주제 입력값 검증"
        page = self.setup_page(logged_in_driver, scenario)

        page.clear_topic_input()
        page.blur_active_element()
        error_message = page.get_error_message_text()
        self.assert_error_message_equals(
            error_message,
            base.QUIZ_TOPIC_REQUIRED_ERROR_MESSAGE,
            "퀴즈 주제 필수값",
        )
        assert page.is_quiz_submit_button_disabled(), (
            "주제 0자 입력 후 다시 생성 버튼이 비활성화되지 않았습니다."
        )
        self.show_step(page, 2, "주제 0자 에러 메시지 및 버튼 비활성화 확인")
        logger.info(f"[{scenario}] 주제 0자 에러 메시지: {error_message}")

        page.enter_topic(base.COMPLEX_TOPIC)
        assert page.get_topic_value() == base.COMPLEX_TOPIC, (
            "복합 문자열 주제 입력값이 유지되지 않았습니다."
        )
        assert not page.has_visible_error_message(), (
            "복합 문자열 주제 입력 후 에러 메시지가 표시되었습니다."
        )
        self.show_step(page, 3, "복합 문자열 주제 입력값 확인")
        logger.info(f"[{scenario}] 복합 문자열 입력 확인 완료")

        long_topic = "가" * base.LONG_TOPIC_LENGTH
        page.clear_topic_input()
        page.enter_topic(long_topic)
        assert len(page.get_topic_value()) == base.LONG_TOPIC_LENGTH, (
            f"5000자 주제 입력값 길이가 다릅니다. actual={len(page.get_topic_value())}"
        )
        assert not page.has_visible_error_message(), (
            "5000자 주제 입력 후 에러 메시지가 표시되었습니다."
        )
        assert page.is_quiz_submit_button_enabled(), (
            "5000자 주제 입력 후 다시 생성 버튼이 활성화되지 않았습니다."
        )
        self.show_step(page, 4, "5000자 주제 입력값 확인")
        logger.info(f"[{scenario}] 5000자 입력 확인 완료")

    @allure.story("Quiz type dropdown")
    @allure.title("퀴즈 유형 드롭다운 검증")
    @pytest.mark.detail
    def test_quiz_type_dropdown(self, logged_in_driver):
        """
        퀴즈 유형 드롭다운 시나리오

        커버 TC: TC_105, TC_107

        Step 1. 로그인 상태로 퀴즈 생성 페이지 진입
        Step 2. 유형 드롭다운 클릭
        Step 3. 드롭다운 목록 및 객관식 단일 선택 옵션 표시 확인
        Step 4. 객관식 단일 선택값 반영 및 드롭다운 닫힘 확인
        """
        scenario = "퀴즈 유형 드롭다운"
        page = self.setup_page(logged_in_driver, scenario)

        page.click_quiz_type_dropdown()
        self.show_step(page, 2, "유형 드롭다운 클릭")
        logger.info(f"[{scenario}] 유형 드롭다운 클릭 완료")

        assert page.is_dropdown_displayed(), "드롭다운 목록이 표시되지 않았습니다."
        assert page.is_dropdown_option_displayed(base.QUIZ_TYPE_SINGLE_CHOICE), (
            "단일 선택 유형 옵션이 표시되지 않았습니다."
        )
        self.show_step(page, 3, "드롭다운 목록 및 옵션 표시 확인")

        page.select_dropdown_option_only(base.QUIZ_TYPE_SINGLE_CHOICE)
        page.wait_until_invisible(page.DROPDOWN_LIST)
        assert page.get_quiz_type_selected_text() == base.QUIZ_TYPE_SINGLE_CHOICE_TEXT, (
            "유형 선택값이 입력 필드에 반영되지 않았습니다."
        )
        self.show_step(page, 4, "유형 선택값 반영 및 드롭다운 닫힘 확인")
        logger.info(f"[{scenario}] 유형 선택 및 드롭다운 닫힘 확인")

    @allure.story("Difficulty dropdown")
    @allure.title("퀴즈 난이도 드롭다운 검증")
    @pytest.mark.detail
    def test_quiz_difficulty_dropdown(self, logged_in_driver):
        """
        퀴즈 난이도 드롭다운 시나리오

        커버 TC: TC_108, TC_109 일부

        Step 1. 로그인 상태로 퀴즈 생성 페이지 진입
        Step 2. 난이도 드롭다운 클릭
        Step 3. 상 / 중 / 하 난이도 옵션 표시 확인
        Step 4. 하 난이도 선택값 반영 및 드롭다운 닫힘 확인
        """
        scenario = "퀴즈 난이도 드롭다운"
        page = self.setup_page(logged_in_driver, scenario)

        page.click_quiz_difficulty_dropdown()
        self.show_step(page, 2, "난이도 드롭다운 클릭")
        logger.info(f"[{scenario}] 난이도 드롭다운 클릭 완료")

        assert page.is_dropdown_displayed(), "드롭다운 목록이 표시되지 않았습니다."
        assert page.is_dropdown_option_displayed(base.QUIZ_DIFFICULTY_HIGH), (
            "상 난이도 옵션이 표시되지 않았습니다."
        )
        assert page.is_dropdown_option_displayed(base.QUIZ_DIFFICULTY_MEDIUM), (
            "중 난이도 옵션이 표시되지 않았습니다."
        )
        assert page.is_dropdown_option_displayed(base.QUIZ_DIFFICULTY_LOW), (
            "하 난이도 옵션이 표시되지 않았습니다."
        )
        self.show_step(page, 3, "난이도 옵션 표시 확인")

        page.select_dropdown_option_only(base.QUIZ_DIFFICULTY_LOW)
        page.wait_until_invisible(page.DROPDOWN_LIST)
        assert page.get_quiz_difficulty_selected_text() == base.QUIZ_DIFFICULTY_LOW_TEXT, (
            "난이도 선택값이 입력 필드에 반영되지 않았습니다."
        )
        self.show_step(page, 4, "하 난이도 선택값 반영 및 드롭다운 닫힘 확인")
        logger.info(f"[{scenario}] 하 난이도 선택 및 드롭다운 닫힘 확인")

    @allure.story("Topic delete button state")
    @allure.title("퀴즈 주제 삭제 시 다시 생성 버튼 상태 검증")
    @pytest.mark.detail
    def test_quiz_topic_delete_disables_submit_button(self, logged_in_driver):
        """
        퀴즈 주제 삭제 시 다시 생성 버튼 상태 검증 시나리오

        커버 TC: TC_113, TC_114, TC_120

        Step 1. 로그인 상태로 퀴즈 생성 페이지 진입
        Step 2. 주제 입력 후 입력값 삭제
        Step 3. 다시 생성 버튼 비활성화 확인
        Step 4. 주제 재입력 후 다시 생성 버튼 활성화 확인
        """
        scenario = "주제 삭제 시 다시 생성 버튼 상태 검증"
        page = self.setup_page(logged_in_driver, scenario)

        page.clear_topic_input()
        page.enter_topic(base.VALID_TOPIC)
        assert page.get_topic_value() == base.VALID_TOPIC, "주제 입력값이 유지되지 않았습니다."

        page.clear_topic_input()
        page.blur_active_element()
        self.show_step(page, 2, "주제 입력값 삭제")
        logger.info(f"[{scenario}] 주제 입력값 삭제 완료")

        assert page.is_quiz_submit_button_disabled(), (
            "주제 삭제 후 다시 생성 버튼이 비활성화되지 않았습니다."
        )
        self.show_step(page, 3, "주제 삭제 후 다시 생성 버튼 비활성화 확인")
        logger.info(f"[{scenario}] 주제 삭제 후 다시 생성 버튼 비활성화 확인 완료")

        page.enter_topic(base.VALID_TOPIC)
        assert page.get_topic_value() == base.VALID_TOPIC, "주제 입력값이 유지되지 않았습니다."
        assert page.is_quiz_submit_button_enabled(), (
            "주제 입력 후 다시 생성 버튼이 활성화되지 않았습니다."
        )
        self.show_step(page, 4, "주제 입력 후 다시 생성 버튼 활성화 확인")
        logger.info(f"[{scenario}] 주제 재입력 후 다시 생성 버튼 활성화 확인 완료")

    @allure.story("Blank topic validation")
    @allure.title("퀴즈 공백 주제 입력 시 버튼 비활성화 검증")
    @pytest.mark.detail
    def test_quiz_blank_topic_disables_submit_button(self, logged_in_driver):
        """
        퀴즈 공백 주제 입력 시 다시 생성 버튼 상태 검증 시나리오

        커버 TC: TC 미등록 - TC_113 확장 케이스

        Step 1. 로그인 상태로 퀴즈 생성 페이지 진입
        Step 2. 공백만 있는 주제 입력
        Step 3. 다시 생성 버튼 비활성화 확인
        Step 4. 주제 필수 에러 메시지 확인
        """
        scenario = "공백 주제 입력 시 다시 생성 버튼 상태 검증"
        page = self.setup_page(logged_in_driver, scenario)

        page.clear_topic_input()
        page.enter_topic(base.BLANK_TOPIC)
        page.blur_active_element()

        assert page.is_quiz_submit_button_disabled(), (
            "공백만 입력한 주제에서 다시 생성 버튼이 비활성화되지 않았습니다."
        )
        error_message = page.get_error_message_text()
        self.assert_error_message_equals(
            error_message,
            base.QUIZ_TOPIC_REQUIRED_ERROR_MESSAGE,
            "퀴즈 공백 주제",
        )
        self.show_step(page, 3, "공백 주제 입력 시 다시 생성 버튼 비활성화 확인")
        self.show_step(page, 4, "공백 주제 필수 에러 메시지 확인")
        logger.info(f"[{scenario}] 공백 주제 에러 메시지: {error_message}")

    @allure.story("Generation stop")
    @allure.title("퀴즈 생성 중지 검증")
    @pytest.mark.detail
    def test_quiz_create_stop(self, logged_in_driver):
        """
        퀴즈 생성 중지 시나리오

        커버 TC: TC 미등록 - 생성 중지 추가 자동화 시나리오

        Step 1. 로그인 상태로 퀴즈 생성 페이지 진입
        Step 2. 유형 드롭다운에서 객관식 단일 선택
        Step 3. 난이도 드롭다운에서 하 선택
        Step 4. 주제 입력값 확인
        Step 5. 다시 생성 버튼 클릭
        Step 6. 모달 내부 다시 생성 버튼 클릭
        Step 7. 생성 시작 확인
        Step 8. 생성 중지 버튼 클릭
        Step 9. 생성 중지 메시지 출력 확인
        """
        scenario = "퀴즈 생성 중지"
        page = self.setup_page(logged_in_driver, scenario)

        self.select_default_options(page, scenario)
        self.enter_valid_topic(page, scenario)
        self.start_generation(page, scenario)

        page.click_stop_button()
        self.show_step(page, 8, "생성 중지 버튼 클릭")
        logger.info(f"[{scenario}] 생성 중지 버튼 클릭 완료")

        stop_message = page.get_stop_message_text()
        self.assert_error_message_equals(
            stop_message,
            base.QUIZ_STOP_MESSAGE_TITLE,
            "퀴즈 생성 중지",
        )
        self.show_step(page, 9, "생성 중지 메시지 확인")
        logger.info(f"[{scenario}] 생성 중지 메시지: {stop_message}")

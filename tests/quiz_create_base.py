import logging

from selenium.webdriver.support.ui import WebDriverWait

from pages.quiz_page import QuizPage


logger = logging.getLogger(__name__)

VALID_TOPIC = "한글을 만든 사람은?"
SUBJECTIVE_TOPIC = "넌센스"
COMPLEX_TOPIC = '가것ABab01!"'
BLANK_TOPIC = "   "
LONG_TOPIC_LENGTH = 5000
QUIZ_TYPE_SINGLE_CHOICE = "0"
QUIZ_TYPE_SUBJECTIVE = "3"
QUIZ_TYPE_SINGLE_CHOICE_TEXT = "객관식 (단일 선택)"
QUIZ_TYPE_SUBJECTIVE_TEXT = "주관식"
QUIZ_DIFFICULTY_LOW = "Level1"
QUIZ_DIFFICULTY_MEDIUM = "Level2"
QUIZ_DIFFICULTY_HIGH = "Level3"
QUIZ_DIFFICULTY_LOW_TEXT = "하"
GENERATION_TIMEOUT_SECONDS = 600
QUIZ_TOPIC_REQUIRED_ERROR_MESSAGE = "1자 이상 입력해주세요."
QUIZ_STOP_MESSAGE_TITLE = "요청에 의해 답변 생성을 중지했습니다."


class QuizCreateBase:
    def setup_quiz_page(self, logged_in_driver):
        self.driver = logged_in_driver
        self.long_wait = WebDriverWait(self.driver, GENERATION_TIMEOUT_SECONDS)
        self.quiz_page = QuizPage(self.driver)

    def show_step(self, page, step_no, message):
        page.show_step(f"Step.{step_no} {message}")

    def assert_error_message_equals(self, actual_message, expected_message, field_name):
        assert actual_message == expected_message, (
            f"{field_name} 에러 메시지가 한국어 기준 문구와 일치하지 않습니다. "
            f"expected={expected_message}, actual={actual_message}"
        )

    def setup_page(self, logged_in_driver, scenario):
        self.setup_quiz_page(logged_in_driver)
        page = self.quiz_page

        page.navigate_to_quiz_page()
        page.verify_quiz_page_url()
        self.show_step(page, 1, f"퀴즈 생성 페이지 진입 - {scenario}")
        logger.info(f"[{scenario}] 퀴즈 생성 페이지 이동 완료")

        return page

    def select_default_options(self, page, scenario):
        page.select_mui_dropdown(
            page.QUIZ_TYPE_DROPDOWN,
            option_value=QUIZ_TYPE_SINGLE_CHOICE,
        )
        self.show_step(page, 2, "유형 드롭다운 선택")
        logger.info(f"[{scenario}] 유형 선택 완료: {QUIZ_TYPE_SINGLE_CHOICE}")

        page.select_mui_dropdown(
            page.QUIZ_DIFFICULTY_DROPDOWN,
            option_value=QUIZ_DIFFICULTY_LOW,
        )
        self.show_step(page, 3, "난이도 드롭다운 선택")
        logger.info(f"[{scenario}] 난이도 선택 완료: {QUIZ_DIFFICULTY_LOW}")

    def enter_valid_topic(self, page, scenario):
        page.clear_topic_input()
        page.enter_topic(VALID_TOPIC)

        assert page.get_topic_value() == VALID_TOPIC, "주제 입력값이 유지되지 않았습니다."
        self.show_step(page, 4, "주제 입력값 확인")
        logger.info(f"[{scenario}] 주제 입력 완료")

    def start_generation(self, page, scenario):
        assert page.is_quiz_submit_button_enabled(), (
            "퀴즈 생성 버튼이 활성화되지 않았습니다."
        )

        page.click_quiz_submit_button()
        self.show_step(page, 5, "다시 생성 버튼 클릭")
        logger.info(f"[{scenario}] 다시 생성 버튼 클릭 완료")

        assert page.is_regenerate_modal_visible(), (
            "다시 생성 확인 모달이 표시되지 않았습니다."
        )
        page.click_modal_regenerate_button()
        self.show_step(page, 6, "모달 내부 다시 생성 버튼 클릭")
        logger.info(f"[{scenario}] 모달 내부 다시 생성 버튼 클릭 완료")

        self.show_step(page, 7, "생성 시작 확인")
        page.wait_until_submit_button_disabled(self.long_wait)
        logger.info(f"[{scenario}] 생성 시작 확인 완료")

import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from pages.ppt_page import PptPage


logger = logging.getLogger(__name__)

VALID_TOPIC = "초등학교 수학 문제"
VALID_INSTRUCTIONS = "더하기 빼기 위주로 주어진 값이 5를 넘지 않는 문제 2개만 내줘"
COMPLEX_TEXT = '가것 ABab01! @2026 테스트'
BLANK_TOPIC = "   "
VALID_SLIDES_COUNT = "6"
VALID_SECTION_COUNT = "2"
MIN_SLIDES_COUNT = "3"
MAX_SLIDES_COUNT = "50"
MIN_SECTION_COUNT = "1"
MAX_SECTION_COUNT = "8"
INVALID_NUMERIC_TEXT = '가것ABab01!"'
NUMERIC_TEXT_EXTRACTED_VALUE = "1"
MAX_TOPIC_LENGTH = 500
OVER_TOPIC_LENGTH = MAX_TOPIC_LENGTH + 1
MAX_INSTRUCTIONS_LENGTH = 2000
OVER_INSTRUCTIONS_LENGTH = MAX_INSTRUCTIONS_LENGTH + 1
GENERATION_TIMEOUT_SECONDS = 600
DOWNLOAD_TIMEOUT_SECONDS = 60
LONG_SLIDES_COUNT = "111111111111111111111111"
LONG_SECTION_COUNT = "1000000000000000000000"
LONG_NUMERIC_FIELD_CASES = (
    ("enter_slides_count", "get_slides_count_value", LONG_SLIDES_COUNT, "슬라이드 수", "TC_066, TC_067, TC_073"),
    ("enter_section_count", "get_section_count_value", LONG_SECTION_COUNT, "섹션 수", "TC_079, TC_080"),
)

TOPIC_LENGTH_ERROR_MESSAGE = "1자 이상 500자 이하로 입력해주세요."
INSTRUCTIONS_LENGTH_ERROR_MESSAGE = "2000자 이하로 입력해주세요."
SLIDES_COUNT_RANGE_ERROR_MESSAGE = "3 이상 50 이하로 입력해주세요."
SECTION_COUNT_RANGE_ERROR_MESSAGE = "1 이상 8 이하로 입력해주세요."
STOP_MESSAGE_KEYWORDS = {
    "요청에 의해 답변 생성을 중지했습니다.",
    "stopped",
    "停止",
}


def multiline_text(base_text, target_length):
    line = f"{base_text}\n"
    repeat_count = (target_length // len(line)) + 1
    return (line * repeat_count)[:target_length]


class PptCreateBase:
    def setup_ppt_page(self, logged_in_driver):
        self.driver = logged_in_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.long_wait = WebDriverWait(self.driver, GENERATION_TIMEOUT_SECONDS)
        self.download_wait = WebDriverWait(self.driver, DOWNLOAD_TIMEOUT_SECONDS)
        self.ppt_page = PptPage(self.driver)

    def assert_error_message_equals(self, actual_message, expected_message, field_name):
        assert actual_message == expected_message, (
            f"{field_name} 에러 메시지가 한국어 기준 문구와 일치하지 않습니다. "
            f"expected={expected_message}, actual={actual_message}"
        )

    def assert_range_error_message(self, actual_message, field_name):
        self.assert_error_message_equals(
            actual_message,
            SLIDES_COUNT_RANGE_ERROR_MESSAGE,
            field_name,
        )

    def assert_section_range_error_message(self, actual_message, field_name):
        self.assert_error_message_equals(
            actual_message,
            SECTION_COUNT_RANGE_ERROR_MESSAGE,
            field_name,
        )

    def assert_count_error_hidden(self, actual_message, field_name):
        assert not actual_message, f"{field_name} 정상 경계값 입력 후 에러 메시지가 남아 있습니다."

    def assert_generate_enabled(self, page):
        assert page.is_generate_enabled(), "PPT 생성 버튼이 활성화되지 않았습니다."

    def assert_generate_disabled(self, page):
        assert page.is_generate_button_disabled(), "PPT 생성 버튼이 비활성화되지 않았습니다."

    def assert_topic_error_visible(self, page):
        message = page.get_topic_error_text()
        assert message, "주제 에러 메시지가 표시되지 않았습니다."
        return message

    def assert_topic_error_hidden(self, page):
        assert not page.get_topic_error_text(), "주제 에러 메시지가 남아 있습니다."

    def assert_instructions_error_visible(self, page):
        message = page.get_instructions_error_text()
        assert message, "지시사항 에러 메시지가 표시되지 않았습니다."
        return message

    def assert_instructions_error_hidden(self, page):
        assert not page.get_instructions_error_text(), "지시사항 에러 메시지가 남아 있습니다."

    def setup_page(self, logged_in_driver, scenario):
        self.setup_ppt_page(logged_in_driver)
        page = self.ppt_page

        page.navigate()
        page.verify_ppt_page_url()
        page.show_step(f"Step.1 PPT 생성 페이지 진입 - {scenario}")
        logger.info(f"[{scenario}] PPT 생성 페이지 이동 완료")

        page.clear_inputs()
        page.show_step(f"Step.2 입력 필드 초기화 - {scenario}")
        logger.info(f"[{scenario}] 입력 필드 초기화 완료")

        return page

    def enter_valid_inputs(self, page):
        page.enter_topic(VALID_TOPIC)
        page.enter_instructions(VALID_INSTRUCTIONS)
        page.enter_slides_count(VALID_SLIDES_COUNT)
        page.enter_section_count(VALID_SECTION_COUNT)

        assert page.get_topic_value() == VALID_TOPIC, "주제 입력값이 유지되지 않았습니다."
        assert page.get_instructions_value() == VALID_INSTRUCTIONS, (
            "지시사항 입력값이 유지되지 않았습니다."
        )
        assert page.get_slides_count_value() == VALID_SLIDES_COUNT, (
            "슬라이드 수 입력값이 유지되지 않았습니다."
        )
        assert page.get_section_count_value() == VALID_SECTION_COUNT, (
            "섹션 수 입력값이 유지되지 않았습니다."
        )
        self.assert_generate_enabled(page)

    def start_generation(self, page, scenario):
        self.assert_generate_enabled(page)

        page.click_generate_button()
        page.show_step("Step.4 생성 버튼 클릭")
        logger.info(f"[{scenario}] 생성 버튼 클릭 완료")

        try:
            page.click_modal_generate_button()
            page.show_step("Step.5 모달 내부 생성 버튼 클릭")
            logger.info(f"[{scenario}] 모달 내부 생성 버튼 클릭 완료")
        except TimeoutException:
            logger.info(f"[{scenario}] 확인 모달 없이 생성이 시작되었습니다.")

        page.show_step("Step.6 생성 시작 확인")
        page.wait_until_generation_starts(self.long_wait)
        logger.info(f"[{scenario}] 생성 시작 확인 완료")

    def wait_generation_complete(self, page, scenario):
        page.show_step("Step.7 생성 완료 확인")
        page.wait_until_generation_completes(self.long_wait)
        assert page.is_result_download_button_visible(), (
            "PPT 생성 결과 다운로드 버튼이 표시되지 않았습니다."
        )
        logger.info(f"[{scenario}] 생성 완료 확인")

    def download_result(self, page, scenario, download_dir):
        before_files = set(download_dir.iterdir())

        page.click_download_button()
        page.show_step("Step.8 생성 결과 다운로드 버튼 클릭")
        logger.info(f"[{scenario}] 생성 결과 다운로드 버튼 클릭 완료")

        def is_download_completed(driver):
            current_files = set(download_dir.iterdir())
            new_files = current_files - before_files
            downloading = any(file.name.endswith(".crdownload") for file in current_files)
            pptx_files = [
                file for file in new_files
                if file.is_file() and file.suffix.lower() == ".pptx"
            ]
            return pptx_files and not downloading

        self.download_wait.until(is_download_completed)
        after_files = set(download_dir.iterdir())
        new_files = after_files - before_files
        downloaded_files = [
            file for file in new_files
            if file.is_file() and file.suffix.lower() == ".pptx"
        ]
        assert downloaded_files, "PPTX 다운로드 파일이 생성되지 않았습니다."
        assert all(file.stat().st_size > 0 for file in downloaded_files), (
            f"다운로드된 PPTX 파일 크기가 0입니다. files={downloaded_files}"
        )
        page.show_step("Step.9 다운로드 완료 확인")
        logger.info(f"[{scenario}] 다운로드 완료 파일: {[file.name for file in downloaded_files]}")

        for file in downloaded_files:
            file.unlink()
        logger.info(f"[{scenario}] 다운로드 검증 파일 삭제 완료")

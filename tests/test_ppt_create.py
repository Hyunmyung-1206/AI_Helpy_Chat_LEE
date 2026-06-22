import logging

import pytest

import ppt_create_base as base


logger = logging.getLogger(__name__)


class TestPptCreate(base.PptCreateBase):
    @pytest.mark.detail
    def test_ppt_topic_validation(self, logged_in_driver):
        """
        PPT 주제 입력값 검증 시나리오

        커버 TC: TC_055, TC_056, TC_057

        Step 1. 로그인 상태로 PPT 생성 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 주제 0자 입력
        Step 4. 주제 0자 에러 메시지 출력 확인
        Step 5. 주제 500자 입력값 길이 확인
        Step 6. 주제 501자 에러 메시지 출력 확인
        Step 7. 한글 / 영문 대소문자 / 숫자 / 특수문자 / 띄어쓰기 주제 입력 확인
        """
        scenario = "주제 입력값 검증"
        page = self.setup_page(logged_in_driver, scenario)

        page.enter_topic("")
        page.blur_active_element()
        page.show_step("Step.3 주제 0자 입력")
        empty_error = self.assert_topic_error_visible(page)
        self.assert_error_message_equals(empty_error, base.TOPIC_LENGTH_ERROR_MESSAGE, "주제 0자")
        page.show_step("Step.4 주제 0자 에러 메시지 확인")
        logger.info(f"[{scenario}] 주제 0자 에러 메시지: {empty_error}")

        page.enter_topic("달" * base.MAX_TOPIC_LENGTH)
        actual_length = len(page.get_topic_value())
        assert actual_length == base.MAX_TOPIC_LENGTH, (
            f"주제 입력값 길이가 다릅니다. expected={base.MAX_TOPIC_LENGTH}, actual={actual_length}"
        )
        self.assert_topic_error_hidden(page)
        page.show_step("Step.5 주제 500자 입력값 길이 확인")

        page.enter_topic("달" * base.OVER_TOPIC_LENGTH)
        page.blur_active_element()
        over_limit_error = self.assert_topic_error_visible(page)
        self.assert_error_message_equals(
            over_limit_error,
            base.TOPIC_LENGTH_ERROR_MESSAGE,
            "주제 501자",
        )
        page.show_step("Step.6 주제 501자 에러 메시지 확인")
        logger.info(f"[{scenario}] 주제 501자 에러 메시지: {over_limit_error}")

        page.enter_topic(base.COMPLEX_TEXT)
        assert page.get_topic_value() == base.COMPLEX_TEXT, "복합 주제 입력값이 유지되지 않았습니다."
        self.assert_topic_error_hidden(page)
        page.show_step("Step.7 한글 / 영문 대소문자 / 숫자 / 특수문자 / 띄어쓰기 주제 입력 확인")

    @pytest.mark.detail
    def test_ppt_instructions_validation(self, logged_in_driver):
        """
        PPT 지시사항 입력값 검증 시나리오

        커버 TC: TC_059, TC_060, TC_061

        Step 1. 로그인 상태로 PPT 생성 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 한글 / 영문 대소문자 / 숫자 / 특수문자 / 띄어쓰기 지시사항 입력 확인
        Step 4. 줄바꿈 포함 지시사항 2000자 입력값 확인
        Step 5. 지시사항 2001자 에러 메시지 출력 확인
        """
        scenario = "지시사항 입력값 검증"
        page = self.setup_page(logged_in_driver, scenario)

        page.enter_topic(base.VALID_TOPIC)
        page.enter_instructions(base.COMPLEX_TEXT)
        assert page.get_instructions_value() == base.COMPLEX_TEXT, (
            "복합 지시사항 입력값이 유지되지 않았습니다."
        )
        self.assert_instructions_error_hidden(page)
        page.show_step("Step.3 한글 / 영문 대소문자 / 숫자 / 특수문자 / 띄어쓰기 지시사항 입력 확인")

        valid_instructions = base.multiline_text("테스트", base.MAX_INSTRUCTIONS_LENGTH)
        page.enter_instructions(valid_instructions)
        actual_length = len(page.get_instructions_value())
        assert actual_length == base.MAX_INSTRUCTIONS_LENGTH, (
            "지시사항 2000자 입력값 길이가 다릅니다. "
            f"expected={base.MAX_INSTRUCTIONS_LENGTH}, actual={actual_length}"
        )
        self.assert_instructions_error_hidden(page)
        page.show_step("Step.4 줄바꿈 포함 지시사항 2000자 입력값 확인")

        over_limit_instructions = base.multiline_text("테스트", base.OVER_INSTRUCTIONS_LENGTH)
        page.enter_instructions(over_limit_instructions)
        page.blur_active_element()
        error_message = self.assert_instructions_error_visible(page)
        self.assert_error_message_equals(
            error_message,
            base.INSTRUCTIONS_LENGTH_ERROR_MESSAGE,
            "지시사항 2001자",
        )
        page.show_step("Step.5 지시사항 2001자 에러 메시지 확인")
        logger.info(f"[{scenario}] 지시사항 2001자 에러 메시지: {error_message}")

    @pytest.mark.detail
    @pytest.mark.parametrize(
        "slides_count, expected_error, field_name",
        [
            pytest.param(base.MIN_SLIDES_COUNT, "", "슬라이드 수 최소 경계값", id="min_valid_3"),
            pytest.param(base.MAX_SLIDES_COUNT, "", "슬라이드 수 최대 경계값", id="max_valid_50"),
            pytest.param("1", base.SLIDES_COUNT_RANGE_ERROR_MESSAGE, "슬라이드 수 1", id="below_min_1"),
            pytest.param("51", base.SLIDES_COUNT_RANGE_ERROR_MESSAGE, "슬라이드 수 51", id="above_max_51"),
        ],
    )
    def test_ppt_slide_count_validation(
        self,
        logged_in_driver,
        slides_count,
        expected_error,
        field_name,
    ):
        """
        PPT 슬라이드 수 입력값 검증 시나리오

        커버 TC: TC_063, TC_064, TC_065

        Step 1. 로그인 상태로 PPT 생성 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 파라미터 슬라이드 수 입력
        Step 4. 정상값은 에러 메시지 미노출, 범위 밖 값은 에러 메시지 출력 확인
        """
        scenario = f"슬라이드 수 입력값 검증 - {field_name}"
        page = self.setup_page(logged_in_driver, scenario)

        page.enter_slides_count(slides_count)
        page.blur_active_element()
        assert page.get_slides_count_value() == slides_count, (
            f"{field_name} 입력값이 유지되지 않았습니다."
        )
        page.show_step(f"Step.3 {field_name} 입력 확인")

        actual_error = page.get_slides_count_error_text()
        if expected_error:
            self.assert_range_error_message(actual_error, field_name)
            page.show_step(f"Step.4 {field_name} 에러 메시지 확인")
            logger.info(f"[{scenario}] {field_name} 에러 메시지: {actual_error}")
        else:
            self.assert_count_error_hidden(actual_error, field_name)
            page.show_step(f"Step.4 {field_name} 정상 입력 확인")

    @pytest.mark.detail
    @pytest.mark.parametrize(
        "section_count, expected_error, field_name",
        [
            pytest.param(base.MIN_SECTION_COUNT, "", "섹션 수 최소 경계값", id="min_valid_1"),
            pytest.param(base.MAX_SECTION_COUNT, "", "섹션 수 최대 경계값", id="max_valid_8"),
            pytest.param("9", base.SECTION_COUNT_RANGE_ERROR_MESSAGE, "섹션 수 9", id="above_max_9"),
        ],
    )
    def test_ppt_section_count_boundary_validation(
        self,
        logged_in_driver,
        section_count,
        expected_error,
        field_name,
    ):
        """
        PPT 섹션 수 경계값 검증 시나리오

        커버 TC: TC_076, TC_078

        Step 1. 로그인 상태로 PPT 생성 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 파라미터 섹션 수 입력
        Step 4. 정상값은 에러 메시지 미노출, 범위 밖 값은 에러 메시지 출력 확인
        """
        scenario = f"섹션 수 경계값 검증 - {field_name}"
        page = self.setup_page(logged_in_driver, scenario)

        page.enter_section_count(section_count)
        page.blur_active_element()
        assert page.get_section_count_value() == section_count, (
            f"{field_name} 입력값이 유지되지 않았습니다."
        )
        page.show_step(f"Step.3 {field_name} 입력 확인")

        actual_error = page.get_section_count_error_text()
        if expected_error:
            self.assert_section_range_error_message(actual_error, field_name)
            page.show_step(f"Step.4 {field_name} 에러 메시지 확인")
            logger.info(f"[{scenario}] {field_name} 에러 메시지: {actual_error}")
        else:
            self.assert_count_error_hidden(actual_error, field_name)
            page.show_step(f"Step.4 {field_name} 정상 입력 확인")

    @pytest.mark.detail
    @pytest.mark.parametrize(
        "enter_method_name, get_method_name, field_name",
        [
            pytest.param(
                "enter_slides_count",
                "get_slides_count_value",
                "슬라이드 수",
                id="slides_count",
            ),
            pytest.param(
                "enter_section_count",
                "get_section_count_value",
                "섹션 수",
                id="section_count",
            ),
        ],
    )
    def test_ppt_slide_and_section_count_reject_zero_input(
        self,
        logged_in_driver,
        enter_method_name,
        get_method_name,
        field_name,
    ):
        """
        PPT 슬라이드, 섹션 수 0 입력 차단 검증 시나리오

        커버 TC: TC_077, 슬라이드 수 0 입력 차단 추가 자동화 시나리오

        Step 1. 로그인 상태로 PPT 생성 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 슬라이드 수 또는 섹션 수 0 입력 불가 확인
        """
        scenario = f"슬라이드, 섹션 수 0 입력 차단 검증 - {field_name}"
        page = self.setup_page(logged_in_driver, scenario)

        enter_method = getattr(page, enter_method_name)
        get_method = getattr(page, get_method_name)

        enter_method("0")
        page.blur_active_element()
        assert get_method() == "", f"{field_name} 0 입력값이 차단되지 않았습니다."
        page.show_step(f"Step.3 {field_name} 0 입력 불가 확인")
        logger.info(f"[{scenario}] {field_name} 0 입력 불가 확인 완료")

    @pytest.mark.detail
    @pytest.mark.parametrize(
        "enter_method_name, get_method_name, field_name",
        [
            pytest.param(
                "enter_slides_count",
                "get_slides_count_value",
                "슬라이드 수",
                id="slides_count",
            ),
            pytest.param(
                "enter_section_count",
                "get_section_count_value",
                "섹션 수",
                id="section_count",
            ),
        ],
    )
    def test_ppt_numeric_fields_reject_text(
        self,
        logged_in_driver,
        enter_method_name,
        get_method_name,
        field_name,
    ):
        """
        PPT 슬라이드, 섹션 수 문자 포함 입력값 검증 시나리오

        커버 TC: TC_074 일부, 섹션 수 문자 입력 추가 자동화 시나리오

        Step 1. 로그인 상태로 PPT 생성 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 슬라이드 수 또는 섹션 수에 문자 포함 값 입력
        Step 4. 숫자만 추출되어 반영되는지 확인
        """
        scenario = f"슬라이드, 섹션 수 문자 포함 입력값 검증 - {field_name}"
        page = self.setup_page(logged_in_driver, scenario)

        enter_method = getattr(page, enter_method_name)
        get_method = getattr(page, get_method_name)

        enter_method(base.INVALID_NUMERIC_TEXT)
        assert get_method() == base.NUMERIC_TEXT_EXTRACTED_VALUE, (
            f"{field_name} 필드가 문자 포함 입력에서 숫자만 반영하지 않았습니다."
        )
        page.show_step(f"Step.3 {field_name} 필드 문자 포함 입력 시 숫자만 반영 확인")
        logger.info(f"[{scenario}] {field_name} 문자 포함 입력값 검증 완료")

    @pytest.mark.detail
    @pytest.mark.xfail(
        reason="Known issue: 숫자 입력 필드의 긴 숫자 입력값이 지수 표기/Infinity로 변환됨",
        strict=True,
    )
    @pytest.mark.parametrize(
        "enter_method_name, get_method_name, long_value, field_name, cover_tc",
        base.LONG_NUMERIC_FIELD_CASES,
    )
    def test_ppt_numeric_field_long_value_cases(
        self,
        logged_in_driver,
        enter_method_name,
        get_method_name,
        long_value,
        field_name,
        cover_tc,
    ):
        """
        PPT 숫자 필드 긴 입력값 변환 검증 시나리오

        커버 TC: TC_066, TC_067, TC_073, TC_079, TC_080 중심

        Step 1. 로그인 상태로 PPT 생성 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 숫자 필드에 긴 입력값 입력
        Step 4. 긴 입력값이 지수 표기 / Infinity로 변환되지 않고 원본 유지되는지 확인
        """
        scenario = f"{field_name} 긴 입력값 변환 검증 - {cover_tc}"
        page = self.setup_page(logged_in_driver, scenario)
        enter_method = getattr(page, enter_method_name)
        get_method = getattr(page, get_method_name)

        enter_method(long_value)
        assert get_method() == long_value, (
            f"{field_name} 긴 입력값이 원본 그대로 유지되지 않았습니다. "
            f"expected={long_value}, actual={get_method()}"
        )
        page.show_step(f"Step.4 {field_name} 긴 입력값 원본 유지 확인")

    @pytest.mark.detail
    def test_ppt_generate_button_state(self, logged_in_driver):
        """
        PPT 생성 버튼 상태 검증 시나리오

        커버 TC: TC_083, TC_084, TC_091, TC_098, TC_101 일부

        Step 1. 로그인 상태로 PPT 생성 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 주제 미입력 상태 생성 버튼 비활성화 확인
        Step 4. 주제 미입력 / 지시사항 입력 상태 생성 버튼 비활성화 확인
        Step 5. 주제 입력 / 지시사항 미입력 상태 생성 버튼 활성화 확인
        Step 6. 주제만 입력한 상태 생성 버튼 활성화 확인
        Step 7. 전체 입력값 입력 상태 생성 버튼 활성화 확인
        """
        scenario = "생성 버튼 상태 검증"
        page = self.setup_page(logged_in_driver, scenario)

        self.assert_generate_disabled(page)
        page.show_step("Step.3 주제 미입력 상태 생성 버튼 비활성화 확인")
        logger.info(f"[{scenario}] 주제 미입력 상태 생성 버튼 비활성화 확인 완료")

        page.enter_instructions(base.VALID_INSTRUCTIONS)
        self.assert_generate_disabled(page)
        page.show_step("Step.4 주제 미입력 / 지시사항 입력 상태 생성 버튼 비활성화 확인")
        logger.info(f"[{scenario}] 주제 미입력 / 지시사항 입력 상태 생성 버튼 비활성화 확인 완료")

        page.enter_topic(base.VALID_TOPIC)
        page.enter_instructions("")
        self.assert_generate_enabled(page)
        page.show_step("Step.5 주제 입력 / 지시사항 미입력 상태 생성 버튼 활성화 확인")
        logger.info(f"[{scenario}] 주제 입력 / 지시사항 미입력 상태 생성 버튼 활성화 확인 완료")

        page.enter_topic(base.VALID_TOPIC)
        page.enter_slides_count("")
        page.enter_section_count("")
        self.assert_generate_enabled(page)
        page.show_step("Step.6 주제만 입력한 상태 생성 버튼 활성화 확인")
        logger.info(f"[{scenario}] 주제만 입력한 상태 생성 버튼 활성화 확인 완료")

        page.enter_instructions(base.VALID_INSTRUCTIONS)
        page.enter_slides_count(base.VALID_SLIDES_COUNT)
        page.enter_section_count(base.VALID_SECTION_COUNT)
        self.assert_generate_enabled(page)
        page.show_step("Step.7 전체 입력값 입력 상태 생성 버튼 활성화 확인")
        logger.info(f"[{scenario}] 전체 입력값 입력 상태 생성 버튼 활성화 확인 완료")

    @pytest.mark.detail
    def test_ppt_topic_delete_disables_generate_button(self, logged_in_driver):
        """
        PPT 주제 삭제 시 다시생성 버튼 상태 검증 시나리오

        커버 TC: TC_057 일부, 주제 삭제 추가 자동화 시나리오

        Step 1. 로그인 상태로 PPT 생성 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 주제 정상값 입력 후 다시생성 버튼 활성화 확인
        Step 4. 주제 입력값 삭제 후 다시생성 버튼 비활성화 확인
        """
        scenario = "주제 삭제 시 다시생성 버튼 상태 검증"
        page = self.setup_page(logged_in_driver, scenario)

        page.enter_topic(base.VALID_TOPIC)
        assert page.get_topic_value() == base.VALID_TOPIC, "주제 입력값이 유지되지 않았습니다."
        self.assert_generate_enabled(page)
        page.show_step("Step.3 주제 정상값 입력 후 다시생성 버튼 활성화 확인")
        logger.info(f"[{scenario}] 주제 정상값 입력 후 다시생성 버튼 활성화 확인 완료")

        page.clear_topic()
        page.blur_active_element()
        assert page.get_topic_value() == "", "주제 입력값이 삭제되지 않았습니다."
        self.assert_generate_disabled(page)
        page.show_step("Step.4 주제 입력값 삭제 후 다시생성 버튼 비활성화 확인")
        logger.info(f"[{scenario}] 주제 입력값 삭제 후 다시생성 버튼 비활성화 확인 완료")

    @pytest.mark.detail
    @pytest.mark.xfail(
        reason="Known issue: 공백만 있는 주제가 유효값으로 처리되어 다시생성 버튼이 활성화됨"
    )
    def test_ppt_blank_topic_disables_generate_button(self, logged_in_driver):
        """
        PPT 공백 주제 입력 시 다시생성 버튼 상태 검증 시나리오

        커버 TC: TC 미등록 - 공백 주제 버그 리포트용

        Step 1. 로그인 상태로 PPT 생성 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 공백만 있는 주제 에러 메시지 및 다시생성 버튼 비활성화 확인
        """
        scenario = "공백 주제 입력 시 다시생성 버튼 상태 검증"
        page = self.setup_page(logged_in_driver, scenario)

        page.enter_topic(base.BLANK_TOPIC)
        page.blur_active_element()

        blank_error = self.assert_topic_error_visible(page)
        self.assert_error_message_equals(blank_error, base.TOPIC_LENGTH_ERROR_MESSAGE, "공백 주제")
        self.assert_generate_disabled(page)
        page.show_step("Step.3 공백만 있는 주제 에러 메시지 및 다시생성 버튼 비활성화 확인")
        logger.info(f"[{scenario}] 공백 주제 에러 메시지: {blank_error}")

    @pytest.mark.detail
    def test_ppt_create_stop(self, logged_in_driver):
        """
        PPT 생성 중지 시나리오

        커버 TC: TC 미등록 - 생성 중지 추가 자동화 시나리오

        Step 1. 로그인 상태로 PPT 생성 페이지 진입
        Step 2. 입력 필드 초기화
        Step 3. 주제 / 지시사항 / 슬라이드 수 / 섹션 수 입력
        Step 4. 생성 버튼 클릭
        Step 5. 모달 내부 생성 버튼 클릭
        Step 6. 생성 시작 확인
        Step 7. 생성 중지 버튼 클릭
        Step 8. 생성 중지 메시지 출력 확인
        """
        scenario = "생성 중지"
        page = self.setup_page(logged_in_driver, scenario)

        self.enter_valid_inputs(page)
        page.show_step("Step.3 주제 / 지시사항 / 슬라이드 수 / 섹션 수 입력")

        self.start_generation(page, scenario)

        page.click_stop_button()
        page.show_step("Step.7 생성 중지 버튼 클릭")
        logger.info(f"[{scenario}] 생성 중지 버튼 클릭 완료")

        stop_message = page.get_stop_message_text()
        assert stop_message, "생성 중지 메시지가 표시되지 않았습니다."
        assert any(keyword in stop_message for keyword in base.STOP_MESSAGE_KEYWORDS), (
            f"생성 중지 메시지가 기대 범위와 다릅니다. actual={stop_message}"
        )
        page.show_step("Step.8 생성 중지 메시지 확인")
        logger.info(f"[{scenario}] 생성 중지 메시지: {stop_message}")


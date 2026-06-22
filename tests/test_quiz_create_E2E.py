import logging

import allure
import pytest

import quiz_create_base as base


logger = logging.getLogger(__name__)


@allure.feature("Quiz Create")
@allure.story("E2E generation")
class TestQuizCreateE2E(base.QuizCreateBase):
    @allure.title("퀴즈 객관식 생성 E2E")
    @pytest.mark.slow
    def test_quiz_create(self, logged_in_driver):
        """
        퀴즈 객관식 생성 시나리오

        커버 TC: TC_103, TC_121, TC_123, TC_124

        Step 1. 로그인 상태로 퀴즈 생성 페이지 진입
        Step 2. 유형 드롭다운에서 객관식 단일 선택
        Step 3. 난이도 드롭다운에서 하 선택
        Step 4. 주제 입력값 확인
        Step 5. 다시 생성 버튼 클릭
        Step 6. 모달 내부 다시 생성 버튼 클릭
        Step 7. 생성 시작 확인
        Step 8. 생성 완료 및 퀴즈 결과 노출 확인
        """
        scenario = "퀴즈 생성"
        page = self.setup_page(logged_in_driver, scenario)

        self.select_default_options(page, scenario)
        self.enter_valid_topic(page, scenario)
        self.start_generation(page, scenario)

        self.show_step(page, 8, "생성 완료 확인")
        page.wait_until_submit_button_enabled(self.long_wait)
        assert page.is_quiz_result_visible(), "퀴즈 생성 결과가 표시되지 않았습니다."
        logger.info(f"[{scenario}] 생성 완료 확인")

    @allure.title("퀴즈 주관식 생성 E2E")
    @pytest.mark.slow
    def test_quiz_create_subjective_type(self, logged_in_driver):
        """
        퀴즈 주관식 생성 시나리오

        커버 TC: TC_103, TC_105, TC_107, TC_108, TC_122

        Step 1. 로그인 상태로 퀴즈 생성 페이지 진입
        Step 2. 유형 드롭다운에서 주관식 선택
        Step 3. 난이도 드롭다운에서 하 선택
        Step 4. 주제 입력값 확인
        Step 5. 다시 생성 버튼 클릭
        Step 6. 모달 내부 다시 생성 버튼 클릭
        Step 7. 생성 시작 확인
        Step 8. 생성 완료 및 주관식 퀴즈 결과 노출 확인
        """
        scenario = "주관식 퀴즈 생성"
        page = self.setup_page(logged_in_driver, scenario)

        page.select_mui_dropdown(
            page.QUIZ_TYPE_DROPDOWN,
            option_value=base.QUIZ_TYPE_SUBJECTIVE,
        )
        self.show_step(page, 2, "주관식 유형 선택")
        logger.info(f"[{scenario}] 유형 선택 완료: {base.QUIZ_TYPE_SUBJECTIVE}")

        page.select_mui_dropdown(
            page.QUIZ_DIFFICULTY_DROPDOWN,
            option_value=base.QUIZ_DIFFICULTY_LOW,
        )
        self.show_step(page, 3, "하 난이도 선택")
        logger.info(f"[{scenario}] 난이도 선택 완료: {base.QUIZ_DIFFICULTY_LOW}")

        page.clear_topic_input()
        page.enter_topic(base.SUBJECTIVE_TOPIC)
        assert page.get_topic_value() == base.SUBJECTIVE_TOPIC, "주관식 생성 주제 입력값이 유지되지 않았습니다."
        self.show_step(page, 4, "주제 입력")
        logger.info(f"[{scenario}] 주제 입력 완료")

        self.start_generation(page, scenario)

        self.show_step(page, 8, "생성 완료 확인")
        page.wait_until_submit_button_enabled(self.long_wait)
        assert page.is_quiz_result_visible(), "주관식 퀴즈 생성 결과가 표시되지 않았습니다."
        logger.info(f"[{scenario}] 생성 완료 확인")

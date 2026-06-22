FROM ai-helpy-chat-golden:local

WORKDIR /app

COPY . .

CMD ["pytest", "tests/test_quiz_create.py", "tests/test_ppt_create.py", "tests/test_deep_create.py", "-n", "3", "--browser", "chrome", "--junitxml=reports/junit.xml"]

FROM python:3.14-slim

ENV PYTHONUTF8=1 \
    PYTHONIOENCODING=utf-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "tests/test_quiz_create.py", "tests/test_ppt_create.py", "tests/test_deep_create.py", "-n", "3", "--browser", "chrome", "--junitxml=reports/junit.xml"]

FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PYTHONIOENCODING=utf-8 \
    HEADLESS=true

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "-n", "3", "-m", "not slow", "tests/test_quiz_create.py", "tests/test_ppt_create.py", "tests/test_deep_create.py", "--tb=short"]

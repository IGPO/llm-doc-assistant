# -------------------- BUILDER STAGE --------------------
FROM python:3.12-slim AS builder

# Установка Poetry
RUN pip install poetry

# Создание рабочей директории
WORKDIR /app

# Копируем только зависимости для кэширования
COPY pyproject.toml poetry.lock* ./

# Конфигурация Poetry: виртуальное окружение внутри проекта
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root --no-interaction --no-ansi

# Копируем остальной код
COPY . .

# -------------------- FINAL STAGE --------------------
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем виртуальное окружение из builder
COPY --from=builder /app/.venv /opt/venv

# Копируем приложение
COPY --from=builder /app /app

# Устанавливаем переменные окружения
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Открываем порт
EXPOSE 8000

# Запуск FastAPI-приложения
CMD ["uvicorn", "llm_doc_assistant.main:app", "--host", "0.0.0.0", "--port", "8000"]

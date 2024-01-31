FROM python:3.12

# Установка зависимостей проекта
COPY requirements.txt /app/requirements.txt

WORKDIR /app

ENV SECRET='your_secret'

RUN pip install -r requirements.txt

# Копирование файлов проекта
COPY . .

# Запуск скрипта
CMD python main.py
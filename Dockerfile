FROM python:3.12

# Установка зависимостей проекта
COPY requirements.txt /app/requirements.txt

ENV SECRET=''

RUN pip install --no-cache-dir -r /app/requirements.txt

# Копирование файлов проекта
COPY . /app
WORKDIR /app

# Запуск скрипта
CMD python main.py
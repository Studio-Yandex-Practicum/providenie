# Используем базовый образ Python 3.12
FROM python:3.12-bookworm

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Копируем исходники
COPY src/ .

# Команда для запуска
CMD ["python", "main.py"]

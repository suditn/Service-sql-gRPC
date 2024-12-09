# Используем официальный Python-образ
FROM python:3.12

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Указываем порт для gRPC
EXPOSE 50051

# Команда для запуска gRPC-сервера
CMD ["python", "grpc_server.py"]
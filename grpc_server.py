import grpc
from concurrent import futures
import sqlite3
from datetime import datetime
import traffic_pb2
import traffic_pb2_grpc

# Реализация сервиса
class TrafficService(traffic_pb2_grpc.TrafficServiceServicer):
    def GetTotalTraffic(self, request, context):
        # Подключаемся к базе данных SQLite
        conn = sqlite3.connect("traffic_db.sqlite")
        cursor = conn.cursor()

        # Формируем запрос с фильтрацией
        query = """
        SELECT SUM(received_traffic) FROM traffic
        JOIN customers ON traffic.customer_id = customers.id
        WHERE customers.name = ?
        """
        params = [request.customer_name]

        # Добавляем фильтры по дате
        if request.start_date:
            query += " AND date >= ?"
            params.append(request.start_date)
        if request.end_date:
            query += " AND date <= ?"
            params.append(request.end_date)
        if request.ip:
            query += " AND ip = ?"
            params.append(request.ip)

        # Выполняем запрос
        cursor.execute(query, params)
        result = cursor.fetchone()
        total_traffic = result[0] if result[0] else 0.0

        # Закрываем соединение с базой
        conn.close()

        # Возвращаем результат
        return traffic_pb2.TrafficResponse(
            customer_name=request.customer_name,
            total_traffic=total_traffic,
        )

# Запуск сервера
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    traffic_pb2_grpc.add_TrafficServiceServicer_to_server(TrafficService(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC сервер запущен на порту 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

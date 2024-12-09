import grpc
from concurrent import futures
import sqlite3
from datetime import datetime
import traffic_pb2
import traffic_pb2_grpc

# Реализация сервиса
class TrafficService(traffic_pb2_grpc.TrafficServiceServicer):
    def GetTotalTraffic(self, request, context):
        conn = sqlite3.connect("traffic_db.sqlite")
        cursor = conn.cursor()

        # Базовый запрос для всех клиентов
        query = """
        SELECT customers.name, SUM(received_traffic)
        FROM traffic
        JOIN customers ON traffic.customer_id = customers.id
        WHERE 1=1
        """
        params = []

        # Фильтрация по имени клиента
        if request.customer_name:
            query += " AND customers.name = ?"
            params.append(request.customer_name)

        # Фильтрация по диапазону дат
        if request.start_date:
            query += " AND date >= ?"
            params.append(request.start_date)
        if request.end_date:
            query += " AND date <= ?"
            params.append(request.end_date)

        # Фильтрация по ip
        if request.ip:
            query += " AND ip = ?"
            params.append(request.ip)

        # Группировка по клиентам
        query += " GROUP BY customers.name"

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        # Формируем ответ
        traffic_list = [
            traffic_pb2.CustomerTraffic(
                customer_name=row[0],
                total_traffic=row[1] if row[1] else 0.0
            )
            for row in results
        ]

        return traffic_pb2.AllTrafficResponse(traffic_list=traffic_list)

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

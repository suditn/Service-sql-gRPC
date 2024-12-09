import grpc
import traffic_pb2
import traffic_pb2_grpc

def run():
    # Подключаемся к gRPC-серверу
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = traffic_pb2_grpc.TrafficServiceStub(channel)

        # Создаём запрос
        request = traffic_pb2.TrafficRequest(
            customer_name="John Doe"#,
            #start_date="2022-01-05 00:00:00",
            #end_date="2026-05-02 23:59:59",
            #ip="192.168.218.159",
        )

        # Отправляем запрос и получаем ответ
        response = stub.GetTotalTraffic(request)
        print(f"Клиент: {response.customer_name}, Трафик: {response.total_traffic} МБ")

if __name__ == "__main__":
    run()

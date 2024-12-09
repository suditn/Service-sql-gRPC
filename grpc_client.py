import grpc
import traffic_pb2
import traffic_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = traffic_pb2_grpc.TrafficServiceStub(channel)

        # Пример запроса без фильтров
        print("Получение трафика без фильтров:")
        response = stub.GetTotalTraffic(traffic_pb2.TrafficRequest())

        for traffic in response.traffic_list:
            print(f"Клиент: {traffic.customer_name}, Трафик: {traffic.total_traffic} МБ")

        # Пример запроса с фильтром по имени
        print("\nПолучение трафика с фильтром по имени:")
        response = stub.GetTotalTraffic(traffic_pb2.TrafficRequest(customer_name="John Doe"))

        for traffic in response.traffic_list:
            print(f"Клиент: {traffic.customer_name}, Трафик: {traffic.total_traffic} МБ")

        # Пример запроса с фильтром по датам


        # Пример запроса с фильтром по ip
        print("\nПолучение трафика с фильтром по ip:")
        response = stub.GetTotalTraffic(traffic_pb2.TrafficRequest(
            ip="192.168.224.118"
        ))

        for traffic in response.traffic_list:
            print(f"Клиент: {traffic.customer_name}, Трафик: {traffic.total_traffic} МБ")

        print("\nПолучение трафика с фильтром по датам:")
        response = stub.GetTotalTraffic(traffic_pb2.TrafficRequest(
            start_date="2022-01-05 10:15:00",
            end_date="2023-03-20 13:00:00"
        ))


        for traffic in response.traffic_list:
            print(f"Клиент: {traffic.customer_name}, Трафик: {traffic.total_traffic} МБ")

if __name__ == "__main__":
    run()
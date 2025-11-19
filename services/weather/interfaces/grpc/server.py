from concurrent import futures

import grpc

from services.weather.interfaces.grpc import health_pb2_grpc
from services.weather.interfaces.grpc.implementations.health_service import (
    HealthServiceImpl,
)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    health_pb2_grpc.add_HealthServiceServicer_to_server(HealthServiceImpl(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC Health Server started on port 50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

import asyncio

import grpc

from services.weather.interfaces.grpc.generated import health_pb2_grpc, weather_pb2_grpc
from services.weather.interfaces.grpc.implementations.health_service import (
    HealthServiceImpl,
)
from services.weather.interfaces.grpc.implementations.weather_service import (
    WeatherServiceImpl,
)

HOST = "0.0.0.0"
PORT = 50052


async def serve():
    server = grpc.aio.server()

    health_pb2_grpc.add_HealthServiceServicer_to_server(HealthServiceImpl(), server)
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherServiceImpl(), server)

    server.add_insecure_port(f"{HOST}:{PORT}")
    await server.start()
    print(f"gRPC listening on {HOST}:{PORT} (Health + Weather)")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())

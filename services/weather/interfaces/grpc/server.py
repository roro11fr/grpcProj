import asyncio

import grpc

from services.weather.core import settings
from services.weather.interfaces.grpc.generated import health_pb2_grpc, weather_pb2_grpc
from services.weather.interfaces.grpc.implementations.health_service import (
    HealthServiceImpl,
)
from services.weather.interfaces.grpc.implementations.weather_service import (
    WeatherServiceImpl,
)


async def serve():
    server = grpc.aio.server()

    health_pb2_grpc.add_HealthServiceServicer_to_server(HealthServiceImpl(), server)
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherServiceImpl(), server)

    server.add_insecure_port(f"{settings.GRPC_HOST}:{settings.GRPC_PORT}")

    print(f"✅ gRPC listening on {settings.GRPC_HOST}:{settings.GRPC_PORT}")
    print("   Services: HealthService, WeatherService (API key protected)")

    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())

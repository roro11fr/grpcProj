from __future__ import annotations

import asyncio
import logging
import sys

import grpc

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from services.weather.core import settings
from services.weather.core.logging_config import setup_logging
from services.weather.interfaces.grpc.generated import health_pb2_grpc, weather_pb2_grpc
from services.weather.interfaces.grpc.implementations.health_service import (
    HealthServiceImpl,
)
from services.weather.interfaces.grpc.implementations.weather_service import (
    WeatherServiceImpl,
)
from services.weather.interfaces.grpc.interceptors.api_key_interceptor import (
    ApiKeyAuthInterceptor,
)

setup_logging()


async def serve():
    server = grpc.aio.server(
        interceptors=[ApiKeyAuthInterceptor()],
        options=[("grpc.max_concurrent_streams", 1024)],
    )

    health_pb2_grpc.add_HealthServiceServicer_to_server(HealthServiceImpl(), server)
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherServiceImpl(), server)

    host = "[::]"
    port = settings.GRPC_PORT
    server.add_insecure_port(f"{host}:{port}")

    masked_key = "set" if (settings.GRPC_API_KEY or "").strip() else "NOT-SET"
    logging.info(f"✅ gRPC listening on {host}:{port} | api_key={masked_key}")
    logging.info(
        "   Services: HealthService, WeatherService (API key protected via interceptor)"
    )

    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())

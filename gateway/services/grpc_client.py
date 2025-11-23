from typing import Optional

import grpc
from grpc.aio import Channel

from gateway.core.settings import get_settings
from services.weather.interfaces.grpc.generated import weather_pb2_grpc  # type: ignore


def build_target() -> str:
    s = get_settings()
    return f"{s.grpc_host}:{s.grpc_port}"


def create_channel() -> Channel:
    return grpc.aio.insecure_channel(build_target())


def create_stub(
    channel: Optional[Channel] = None,
) -> weather_pb2_grpc.WeatherServiceStub:
    ch = channel or create_channel()
    return weather_pb2_grpc.WeatherServiceStub(ch)


def default_metadata() -> Optional[list[tuple[str, str]]]:
    s = get_settings()
    return [("x-api-key", s.grpc_api_key)] if s.grpc_api_key else None

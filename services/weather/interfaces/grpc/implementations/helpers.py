import asyncio
from typing import Tuple

import grpc

from services.weather.interfaces.grpc.generated import weather_pb2


class InvalidArgument(ValueError):
    """Local exception for invalid input mapping to INVALID_ARGUMENT."""

    pass


def validate_city(raw: str | None) -> str:
    city = (raw or "").strip()
    if not city:
        raise InvalidArgument("city is required")
    return city


async def fetch_weather(client, city: str) -> Tuple[str, float, str, int, float]:
    """Delegate to client, kept separate for testability."""
    return await client.get_current_weather(city)


def persist_reading(
    repo, name: str, temp_c: float, description: str, humidity: int, wind_speed: float
) -> None:
    async def _persist():
        try:
            await repo.insert_reading(
                city=name,
                temp_c=temp_c,
                description=description,
                humidity=humidity,
                wind_speed=wind_speed,
            )
        except Exception:
            # Intenționat nu ridicăm — persistența nu blochează RPC-ul.
            # TODO: adaugă logging aici dacă dorești.
            pass

    asyncio.create_task(_persist())


def to_proto(
    name: str, temp_c: float, description: str, humidity: int, wind_speed: float
):
    return weather_pb2.GetCurrentWeatherResponse(
        city=name,
        temp_c=temp_c,
        description=description,
        humidity=humidity,
        wind_speed=wind_speed,
    )


async def abort_by_exception(context, e: Exception) -> None:
    if isinstance(e, InvalidArgument):
        await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
    elif isinstance(e, PermissionError):
        await context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
    elif isinstance(e, LookupError):
        await context.abort(grpc.StatusCode.NOT_FOUND, str(e))
    elif isinstance(e, ConnectionError):
        await context.abort(grpc.StatusCode.UNAVAILABLE, str(e))
    else:
        await context.abort(grpc.StatusCode.INTERNAL, f"Internal error: {e}")

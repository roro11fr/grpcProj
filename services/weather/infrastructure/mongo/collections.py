from __future__ import annotations

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from services.weather.core import settings

from .client import get_mongo_client

__all__ = ["get_weather_collection"]

_weather_collection: Optional[AsyncIOMotorCollection] = None


async def get_weather_collection() -> AsyncIOMotorCollection:
    """Get a singleton MongoDB collection instance for weather data."""
    global _weather_collection
    if _weather_collection is not None:
        return _weather_collection

    client = get_mongo_client()
    db = client[settings.MONGO_DB]
    coll = db[settings.MONGO_COLL]

    await coll.create_index([("city", 1), ("observed_at_unix", -1)])

    _weather_collection = coll
    return _weather_collection

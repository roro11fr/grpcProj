from __future__ import annotations

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from services.weather.core import settings

__all__ = ["get_mongo_client"]

_client: Optional[AsyncIOMotorClient] = None


def get_mongo_client() -> AsyncIOMotorClient:
    """Get a singleton MongoDB client instance."""
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGO_URI)
    return _client

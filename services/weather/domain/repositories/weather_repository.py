from __future__ import annotations

import time
from typing import Dict, List, Optional

from services.weather.infrastructure.mongo.collections import get_weather_collection


class WeatherRepository:
    """Repository for storing and retrieving weather data in MongoDB."""

    async def insert_reading(
        self,
        *,
        city: str,
        temp_c: float,
        description: str,
        humidity: int,
        wind_speed: float,
        observed_at_unix: Optional[int] = None,
        source: str = "openweather",
    ) -> str:
        coll = await get_weather_collection()
        doc = {
            "city": city,
            "temp_c": float(temp_c),
            "description": str(description),
            "humidity": int(humidity),
            "wind_speed": float(wind_speed),
            "observed_at_unix": int(observed_at_unix or time.time()),
            "source": source,
        }
        res = await coll.insert_one(doc)
        return str(res.inserted_id)

    async def find_range(
        self,
        *,
        city: str,
        start_unix: int,
        end_unix: int,
        limit: Optional[int] = None,
    ) -> List[Dict]:
        coll = await get_weather_collection()
        cursor = coll.find(
            {
                "city": city,
                "observed_at_unix": {"$gte": int(start_unix), "$lte": int(end_unix)},
            },
            projection={"_id": 0},
        ).sort("observed_at_unix", -1)
        return await cursor.to_list(length=limit or 0)

    async def find_recent(self, limit: int = 2):
        """
        Returnează ultimele N înregistrări, sortate descrescător după observed_at_unix.
        """
        coll = await get_weather_collection()  # folosește ce ai deja
        cursor = (
            coll.find({}, projection={"_id": 0})
            .sort("observed_at_unix", -1)
            .limit(max(1, int(limit)))
        )
        # pentru Motor: to_list
        return await cursor.to_list(length=limit or 0)

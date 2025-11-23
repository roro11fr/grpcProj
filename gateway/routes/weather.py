from datetime import datetime, timezone
from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from grpc.aio import AioRpcError, Channel
from motor.motor_asyncio import AsyncIOMotorClient

from gateway.core.errors import verify_grpc_error_status
from gateway.core.models import RecentOut, WeatherOut
from gateway.services.db_client import get_collection
from gateway.services.grpc_client import create_stub, default_metadata
from services.weather.interfaces.grpc.generated import weather_pb2

router = APIRouter(prefix="/api", tags=["weather"])


def get_channel(req: Request) -> Channel:
    ch = getattr(req.app.state, "grpc_channel", None)
    if ch is None:
        raise HTTPException(status_code=500, detail="gRPC channel not ready")
    return ch


def get_mongo(req: Request) -> AsyncIOMotorClient:
    cli = getattr(req.app.state, "mongo_client", None)
    if cli is None:
        raise HTTPException(status_code=500, detail="Mongo client not ready")
    return cli


@router.get("/weather", response_model=WeatherOut)
async def get_weather(
    city: str = Query(..., min_length=1),
    channel: Annotated[Channel, Depends(get_channel)] = None,
):
    try:
        stub = create_stub(channel)
        resp = await stub.GetCurrentWeather(
            weather_pb2.GetCurrentWeatherRequest(city=city),
            metadata=default_metadata(),
        )
        return WeatherOut(
            city=resp.city,
            temp_c=resp.temp_c,
            description=resp.description,
            humidity=resp.humidity,
            wind_speed=resp.wind_speed,
        )
    except AioRpcError as e:
        raise HTTPException(
            status_code=verify_grpc_error_status(e), detail=e.details() or str(e)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recent")
async def get_recent(
    limit: int = Query(10, ge=1, le=5000),
    city: str | None = Query(None, min_length=1),
    mongo: Annotated[AsyncIOMotorClient, Depends(get_mongo)] = None,
):
    coll = get_collection(mongo)
    find_filter: Dict = {}
    if city:
        find_filter["city"] = city

    cursor = (
        coll.find(find_filter, projection={"_id": 0})
        .sort("observed_at_unix", -1)
        .limit(limit)
    )
    docs: List[Dict] = await cursor.to_list(length=limit)

    items: list[RecentOut] = []
    for d in reversed(docs):
        unix_ts = int(d.get("observed_at_unix") or 0)
        iso_ts = (
            datetime.fromtimestamp(unix_ts, tz=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
            if unix_ts > 0
            else ""
        )
        items.append(
            RecentOut(
                city=str(d.get("city", "")),
                temp=float(d.get("temp_c", 0.0)),
                description=str(d.get("description", "")),
                humidity=int(d.get("humidity", 0)),
                wind_speed=float(d.get("wind_speed", 0.0)),
                ts=iso_ts,
            )
        )
    return {"items": [i.model_dump() for i in items]}

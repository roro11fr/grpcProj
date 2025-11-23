from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from grpc.aio import Channel
from motor.motor_asyncio import AsyncIOMotorClient

from gateway.core.settings import get_settings
from gateway.routes import weather as weather_routes
from gateway.routes.health import router as health_router
from gateway.routes.weather import router as weather_router
from gateway.services.db_client import create_mongo_client
from gateway.services.grpc_client import create_channel


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.grpc_channel = create_channel()
    app.state.mongo_client = create_mongo_client()
    try:
        yield
    finally:
        await app.state.grpc_channel.close()
        app.state.mongo_client.close()


def create_app() -> FastAPI:
    s = get_settings()
    app = FastAPI(title="Weather Gateway", version="1.2.0", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=s.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def provide_channel() -> Channel:
        return app.state.grpc_channel

    def provide_mongo() -> AsyncIOMotorClient:
        return app.state.mongo_client

    weather_routes._provide_channel = provide_channel
    weather_routes._provide_mongo = provide_mongo

    app.include_router(health_router)
    app.include_router(weather_router)

    return app

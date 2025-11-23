import os
from typing import List


class Settings:
    def __init__(self) -> None:
        # CORS
        self.frontend_origin_raw = os.getenv(
            "FRONTEND_ORIGIN",
            "http://localhost:5173,http://127.0.0.1:5173",
        )
        self.allowed_origins: List[str] = [
            o.strip() for o in self.frontend_origin_raw.split(",") if o.strip()
        ]

        # gRPC target & auth
        self.grpc_host = os.getenv("GRPC_HOST", "weather-grpc")
        self.grpc_port = int(os.getenv("GRPC_PORT", "50052"))
        self.grpc_api_key = os.getenv("GRPC_API_KEY", "")

        # Mongo
        self.mongo_url = os.getenv("MONGO_URL", "mongodb://mongo:27017")
        self.mongo_db = os.getenv("MONGO_DB", "weather_db")
        self.mongo_coll = os.getenv("MONGO_COLL", "weather_readings")

        # HTTP
        self.http_port = int(os.getenv("PORT", "8080"))


_settings = Settings()


def get_settings() -> Settings:
    return _settings

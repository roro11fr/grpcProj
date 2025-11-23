from __future__ import annotations

from services.weather.core.logging_config import get_logger
from services.weather.interfaces.grpc.generated import health_pb2, health_pb2_grpc

log = get_logger("weather.health")


class HealthServiceImpl(health_pb2_grpc.HealthServiceServicer):
    async def HealthCheck(self, request, context):
        log.info("[HEALTH] HealthCheck START")
        resp = health_pb2.HealthCheckResponse(status="SERVING")
        log.info("[HEALTH] HealthCheck END -> %s", resp.status)
        return resp

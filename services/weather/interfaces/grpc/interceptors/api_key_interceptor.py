import logging

import grpc

from services.weather.core import settings

from .utils import metadata_to_dict

log = logging.getLogger("weather.interceptor")
HEALTH_FQN = "/weather.health.v1.HealthService/HealthCheck"


class ApiKeyAuthInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method

        if method == HEALTH_FQN:
            log.info(f"[INTERCEPTOR] method={method} → ALLOW (health)")
            return await continuation(handler_call_details)

        expected = (
            getattr(settings, "GRPC_API_KEY", "")
            or getattr(settings, "grpc_api_key", "")
            or ""
        ).strip()
        supplied = (
            metadata_to_dict(handler_call_details.invocation_metadata).get(
                "x-api-key", ""
            )
            or ""
        ).strip()

        if not expected:
            log.warning(f"[INTERCEPTOR] method={method} → DENY (no key configured)")
            return _deny_handler("Server missing GRPC_API_KEY")

        if supplied != expected:
            log.warning(f"[INTERCEPTOR] method={method} → DENY (invalid key)")
            return _deny_handler("Invalid x-api-key")

        log.info(f"[INTERCEPTOR] method={method} → OK (authorized)")
        return await continuation(handler_call_details)


def _deny_handler(message: str):
    def deny(request, context):
        context.abort(grpc.StatusCode.UNAUTHENTICATED, message)

    return grpc.unary_unary_rpc_method_handler(deny)

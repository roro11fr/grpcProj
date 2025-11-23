import grpc

from services.weather.core import settings

from .utils import is_authorized, metadata_to_dict, wrap_with_denied


class ApiKeyAuthInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        md = metadata_to_dict(handler_call_details.invocation_metadata)
        supplied = md.get("x-api-key")
        expected = getattr(settings, "GRPC_API_KEY", None)

        if is_authorized(supplied, expected):
            return await continuation(handler_call_details)

        original = await continuation(handler_call_details)
        if original is None:
            return None
        return wrap_with_denied(original)

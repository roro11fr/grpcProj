import grpc


class ApiKeyAuthInterceptor(grpc.aio.ServerInterceptor):

    async def intercept_service(self, continuation, handler_call_details):
        md = dict(handler_call_details.invocation_metadata or [])
        supplied = md.get("x-api-key")

        from services.weather.core import settings

        if not settings.GRPC_API_KEY or supplied == settings.GRPC_API_KEY:
            return await continuation(handler_call_details)

        async def deny_unary_unary(request, context):
            await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid x-api-key")

        async def deny_unary_stream(request, context):
            await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid x-api-key")
            if False:
                yield

        async def deny_stream_unary(request_iter, context):
            await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid x-api-key")

        async def deny_stream_stream(request_iter, context):
            await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid x-api-key")
            if False:
                yield

        return grpc.aio.rpc_method_handler(
            unary_unary=deny_unary_unary,
            unary_stream=deny_unary_stream,
            stream_unary=deny_stream_unary,
            stream_stream=deny_stream_stream,
        )

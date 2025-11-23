import grpc


def metadata_to_dict(metadata) -> dict[str, str]:
    return dict(metadata or [])


def is_authorized(supplied: str | None, expected: str | None) -> bool:
    if not expected:
        return True
    return supplied == expected


def wrap_with_denied(original):
    async def _abort_unauthed(context):
        await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid x-api-key")

    if original.unary_unary:

        async def deny_unary_unary(request, context):
            await _abort_unauthed(context)

        return grpc.aio.unary_unary_rpc_method_handler(
            deny_unary_unary,
            request_deserializer=original.request_deserializer,
            response_serializer=original.response_serializer,
        )

    if original.unary_stream:

        async def deny_unary_stream(request, context):
            await _abort_unauthed(context)
            if False:
                yield

        return grpc.aio.unary_stream_rpc_method_handler(
            deny_unary_stream,
            request_deserializer=original.request_deserializer,
            response_serializer=original.response_serializer,
        )

    if original.stream_unary:

        async def deny_stream_unary(request_iter, context):
            await _abort_unauthed(context)

        return grpc.aio.stream_unary_rpc_method_handler(
            deny_stream_unary,
            request_deserializer=original.request_deserializer,
            response_serializer=original.response_serializer,
        )

    if original.stream_stream:

        async def deny_stream_stream(request_iter, context):
            await _abort_unauthed(context)
            if False:
                yield

        return grpc.aio.stream_stream_rpc_method_handler(
            deny_stream_stream,
            request_deserializer=original.request_deserializer,
            response_serializer=original.response_serializer,
        )

    return original

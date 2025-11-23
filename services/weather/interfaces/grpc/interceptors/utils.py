import grpc


def metadata_to_dict(metadata) -> dict[str, str]:
    return dict(metadata or [])


def is_authorized(supplied: str | None, expected: str | None) -> bool:
    supplied = (supplied or "").strip()
    expected = (expected or "").strip()
    return bool(expected) and supplied == expected


def deny_handler(message: str):
    def deny(request, context):
        context.abort(grpc.StatusCode.UNAUTHENTICATED, message)

    return grpc.unary_unary_rpc_method_handler(deny)

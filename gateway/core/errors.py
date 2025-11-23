from grpc import StatusCode
from grpc.aio import AioRpcError

GRPC_TO_HTTP_STATUS_MAP = {
    StatusCode.INVALID_ARGUMENT: 400,
    StatusCode.NOT_FOUND: 404,
    StatusCode.PERMISSION_DENIED: 403,
    StatusCode.UNAUTHENTICATED: 401,
    StatusCode.ALREADY_EXISTS: 409,
    StatusCode.FAILED_PRECONDITION: 412,
    StatusCode.RESOURCE_EXHAUSTED: 429,
    StatusCode.UNAVAILABLE: 503,
    StatusCode.DEADLINE_EXCEEDED: 504,
    StatusCode.UNIMPLEMENTED: 501,
    StatusCode.UNKNOWN: 502,
    StatusCode.INTERNAL: 502,
    StatusCode.CANCELLED: 499,
    StatusCode.ABORTED: 409,
    StatusCode.OUT_OF_RANGE: 400,
    StatusCode.DATA_LOSS: 500,
}


def verify_grpc_error_status(error: AioRpcError) -> int:
    """
    Translates a gRPC AioRpcError to the corresponding HTTP status code.
    Returns 502 (Bad Gateway) if the error code is not recognized.
    """
    return GRPC_TO_HTTP_STATUS_MAP.get(error.code(), 502)

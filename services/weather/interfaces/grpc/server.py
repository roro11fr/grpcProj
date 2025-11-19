import asyncio

import grpc

from services.weather.interfaces.grpc import health_pb2, health_pb2_grpc


class HealthServiceImpl(health_pb2_grpc.HealthServiceServicer):
    async def HealthCheck(self, request, context):
        print(f"Received request: {request}")
        return health_pb2.HealthCheckResponse(status="SERVING")


async def serve(host: str = "0.0.0.0", port: int = 50051):
    server = grpc.aio.server(options=[("grpc.so_reuseport", 0)])
    health_pb2_grpc.add_HealthServiceServicer_to_server(HealthServiceImpl(), server)
    server.add_insecure_port(f"{host}:{port}")
    await server.start()
    print(f"[gRPC] Health server started on {host}:{port}")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())

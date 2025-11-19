import asyncio

import grpc

from services.weather.interfaces.grpc.generated import health_pb2, health_pb2_grpc


async def main(target: str = "localhost:50051"):
    async with grpc.aio.insecure_channel(target) as channel:
        stub = health_pb2_grpc.HealthServiceStub(channel)
        resp = await stub.HealthCheck(health_pb2.HealthCheckRequest())
        print(resp.status)


if __name__ == "__main__":
    asyncio.run(main())

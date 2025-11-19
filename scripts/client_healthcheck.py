import asyncio

import grpc

from services.weather.interfaces.grpc.generated import health_pb2, health_pb2_grpc


async def main():
    async with grpc.aio.insecure_channel("localhost:50052") as ch:
        stub = health_pb2_grpc.HealthServiceStub(ch)
        resp = await stub.HealthCheck(health_pb2.HealthCheckRequest())
        print(resp.status)


if __name__ == "__main__":
    asyncio.run(main())

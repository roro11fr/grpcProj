import asyncio

import grpc

from services.weather.interfaces.grpc.generated import weather_pb2, weather_pb2_grpc


async def main():
    async with grpc.aio.insecure_channel("localhost:50052") as ch:
        stub = weather_pb2_grpc.WeatherServiceStub(ch)
        resp = await stub.GetCurrentWeather(
            weather_pb2.GetCurrentWeatherRequest(city="Suceava")
        )
        print(resp.city, resp.temp_c, resp.description)


if __name__ == "__main__":
    asyncio.run(main())

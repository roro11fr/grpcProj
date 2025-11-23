import asyncio
import os
import sys
import time

import grpc
from dotenv import load_dotenv

from services.weather.interfaces.grpc.generated import weather_pb2, weather_pb2_grpc

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

API_KEY = "-"
CITIES = ["Iasi", "Cluj", "Suceava", "Timisoara", "Oradea"]
TARGET = f"localhost:{os.getenv('GRPC_PORT', '50052')}"
REQUEST = weather_pb2.GetCurrentWeatherRequest


async def call_city(stub, city):
    req = REQUEST(city=city)
    t0 = time.time()
    resp = await stub.GetCurrentWeather(req, metadata=(("x-api-key", API_KEY),))
    return city, time.time() - t0, resp.temp_c


async def main():
    async with grpc.aio.insecure_channel(TARGET) as channel:
        await asyncio.wait_for(channel.channel_ready(), timeout=5)
        stub = weather_pb2_grpc.WeatherServiceStub(channel)
        results = await asyncio.gather(*(call_city(stub, c) for c in CITIES))
        for city, dur, temp in results:
            print(f"{city:10s} took {dur:.2f} s  temp={temp}")
    print(f"API_KEY used: {API_KEY}")


if __name__ == "__main__":
    asyncio.run(main())

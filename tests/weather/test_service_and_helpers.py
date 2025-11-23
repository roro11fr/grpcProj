import grpc
import pytest

from services.weather.interfaces.grpc.generated import weather_pb2
from services.weather.interfaces.grpc.implementations.helpers import (
    InvalidArgument,
    abort_by_exception,
    to_proto,
    validate_city,
)
from services.weather.interfaces.grpc.implementations.weather_service import (
    WeatherServiceImpl,
)

pytestmark = pytest.mark.unit


class DummyClient:
    async def get_current_weather(self, city: str):
        return ("London", 12.3, "clear sky", 45, 3.2)


class DummyRepo:
    def __init__(self):
        self.saved = []

    def insert_reading(self, city, temp_c, description, humidity, wind_speed):
        self.saved.append((city, temp_c, description, humidity, wind_speed))


class DummyContext:
    def __init__(self):
        self.aborted = None

    async def abort(self, code, details):
        self.aborted = (code, details)
        raise RuntimeError("aborted")


@pytest.mark.asyncio
async def test_weather_service_happy_path():
    svc = WeatherServiceImpl(client=DummyClient(), repo=DummyRepo())
    req = weather_pb2.GetCurrentWeatherRequest(city="London")
    resp = await svc.GetCurrentWeather(req, DummyContext())
    assert resp.city == "London"
    assert resp.temp_c == pytest.approx(12.3)
    assert resp.description == "clear sky"
    assert resp.humidity == 45
    assert resp.wind_speed == pytest.approx(3.2)


@pytest.mark.asyncio
async def test_weather_service_invalid_city_aborts():
    svc = WeatherServiceImpl(client=DummyClient(), repo=DummyRepo())
    req = weather_pb2.GetCurrentWeatherRequest(city="")
    with pytest.raises(RuntimeError):
        await svc.GetCurrentWeather(req, DummyContext())


def test_validate_city_ok():
    assert validate_city("  Suceava  ") == "Suceava"


def test_validate_city_raises_on_blank():
    with pytest.raises(InvalidArgument):
        validate_city("   ")


def test_to_proto_maps_fields():
    msg = to_proto("Cluj", 10.0, "Cloudy", 80, 5.0)
    assert isinstance(msg, weather_pb2.GetCurrentWeatherResponse)
    assert msg.city == "Cluj"
    assert msg.temp_c == pytest.approx(10.0)
    assert msg.description == "Cloudy"
    assert msg.humidity == 80
    assert msg.wind_speed == pytest.approx(5.0)


@pytest.mark.asyncio
async def test_abort_by_exception_mappings():
    for exc, code in [
        (InvalidArgument("bad"), grpc.StatusCode.INVALID_ARGUMENT),
        (PermissionError("nope"), grpc.StatusCode.PERMISSION_DENIED),
        (LookupError("missing"), grpc.StatusCode.NOT_FOUND),
        (ConnectionError("net"), grpc.StatusCode.UNAVAILABLE),
        (RuntimeError("whoops"), grpc.StatusCode.INTERNAL),
    ]:
        c = DummyContext()
        with pytest.raises(RuntimeError):
            await abort_by_exception(c, exc)
        assert c.aborted[0] == code

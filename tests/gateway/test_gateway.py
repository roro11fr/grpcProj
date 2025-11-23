# tests/gateway/test_gateway.py
import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


def make_test_app(monkeypatch):
    from gateway.application.app import create_app

    app = create_app()

    app.router.lifespan_context = None

    import gateway.routes.weather as weather_routes

    class FakeResp:
        def __init__(self):
            self.city = "London"
            self.temp_c = 20.0
            self.description = "clear sky"
            self.humidity = 50
            self.wind_speed = 4.0

    class FakeStub:
        async def GetCurrentWeather(self, request, metadata=None):
            return FakeResp()

    monkeypatch.setattr(
        weather_routes, "get_channel", lambda request=None: object(), raising=True
    )
    monkeypatch.setattr(
        weather_routes, "get_mongo", lambda request=None: None, raising=True
    )
    monkeypatch.setattr(
        weather_routes, "create_stub", lambda ch: FakeStub(), raising=True
    )

    return app


def test_health_endpoint():
    from gateway.application.app import create_app

    app = create_app()
    app.router.lifespan_context = None
    client = TestClient(app)
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_weather_endpoint_with_stub(monkeypatch):
    app = make_test_app(monkeypatch)
    client = TestClient(app)
    r = client.get("/api/weather", params={"city": "London"})
    assert r.status_code == 200
    body = r.json()
    assert body["city"] == "London"
    assert "temp_c" in body and "humidity" in body and "description" in body


def test_weather_endpoint_422_for_missing_city(monkeypatch):
    app = make_test_app(monkeypatch)
    client = TestClient(app)
    r = client.get("/api/weather")
    assert r.status_code in (400, 422)

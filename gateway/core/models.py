from pydantic import BaseModel


class WeatherOut(BaseModel):
    city: str
    temp_c: float
    description: str
    humidity: int
    wind_speed: float


class RecentOut(BaseModel):
    city: str
    temp: float
    description: str
    humidity: int
    wind_speed: float
    ts: str

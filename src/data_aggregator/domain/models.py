from abc import ABC

from pydantic import BaseModel


class ResponseModel(ABC):
    pass


class RawWeatherResponse(BaseModel, ResponseModel):
    coordinates: tuple[float, float]
    timezone_b: bytes
    time: int
    temperature_2m: float
    relative_humidity_2m: float
    is_day: float
    rain: float

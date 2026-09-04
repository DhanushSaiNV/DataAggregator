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


class CountryModel(BaseModel):
    official_name: str
    capitals: list[str]
    region: str
    subregion: str
    currencies: list[str]
    languages: list[str]

    
class RawCountriesResponse(BaseModel, ResponseModel):
    countries: list[CountryModel]
    count: int
    
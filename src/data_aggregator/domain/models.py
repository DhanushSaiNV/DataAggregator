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


class MarketDataModel(BaseModel):
    current_price: dict[str, int | float]
    high_24h: dict[str, int | float]
    low_24h: dict[str, int | float]
    price_change_24h: float
    price_change_percentage_24h: float
    price_change_percentage_7d: float
    price_change_percentage_30d: float
    price_change_percentage_200d: float
    price_change_percentage_1y: float


class RawCoinResponse(BaseModel, ResponseModel):
    id: str
    symbol: str
    name: str
    categories: list[str]
    # description: dict[str, str]
    # genesis_date: str
    market_data: MarketDataModel
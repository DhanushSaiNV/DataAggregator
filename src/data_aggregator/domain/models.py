
from abc import ABC
from datetime import datetime, timezone
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# ResponseModel
# ├── ValidatedResponseModel
# │   ├── ValidatedWeatherResponse
# │   ├── ValidatedCountriesResponse
# │   └── ValidatedCoinResponse
# │
# ├── CleanedResponseModel
# ├── TransformedResponseModel
# ├── RawWeatherResponse
# ├── RawCountriesResponse
# └── RawCoinResponse

class ResponseModel(BaseModel, ABC):
    pass

class ValidatedResponseModel(ResponseModel):
    pass

class CleanedResponseModel(ResponseModel):
    pass

class TransformedResponseModel(ResponseModel):
    pass


class RawWeatherResponse(ResponseModel):
    coordinates: tuple[float, float]
    timezone_b: bytes
    time: int
    temperature_2m: float
    relative_humidity_2m: float
    is_day: float
    rain: float


class ValidatedWeatherResponse(ValidatedResponseModel):
    latitude: Annotated[float, Field(ge=-90.0, le=90.0)]
    longitude: Annotated[float, Field(ge=-180.0, le=180.0)]
    timezone_b: Annotated[str, Field(min_length=1)]
    time: datetime
    temperature_2m: Annotated[float, Field(ge=-100.0, le=100.0)]
    relative_humidity_2m: Annotated[int, Field(ge=0, le=100)]
    is_day: bool
    rain: Annotated[float, Field(ge=0.0)]

    @model_validator(mode="before")
    @classmethod
    def unpack_coordinates(cls, data):
        # Handle RawWeatherResponse or dict input
        if isinstance(data, RawWeatherResponse):
            data = data.model_dump()
        if "coordinates" in data:
            lat, lon = data.pop("coordinates")
            data.setdefault("latitude", lat)
            data.setdefault("longitude", lon)
        return data

    @field_validator("timezone_b", mode="before")
    @classmethod
    def decode_timezone(cls, v):
        if isinstance(v, bytes):
            return v.decode("utf-8")
        return v

    @field_validator("time", mode="before")
    @classmethod
    def parse_unix_time(cls, v):
        if isinstance(v, (int, float)):
            return datetime.fromtimestamp(v, tz=timezone.utc)
        return v

    @field_validator("relative_humidity_2m", mode="before")
    @classmethod
    def coerce_humidity(cls, v):
        # Round the float to nearest int; reject clearly out-of-range early
        if isinstance(v, float):
            if v < 0 or v > 100:
                raise ValueError(f"relative_humidity_2m out of range: {v}")
            return round(v)
        return v

    @field_validator("is_day", mode="before")
    @classmethod
    def coerce_is_day(cls, v):
        if isinstance(v, (int, float)):
            if v not in (0, 1, 0.0, 1.0):
                raise ValueError(f"is_day must be 0 or 1, got {v}")
            return bool(int(v))
        return v

    @field_validator("rain", mode="before")
    @classmethod
    def validate_rain(cls, v):
        if isinstance(v, (int, float)) and v < 0:
            raise ValueError(f"rain cannot be negative: {v}")
        return v


class CountryModel(BaseModel):
    official_name: str
    capitals: list[str]
    region: str
    subregion: str
    currencies: list[str]
    languages: list[str]

    
class RawCountriesResponse(ResponseModel):
    countries: list[CountryModel]
    count: int


class ValidatedCountryModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    official_name: Annotated[str, Field(min_length=1)]
    capitals: Annotated[list[Annotated[str, Field(min_length=1)]], Field(min_length=1)]
    region: Annotated[str, Field(min_length=1)]
    subregion: Annotated[str, Field(min_length=1)]
    currencies: Annotated[list[Annotated[str, Field(min_length=1)]], Field(min_length=1)]
    languages: Annotated[list[Annotated[str, Field(min_length=1)]], Field(min_length=1)]

    @field_validator("official_name", "region", "subregion", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("capitals", "currencies", "languages")
    @classmethod
    def ensure_unique(cls, v: list[str]) -> list[str]:
        if len(v) != len(set(v)):
            raise ValueError("list items must be unique")
        return v


class ValidatedCountriesResponse(ValidatedResponseModel):
    model_config = ConfigDict(from_attributes=True)

    countries: list[ValidatedCountryModel]
    count: Annotated[int, Field(ge=0)]

    @model_validator(mode="after")
    def check_count(self):
        if self.count != len(self.countries):
            raise ValueError(
                f"count ({self.count}) does not match number of countries "
                f"({len(self.countries)})"
            )
        return self

    @field_validator("countries")
    @classmethod
    def ensure_unique_countries(
        cls, v: list[ValidatedCountryModel]
    ) -> list[ValidatedCountryModel]:
        names = [c.official_name for c in v]
        if len(names) != len(set(names)):
            raise ValueError("duplicate country official_name found")
        return v

    
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


class RawCoinResponse(ResponseModel):
    id: str
    symbol: str
    name: str
    categories: list[str]
    # description: dict[str, str]
    # genesis_date: str
    market_data: MarketDataModel


# ISO 4217-style currency key: 3 lowercase letters (e.g. "usd", "eur", "btc")
CurrencyCode = Annotated[str, Field(pattern=r"^[a-z]{3}$")]
Price = Annotated[float, Field(ge=0.0)]
Percentage = Annotated[float, Field(ge=-100.0, le=100000.0)]


class ValidatedMarketDataModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    current_price: dict[CurrencyCode, Price]
    high_24h: dict[CurrencyCode, Price]
    low_24h: dict[CurrencyCode, Price]

    price_change_24h: float
    price_change_percentage_24h: Percentage
    price_change_percentage_7d: Percentage
    price_change_percentage_30d: Percentage
    price_change_percentage_200d: Percentage
    price_change_percentage_1y: Percentage

    @field_validator(
        "current_price", "high_24h", "low_24h",
        mode="before",
    )
    @classmethod
    def normalize_price_map(cls, v):
        if not isinstance(v, dict):
            return v
        return {str(k).lower(): val for k, val in v.items()}

    @model_validator(mode="after")
    def check_price_maps_consistent(self):
        keys = set(self.current_price)
        for name in ("high_24h", "low_24h"):
            other = getattr(self, name)
            if set(other) != keys:
                missing = keys ^ set(other)
                raise ValueError(
                    f"{name} currencies {missing} do not match current_price"
                )
        return self

    @model_validator(mode="after")
    def check_high_low_bounds(self):
        for currency, current in self.current_price.items():
            high = self.high_24h[currency]
            low = self.low_24h[currency]
            if low > high:
                raise ValueError(
                    f"{currency}: low_24h ({low}) > high_24h ({high})"
                )
            if not (low <= current <= high):
                raise ValueError(
                    f"{currency}: current_price ({current}) not within "
                    f"[low_24h={low}, high_24h={high}]"
                )
        return self


class ValidatedCoinResponse(ValidatedResponseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[str, Field(min_length=1)]
    symbol: Annotated[str, Field(min_length=1, pattern=r"^[a-z0-9]+$")]
    name: Annotated[str, Field(min_length=1)]
    categories: list[Annotated[str, Field(min_length=1)]]
    market_data: ValidatedMarketDataModel

    @field_validator("id", "name", mode="before")
    @classmethod
    def strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("symbol", mode="before")
    @classmethod
    def normalize_symbol(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @field_validator("categories")
    @classmethod
    def dedupe_categories(cls, v: list[str]) -> list[str]:
        # preserve order, drop duplicates
        seen: set[str] = set()
        result: list[str] = []
        for c in v:
            c = c.strip()
            if c and c not in seen:
                seen.add(c)
                result.append(c)
        return result
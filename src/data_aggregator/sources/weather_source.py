from typing import Self

import openmeteo_requests
from pydantic import ValidationError

from data_aggregator.domain.exceptions import *
from data_aggregator.domain.models import RawWeatherResponse
from data_aggregator.sources.data_source import DataSource

BASE_URL = "https://api.open-meteo.com/v1/forecast"

DEFAULT_PARAMS = {
    "latitude": 16.2997,
    "longitude": 80.4573,
    "daily": ["sunrise", "sunset"],
    "current": ["temperature_2m", "relative_humidity_2m", "is_day", "rain"],
    "timezone": "auto",
}


class WeatherSource(DataSource):
    def __init__(
        self, base_url: str = BASE_URL, endpoints: list[str] | None = None
    ) -> None:
        super().__init__(base_url, endpoints)
        self.openmeteo = openmeteo_requests.Client()


    def fetch(self, endpoint: str | None = None, *kwargs) -> Self:
        """Fetches the data and returns raw response dict"""
        response = self.openmeteo.weather_api(BASE_URL, DEFAULT_PARAMS)[0]

        current = response.Current()

        response_dict: dict = {
            "coordinates": (response.Latitude(), response.Longitude()),
            "timezone_b": response.Timezone(),
            "time": current.Time(),
            "temperature_2m": current.Variables(0).Value(),
            "relative_humsidity_2m": current.Variables(1).Value(),
            "is_day": current.Variables(2).Value(),
            "rain": current.Variables(3).Value(),
        }

        self.response_dict: dict = response_dict

        return self


    def parse(self, response_dict: dict | None = None) -> RawWeatherResponse:
        """Parses raw response dict and returns RawWeatherResponse"""
        try:
            response: RawWeatherResponse = RawWeatherResponse.model_validate(
                response_dict if response_dict else self.response_dict
            )

            return response

        except ValidationError as e:
            raise ResponseValidationError(
                self.response_dict, RawWeatherResponse, e
            ) from e

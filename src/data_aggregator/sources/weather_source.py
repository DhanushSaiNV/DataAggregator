from typing import Self

import openmeteo_requests

from data_aggregator.domain.decorators import parser
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

    response_model = RawWeatherResponse

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
            "relative_humidity_2m": current.Variables(1).Value(),
            "is_day": current.Variables(2).Value(),
            "rain": current.Variables(3).Value(),
        }

        self.response_dict: dict = response_dict

        return self

    @parser
    def parse(self, response_dict: dict | None = None) -> RawWeatherResponse:
        """Parses raw response dict and returns RawWeatherResponse"""
        response: RawWeatherResponse = RawWeatherResponse.model_validate(
            response_dict if response_dict else self.response_dict
        )

        return response


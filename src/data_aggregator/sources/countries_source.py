import os
from typing import Self

import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout
from pydantic import ValidationError

from data_aggregator.domain import RawCountriesResponse, ResponseModel
from data_aggregator.domain.exceptions import *
from data_aggregator.sources.data_source import DataSource

load_dotenv(r"C:\Users\dhanu\Documents\codes\Career\PythonMastery\DataAggregator\.env")

API_KEY = os.getenv("REST_COUNTRIES_API_KEY")

BASE_URL = "https://api.restcountries.com/countries/v5"


class CountriesSource(DataSource):
    def __init__(
        self, base_url: str = BASE_URL, endpoints: list[str] | None = None
    ) -> None:
        super().__init__(base_url, endpoints)
        self.header = {"Authorization": f"Bearer {API_KEY}"}

    def fetch(self, endpoint: str, *kwargs) -> Self:
        """Fetches the data and returns raw response Self"""
        try:
            response = requests.get(BASE_URL + endpoint, headers=self.header)

            res_dict = response.json()

            countries = []

            for country in res_dict["data"]["objects"]:
                countries.append(
                    {
                        "official_name": country["names"]["official"],
                        "capitals": [capital["name"] for capital in country["capitals"]],
                        "region": country["region"],
                        "subregion": country["subregion"],
                        "currencies": [
                            currency["name"] for currency in country["currencies"]
                        ],
                        "languages": [
                            language["name"] for language in country["languages"]
                        ],
                    }
                )

            self.response_dict = {"countries": countries, "count": len(countries)}

            return self

        except (Timeout, ConnectionError, HTTPError, RequestException) as e:
            raise DataFetchError(f"Fetching failed in {self.__class__}") from e

    def parse(self, response_dict: dict | None=None) -> RawCountriesResponse:
        """parses raw response dict and resturn RawCountriesResponseModel"""

        try:
            response = RawCountriesResponse.model_validate(
                response_dict if response_dict else self.response_dict
            )

            return response
        except ValidationError as e:
            raise ResponseValidationError(
                self.response_dict, RawCountriesResponse, e
            ) from e
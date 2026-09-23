import os
from typing import Self

import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from data_aggregator.domain import RawCountriesResponse, ValidatedCountriesResponse
from data_aggregator.domain.decorators import parser
from data_aggregator.domain.exceptions import *

from .data_source import DataSource

load_dotenv(r"C:\Users\dhanu\Documents\codes\Career\PythonMastery\DataAggregator\.env")

API_KEY = os.getenv("REST_COUNTRIES_API_KEY")

if not API_KEY:
    raise APIKeyError("REST COUNTRIES API KEY NOT FOUND.")


BASE_URL = "https://api.restcountries.com/countries/v5"


class CountriesSource(DataSource):
    response_model = RawCountriesResponse
    validated_model = ValidatedCountriesResponse
    
    def __init__(
        self
    ) -> None:
        self.header = {"Authorization": f"Bearer {API_KEY}"}
        

    def fetch(self, endpoint: str = "?q=indi&pretty=1", *kwargs) -> Self:
        """Fetches the data and returns raw response Self"""
        try:
            response = requests.get(BASE_URL + endpoint, headers=self.header)

            res_dict = response.json()

            countries = []

            for country in res_dict["data"]["objects"]:
                countries.append(
                    {
                        "official_name": country["names"]["official"],
                        "capitals": [
                            capital["name"] for capital in country["capitals"]
                        ],
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

    @parser
    def parse(self, response_dict: dict | None = None) -> RawCountriesResponse:
        """parses raw response dict and resturn RawCountriesResponseModel"""

        response = RawCountriesResponse.model_validate(
            response_dict if response_dict is not None else self.response_dict
        )

        self.response = response

        return response

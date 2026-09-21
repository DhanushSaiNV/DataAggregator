import os
from typing import Self

from coingecko_sdk import Coingecko
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from data_aggregator.domain import RawCoinResponse
from data_aggregator.domain.decorators import parser
from data_aggregator.domain.exceptions import *
from data_aggregator.shared.key_parser import parse_keys

from .data_source import DataSource

load_dotenv(r"C:\Users\dhanu\Documents\codes\Career\PythonMastery\DataAggregator\.env")

API_KEY = os.getenv("COINGECKO_API_KEY")

__all__ = [
    "CoinSource"
]

class CoinSource(DataSource):

    response_model = RawCoinResponse

    def __init__(self, base_url: str = "", endpoints: list[str] | None = None) -> None:
        super().__init__(base_url, endpoints)

        self.client = Coingecko(demo_api_key=API_KEY, environment="demo")

    def fetch(self, endpoint: str, *kwargs) -> Self:
        """Fetches the data and returns raw response Self"""
        try:
            response = self.client.coins.get_id(endpoint).model_dump()

            coin_response_dict = parse_keys(
                response,
                ["id", "symbol", "name", "categories"],
            )

            market_dict = parse_keys(
                response,
                [
                    "current_price",
                    "high_24h",
                    "low_24h",
                    "price_change_24h",
                    "price_change_percentage_24h",
                    "price_change_percentage_7d",
                    "price_change_percentage_30d",
                    "price_change_percentage_200d",
                    "price_change_percentage_1y",
                ],
            )

            coin_response_dict["market_data"] = market_dict

            self.response_dict = coin_response_dict

            return self

        except (Timeout, ConnectionError, HTTPError, RequestException) as e:
            raise DataFetchError(f"Fetching failed in {self.__class__}") from e

    @parser
    def parse(self, response_dict: dict | None = None) -> RawCoinResponse:
        """parses raw response dict and resturn RawCoinResponseModel"""

        response = RawCoinResponse.model_validate(
            response_dict if response_dict is not None else self.response_dict
        )

        return response

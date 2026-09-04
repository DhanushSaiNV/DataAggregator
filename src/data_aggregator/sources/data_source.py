from abc import ABC, abstractmethod
from typing import Any, Self

from data_aggregator.domain import ResponseModel


class DataSource(ABC):
    def __init__(
        self, base_url: str, endpoints: list[str] | None
    ) -> None:
        self.base_url = base_url
        self.endpoints = endpoints


    @abstractmethod
    def fetch(self, endpoint: str, *kwargs) -> Self | Any:
        """Fetches the data and returns RawWeatherResponse"""
        

    @abstractmethod
    def parse(self, response_dict: dict | None) -> ResponseModel:
        pass

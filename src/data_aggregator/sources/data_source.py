from abc import ABC, abstractmethod
from typing import Self

from data_aggregator.domain import ResponseModel
from data_aggregator.sources.weather_source import RawWeatherResponse


class DataSource(ABC):
    def __init__(
        self, base_url: str, endpoints: list[str]
    ) -> None:
        self.base_url = base_url
        self.endpoints = endpoints


    @abstractmethod
    def fetch(self, endpoint: str, *kwargs) -> dict | Self:
        """Fetches the data and returns RawWeatherResponse"""
        

    @abstractmethod
    def parse(self, response_dict: dict | None) -> ResponseModel:
        pass

from abc import ABC, abstractmethod
from typing import Any, Self

from data_aggregator.domain import ResponseModel, ValidatedResponseModel


class DataSource(ABC):
    response_model: type[ResponseModel]
    validated_model: type[ValidatedResponseModel]
    
    def __init__(
        self
    ) -> None:
        pass

    @abstractmethod
    def fetch(self, endpoint: str = "", *kwargs) -> Self | Any:
        """Fetches the data and returns RawWeatherResponse"""
        

    @abstractmethod
    def parse(self, response_dict: dict | None = None) -> ResponseModel:
        pass

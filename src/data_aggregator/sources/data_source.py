from abc import ABC, abstractmethod

from data_aggregator.domain.models import ResponseModel


class DataSource(ABC):
    def __init__(
        self, base_url: str, endpoints: list[str], res_model: ResponseModel
    ) -> None:
        self.base_url = base_url
        self.endpoints = endpoints
        self.res_model = res_model

    @abstractmethod
    def fetch(self, endpoint: str, *kwargs) -> ResponseModel:
        pass

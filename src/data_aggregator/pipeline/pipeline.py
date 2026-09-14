from data_aggregator.domain.models import (
    ResponseModel,
    ValidatedCoinResponse,
    ValidatedCountriesResponse,
    ValidatedResponseModel,
    ValidatedWeatherResponse,
)


class Pipeline:
    def __init__(self, responses) -> None:
        self.responses: list[ResponseModel] = responses

    def run(self, response, source, model):
        ...
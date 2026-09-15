from enum import Enum, auto

from pydantic import ValidationError

from data_aggregator.domain.exceptions import (
    InvalidPipelineStageError,
    ValidationPipelineError,
)
from data_aggregator.domain.models import (
    ResponseModel,
    TransformedResponseModel,
    ValidatedCoinResponse,
    ValidatedCountriesResponse,
    ValidatedResponseModel,
    ValidatedWeatherResponse,
)
from data_aggregator.pipeline.transformers import (
    transform_coins,
    transform_countries,
    transform_weather,
)
from data_aggregator.sources.data_source import DataSource
from data_aggregator.sources.weather_source import WeatherSource
from data_aggregator.sources.coin_source import CoinSource
from data_aggregator.sources.countries_source import CountriesSource


class PipelineStage(Enum):
    VALIDATE = auto()
    CLEAN = auto()
    TRANSFORM = auto()


TRANSFORMERS = {
    WeatherSource : transform_weather,
    CoinSource : transform_coins,
    CountriesSource : transform_countries
}

    
class Pipeline:
    def __init__(self, *stages: PipelineStage) -> None:
        for stage in stages:
            if not isinstance(stage, PipelineStage):
                raise InvalidPipelineStageError(f"Invalid Pipeline Stage: {stage} must be one of valid pipeline stages.")

        self.stages = stages

        self.STEP_REGISTRY = {
            PipelineStage.VALIDATE: self.validate,
            PipelineStage.TRANSFORM: self.transform
        }


    def validate(
            self,
            response: ResponseModel,
            model: type[ValidatedResponseModel]
    ) -> ValidatedResponseModel:
        """Validates ResponseModel(s) and returns ValidatedResponseModel(s)"""
        try:
            return model.model_validate(response)

        except ValidationError as err:
            raise ValidationPipelineError("Pipeline Validation Error: Error while validating response.") from err

        
    def transform(
            self,
            response: ValidatedResponseModel,
            model: type[DataSource]
    ) -> TransformedResponseModel:
        # Run respective transformer fn based on model.
        pass
    
    def run(self, response, source, model):
        ...
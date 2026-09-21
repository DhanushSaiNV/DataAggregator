from data_aggregator.domain.exceptions import *
from data_aggregator.pipeline import Pipeline, PipelineStage, PipelineState
from data_aggregator.sources import (
    CoinSource,
    CountriesSource,
    DataSource,
    WeatherSource,
)


class DataAggregator:
    def __init__(
        self,
        sources: list[type[DataSource]],
        pipeline_stages: list[PipelineStage]
    ) -> None:
        self.sources = sources
        self.pipeline_stages = pipeline_stages


        self.pipeline = Pipeline(
            PipelineStage.VALIDATE,
            PipelineStage.TRANSFORM
        )

        self.pipeline_state: PipelineStage


    def _fetch(self) -> list[ResponseModel]:
        pass


    def _transform(self) -> None:
        pass


    def _display(self):
        pass
            
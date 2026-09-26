from typing import Self

from data_aggregator.domain import *
from data_aggregator.pipeline import (
        Pipeline,
        PipelineConfig,
        PipelineStage,
        PipelineState,
)
from data_aggregator.sources import AsyncDataSource, DataSource


def transform(pipeline, pipeline_configs, pipeline_output_states):
        if not pipeline_configs:
            raise AggregatorError("ERROR: Invalid pipeline config.")

        for config in pipeline_configs:
            try:
                output_state: PipelineState = pipeline.run(config)
            except InvalidPipelineStageError as err:
                raise AggregatorError("ERROR: Invalid pipeline stage.") from err
            except ValidationPipelineError as err:
                raise AggregatorError(
                    f"ERROR: Response Validation failed; {err.message}"
                ) from err
            except InvalidTransformerError as err:
                raise AggregatorError("ERROR: Invalid Transformer; ") from err

            pipeline_output_states.append(output_state)


def _display(pipeline_output_states):
    for output_state in pipeline_output_states:
        display(output_state.data)
        print("\n")
        print("-" * 10)
        print("\n")



class DataAggregator:
    def __init__(
        self,
        sources: list[type[DataSource]],
        pipeline_stages: list[PipelineStage],
    ) -> None:
        self.sources = sources
        self.pipeline_stages = pipeline_stages

        self.pipeline_configs: list[PipelineConfig] = []
        self.pipeline_state: PipelineState
        self.pipeline_output_states: list[PipelineState] = []

        self.pipeline = Pipeline(*pipeline_stages)

    def fetch(self) -> Self:
        """Fetches data from provided DataSource classes. Parses them."""
        self.responses: list[ResponseModel] = []

        for Source in self.sources:
            if not issubclass(Source, DataSource):
                raise InvalidSourceError(
                    f"Source `{Source.__name__}` is not a valid DataSource instance."
                )

            datasource_obj: DataSource = Source()

            response: ResponseModel = self.__fetch_parse_from_datasource(datasource_obj)

            self.__update_pipeline_configs(
                datasource_obj,
                response,
                Source,
            )

            self.responses.append(response)

        return self

    def __update_pipeline_configs(self, datasource_obj, response, Source):
        self.pipeline_configs.append(
            PipelineConfig(
                response=response,
                source=Source,
                validation_model=datasource_obj.validated_model,
            )
        )

    def __fetch_parse_from_datasource(
        self, datasource_obj: DataSource
    ) -> ResponseModel:
        try:
            return datasource_obj.fetch().parse()

        except ResponseValidationError as err:
            raise AggregatorError(
                f"ERROR: Data Validation Failed.\n{err.message}"
            ) from err

        except DataFetchError as err:
            raise AggregatorError("ERROR: Data fetching failed.") from err

    def run(self, display: bool = True):
        self.fetch()
        transform(self.pipeline, self.pipeline_configs, self.pipeline_output_states)

        if display:
            _display(self.pipeline_output_states)

        return self.pipeline_output_states

    

class AsyncDataAggregator:
    def __init__(
        self,
        sources: list[type[AsyncDataSource]],
        pipeline_stages: list[PipelineStage],
    ) -> None:
        self.sources = sources
        self.pipeline_stages = pipeline_stages

        self.pipeline_configs: list[PipelineConfig] = []
        self.pipeline_state: PipelineState
        self.pipeline_output_states: list[PipelineState] = []

        self.pipeline = Pipeline(*pipeline_stages)

    async def fetch(self) -> Self:
        """Fetches data from provided DataSource classes. Parses them."""
        self.responses: list[ResponseModel] = []

        for Source in self.sources:
            if not issubclass(Source, DataSource | AsyncDataSource):
                raise InvalidSourceError(
                    f"Source `{Source.__name__}` is not a valid DataSource instance."
                )

            datasource_obj: DataSource = Source()

            response: ResponseModel = await self.__fetch_parse_from_datasource(datasource_obj)

            self.__update_pipeline_configs(
                datasource_obj,
                response,
                Source,
            )

            self.responses.append(response)

        return self

    def __update_pipeline_configs(self, datasource_obj, response, Source):
        self.pipeline_configs.append(
            PipelineConfig(
                response=response,
                source=Source,
                validation_model=datasource_obj.validated_model,
            )
        )

    async def __fetch_parse_from_datasource(
        self, datasource_obj: AsyncDataSource
    ) -> ResponseModel:
        try:
            response = await datasource_obj.fetch()
            
            return response.parse()

        except ResponseValidationError as err:
            raise AggregatorError(
                f"ERROR: Data Validation Failed.\n{err.message}"
            ) from err

        except DataFetchError as err:
            raise AggregatorError("ERROR: Data fetching failed.") from err

    async def run(self, display: bool = True):
        await self.fetch()
        transform(self.pipeline, self.pipeline_configs, self.pipeline_output_states)
        
        if display:
            _display(self.pipeline_output_states)

        return self.pipeline_output_states
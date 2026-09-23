from typing import Self

from data_aggregator.domain import *
from data_aggregator.pipeline import (
    Pipeline,
    PipelineConfig,
    PipelineStage,
    PipelineState,
)
from data_aggregator.sources import DataSource


class DataAggregator:
    def __init__(
        self, sources: list[type[DataSource]], pipeline_stages: list[PipelineStage]
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

    def __fetch_parse_from_datasource(self, datasource_obj: DataSource) -> ResponseModel:
        try:
            return datasource_obj.fetch().parse()
        
        except ResponseValidationError as err:
            raise AggregatorError(
                f"ERROR: Data Validation Failed.\n{err.message}"
            ) from err

        except DataFetchError as err:
            raise AggregatorError("ERROR: Data fetching failed.") from err

    def transform(self) -> Self:
        if not self.pipeline_configs:
            raise AggregatorError("ERROR: Invalid pipeline config.")

        for config in self.pipeline_configs:
            try:
                output_state: PipelineState = self.pipeline.run(
                    config
                )
            except InvalidPipelineStageError as err:
                raise AggregatorError("ERROR: Invalid pipeline stage.") from err
            except ValidationPipelineError as err:
                raise AggregatorError(f"ERROR: Response Validation failed; {err.message}") from err
            except InvalidTransformerError as err:
                raise AggregatorError("ERROR: Invalid Transformer; ") from err
            
            self.pipeline_output_states.append(
                output_state
            )

        return self


    def display(self) -> Self:
        for output_state in self.pipeline_output_states:
            display(output_state.data)
            print("\n")
            print("-" * 10)
            print("\n")

        return self


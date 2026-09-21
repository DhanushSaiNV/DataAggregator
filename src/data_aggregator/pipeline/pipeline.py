from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum, auto

from pydantic import ValidationError

from data_aggregator.domain.exceptions import (
    InvalidPipelineStageError,
    InvalidTransformerError,
    ValidationPipelineError,
)
from data_aggregator.domain.models import (
    ResponseModel,
    TransformedResponseModel,
    ValidatedResponseModel,
)
from data_aggregator.sources.data_source import DataSource


class PipelineStage(Enum):
    VALIDATE = auto()
    TRANSFORM = auto()


type StageInput = ResponseModel | ValidatedResponseModel | TransformedResponseModel

type StageOutput = ResponseModel | ValidatedResponseModel | TransformedResponseModel


@dataclass
class PipelineState:
    source: type[DataSource]
    response: ResponseModel
    validation_model: type[ValidatedResponseModel]
    data: ResponseModel = field(init=False)

    def __post_init__(self):
        self.data = self.response


class Pipeline:
    def __init__(self, *stages: PipelineStage) -> None:
        for stage in stages:
            if not isinstance(stage, PipelineStage):
                raise InvalidPipelineStageError(
                    f"Invalid Pipeline Stage: {stage} must be one of valid pipeline stages."
                )

        self.stages = stages

        self.STEP_REGISTRY: dict[PipelineStage, Callable] = {
            PipelineStage.VALIDATE: self._validate,
            PipelineStage.TRANSFORM: self._transform,
        }

    def _validate(self, state: PipelineState) -> StageOutput:
        """Validates ResponseModel(s) and returns ValidatedResponseModel(s)"""
        try:
            return state.validation_model.model_validate(state.response)

        except ValidationError as err:
            raise ValidationPipelineError(
                "Pipeline Validation Error: Error while validating response."
            ) from err

    def _transform(self, state: PipelineState) -> StageOutput:
        # Run respective transformer fn based on source.
        try:
            from data_aggregator.pipeline.transformers import transform_response

            transform_fn: Callable = transform_response
        except KeyError as err:
            raise InvalidTransformerError(
                f"Transformer {state.source.__name__} Not Found"
            ) from err

        return transform_fn(state.data)

    def run(
        self,
        response: ResponseModel,
        source: type[DataSource],
        validation_model: type[ValidatedResponseModel],
    ) -> PipelineState:
        """
        Takes a response, its source and response model
        performs stages of pipeline steps from self.stages
        returns ProcessedData
        """

        self.state = PipelineState(
            response=response, source=source, validation_model=validation_model
        )

        for stage in self.stages:
            self.state.data = self.STEP_REGISTRY[stage](self.state)
            # print(f"\nDEBUG: Stage{stage.name}, Data: ", self.state.data)

        return self.state

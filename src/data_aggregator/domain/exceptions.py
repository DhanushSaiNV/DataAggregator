from typing import Any

from data_aggregator.domain.models import ResponseModel

"""
- AggregatorError
 |
 |- DataFetchError
 | |-- ResponseValidationError
 | |-- 
 |
 |- PipelineError
 | |-- InvalidPipelineStageError
 | |-- ValidationPipelineError
 |
 |- VisualError
  ...

"""


class AggregatorError(Exception):
    """Base exception for expected application errors"""


class DataFetchError(AggregatorError):
    pass


class ResponseValidationError(DataFetchError):
    def __init__(
        self,
        response_dict: dict[Any, Any] | None = None,
        response_model: type[ResponseModel] | None = None,
        *args: object,
    ) -> None:
        self.response_dict = response_dict
        self.response_model = response_model
        self.argslist = args

        dict_msg = (
            str(response_dict)
            if response_dict is not None
            else "Response dict not passed."
        )
        
        model_msg = (
            repr(response_model.__name__)
            if response_model is not None
            else "Response model not passed."
        )

        args_str = " ".join(str(arg) for arg in args) if args else ""
        
        message = f"Validation error: {dict_msg}\nExpected model: {model_msg}\n{args_str}".strip()

        super().__init__(message, *args)


class PipelineError(AggregatorError):
    pass

class InvalidPipelineStageError(PipelineError):
    pass

class ValidationPipelineError(PipelineError):
    pass

class VisualEror(AggregatorError):
    pass

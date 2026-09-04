from functools import wraps

from pydantic import ValidationError

from data_aggregator.domain.exceptions import *


def parser(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)

        except ValidationError as e:
            raise ResponseValidationError(
                self.response_dict, self.response_model, e
            ) from e

    return wrapper
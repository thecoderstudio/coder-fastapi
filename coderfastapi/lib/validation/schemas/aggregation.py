from codercore.lib.aggregation import (
    AggregationParameters,
    DatedAggregationParametersMixin,
)
from pydantic import model_validator
from pydantic.dataclasses import dataclass
from pydantic_core import ArgsKwargs


@dataclass
class AggregationParametersSchema(AggregationParameters):
    pass


@dataclass
class DatedAggregationParametersMixinSchema(DatedAggregationParametersMixin):
    @model_validator(mode="before")
    @classmethod
    def validate(cls, values: ArgsKwargs) -> ArgsKwargs:
        kwargs = values.kwargs if values.kwargs else {}
        max_date = kwargs.get("max_date")
        min_date = kwargs.get("min_date")
        if max_date and min_date and max_date < min_date:
            raise ValueError("max_date must be >= min_date")
        return values

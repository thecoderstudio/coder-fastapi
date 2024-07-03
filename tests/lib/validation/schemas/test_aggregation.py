from datetime import UTC, datetime

import pytest
from codercore.lib.aggregation import DatePrecision
from codercore.test.pydantic import check_validation_value_error
from pydantic_core import ArgsKwargs

from coderfastapi.lib.validation.schemas.aggregation import (
    AggregationParametersSchema,
    DatedAggregationParametersMixinSchema,
)


def test_aggregation_parameters_schema_complete():
    grouped_by = ["a", "b"]
    params = AggregationParametersSchema(grouped_by=grouped_by)
    assert params.grouped_by == grouped_by


def test_aggregation_parameters_schema_defaults():
    params = AggregationParametersSchema()
    assert params.grouped_by == []


@pytest.mark.parametrize("date_precision", tuple(DatePrecision))
def test_dated_aggregation_parameters_mixin_schema_complete(date_precision):
    min_date = datetime.now(UTC)
    max_date = datetime.now(UTC)
    params = DatedAggregationParametersMixinSchema(
        min_date=min_date,
        max_date=max_date,
        date_precision=date_precision,
    )
    assert params.min_date == min_date
    assert params.max_date == max_date
    assert params.date_precision == date_precision


def test_dated_aggregation_parameters_mixin_schema_max_date_preceeds_min_date():
    max_date = datetime.now(UTC)
    min_date = datetime.now(UTC)
    with pytest.raises(ValueError) as e:
        DatedAggregationParametersMixinSchema(min_date=min_date, max_date=max_date)

    error = e.value.errors(include_url=False)[0]
    del error["ctx"]
    assert error == {
        "type": "value_error",
        "loc": (),
        "msg": "Value error, max_date must be >= min_date",
        "input": ArgsKwargs(
            (),
            {
                "min_date": min_date,
                "max_date": max_date,
            },
        ),
    }


def test_dated_aggregation_parameters_mixin_schema_defaults():
    params = DatedAggregationParametersMixinSchema()
    assert params.min_date is None
    assert params.max_date is None
    assert params.date_precision is None

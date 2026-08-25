from datetime import date

import pytest

from bcch_sdk.builders.parameters import ParameterBuilder
from bcch_sdk.builders.time_series import TimeSeriesBuilder
from bcch_sdk.exceptions import (
    InvalidCredentialsException,
    InvalidDateException,
    InvalidSeriesException,
)
from bcch_sdk.types.enums import Frequency
from tests.factories import DUMMY_CREDENTIALS


@pytest.mark.parametrize("value", [None, "", "   ", ",", [], [""], {}, {"x": ""}])
def test_time_series_builder_rejects_empty_inputs(value: object) -> None:
    with pytest.raises(InvalidSeriesException):
        TimeSeriesBuilder.to_list(value)  # type: ignore[arg-type]


def test_time_series_builder_normalizes_and_deduplicates_values() -> None:
    assert TimeSeriesBuilder.to_list(" SF1, SF2, SF1 ") == ["SF1", "SF2"]


def test_time_series_builder_rejects_non_string_values() -> None:
    with pytest.raises(InvalidSeriesException, match="must be a string"):
        TimeSeriesBuilder.to_list(["SF1", 2])  # type: ignore[list-item]


def test_parameter_builder_rejects_reversed_date_range() -> None:
    with pytest.raises(InvalidDateException, match="first date"):
        ParameterBuilder.build_get_series_params(
            DUMMY_CREDENTIALS,
            "SF1",
            date(2024, 2, 1),
            date(2024, 1, 1),
        )


@pytest.mark.parametrize("value", ["", "2024/01/01", 1])
def test_parameter_builder_rejects_invalid_dates(value: object) -> None:
    with pytest.raises(InvalidDateException):
        ParameterBuilder.build_get_series_params(
            DUMMY_CREDENTIALS,
            "SF1",
            value,  # type: ignore[arg-type]
        )


def test_parameter_builder_rejects_empty_credentials() -> None:
    with pytest.raises(InvalidCredentialsException):
        ParameterBuilder.build_get_series_params(
            {"username": "", "password": ""},
            "SF1",
        )


def test_parameter_builder_accepts_valid_values() -> None:
    params = ParameterBuilder.build_get_series_params(
        DUMMY_CREDENTIALS,
        " SF1 ",
        "2024-01-01",
        "2024-01-31",
    )
    assert params["timeseries"] == "SF1"
    assert params["firstdate"] == "2024-01-01"
    assert params["lastdate"] == "2024-01-31"
    assert ParameterBuilder.build_search_params(DUMMY_CREDENTIALS, Frequency.DAILY)

import pandas
import polars
import pytest

from src.exceptions import ResponseParseException
from src.mappers.dataframe import DataFrameMapper
from src.models.series import Series
from src.models.web_service import WebServiceResponse

from tests.factories import build_search_response, build_series_response


def test_get_series_returns_polars_by_default() -> None:
    response = build_series_response(series_id="SF_TEST", observations_count=2)

    result = DataFrameMapper.get_series(response)

    assert isinstance(result, polars.DataFrame)
    assert result.columns == ["date", "SF_TEST"]
    assert result.height == 2


def test_get_series_returns_pandas_when_requested() -> None:
    response = build_series_response(series_id="SF_TEST", observations_count=2)

    result = DataFrameMapper.get_series(response, polars_response=False)

    assert isinstance(result, pandas.DataFrame)
    assert list(result.columns) == ["date", "SF_TEST"]
    assert len(result) == 2


def test_get_series_raises_when_series_is_missing() -> None:
    response = WebServiceResponse(
        code=0,
        description="Success",
        series=None,
        series_information=None,
    )

    with pytest.raises(ResponseParseException, match="did not include series data"):
        DataFrameMapper.get_series(response)


def test_get_series_raises_when_observations_are_empty() -> None:
    response = WebServiceResponse(
        code=0,
        description="Success",
        series=Series(
            id="SF_EMPTY",
            spanish_description="Empty",
            english_description="Empty",
            observations=[],
        ),
        series_information=None,
    )

    with pytest.raises(
        ResponseParseException, match="did not contain any observations"
    ):
        DataFrameMapper.get_series(response)


def test_search_series_returns_pandas_when_requested() -> None:
    response = build_search_response(items_count=2)

    result = DataFrameMapper.search_series(response, polars_response=False)

    assert isinstance(result, pandas.DataFrame)
    assert list(result["id"]) == ["SF0", "SF1"]


def test_search_series_raises_when_information_is_missing() -> None:
    response = WebServiceResponse(
        code=0,
        description="Success",
        series=None,
        series_information=None,
    )

    with pytest.raises(
        ResponseParseException, match="did not include series information"
    ):
        DataFrameMapper.search_series(response)


def test_search_series_raises_when_information_is_empty() -> None:
    response = WebServiceResponse(
        code=0,
        description="Success",
        series=None,
        series_information=[],
    )

    with pytest.raises(ResponseParseException, match="did not contain any series"):
        DataFrameMapper.search_series(response)

import logging
from typing import Self
from types import TracebackType
from datetime import datetime, date

from dataclasses import dataclass

from httpx import AsyncClient, HTTPStatusError, QueryParams, RequestError, Response

from .base import BaseAsyncClient

from src.builders.parameters import ParameterBuilder

from src.models.web_service import WebServiceResponse

from src.types.enums import Frequency

from src.exceptions import (
    InvalidsCredentialsException,
    InvalidDateException,
    InvalidSeriesException,
    InvalidFrequencyException,
    WebServiceResponseException,
    TransportException,
    ResponseParseException,
)


logger = logging.getLogger(__name__)


@dataclass
class BCChAsyncClient(BaseAsyncClient):
    """
    The `BCChAsyncClient` class is an asynchronous client for the Banco Central de Chile API.

    Args:
        session (AsyncClient): client for making requests to the API.
    """

    session: AsyncClient | None = None

    def __post_init__(self):
        logger.debug("Initializing BCChAsyncClient with timeout=%s", self.timeout)
        if self.session is None:
            self.session = AsyncClient(timeout=self.timeout, transport=self.transport)

    async def _validate_response(self, response: Response) -> WebServiceResponse:
        try:
            response.raise_for_status()
        except HTTPStatusError as exc:
            logger.debug("HTTP status error for %s: %s", response.url, exc)
            raise WebServiceResponseException(
                f"Request failed with status code: {response.status_code}"
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            logger.debug("Invalid JSON response from %s: %s", response.url, exc)
            raise ResponseParseException(
                "Failed to decode JSON from the Banco Central API response."
            ) from exc

        return WebServiceResponse.model_validate(payload)

    async def get_series(
        self,
        time_series: str,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
    ):
        if self.session is None:
            raise TransportException("HTTP client session is not initialized.")

        if self.credentials is None:
            raise InvalidsCredentialsException("Client credentials must be provided.")

        params = ParameterBuilder.build_get_series_params(
            self.credentials,
            time_series,
            first_date,
            last_date,
        )

        logger.info("Requesting async series %s", time_series)
        logger.debug("Async GET params: %s", params)

        try:
            response = await self.session.get(
                self.base_url, params=QueryParams(**params)
            )
            r = await self._validate_response(response)
        except RequestError as exc:
            logger.error(
                "Transport error while requesting series %s: %s", time_series, exc
            )
            raise TransportException(
                "A transport error occurred while requesting series data."
            ) from exc

        if r.code == -50:
            raise InvalidSeriesException("The requested series identifier is invalid.")

        if r.code == -1:
            raise InvalidDateException(
                "The requested dates are invalid or outside the supported range."
            )

        return r

    async def search_series(
        self,
        frequency: Frequency,
    ) -> WebServiceResponse:
        if self.session is None:
            raise TransportException(
                "Session is not initialized. Use 'with' statement to manage the session."
            )

        if self.credentials is None:
            raise InvalidsCredentialsException("Client credentials must be provided.")

        params = ParameterBuilder.build_search_params(self.credentials, frequency)

        logger.info("Searching async series metadata for frequency %s", frequency)
        logger.debug("Async search params: %s", params)

        try:
            response = await self.session.get(
                self.base_url, params=QueryParams(**params)
            )
            r = await self._validate_response(response)
        except RequestError as exc:
            logger.error(
                "Transport error while searching frequency %s: %s", frequency, exc
            )
            raise TransportException(
                "A transport error occurred while executing the search request."
            ) from exc

        if r.code == -5:
            raise InvalidsCredentialsException("The provided credentials are invalid.")

        if r.code == -1:
            raise InvalidFrequencyException(
                "The requested frequency is invalid for the search operation."
            )

        return r

    async def __aenter__(self) -> Self:
        if self.session is None:
            logger.debug("Opening async client session in context manager")
            self.session = AsyncClient(timeout=self.timeout)

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self.session:
            logger.debug("Closing async client session")
            await self.session.aclose()

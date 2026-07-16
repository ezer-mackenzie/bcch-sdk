from typing import Self
from types import TracebackType
from datetime import datetime, date

from dataclasses import dataclass

import logging

from httpx import AsyncClient, QueryParams, RequestError

from .base_async import BaseAsyncClient

from ..builders.parameters import ParameterBuilder

from ..models.web_service import WebServiceResponse

from ..types.enums import Frequency

from ..exceptions import (
    InvalidsCredentialsException,
    InvalidDateException,
    InvalidSeriesException,
    InvalidFrequencyException,
    TransportException,
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

            r = self._validate_response(response)

            if r.code == -50:
                raise InvalidSeriesException(
                    "The requested series identifier is invalid."
                )

            if r.code == -1:
                raise InvalidDateException(
                    "The requested dates are invalid or outside the supported range."
                )

            return r

        except RequestError as exc:
            logger.error(
                "Transport error while requesting series %s: %s", time_series, exc
            )
            raise TransportException(
                "A transport error occurred while requesting series data."
            ) from exc

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
            r = self._validate_response(response)

            if r.code == -5:
                raise InvalidsCredentialsException(
                    "The provided credentials are invalid."
                )

            if r.code == -1:
                raise InvalidFrequencyException(
                    "The requested frequency is invalid for the search operation."
                )

            return r

        except RequestError as exc:
            logger.error(
                "Transport error while searching frequency %s: %s", frequency, exc
            )
            raise TransportException(
                "A transport error occurred while executing the search request."
            ) from exc

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

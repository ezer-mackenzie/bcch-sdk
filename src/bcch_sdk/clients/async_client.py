from typing import Self
from types import TracebackType
from datetime import datetime, date

from dataclasses import dataclass, field

import logging

from httpx import AsyncClient, QueryParams, RequestError

from .base.async_client import BaseAsyncClient

from ..builders.parameters import ParameterBuilder

from ..models.web_service import WebServiceResponse

from ..types.enums import Frequency

from ..exceptions import InvalidCredentialsException, TransportException


logger = logging.getLogger(__name__)


@dataclass
class BCChAsyncClient(BaseAsyncClient):
    """
    The `BCChAsyncClient` class is an asynchronous client for the Banco Central de Chile API.

    Args:
        session (AsyncClient): client for making requests to the API.
    """

    session: AsyncClient | None = None
    _owns_session: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        logger.debug("Initializing BCChAsyncClient with timeout=%s", self.timeout)
        if self.session is None:
            self._open_session()

    def _open_session(self) -> None:
        self.session = AsyncClient(timeout=self.timeout, transport=self.transport)
        self._owns_session = True

    async def get_series(
        self,
        time_series: str,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
    ) -> WebServiceResponse:
        if self.session is None:
            raise TransportException("HTTP client session is not initialized.")

        if self.credentials is None:
            raise InvalidCredentialsException("Client credentials must be provided.")

        params = ParameterBuilder.build_get_series_params(
            self.credentials,
            time_series,
            first_date,
            last_date,
        )

        logger.info("Requesting async series %s", time_series)

        try:
            response = await self.session.get(
                self.base_url, params=QueryParams(**params)
            )

            r = self._validate_response(response)

            return self._validate_api_code(r, operation="get_series")

        except RequestError:
            logger.error("Transport error while requesting series %s", time_series)
            raise TransportException(
                "A transport error occurred while requesting series data."
            ) from None

    async def search_series(
        self,
        frequency: Frequency,
    ) -> WebServiceResponse:
        if self.session is None:
            raise TransportException(
                "Session is not initialized. Use 'with' statement to manage the session."
            )

        if self.credentials is None:
            raise InvalidCredentialsException("Client credentials must be provided.")

        params = ParameterBuilder.build_search_params(self.credentials, frequency)

        logger.info("Searching async series metadata for frequency %s", frequency)

        try:
            response = await self.session.get(
                self.base_url, params=QueryParams(**params)
            )
            r = self._validate_response(response)

            return self._validate_api_code(r, operation="search_series")

        except RequestError:
            logger.error("Transport error while searching frequency %s", frequency)
            raise TransportException(
                "A transport error occurred while executing the search request."
            ) from None

    async def __aenter__(self) -> Self:
        if self.session is None:
            logger.debug("Opening async client session in context manager")
            self._open_session()

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self.session and self._owns_session:
            logger.debug("Closing async client session")
            await self.session.aclose()
            self.session = None
            self._owns_session = False

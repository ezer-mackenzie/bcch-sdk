from typing import Self
from types import TracebackType
from datetime import datetime, date

from dataclasses import dataclass, field

from httpx import Client, QueryParams, RequestError

import logging

from .base.sync_client import BaseSyncClient

from ..builders.parameters import ParameterBuilder

from ..models.web_service import WebServiceResponse
from ..types.enums import Frequency

from ..exceptions import InvalidCredentialsException, TransportException


logger = logging.getLogger(__name__)


@dataclass
class BCChSyncClient(BaseSyncClient):
    session: Client | None = None
    _owns_session: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        logger.debug("Initializing BCChSyncClient with timeout=%s", self.timeout)
        if self.session is None:
            self._open_session()

    def _open_session(self) -> None:
        self.session = Client(timeout=self.timeout, transport=self.transport)
        self._owns_session = True

    def get_series(
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

        logger.info("Requesting series %s", time_series)

        try:
            response = self.session.get(self.base_url, params=QueryParams(**params))
            r = self._validate_response(response)
        except RequestError:
            logger.error("Transport error while requesting series %s", time_series)
            raise TransportException(
                "A transport error occurred while requesting series data."
            ) from None

        return self._validate_api_code(r, operation="get_series")

    def search_series(self, frequency: Frequency) -> WebServiceResponse:
        if self.session is None:
            raise TransportException("HTTP client session is not initialized.")

        if self.credentials is None:
            raise InvalidCredentialsException("Client credentials must be provided.")

        params = ParameterBuilder.build_search_params(self.credentials, frequency)

        logger.info("Searching series metadata for frequency %s", frequency)

        try:
            response = self.session.get(self.base_url, params=QueryParams(**params))
            r = self._validate_response(response)
        except RequestError:
            logger.error("Transport error while searching frequency %s", frequency)
            raise TransportException(
                "A transport error occurred while executing the search request."
            ) from None

        return self._validate_api_code(r, operation="search_series")

    def __enter__(self) -> Self:
        if self.session is None:
            logger.debug("Opening sync client session in context manager")
            self._open_session()

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self.session and self._owns_session:
            logger.debug("Closing sync client session")
            self.session.close()
            self.session = None
            self._owns_session = False

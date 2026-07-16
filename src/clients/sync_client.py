from typing import Self
from types import TracebackType
from datetime import datetime, date

from dataclasses import dataclass

from httpx import Client, QueryParams, RequestError

import logging

from .base_sync import BaseSyncClient

from ..builders.parameters import ParameterBuilder

from ..models.web_service import WebServiceResponse 
from ..types.enums import Frequency

from ..exceptions import (
    InvalidsCredentialsException,
    InvalidDateException,
    InvalidFrequencyException,
    InvalidSeriesException,
    TransportException,
)


logger = logging.getLogger(__name__)

@dataclass
class BCChSyncClient(BaseSyncClient):
    session: Client | None = None

    def __post_init__(self) -> None:
        logger.debug("Initializing BCChSyncClient with timeout=%s", self.timeout)
        if self.session is None:
            self.session = Client(timeout=self.timeout, transport=self.transport)

    def get_series(
        self,
        time_series: str,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
    ) -> WebServiceResponse:
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

        logger.info("Requesting series %s", time_series)
        logger.debug("Sync GET params: %s", params)

        try:
            response = self.session.get(self.base_url, params=QueryParams(**params))
            r = self._validate_response(response)
        except RequestError as exc:
            logger.error("Transport error while requesting series %s: %s", time_series, exc)
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

    def search_series(self, frequency: Frequency) -> WebServiceResponse:
        if self.session is None:
            raise TransportException("HTTP client session is not initialized.")

        if self.credentials is None:
            raise InvalidsCredentialsException("Client credentials must be provided.")

        params = ParameterBuilder.build_search_params(self.credentials, frequency)

        logger.info("Searching series metadata for frequency %s", frequency)
        logger.debug("Sync search params: %s", params)

        try:
            response = self.session.get(self.base_url, params=QueryParams(**params))
            r = self._validate_response(response)
        except RequestError as exc:
            logger.error("Transport error while searching frequency %s: %s", frequency, exc)
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

    def __enter__(self) -> Self:
        if self.session is None:
            logger.debug("Opening sync client session in context manager")
            self.session = Client(timeout=self.timeout)

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self.session:
            logger.debug("Closing sync client session")
            self.session.close()

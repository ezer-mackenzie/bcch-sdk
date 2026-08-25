from httpx import Timeout, HTTPStatusError, Response
from httpx_retries import RetryTransport, Retry

from dataclasses import dataclass, field

import json
import logging
from pydantic import ValidationError

from ...types.auth import InternalCredentials

from ...models.web_service import WebServiceResponse

from ...exceptions import (
    InvalidCredentialsException,
    InvalidDateException,
    InvalidFrequencyException,
    InvalidSeriesException,
    WebServiceResponseException,
    ResponseParseException,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class BaseClient:
    credentials: InternalCredentials | None = None

    base_url: str = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
    timeout: Timeout = field(
        default_factory=lambda: Timeout(10.0),
    )

    retry_policy: Retry = field(
        default_factory=lambda: Retry(total=3, backoff_factor=0.5),
    )

    def __post_init__(self) -> None:
        if self.credentials is None or not self.credentials.get("username", "").strip():
            raise InvalidCredentialsException("Client credentials must be provided.")
        if not self.credentials.get("password", "").strip():
            raise InvalidCredentialsException("Client credentials must be provided.")

    @property
    def transport(self) -> RetryTransport:
        return RetryTransport(retry=self.retry_policy)

    @staticmethod
    def _validate_api_code(
        response: WebServiceResponse,
        *,
        operation: str,
    ) -> WebServiceResponse:
        if response.code == 0:
            return response
        if response.code == -5:
            raise InvalidCredentialsException("The provided credentials are invalid.")
        if operation == "get_series" and response.code == -50:
            raise InvalidSeriesException("The requested series identifier is invalid.")
        if operation == "get_series" and response.code == -1:
            raise InvalidDateException(
                "The requested dates are invalid or outside the supported range."
            )
        if operation == "search_series" and response.code == -1:
            raise InvalidFrequencyException(
                "The requested frequency is invalid for the search operation."
            )
        raise WebServiceResponseException(
            f"Banco Central API error {response.code}: {response.description}"
        )

    def _validate_response(self, response: Response) -> WebServiceResponse:
        try:
            response.raise_for_status()
        except HTTPStatusError:
            logger.debug("HTTP response failed with status %s", response.status_code)
            raise WebServiceResponseException(
                f"Request failed with status code: {response.status_code}"
            ) from None

        try:
            # Banco Central returns JSON encoded as ISO-8859-1.
            # We parse response.text instead of response.json() to respect the charset.
            payload = json.loads(response.text)
            return WebServiceResponse.model_validate(payload)

        except json.JSONDecodeError as exc:
            raise ResponseParseException(
                "Failed to decode JSON from the Banco Central API response."
            ) from exc

        except ValidationError as exc:
            raise ResponseParseException(
                "The Banco Central API response does not match the expected schema."
            ) from exc

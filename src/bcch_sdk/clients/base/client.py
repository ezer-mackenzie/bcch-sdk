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

    def __post_init__(self):
        if self.credentials is None:
            raise InvalidCredentialsException("Client credentials must be provided.")

    @property
    def transport(self):
        return RetryTransport(retry=self.retry_policy)

    def _validate_response(self, response: Response) -> WebServiceResponse:
        try:
            response.raise_for_status()
        except HTTPStatusError as exc:
            logger.debug("HTTP status error for %s: %s", response.url, exc)
            raise WebServiceResponseException(
                f"Request failed with status code: {response.status_code}"
            ) from exc

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

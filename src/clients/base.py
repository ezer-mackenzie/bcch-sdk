from abc import ABC
from abc import abstractmethod
from datetime import datetime, date

from httpx import Timeout
from httpx_retries import RetryTransport, Retry

from dataclasses import dataclass, field

from src.types.auth import InternalCredentials
from src.types.enums import Frequency

from src.models.web_service import WebServiceResponse

from src.exceptions import InvalidsCredentialsException

@dataclass(slots=True)
class BaseClient:
    credentials: InternalCredentials | None = None

    base_url: str = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
    timeout: Timeout = Timeout(10.0)

    retry_policy: Retry = field(
        default_factory=lambda: Retry(total=3, backoff_factor=0.5),
    )

    def __post_init__(self):
        if self.credentials is None:
            raise InvalidsCredentialsException("Client credentials must be provided.")

    @property
    def transport(self):
        return RetryTransport(retry=self.retry_policy)

class BaseSyncClient(BaseClient, ABC):
    @abstractmethod
    def get_series(
        self,
        time_series: str,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
    ) -> WebServiceResponse:
        ...

    @abstractmethod
    def search_series(self, frequency: Frequency) -> WebServiceResponse:
        ...


class BaseAsyncClient(BaseClient, ABC):
    @abstractmethod
    async def get_series(
        self,
        time_series: str,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
    ) -> WebServiceResponse:
        ...

    @abstractmethod
    async def search_series(self, frequency: Frequency) -> WebServiceResponse:
        ...

from abc import ABCMeta
from abc import abstractmethod
from datetime import datetime, date

from httpx_retries import RetryTransport, Retry

from dataclasses import dataclass, field

from src.parameters.builder import ParameterBuilder

from src.types.auth import Credentials
from src.types.response.model import WebServiceResponse
from src.types.enums import Frequency

from src.exceptions import InvalidsCredentialsError


@dataclass(slots=True)
class BaseClient(metaclass=ABCMeta):
    credentials: Credentials | None = None

    base_url: str = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
    timeout: int = 10  # default timeout in seconds

    retry_policy: Retry = field(
        default_factory=lambda: Retry(total=3, backoff_factor=0.5),
    )
    parameter_builder: ParameterBuilder = field(default_factory=ParameterBuilder)

    def __post_init__(self):
        if self.credentials is None:
            raise InvalidsCredentialsError("Client credentials must be provided.")

    @abstractmethod
    def get_series(
        self,
        time_serie: str,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
    ) -> WebServiceResponse:
        raise NotImplementedError

    @abstractmethod
    def search_series(self, frequency: Frequency) -> WebServiceResponse:
        raise NotImplementedError

    @property
    def transport(self):
        return RetryTransport(retry=self.retry_policy)

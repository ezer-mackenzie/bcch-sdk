from httpx_retries import RetryTransport, Retry
from dataclasses import dataclass, field

from src.parameters.builder import ParameterBuilder

from src.types.auth import Credentials
from src.exceptions import InvalidsCredentialsError

@dataclass(slots=True)
class BCChBaseClient:
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

    @property
    def transport(self):
        return RetryTransport(retry=self.retry_policy)

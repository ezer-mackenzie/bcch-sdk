from dataclasses import dataclass, field

from httpx import Timeout

from ..exceptions import InvalidConfigurationException
from .auth import InternalCredentials


@dataclass(frozen=True, repr=False, slots=True)
class BCChConfig:
    credentials: InternalCredentials | None
    timeout: Timeout = field(
        default_factory=lambda: Timeout(10.0),
    )
    max_concurrency: int = 8

    def __post_init__(self) -> None:
        if self.max_concurrency < 1:
            raise InvalidConfigurationException(
                "max_concurrency must be greater than zero."
            )

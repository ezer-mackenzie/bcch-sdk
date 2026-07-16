from dataclasses import dataclass, field

from httpx import Timeout

from .auth import InternalCredentials


@dataclass(frozen=True, repr=False, slots=True)
class BCChConfig:
    credentials: InternalCredentials | None
    timeout: Timeout = field(
        default_factory=lambda: Timeout(10.0),
    )

from abc import ABC
from abc import abstractmethod

from httpx import Timeout
from typing import Generic, Self

from dataclasses import dataclass

from ...types.client import TClient
from ...types.config import BCChConfig


@dataclass(slots=True)
class BaseSDK(Generic[TClient], ABC):
    configuration: BCChConfig | None = None

    @classmethod
    def from_credentials(
        cls,
        username: str,
        password: str,
        timeout: Timeout | None = None,
    ) -> Self:
        config = BCChConfig(
            credentials={"username": username, "password": password},
            timeout=timeout or Timeout(10.0),
        )
        return cls(configuration=config)

    @abstractmethod
    def client(self) -> TClient: ...

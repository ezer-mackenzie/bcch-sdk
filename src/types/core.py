from typing import TypeVar

from dataclasses import dataclass

from httpx import Timeout

from .auth import InternalCredentials

ClientT = TypeVar("ClientT")
ResponseT = TypeVar("ResponseT")


@dataclass(frozen=True, repr=False, slots=True)
class BCChConfig:
    credentials: InternalCredentials | None
    timeout: Timeout = Timeout(10.0)

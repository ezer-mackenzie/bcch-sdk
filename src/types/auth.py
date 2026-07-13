from typing import TypedDict


class InternalCredentials(TypedDict):
    username: str
    password: str


QueryCredentials = TypedDict("QueryCredentials", {"user": str, "pass": str})

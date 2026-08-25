from ..exceptions import InvalidCredentialsException
from ..types.auth import InternalCredentials, QueryCredentials


class CredentialsMapper:
    @staticmethod
    def to_query_credentials(credentials: InternalCredentials) -> QueryCredentials:
        username = credentials.get("username", "").strip()
        password = credentials.get("password", "")
        if not username or not password.strip():
            raise InvalidCredentialsException(
                "Username and password must both be non-empty."
            )

        return {"user": username, "pass": password}

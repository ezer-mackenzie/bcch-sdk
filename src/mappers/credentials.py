from src.types.auth import InternalCredentials, QueryCredentials


class CredentialsMapper:
    @staticmethod
    def to_query_credentials(credentials: InternalCredentials) -> QueryCredentials:
        return {"user": credentials["username"], "pass": credentials["password"]}

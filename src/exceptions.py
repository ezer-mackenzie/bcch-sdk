class BCChSDKBaseException(Exception):
    """Base exception for all Banco Central Chile SDK errors."""

    default_message = "An unexpected error occurred in the Banco Central Chile SDK."

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)


class InvalidCredentialsException(BCChSDKBaseException):
    """Raised when the provided credentials are invalid."""

    default_message = "Invalid credentials were provided."


class InvalidsCredentialsException(InvalidCredentialsException):
    """Backward-compatible alias for invalid credentials errors."""

    pass


class InvalidSeriesException(BCChSDKBaseException):
    """Raised when the provided series identifier is invalid."""

    default_message = "The provided series identifier is invalid."


class InvalidFrequencyException(BCChSDKBaseException):
    """Raised when the requested frequency is invalid."""

    default_message = "The provided frequency is invalid."


class InvalidDateException(BCChSDKBaseException):
    """Raised when the provided date is invalid or out of range."""

    default_message = "The provided date is invalid or out of range."


class InvalidConfigurationException(BCChSDKBaseException):
    """Raised when the SDK configuration is missing or incomplete."""

    default_message = "SDK configuration is missing or incomplete."


class TransportException(BCChSDKBaseException):
    """Raised when a transport or network error occurs."""

    default_message = "A transport error occurred while contacting the Banco Central API."


class ResponseParseException(BCChSDKBaseException):
    """Raised when the SDK cannot parse the API response."""

    default_message = "The SDK could not parse the response from the Banco Central API."


class WebServiceResponseException(BCChSDKBaseException):
    """Raised when the API returns an unexpected or failed response."""

    default_message = "The Banco Central API returned an unexpected response."

import unittest

from src.exceptions import (
    BCChSDKBaseException,
    InvalidConfigurationException,
    InvalidCredentialsException,
    ResponseParseException,
)


class CustomExceptionTests(unittest.TestCase):
    def test_base_exception_uses_default_message(self) -> None:
        exc = BCChSDKBaseException()

        self.assertEqual(
            str(exc),
            "An unexpected error occurred in the Banco Central Chile SDK.",
        )

    def test_credentials_exception_has_default_message(self) -> None:
        exc = InvalidCredentialsException()

        self.assertEqual(str(exc), "Invalid credentials were provided.")

    def test_legacy_credentials_alias_is_preserved(self) -> None:
        exc = InvalidCredentialsException()

        self.assertIsInstance(exc, InvalidCredentialsException)
        self.assertEqual(str(exc), "Invalid credentials were provided.")

    def test_configuration_exception_has_default_message(self) -> None:
        exc = InvalidConfigurationException()

        self.assertEqual(
            str(exc),
            "SDK configuration is missing or incomplete.",
        )

    def test_response_parse_exception_has_default_message(self) -> None:
        exc = ResponseParseException()

        self.assertEqual(
            str(exc),
            "The SDK could not parse the response from the Banco Central API.",
        )


if __name__ == "__main__":
    unittest.main()

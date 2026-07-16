from importlib.metadata import version

import bcch_sdk
from bcch_sdk import (
    BCChAsyncSDK,
    BCChConfig,
    BCChSyncSDK,
    Frequency,
    InvalidCredentialsException,
    InvalidsCredentialsException,
    ObservationSeries,
    SerieInformation,
    Series,
    WebServiceResponse,
)
from bcch_sdk.clients import BCChAsyncClient, BCChSyncClient
from bcch_sdk.models import WebServiceResponse as ExportedWebServiceResponse


def test_public_package_exports_sdk_classes() -> None:
    assert BCChSyncSDK.__name__ == "BCChSyncSDK"
    assert BCChAsyncSDK.__name__ == "BCChAsyncSDK"


def test_public_subpackages_export_common_types_and_clients() -> None:
    assert BCChConfig.__name__ == "BCChConfig"
    assert Frequency.DAILY.value == "DAILY"
    assert BCChSyncClient.__name__ == "BCChSyncClient"
    assert BCChAsyncClient.__name__ == "BCChAsyncClient"


def test_public_package_exports_common_models_and_errors() -> None:
    assert WebServiceResponse is ExportedWebServiceResponse
    assert Series.__name__ == "Series"
    assert ObservationSeries.__name__ == "ObservationSeries"
    assert SerieInformation.__name__ == "SerieInformation"
    assert issubclass(InvalidsCredentialsException, InvalidCredentialsException)


def test_public_version_matches_installed_distribution() -> None:
    assert bcch_sdk.__version__ == version("bcch-sdk")


def test_public_all_contains_stable_entrypoints() -> None:
    expected = {
        "__version__",
        "BCChSyncSDK",
        "BCChAsyncSDK",
        "BCChConfig",
        "Frequency",
        "WebServiceResponse",
        "InvalidCredentialsException",
    }

    assert expected.issubset(set(bcch_sdk.__all__))

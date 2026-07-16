from bcch_sdk import BCChAsyncSDK, BCChSyncSDK
from bcch_sdk.clients import BCChAsyncClient, BCChSyncClient
from bcch_sdk.types import BCChConfig, Frequency


def test_public_package_exports_sdk_classes() -> None:
    assert BCChSyncSDK.__name__ == "BCChSyncSDK"
    assert BCChAsyncSDK.__name__ == "BCChAsyncSDK"


def test_public_subpackages_export_common_types_and_clients() -> None:
    assert BCChConfig.__name__ == "BCChConfig"
    assert Frequency.DAILY.value == "DAILY"
    assert BCChSyncClient.__name__ == "BCChSyncClient"
    assert BCChAsyncClient.__name__ == "BCChAsyncClient"

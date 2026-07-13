# Banco Central Chile SDK

A Python client library for the Banco Central de Chile SieteRestWS API.

This repository provides sync and async wrappers over the API, returning data as `pandas.DataFrame` or `polars.DataFrame` and managing retries, timeout configuration, and error handling.

## Features

- Synchronous and asynchronous SDK layers
- Built-in HTTP retries using `httpx-retries`
- Configurable `httpx.Timeout`
- `get_series(...)` and `search_series(...)`
- Output as `pandas.DataFrame` or `polars.DataFrame`
- Standard `logging` integration using `logging.getLogger(__name__)`
- Typed configuration and credentials

## Requirements

- Python 3.14+
- `aiohttp`
- `httpx[brotli,zstd]`
- `pydantic`
- `polars`
- `pandas`
- `httpx-retries`

## Installation

This project is structured for development in a `src/` layout.

Use Poetry if available:

```bash
poetry install
```

Or install the runtime dependencies manually:

```bash
python -m pip install aiohttp httpx[brotli,zstd] pydantic polars pandas httpx-retries
```

If you want to run code from the repository directly, make sure the `src/` folder is on `PYTHONPATH`:

```bash
export PYTHONPATH=$(pwd)/src
```

## Quickstart

Import the SDK classes and configure the client using `BCChConfig`.

### Sync example

```python
from httpx import Timeout
from src.types.core import BCChConfig
from src.sdk.sync_sdk import BCChSyncSDK

config = BCChConfig(
    credentials={"username": "your_user", "password": "your_pass"},
    timeout=Timeout(10.0),
)

sdk = BCChSyncSDK(configuration=config)

series_data = sdk.get_series(
    time_series="SF6041",
    first_date="2023-01-01",
    last_date="2023-12-31",
    polars_response=False,
)

print(series_data)
```

### Async example

```python
import asyncio
from httpx import Timeout
from src.types.core import BCChConfig
from src.sdk.async_sdk import BCChAsyncSDK

async def main() -> None:
    config = BCChConfig(
        credentials={"username": "your_user", "password": "your_pass"},
        timeout=Timeout(10.0),
    )

    sdk = BCChAsyncSDK(configuration=config)

    series_data = await sdk.get_series(
        time_series=["SF6041", "SF6060"],
        first_date="2023-01-01",
        last_date="2023-12-31",
        polars_response=True,
    )

    print(series_data)

asyncio.run(main())
```

### Search series example

```python
from src.types.enums import Frequency

result = sdk.search_series(Frequency.MONTHLY, polars_response=False)
print(result)
```

## Configuration

The main configuration object is `BCChConfig` from `src.types.core`.

- `credentials`: a typed dict with `username` and `password`
- `timeout`: an `httpx.Timeout` object

The SDK clients use `httpx` under the hood and will apply retries and timeout settings automatically.

## Logging

This library uses `logging.getLogger(__name__)` in each module. Consumers should configure handlers and levels in their own applications.

Example:

```python
import logging

logging.basicConfig(level=logging.INFO)
```

## Contributing

See `CONTRIBUTING.md` for contribution guidelines.

## Security

See `SECURITY.md` for security reporting and vulnerability handling.

## Code of Conduct

See `CODE_OF_CONDUCT.md` for community expectations.


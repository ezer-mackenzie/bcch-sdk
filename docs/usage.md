# Ejemplos de Uso

Esta página reúne patrones comunes. Para una primera instalación, revisa primero el [Quickstart](quickstart.md).

## SDK sincrónico con polars

`polars` es la respuesta por defecto.

```python
from bcch_sdk import BCChConfig, BCChSyncSDK

sdk = BCChSyncSDK(
    configuration=BCChConfig(
        credentials={"username": "tu_usuario", "password": "tu_password"}
    )
)

frames = sdk.get_series(
    time_series="SF43718",
    first_date="2024-01-01",
    last_date="2024-01-31",
)

frame = frames[0]
print(frame)
```

## SDK sincrónico con pandas

```python
frames = sdk.get_series(
    time_series="SF43718",
    first_date="2024-01-01",
    last_date="2024-01-31",
    polars_response=False,
)

frame = frames[0]
print(frame.head())
```

## Varias series

```python
series = {
    "uf": "F073.UFF.PRE.Z.D",
    "dolar": "F073.TCO.PRE.Z.D",
}

frames = sdk.get_series(
    time_series=series,
    first_date="2024-01-01",
    last_date="2024-01-31",
)

for name, frame in zip(series, frames):
    print(name, frame.shape)
```

## Búsqueda de catálogo

```python
from bcch_sdk import Frequency

daily_catalog = sdk.search_series(Frequency.DAILY)
monthly_catalog = sdk.search_series(Frequency.MONTHLY, polars_response=False)

print(daily_catalog)
print(monthly_catalog.head())
```

## Cliente directo

Los clientes directos retornan modelos de dominio, no DataFrames. Son útiles si necesitas controlar el mapeo tú mismo.

```python
from bcch_sdk.clients import BCChSyncClient

with BCChSyncClient(
    credentials={"username": "tu_usuario", "password": "tu_password"}
) as client:
    response = client.get_series(
        "SF43718",
        first_date="2024-01-01",
        last_date="2024-01-31",
    )

print(response.code)
print(response.series)
```

## Cliente asíncrono directo

```python
import asyncio

from bcch_sdk.clients import BCChAsyncClient


async def main() -> None:
    async with BCChAsyncClient(
        credentials={"username": "tu_usuario", "password": "tu_password"}
    ) as client:
        response = await client.get_series("SF43718")
        print(response.series)


asyncio.run(main())
```

## Manejo de errores

```python
from bcch_sdk import (
    InvalidCredentialsException,
    InvalidDateException,
    InvalidFrequencyException,
    InvalidSeriesException,
    ResponseParseException,
    TransportException,
    WebServiceResponseException,
)

try:
    frames = sdk.get_series("SF43718", first_date="2024-01-01")
except InvalidCredentialsException:
    print("Credenciales inválidas.")
except InvalidSeriesException:
    print("Serie inválida o no disponible.")
except InvalidDateException:
    print("Fecha inválida o fuera de rango.")
except InvalidFrequencyException:
    print("Frecuencia inválida para búsqueda.")
except WebServiceResponseException:
    print("El servicio respondió con un estado HTTP inesperado.")
except ResponseParseException:
    print("La respuesta no pudo convertirse al modelo esperado.")
except TransportException:
    print("Error de red o transporte.")
```

## Timeouts

Puedes pasar un `httpx.Timeout` personalizado en la configuración.

```python
from httpx import Timeout

config = BCChConfig(
    credentials={"username": "tu_usuario", "password": "tu_password"},
    timeout=Timeout(20.0),
)

sdk = BCChSyncSDK(configuration=config)
```

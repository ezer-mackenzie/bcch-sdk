# Quickstart

Esta guía muestra el camino recomendado para empezar con `bcch-sdk`.

## Instalación

```bash
python -m pip install bcch-sdk
```

Para desarrollo local desde el repositorio:

```bash
poetry install
```

## Credenciales

El Banco Central de Chile requiere credenciales para consultar SieteRestWS. El SDK recibe un diccionario con `username` y `password`.

```python
from bcch_sdk import BCChConfig

config = BCChConfig(
    credentials={
        "username": "tu_usuario",
        "password": "tu_password",
    }
)
```

## Consulta sincrónica

Usa `BCChSyncSDK` para scripts, notebooks o procesos batch simples.

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

print(frames[0])
```

`get_series` siempre retorna una secuencia de DataFrames. Si consultas una serie, usa `frames[0]`.

## Consulta asíncrona

Usa `BCChAsyncSDK` cuando tu aplicación ya trabaja con `asyncio`.

```python
import asyncio

from bcch_sdk import BCChAsyncSDK, BCChConfig


async def main() -> None:
    sdk = BCChAsyncSDK(
        configuration=BCChConfig(
            credentials={"username": "tu_usuario", "password": "tu_password"}
        )
    )

    frames = await sdk.get_series(
        time_series=["SF43718", "F073.TCO.PRE.Z.D"],
        first_date="2024-01-01",
        last_date="2024-01-31",
    )

    for frame in frames:
        print(frame)


asyncio.run(main())
```

## Buscar series

```python
from bcch_sdk import BCChConfig, BCChSyncSDK, Frequency

sdk = BCChSyncSDK(
    configuration=BCChConfig(
        credentials={"username": "tu_usuario", "password": "tu_password"}
    )
)

catalog = sdk.search_series(Frequency.DAILY)

print(catalog)
```

## Manejo básico de errores

```python
from bcch_sdk import (
    BCChConfig,
    BCChSyncSDK,
    InvalidCredentialsException,
    InvalidDateException,
    InvalidSeriesException,
    TransportException,
)

sdk = BCChSyncSDK(
    configuration=BCChConfig(
        credentials={"username": "tu_usuario", "password": "tu_password"}
    )
)

try:
    frames = sdk.get_series("SF43718", first_date="2024-01-01")
except InvalidCredentialsException:
    print("Credenciales inválidas.")
except InvalidSeriesException:
    print("La serie solicitada no existe o no está disponible.")
except InvalidDateException:
    print("El rango de fechas no es válido para la serie.")
except TransportException:
    print("No se pudo contactar al servicio del Banco Central.")
```

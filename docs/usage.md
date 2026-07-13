# Ejemplos de Uso y Quickstart

## Uso rápido (sincrónico)

Ejemplo mínimo con `BCChSyncClient`:

```python
from src.types.auth import InternalCredentials
from src.clients.sync_client import BCChSyncClient

creds: InternalCredentials = {"username": "mi_user", "password": "mi_pass"}

client = BCChSyncClient(credentials=creds)
resp = client.get_series("SF43718", first_date="2020-01-01", last_date="2023-01-01")
print(resp.series)
```

## Uso asíncrono

```python
import asyncio
from src.types.auth import InternalCredentials
from src.clients.async_client import BCChAsyncClient

async def main():
    creds: InternalCredentials = {"username": "mi_user", "password": "mi_pass"}
    async with BCChAsyncClient(credentials=creds) as client:
        resp = await client.get_series("SF43718")
        print(resp.series)

asyncio.run(main())
```

## Uso del SDK para múltiples series (paralelo)

La capa `sdk` y `concurrency` ofrece helpers para ejecutar múltiples consultas en paralelo sin reescribir la gestión de hilos/asíncrona.

Consulta la sección de `sdk/` para ejemplos más avanzados y patrones de agregación de resultados.

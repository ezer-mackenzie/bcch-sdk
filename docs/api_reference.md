# Referencia de la API del SDK

Esta página resume la API pública que debe usar cualquier consumidor del SDK.

## SDK público

La API estable se importa desde `bcch_sdk` y sus subpaquetes públicos. Los módulos `builders`, `dto` y `mappers` son detalles internos y pueden cambiar en releases menores antes de `1.0.0`.

### Imports recomendados

```python
from bcch_sdk import BCChSyncSDK, BCChAsyncSDK
from bcch_sdk import BCChConfig, Frequency
from bcch_sdk import InvalidCredentialsException, TransportException
```

También son públicos:

- `bcch_sdk.clients`: `BCChSyncClient`, `BCChAsyncClient`
- `bcch_sdk.sdk`: `BCChSyncSDK`, `BCChAsyncSDK`
- `bcch_sdk.types`: `BCChConfig`, `Frequency`, `InternalCredentials`
- `bcch_sdk.models`: `WebServiceResponse`, `Series`, `ObservationSeries`, `SeriesInformation`

`SerieInformation` se mantiene como alias compatible de `SeriesInformation` durante la serie `0.x`.

### Versionado

- `bcch_sdk.__version__` expone la versión instalada del paquete.
- Antes de `1.0.0`, cualquier cambio incompatible en imports públicos debe subir la versión menor.
- Desde `1.0.0`, cambios incompatibles deben reservarse para una versión mayor.

### SDKs

- `BCChSyncSDK`: capa de alto nivel para consultar una o varias series de forma sincrónica y retornar DataFrames.
- `BCChAsyncSDK`: capa de alto nivel para consultar una o varias series de forma asíncrona y retornar DataFrames.

### Clientes

- `BCChSyncClient` (ver [src/bcch_sdk/clients/sync_client.py](https://github.com/ezer-mackenzie/bank-central-chile-sdk/blob/main/src/bcch_sdk/clients/sync_client.py))
  - `get_series(time_series, first_date=None, last_date=None) -> WebServiceResponse`
  - `search_series(frequency) -> WebServiceResponse`

- `BCChAsyncClient` (ver [src/bcch_sdk/clients/async_client.py](https://github.com/ezer-mackenzie/bank-central-chile-sdk/blob/main/src/bcch_sdk/clients/async_client.py))
  - `async get_series(time_series, first_date=None, last_date=None) -> WebServiceResponse`
  - `async search_series(frequency) -> WebServiceResponse`

### Modelos de datos (returns)

- `WebServiceResponse` (Pydantic):
  - `code: int` — código de respuesta del backend.
  - `description: str` — descripción textual.
  - `series: Series | None` — estructura con observaciones (si corresponde).
  - `series_information: list[SeriesInformation] | None` — catálogo/metadata (si corresponde).

- `Series`:
  - `id`, `spanish_description`, `english_description`, `observations` (lista de `ObservationSeries`).

- `ObservationSeries`:
  - `index_date` (date), `value` (float), `status_code` (str)

### Parámetros HTTP y mapeos

- El argumento Python `time_series` se normaliza y finalmente se pasa en la query param `timeseries` (clave del backend). Consulte [src/bcch_sdk/builders/parameters.py](https://github.com/ezer-mackenzie/bank-central-chile-sdk/blob/main/src/bcch_sdk/builders/parameters.py).

### Errores que puedes capturar

- `TransportException` — problemas de red o inicialización de sesión.
- `WebServiceResponseException` — respuestas HTTP con status != 200.
- `ResponseParseException` — payload JSON inválido.
- `InvalidCredentialsException`, `InvalidSeriesException`, `InvalidDateException`, `InvalidFrequencyException` — errores de negocio.

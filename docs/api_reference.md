# Referencia de la API del SDK

Esta página resume la API pública que debe usar cualquier consumidor del SDK.

## SDK público

- `src/bcch_sdk/sdk/sync_sdk.py` y `src/bcch_sdk/sdk/async_sdk.py` exponen las funciones de alto nivel. Estas integran a los clientes y a los helpers de concurrencia.

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
  - `series_information: list[SerieInformation] | None` — catálogo/metadata (si corresponde).

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

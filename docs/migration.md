
# Guía de Migración: implementación legacy → `src/`

## Migración de v1 a v2

v2 mantiene los clientes, modelos y métodos principales, pero introduce dos
cambios incompatibles:

1. Instale el backend de DataFrame explícitamente:
   `bcch-sdk[polars]`, `bcch-sdk[pandas]` o `bcch-sdk[dataframe]`.
2. Reemplace `SerieInformation` por `SeriesInformation` e
   `InvalidsCredentialsException` por `InvalidCredentialsException`.

Una instalación base (`pip install bcch-sdk`) permite usar
`BCChSyncClient`/`BCChAsyncClient` y los modelos Pydantic. Invocar el SDK de
alto nivel sin el extra requerido produce
`MissingDataFrameDependencyException` con una instrucción de instalación.

Esta guía documenta las diferencias funcionales y de diseño entre la implementación legacy (código anterior usado como referencia) y la nueva implementación reescrita bajo `src/`.

Resumen rápido:

- La implementación legacy ofrecía una clase `Session` que exponía `get` y `search` (métodos sync usando `requests`).
- La reimplementación en `src/` separa responsabilidades en:
  - `clients/` — clientes sync/async con transporte y validación robusta.
  - `builders/` — construcción de parámetros y normalización de entradas.
  - `models/` — validación y conversión directa de payloads a modelos tipados (Pydantic).
  - `sdk/` — capa pública que ofrece conveniencias y concurrencia.

Detalles por módulo

- Legacy `credentials` vs `bcch_sdk.types.auth` + `bcch_sdk/mappers/credentials`

  - Legacy: funciones `get_credentials()` y `read_credentials(file)` que devuelven `(user, password)` leídos desde input o archivo.
  - Nueva: uso de `InternalCredentials` (`src/bcch_sdk/types/auth.py`) como `TypedDict` y `CredentialsMapper.to_query_credentials` (`bcch_sdk/mappers/credentials.py`) para transformar al dict de query esperado (`user`, `pass`).
  - Razonamiento: tipos explícitos y separación de IO (lectura de credenciales) de mapeo a parámetros de consulta.

- Legacy `exception` vs `src/bcch_sdk/exceptions`

  - Legacy: excepciones simples que heredan de `Exception` (p. ej. `InvalidSeries`, `InvalidCredentials`).
  - Nueva: jerarquía de excepciones más rica (`TransportException`, `ResponseParseException`, `InvalidCredentialsException`, `InvalidDateException`, etc.) que mejoran el control de flujos y diferenciación de fallos.
  - Razonamiento: distinguir problemas de transporte, parseo y errores de negocio facilita manejo en aplicaciones consumidoras.

- Legacy `webservice.Session` vs `src/bcch_sdk/clients/` (`BCChSyncClient` y `BCChAsyncClient`)

  - Legacy: `Session.get(time_series, first_date, last_date)` y `Session.search(frequency)` usando `requests.get`, parseo JSON directo y conversión con clases `WSResponse`.
  - Nueva: clientes sincronous y asíncronos (`src/bcch_sdk/clients/sync_client.py` y `src/bcch_sdk/clients/async_client.py`) que:
    - Soportan `httpx` con `Timeout` y `RetryTransport`.
    - Centralizan validación y parseo en `_validate_response` retornando `WebServiceResponse` tipado (`src/bcch_sdk/models/web_service.py`).
    - Tiran excepciones concretas para códigos de API y errores de transporte.
  - Razonamiento: independencia de la librería de transporte, mejores tiempos de espera configurables y reintentos automáticos.

- Formato de parámetros HTTP

  - Legacy: construía `params` con las claves `user`, `pass`, `firstdate`, `lastdate`, `timeseries` y `function`.
  - Nueva: `src/bcch_sdk/builders/parameters.py` encapsula la construcción de parámetros y usa `CredentialsMapper` además de `DateBuilder`. La clave usada para las series es `timeseries` (coincide con legacy).
  - Importante: la API Python expone `time_series` como nombre de variable/argumento, y `ParameterBuilder` mappea a la clave HTTP `timeseries`.

- Manejo de respuestas: implementación legacy vs `src/bcch_sdk/models/*`

  - Legacy: `WSResponse`, `GSResponse`, `SSResponse` con métodos para transformar a `pandas.Series` / `pandas.DataFrame`.
  - Nueva: modelos Pydantic (`src/bcch_sdk/models/web_service.py`, `src/bcch_sdk/models/series.py`, `src/bcch_sdk/models/series_information.py`, `src/bcch_sdk/models/observation_series.py`) que normalizan nombres de campos (camelCase → snake_case y traducciones más claras, p. ej. `descripEsp` → `spanish_description`).
  - Razonamiento: los alias de validación de Pydantic eliminan la necesidad de DTOs duplicados, mejoran la interoperabilidad con herramientas de tipado y permiten que `DataFrameMapper` genere DataFrames cuando se necesite.

Migración práctica — pasos recomendados para los usuarios del paquete legacy:

1. Reemplace `Session` por `BCChSyncClient` o `BCChAsyncClient`.
2. Cambie la lectura de credenciales para usar `InternalCredentials` o pasar un dict `{"username": ..., "password": ...}` y deje que la `CredentialsMapper` haga la transformación.
3. Ajuste el nombre del argumento `time_series` (el SDK lo usa así) — los parámetros HTTP continuarán usando `timeseries`.
4. Actualice su manejo de excepciones para capturar `TransportException`, `InvalidCredentialsException`, `ResponseParseException` en lugar de las excepciones legacy.

En la página de comparación (Comparison) se incluyen ejemplos concretos y fragmentos de código lado a lado.

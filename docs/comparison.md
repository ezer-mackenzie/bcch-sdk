# Comparación detallada: implementación legacy vs `src/` (nueva)

Esta página muestra comparaciones lado a lado (conceptuales y de código) entre la implementación legacy (código anterior usado como referencia) y sus contrapartes modernas en `src/`.

## 1) Inicialización y credenciales

- Legacy (anterior):

  - `get_credentials()` y `read_credentials(file)` eran funciones de I/O que preguntaban por `user` y `pass` o leían un archivo.

- Nueva — `src/bcch_sdk/types/auth.py` + `bcch_sdk/mappers/credentials.py`:

  - `InternalCredentials` es un `TypedDict` con `username` y `password`.
  - `CredentialsMapper.to_query_credentials` transforma un `InternalCredentials` a `{"user": ..., "pass": ...}`. ([bcch_sdk/mappers/credentials.py](https://github.com/ezer-mackenzie/bank-central-chile-sdk/blob/main/bcch_sdk/mappers/credentials.py))

**Impacto**: la nueva aproximación separa la lectura de credenciales de su transformación en parámetros HTTP; facilita testing y evita I/O oculto en librerías.

## 2) Cliente HTTP y transporte

- Legacy (anterior):

  - Uso directo de `requests.get` con `r = requests.get(self.URL, params=params)`.
  - Parseo inmediato `r.json()` y mapeo a `WSResponse`.

- Nueva — `src/bcch_sdk/clients/sync_client.py` / `src/bcch_sdk/clients/async_client.py`:

  - Uso de `httpx.Client`/`httpx.AsyncClient` con soporte para `Timeout` y `RetryTransport`.
  - Centralización de validación en `_validate_response`, conversiones a modelos `WebServiceResponse` vía `WebServiceResponse.model_validate(payload)`.

**Impacto**: mayor robustez en redes, control de tiempo de espera, reintentos configurables y mejor separación de responsabilidades.

## 3) Parámetros HTTP: nombres y mapeos

- Legacy (anterior): `params` incluye clave `"timeseries"` para la lista de series.
- Nueva: `ParameterBuilder.build_get_series_params` usa `timeseries` también (coincide), pero el API público de Python usa `time_series` como argumento y `TimeSeriesBuilder` normaliza entradas. Ver [src/bcch_sdk/builders/parameters.py](https://github.com/ezer-mackenzie/bank-central-chile-sdk/blob/main/src/bcch_sdk/builders/parameters.py) y [src/bcch_sdk/builders/time_series.py](https://github.com/ezer-mackenzie/bank-central-chile-sdk/blob/main/src/bcch_sdk/builders/time_series.py).

**Nota importante**: la diferencia entre `time_series` (argumento Python) y `timeseries` (clave HTTP) es una decisión intencional para mantener una API Python idiomática mientras se sigue la expectativa del backend.

## 4) Respuestas y modelos

- Legacy (anterior): `WSResponse`, `GSResponse`, `SSResponse` con métodos `to_series()` y `to_df()` (devuelven `pandas` objetos).
- Nueva: Pydantic models (`WebServiceResponse`, `Series`, `SerieInformation`, `ObservationSeries`) que usan `snake_case` y tipos concretos (`date`, `float`). Esto facilita validación, serialización y la escritura de mappers hacia `pandas` cuando sea necesario.

**Ejemplo de campo renombrado**: `Series['descripEsp']` (legacy) → `spanish_description` (nuevo); `Obs[indexDateString]` → `ObservationSeries.index_date`.

## 5) Errores y códigos de respuesta

- Legacy: comprobaba códigos (`Codigo`) y lanzaba excepciones legacy (`InvalidSeries`, `InvalidDate`, `InvalidCredentials`).
- Nueva: el cliente convierte la carga en un `WebServiceResponse` con `code` y `description`. Además lanza excepciones específicas para HTTP, parseo y negocio (códigos `-50`, `-1` traducidos a `InvalidSeriesException`, `InvalidDateException`).

**Recomendación**: capturar las excepciones específicas para poder distinguir problemas de red vs. datos.

## 6) Concurrencia y SDK de alto nivel

- Legacy: no hay API asíncrona nativa ni helpers de concurrencia.
- Nueva: `src/bcch_sdk/sdk/` expone `sync` y `async` SDKs y `src/bcch_sdk/sdk/concurrency.py` contiene helpers reutilizables (`run_in_threads`, `gather_async_tasks`).

**Beneficio**: usuarios pueden ejecutar múltiples consultas en paralelo sin reescribir el manejo de concurrencia.

## 7) Resumen de diferencias clave (tabla conceptual)

- API pública: `Session` (legacy) vs `BCChSyncClient`/`BCChAsyncClient` (nuevo)
- Transporte: `requests` vs `httpx + retries + timeout`
- Modelos: estructuras personalizadas + pandas vs Pydantic + mappers
- Errores: excepciones genéricas vs jerarquía específica

En las siguientes secciones de esta documentación encontrarás ejemplos concretos de migración, fragmentos de código y patrones recomendados.

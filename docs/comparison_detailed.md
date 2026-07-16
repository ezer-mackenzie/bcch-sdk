## Comparación profunda y guía práctica (implementación legacy → `src`)

Este documento es exhaustivo: explica las piezas de la implementación legacy (código anterior usado como referencia), su propósito y cómo se implementa cada responsabilidad en la nueva estructura `src/`. Incluye ejemplos de migración, puntos débiles del legacy y mejoras introducidas.

---

## Índice

- `credentials` y autenticación
- Manejo de parámetros y nombres (`timeseries` vs `time_series`)
- Peticiones HTTP y reintentos
- Validación y parseo de respuestas
- Modelado de datos
- Errores y jerarquía de excepciones
- Concurrencia y SDK
- Tests y cómo cubrir cambios
- Recomendaciones finales y checklist de migración

---

## `credentials` y autenticación

Legacy (anterior):

- `get_credentials()` — interacción con el usuario (input + getpass).
- `read_credentials(file)` — lee dos primeras líneas (user, pass) de un archivo.

Problemas del enfoque legacy:

- Mezcla de I/O con librería; las librerías no deben pedir input al usuario.
- Dificulta testing.

Nueva aproximación (`src/bcch_sdk/types/auth.py` + `bcch_sdk/mappers/credentials.py`):

- `InternalCredentials` es un `TypedDict` explícito.
- `CredentialsMapper.to_query_credentials` convierte `InternalCredentials` a `{"user": ..., "pass": ...}`.

Consejos de migración:

1. Evita cambiar código que lee credenciales (scripts CLI). Reemplaza su salida por un `InternalCredentials`.
2. Para tests, crea fixtures `{"username": "u", "password": "p"}` y prueba `CredentialsMapper`.

Código relacionado:

- `src/bcch_sdk/types/auth.py`
- `bcch_sdk/mappers/credentials.py`

---

## Manejo de parámetros y nombres (`timeseries` vs `time_series`)

Observación práctica:

- Legacy usaba la clave HTTP `timeseries`.
- La API Python en `src/` expone argumentos idiomáticos `time_series` y usa `ParameterBuilder` para producir `timeseries` en la query.

Ventajas de esta separación:

- API Python más clara (`time_series` es más legible).
- Centralización del mapeo en `ParameterBuilder` evita fugas de nombres en todo el código.

Archivo clave: `src/bcch_sdk/builders/parameters.py`

Ejemplo de uso:

```py
params = ParameterBuilder.build_get_series_params(creds, "SF43718")
# params["timeseries"] == "SF43718"
```

Recomendación: no cambiar la clave `timeseries` en las peticiones HTTP salvo que la API cambie; solo normaliza la interfaz Python.

---

## Peticiones HTTP y reintentos

Legacy:

- Usaba `requests.get` sin reintentos ni `Timeout` configurable.

Nueva implementación:

- `httpx.Client` / `httpx.AsyncClient` con `Timeout` y `RetryTransport`.
- Reintentos por defecto: 3, backoff 0.5 (configurable en `BaseClient.retry_policy`).

Impacto:

- Resiliencia frente a fallos transitorios de red.
- Mayor control del comportamiento en producción.

Recomendación operacional:

- Exponer `timeout` y `retry_policy` a usuarios avanzados a través de la configuración del cliente.

---

## Validación y parseo de respuestas

Legacy:

- Parseo directo `r.json()` y mapeo a `WSResponse`.

Nueva:

- `_validate_response` centraliza:
  - `raise_for_status()` con mapeo a `WebServiceResponseException`.
  - `json()` parse con captura de `ValueError` → `ResponseParseException`.
  - Validación a Pydantic `WebServiceResponse.model_validate(payload)`.

Beneficios:

- Errores más claros y fáciles de capturar en el cliente que consume el SDK.

---

## Modelado de datos

Legacy: estructuras simples y `pandas` helpers dentro de `WSResponse`.

Nuevo: Pydantic models con nombres descriptivos y tipos precisos:

- `Series` → `id`, `spanish_description`, `english_description`, `observations`.
- `ObservationSeries` → `index_date` (date), `value` (float), `status_code`.

Consecuencia: los consumidores pueden trabajar con objetos tipados y convertir a DataFrame sólo cuando lo necesiten, evitando la dependencia inmediata a `pandas`.

---

## Errores y jerarquía de excepciones

Legacy: excepciones planas (`InvalidSeries`, `InvalidCredentials`, ...).

Nuevo: jerarquía que distingue:

- Errores de transporte (`TransportException`).
- Errores de parseo (`ResponseParseException`).
- Errores de negocio (`InvalidCredentialsException`, `InvalidSeriesException`, ...).

Recomendación de manejo en aplicaciones:

```py
try:
    resp = client.get_series(...)
except InvalidCredentialsException:
    # pedir login o abortar
except TransportException:
    # volver a intentar o avisar al usuario
except ResponseParseException:
    # aviso y reporte
```

---

## Concurrencia y SDK

La nueva estructura facilita:

- Ejecución paralela segura de consultas con helpers `run_in_threads` y `gather_async_tasks`.
- SDK `sync_sdk` y `async_sdk` exponen funciones convenientes para usuarios que sólo quieren obtener series sin manejar clientes directamente.

Ejemplo conceptual (paralelizar 10 series):

```py
from bcch_sdk.sdk.concurrency import run_in_threads
from bcch_sdk.sdk.sync_sdk import BCChSDK

sdk = BCChSDK.from_credentials(creds)
series = ["SF1","SF2",...]
results = run_in_threads(lambda s: sdk.get_series(s), series)
```

---

## Tests y cómo cubrir cambios

Recomendación de librerías:

- `pytest` para tests generales.
- `respx` para mockear `httpx` en tests sync/async.

Casos de prueba esenciales:

- `ParameterBuilder.build_get_series_params` con combinaciones de `first_date`/`last_date` y tipos.
- `TimeSeriesBuilder.to_list` con strings, listas, dicts y errores.
- Clientes `get_series`/`search_series` simulando códigos backend (p.ej. `-50`, `-1`, `-5`).

---

## Recomendaciones finales y checklist para migración

1. Reemplazar `Session` por `BCChSyncClient` o `BCChAsyncClient`.
2. Pasar credenciales como `InternalCredentials` (evitar I/O en librería).
3. Actualizar excepciones capturadas en el código consumidor.
4. Añadir tests que cubran mapeos de parámetros y respuesta.
5. Revisar puntos de integración que dependan de `pandas` si ahora se usan modelos Pydantic.

---

Si quieres, puedo generar ejemplos de migración automáticos (scripts) que tomen fragmentos del código legacy y produzcan el equivalente usando `src/`.

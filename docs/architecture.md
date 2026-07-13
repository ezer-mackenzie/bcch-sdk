# Arquitectura y Diseño

Esta sección describe la organización del código, decisiones de diseño y patrones usados en la reimplementación.

## Principales paquetes en `src/`

- `clients/`: clientes HTTP sync y async, con gestión de `Timeout` y `RetryTransport`.
- `builders/`: funciones puras que construyen parámetros, normalizan fechas y series.
- `mappers/`: adaptadores entre `Internal` y `Query` representations o para transformar payloads a objetos/DF.
- `models/`: modelos Pydantic que describen respuestas y sub-objetos con nombres idiomáticos.
- `sdk/`: capa pública (convenience) que utiliza clientes, builders y concurrency helpers para ofrecer una API simple.

## Diseño de transportabilidad

- Separación de responsabilidades: los clientes se encargan únicamente de transporte y validación de respuestas; los mappers y builders se encargan de la transformación de datos.
- Uso de `httpx` para permitir sync y async con paridad de comportamientos.

## Logging y Telemetría

- Cada módulo define `logger = logging.getLogger(__name__)` y emite `debug/info/warning/error` apropiadamente.
- No hay handlers globales en la biblioteca — el consumidor configura logging.

## Timeout y reintentos

- `BCChConfig` y `BaseClient` exponen `Timeout` y `Retry` configurables.
- Valores por defecto: timeout 10s y retry total 3 con backoff 0.5.

## Concurrencia

- `src/sdk/concurrency.py` exporta `run_in_threads` y `gather_async_tasks` para evitar duplicación de patrones concurrency.

## Modelos y nomenclatura

- Los modelos Pydantic usan `snake_case` y nombres explícitos: `spanish_description`, `english_description`, `index_date`, `value`.
- Esto simplifica el mapping desde el payload JSON original y facilita el uso desde código Python.

# Roadmap

Este roadmap separa lo que falta para declarar `1.0.0` de las mejoras que conviene dejar para después de estabilizar la API.

## Antes de 0.9.0

- Validar que CI instala el wheel en un entorno limpio.
- Mantener `pandas` y `polars` como dependencias runtime obligatorias.
- Mantener `SerieInformation` como alias compatible de `SeriesInformation`.
- Revisar que los ejemplos de MkDocs usen solamente imports públicos.
- Confirmar que `README.md`, `CHANGELOG.md` y la referencia de API describen el mismo contrato.

## 0.9.0 Release Candidate

`0.9.0` debe funcionar como candidata final antes de `1.0.0`.

Validaciones esperadas:

- `poetry check`
- `poetry run ruff check .`
- `poetry run pytest -q`
- `poetry run pytest -q -m benchmark --benchmark-disable`
- `poetry run mkdocs build --strict`
- `poetry build`
- instalación del wheel en un entorno limpio

El objetivo de `0.9.0` es encontrar problemas de empaquetado, documentación o API pública antes de congelar compatibilidad.

## 1.0.0

La versión `1.0.0` debe congelar:

- Imports públicos desde `bcch_sdk`.
- Excepciones públicas.
- Modelos públicos de respuesta.
- Contrato de DataFrames.
- Política de dependencias runtime.
- Flujo de release con tags y build validado.

## Post 1.0.0

Estas mejoras son valiosas, pero no deberían bloquear `1.0.0`.

### Cache opcional

El cache debe ser opt-in, no comportamiento por defecto.

Motivos:

- Las series económicas pueden corregirse o actualizarse.
- Un TTL incorrecto puede entregar datos vencidos.
- Las credenciales viajan en parámetros de request y no deben filtrarse en claves de cache visibles.
- La API pública de cache necesita diseño propio para no romper compatibilidad después.

Diseño recomendado:

- `cache=None` por defecto.
- Backend enchufable, por ejemplo `MemoryCache`.
- TTL explícito configurado por el usuario.
- Claves de cache que excluyan credenciales en texto plano.
- Métodos para limpiar cache.
- Tests para sync y async.

Ejemplo conceptual futuro:

```python
from datetime import timedelta

from bcch_sdk import BCChConfig, BCChSyncSDK
from bcch_sdk.cache import MemoryCache

sdk = BCChSyncSDK(
    configuration=BCChConfig(
        credentials={"username": "tu_usuario", "password": "tu_password"}
    ),
    cache=MemoryCache(ttl=timedelta(minutes=30)),
)
```

### Dependencias DataFrame opcionales

Separar `pandas` y `polars` en extras puede reducir peso de instalación, pero requiere rediseñar imports, errores y contrato de retorno.

Posibles extras futuros:

- `bcch-sdk[pandas]`
- `bcch-sdk[polars]`
- `bcch-sdk[dataframe]`

### Integraciones adicionales

- Exportar a CSV/Parquet desde helpers opcionales.
- Documentar recetas para notebooks.
- Agregar ejemplos con variables de entorno para credenciales.
- Agregar tests de contrato con payloads reales anonimizados.

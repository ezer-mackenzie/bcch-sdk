# Roadmap

`bcch-sdk` está orientado a estabilidad de API en la serie `1.x`. Esta página documenta qué queda congelado y qué mejoras pueden evaluarse en versiones futuras.

## Estable en 1.x

La serie `1.x` mantiene estable:

- Imports públicos desde `bcch_sdk`.
- Excepciones públicas.
- Modelos públicos de respuesta.
- Contrato de DataFrames.
- Dependencias runtime principales.
- Flujo de release con tags, build y validación de wheel.

## Cambios compatibles

Pueden entrar en versiones menores o patch:

- Nuevos ejemplos de documentación.
- Nuevos modelos o helpers públicos que no rompan imports existentes.
- Mejoras internas de transporte, logging o parsing.
- Más cobertura de tests.
- Correcciones de errores.

## Cambios reservados para versión mayor

Requieren una versión mayor:

- Remover imports públicos.
- Cambiar tipos de retorno de métodos públicos.
- Hacer opcionales dependencias que hoy forman parte del contrato principal.
- Cambiar la jerarquía pública de excepciones de forma incompatible.

## Cache opcional

El cache sigue siendo una mejora futura recomendable, pero debe ser opt-in.

Motivos:

- Las series económicas pueden corregirse o actualizarse.
- Un TTL incorrecto puede entregar datos vencidos.
- Las credenciales viajan en parámetros de request y no deben filtrarse en claves de cache visibles.
- La API pública de cache necesita diseño propio para preservar compatibilidad.

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

## Dependencias DataFrame opcionales

Separar `pandas` y `polars` en extras puede reducir peso de instalación, pero requiere rediseñar imports, errores y contrato de retorno.

Posibles extras futuros:

- `bcch-sdk[pandas]`
- `bcch-sdk[polars]`
- `bcch-sdk[dataframe]`

## Integraciones adicionales

- Exportar a CSV/Parquet desde helpers opcionales.
- Documentar recetas para notebooks.
- Agregar ejemplos con variables de entorno para credenciales.
- Agregar tests de contrato con payloads reales anonimizados.

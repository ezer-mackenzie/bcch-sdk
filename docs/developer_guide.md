# Developer Guide

Esta sección está dirigida a contribuyentes y desarrolladores que modifican el SDK.

## Estructura del repositorio

- `src/` — código fuente principal.
- Implementación legacy: el código anterior (usado como referencia durante el desarrollo) puede haber sido removido del repositorio; la nueva fuente está en `src/`.
- `docs/` — documentación MkDocs.

## Formato de código y linting

- Recomendado: `ruff` para linting y `black`/`ruff format` para formateo (si usas `python` 3.14, ajusta las versiones).

## Tests

- Añadir pruebas unitarias para builders, mappers y clientes. Para clientes, usar `respx` (sync/async) para mockear respuestas `httpx`.

Ejemplo de test para `ParameterBuilder` (esqueleto):

```python
def test_build_get_series_params_minimal():
    creds = {"username": "u","password": "p"}
    params = ParameterBuilder.build_get_series_params(creds, "SF43718")
    assert params["timeseries"] == "SF43718"
```

## Cómo ejecutar la documentación localmente

Instala `mkdocs` y el tema `material` localmente (no lo ejecutaré aquí por petición tuya). Comandos de referencia:

```bash
python -m pip install mkdocs mkdocs-material
mkdocs serve
```

## Contribuciones y Pull Requests

- Mantener la API pública estable; los cambios de breaking deben ir con bump de versión y changelog.
- Añadir tests para cada feature nueva y documento de migración si el cambio afecta la API pública.

# DataFrames

El SDK considera `pandas` y `polars` parte del contrato principal. Por eso ambas librerías son dependencias runtime obligatorias en la serie estable `1.x`.

## Respuesta por defecto

Por defecto, `get_series` y `search_series` retornan `polars.DataFrame`.

```python
from bcch_sdk import BCChConfig, BCChSyncSDK

sdk = BCChSyncSDK(
    configuration=BCChConfig(
        credentials={"username": "tu_usuario", "password": "tu_password"}
    )
)

frames = sdk.get_series("SF43718")

print(type(frames[0]))
```

## Respuesta con pandas

Usa `polars_response=False` para solicitar `pandas.DataFrame`.

```python
frames = sdk.get_series(
    "SF43718",
    first_date="2024-01-01",
    last_date="2024-01-31",
    polars_response=False,
)

print(type(frames[0]))
```

La misma opción está disponible en `search_series`.

```python
from bcch_sdk import Frequency

catalog = sdk.search_series(
    Frequency.MONTHLY,
    polars_response=False,
)
```

## Múltiples series

Cuando pides varias series, el SDK retorna una lista de DataFrames en el mismo orden solicitado.

```python
frames = sdk.get_series(
    ["SF43718", "F073.TCO.PRE.Z.D"],
    first_date="2024-01-01",
    last_date="2024-01-31",
)

for frame in frames:
    print(frame.columns)
```

También puedes pasar una cadena separada por comas.

```python
frames = sdk.get_series("SF43718,F073.TCO.PRE.Z.D")
```

## Forma de los datos

Para una serie, el DataFrame tiene:

- `date`: fecha de observación.
- una columna con el identificador de la serie.

Ejemplo conceptual:

| date | SF43718 |
| --- | ---: |
| 2024-01-01 | 1.0 |
| 2024-01-02 | 1.1 |

## Decisión de dependencias

Separar `pandas` y `polars` en extras opcionales queda reservado para una versión mayor futura. Ese cambio requiere rediseñar imports, errores y contratos de respuesta.

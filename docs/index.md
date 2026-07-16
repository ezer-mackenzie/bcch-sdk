# Banco Central Chile SDK

Bienvenido a la documentación del SDK para acceder al SieteRestWS del Banco Central de Chile.

`bcch-sdk` entrega clientes sincrónicos y asíncronos, manejo de errores tipado, reintentos HTTP y respuestas en `polars.DataFrame` o `pandas.DataFrame`.

## Por dónde empezar

- [Quickstart](quickstart.md): instalación, credenciales y primeras consultas.
- [DataFrames](dataframes.md): forma de las respuestas y elección entre `polars` y `pandas`.
- [Ejemplos de uso](usage.md): patrones comunes con SDKs y clientes directos.
- [Referencia de API](api_reference.md): imports públicos, modelos, errores y versionado.
- [Release Checklist](release_checklist.md): pasos para publicar versiones de forma repetible.

## Qué cubre esta documentación

- Introducción y visión general del SDK.
- Guía de migración desde la implementación legacy.
- Referencia de la API pública del SDK (sync / async).
- Arquitectura interna y decisiones de diseño.
- Ejemplos de uso y patrones recomendados.

## Contrato actual

- Paquete importable: `bcch_sdk`.
- Versión pública: `bcch_sdk.__version__`.
- Dependencias DataFrame obligatorias: `pandas` y `polars`.
- Compatibilidad en la serie `0.x`: los cambios incompatibles deben subir versión menor.

La documentación está escrita en español para acompañar el contexto del Banco Central de Chile y los ejemplos locales.

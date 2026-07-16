# Release Checklist

Esta checklist resume el flujo recomendado antes de publicar una versión.

## Antes de cambiar la versión

- Revisar que `git status --short` esté limpio o que los cambios pendientes pertenezcan al release.
- Confirmar el siguiente número de versión según semver.
- Actualizar `CHANGELOG.md` con fecha, cambios y notas de compatibilidad.
- Actualizar documentación si cambia cualquier import, comportamiento o dependencia.

## Validación local

```bash
poetry check
poetry run ruff check .
poetry run pytest -q
poetry run pytest -q -m benchmark --benchmark-disable
poetry run mkdocs build --strict
poetry build
```

## Validación del wheel

El wheel debe poder instalarse en un entorno limpio.

```bash
python -m venv /tmp/bcch-sdk-wheel-test
/tmp/bcch-sdk-wheel-test/bin/python -m pip install --upgrade pip
/tmp/bcch-sdk-wheel-test/bin/python -m pip install dist/*.whl
/tmp/bcch-sdk-wheel-test/bin/python -c "import bcch_sdk; print(bcch_sdk.__version__)"
```

## Commit y tag

```bash
git add -A
git commit -m "chore: release vX.Y.Z"
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

## Push

```bash
git push origin main
git push origin vX.Y.Z
```

Si necesitas subir varios tags:

```bash
git push origin v0.3.0 v0.4.0 v0.5.0 v0.6.0 v0.7.0 v0.8.0 v0.8.1 v0.9.0
```

## Publicación

El workflow de publicación se ejecuta cuando se publica un GitHub Release.

Antes de publicar el release:

- Confirmar que CI está verde para el commit taggeado.
- Confirmar que MkDocs construye con `--strict`.
- Revisar que el release de GitHub apunte al tag correcto.
- Copiar el resumen de `CHANGELOG.md` correspondiente a la versión.

## Criterio para 1.0.0

Publicar `1.0.0` solo cuando:

- La superficie pública de imports esté congelada.
- La jerarquía de excepciones esté documentada.
- Los modelos de respuesta públicos estén documentados.
- El wheel haya sido validado desde un entorno limpio.
- La CI ejecute lint, tests, build y validación de wheel.
- La documentación esté desplegable sin warnings.

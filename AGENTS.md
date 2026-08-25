# AGENTS.md

## Project overview

`bcch-sdk` is a typed Python 3.12+ client for the Banco Central de Chile
SieteRestWS API. Source code lives in `src/bcch_sdk`, tests in `tests`, and
MkDocs documentation in `docs`.

API responses are validated directly into the Pydantic models under `models`;
do not introduce a parallel DTO representation. Mappers are reserved for
transformations that produce a genuinely different representation, such as
query credentials or DataFrames.

Pandas and Polars are optional v2 extras. Keep imports lazy so the base package
and low-level clients remain usable without either DataFrame backend.

## Working agreements

- Keep public APIs typed and preserve synchronous and asynchronous behavior.
- Prefer focused changes; do not modify generated `dist/` or `site/` output.
- Never commit credentials or values from `.env`.
- Update tests and user-facing documentation when behavior changes.
- Preserve unrelated working-tree changes.

## Local validation

Install dependencies with `poetry install`. Before handing off a change, run
the checks relevant to it:

```bash
poetry run ruff check .
poetry run mypy
poetry run pytest -q
poetry build
poetry run mkdocs build --strict
```

The full test command excludes tests marked `benchmark` by default. Run them
explicitly with `poetry run pytest -m benchmark` when changing concurrency,
dataframe mapping, requests, or performance-sensitive code.

## CI and coverage

The main CI workflow lints, tests, builds, and validates the wheel. Its test
step creates `coverage.xml` and uploads it as the `coverage-report` artifact.
Only after that job succeeds, `.github/workflows/codecov.yml` downloads the
artifact and uploads it to Codecov using GitHub OIDC authentication. The caller
and reusable workflow must retain `id-token: write` permission.

## Commits

Use concise Conventional Commit-style subjects consistent with the history,
such as `feat:`, `fix:`, `test:`, `docs:`, and `ci:`. Do not amend, rebase,
force-push, or otherwise rewrite existing commits unless the user explicitly
requests it and the exact affected commits and trailers are known.

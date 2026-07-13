# Contributing to Banco Central Chile SDK

Thank you for your interest in contributing to this project. Contributions are welcome from everyone.

## How to contribute

1. Fork the repository.
2. Create a feature branch with a clear name.
3. Make your changes in a clean and focused way.
4. Open a pull request and describe the purpose of your change.

## Development workflow

- Use Python 3.14 or newer.
- Prefer `poetry install` to install dependencies from `pyproject.toml`.
- Keep the code compatible with the existing package structure.
- If you add or change behavior, include a short example or doc update.

## Code style

- Follow Python best practices and idiomatic naming.
- Keep functions small and focused.
- Use type hints consistently.
- Use `logging.getLogger(__name__)` for library logging.
- Avoid side effects at import time.

## Testing

- Add unit tests for bug fixes and new features.
- Keep tests readable and precise.
- Prefer direct validation of API behavior, error conditions, and expected output.

## Documentation

- Add or update `README.md` examples when public behavior changes.
- Keep API usage examples correct and minimal.

## Reporting issues

If you find a bug or have an enhancement request, open an issue with:

- a clear summary
- steps to reproduce
- expected and actual behavior
- relevant code snippets or configuration

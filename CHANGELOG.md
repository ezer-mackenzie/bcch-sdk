# Changelog

All notable changes to this project are documented here.

This project follows semantic versioning before `1.0.0` with the same discipline as stable releases: breaking import or API changes get a minor version bump, and compatible fixes get patch releases.

## [0.8.1] - 2026-07-16

### Fixed

- Replaced the remaining HTTP status logging TODO with module-level debug logging.

### Added

- Added a MkDocs roadmap page for `0.9.0`, `1.0.0`, and post-`1.0.0` improvements.
- Documented cache as a future opt-in feature rather than a pre-`1.0.0` requirement.

## [0.8.0] - 2026-07-16

### Added

- Added CI validation that installs the built wheel in a clean virtual environment and imports the public API.
- Added Quickstart documentation with sync, async, search, and error handling examples.
- Added DataFrames documentation covering `polars`, `pandas`, multiple series, and the dependency policy.
- Added a release checklist for local validation, wheel installation, tags, pushes, and PyPI publication.

### Changed

- Expanded MkDocs navigation and rewrote usage examples around the stable `bcch_sdk` public API.

## [0.7.0] - 2026-07-16

### Documented

- Confirmed `pandas` and `polars` remain mandatory runtime dependencies for the `0.x` and `1.0` release line.
- Documented that splitting DataFrame libraries into optional extras is deferred until after the stable API is established.

## [0.6.0] - 2026-07-16

### Added

- Added `SeriesInformation` as the preferred public model name for series metadata.
- Kept `SerieInformation` as a compatibility alias for the `0.x` series.

### Changed

- Updated public exports, type annotations, tests, and documentation to prefer `SeriesInformation`.

## [0.5.0] - 2026-07-16

### Added

- Added `bcch_sdk.__version__`.
- Exported common configuration, enum, model, and exception types from the package root.
- Exported common domain models from `bcch_sdk.models`.
- Added public API tests for stable imports, version metadata, model exports, and credentials exception compatibility.
- Documented the supported public import surface and internal modules.

## [0.4.0] - 2026-07-16

### Added

- Added PyPI metadata: license, keywords, project URLs, classifiers, and changelog link.
- Added sync and async client tests with `httpx.MockTransport`.
- Covered HTTP status errors, invalid credentials, invalid series, invalid dates, invalid search frequency, and successful response mapping.

## [0.3.0] - 2026-07-16

### Changed

- Renamed the import package from `src` to `bcch_sdk`.
- Updated package metadata so wheels and sdists publish `bcch_sdk` as the top-level package.
- Moved lint, test, benchmark, and documentation tools out of runtime dependencies.
- Excluded benchmarks from the default pytest run.
- Updated README and documentation examples to use `bcch_sdk` imports.

### Fixed

- Reopened sync and async context-managed HTTP clients with retry transport enabled.
- Accepted Banco Central API payloads that include only `Series` or only `SeriesInfos`.
- Used `InvalidCredentialsException` as the primary credentials error while preserving `InvalidsCredentialsException` as a compatibility alias.

### Added

- CI steps for linting, tests, and package builds.
- Public API tests for package exports.
- Response mapping tests for series-only and search-only payloads.

## 1.0.0 Release Path

The next releases should focus on reducing user-facing risk before declaring the API stable.

### 0.9.0

- Publish as a release candidate.
- Run the full test suite, benchmark suite, strict docs build, and package build from a clean environment.
- Validate installation from the built wheel in a fresh virtual environment.

### 1.0.0

- Mark the package as stable once the public import surface, error hierarchy, response models, and release pipeline are frozen.

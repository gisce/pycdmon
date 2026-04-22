# Changelog

All notable changes to this project will be documented in this file.

Releases are managed by Python Semantic Release.

## Unreleased

### Fixed

- Release workflow now uploads built distributions to PyPI with `twine` when `PYPI_TOKEN` (or fallback `PYPI_MASTER_TOKEN`) is configured.

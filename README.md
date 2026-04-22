# pycdmon

Professional Python client for cdmon Domains & DNS API.

- Full endpoint coverage for core domain + DNS operations
- Sync and async clients
- Typed payload helpers
- Clean error model (`CdmonApiError`, `CdmonTransportError`)
- Designed for human and agent workflows

## Install

```bash
pip install pycdmon
```

Or from source:

```bash
pip install -e .[dev]
```

## Quickstart

```python
from pycdmon import CdmonDomainsClient

with CdmonDomainsClient(api_key="YOUR_API_KEY") as client:
    result = client.check("example.com")
    print(result["data"]["result"]["available"])
```

## Async usage

```python
import asyncio
from pycdmon import AsyncCdmonDomainsClient

async def main() -> None:
    async with AsyncCdmonDomainsClient(api_key="YOUR_API_KEY") as client:
        print(await client.check("example.com"))

asyncio.run(main())
```

## CLI (`cdmon`)

After installation, a `cdmon` command is available:

```bash
export CDMON_API_KEY="your_api_key"
cdmon check example.com
cdmon info example.com
cdmon authcode example.com
cdmon renew example.com --period 1
cdmon transfer example.com 'AUTH-CODE'
cdmon dns-records example.com
cdmon dns-create example.com --host @ --type A --destination 1.2.3.4 --ttl 900
cdmon dns-delete example.com --host @ --type A
cdmon price com create
cdmon periods com renew
cdmon balance
cdmon status check
```

You can also pass the key inline:

```bash
cdmon --api-key "$CDMON_API_KEY" check example.com
```

## Supported operations

- Endpoint status: `status`
- Domains: `check`, `info`, `authcode`, `list_domains`, `register`, `renew`, `transfer`, `restore`
- Domain options: `set_block`, `set_whois_private`, `set_dnssec`, `modify_contact`
- DNS: `set_nameservers`, `get_dns_records`, `create_dns_record`, `edit_dns_record`, `delete_dns_record`, `send_dns_key`
- Billing/meta: `get_price`, `get_periods`, `balance`
- Auto-renewal: `get_autorenewal`, `manage_autorenewal`

## Error handling

```python
from pycdmon import CdmonApiError, CdmonDomainsClient

try:
    with CdmonDomainsClient(api_key="...") as client:
        client.transfer("example.com", "wrong-authcode")
except CdmonApiError as exc:
    print(exc.status_code, exc.message)
    print(exc.payload)
```

## Agent-friendly repo workflow

This repository is structured to be easy for coding agents:

- `src/` strict package layout
- `tests/` isolated, deterministic HTTP tests
- `examples/` runnable snippets
- `docs/` implementation and API notes
- CI with lint + tests

Suggested autonomous loop for agents:

1. Add/update behavior in `src/pycdmon`
2. Add/adjust tests in `tests/`
3. Run `ruff check . && pytest`
4. Keep commits small and descriptive

## Releases

This repository supports automatic releases from `main` using **Python Semantic Release** and Conventional Commits.

### Why this approach

This is a Python package, so the release automation is now Python-native:

- no `package.json`
- no Node-based `semantic-release`
- versioning is configured in `pyproject.toml`
- the workflow uses `python-semantic-release`, `build`, and optional `twine`

Conventional Commits are still used, but they are only the **input convention** for deciding the version bump. They do not imply a Node/npm release stack.

### How it works

- merge changes into `main`
- GitHub Actions runs validation (`ruff check .` and `pytest`)
- `python-semantic-release` inspects commit messages since the last tag
- if a release is warranted, it will:
  - determine the next version
  - update `pyproject.toml`
  - create the release commit and tag
  - publish the GitHub Release
- if `PYPI_TOKEN` is defined in repository secrets, the workflow also publishes to PyPI
- if `PYPI_TOKEN` is not defined but `PYPI_MASTER_TOKEN` exists, the workflow falls back to that token for PyPI publication

### Commit conventions

Use Conventional Commits so release automation can infer version bumps:

- `fix:` -> patch release
- `feat:` -> minor release
- `feat!:` or any commit with `BREAKING CHANGE:` -> major release
- `docs:`, `test:`, `chore:` -> no release by default

Example:

```bash
git commit -m "fix: handle TXT DNS records with value field"
```

### Notes

- The release workflow only runs on pushes to `main`.
- The repository must allow GitHub Actions to push release commits and tags using `GITHUB_TOKEN`.
- If branch protection is strict, make sure it still permits the release workflow to push the generated release commit.
- If neither `PYPI_TOKEN` nor `PYPI_MASTER_TOKEN` is present, the workflow still creates the Git tag and GitHub Release and skips the PyPI upload.

## API reference source

Based on cdmon official API docs:
https://apidedominioscat.docs.apiary.io/#introduction/endpoints-disponibles

## License

MIT

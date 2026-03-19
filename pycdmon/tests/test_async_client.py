from __future__ import annotations

import asyncio

import httpx
import pytest

from pycdmon import AsyncCdmonDomainsClient, CdmonApiError


def test_async_balance_success() -> None:
    async def run() -> None:
        transport = httpx.MockTransport(
            lambda _req: httpx.Response(200, json={"status": "ok", "data": {"amount": "12.34"}})
        )
        client = httpx.AsyncClient(
            base_url="https://api-domains.cdmon.services/api-domains/",
            headers={
                "apikey": "x",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            transport=transport,
        )

        sdk = AsyncCdmonDomainsClient(api_key="x", client=client)
        response = await sdk.balance()
        assert response["status"] == "ok"
        assert response["data"]["amount"] == "12.34"

    asyncio.run(run())


def test_async_ko_status_raises_api_error() -> None:
    async def run() -> None:
        transport = httpx.MockTransport(
            lambda _req: httpx.Response(200, json={"status": "ko", "data": {"msg": "bad auth"}})
        )
        client = httpx.AsyncClient(
            base_url="https://api-domains.cdmon.services/api-domains/",
            headers={
                "apikey": "x",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            transport=transport,
        )

        sdk = AsyncCdmonDomainsClient(api_key="x", client=client)
        with pytest.raises(CdmonApiError) as exc:
            await sdk.get_autorenewal("example.com")

        assert exc.value.status_code == 200
        assert "bad auth" in str(exc.value)

    asyncio.run(run())

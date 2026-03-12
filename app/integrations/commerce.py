from __future__ import annotations

from typing import Any

import httpx


class CommerceApiClient:
    """Generic HTTP client for external commerce channels."""

    def __init__(self, base_url: str, api_key: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def fetch_orders(self) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=20) as client:
            response = await client.get("/orders", headers=self._headers())
            response.raise_for_status()
            payload = response.json()
            if isinstance(payload, list):
                return payload
            return payload.get("orders", [])

    async def push_inventory(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=20) as client:
            response = await client.post("/inventory", json={"items": rows}, headers=self._headers())
            response.raise_for_status()
            return response.json()

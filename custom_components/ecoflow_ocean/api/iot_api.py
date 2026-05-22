"""EcoFlow IoT Developer API client (async)."""

from __future__ import annotations

import hashlib
import hmac
import logging
import random
import time
from typing import Any

import aiohttp

from .const import IOT_CERT_PATH, IOT_DEVICE_LIST_PATH, IOT_MIN_FETCH_INTERVAL_S

_LOGGER = logging.getLogger(__name__)


class IoTApiClient:
    """HMAC-SHA256 signed client for certification and device list endpoints."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        access_key: str,
        secret_key: str,
        base_url: str,
    ) -> None:
        self._session = session
        self._access_key = access_key.strip()
        self._secret_key = secret_key.strip()
        self._base_url = base_url.rstrip("/")
        self._cached: dict[str, Any] | None = None
        self._last_fetch_ts: float = 0.0

    @staticmethod
    def sign(params: dict[str, str], secret_key: str) -> str:
        """HMAC-SHA256 over alphabetically sorted key=value pairs."""
        sorted_params = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
        return hmac.new(
            secret_key.encode(),
            sorted_params.encode(),
            hashlib.sha256,
        ).hexdigest()

    def _make_signed_headers(self) -> dict[str, str]:
        nonce = str(random.randint(100000, 999999))
        timestamp = str(int(time.time() * 1000))
        params = {
            "accessKey": self._access_key,
            "nonce": nonce,
            "timestamp": timestamp,
        }
        sig = self.sign(params, self._secret_key)
        return {
            "accessKey": self._access_key,
            "nonce": nonce,
            "timestamp": timestamp,
            "sign": sig,
        }

    async def get_mqtt_credentials(self) -> dict[str, Any] | None:
        """Validate keys and return MQTT certificate credentials."""
        if self._cached is not None:
            return self._cached
        return await self._fetch_credentials()

    async def get_device_list(self) -> list[dict[str, Any]] | None:
        """Return devices bound to the developer application."""
        url = f"{self._base_url}{IOT_DEVICE_LIST_PATH}"
        headers = self._make_signed_headers()
        try:
            async with self._session.get(
                url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                resp.raise_for_status()
                body = await resp.json()
                code = str(body.get("code"))
                if code != "0":
                    _LOGGER.warning(
                        "Device list failed — code=%s message=%s (%s)",
                        code,
                        body.get("message"),
                        self._base_url,
                    )
                    return None
                data = body.get("data")
                if not data:
                    return None
                return data if isinstance(data, list) else None
        except (aiohttp.ClientError, TimeoutError) as exc:
            _LOGGER.warning("Device list request failed: %s", exc)
            return None

    async def _fetch_credentials(self) -> dict[str, Any] | None:
        now = time.monotonic()
        if (now - self._last_fetch_ts) < IOT_MIN_FETCH_INTERVAL_S and self._cached:
            return self._cached

        if not self._access_key or not self._secret_key:
            return None

        self._last_fetch_ts = now
        url = f"{self._base_url}{IOT_CERT_PATH}"
        headers = self._make_signed_headers()
        try:
            async with self._session.get(
                url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                resp.raise_for_status()
                body = await resp.json()
                code = str(body.get("code"))
                if code != "0":
                    _LOGGER.warning(
                        "Certification failed — code=%s message=%s (%s)",
                        code,
                        body.get("message"),
                        self._base_url,
                    )
                    return None
                data = body.get("data")
                if not data:
                    return None
                self._cached = data
                return data
        except (aiohttp.ClientError, TimeoutError) as exc:
            _LOGGER.warning("Certification request failed: %s", exc)
            return None

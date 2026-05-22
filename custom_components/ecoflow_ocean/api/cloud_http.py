"""EcoFlow HTTP quota client for GET /iot-open/sign/device/quota/all."""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import logging
import random
import time
from typing import Any

import aiohttp

from .const import HTTP_RETRIES, HTTP_RETRY_BACKOFF_S, IOT_QUOTA_ALL_PATH, QUOTA_HTTP_MIN_INTERVAL_S

_LOGGER = logging.getLogger(__name__)


class EcoFlowHTTPQuota:
    """Signed async client for PowerOcean quota polling."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        access_key: str,
        secret_key: str,
        device_sn: str,
        base_url: str,
        min_interval: float = QUOTA_HTTP_MIN_INTERVAL_S,
    ) -> None:
        self._session = session
        self._access_key = access_key
        self._secret_key = secret_key
        self._device_sn = device_sn
        self._base_url = base_url.rstrip("/")
        self._min_interval = min_interval
        self._last_call: float = 0.0
        self.last_error_code: str | None = None

    async def get_quota_all(self) -> dict[str, Any] | None:
        """Fetch all quota fields for the configured serial number."""
        if not self._check_rate_limit():
            return None
        url = f"{self._base_url}{IOT_QUOTA_ALL_PATH}"
        return await self._request_with_retry(url, query={"sn": self._device_sn})

    def _check_rate_limit(self) -> bool:
        now = time.monotonic()
        if now - self._last_call < self._min_interval:
            return False
        self._last_call = now
        return True

    def _sign_headers(self, params_dict: dict[str, Any]) -> dict[str, str]:
        ts = str(int(time.time() * 1000))
        nonce = str(random.randint(100000, 999999))
        flat = self._flatten(params_dict)
        flat.sort(key=lambda kv: kv[0])
        kv_string = "&".join(f"{k}={v}" for k, v in flat)
        tail = f"accessKey={self._access_key}&nonce={nonce}&timestamp={ts}"
        sign_string = (kv_string + "&" if kv_string else "") + tail
        sig = hmac.new(
            self._secret_key.encode("utf-8"),
            sign_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return {
            "accessKey": self._access_key,
            "nonce": nonce,
            "timestamp": ts,
            "sign": sig,
        }

    @staticmethod
    def _flatten(obj: Any, parent: str = "") -> list[tuple[str, str]]:
        items: list[tuple[str, str]] = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f"{parent}.{k}" if parent else k
                items.extend(EcoFlowHTTPQuota._flatten(v, new_key))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                new_key = f"{parent}[{i}]"
                items.extend(EcoFlowHTTPQuota._flatten(v, new_key))
        else:
            items.append((parent, str(obj)))
        return items

    class _RetryableAPIError(Exception):
        pass

    async def _request_with_retry(
        self, url: str, *, query: dict[str, str]
    ) -> dict[str, Any] | None:
        for attempt in range(1, HTTP_RETRIES + 1):
            try:
                headers = self._sign_headers(query)
                timeout = aiohttp.ClientTimeout(total=15)
                async with self._session.get(
                    url, headers=headers, params=query, timeout=timeout
                ) as resp:
                    data = await resp.json()
                    code = str(data.get("code"))
                    if resp.ok and code == "0":
                        self.last_error_code = None
                        payload = data.get("data")
                        return payload if isinstance(payload, dict) else {}
                    if code == "8521":
                        raise self._RetryableAPIError(code)
                    if code == "1006":
                        self.last_error_code = "1006"
                        _LOGGER.warning(
                            "Device %s not linked to API key — bind it at developer.ecoflow.com",
                            self._device_sn,
                        )
                        return None
                    self.last_error_code = code
                    _LOGGER.warning(
                        "Quota error code=%s message=%s sn=%s",
                        code,
                        data.get("message"),
                        self._device_sn,
                    )
                    return None
            except (aiohttp.ClientError, TimeoutError, self._RetryableAPIError) as exc:
                if attempt >= HTTP_RETRIES:
                    _LOGGER.error("Quota request failed for %s: %s", self._device_sn, exc)
                elif attempt < HTTP_RETRIES:
                    await asyncio.sleep(HTTP_RETRY_BACKOFF_S)
        self.last_error_code = "network"
        return None

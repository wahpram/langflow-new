# infrastructure/webhook_client.py
import httpx
from google.api_core.exceptions import MethodNotAllowed
from httpx import HTTPStatusError

from api.domain.entities import OutboundEvent

import httpx
from api.domain.entities import OutboundEvent

class WebhookClient:
    async def send(self, url: str, event: OutboundEvent):
        body = event.model_dump(mode="json")
        headers = {"Content-Type": "application/json"}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, json=body, headers=headers)
            resp.raise_for_status()  # biarkan meledak kalau 4xx/5xx
            try:
                return resp.json()
            except Exception:
                return {"text": resp.text}
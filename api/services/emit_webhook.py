# api/services/emit.py
from fastapi import HTTPException
from httpx import HTTPStatusError

from api.domain.entities import OutboundEvent
from api.infrastructure.webhook_client import WebhookClient
from api.usecases.emit_event import EmitEventUseCase
from api.core.langflow import get_langflow_webhook_url

async def emit_to_langflow(event: OutboundEvent) -> dict:
    """
    Centralized helper untuk mengirim event ke Langflow Webhook.
    - Membuat client & usecase
    - Mendapatkan URL webhook dari satu sumber
    - Menangani error mapping ke HTTPException
    """
    client = WebhookClient()
    usecase = EmitEventUseCase(client)
    url = get_langflow_webhook_url()

    try:
        result = await usecase(url=url, event=event)
        return {"status": "sent", "langflow_response": result}
    except HTTPStatusError as e:
        # propagate status Langflow ke caller
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

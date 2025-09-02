from api.domain.entities import OutboundEvent
from api.infrastructure.webhook_client import WebhookClient


class EmitEventUseCase:
    def __init__(self, client: WebhookClient):
        self.client = client

    async def __call__(self, url: str, event: OutboundEvent):
        await self.client.send(url, event)
import uuid
from datetime import datetime

from fastapi import FastAPI, APIRouter, HTTPException
from httpx import HTTPStatusError

from api.domain.entities import OutboundEvent
from api.infrastructure.webhook_client import WebhookClient
from api.usecases.emit_event import EmitEventUseCase
from api.core.configs import project_settings

app = FastAPI(title=project_settings.APP_NAME)

router = APIRouter(
    prefix="/api/v1",
)



@app.post("/emit")
async def emit(data: dict):
    event = OutboundEvent(
        type="please.rename.me",
        data=data,
        id=str(uuid.uuid4()),
        occurred_at=datetime.utcnow(),
    )
    client = WebhookClient()
    usecase = EmitEventUseCase(client)
    try:
        result = await usecase(project_settings.LANGFLOW_BASE_URL + "/api/v1/webhook/", event)
        return {"status": "sent", "langflow_response": result}
    except HTTPStatusError as e:
        status = e.response.status_code
        detail = e.response.text
        raise HTTPException(status_code=status, detail=detail)

@app.get("/health")
async def health():
    return {"status": "ok"}


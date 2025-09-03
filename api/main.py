import uuid
from datetime import datetime

from fastapi import FastAPI, APIRouter, HTTPException
from httpx import HTTPStatusError

from api.domain.entities import OutboundEvent
from api.infrastructure.webhook_client import WebhookClient
from api.usecases.emit_event import EmitEventUseCase
from api.core.configs import project_settings as settings

app = FastAPI(title=settings.APP_NAME)

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
    url = f"{settings.LANGFW_BASE_URL}:{settings.LANGFW_PORT}/api/v1/webhook/{settings.LANGFW_PROJECT_ID}"
    try:
        result = await usecase(
            url=url,
            event=event
        )
        return {"status": "sent", "langflow_response": result}
    except HTTPStatusError as e:
        status = e.response.status_code
        detail = e.response.text
        raise HTTPException(status_code=status, detail=detail)

@app.get("/health")
async def health():
    return {"status": "ok"}

#TODO: Route to organization search
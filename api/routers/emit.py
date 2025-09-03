import uuid
from datetime import datetime
from fastapi import APIRouter
from api.domain.entities import OutboundEvent
from api.services.emit_webhook import emit_to_langflow

router = APIRouter(tags=["emit"])

@router.post("/emit")
async def emit(data: dict):
    event = OutboundEvent(
        type="please.rename.me",
        data=data,
        id=str(uuid.uuid4()),
        occurred_at=datetime.utcnow(),
    )
    return await emit_to_langflow(event)


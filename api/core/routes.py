# import uuid
# from datetime import datetime
#
# from fastapi import APIRouter
#
# from api.core.configs import project_settings
# from api.domain.entities import OutboundEvent
# from api.infrastructure.webhook_client import WebhookClient
# from api.main import app
# from api.usecases.emit_event import EmitEventUseCase
#
# router = APIRouter(
#     prefix="/api/v1",
# )
#
#
# @app.post("/emit")
# async def emit(data: dict):
#     event = OutboundEvent(
#        type="please.rename.me",
#         data=data,
#         id=str(uuid.uuid4()),
#         occurred_at=datetime.utcnow(),
#     )
#     usecase = EmitEventUseCase(WebhookClient)
#     result = await usecase(
#         url=project_settings.LANGFLOW_BASE_URL + "/api/v1/webhook/",
#         event=event
#     )
#     return {
#         "status": "sent",
#         "langflow_response": result
#     }
#

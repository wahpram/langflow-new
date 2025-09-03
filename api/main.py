import uuid
from datetime import datetime

from fastapi import FastAPI, APIRouter, HTTPException
from httpx import HTTPStatusError

from api.domain.entities import OutboundEvent, OrganizationKeywordSearch
from api.infrastructure.webhook_client import WebhookClient
from api.usecases.emit_event import EmitEventUseCase
from api.core.configs import project_settings as settings

app = FastAPI(title=settings.APP_NAME)
LANGFW_WEBHOOK_URL = f"{settings.LANGFW_BASE_URL}:{settings.LANGFW_PORT}/api/v1/webhook/{settings.LANGFW_PROJECT_ID}"

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
        result = await usecase(
            url=LANGFW_WEBHOOK_URL,
            event=event
        )
        return {"status": "sent", "langflow_response": result}
    except HTTPStatusError as e:
        status = e.response.status_code
        detail = e.response.text
        raise HTTPException(status_code=status, detail=detail)


@app.post("/emit/org-search")
async def emit_org_search(body: OrganizationKeywordSearch):
    # Siapkan payload sesuai spesifikasi Apollo (nanti diolah oleh Langflow)
    apollo_payload = {
        "organization_num_employees_ranges": body.employees_ranges,
        "organization_locations": body.locations,
        "organization_not_locations": body.not_locations,
        "revenue_range": {
            "min": body.min_revenue,
            "max": body.max_revenue,
        },
        "q_organization_keyword_tags": body.keyword_tags,
        "q_organization_name": body.organization_name,
        "page": body.page,
        "per_page": body.per_page,
    }

    event = OutboundEvent(
        type="apollo.organization.search",
        data=apollo_payload,
        id=str(uuid.uuid4()),
        occurred_at=datetime.utcnow(),
    )

    client = WebhookClient()
    usecase = EmitEventUseCase(client)

    try:
        result = await usecase(
            url=LANGFW_WEBHOOK_URL,
            event=event
        )
        return {"status": "sent", "langflow_response": result}
    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@app.get("/health")
async def health():
    return {"status": "ok"}

#TODO: Route to organization search
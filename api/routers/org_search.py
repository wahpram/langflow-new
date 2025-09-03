# api/routers/org_search.py
import uuid
from datetime import datetime
from fastapi import APIRouter
from api.domain.entities import OutboundEvent, OrganizationKeywordSearch
from api.services.emit_webhook import emit_to_langflow

router = APIRouter(prefix="/emit", tags=["emit-apollo"])

@router.post("/org-search")
async def emit_org_search(body: OrganizationKeywordSearch):
    apollo_payload = {
        "organization_num_employees_ranges": body.employees_ranges,
        "organization_locations": body.locations,
        "organization_not_locations": body.not_locations,
        "revenue_range": {"min": body.min_revenue, "max": body.max_revenue},
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
    return await emit_to_langflow(event)


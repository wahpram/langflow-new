from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict

class OutboundEvent(BaseModel):
    type: str
    data: Dict[str, Any]
    id: str
    occurred_at: datetime

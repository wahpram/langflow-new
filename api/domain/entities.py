from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any, Dict
from datetime import datetime
import re

class OutboundEvent(BaseModel):
    type: str
    data: Dict[str, Any]
    id: str
    occurred_at: datetime



_EMP_RANGE_RE = re.compile(r"^\d+,\d+$")

class OrganizationKeywordSearch(BaseModel):
    # Apollo: organization_num_employees_ranges[]= "min,max"
    employees_ranges: List[str] = Field(default_factory=list, description='["1,10","250,500"]')

    # Apollo: organization_locations[] / organization_not_locations[]
    locations: List[str] = Field(default_factory=list)
    not_locations: List[str] = Field(default_factory=list)

    # Apollo: revenue_range[min] / revenue_range[max]
    min_revenue: Optional[int] = Field(default=None, ge=0)
    max_revenue: Optional[int] = Field(default=None, ge=0)

    # Apollo: q_organization_keyword_tags[]
    keyword_tags: List[str] = Field(default_factory=list)

    # Apollo: q_organization_name
    organization_name: Optional[str] = None

    # Apollo Pagination
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=25, ge=1, le=100)

    @field_validator("employees_ranges")
    @classmethod
    def _check_emp_ranges(cls, v: List[str]) -> List[str]:
        for s in v:
            if not _EMP_RANGE_RE.match(s):
                raise ValueError(f'Invalid employees range "{s}". Use "min,max" (e.g. "1,10").')
            lo, hi = map(int, s.split(","))
            if lo > hi:
                raise ValueError(f'Employees range "{s}" has min>max.')
        return v

    @field_validator("max_revenue")
    @classmethod
    def _check_rev(cls, v, info):
        min_rev = info.data.get("min_revenue")
        if v is not None and min_rev is not None and v < min_rev:
            raise ValueError("max_revenue must be >= min_revenue")
        return v

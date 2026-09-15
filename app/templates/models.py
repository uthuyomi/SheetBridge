from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel

OutputType = Literal[
        "excel",
        "google_sheets"
]

TemplateStatus = Literal[
    "pending",
    "analyzing",
    "pending_confirmation",
    "active",
    "error"
]

class TemplateCreate(BaseModel):
    name: str
    file_path: str | None = None
    output_type: OutputType = "excel"
    

class Template(BaseModel):
    id: UUID
    
    name: str
    file_path: str | None = None
    
    output_type: OutputType
    status: TemplateStatus
    
    version: int
    
    definition: dict[str, Any] | None
    
    created_at: datetime
    updated_at: datetime
    
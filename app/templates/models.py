from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field

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

ValueType = Literal[
    "string",
    "integer",
    "number",
    "date",
    "boolean",
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
    
class TemplateExampleCreate(BaseModel):
    template_id: UUID
    file_path: str | None = None
    
    
class TemplateExample(BaseModel):
    id: UUID
    
    template_id: UUID
    file_path: str | None
    
    created_at: datetime
    
class CellTarget(BaseModel):
    sheet: str
    cell: str
    
class FieldDefinition(BaseModel):
    key: str
    label: str
    type: ValueType = "string"
    
    target: CellTarget
    
    required: bool = False
    description: str | None = None
    
    
class TableTarget(BaseModel):
    sheet: str
    start_row: int
    
    
class TableColumnDefinition(BaseModel):
    key: str
    label: str
    column: str
    
    type: ValueType = "string"
    required: bool = False
    description: str | None = None
    
class TableDefinition(BaseModel):
    key: str
    label: str
    
    target: TableTarget
    columns: list[TableColumnDefinition]
    
    max_rows: int | None = None
    description: str | None = None
    
    
class TemplateDefinition(BaseModel):
    version: int = 1
    
    fields: list[FieldDefinition] = Field(
        default_factory=list
    )
    
    tables: list[TableDefinition] = Field(
        default_factory=list
    )

    
    
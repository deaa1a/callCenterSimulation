from datetime import datetime
from enum import IntEnum, Enum
from uuid import UUID, uuid4
from typing import Optional, Annotated
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    ValidationInfo,
    ConfigDict,
    AfterValidator
)

def check_uuid_format(value: UUID) -> UUID:
    if not isinstance(value, UUID):
        raise ValueError("Formato UUID inválido")
    return value

UUIDType = Annotated[UUID, AfterValidator(check_uuid_format)]

class TicketPriority(IntEnum):
    URGENT = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    MINIMAL = 5

class TicketStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Ticket(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        arbitrary_types_allowed=True
    )

    id: int
    creation_date: datetime = Field(default_factory=datetime.now)
    priority: TicketPriority
    status: TicketStatus = TicketStatus.PENDING
    assigned_agent_id: Optional[UUIDType] = None
    assignment_date: Optional[datetime] = None
    resolution_date: Optional[datetime] = None
    execution_id: UUIDType

    @field_validator("assigned_agent_id", mode="after")
    @classmethod
    def validate_agent_assignment(cls, v: Optional[UUID], info: ValidationInfo) -> Optional[UUID]:
        status = info.data.get("status")
        if status in [TicketStatus.ASSIGNED, TicketStatus.IN_PROGRESS] and v is None:
            raise ValueError("Se requiere ID de agente para estados asignados")
        return v

    @field_validator("assignment_date", mode="after")
    @classmethod
    def validate_assignment_date(cls, v: Optional[datetime], info: ValidationInfo) -> datetime:
        if info.data.get("status") == TicketStatus.ASSIGNED and v is None:
            return datetime.now()
        return v  # type: ignore

    @field_validator("resolution_date", mode="after")
    @classmethod
    def validate_resolution_date(cls, v: Optional[datetime], info: ValidationInfo) -> datetime:
        if info.data.get("status") == TicketStatus.COMPLETED and v is None:
            return datetime.now()
        return v  # type: ignore

    @field_validator("execution_id", mode="after")
    @classmethod
    def validate_execution_id(cls, v: UUID) -> UUID:
        if v.version is None:
            raise ValueError("ID de ejecución inválido")
        return v

from enum import Enum
from typing import Optional

from pydantic import Field
from pydantic.v1 import BaseModel
from uuid import UUID, uuid4

class AgentStatus(str, Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    DISABLED = "disabled"


class Agent(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    name: Optional[str] = None
    status: AgentStatus = AgentStatus.AVAILABLE
    current_ticket: Optional[UUID] = None
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from callcentersimulation.domain.model.agent import AgentStatus

Base = declarative_base()

class TicketRecord(Base):
    __tablename__ = 'agents'

    id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    name : Mapped[str]
    status: Mapped[str] = mapped_column(default=AgentStatus.AVAILABLE.value)
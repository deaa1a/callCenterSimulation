import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.callcentersimulation.domain.model.ticket import Ticket, TicketStatus, TicketPriority

Base = declarative_base()

class TicketRecord(Base):
    __tablename__ = 'tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    execution_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    priority: Mapped[int]
    creation_date: Mapped[datetime]
    assigned_agent_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    assignment_date: Mapped[datetime | None]
    resolution_date: Mapped[datetime | None]
    status: Mapped[str] = mapped_column(default=TicketStatus.PENDING.value)

    @classmethod
    def from_domain(cls, ticket: Ticket) -> 'TicketRecord':
        return cls(
            id=ticket.id,
            execution_id=ticket.execution_id,
            priority=ticket.priority,
            creation_date=ticket.creation_date,
            assigned_agent_id=ticket.assigned_agent_id,
            assignment_date=ticket.assignment_date,
            resolution_date=ticket.resolution_date,
            status=ticket.status.value
        )

    def to_domain(self) -> Ticket:
        return Ticket(
            id=self.id,
            execution_id=self.execution_id,
            priority=TicketPriority(self.priority),
            creation_date=self.creation_date,
            assigned_agent_id=self.assigned_agent_id,
            assignment_date=self.assignment_date,
            resolution_date=self.resolution_date,
            status=TicketStatus(self.status)
        )

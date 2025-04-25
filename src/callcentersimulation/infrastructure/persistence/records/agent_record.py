from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from callcentersimulation.domain.model.agent import AgentStatus, Agent

Base = declarative_base()

class AgentRecord(Base):
    __tablename__ = 'agents'

    id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    name : Mapped[str]
    status: Mapped[str] = mapped_column(default=AgentStatus.AVAILABLE.value)


    @classmethod
    def from_domain(cls, agent: Agent) -> 'AgentRecord':
        return cls(
            id=agent.id,
            name=agent.name,
            status=agent.status.value
        )

    def to_domain(self) -> Agent:
        return Agent(
            id=self.id,
            name=self.name,
            status=AgentStatus(self.status)
        )
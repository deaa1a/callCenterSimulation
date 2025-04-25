from contextlib import asynccontextmanager
from datetime import datetime
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.callcentersimulation.domain.model.ticket import Ticket
from src.callcentersimulation.domain.ports.ticket_repository import TicketRepository
from src.callcentersimulation.infrastructure.persistence.records.ticket_record import TicketRecord


class SQLTicketRepository(TicketRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    @asynccontextmanager
    async def _transaction_manager(self):
        try:
            yield
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e

    async def save_batch(self, tickets: list[Ticket]) -> list[Ticket]:
        async with self._transaction_manager():
            entities = [TicketRecord.from_domain(ticket) for ticket in tickets]
            self._session.add_all(entities)
            await self._session.flush(entities)
        return [entity.to_domain() for entity in entities]


    async def get_by_execution_id(self, execution_id: UUID) -> List[Ticket]:
        stmt = select(TicketRecord).where(
            TicketRecord.execution_id == execution_id
        )
        result = await self._session.execute(stmt)
        records = result.scalars().all()
        return [record.to_domain() for record in records]


    async def update(self, tickets: list[Ticket]):
        async with self._transaction_manager():
            for ticket in tickets:
                record = await self._session.get(TicketRecord, ticket.id)

                record.priority = ticket.priority
                record.status = ticket.status
                record.assigned_agent_id = ticket.agent.id if ticket.agent else None
                record.assignment_date = ticket.assignment_date
                record.resolution_date = ticket.resolution_date
                record.resolution_time = ticket.processing_time

            await self._session.flush()

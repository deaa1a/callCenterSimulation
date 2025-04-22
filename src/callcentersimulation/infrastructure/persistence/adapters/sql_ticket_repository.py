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
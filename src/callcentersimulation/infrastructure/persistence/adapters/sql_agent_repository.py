from contextlib import asynccontextmanager
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from callcentersimulation.domain.model.agent import Agent
from callcentersimulation.domain.ports.agent_repository import AgentRepository
from callcentersimulation.infrastructure.persistence.records.agent_record import AgentRecord


class SQLAgentRepository(AgentRepository):

    @asynccontextmanager
    async def _transaction_manager(self):
        try:
            yield
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e

    async def save(self, agent: Agent) -> Agent:
        async with self._transaction_manager():
            record = AgentRecord.from_domain(agent)
            self._session.add(record)
            await self._session.flush()
        return record.to_domain()

    async def get_available_agents(self) -> List[Agent]:
        pass

    async def get_available_agents_by_demand(self, number: int) -> List[Agent]:
        stmt = (
            select(AgentRecord)
            .where(AgentRecord.status == "available")
            .limit(number)
        )
        result = await self._session.execute(stmt)
        records = result.scalars().all()
        return [record.to_domain() for record in records]

    def __init__(self, session: AsyncSession):
        self._session = session



from contextlib import asynccontextmanager
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from callcentersimulation.domain.model.agent import Agent
from callcentersimulation.domain.ports.agent_repository import AgentRepository


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
        pass

    async def get_available_agents(self) -> List[Agent]:
        pass

    async def get_available_agents_by_demand(self, number: int) -> List[Agent]:
        pass

    def __init__(self, session: AsyncSession):
        self._session = session



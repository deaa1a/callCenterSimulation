from abc import ABC, abstractmethod
from typing import List

from callcentersimulation.domain.model.agent import Agent


class AgentRepository(ABC):
    @abstractmethod
    async def save(self, agent: Agent) -> Agent:
        pass

    @abstractmethod
    async def get_available_agents(self) -> List[Agent]:
        pass

    @abstractmethod
    async def get_available_agents_by_demand(self, number: int) -> List[Agent]:
        pass


from typing import List

from callcentersimulation.domain.model.agent import Agent
from callcentersimulation.domain.ports.agent_repository import AgentRepository


class GetSpecificNumberAvailableAgentsUseCase:
    def __init__(
            self,
            agent_repo: AgentRepository,
    ):
        self.agent_repo = agent_repo

    async def execute(self,num_available_agents: int) -> List[Agent]:
        return await self.agent_repo.get_available_agents_by_demand(num_available_agents)
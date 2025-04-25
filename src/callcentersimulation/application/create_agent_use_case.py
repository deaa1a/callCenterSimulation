from uuid import UUID

from callcentersimulation.domain.model.agent import Agent
from callcentersimulation.domain.ports.agent_repository import AgentRepository


class CreateAgentUseCase:
    def __init__(self, agent_repo: AgentRepository):
        self.agent_repo = agent_repo

    async def execute(self, agent: Agent) -> UUID:
        await self.agent_repo.save(agent)
        return agent.id
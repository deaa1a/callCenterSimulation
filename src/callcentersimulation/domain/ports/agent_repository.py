from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from domain.model.agent import Agent, AgentStatus

class AgentRepository(ABC):
    @abstractmethod
    async def save(self, agent: Agent) -> Agent:
        pass
    
    @abstractmethod
    async def get_available(self) -> List[Agent]:
        pass
    
    @abstractmethod
    async def get_by_id(self, agent_id: UUID) -> Optional[Agent]:
        pass
    
    @abstractmethod
    async def update_status(self, 
                          agent_id: UUID, 
                          status: AgentStatus) -> Agent:
        pass
    
    @abstractmethod
    async def assign_ticket(self, 
                          agent_id: UUID, 
                          ticket_id: UUID) -> Agent:
        pass
    
    @abstractmethod
    async def complete_ticket(self, agent_id: UUID) -> Agent:
        pass

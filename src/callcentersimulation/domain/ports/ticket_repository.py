from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.callcentersimulation.domain.model.ticket import Ticket


class TicketRepository(ABC):
    @abstractmethod
    async def save_batch(self, tickets: List[Ticket]) -> List[Ticket]:
        pass

    @abstractmethod
    async def get_by_execution_id(self, execution_id: UUID) -> List[Ticket]:
        pass

    @abstractmethod
    async def update(self, tickets: List[Ticket]):
        pass



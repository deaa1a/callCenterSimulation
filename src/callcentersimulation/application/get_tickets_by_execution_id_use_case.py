from uuid import UUID
from typing import List

from callcentersimulation.domain.model.ticket import Ticket
from callcentersimulation.domain.ports.ticket_repository import TicketRepository


class GetTicketByExecutionIdUseCase:
    def __init__(self, ticket_repo: TicketRepository):
        self.ticket_repo = ticket_repo

    async def execute(self, execution_id: UUID) -> List[Ticket]:
        return await self.ticket_repo.get_by_execution_id(execution_id)
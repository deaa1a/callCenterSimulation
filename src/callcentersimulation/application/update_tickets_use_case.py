from typing import List
from src.callcentersimulation.domain.model.ticket import Ticket
from src.callcentersimulation.domain.ports.ticket_repository import TicketRepository

class UpdateTicketsUseCase:
    def __init__(self, ticket_repo: TicketRepository):
        self.ticket_repo = ticket_repo

    async def execute(self, tickets: List[Ticket]):
        await self.ticket_repo.update(tickets)

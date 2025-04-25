import random
import time
from datetime import datetime
from uuid import UUID

from callcentersimulation.domain.model.agent import Agent
from callcentersimulation.domain.model.concurrent_list import ConcurrentList
from callcentersimulation.domain.model.ticket import Ticket, TicketStatus


class ProcessTicketUseCase:

    def execute(self, tickets : ConcurrentList, agent : Agent):
        while True:
            ticket = tickets.get_next_ticket()
            if not ticket:
                break

        start_time = time.perf_counter()
        processing_time = random.uniform(0, 4)
        time.sleep(processing_time)

        updated_ticket = Ticket(
            **ticket.dict(),
            status=TicketStatus.COMPLETED,
            agent= agent,
            assignment_date=datetime.now(),
            resolution_date=datetime.now(),
            processing_time=time.perf_counter() - start_time
        )

        tickets.update_ticket(ticket, updated_ticket)
        tickets.log(
            f"Agent -{agent.id} | "
            f"Completed Ticket #{ticket.id} ({ticket.priority.name}) | "
            f"Time: {processing_time:.2f}s"
        )
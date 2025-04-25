import random
import time
from datetime import datetime

from callcentersimulation.domain.model.agent import Agent
from callcentersimulation.domain.model.concurrent_list import ConcurrentList
from callcentersimulation.domain.model.ticket import Ticket, TicketStatus, TicketPriority


class ProcessTicketUseCase:

    def execute(self, tickets : ConcurrentList, agent : Agent):
        while True:
            ticket = tickets.get_next_ticket()
            if not ticket:
                break

            start_time = time.perf_counter()
            processing_time = random.uniform(0, 3)
            time.sleep(processing_time)

            excluded_fields = {
                'status',
                'agent',
                'assignment_date',
                'resolution_date',
                'processing_time'
            }

            ticket_data = ticket.dict()
            for field in excluded_fields:
                ticket_data.pop(field, None)

            updated_ticket = Ticket(
                **ticket_data,
                status=TicketStatus.COMPLETED,
                agent=agent,
                assignment_date=datetime.now(),
                resolution_date=datetime.now(),
                processing_time=time.perf_counter() - start_time
            )

            tickets.update_ticket(ticket, updated_ticket)
            tickets.log(
                f"Id -{updated_ticket.id} | "
                f"Creation date -{updated_ticket.creation_date} | "
                f"Priority -{TicketPriority(updated_ticket.priority).name} | "
                f"Agent id -{agent.id} | "
                f"Agent name -{agent.name} | "
                f"assignment date -{updated_ticket.assignment_date} | "
                f"resolution date -{updated_ticket.resolution_date} | "
                f"Time: {processing_time:.2f}s"
            )
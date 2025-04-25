import multiprocessing
from uuid import UUID

from callcentersimulation.application.create_concurrent_list_use_case import CreateConcurrentListUseCase
from callcentersimulation.application.get_specific_number_available_agents_use_case import \
    GetSpecificNumberAvailableAgentsUseCase
from callcentersimulation.application.get_tickets_by_execution_id_use_case import GetTicketByExecutionIdUseCase
from callcentersimulation.application.process_ticket_use_case import ProcessTicketUseCase
from callcentersimulation.application.update_tickets_use_case import UpdateTicketsUseCase


class ProcessTicketsUseCase:
    def __init__(
            self,
            get_ticket_by_execution_id: GetTicketByExecutionIdUseCase,
            get_available_agents: GetSpecificNumberAvailableAgentsUseCase,
            create_concurrent_list: CreateConcurrentListUseCase,
            process_ticket :ProcessTicketUseCase,
            update_tickets: UpdateTicketsUseCase
    ):
        self.get_ticket_by_execution_id = get_ticket_by_execution_id
        self.get_available_agents = get_available_agents
        self.create_concurrent_list = create_concurrent_list
        self.process_ticket = process_ticket
        self.update_tickets = update_tickets

    async def execute(self, execution_id: UUID, num_agents: int):

        tickets = await self.get_ticket_by_execution_id.execute(execution_id)
        sorted_tickets = sorted(tickets, key=lambda t: t.priority)

        agents = await self.get_available_agents.execute(num_agents)
        workers = []
        with multiprocessing.Manager() as manager:
            concurrent_list = self.create_concurrent_list.execute(manager, sorted_tickets)

            for agent in agents:
                p = multiprocessing.Process(
                    target=self.process_ticket.execute,
                    args=(concurrent_list, agent)
                )
                workers.append(p)
                p.start()

            for p in workers:
                p.join()

            result = list(concurrent_list.tickets)

        await self.update_tickets.execute(result)
        return result
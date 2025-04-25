import multiprocessing
from typing import List

from callcentersimulation.domain.model.concurrent_list import ConcurrentList
from callcentersimulation.domain.model.ticket import Ticket


class CreateConcurrentListUseCase:

    def execute(self, manager: multiprocessing.Manager ,tickets: List[Ticket]):
        return ConcurrentList(manager, tickets)
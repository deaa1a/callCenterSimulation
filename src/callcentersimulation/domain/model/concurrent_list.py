import multiprocessing
from typing import List
import time

from callcentersimulation.domain.model.ticket import Ticket


class ConcurrentList:
    def __init__(self, manager: multiprocessing.Manager, tickets: List[Ticket]):
        self.tickets = manager.list(tickets)
        self.queue = manager.Queue()
        self.lock = manager.Lock()
        self.print_lock = manager.Lock()
        self.start_time = time.perf_counter()
        self._initialize_queue()

    def _initialize_queue(self):
        for ticket in self.tickets:
            self.queue.put(ticket)

    def get_next_ticket(self):
        try:
            return self.queue.get_nowait()
        except:
            return None

    def update_ticket(self, original: Ticket, updated: Ticket):
        with self.lock:
            index = self.tickets.index(original)
            self.tickets[index] = updated

    def log(self, message: str):
        with self.print_lock:
            elapsed = time.perf_counter() - self.start_time
            print(f"[+{elapsed:6.2f}s] {message}", flush=True)
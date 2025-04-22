from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from domain.model.execution import Execution, ExecutionStatus

class ExecutionRepository(ABC):
    @abstractmethod
    async def save(self, execution: Execution) -> Execution:
        pass
    
    @abstractmethod
    async def get_by_id(self, execution_id: UUID) -> Optional[Execution]:
        pass
    
    @abstractmethod
    async def update_status(self, 
                          execution_id: UUID, 
                          status: ExecutionStatus) -> Execution:
        pass
    
    @abstractmethod
    async def increment_processed(self, execution_id: UUID) -> Execution:
        pass

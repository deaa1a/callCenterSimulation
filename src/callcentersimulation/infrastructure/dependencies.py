from typing import Annotated, AsyncGenerator

from fastapi import Depends
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from callcentersimulation.application.create_agent_use_case import CreateAgentUseCase
from callcentersimulation.application.create_concurrent_list_use_case import CreateConcurrentListUseCase
from callcentersimulation.application.get_specific_number_available_agents_use_case import \
    GetSpecificNumberAvailableAgentsUseCase
from callcentersimulation.application.get_tickets_by_execution_id_use_case import GetTicketByExecutionIdUseCase
from callcentersimulation.application.process_ticket_use_case import ProcessTicketUseCase
from callcentersimulation.application.process_tickets_use_case import ProcessTicketsUseCase
from callcentersimulation.infrastructure.persistence.adapters.sql_agent_repository import SQLAgentRepository
from src.callcentersimulation.application.create_ticket_use_case import CreateTicketUseCase
from src.callcentersimulation.infrastructure.persistence.adapters.sql_ticket_repository import SQLTicketRepository
from src.callcentersimulation.infrastructure.persistence.conf.database import AsyncSessionLocal
from src.callcentersimulation.infrastructure.utils.csv_ticket_processor import CsvTicketProcessor

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

def get_ticket_repo(db: Annotated[AsyncSession, Depends(get_async_db)]) -> SQLTicketRepository:
    return SQLTicketRepository(db)

def get_agent_repo(db: Annotated[AsyncSession, Depends(get_async_db)]) -> SQLAgentRepository:
    return SQLAgentRepository(db)

def get_create_use_case(
    repo: Annotated[SQLTicketRepository, Depends(get_ticket_repo)]) -> CreateTicketUseCase:
    return CreateTicketUseCase(repo)

def get_ticket_by_execution_id_use_case(
    repo: Annotated[SQLTicketRepository, Depends(get_ticket_repo)]) -> GetTicketByExecutionIdUseCase:
    return GetTicketByExecutionIdUseCase(repo)

def get_csv_processor() -> CsvTicketProcessor:
    return CsvTicketProcessor(execution_id=uuid4())

def get_available_agents_use_case(
    repo: Annotated[SQLAgentRepository, Depends(get_ticket_repo)]
) -> GetSpecificNumberAvailableAgentsUseCase:
    return GetSpecificNumberAvailableAgentsUseCase(repo)

def get_create_agent_use_case(
    repo: Annotated[SQLAgentRepository, Depends(get_ticket_repo)]
) -> CreateAgentUseCase:
    return CreateAgentUseCase(repo)

def get_create_concurrent_list_use_case() -> CreateConcurrentListUseCase:
    return CreateConcurrentListUseCase()

def get_process_ticket_use_case() -> ProcessTicketUseCase:
    return ProcessTicketUseCase()

def get_process_tickets_use_case(
    get_ticket_by_execution_id: Annotated[GetTicketByExecutionIdUseCase, Depends(get_ticket_by_execution_id_use_case)],
    get_available_agents: Annotated[GetSpecificNumberAvailableAgentsUseCase, Depends(get_available_agents_use_case)],
    create_concurrent_list: Annotated[CreateConcurrentListUseCase, Depends(get_create_concurrent_list_use_case)],
    process_ticket: Annotated[ProcessTicketUseCase, Depends(get_process_ticket_use_case)]
) -> ProcessTicketsUseCase:
    return ProcessTicketsUseCase(
        get_ticket_by_execution_id=get_ticket_by_execution_id,
        get_available_agents=get_available_agents,
        create_concurrent_list=create_concurrent_list,
        process_ticket=process_ticket
    )
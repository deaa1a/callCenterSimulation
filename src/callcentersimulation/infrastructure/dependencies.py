from typing import Annotated, AsyncGenerator

from fastapi import Depends
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.callcentersimulation.application.create_ticket_use_case import CreateTicketUseCase
from src.callcentersimulation.infrastructure.persistence.adapters.sql_ticket_repository import SQLTicketRepository
from src.callcentersimulation.infrastructure.persistence.conf.database import AsyncSessionLocal
from src.callcentersimulation.infrastructure.utils.csv_ticket_processor import CsvTicketProcessor


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

def get_ticket_repo(db: Annotated[AsyncSession, Depends(get_async_db)]) -> SQLTicketRepository:
    return SQLTicketRepository(db)

def get_create_use_case(
    repo: Annotated[SQLTicketRepository, Depends(get_ticket_repo)]) -> CreateTicketUseCase:
    return CreateTicketUseCase(repo)

def get_csv_processor() -> CsvTicketProcessor:
    return CsvTicketProcessor(execution_id=uuid4())
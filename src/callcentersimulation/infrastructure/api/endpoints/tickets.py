from uuid import UUID

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
import logging

from callcentersimulation.application.process_tickets_use_case import ProcessTicketsUseCase
from src.callcentersimulation.application.create_ticket_use_case import CreateTicketUseCase
from src.callcentersimulation.infrastructure.dependencies import (
    get_csv_processor,
    get_create_use_case, get_process_tickets_use_case
)
from src.callcentersimulation.infrastructure.utils.csv_ticket_processor import CsvTicketProcessor

router = APIRouter(tags=["Tickets"])
logger = logging.getLogger(__name__)


@router.post("/tickets", response_model=dict)
async def upload_tickets(
        file: UploadFile = File(...),
        processor: CsvTicketProcessor = Depends(get_csv_processor),
        use_case: CreateTicketUseCase = Depends(get_create_use_case)
):
    try:

        content = await file.read()

        tickets = processor.process(content)

        if not tickets:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid tickets found in file"
            )

        await use_case.execute(tickets)

        return {
            "message": "File processed successfully",
            "execution_id": str(processor.execution_id),
            "tickets_processed": len(tickets)
        }

    except ValueError as e:
        logger.error(f"Error validating CSV: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        logger.exception("Unexpected error processing tickets")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error processing file"
        ) from e


@router.post("/executions/{execution_id}/tickets/agents/{number_of_agents}", response_model=dict)
async def process_tickets(
        execution_id: UUID,
        number_of_agents: int,
        process_tickets : ProcessTicketsUseCase = Depends(get_process_tickets_use_case)
):
    try:
        await process_tickets.execute(execution_id, number_of_agents)

    except Exception as e:
        logger.exception("Unexpected error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error "
        ) from e


from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
import logging

from src.callcentersimulation.application.create_ticket_use_case import CreateTicketUseCase
from src.callcentersimulation.infrastructure.dependencies import (
    get_csv_processor,
    get_create_use_case
)
from src.callcentersimulation.infrastructure.utils.csv_ticket_processor import CsvTicketProcessor

router = APIRouter(tags=["Tickets"])
logger = logging.getLogger(__name__)


@router.post("/upload-tickets", response_model=dict)
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
        logger.error(f"Error validando CSV: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        logger.exception("Error inesperado procesando tickets")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno procesando archivo"
        ) from e

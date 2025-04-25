from fastapi import APIRouter, Depends, HTTPException, status
import logging

from callcentersimulation.application.create_agent_use_case import CreateAgentUseCase
from callcentersimulation.infrastructure.api.dto.agent_dto import AgentDto
from callcentersimulation.infrastructure.dependencies import get_create_agent_use_case

router = APIRouter(tags=["Agents"])
logger = logging.getLogger(__name__)

@router.post("/agents", response_model=dict)
async def upload_tickets(
        agent_dto: AgentDto,
        use_case: CreateAgentUseCase = Depends(get_create_agent_use_case)
):
    try:

        agent = await use_case.execute(agent_dto.to_domain())

        return {
            "message": "Agent created successfully",
            "agent": agent
        }

    except Exception as e:
        logger.exception("Unexpected error creating agent")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error creating agent"
        ) from e
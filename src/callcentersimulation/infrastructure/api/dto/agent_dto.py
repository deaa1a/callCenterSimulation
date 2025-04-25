from typing import Optional

from pydantic.v1 import BaseModel

from callcentersimulation.domain.model.agent import Agent

class AgentDto(BaseModel):
    name: str

    def to_domain(self) -> Agent:
        return Agent(
            name=self.name,
        )
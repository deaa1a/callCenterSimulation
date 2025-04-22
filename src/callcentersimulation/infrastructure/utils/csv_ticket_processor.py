import logging
from io import BytesIO
from typing import List
from uuid import UUID

import pandas as pd

from src.callcentersimulation.domain.model.ticket import Ticket, TicketPriority

logger = logging.getLogger(__name__)


class CsvTicketProcessor:
    def __init__(self, execution_id: UUID):
        self.execution_id = execution_id

    def process(self, file_content: bytes) -> List[Ticket]:
        try:
            buffer = BytesIO(file_content)
            df = pd.read_csv(
                buffer,
                usecols=["id", "fecha_creacion", "prioridad"],
                dtype={"id": int, "prioridad": int},
                parse_dates=["fecha_creacion"],
                dayfirst=True,
                encoding='utf-8',
                on_bad_lines='warn'
            )

            return self._validate_rows(df)

        except (KeyError, pd.errors.ParserError) as e:
            logger.error(f"Error de formato en CSV: {str(e)}")
            raise ValueError("Formato de archivo inválido") from e

    def _validate_rows(self, df: pd.DataFrame) -> List[Ticket]:
        tickets = []
        for index, row in df.iterrows():
            try:
                if pd.isna(row["fecha_creacion"]):
                    raise ValueError("Invalid creation date")
                priority = TicketPriority(row["prioridad"])
                tickets.append(Ticket(
                    id=row["id"],
                    creation_date=row["fecha_creacion"].to_pydatetime(),
                    priority=priority,
                    execution_id=self.execution_id
                ))
            except Exception as e:
                logger.warning(f"Fila {index} ignorada: {str(e)}")
        return tickets

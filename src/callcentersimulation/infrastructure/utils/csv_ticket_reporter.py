import io
from io import StringIO
from typing import List

import pandas as pd

from callcentersimulation.domain.model.ticket import Ticket

class CsvTicketReporter:

    def process(self,tickets : List[Ticket] ) -> StringIO:
        df = pd.DataFrame([{
            "id": t.id,
            "fecha_creacion": t.creation_date,
            "prioridad": t.priority,
            "agente": t.agent.id,
            "fecha_asignacion": t.assignment_date,
            "fecha_resolucion": t.resolution_date,
            "tiempo_procesamiento": t.processing_time,
            "estado": t.status
        } for t in tickets])

        for col in ["fecha_creacion", "fecha_asignacion", "fecha_resolucion"]:
            df[col] = df[col].astype(str)

        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        return output
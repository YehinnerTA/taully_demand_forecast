from typing import List
from domain.entities.demand import Demand
from application.services.ingest_service import IngestService

class ProcessReportUseCase:
    def __init__(self, ingest_service: IngestService):
        self.ingest_service = ingest_service

    def execute(self, file_path: str) -> List[Demand]:
        print(f"Procesando reporte: {file_path}")
        demands = self.ingest_service.process_file(file_path)
        print(f"Demanda consolidada para {len(demands)} categorías/fechas")
        return demands
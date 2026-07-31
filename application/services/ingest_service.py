from typing import List
from pathlib import Path

from domain.entities.sale import Sale
from domain.entities.demand import Demand
from domain.interfaces.repositories import SaleReader, DemandRepository, ProductCatalogRepository
from infrastructure.readers.excel_reader import ExcelReader
from infrastructure.readers.pdf_reader import PDFReader

class IngestService:
    def __init__(
        self,
        catalog_repo: ProductCatalogRepository,
        demand_repo: DemandRepository
    ):
        self.catalog_repo = catalog_repo
        self.demand_repo = demand_repo

    def process_file(self, file_path: str) -> List[Demand]:
        # 1. Seleccionar el reader adecuado según la extensión
        path = Path(file_path)
        if path.suffix.lower() in ['.xlsx', '.xls']:
            reader: SaleReader = ExcelReader()
        elif path.suffix.lower() == '.pdf':
            reader: SaleReader = PDFReader()
        else:
            raise ValueError("Formato no soportado. Use .xlsx, .xls o .pdf")

        # 2. Leer las ventas del archivo
        sales: List[Sale] = reader.read_sales(str(path))

        # 3. Enriquecer con categoría (Family) usando el catálogo
        demands_dict = {}
        for sale in sales:
            product = self.catalog_repo.get_product(sale.product_name)
            if product is None:
                # Si no está en el catálogo, lo ignoramos o asignamos "DESCONOCIDO"
                # Para este caso, lo asignamos a "OTROS" para no perder el dato
                category = "OTROS"
            else:
                category = product.family  # Usamos 'family' como agrupador principal

            # Agrupar por (fecha, categoria) sumando cantidades
            key = (sale.date, category)
            if key in demands_dict:
                demands_dict[key] += sale.quantity
            else:
                demands_dict[key] = sale.quantity

        # 4. Convertir a entidades Demand
        demands = [
            Demand(date=date, category=cat, quantity=qty)
            for (date, cat), qty in demands_dict.items()
        ]

        # 5. Guardar en el repositorio (historial)
        self.demand_repo.save_demands(demands)

        return demands
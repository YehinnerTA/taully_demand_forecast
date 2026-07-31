import pandas as pd
import tabula
import pdfplumber
import re
from typing import List
from datetime import datetime

from domain.interfaces.repositories import SaleReader
from domain.entities.sale import Sale
from infrastructure.utils.date_extractor import extract_date_from_text
from infrastructure.utils.date_cleaner import clean_sales_dataframe

class PDFReader(SaleReader):
    """
    Lee archivos PDF que siguen el formato del sistema POS:
    - Encabezado con 'FECHAI: dd/mm/yyyy' y 'FECHAF: dd/mm/yyyy'.
    - Tabla con columnas: PROD, DESC, CANT, TOTAL.
    """
    def read_sales(self, file_path: str) -> List[Sale]:
        # 1. Extraer la fecha del PDF usando pdfplumber
        fecha = None
        with pdfplumber.open(file_path) as pdf:
            texto_completo = ""
            for page in pdf.pages:
                texto_completo += page.extract_text() + "\n"
            fecha = extract_date_from_text(texto_completo)

        # 2. Extraer la tabla usando tabula (busca la primera tabla que tenga PROD y CANT)
        tablas = tabula.read_pdf(file_path, pages='all', multiple_tables=True, guess=False)
        
        df_ventas = None
        for tabla in tablas:
            # Normalizar nombres de columnas
            tabla.columns = tabla.columns.str.upper().str.strip()
            if 'PROD' in tabla.columns and 'CANT' in tabla.columns:
                df_ventas = tabla[['PROD', 'DESC', 'CANT', 'TOTAL']].copy()
                break
        
        if df_ventas is None:
            raise ValueError("No se encontró la tabla de ventas en el PDF")
        
        # 3. Limpiar los datos (quitar ANULADO, convertir a números)
        df_ventas = clean_sales_dataframe(df_ventas)

        # 4. Mapear a entidades Sale
        sales = []
        for _, row in df_ventas.iterrows():
            sale = Sale(
                date=fecha,
                product_name=str(row['PROD']).strip(),
                quantity=float(row['CANT']),
                total=float(row['TOTAL'])
            )
            sales.append(sale)

        return sales
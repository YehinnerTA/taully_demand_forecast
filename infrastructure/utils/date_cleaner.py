import pandas as pd

def clean_sales_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el DataFrame de ventas:
    - Elimina filas con 'ANULADO', 'Total', 'Subtotal' en la columna PROD.
    - Convierte CANT y TOTAL a números.
    - Elimina filas con CANT nula o cero.
    - Resetea el índice.
    """
    if 'PROD' not in df.columns:
        raise ValueError("El DataFrame no contiene la columna 'PROD'")

    # 1. Filtrar filas no deseadas
    df = df[~df['PROD'].astype(str).str.contains('ANULADO|Total|Subtotal|Grupos', case=False, na=False)]

    # 2. Convertir columnas numéricas
    df['CANT'] = pd.to_numeric(df['CANT'], errors='coerce')
    df['TOTAL'] = pd.to_numeric(df['TOTAL'], errors='coerce')

    # 3. Eliminar filas con CANT nula o cero
    df = df.dropna(subset=['CANT'])
    df = df[df['CANT'] > 0]

    # 4. Resetear índice
    df = df.reset_index(drop=True)

    return df
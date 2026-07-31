from dataclasses import dataclass
from datetime import datetime

@dataclass
class Sale:
    """Representa una venta de un producto en una fecha específica."""
    date: datetime
    product_name: str
    quantity: float
    total: float

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        if self.total < 0:
            raise ValueError("El total no puede ser negativo")
from dataclasses import dataclass

@dataclass
class Product:
    """Representa un producto del catálogo maestro."""
    product_name: str
    family: str
    category: str
    brand: str = ""
    cost: float = 0.0
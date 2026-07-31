from domain.interfaces.repositories import ProductCatalogRepository
from domain.entities.product import Product
from typing import List

class CatalogService:
    def __init__(self, catalog_repo: ProductCatalogRepository):
        self.catalog_repo = catalog_repo

    def get_all_products(self) -> List[Product]:
        return self.catalog_repo.get_all_products()

    def get_product(self, name: str) -> Product:
        return self.catalog_repo.get_product(name)
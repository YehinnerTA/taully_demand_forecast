from abc import ABC, abstractmethod
import pandas as pd

class MLModel(ABC):
    """Contrato para el modelo de Machine Learning."""
    @abstractmethod
    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        pass

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> pd.Series:
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        pass

    @classmethod
    @abstractmethod
    def load(cls, path: str) -> 'MLModel':
        pass
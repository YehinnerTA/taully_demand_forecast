import joblib
import numpy as np

class ModelPredictor:
    def __init__(self):
        self.model = None

    def load_model(self, path: str):
        self.model = joblib.load(path)

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise ValueError("Primero debe cargar un modelo usando load_model()")
        return self.model.predict(X)
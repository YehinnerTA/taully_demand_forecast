import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from typing import Dict

class ModelTrainer:
    def __init__(self):
        self.best_model = None

    def train(self, X: np.ndarray, y: np.ndarray, model_name: str = "model") -> Dict[str, float]:
        # Dividir en entrenamiento y prueba (80/20)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

        # Usar RandomForest como ejemplo (se puede cambiar a XGBoost)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Predecir y evaluar
        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # MAPE (evitar divisiones por cero)
        mask = y_test != 0
        if np.any(mask):
            mape = np.mean(np.abs((y_test[mask] - y_pred[mask]) / y_test[mask])) * 100
        else:
            mape = float('inf')

        self.best_model = model
        return {'mae': mae, 'rmse': rmse, 'mape': mape}

    def save_best_model(self, path):
        if self.best_model is not None:
            joblib.dump(self.best_model, path)
        else:
            raise ValueError("No hay modelo entrenado para guardar")
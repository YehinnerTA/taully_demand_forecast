from application.services.train_service import TrainService
from application.services.predict_service import PredictService

class RunForecastUseCase:
    def __init__(self, train_service: TrainService, predict_service: PredictService):
        self.train_service = train_service
        self.predict_service = predict_service

    def execute(self, days: int = 7):
        print("Entrenando modelo...")
        metrics = self.train_service.run()
        print(f"Métricas del mejor modelo: MAPE={metrics.get('mape', 'N/A')}%, RMSE={metrics.get('rmse', 'N/A')}")

        print(f"Generando predicciones para {days} días...")
        predictions = self.predict_service.predict_future(days)
        
        print("\nPredicciones por categoría:")
        for cat, demands in predictions.items():
            print(f"\n  {cat}:")
            for d in demands:
                print(f"    {d.date.strftime('%Y-%m-%d')}: {d.quantity:.2f} unidades")
        
        return predictions
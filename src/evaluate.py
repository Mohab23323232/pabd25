import joblib
import numpy as np
import json
import os
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

if __name__ == "__main__":
    model = joblib.load("models/apartment_price_model.pkl")
    X_test, y_test = joblib.load("data/processed/test_data.pkl")

    predictions = model.predict(X_test)
    metrics = {
        "mae": mean_absolute_error(y_test, predictions),
        "rmse": np.sqrt(mean_squared_error(y_test, predictions)),
        "r2": r2_score(y_test, predictions)
    }

    os.makedirs("reports", exist_ok=True)

with open("reports/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)
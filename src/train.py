import joblib
from sklearn.ensemble import RandomForestRegressor
import os

if __name__ == "__main__":
    X_train, y_train = joblib.load("data/processed/train_data.pkl")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/apartment_price_model.pkl")
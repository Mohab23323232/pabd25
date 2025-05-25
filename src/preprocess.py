import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import os

if __name__ == "__main__":
    df = pd.read_csv("data/processed/train.csv", index_col=0)

    df['floor_ratio'] = df['floor'] / df['floors_count']
    df['rooms_count'] = df['rooms_count'].astype(int).clip(upper=3)

    X = df[['total_meters', 'floor_ratio', 'rooms_count']]
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), ['total_meters', 'floor_ratio']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['rooms_count'])
    ])

    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("models", exist_ok=True)

    joblib.dump((X_train, y_train), "data/processed/train_data.pkl")
    joblib.dump((X_test, y_test), "data/processed/test_data.pkl")
    joblib.dump(preprocessor, "models/preprocessor.pkl")
import os
import glob
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split

def load_data(train_data_path):
    csv_files = glob.glob(os.path.join(train_data_path, "*.csv"))
    dfs = [pd.read_csv(file) for file in csv_files]
    return pd.concat(dfs, ignore_index=True)

def process_cian(data):
    data = data[['url', 'total_meters', 'price', 'floor', 'floors_count', 'rooms_count']].copy()
    data['url_id'] = data['url'].apply(lambda x: x.split('/')[-2])
    data = data.set_index('url_id')
    for col in ['total_meters', 'price', 'floor', 'floors_count', 'rooms_count']:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    return data.dropna()

if __name__ == "__main__":
    raw_path = "data/raw"
    os.makedirs("data/processed", exist_ok=True)

    df = load_data(raw_path)
    df_clean = process_cian(df)

    X = df_clean[['total_meters', 'floor', 'floors_count', 'rooms_count']]
    y = df_clean['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    joblib.dump((X_train, y_train), "data/processed/train_data.pkl")
    joblib.dump((X_test, y_test), "data/processed/test_data.pkl")
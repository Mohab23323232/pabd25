from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from logging.config import dictConfig
import config as cfg
import pandas as pd
import joblib
import os
from datetime import datetime
from dotenv import load_dotenv

from models.PredictPriceRequest import PredictPriceRequest
from models.PredictPriceResponse import PredictPriceResponse


load_dotenv()
print("Loaded credentials:", os.getenv("BASIC_AUTH_USERNAME"), os.getenv("BASIC_AUTH_PASSWORD"))

dictConfig(cfg.log_config)

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()

from werkzeug.security import generate_password_hash
users = {
    os.getenv("BASIC_AUTH_USERNAME"): generate_password_hash(os.getenv("BASIC_AUTH_PASSWORD"))
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None

def load_model_and_preprocessor():
    try:
        model = joblib.load(cfg.LRM_TRAINED_PATH)
        preprocessor = joblib.load(cfg.PREPROCESSOR_PATH)
        app.logger.info("Loaded model and preprocessor locally")
    except Exception as e:
        app.logger.warning(f"Failed to load model and preprocessor: {e}")
        raise e
    return model, preprocessor

def predict_price(request_data: PredictPriceRequest) -> float:
    model, preprocessor = load_model_and_preprocessor()
    input_df = pd.DataFrame([{
        'total_meters': request_data.area,
        'floor': request_data.floor,
        'floors_count': request_data.floors_count,
        'rooms_count': request_data.rooms_count,
        'floor_ratio': request_data.floor / request_data.floors_count,
    }])
    print("🔥🔥 REQUEST RECEIVED AT", datetime.now())
    input_processed = preprocessor.transform(input_df)
    predicted_price = model.predict(input_processed)[0]
    return predicted_price

@app.route("/api/predict", methods=["POST"])
@auth.login_required
def predict():
    request_body = request.get_json()
    app.logger.warning(f"📥 RAW BODY = {request_body}")
    app.logger.info(f"Received request: {request_body}")
    try:
        dto = PredictPriceRequest(**request_body)
        price = predict_price(dto)
        response = PredictPriceResponse(price=price)
        app.logger.info(f"Prediction: {response.model_dump()}")
        return jsonify(response.model_dump()), 200
    except Exception as e:
        app.logger.warning(f"Invalid request: {e}")
        return jsonify({'error': 'Invalid input'}), 422

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

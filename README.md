Сервис прогнозирования цен на жилье
Начальная разработка и подготовка
Этап 1: Проектирование архитектуры и настройка окружения
•	Проект структурирован в виде модульного ML-пайплайна с этапами: сбор, предобработка, обучение и развёртывание.
•	Настроено виртуальное окружение, созданы файлы .gitignore, .dvcignore, requirements.txt, dvc.yaml и базовая структура каталогов.
Этап 2: Разработка базового API и логирования
•	Реализован базовый REST API на Flask (service/app.py) с маршрутом /api/predict.
•	Включено логирование запросов в файл logs/server.log.
•	Для отладки использовалась простая эвристика в Jupyter: оценка по 300 тыс. руб/м².
Этап 3: Обучение модели и интеграция
•	В notebooks/train.ipynb обучена модель RandomForestRegressor.
•	Проведён EDA-анализ (notebooks/eda.ipynb).
•	Модель сериализована в apartment_price_model.pkl, предобработка — в apartment_price_model_preprocessor.pkl.
•	Модель и препроцессор подключены в app.py и загружаются при запуске.
Этап 4: Автоматизация через скрипты (src/)
•	Созданы модульные скрипты process_data.py, train_model.py, evaluate_model.py.
•	Добавлены аргументы командной строки, логирование и PEP8-структура.
•	Все шаги протестированы на новых данных.
Этап 5: Улучшение модели и ветвление
•	Использованы признаки: площадь, этаж, этажность, количество комнат.
•	Ветки Git:
o	main: финальная версия.
o	lin_reg: простая линейная регрессия.
o	your_best_model: содержит лучшую модель.
________________________________________
Описание проекта
Полноценный ML/DevOps конвейер для прогнозирования цен квартир. Включает сбор данных, предобработку, обучение, API, оркестрацию (Airflow) и контейнеризацию (Docker).
Структура проекта
PABD25/
PABD25/
├── .dvc/
│   ├── cache/
│   └── tmp/
├── .gitignore
├── config/
├── data/
│   ├── processed/
│   └── raw/
│       ├── 1_2025-05-25_16-42.csv
│       ├── 2_2025-05-25_16-42.csv
│       └── 3_2025-05-25_16-43.csv
├── img/
│   └── arch.png
├── notebooks/
│   ├── eda.ipynb
│   └── train.ipynb
├── reports/
│   ├── metrics.csv
│   ├── metrics.json
│   └── metrics.txt
├── service/
│   ├── logs/
│   │   ├── .gitkeep
│   │   └── server.log
│   ├── models/
│   │   ├── apartment_price_model.pkl
│   │   └── apartment_price_model_preprocessor.pkl
│   │   ├── PredictPriceRequest.py
│   │   └── PredictPriceResponse.py
│   ├── requests/
│   │   └── predict-post.http
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   │   └── index.html
│   ├── .env
│   ├── app.py
│   ├── config.py
│   └── Dockerfile
├── src/
│   ├── logs/
│   ├── evaluate_model.py
│   ├── parse_cian.py
│   ├── process_data.py
│   └── train_model.py
├── venv/
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   └── share/
├── .dvcignore
├── .gitignore
├── dvc.lock
├── dvc.yaml
├── LICENSE
├── README.md
└── requirements.txt
Локальный запуск
Установка зависимостей
pip install -r requirements.txt
Запуск приложения (режим разработки)
cd service
python app.py
Интерфейс: http://localhost:5000
Использование API
POST /api/predict
POST http://localhost:5000/api/predict
Content-Type: application/json
Authorization: Basic YWRtaW46MTIzNA==

{
  "area": 60,
  "floor": 2,
  "floors_count": 5,
  "rooms_count": 3
}
Пример ответа:
{
  "price": 6200000.0 ₽
}
Авторизация
Файл .env:
BASIC_AUTH_USERNAME=admin
BASIC_AUTH_PASSWORD=1234
Обученная модель
•	Алгоритм: RandomForestRegressor
•	Предобработка: StandardScaler, OneHotEncoder
•	Файлы: apartment_price_model.pkl, apartment_price_model_preprocessor.pkl
________________________________________
Этап 6: DVC
•	process_data → data/processed/train.csv
•	train_model → models/*.pkl
•	evaluate_model → reports/
dvc repro
Этап 7: Airflow
•	DAG (barini-dag.py) парсит и загружает данные в PostgreSQL
•	Запуск модели и отчёта
•	Интерфейс: http://localhost:8080

Этап 8: Docker
•	Контейнер с Gunicorn + Flask + .env
docker build -t housing-service .
docker run -p 5000:5000 housing-service
Этап 9: Документация и приёмка
 9.2 Ручное тестирование API
Сервис протестирован через запрос:
POST http://localhost:5000/api/predict
Content-Type: application/json
Authorization: Basic YWRtaW46MTIzNA==
{
  "area": 60,
  "floor": 2,
  "floors_count": 5,
  "rooms_count": 3
}
Ответ:
{
  "predicted_price": 6200000.0 ₽
}
 9.3 Метрики модели
Файлы в reports/:
•	metrics.json
•	metrics.txt
•	metrics.csv
Пример:
{
  "R2": 0.82,
  "MAE": 450000.0,
  "RMSE": 600000.0
}
 9.4 Логирование
Все действия и ошибки записываются в service/logs/server.log
________________________________________
Автор
•	GitHub: @Mohab23323232
•	Email: mohab.1994@mail.ru

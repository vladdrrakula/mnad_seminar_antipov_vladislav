from pathlib import Path
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from backend.ml.train import train_model

app = FastAPI()

class TrainRequest(BaseModel):
    filename: str
    model_name: str
    train_size: float = 0.8

@app.post("/train")
def train(req: TrainRequest, background_tasks: BackgroundTasks):

    path = Path("data") / req.filename
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Data file not found")

    background_tasks.add_task(train_model, req.filename, req.model_name, req.train_size)
    return {"message": "Модель отправлена на обучение"}

# НОВАЯ ЧАСТЬ
import joblib
import pandas as pd
from pathlib import Path

class PredictRequest(BaseModel):
    level: float
    levels: float
    rooms: float
    area: float
    kitchen_area: float
    building_type: float
    object_type: float
    level_last: float
    level_first: float

MODEL_PATH = Path("backend/ml/model.pkl")
if MODEL_PATH.exists():
    try:
        my_model = joblib.load(MODEL_PATH)
        print("✅ Твоя модель успешно загружена!")
    except Exception as e:
        my_model = None
        print(f"❌ Ошибка загрузки модели: {e}")
else:
    my_model = None
    print(f"⚠️ Файл модели не найден по пути: {MODEL_PATH}")

@app.post("/predict")
def predict_price(data: PredictRequest):
    """
    Принимает 9 признаков и возвращает предсказание модели
    """
    if my_model is None:
        raise HTTPException(status_code=503, detail="Модель не загружена на сервере")
    
    try:
        input_df = pd.DataFrame([data.dict()])
        
        prediction = my_model.predict(input_df)[0]
        
        return {
            "prediction": float(prediction),
            "message": f"Предсказанное значение: {float(prediction):.3f}"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка во время предсказания: {str(e)}")

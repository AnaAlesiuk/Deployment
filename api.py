from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from joblib import load

app = FastAPI()


class Body(BaseModel):
    input: List[List[float]]


@app.post("/predict")
async def predict(body: Body):
    model = load('get_around_model.joblib')
    predictions = model.predict(body.input)
    return predictions.tolist()


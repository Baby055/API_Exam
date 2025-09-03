from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

cars_db: Dict[str, dict] = {}


class Characteristic(BaseModel):
    max_speed: float
    max_fuel_capacity: float

class Car(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristic

# a
@app.get("/ping")
def ping():
    return "pong"

# b
@app.post("/cars", status_code=201)
def create_car(car: Car):
    cars_db[car.identifier] = car.dict()
    return car

# c
@app.get("/cars", response_model=List[Car])
def get_cars():
    return list(cars_db.values())

# d
@app.get("/cars/{id}", response_model=Car)
def get_car(id: str):
    if id not in cars_db:
        raise HTTPException(status_code=404, detail=f"Car with id '{id}' not found.")
    return cars_db[id]


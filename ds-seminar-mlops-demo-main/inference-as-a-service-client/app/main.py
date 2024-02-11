from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.preprocessing import PolynomialFeatures
import requests

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InputData(BaseModel):
    weight_kg: float
    year: int

def fuel_conversion(fuel):
    g = 3.785411784   # liters per gallon
    m = 1609.344    # meters per mile
    kpg = (g / m * 1000)    # kilometers per gallon 
    return  100 / fuel * kpg    # returns fuel as mpg to l/100km or vice versa

@app.post('/predict_fuel_consumption_l_100_km')
async def predict_fuel_consumption(data: InputData):
    try:
        weight_lbs = data.weight_kg * 2.205
        year_mod_100 = data.year % 100

        input_data = [
            [weight_lbs, year_mod_100]
        ]

        transformed_input = PolynomialFeatures(degree=2).fit_transform(input_data).tolist()

        inference_input = {
            'instances': transformed_input
        }

        print("request: " + str(inference_input))

        # request: {'instances': [[1.0, 26731.215, 31.0, 714557855.376225, 828667.665, 961.0]]}
        # request: {'instances': [[1.0, 26731.215, 31.0, 714557855.376225, 828667.665, 961.0]]}

        response = requests.post(
            "http://172.203.45.190/kserve/v1/models/sklearn-mpg:predict", 
            json=inference_input, 
            headers={"Host": "sklearn-mpg.kserve-deploy-test.example.com"}
        )

        print("response: " + str(response))

        print("response: " + str(response.json()))

        mpg = response.json()["predictions"][0]
        fuel_consumption = fuel_conversion(mpg)

        return {'fuel_consumption_l_100_km': fuel_consumption}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

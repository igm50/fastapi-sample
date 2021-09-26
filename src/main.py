from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

from database import Database
from model import City

app = FastAPI()
db = Database()


class CityOut(BaseModel):
    id: int
    name: str
    country_code: str
    district: str
    population: int

    @classmethod
    def fromCities(cls, cities: List[City]) -> str:
        return [cls.fromCity(city) for city in cities]

    @staticmethod
    def fromCity(city: City) -> str:
        return {"id": city.id, "name": city.name, "country_code": city.country_code, "district": city.district, "population": city.population}


@app.get("/city", response_model=List[CityOut])
def read_city():
    cities = db.read_cities(10)
    return CityOut.fromCities(cities)


@app.get("/city/{city_id}", response_model=CityOut)
def read_city(city_id: int):
    city = db.read_city(city_id)
    return CityOut.fromCity(city)

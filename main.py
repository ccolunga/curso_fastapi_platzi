# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()


# Models

class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'


class Location(BaseModel):
    city: str
    state: str
    country: str


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        example="Cesar"
    )
    last_name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        example="Colunga"
    )
    age: int = Field(
        ...,
        gt=0,
        le=110,
        example="25"
    )
    hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=False)

    # Se crea una clase dentro de la clase person para tomar el siguiente schema de ejemplo
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Cesar",
    #             "last_name": "Colunga",
    #             "age": 26,
    #             "hair_color": "black",
    #             "is_married": False
    #         }
    #     }


@app.get('/')
def home():
    return {"Hello": "World"}


@app.post('/person/new')
# Agregar los 3 puntos seguidos convierte al parametro obligatorio
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters
@app.get('/person/detail')
# Funcion para probar la validacion en los query parameter.
# El Age esta obligatorio, no se recomienda hacer esto, si necesitas un
# parametro obligatorio se recomienda hacerlo en un path parameter
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person Name. It's between 1 and 50 characters",
        example="Rocio"
    ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the age of the person. It's Required",
        example=25
    )
):
    return {name: age}


# Validaciones: Path Parameters
@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is the ID Person",
        examples=123
    )
):
    return {person_id: "It exist!"}


# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    #location: Location = Body(...)
):
    #results = person.dict()
    # results.update(location.dict())
    # return results
    return person

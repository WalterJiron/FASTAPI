# Para las validacion en uso de clases
from pydantic import BaseModel, Field
# Field: sirve para las valivaciones (rangos que queremos que ingresen.)
# BaseModel: Sirve para que una clase se maneje como plantilla.

# Para el manejo de tipos
from typing import Optional

# Para el manejo de la fecha actual
from datetime import datetime


# Clase para la validacion de datos con las funciones
class Movies(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str


class CreateMovie(BaseModel):
    id: int = Field(gt= 0)
    title: str = Field(min_length= 3, max_length= 50)
    overview: str = Field(min_length= 5, max_length= 100)
    year: int = Field(le= datetime.now().year, gt=1650, default= datetime.now().year-1)
    rating: float = Field(ge= 0.00, le= 10.00, default= 5.5)
    category: str = Field(min_length= 3, max_length= 20)

    """
         para los campos enteros se usa:
            gt = mayor que.
            ge = mayores o iguales que. 
            lt = menores que.
            le = menores o iguales que.
    """


class UpdateMovie(BaseModel):
    title: str
    overview: Optional[str]
    year: int
    rating: float
    category: str

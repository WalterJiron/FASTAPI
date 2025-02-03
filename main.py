from fastapi import FastAPI, Path, Query
# Path: se usa para las validaciones  de los parametros tipo ruta
# Query: Para validar los parametro de tipo cueri

# Para mandar HTML.
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse
# HTMLResponse: Responde con contenido HTML
# JSONResponse: Responde con un formato json
# RedirectResponse: responde con una redireccion y el estatus de la redireccion (303)
# FileResponse: Lee y envia el archivo que le pasemos.

from fastapi.exceptions import HTTPException
# HTTPException: se usa en caso de excepciones (posibles errores o porblemas)

# Para las validacion en uso de clases
from pydantic import BaseModel, Field   
# Field: sirve para las valivaciones (rangos que queremos que ingresen.)
# BaseModel: Sirve para que una clase se maneje como plantilla.

# Para el manejo de tipos
from typing import Optional, List  

# Para el manejo de la fecha actual
from datetime import datetime

app = FastAPI()

app.title = 'Documentacion Fastapi'   # Titulo de la documentacion



# Clase para la validacion de datos con las funciones
class Movies(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str


# Arcivos con los  que travajamos 
movies: List[Movies] = []



class CreateMovie(BaseModel):
    id: Optional[int] = Field(gt= len(movies), lt= len(movies)+2, default_factory= lambda: len(movies) +1)
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


# ------------------------------ peticiones HTTPS - get ------------------------------ #

@app.get('/', tags=['Home'])
def home():
    return HTMLResponse('<h1> Hola mundo.</h1>')

# Mostar las movies
@app.get('/movies', tags=['Movies'])
def get_movies() -> List[Movies]:
    if movies:
        contenido = [movie.model_dump() for movie in movies]
        return JSONResponse(content=contenido)
    return HTTPException(status_code=404, detail='Movies no encontradas')
    

# Buscar una movie por el id
@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(gt=0)) -> Movies:
    for movie in movies:
        if movie.id == id:
            return JSONResponse(content= movie.model_dump(),)
    raise HTTPException(status_code=404, detail="Movie no encontrada")

# Filtrar una movie por category y year 
@app.get('/movies/', tags=['Movies'])
def filter_movie(
    category: str = Query(min_length= 3, max_length= 20), 
    year: int = Query(gt=1650, le= datetime.now().year)
) -> Movies:
    for movie in movies:
        if (movie.category.lower() == category.lower()) and (movie.year == year):
            return JSONResponse(content= movie.model_dump())
    raise HTTPException(status_code=404, detail="Movie no encontrada")

# Agregar una nueva movie
@app.post('/movies', tags=['Movies'], status_code= 201)
def post_movie(movie: CreateMovie) -> RedirectResponse:
    new_movie = Movies(**movie.model_dump())  # Convertir CreateMovie a Movies
    movies.append(new_movie)
    return RedirectResponse('/movies', status_code=303)

# Actualizar una movie 
@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, update_movie: UpdateMovie) -> Movies:
    for movie in movies:
        if movie.id == id:
            if update_movie.title:
                movie.title = update_movie.title
            if update_movie.overview:
                movie.overview = update_movie.overview
            if update_movie.year:
                movie.year = update_movie.year
            if update_movie.rating:
                movie.rating = update_movie.rating
            if update_movie.category:
                movie.category = update_movie.category
            return JSONResponse(content= movie.model_dump())
    raise HTTPException(status_code=404, detail="Movie no encontrada")

# Eliminar una movie
@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int) -> RedirectResponse:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
            return RedirectResponse('/movies', status_code= 303)
    raise HTTPException(status_code=404, detail="Movie no encontrada")


# -------------------------- AGREGAR PDFS -------------------------- #
@app.get('/fastapi_MVC/PDF', tags=['PDFS'])
def get_pdf() -> FileResponse:
    return FileResponse('FASTAPI-MVC.pdf')
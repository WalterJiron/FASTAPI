from fastapi import Path, Query, APIRouter
# Path: se usa para las validaciones  de los parametros tipo ruta
# Query: Para validar los parametro de tipo cueri

# Para mandar tipos de respuestas
from fastapi.responses import JSONResponse, RedirectResponse
# JSONResponse: Responde con un formato json
# RedirectResponse: responde con una redireccion y el estatus de la redireccion (303)
# FileResponse: Lee y envia el archivo que le pasemos.

# Para los tipos de excepciones
from fastapi.exceptions import HTTPException
# HTTPException: se usa en caso de excepciones (posibles errores o porblemas)

# Para el manejo de tipos
from typing import List

# Para el manejo de la fecha actual
from datetime import datetime

# Llamada a los modelos de los muvies
from src.models.movie_model import Movies, CreateMovie, UpdateMovie

movie_router = APIRouter()


# Arcivos con los  que travajamos 
movies: List[Movies] = []


# Mostar las movies
@movie_router.get('/movies', tags=['Movies'])
def get_movies() -> List[Movies]:
    if movies:
        contenido = [movie.model_dump() for movie in movies]
        return JSONResponse(content=contenido)
    return HTTPException(status_code= 500, detail='No hay movies registradas')
    

# Buscar una movie por el id
@movie_router.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(gt=0)) -> Movies:
    for movie in movies:
        if movie.id == id:
            return JSONResponse(content= movie.model_dump(),)
    raise HTTPException(status_code=404, detail="Movie no encontrada")


# Filtrar una movie por category y year 
@movie_router.get('/movies/', tags=['Movies'])
def filter_movie(
    category: str = Query(min_length= 3, max_length= 20), 
    year: int = Query(gt=1650, le= datetime.now().year)
) -> List[Movies]:
    if not movies:
        return HTTPException(status_code=404, detail= 'La lista de movies esta vacia')
    
    list_movies: List[Movies] = [movie for movie in movies if (movie.category.lower() == category.lower()) and (movie.year == year)]

    if not list_movies:
        raise HTTPException(status_code=404, detail='Movie no encontrada')
    
    return list_movies


# Agregar una nueva movie
@movie_router.post('/movies', tags=['Movies'], status_code= 201)
def post_movie(movie: CreateMovie) -> RedirectResponse:
    movies.append(movie)
    return RedirectResponse('/movies', status_code=303)

# Actualizar una movie 
@movie_router.put('/movies/{id}', tags=['Movies'])
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
@movie_router.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int) -> RedirectResponse:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
            return RedirectResponse('/movies', status_code= 303)
    raise HTTPException(status_code=404, detail="Movie no encontrada")

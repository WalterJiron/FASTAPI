from fastapi import FastAPI

# Para mandar HTML.
from fastapi.responses import HTMLResponse, FileResponse
# HTMLResponse: Responde con contenido HTML
# FileResponse: Lee y envia el archivo que le pasemos.

# LLamamos a las rutas de movies
from src.routers.movie_router import movie_router


app = FastAPI()

app.title = 'Documentacion Fastapi'   # Titulo de la documentacion



@app.get('/', tags=['Home'])
def home():
    return HTMLResponse('<h1> Hola mundo.</h1>')

# ------------------------------ peticiones HTTP de movies ------------------------------ #
# Agregamos las rutas que importamos
app.include_router(router= movie_router)



# -------------------------- AGREGAR PDFS -------------------------- #
@app.get('/fastapi_MVC/PDF', tags=['PDFS'])
def get_pdf() -> FileResponse:
    return FileResponse('FASTAPI-MVC.pdf')
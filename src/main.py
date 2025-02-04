from fastapi import FastAPI, status

# Para un mejor manejode las peticiones HTTP
from fastapi.requests import Request
# Request: Sirve para mejora la solicitud HTTP entrantes en FASTAPI.

# Para mandar HTML.
from fastapi.responses import HTMLResponse, FileResponse, Response, JSONResponse
# HTMLResponse: Responde con contenido HTML
# FileResponse: Lee y envia el archivo que le pasemos.
# Response: Responde con contenido personalizado.
# JSONResponse: Responde con contenido JSON.

# LLamamos a las rutas de movies
from src.routers.movie_router import movie_router


app = FastAPI()

app.title = 'Documentacion Fastapi'   # Titulo de la documentacion

# Creamos un middleware para un mejor manejo de errores de nuestro codigo.
@app.middleware('http')
async def  http_error_handle(request: Request, call_nex) -> Response | JSONResponse:
    try:
        return await call_nex(request)
    except Exception as e:
        content = f'eror: {str(e)}'
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(content= content, status_code= status_code)


@app.get('/', tags=['Home'])
def home():
    return HTMLResponse('<h1> Hola mundo.</h1>')

# ------------------------------ peticiones HTTP de movies ------------------------------ #
# Agregamos las rutas que importamos
app.include_router(router= movie_router)



# -------------------------- AGREGAR PDFS -------------------------- #
@app.get('/fastapi_MVC/PDF', tags=['PDFS'])
def get_pdf() -> FileResponse:
    return FileResponse('src/FASTAPI-MVC.pdf')
```markdown
# FastAPI Application

This module contains the main settings and routes for the FastAPI application.

## Imports

- **FastAPI**: Main framework for creating web applications.
- **Path, Query**: Used for validations of route and query parameters.
- **HTMLResponse, JSONResponse, RedirectResponse, FileResponse**: Responses for different types of content.
- **HTTPException**: HTTP exception handling.
- **BaseModel, Field**: Validations and data management with Pydantic.
- **Optional, List**: Data types for type annotations.
- **date and time**: Management of dates and times.

## Classes

- **Movies**: Data model for movies.
- **CreateMovie**: Model for creating new films with validations.
- **UpdateMovie**: Model for updating movies.

## Routes

- **GET /**: Home page.
- **GET /movies**: Get all the movies.
- **GET /movies/{id}**: Get a movie by ID.
- **GET /movies/**: Filter movies by category and year.
- **POST /movies**: Add a new movie.
- **PUT /movies/{id}**: Update an existing movie.
- **DELETE /movies/{id}**: Delete a movie.
- **GET /fastapi_MVC/PDF**: Get a PDF file.

## To Run

```bash
uvicorn main:app --reload
```
```
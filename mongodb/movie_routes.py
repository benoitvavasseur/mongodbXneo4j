import re
from typing import List
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi import Response
from fastapi.encoders import jsonable_encoder

from models import Movie, MovieUpdate, User, MoviesNeo4j

router = APIRouter()

@router.get("/", response_description="List all movies", response_model=List[Movie])
def list_movies(request: Request):
    if(movies := request.app.database["movies"].find(limit=10)) is not None:
        return movies
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movies not found")


@router.get("/search/", response_description="Search for a movie by title or actor", response_model=List[Movie])
def search_movies(request: Request, title: Optional[str] = None, actor: Optional[str] = None):
    query = {}
    if title:
        regex_title = re.compile(re.escape(title), re.IGNORECASE)  # Case-insensitive regex for title
        query["title"] = regex_title
    if actor:
        regex_actor = re.compile(re.escape(actor), re.IGNORECASE)  # Case-insensitive regex for actor
        query["cast"] = regex_actor

    movies = request.app.database["movies"].find(query)
    return list(movies)


@router.put("/update/", response_description="Update a movie by title", response_model=Movie)
def update_movie_by_title(request: Request, title: str, movie: MovieUpdate = Body(...)):
    movie_data = {k: v for k, v in movie.model_dump().items() if v is not None}

    if len(movie_data) >= 1:
        update_result = request.app.database["movies"].update_one(
            {"title": title}, {"$set": movie_data}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with title '{title}' not found")

    updated_movie = request.app.database["movies"].find_one({"title": title})
    if updated_movie:
        return updated_movie

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with title '{title}' not found")


@router.get("/users_rated_movie/", response_description="List all users who rated a movie", response_model=List[User])
def users_rated_movie(request: Request, title: str):
    users = request.app.neo4j_driver.session().run(
        "MATCH (p:Person)-[:REVIEWED]->(:Movie {title: $title}) RETURN p", title=title
    )

    return users

@router.get("/movies_rated_by_user/", response_description="List all movies rated by a user")
def movies_rated_by_user(request: Request, name: str):
    movies = request.app.neo4j_driver.session().run(
        "MATCH (:Person {name:$name}) - [:REVIEWED] -> (m:Movie) RETURN COUNT(m), COLLECT(m) ", name=name
    )
    data = movies.single()
    return{"user": name, "count": data[0], "movies": data[1]}
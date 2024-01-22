"""
@file movies_routes
@brief FastAPI Movie API

This module defines FastAPI routes for managing movies, including listing, searching, updating,
and retrieving information about movies and users.

@note This API assumes the use of MongoDB and Neo4j databases for storing movie and user
        information.

@attention  Before running this API, ensure that the required dependencies, such as FastAPI,
    PyMongo, and Neo4j, are installed.

@section movies_routes Movie Routes
This section contains FastAPI routes related to movie management.
"""

import re
from typing import List
from typing import Optional

from fastapi import APIRouter, Body, Request, HTTPException, status

from models import Movie, MovieUpdate, User

# Init the API Router
router = APIRouter()


"""
@fn list_movies
@brief List all movies.

This route returns a list of movies from the MongoDB database.

@param request: The FastAPI Request object.
@return: A list of movies.
@exception HTTPException: If movies are not found, a 404 error is raised.

@see models.Movie
"""
@router.get("/", response_description="List all movies", response_model=List[Movie])
def list_movies(request: Request):
    if(movies := request.app.database["movies"].find(limit=10)) is not None:
        return movies
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movies not found")


"""
@fn search_movies
@brief Search for a movie by title or actor.

This route allows searching for movies based on title or actor.
It uses regular expressions for case-insensitive matching.

@param request: The FastAPI Request object.
@param title: Optional. The title of the movie to search for.
@param actor: Optional. The actor's name to search for.
@exception HTTPException: If no movie with the specified title or actor is found,
a 404 error is raised.

@return: A list of matching movies.
"""
@router.get("/search/", response_description="Search for a movie by title or actor",
            response_model=List[Movie])
def search_movies(request: Request, title: Optional[str] = None, actor: Optional[str] = None):
    query = {}
    if title:
        regex_title = re.compile(re.escape(title), re.IGNORECASE)  # Case-insensitive regex for title
        query["title"] = regex_title
    if actor:
        regex_actor = re.compile(re.escape(actor), re.IGNORECASE)  # Case-insensitive regex for actor
        query["cast"] = regex_actor

    movies = request.app.database["movies"].find(query)
    if movies:
        return list(movies)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movies not found")


"""
@fn update_movie_by_title
@brief Update a movie by title.

This route allows updating movie information, including title, plot, genres, etc.,
based on the specified title.

@param request: The FastAPI Request object.
@param title: The title of the movie to update.
@param movie: The updated movie information.
@return: The updated movie.
@exception HTTPException: If the movie with the specified title is not found, a 404 error is raised.

@see models.Movie
@see models.MovieUpdate
"""
@router.put("/update/", response_description="Update a movie by title", response_model=Movie)
def update_movie_by_title(request: Request, title: str, movie: MovieUpdate = Body(...)):
    movie_data = {k: v for k, v in movie.model_dump().items() if v is not None}

    if len(movie_data) >= 1:
        update_result = request.app.database["movies"].update_one(
            {"title": title}, {"$set": movie_data}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Movie with title '{title}' not found")

    updated_movie = request.app.database["movies"].find_one({"title": title})
    if updated_movie:
        return updated_movie

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Movie with title '{title}' not found")


"""
@fn common_movies_count
@brief Count of movies common between MongoDB and Neo4j databases.

This route queries both MongoDB and Neo4j databases to find movies with matching titles and returns
the count along with a list of common movie titles.

@param request: The FastAPI Request object.
@return: A dictionary containing the common movies count and a list of common movie titles.
@exception HTTPException: If common movies are not found, a 404 error is raised.
"""
@router.get("/common_movies_count",
            response_description="Count of movies common between MongoDB and Neo4j")
def common_movies_count(request: Request):
    mongodb_movies = request.app.database["movies"].find({}, {"title": 1})
    mongodb_titles = {movie["title"] for movie in mongodb_movies}
    

    with request.app.neo4j_driver.session() as session:
        query = """
        MATCH (m:Movie)
        WHERE m.title IN $titles
        RETURN m.title
        """
        result = session.run(query, titles=list(mongodb_titles))
        neo4j_titles = {record["m.title"] for record in result}

    common_movies = mongodb_titles.intersection(neo4j_titles)
    if common_movies:
        return {"common_movies_count": len(common_movies), "m.title": list(common_movies)}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Common movies not found")       


"""
@fn users_rated_movie
@brief List all users who rated a specified movie.

This route retrieves information about users who have reviewed and rated a specific movie in the
Neo4j database.

@param request: The FastAPI Request object.
@param title: The title of the movie to retrieve user ratings.
@return: A list of users who rated the specified movie.
@exception HTTPException: If users who rated the movie are not found, a 404 error is raised.

@see models.User
"""
@router.get("/users_rated_movie/", response_description="List all users who rated a movie",
            response_model=List[User])
def users_rated_movie(request: Request, title: str):
    users = request.app.neo4j_driver.session().run(
        "MATCH (p:Person)-[:REVIEWED]->(:Movie {title: $title}) RETURN p", title=title
    )

    if users:
        return users
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Users who rated movie '{title}' not found")


"""
@fn movies_rated_by_user
@brief List all movies rated by a user.

This route retrieves information about movies that a specific user has reviewed and rated in the
Neo4j database.

@param request: The FastAPI Request object.
@param name: The name of the user to retrieve rated movies.
@return: Information about the movies rated by the specified user.
@exception HTTPException: If movies rated by the user are not found, a 404 error is raised.
"""
@router.get("/movies_rated_by_user/", response_description="List all movies rated by a user")
def movies_rated_by_user(request: Request, name: str):
    movies = request.app.neo4j_driver.session().run(
        "MATCH (:Person {name:$name}) - [:REVIEWED] -> (m:Movie) RETURN COUNT(m), COLLECT(m) ",
        name=name
    )
    data = movies.single()
    if data:
        return{"user": name, "count": data[0], "movies": data[1]}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Movies rated by user '{name}' not found")

import uuid
from typing import Optional
from pydantic import BaseModel, Field
from typing import List


class Movie(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    plot: str = Field(...)
    genres: List[str] = Field(...)
    runtime: int = Field(...)
    cast: List[str] = Field(...)
    poster: str = Field(...)
    title: str = Field(...)
    fullplot: str = Field(...)
    languages: List[str] = Field(...)
    released: str = Field(...)
    directors: List[str] = Field(...)
    writers: List[str] = Field(...)
    rated: str = Field(...)
    awards: dict = Field(...)
    lastupdated: str = Field(...)
    year: int = Field(...)
    imdb: dict = Field(...)
    countries: List[str] = Field(...)
    type: str = Field(...)
    tomatoes: dict = Field(...)
    num_mflix_comments: int = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "plot": "A group of bandits stage a brazen train hold-up, only to find a determined posse hot on their heels.",
                "genres": ["Short", "Western"],
                "runtime": 11,
                "cast": [
                    "A.C. Abadie",
                    "Gilbert M. 'Broncho Billy' Anderson",
                    "George Barnes",
                    "Justus D. Barnes"
                ],
                "poster": "https://m.media-amazon.com/images/M/MV5BMTU3NjE5NzYtYTYyNS00MDVmLWIwYjgtMmYwYWIxZDYyNzU2XkEyXkFqcGdeQXVyNzQzNzQxNzI@._V1_SY1000_SX677_AL_.jpg",
                "title": "The Great Train Robbery",
                "fullplot": "Among the earliest existing films in American cinema - notable as the first film that presented a narrative story to tell - it depicts a group of cowboy outlaws who hold up a train and rob the passengers. They are then pursued by a Sheriff's posse. Several scenes have color included - all hand tinted.",
                "languages": ["English"],
                "released": -2085523200000,
                "directors": ["Edwin S. Porter"],
                "rated": "TV-G",
                "awards": {"wins": 1, "nominations": 0, "text": "1 win."},
                "lastupdated": "2015-08-13 00:27:59.177000000",
                "year": 1903,
                "imdb": {"rating": 7.4, "votes": 9847, "id": 439},
                "countries": ["USA"],
                "type": "movie",
                "tomatoes": {
                    "viewer": {"rating": 3.7, "numReviews": 2559, "meter": 75},
                    "fresh": 6,
                    "critic": {"rating": 7.6, "numReviews": 6, "meter": 100},
                    "rotten": 0,
                    "lastUpdated": {"$date": "2015-08-08T19:16:10.000Z"}
                },
                "num_mflix_comments": 0
            }
        }


class MovieUpdate(BaseModel):
    plot: Optional[str]
    genres: Optional[List[str]]
    runtime: Optional[int]
    cast: Optional[List[str]]
    poster: Optional[str]
    title: Optional[str]
    fullplot: Optional[str]
    languages: Optional[List[str]]
    released: Optional[int]
    directors: Optional[List[str]]
    rated: Optional[str]
    awards: Optional[dict]
    lastupdated: Optional[str]
    year: Optional[int]
    imdb: Optional[dict]
    countries: Optional[List[str]]
    type: Optional[str]
    tomatoes: Optional[dict]
    num_mflix_comments: Optional[int]

    class Config:
        json_schema_extra = {
            "example": {
                "plot": "Updated plot description",
                "genres": ["Drama", "Thriller"],
                "runtime": 120,
                "cast": ["Actor1", "Actor2"],
                "poster": "https://example.com/new_poster.jpg",
                "title": "Updated Movie Title",
                "fullplot": "Updated full plot description",
                "languages": ["English", "French"],
                "released": 1643078400000,  # Timestamp for the release date
                "directors": ["Director1", "Director2"],
                "rated": "R",
                "awards": {"wins": 2, "nominations": 1, "text": "2 wins, 1 nomination"},
                "lastupdated": "2024-01-16 14:30:00.000000000",
                "year": 2022,
                "imdb": {"rating": 8.5, "votes": 15000, "id": 1234},
                "countries": ["USA", "Canada"],
                "type": "movie",
                "tomatoes": {
                    "viewer": {"rating": 4.5, "numReviews": 500, "meter": 90},
                    "fresh": 15,
                    "critic": {"rating": 9.0, "numReviews": 5, "meter": 100},
                    "rotten": 0,
                    "lastUpdated": {"$date": "2024-01-16T14:30:00.000Z"}
                },
                "num_mflix_comments": 10
            }
        }

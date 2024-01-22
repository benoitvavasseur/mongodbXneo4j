from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from movie_routes import router as movie_router
from neo4j import GraphDatabase

config = dotenv_values(".env")

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    # MongoDB client    
    app.mongodb_client = MongoClient(config["CONNECTION_STRING"], server_api=ServerApi('1'))
    app.database = app.mongodb_client.get_database(config["DB_NAME"])

    # Neo4j driver
    app.neo4j_driver = GraphDatabase.driver(
        "bolt://35.171.16.234:7687",
        auth=("neo4j", "foreground-highway-coat")
    )


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(movie_router, tags=["movies"], prefix="/movies")
"""
@file main_movies
@brief FastAPI Application Configuration and Startup Script

This script initializes and configures a FastAPI application with MongoDB and Neo4j connections.
It includes startup and shutdown events to handle database connections.

@attention
To use this script effectively, ensure that the required dependencies in requirements.txt, are
installed.
This script also assumes the presence of a configuration file named '.env' with the required environment
variables. Make sure to create this file and define the necessary variables, such as 
CONNECTION_STRING, DB_NAME, NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD.
"""
from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from movie_routes import router as movie_router
from neo4j import GraphDatabase

config = dotenv_values(".env")

app = FastAPI()

"""
@event
FastAPI Startup Event: `startup_db_client`

This event is triggered on application startup and is responsible for initializing MongoDB and
Neo4j database connections.

@param app: The FastAPI application instance.
@var app.mongodb_client: MongoDB client instance for database operations.
@var app.database: MongoDB database instance for the specified DB_NAME.
@var app.neo4j_driver: Neo4j driver instance for database operations.
"""
@app.on_event("startup")
def startup_db_client():
    # MongoDB client    
    app.mongodb_client = MongoClient(config["CONNECTION_STRING"], server_api=ServerApi('1'))
    app.database = app.mongodb_client.get_database(config["DB_NAME"])

    # Neo4j driver
    app.neo4j_driver = GraphDatabase.driver(
        config["NEO4J_URI"],
        auth=(config["NEO4J_USERNAME"], config["NEO4J_PASSWORD"]),
    )

"""
@event
FastAPI Shutdown Event: `shutdown_db_client`

This event is triggered on application shutdown and is responsible for closing the MongoDB and
Neo4j database connections.

@param app: The FastAPI application instance.
@method app.mongodb_client.close(): Closes the MongoDB client connection.
@method app.neo4j_driver.close(): Closes the Neo4j driver connection.
"""
@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    app.neo4j_driver.close()

app.include_router(movie_router, tags=["movies"], prefix="/movies")
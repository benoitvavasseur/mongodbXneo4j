from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from movie_routes import router as movie_router

config = dotenv_values(".env")

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["CONNECTION_STRING"], server_api=ServerApi('1'))
    print("liste des bases de données:", app.mongodb_client.list_database_names())
    app.database = app.mongodb_client.get_database(config["DB_NAME"])
    print(app.database.list_collection_names())
    print("Nombre de films dans la base de données : ", app.database["movies"].count_documents({}))
    print("Connected to MongoDB")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(movie_router, tags=["movies"], prefix="/movies")
# mongodbXneo4j

## Description
This project consists of a Python application which connects to a MongoDB database (Atlas) to perform Read and Update 
operations on a collection of movies as well as a Neo4j database (Sandbox) to perform Read operations on another 
collection of movies.
One of the routes finds the movies which are in both databases and returns them.

## Installation
A requirements.txt file is provided to install the required packages. To install them, run the following command:
```bash
pip install -r requirements.txt
```

## Modify the .env file
The .env file contains the environment variables used by the application. 
Please modify the following variables:
- CONNECTION_STRING: the connection string to the MongoDB database
- NEO4J_URI: the URI of the Neo4j database
- NEO4J_USERNAME: the username of the Neo4j database
- NEO4J_PASSWORD: the password of the Neo4j database

## Run the application
To run the application, run the following command:
```bash
python -m uvicorn main_movies:app --reload
```

## Access to documentation
By default, the documentation is available at the following address: 
http://127.0.0.1:8000/docs


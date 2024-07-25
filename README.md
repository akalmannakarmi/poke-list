# Poke-List

## Overview
Poke-List is a Python FastAPI project that allows users to search for Pokémon by name and type. The Pokémon data is sourced from PokeAPI. This project uses asyncpg and SQLAlchemy 2 syntax with PostgreSQL.

## Requirements
- Python 3.10+
- Python virtual environment (venv)

## Configuration
### Clone the repository:
```bash
git clone git@github.com:akalmannakarmi/poke-list.git
cd poke-list
```

### Set up your environment variable
Change the DATABASE_URL in the .env file to match your PostgreSQL configuration:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
```

## Initialize Project
To initialize the project, use the following command:
```bash
make init
```
This command will:

Set up the virtual environment
Install required dependencies
Initialize the database

## Run Project
To start the project, run:
```bash
make run
```
This will start the FastAPI server on the default host and port (http://127.0.0.1:8000).

## Clean Project
To clean the project (remove virtual environment and other generated files), use:
```bash
make clean
```

## Run Project in Docker
To start the project inside a docker container:
```bash
make dock
```
The Docker setup does not support connecting to a database on localhost. Instead, use an external database URL. Update the .env file with the correct database URL for the external database. Ensure that the Docker container has network access to the external database.

## Usage
### Endpoints

#### JSON Data Endpoint:
```
GET /api/v1/pokemons
```
Returns Pokémon data in JSON format.


#### Web Page Endpoint:
```
GET /api/v2/pokemons
```
Returns a web page with Pokémon data.

### Query Parameters

Both endpoints support the following query parameters:

- name: Filter Pokémon by name.
- type: Filter Pokémon by type.
- limit: Limit the number of results returned.
- offset: Offset the results for pagination.

#### Example Requests

-Get all Pokémon of type "fire":
```
GET /api/v1/pokemons?type=fire
```

- Get Pokémon with name "pikachu":
```
GET /api/v2/pokemons?name=pikachu
```

- Get the first 10 Pokémon:
```
GET /api/v1/pokemons?limit=10
```

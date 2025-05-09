## Call center simulation

A simulation of a call center using FastAPI and PostgreSQL.

###  Results

There are two short videos, one with the demo and the other with a brief explanation of the implementation of the challenge agents.

Demo.mov (4:18)
Arquitectura.mov (3:57) 

number of **results** are the output results of running the 3 agent cases


## Prerequisites

- Docker
- Python 3.10+
- Poetry

###  Set Up the Database

The application uses PostgreSQL as its database. Use Docker to set it up:

1. Build the Docker image:

```
docker build -t postgres-call-center .
```

2. Run the container:

```
docker run -d --name postgres-container-call-center -p 5432:5432 postgres-call-center
```

###  Run

The application was built using fastAPI and Poetry as manger dependency 

1. Install dependencies with poetry

```
poetry install

```
1. start server from the root of the project  

```
uvicorn src.callcentersimulation.main:app --reload --app-dir .
```

Alternatively, you can run the application using runserver.py if you are working within PyCharm.


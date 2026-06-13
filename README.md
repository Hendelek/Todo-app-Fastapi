# Todo App — FastAPI + PostgreSQL

As part of a backend development internship, I was given a ready-made React frontend and tasked with building the backend from scratch. The frontend was untouchable — the goal was simply to make everything work together.

## What I built

A REST API using FastAPI connected to PostgreSQL via SQLAlchemy ORM. The project follows a layered architecture — models, schemas, repositories, services, routers. The database runs in Docker.

## Stack

- Python, FastAPI, Uvicorn
- SQLAlchemy ORM, PostgreSQL, psycopg
- Docker
- React (frontend — provided by mentor)

## Architecture
app/

├── api/

│   ├── routers/       # HTTP endpoints

│   └── dependencies.py

├── models/            # ORM models

├── schemas/           # Pydantic schemas

├── repositories/      # Database layer

├── services/          # Business logic

├── core/              # Config

└── db/                # Session and engine

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks | Get all tasks |
| POST | /tasks | Create a task |
| PATCH | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |
| GET | /categories | Get all categories |
| POST | /categories | Create a category |
| PATCH | /categories/{id} | Update a category |
| DELETE | /categories/{id} | Delete a category |

## Getting started

**1. Start PostgreSQL with Docker**

```bash
docker run -d --name pg-container -e POSTGRES_PASSWORD=admin -e POSTGRES_USER=postgres -e POSTGRES_DB=postgres -p 15432:5432 -v pgdata:/var/lib/postgresql/data postgres:16
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the server**

```bash
uvicorn app.main:app --port 8080 --reload
```

Frontend: `http://localhost:3000`  
Backend: `http://localhost:8080`

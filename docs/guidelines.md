# Code Guildelines - BeeM

---

## Table of Contents

- [General Principles](#general-principles)
- [Python Guidelines](#python-guidelines)
  - [Code Style](#code-style)
  - [Structure and Organization](#structure-and-organization)
  - [Type Hinting](#type-hinting)
  - [Testing](#testing)
- [FastAPI Guidelines](#fastapi-guidelines)
  - [Project Structure](#project-structure)
  - [API Design](#api-design)
  - [Error Handling](#error-handling)
- [Docker Guidelines](#docker-guidelines)
  - [Best Practices](#best-practices)
  - [Dockerfile Structure](#dockerfile-structure)
  - [Docker Compose](#docker-compose)
- [PostgreSQL Guidelines](#postgresql-guidelines)
  - [Database Design](#database-design)
  - [Connection Management](#connection-management)
- [MongoDB Guidelines](#mongodb-guidelines)
  - [Schema Design](#schema-design)
  - [Indexes and Queries](#indexes-and-queries)
  - [Connection Pooling](#connection-pooling)
- [Redis Guidelines](#redis-guidelines)
  - [Best Practices](#best-practices)
  - [Cache Design](#cache-design)
  - [Persistence](#persistence)
- [Airflow Guidelines](#airflow-guidelines)
  - [DAG Design](#dag-design)
  - [Task Management](#task-management)
  - [Monitoring and Logging](#monitoring-and-logging)
- [Grafana Guidelines](#grafana-guidelines)
  - [Dashboard Design](#dashboard-design)
  - [Metrics and Alerts](#metrics-and-alerts)
  - [Authentication and Security](#authentication-and-security)
- [Security Best Practices](#security-best-practices)

---

## General Principles
**Consistency:**
- Always follow the same conventions throughout the project. 
- Use linters and formatters where possible to enforce these conventions.

**Clean Code:**
- Aim for readable, maintainable, and well-documented code.

**Unit Test:**
- Start a new feature by coding unit tests.

**Error Handling:**
- Ensure robust error handling, especially for I/O operations, database transactions, and external APIs.
- Apply features when an error occurs.

**Security:**
- Always consider security aspects, especially when dealing with external data and user input.
- Never hardcode credentials, use environment variables and secrets !

**Logs:**
- Add logs & debug statements to avoid losing time when coding or to solve an issue.
- Even for a functional code, keep logs and a way to analyze them.

---

## Python Guidelines

### Code Style

- **Follow [PEP8](https://peps.python.org/pep-0008/)** as the main guideline for Python code style. 
- **Use [`black`](https://github.com/psf/black)** for formatting and **[`flake8`](https://flake8.pycqa.org/en/latest/)** for linting. ->
- **Type Hinting**: Include type hints to improve code clarity. (See [Type Hinting](#type-hinting) below)
- **Write Unit Tests**: Use `pytest` for unit testing. (See [Testing](#testing))
- **Define a convention for you Classes, Functions, variables names**
```python
PORT = 8080 # Const is UPPERCASE
client_name # Variables use snake case
sumAllNumbers # Functions start with lowercase and then use uppercase for each word composing the name
CompanyClient # Classes start with uppercase and continue for each word composing the name
```

### Structure and Organization

- **Organize code into modules**: Structure your project to separate concerns.
- **Use meaningful names**: For modules, functions, variables, and classes.
- **Keep functions small**: Each function should ideally do one thing and do it well.

### Type Hinting

- Use Python's built-in type hinting to make code clearer and easier to understand:
  
```python
def process_data(data: List[str]) -> int:
    return len(data)
```

### Testing
- Write unit tests using pytest. Aim for high test coverage for critical parts of the codebase.
- Use pytest fixtures to set up reusable test data.

### Venv
- Use Virtual Environments for developing, testing.
- Do not use a single global Venv for all your tasks.
- Choose one Venv stack at the beginning of the project, use it as a convention (ex: Python3 Venv ; Conda ; Poetry ; ..)
- Make sure your venv are added to .gitignore and add requirements.txt files for the contributors.


## FastAPI Guidelines

### Project Structure
Organize your FastAPI project as follows:
```
app/
  ├── main.py       # Entry point for FastAPI app
  ├── routers/      # API routes
  ├── models/       # Pydantic models and DB models
  ├── services/     # Business logic
  ├── utils/        # Helper functions
```

Some explanations about the directories:
``` markdown
# main.py:
This is the entry point for your FastAPI (or Flask) application. It is the file where you initialize the FastAPI or Flask app and define the main settings, routes, and middleware that tie everything together.

**Responsibilities:**
- Initialize the FastAPI/Flask instance.
- Register routers (API endpoints) or Blueprints in Flask.
- Configure middleware (e.g., CORS, security, logging).
- Set up application-level configurations (e.g., environment variables, error handlers).
- Optionally, run the server (e.g., uvicorn.run(app) in FastAPI, app.run() in Flask).
```


``` markdown
# routers/:
- This folder contains API route definitions (aka endpoints).
- These files define how the application responds to HTTP requests (GET, POST, PUT, DELETE, etc.).
- The routers are typically split by functionality (e.g., user_router.py, item_router.py), making it easier to manage and scale.

**Responsibilities:**
- Define the various HTTP methods (GET, POST, etc.) and the paths for your API endpoints.
- Connect with the appropriate services to execute business logic.
Handle request and response validation using Pydantic models.

Example content in routers/:
- user_router.py: Contains endpoints like /users/, /users/{user_id}, for managing user data.
- item_router.py: Contains endpoints like /items/, /items/{item_id}, for handling item-related operations.
```

``` markdown
# models/:
- The models directory contains the Pydantic models and database models.
- These models are used for data validation, serialization, and database schema definition.

**- Pydantic models:** Used by FastAPI for data validation and request/response handling. They ensure that the incoming request data and outgoing responses are correctly structured.
**- Database models:** Define how your data is structured in the database using ORM (Object-Relational Mapping) libraries like SQLAlchemy.
```
Example content in models/:
``` python
# user.py
# #Defines both the Pydantic models and SQLAlchemy models for users. For example:

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

# Pydantic model for request validation
class UserCreate(BaseModel):
    username: str
    email: str

# SQLAlchemy model for the database schema
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
```


``` markdown
# services/
- The services folder is where the business logic of your application is stored.
- This is where you define the main actions related to your business operations, separate from route handling or data validation (which is handled in models or Pydantic).

Business logic: Services contain functions or classes that perform complex tasks, such as interacting with databases, external APIs, or executing domain-specific algorithms.

Example of content in services/:
- user_service.py: containing functions like create_user(), get_user_by_id(), update_user(), etc.
- payment_service.py: containing business logic for payment processing, such as process_payment(), refund_payment(), etc.
- auth_service.py: handling authentication, authorization, password hashing, etc.
- Services are designed to be used by the routers (in routers/), which handle the HTTP/REST part and define how clients interact with your API.
``` 

``` markdown
# utils/
- The utils folder contains utility functions or helpers—generic functions that can be reused across different parts of the project.
- This folder gathers everything that may not be specific to business logic but helps with development.

Utility functions: These functions help avoid code duplication by centralizing common or recurring tasks, such as date formatting, sending emails, simple input validation, etc.

Example of content in utils/:
- date_utils.py: functions to manipulate dates and times, such as format_date(), parse_datetime().
- email_utils.py: functions for sending emails or validating email addresses, such as send_email(), is_valid_email().
- token_utils.py: for generating, signing, or validating JWT tokens or other types of tokens.
``` 




### API Design
- Use RESTful principles: Make sure your API endpoints follow REST conventions (GET, POST, PUT, DELETE).
- Version your API: Always version your API to support backward compatibility.
- Pydantic Models: Use Pydantic models for request validation and serialization.


### Error Handling
Handle errors gracefully using HTTPException and custom exception handlers.
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
```

## Docker Guidelines
### Best Practices
- Use official base images where possible.
- Minimize image layers: Combine RUN instructions in Dockerfiles to reduce image size.
- Use .dockerignore: Exclude unnecessary files from your Docker build context using .dockerignore.
- Submit your images to a vulnerability test ([Docker Scout](https://docs.docker.com/scout/))

### Dockerfile Structure
Example of a simple FastAPI Dockerfile:
```Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
- Use Docker Compose to define and manage multi-container environments (e.g., FastAPI, PostgreSQL, Redis, etc.).
- Do not combine all your services in only one docker-compose file if not needed
``` yaml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres
    environment:
    MY_ENV_VAR: my_value
```

## PostgreSQL Guidelines
### Database Design
- Follow normalization principles to avoid data redundancy and ensure efficient querying.
- Use indexes for frequently queried fields to improve performance.

### Connection Management
- Use a connection pool (e.g., asyncpg or psycopg2) for efficient connection management.


## MongoDB Guidelines
### Schema Design
- Design Documents with Denormalization in Mind: MongoDB is designed for document-based storage, so consider embedding related data when necessary.
- Avoid Massive Documents: Ensure that no document grows too large by proper data partitioning or design.

### Indexes and Queries
- Optimize Queries with Indexes: Always monitor query performance using explain().
- Use Compound Indexes: When multiple fields are queried together, create compound indexes to speed up those queries.

### Connection Pooling
- Use connection pooling to avoid opening and closing connections repeatedly, especially in high-traffic environments.

Example:
``` python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.my_database
```


## Redis Guidelines
### Best Practices
- Use Redis as a Cache: Redis is excellent for caching purposes. Store frequently accessed data like API responses or session information.
- Expiration Policies: Always set an expiration (TTL) on cached data.
### Cache Design
- Cache-In-Front: Implement a cache-in-front pattern where Redis caches the result of database queries or expensive computations.
### Persistence
- Rely on In-Memory First: Redis is primarily an in-memory store. Only enable persistence (RDB or AOF) if needed for specific use cases where data durability is important.
``` python
import aioredis

redis = await aioredis.create_redis_pool('redis://localhost')
```

## Airflow Guidelines
### DAG Design
- DAG Modularity: Write reusable and modular DAGs.
- Idempotent Tasks: Ensure that tasks are idempotent.
### Task Management
- Task Granularity: Break down complex workflows into smaller tasks that are easy to monitor and debug.

Example DAG structure:
``` python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def process_data():
    pass

with DAG('my_dag', start_date=datetime(2023, 1, 1)) as dag:
    task = PythonOperator(
        task_id='process_data',
        python_callable=process_data
    )
```

### Monitoring and Logging
- Use Airflow logs and set up alerts for task failures using email or webhooks.


## Grafana Guidelines
### Dashboard Design
- Modular Dashboards: Design dashboards to be modular and reusable across different services.
- Use Variables: Utilize Grafana's variables to make dashboards more interactive and flexible.

### Metrics and Alerts
- Set up Alerts: Configure alerts for critical metrics (e.g., CPU usage, database performance).
``` yaml
alert:
  - alert: HighCPUUsage
    expr: node_cpu_seconds_total > 0.9
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High CPU Usage"
```

### Authentication and Security
- Enable Authentication: Ensure that Grafana requires login for access.
- Use Role-Based Access Control (RBAC): Configure roles to control access to dashboards and data sources.

### Security Best Practices
- Use Environment Variables: Always manage secrets using environment variables or a secret management system like Vault.
- Input Validation: Ensure that all user inputs are
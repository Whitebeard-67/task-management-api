# Task Management API

A RESTful task management API built with Python and FastAPI. The project provides user authentication, JWT-protected task management, ownership-based authorization, search, pagination, sorting, input validation, and MySQL database integration.

## Features

- User registration
- Secure password hashing
- User login with JWT authentication
- Protected endpoints using Bearer tokens
- Create, read, update, and delete tasks
- Task ownership authorization
- Task search
- Pagination
- Sorting
- Request validation with Pydantic
- Environment-based configuration
- Automatic database connection cleanup
- Interactive API documentation with Swagger UI

## Tech Stack

- **Python**
- **FastAPI**
- **Uvicorn**
- **MySQL**
- **mysql-connector-python**
- **Pydantic**
- **JWT**
- **Argon2 password hashing**
- **python-dotenv**

## Project Structure

```text
task-management-api/
├── main.py
├── auth.py
├── config.py
├── database.py
├── requirements.txt
├── .env
├── .gitignore
└── routers/
    ├── users.py
    └── tasks.py
```

### Main Components

- `main.py` — creates the FastAPI application and registers routers.
- `routers/users.py` — user registration and login endpoints.
- `routers/tasks.py` — task CRUD, search, pagination, and sorting endpoints.
- `auth.py` — password hashing, JWT creation/verification, and OAuth2 bearer authentication.
- `database.py` — MySQL connection and FastAPI database dependency.
- `config.py` — loads environment variables.
- `.env` — local configuration and secrets. This file should not be committed to Git.

## API Endpoints

### Users

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/users/register` | Register a new user | No |
| POST | `/users/login` | Login and receive JWT | No |

### Tasks

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/tasks` | Get tasks with pagination and sorting | No |
| POST | `/tasks` | Create a task | Yes |
| GET | `/tasks/search` | Search tasks by title | No |
| GET | `/tasks/{task_id}` | Get a task by ID | No |
| PUT | `/tasks/{task_id}` | Update an owned task | Yes |
| DELETE | `/tasks/{task_id}` | Delete an owned task | Yes |

## Authentication

The API uses JWT-based authentication.

1. Register an account using `/users/register`.
2. Login using `/users/login`.
3. The API returns an access token.
4. Send the token with protected requests using:

```text
Authorization: Bearer <your-token>
```

Task creation, updating, and deletion require authentication.

Task updates and deletions are also restricted to the user who owns the task.

## Pagination and Sorting

The `GET /tasks` endpoint supports pagination and sorting.

Example:

```text
GET /tasks?page=1&limit=10&sort=id&order=asc
```

Supported sort fields:

- `id`
- `title`

Supported sort orders:

- `asc`
- `desc`

## Database Setup

Create a MySQL database and the required tables before running the API.

Example database:

```sql
CREATE DATABASE project3;
USE project3;
```

The project requires:

- `users`
- `tasks`

The exact table definitions should match the SQL schema used by the application.

## Environment Variables

Create a `.env` file in the project root:

```env
secretkey=your-secret-key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=project3
```

Do not commit your real `.env` file or secret values to GitHub.

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd task-management-api
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the `.env` file and create the MySQL database/tables.

## Running the API

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Notes

This project was built as a backend learning project to practice REST APIs, authentication, authorization, database integration, dependency injection, validation, and modular FastAPI architecture.

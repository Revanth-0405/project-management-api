# Project Management API

A production-ready REST API for managing projects and tasks using a dual-database architecture:

* **SQL (SQLite)** → Projects
* **NoSQL (DynamoDB Local)** → Tasks

This project demonstrates clean architecture, REST best practices, scalable database design, validation, logging, testing, and containerization.

---

## Architecture Overview

Layered backend architecture:

```
Routes → Services → Database
```

**Design principles used**

* Separation of concerns
* Reusable utilities
* Structured error handling
* Scalable query design
* Clean imports via packages

---

## Tech Stack

| Layer            | Technology       |
| ---------------- | ---------------- |
| Backend          | Python + Flask   |
| ORM              | Flask-SQLAlchemy |
| Relational DB    | SQLite           |
| NoSQL DB         | DynamoDB Local   |
| Testing          | unittest         |
| Containerization | Docker           |

---

## Folder Structure

```
project-management-api/
│
├── models/
├── routes/
├── services/
├── utils/
├── tests/
│
│
├── app.py
├── database.py
├── create_table.py
├── requirements.txt
├── Dockerfile
├── logging_config.py
└── README.md
```

---

## Setup Instructions

### 1 — Install Dependencies

```
pip install -r requirements.txt
```

---

### 2 — Start DynamoDB Local

Run DynamoDB Local separately:

```
java -jar DynamoDBLocal.jar -sharedDb
```

---

### 3 — Create Tasks Table

```
python create_table.py
```

---

### 4 — Run API

```
python app.py
```

Server starts at:

```
http://localhost:5000
```

---

## Docker Run (Optional)

Build image:

```
docker build -t project-api .
```

Run container:

```
docker run -p 5000:5000 project-api
```

---

## API Endpoints

---

### Projects

| Method | Endpoint                     | Description        |
| ------ | ---------------------------- | ------------------ |
| POST   | `/api/projects`              | Create project     |
| GET    | `/api/projects`              | List projects      |
| GET    | `/api/projects/<id>`         | Get project        |
| PUT    | `/api/projects/<id>`         | Update project     |
| DELETE | `/api/projects/<id>`         | Delete project     |
| GET    | `/api/projects/<id>/summary` | Project statistics |

---

### Tasks

| Method | Endpoint                   | Description |
| ------ | -------------------------- | ----------- |
| POST   | `/api/projects/<id>/tasks` | Create task |
| GET    | `/api/projects/<id>/tasks` | List tasks  |
| GET    | `/api/tasks/<task_id>`     | Get task    |
| PUT    | `/api/tasks/<task_id>`     | Update task |
| DELETE | `/api/tasks/<task_id>`     | Delete task |

---

## Example Requests

### Create Project

```
POST /api/projects
{
  "name": "Website Redesign",
  "description": "Revamp UI"
}
```

---

### Create Task

```
POST /api/projects/1/tasks
{
  "title": "Design Homepage",
  "priority": "high"
}
```

---

### Summary Response

```
GET /api/projects/1/summary
```

```
{
 "project_id":1,
 "project_name":"Website Redesign",
 "total_tasks":5,
 "by_status":{"todo":2,"done":1},
 "by_priority":{"high":2,"medium":2,"low":1}
}
```

---

## Query Parameters

Projects list:

```
?page=1
&per_page=5
&status=active
```

Tasks list:

```
?status=todo
?priority=high
```

---

## Validation Rules

* Project name must be unique
* Priority must be: low / medium / high
* Status must be: todo / in_progress / done
* All requests must be JSON

---

## Error Format

All errors follow a consistent structure:

```
{
  "error": "message"
}
```

---

## Running Tests

```
python -m unittest discover tests
```

---

## Design Decisions

Why SQLite + DynamoDB?

| Choice           | Reason                      |
| ---------------- | --------------------------- |
| SQL for Projects | relational integrity        |
| NoSQL for Tasks  | scalable flexible task data |
| Query over Scan  | performance optimized       |
| Service Layer    | business logic isolation    |
| Blueprints       | modular routing             |

---

## Production-Level Practices Implemented

* Structured logging
* Input validation
* Pagination support
* Filtering support
* Global error handler
* Clean package exports
* Environment-safe timestamps
* Docker support
* Unit tests

---

## Performance Considerations

Tasks are queried using DynamoDB partition keys instead of full table scans, ensuring scalable performance as data grows.

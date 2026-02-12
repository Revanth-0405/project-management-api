#  Project Management API

A production-quality RESTful API built using **Flask**, demonstrating clean endpoint design, SQL + NoSQL integration, validation, and structured architecture.

This project satisfies the assessment requirements for:

* Clean RESTful API design
* SQL database integration
* NoSQL database integration
* Proper error handling
* Production-ready code structure

---

#  Tech Stack

### Framework

* Flask

### Databases

* **SQLite** → Projects (Relational Database)
* **DynamoDB Local** → Tasks (Document-Based NoSQL Database)

### Libraries

* Flask
* Flask-SQLAlchemy
* boto3

---

#  Architecture

```
Client
   ↓
Routes (HTTP Layer)
   ↓
Services (Business Logic)
   ↓
Databases
   ├── SQLite (Projects)
   └── DynamoDB Local (Tasks)
```

### Folder Structure

```
project-management-api/
│
├── app.py
├── database.py
├── create_table.py
├── requirements.txt
├── logging_config.py
│
├── models/
├── services/
├── routes/
├── utils/
├── tests/
│
└── Dockerfile
```

---

#  Design Decisions

### 1️ Dual Database Architecture

Projects are stored in SQLite because project data is structured and relational.

Tasks are stored in DynamoDB Local because task data is flexible and benefits from document-based storage.

---

### 2️ UUID for Task IDs

Tasks use UUID instead of incremental integers to ensure global uniqueness and prevent collisions.

---

### 3️ Layered Architecture

Separation of concerns:

* Routes → HTTP handling
* Services → Business logic
* Models → Schema definition
* Utils → Reusable helpers

---

### 4️ Pagination & Filtering

Implemented `page` and `per_page` to prevent large dataset overload and improve scalability.

---

### 5️ Error Handling Strategy

Consistent JSON error responses:

```json
{
  "error": "Error message"
}
```

Supported status codes:

* 200 OK
* 201 Created
* 400 Bad Request
* 404 Not Found
* 409 Conflict
* 500 Internal Server Error

---

#  Setup Instructions

## 1️ Clone Repository

```
git clone https://github.com/yourusername/project-management-api.git
cd project-management-api
```

---

## 2️ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

---

## 3️ Install Dependencies

```
pip install -r requirements.txt
```

---

## 4️ Start DynamoDB Local

Download DynamoDB Local from AWS documentation.

Inside DynamoDB folder:

```
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
```

Keep this running.

---

## 5️ Create Tasks Table

```
python create_table.py
```

---

## 6️ Start Flask Server

```
python app.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

#  API Endpoints

---

##  Projects

### Create Project

```
POST /api/projects
```

### List Projects

```
GET /api/projects?page=1&per_page=5
```

### Get Project

```
GET /api/projects/{id}
```

### Update Project

```
PUT /api/projects/{id}
```

### Delete Project

```
DELETE /api/projects/{id}
```

---

##  Tasks

### Create Task

```
POST /api/projects/{id}/tasks
```

### List Tasks

```
GET /api/projects/{id}/tasks
```

Supports filtering:

```
?status=todo
?priority=high
```

### Get Task

```
GET /api/tasks/{task_id}
```

### Update Task

```
PUT /api/tasks/{task_id}
```

### Delete Task

```
DELETE /api/tasks/{task_id}
```

---

#  curl Examples

---

## Create Project

```
curl -X POST http://127.0.0.1:5000/api/projects \
-H "Content-Type: application/json" \
-d "{\"name\":\"Website Redesign\",\"description\":\"Revamp UI\"}"
```

---

## Get Projects

```
curl http://127.0.0.1:5000/api/projects
```

---

## Create Task

```
curl -X POST http://127.0.0.1:5000/api/projects/1/tasks \
-H "Content-Type: application/json" \
-d "{\"title\":\"Design homepage\",\"priority\":\"high\"}"
```

---

## List Tasks

```
curl http://127.0.0.1:5000/api/projects/1/tasks
```

---

## Update Task

```
curl -X PUT http://127.0.0.1:5000/api/tasks/<task_id> \
-H "Content-Type: application/json" \
-d "{\"status\":\"done\"}"
```

---

## Delete Task

```
curl -X DELETE http://127.0.0.1:5000/api/tasks/<task_id>
```

---

#  Docker (Optional)

Build:

```
docker build -t project-api .
```

Run:

```
docker run -p 5000:5000 project-api
```

---

#  Run Tests

```
python -m unittest
```

---

#  Final Notes

* Ensure DynamoDB Local is running before starting Flask.
* SQLite database file (`projects.db`) is auto-generated.
* No authentication implemented (not required by assessment).
* Follows REST best practices and production-quality structure.

---

#  Assessment Compliance

✔ RESTful Design
✔ SQL Integration
✔ NoSQL Integration
✔ Error Handling
✔ Pagination & Filtering
✔ Production-Quality Structure

---

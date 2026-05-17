#  Vacation Planner API

The Vacation Planner API is a backend system built with FastAPI that helps users plan and manage their trips efficiently.

## Overview

This project covers core backend development concepts including:

- FastAPI fundamentals
- RESTful API design
- SQL database integration
- ORM usage (SQLAlchemy)
- CRUD operations
- JWT-based authentication
- Background tasks
- Environment-based configuration

##  Features

Users can:

- Register and log into the platform
- Create and manage trips
- Build personalized itineraries with daily activities
- Securely access protected routes using JWT authentication

## ⚙️ Setup Instructions
 
### Prerequisites
 
- Python 3.13+
- PostgreSQL
- [uv](https://github.com/astral-sh/uv) package manager
---
### 1. Clone the Repository
 
```bash
git clone https://github.com/13XAVI/Vacations-Planner.git
cd vacation-planner    
```
---
 
### 2. Create a Virtual Environment & Install Dependencies
 
```bash
uv venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows
 
uv pip install -r requirements.txt
# or if using pyproject.toml
uv sync
```
---
 
### 3. Configure Environment Variables
 
Copy the example env file and fill in your values:
 
```bash
.env.example
```
---
 
### 4. Create the Database
 
Make sure PostgreSQL is running, then create your database:
 
```sql
CREATE DATABASE vacation_planner;
```
---
### 5. Run Migrations
 
```bash
alembic upgrade head
```
---
 
### 6. Start the Server
 
```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
```

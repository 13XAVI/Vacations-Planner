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

### 1. Clone the repository

    git clone https://github.com/13XAVI/Vacations-Planner.git
    cd vacation-planner    

### 2. Create virtual environment
    uv venv
### 3. Install the dependencies

If using requirements.txt:

```bash
uv pip install -r requirements.txt
```

If using pyproject.toml:

```bash
uv sync
```

### Running the Application

```bash
uv run uvicorn app.main:app --reload
```

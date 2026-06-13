# Vacation Planner API

The Vacation Planner API is a backend system built with FastAPI that helps users plan and manage their trips, including AI-generated itineraries powered by Claude.

## Overview

This project covers core backend development concepts including:

- FastAPI fundamentals
- RESTful API design
- SQL database integration with async SQLAlchemy
- ORM usage (SQLAlchemy + Alembic migrations)
- CRUD operations
- JWT-based authentication
- LLM integration (Anthropic Claude)
- Environment-based configuration

## Features

Users can:

- Register and log into the platform
- Create and manage trips (destination, days, budget, travel style)
- Generate personalized itineraries using AI, based on their trip details
- Retrieve and update previously generated itineraries
- Securely access all protected routes using JWT authentication

---

## Architecture

### Project Structure

```
app/
├── api/
│   ├── routes/
│   │   ├── auth.py          # Registration and login endpoints
│   │   ├── users.py         # User profile endpoints
│   │   ├── trips.py         # Trip CRUD endpoints
│   │   └── itinerary.py     # Itinerary generation and retrieval
│   └── routes_deps.py       # Shared dependencies (auth, logging middleware)
├── core/
│   ├── base.py              # SQLAlchemy declarative base
│   ├── config.py            # Environment variable settings
│   ├── lifespan_db.py       # DB session factory and startup
│   └── validation.py        # Custom request validation error handler
├── llm/
│   └── prompts.py           # Prompt builder and LLM call logic
├── models/
│   ├── users.py             # Users table
│   ├── trips.py             # Trips table
│   └── itinerary.py         # Itineraries table
├── schemas/
│   ├── users.py             # Pydantic schemas for users
│   ├── trips.py             # Pydantic schemas for trips
│   └── itinerary.py         # Pydantic schemas for itineraries
├── services/
│   ├── auth.py              # Registration and login logic
│   ├── trips.py             # Trip database operations
│   └── itinerary.py         # Itinerary database operations + LLM orchestration
├── utils/
│   └── jwt.py               # Token creation and decoding
└── main.py                  # App entrypoint, middleware, router registration
```

### Request Flow

```
Client
  │
  ▼
FastAPI (main.py)
  │  CORSMiddleware
  │  BaseHTTPMiddleware (request logging)
  │
  ▼
Route Handler (api/routes/)
  │  JWT auth via get_current_user dependency
  │
  ▼
Service Layer (services/)
  │  Business logic and DB queries (AsyncSession)
  │
  ├──► PostgreSQL (via SQLAlchemy async)
  │
  └──► LLM Service (llm/prompts.py)
         │  Builds prompt from trip data
         │  Calls Anthropic API
         └──► Returns structured JSON itinerary
```

### Database Schema

```
users
  id          UUID  PK
  email       TEXT  unique
  username    TEXT
  password    TEXT  (hashed)
  role        TEXT  (user | admin)

trips
  id          UUID  PK
  user_id     UUID  FK → users.id
  destination TEXT
  days        INT
  budget      FLOAT
  trip_style  TEXT

itineraries
  id          UUID  PK
  trip_id     UUID  FK → trips.id
  days        JSON  (AI-generated itinerary data)
```

---

## LLM Integration

Itineraries are generated using [Claude Haiku](https://www.anthropic.com/claude) (`claude-haiku-4-5`) via the Anthropic API.

### How It Works

1. The user sends `POST /itineraries?trip_id=<uuid>` with a valid JWT token.
2. The API reads the trip details (destination, days, budget, travel style) from the database.
3. A structured prompt is built from those details and sent to Claude.
4. Claude returns a JSON array of daily plans, which is validated and saved to the database.
5. The itinerary is returned in the response.

### Prompt Design

The prompt instructs the model to:

- Suggest only real, verifiable places within the destination area
- Keep all costs within the specified total budget
- Match activities to the user's travel style (budget, adventure, luxury, cultural, family)
- Include practical information such as opening hours and booking tips
- Return valid JSON only, with no markdown or extra explanation

### Generation Settings

| Setting | Value | Reason |
|---|---|---|
| Model | `claude-haiku-4-5` | Fast and cost-effective for structured output |
| Temperature | `0.3` | Low — ensures consistent JSON structure with slight variation between users |
| Max tokens | `4000` | Enough for multi-day itineraries with detailed activities |
| System prompt | Yes | Separates role/rules from the per-request content |

### Itinerary JSON Structure

Each generated itinerary follows this format:

```json
[
  {
    "day": 1,
    "theme": "Arrival and City Exploration",
    "activities": [
      {
        "time": "09:00 AM",
        "activity": "Visit Kigali Genocide Memorial",
        "location": "Kigali, Rwanda",
        "estimated_cost": 10.00,
        "notes": "Open daily 8am-5pm. Book tickets in advance."
      }
    ],
    "daily_budget": 85.00,
    "accommodation": "Hotel des Mille Collines, Kigali"
  }
]
```

---

## Setup Instructions

### Prerequisites

- Python 3.13+
- PostgreSQL
- [uv](https://github.com/astral-sh/uv) package manager
- Anthropic API key

### 1. Clone the Repository

```bash
git clone https://github.com/13XAVI/Vacations-Planner.git
cd vacation-planner
```

### 2. Create a Virtual Environment and Install Dependencies

```bash
uv venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows

uv sync
```

### 3. Configure Environment Variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Required variables:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/vacation_planner
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
TOKEN_EXPIRE_MINUTES=60
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 4. Create the Database

```sql
CREATE DATABASE vacation_planner;
```

### 5. Run Migrations

```bash
alembic upgrade head
```

### 6. Start the Server

```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
```

API documentation is available at `http://127.0.0.1:8080/docs` once the server is running.

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | No | Create a new account |
| POST | `/auth/login` | No | Get a JWT token |
| GET | `/users/me` | Yes | Get current user profile |
| POST | `/trips` | Yes | Create a trip |
| GET | `/trips` | Yes | List all trips |
| GET | `/trips/{trip_id}` | Yes | Get a single trip |
| PUT | `/trips/{trip_id}` | Yes | Update a trip |
| DELETE | `/trips/{trip_id}` | Admin | Delete a trip |
| POST | `/itineraries?trip_id=` | Yes | Generate an itinerary for a trip |
| GET | `/itineraries/{trip_id}` | Yes | Retrieve a saved itinerary |
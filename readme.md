# SWC Fantasy Football API

A FastAPI-based REST API providing read-only access to SportsWorldCentral fantasy football data.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Create database (if needed)
python3 database/generate_db.ipynb

# Run the server
uvicorn app.main:app --reload

# Run tests
pytest
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Health check |
| `GET /v0/players` | List players (filter by name, date) |
| `GET /v0/players/{player_id}` | Get player by ID |
| `GET /v0/performances/` | List performances (filter by date) |
| `GET /v0/leagues/` | List leagues |
| `GET /v0/leagues/{league_id}` | Get league by ID |
| `GET /v0/teams/` | List teams (filter by name, league) |
| `GET /v0/counts/` | Get league/team/player counts |

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## Data

- 1018 players
- 20 teams
- 5 leagues
- 17306 performance records
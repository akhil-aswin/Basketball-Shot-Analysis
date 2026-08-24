# NBA Shot Chart

Compare shot charts for any two NBA players, side by side, across any season back to 2017-18. Built on real shot-location data from the `nba_api` stats endpoints, with FastAPI serving a JSON/SVG API and a React frontend for the UI.

## Features

- **Side-by-side comparison** — pick two players and two seasons independently, see shot charts, shooting splits (FG%, 3P%, points per shot), and attempt volume rendered as an SVG court overlay.
- **Player archetypes & similarity** — each player is pre-clustered into a shot-tendency archetype (e.g. "Paint Attacker", "Movement Shooter") based on the zone distribution of their attempts, with a list of the most similar players by shot profile.
- **Filtering** — narrow the player pool by height, weight, experience, position, draft pick, and archetype.
- **9 seasons of data** — 2017-18 through 2025-26.

## Project structure

```
main.py              FastAPI app entrypoint; serves the API and the built frontend
routers/api.py        API routes (/api/players, /api/shots/{id}, /api/seasons)
data.py               nba_api calls + caching for player rosters and shot data
stats.py               Shooting split calculations
chart.py               SVG shot chart rendering
similarity.py          Reads precomputed archetypes/similarity from similarity_data.json
precompute.py           One-off script to (re)generate similarity_data.json
frontend/              React + Vite single-page app
```

`chart_comparison.py`, `template.py`, `chart_comparison_streamlit`-related config, and `.devcontainer/` are a legacy Streamlit version of this app kept for reference.

## Prerequisites

- Python 3.11+
- Node.js 18+

## Setup

### Backend

```bash
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Running locally

Run the API and the frontend dev server in two terminals:

```bash
# Terminal 1 — API on http://localhost:8000
uvicorn main:app --reload

# Terminal 2 — frontend on http://localhost:5173
cd frontend
npm run dev
```

The Vite dev server proxies `/api` requests to `http://localhost:8000` (see `frontend/vite.config.js`), so open `http://localhost:5173`.

## Production build

Build the frontend and let FastAPI serve it directly:

```bash
cd frontend
npm run build
cd ..
uvicorn main:app
```

With `frontend/dist` present, `main.py` mounts the built assets and serves the SPA for all non-API routes on `http://localhost:8000`.

## Regenerating similarity data

Player archetypes and similar-player lists come from `similarity_data.json`, precomputed offline because the NBA stats API is rate-limited:

```bash
python precompute.py
```

This takes roughly 8 minutes per season and should be re-run only when you want to refresh the dataset (e.g. for a new season).

## API

| Endpoint | Description |
|---|---|
| `GET /api/seasons` | List of supported seasons |
| `GET /api/players?season=` | All players active in a season, with archetype |
| `GET /api/shots/{player_id}?slot=&season=` | Shot chart SVG, shooting stats, archetype, and similar players for a player/season |

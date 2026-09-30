# PocketSmart AI — Complete Project

A complete FastAPI + Jinja2 implementation of the supplied PocketSmart AI specification: Home Interior, Party and Jewelry budget planners, authentication, history, Gemini integration and deterministic fallbacks.

## Why FastAPI
The supplied document describes Flask in its early architecture section but later milestones explicitly require FastAPI, `main.py`, FastAPI routes, Jinja2 templates and `/token` authentication. This implementation follows the later FastAPI architecture consistently.

## Current Gemini integration
The original document names Gemini 1.5 Flash Pro. Model availability changes, so the model is configurable through `GEMINI_MODEL` and defaults to `gemini-2.5-flash`. The current Google Gen AI Python SDK is `google-genai`.

## VS Code — Windows
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs.

## Gemini
Put your key in `.env`:
```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```
Without a key the application still runs and uses fallback recommendations, so you can test the complete UI/API first.

## Tests
```bash
pytest -q
```

## Docker
```bash
copy .env.example .env
# edit .env if Gemini is needed
docker compose up --build
```

## API
- POST `/register`
- POST `/login`
- POST `/logout`
- POST `/token`
- GET `/session-info`
- GET `/session-data`
- POST `/generate-home`
- POST `/generate-party`
- POST `/generate-jewelry` (multipart form + optional image)
- GET `/history`
- GET `/recommendations-details/{id}`
- GET `/startup`
- GET `/health`

## Included pages
Home, Register, Login, Dashboard, Home Planner, Party Planner, Jewelry Planner, Recommendation Details and History.

## Data and platform integrations
The app does not scrape or impersonate Amazon, Flipkart, IKEA, Swiggy, Zomato or OYO. It creates search links for those platforms. If official partner APIs are available to you, they can be added behind a service adapter without changing the planner UI.

## Production hardening
Use HTTPS, a production database such as PostgreSQL, a secret manager, secure cookies, CSRF protection for browser cookie flows, rate limiting, email verification and official third-party APIs before deployment.

# Spotify → YouTube Music Playlist Transfer — Project Plan

## Goal

A cross-platform mobile app that transfers a user's Spotify playlists to YouTube Music. This is also a **portfolio/showcase project** — meant to be shown to companies during job applications. Code quality, architectural decisions, and current best practices matter at every step.

## Priority Order

1. **Performance** — correct async/await usage, DB connection pooling, no N+1 queries, a background job system for heavy work (playlist matching).
2. **Security** — encrypted storage of OAuth tokens, secret management via `.env`, rate limiting, input validation with Pydantic, correctly configured CORS, ORM usage against SQL injection, non-root Docker user.
3. **Modern/impressive practices** — Pydantic v2, SQLAlchemy 2.0 async ORM, structured logging, health-check endpoints, well-configured OpenAPI docs, pytest test coverage, a CI/CD-ready project structure.

## Tech Stack

- **Backend:** Python 3.14 + FastAPI, package management with `uv`
- **Database:** PostgreSQL (Docker container)
- **Containerization:** Docker + Docker Compose (backend, db, later Redis)
- **Libraries:** `spotipy`, `ytmusicapi` (unofficial), `rapidfuzz` (song matching)
- **Background jobs:** Celery + Redis or FastAPI BackgroundTasks (decision made with reasoning in Phase 6)
- **Frontend (later):** React Native + Expo
- **IDE:** IntelliJ IDEA (Python plugin)

## Development Approach

At every step: explain what was done, why it was done that way, and how it works. Don't move to the next step until the current one is tested and verified. The user applies each step themselves, on their own machine.

## Folder Structure (backend)

```
melodex-api/
├── app/
│   ├── main.py
│   ├── core/           # config, security, dependencies
│   ├── api/            # routers
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── services/        # spotify_client, ytmusic_client, matcher
│   └── db/             # session, migrations (Alembic)
├── tests/
├── pyproject.toml
├── uv.lock
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Phases (Roadmap)

### Phase 1 — Project skeleton and infrastructure [DONE]
Python 3.14 project with `uv init`, FastAPI + PostgreSQL brought up via Docker Compose, a minimal health-check endpoint, a multi-stage Dockerfile (uv-based, non-root user). Outcome: a skeleton that runs with `docker compose up` and responds on `/health`.

### Phase 2 — Database layer [DONE]
Async SQLAlchemy 2.0 engine/session setup, first models (User, Playlist, Track, TransferJob), migration management with Alembic. Reasoning for the async engine choice and the table design explained in detail.

### Phase 3 — Spotify integration [DONE]
OAuth flow with `spotipy`, encrypted storage of tokens (never on the client), endpoints to fetch the user's playlists.

### Phase 4 — YouTube Music integration [DONE]
Authentication and search/add operations with `ytmusicapi`, the risks that come with an unofficial API and how they're mitigated. Note: switched from OAuth (device flow) to browser-header authentication after hitting an open upstream bug in ytmusicapi's OAuth token handling (search requests returned HTTP 400). Browser auth credentials are valid ~2 years tied to the browser session and require manual regeneration if revoked.

### Phase 5 — Song matching engine
Spotify ↔ YouTube Music song matching algorithm using `rapidfuzz`, a match confidence score, a user-confirmation flow for uncertain matches.

### Phase 6 — Background job system
Reasoned choice between Celery+Redis and FastAPI BackgroundTasks for long-running work like playlist transfers, job status tracking (pending/running/done/failed).

### Phase 7 — API completion, rate limiting, tests
Pydantic validation on all endpoints, rate limiting, CORS configuration, unit/integration tests with pytest, coverage report.

### Phase 8 — Security hardening
Docker container security scan, secret management review, dependency vulnerability scanning.

### Phase 9 — Frontend (React Native + Expo)
Mobile app: login screens, playlist listing, transfer status tracking, backend API integration.

### Phase 10 — CI/CD and release readiness
GitHub Actions test/lint/build pipeline, pushing Docker images to a registry, deployment documentation.

---

**Current status:** Phase 1–4 complete. Starting Phase 5 — song matching engine.
# Quickstart: Full-Stack Web Application (Phase II)

**Feature**: 002-fullstack-web

## Prerequisites

- Python 3.13+ with `uv`
- Node.js 20+ with `npm` (or pnpm/bun)
- Neon PostgreSQL account (free tier: https://neon.tech)
- Git

## Environment Setup

### 1. Neon Database

1. Create a Neon project at https://console.neon.tech
2. Copy the connection string (use the pooled connection endpoint with `-pooler` suffix)
3. Note: Better Auth and backend share the same database

### 2. Backend Setup

```bash
cd backend
cp .env.example .env
# Edit .env with your values:
#   DATABASE_URL=postgresql+psycopg://user:pass@ep-xxx-pooler.region.neon.tech/dbname?sslmode=require
#   JWKS_URL=http://localhost:3000/api/auth/jwks
#   FRONTEND_URL=http://localhost:3000

uv sync
uv run alembic upgrade head   # Run migrations (if using Alembic)
uv run uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend
cp .env.example .env.local
# Edit .env.local with your values:
#   NEXT_PUBLIC_API_URL=http://localhost:8000
#   DATABASE_URL=postgresql://user:pass@ep-xxx.region.neon.tech/dbname?sslmode=require
#   BETTER_AUTH_SECRET=<generate-a-random-secret>
#   BETTER_AUTH_URL=http://localhost:3000

npm install
npm run dev
```

### 4. Verify

1. Open http://localhost:3000 — you should see the sign-in page
2. Register a new account
3. Create a task — it should appear in the list
4. Open http://localhost:8000/docs — FastAPI Swagger UI (for API testing)

## Running Tests

```bash
# Backend
cd backend && uv run pytest -x -q

# Frontend
cd frontend && npm test
```

## Environment Variables Reference

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | Neon PostgreSQL connection (pooled) | `postgresql+psycopg://...` |
| JWKS_URL | Better Auth JWKS endpoint | `http://localhost:3000/api/auth/jwks` |
| FRONTEND_URL | Frontend origin for CORS | `http://localhost:3000` |

### Frontend (.env.local)

| Variable | Description | Example |
|----------|-------------|---------|
| NEXT_PUBLIC_API_URL | Backend API base URL | `http://localhost:8000` |
| DATABASE_URL | Neon PostgreSQL connection (direct, for Better Auth) | `postgresql://...` |
| BETTER_AUTH_SECRET | Secret for signing sessions | Random 32+ char string |
| BETTER_AUTH_URL | Base URL for auth callbacks | `http://localhost:3000` |

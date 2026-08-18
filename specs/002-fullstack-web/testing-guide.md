# Testing Guide: Phase II Web App

How to run the full-stack web app locally and manually verify each feature.

**Prerequisites**: Python 3.13 + `uv`, Node.js 20+, and a Neon PostgreSQL database.

> You need a real Neon database. Both services fail at DNS resolution with the
> placeholder host in `.env.example` (`ENOTFOUND ep-xxx.region.neon.tech`).
> Free tier: https://console.neon.tech

---

## 1. Setup

### Database

Create a Neon project and copy two connection strings from the dashboard:

- **Pooled** (has `-pooler` in the host) → backend
- **Direct** (no `-pooler`) → frontend

Both services share one database: Better Auth owns the `user`/`session`/`account`/
`verification` tables, the backend owns `tasks`.

### Backend

```bash
cd backend
cp .env.example .env
```

Edit `.env`:

```
DATABASE_URL=postgresql+psycopg://<user>:<pass>@<host>-pooler.<region>.neon.tech/<db>?sslmode=require
JWKS_URL=http://localhost:3000/api/auth/jwks
FRONTEND_URL=http://localhost:3000
```

```bash
uv sync --extra dev
uv run uvicorn src.main:app --reload --port 8000
```

Tables are created automatically at startup. There is no migration step —
ignore the `alembic upgrade head` line in `quickstart.md`, Alembic is not
installed and no migrations exist.

### Frontend

```bash
cd frontend
cp .env.example .env.local
```

Edit `.env.local` — note `DATABASE_URL` here is the **direct** (non-pooled) string:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=postgresql://<user>:<pass>@<host>.<region>.neon.tech/<db>?sslmode=require
BETTER_AUTH_SECRET=<random string, 32+ chars>
BETTER_AUTH_URL=http://localhost:3000
```

Generate a secret with `openssl rand -base64 32`.

```bash
npm install
npm run dev
```

Both must run at once: the backend verifies tokens by fetching JWKS from the
frontend at `JWKS_URL`. Open http://localhost:3000.

---

## 2. Feature tests

Each test is independent. Backend logs are JSON on stdout and in
`~/.todo-app-web/app.log`.

### Auth (US1)

| # | Steps | Expected |
|---|-------|----------|
| 1.1 | Visit `/` while logged out | Redirects to `/sign-in` |
| 1.2 | Visit `/dashboard` directly while logged out | Redirects to `/sign-in` — the auth guard blocks it |
| 1.3 | Sign up with a valid email + password | Lands on `/dashboard`, shows your email |
| 1.4 | Sign out, then sign back in | Returns to `/dashboard` |
| 1.5 | Sign in with a wrong password | Inline error, stays on `/sign-in` |
| 1.6 | Visit `/` while logged in | Redirects to `/dashboard` |

### Task CRUD (US2)

| # | Steps | Expected |
|---|-------|----------|
| 2.1 | Create a task titled `Buy groceries` | Appears in the list immediately |
| 2.2 | Create one with every field set (description, priority, category, due date, recurrence, time, reminder) | All values persist after reload |
| 2.3 | Edit a task's title | Updated text shown |
| 2.4 | Delete a task | Confirmation prompt, then it disappears |
| 2.5 | Submit with an empty title | Rejected (backend returns 422) |
| 2.6 | Reload the page | Tasks persist |

**User isolation** — the most important check:

1. Create a task as user A, then sign out.
2. Register user B and open the dashboard.
3. B must see an empty list, never A's tasks.

### Completion + recurrence (US3)

| # | Steps | Expected |
|---|-------|----------|
| 3.1 | Toggle a task complete | Marked done; toggles back on a second click |
| 3.2 | Create a **weekly** task due `2026-03-02`, then complete it | A *new* task appears due `2026-03-09`, incomplete |
| 3.3 | Complete a task with no recurrence | No new task created |

Daily +1 day, weekly +7, monthly +1 month, yearly +1 year.

### Search / filter / sort (US4)

Create a few tasks with differing priorities and categories first.

| # | Steps | Expected |
|---|-------|----------|
| 4.1 | Type a keyword in search | Matches on title *and* description, case-insensitive |
| 4.2 | Filter status `active` / `completed` | Only matching tasks |
| 4.3 | Filter by priority, then category | List narrows correctly |
| 4.4 | Sort by due date / title / priority, asc and desc | Order flips |
| 4.5 | Combine a search with a filter | Both apply together |

### Responsive layout (US5)

DevTools device toolbar, or just resize:

- **1920px** — full layout
- **768px** — tablet; nothing clipped or overlapping
- **375px** — mobile; buttons tappable, no horizontal scroll, forms usable

Check the dashboard, both auth pages, task cards, and the filter bar.

### Error handling

| # | Steps | Expected |
|---|-------|----------|
| 6.1 | Stop the backend (Ctrl-C), then act on a task | Friendly "Can't reach the server" boundary with a working **Try again** |
| 6.2 | Restart the backend, click **Try again** | Recovers without a full page reload |

---

## 3. API testing without the UI

Swagger UI is at http://localhost:8000/docs.

Endpoints require a **JWT**, which you get from `/api/auth/token` (*not*
`/api/auth/get-session` — that returns an opaque session id the backend rejects).

```bash
# Sign in and keep the session cookie
curl -s -c /tmp/c.txt -X POST http://localhost:3000/api/auth/sign-in/email \
  -H 'Content-Type: application/json' \
  -d '{"email":"you@example.com","password":"yourpassword"}'

# Exchange the cookie for a JWT
TOKEN=$(curl -s -b /tmp/c.txt http://localhost:3000/api/auth/token | jq -r .token)

curl -s http://localhost:8000/api/tasks -H "Authorization: Bearer $TOKEN"

curl -s -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"title":"Buy groceries","priority":"high"}'
```

Auth checks worth running:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/api/tasks
# 401 — no token

curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/api/tasks \
  -H "Authorization: Bearer bad.token.here"
# 401 — invalid signature
```

Requesting another user's task by id returns **404**, not 403 — deliberate, so
ids can't be enumerated.

---

## 4. Automated tests

```bash
cd backend && uv run pytest -q     # 36 tests, no database needed
```

`npm test` in `frontend/` is a placeholder that always passes — there is no
frontend test suite yet.

---

## 5. Troubleshooting

| Symptom | Cause |
|---------|-------|
| `ENOTFOUND ep-xxx.region.neon.tech` | Still using the `.env.example` placeholder host |
| `Failed to spawn: pytest` | Ran `uv sync` without `--extra dev` |
| Every task call returns 401 | Backend can't reach `JWKS_URL` — the frontend must be running on port 3000 |
| Backend exits on startup | `DATABASE_URL` unreachable, or missing `?sslmode=require` |
| `exec: .../python3: not found` | Stale `backend/.venv` from a moved directory — `rm -rf .venv && uv sync --extra dev` |
| Sign-up returns 500 | Frontend `DATABASE_URL` wrong; use the **direct**, not pooled, string |

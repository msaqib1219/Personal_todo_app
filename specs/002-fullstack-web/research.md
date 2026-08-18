# Research: Full-Stack Web Application (Phase II)

**Feature**: 002-fullstack-web
**Date**: 2026-03-02

## R1: Better Auth + FastAPI JWT Integration

**Decision**: Use JWKS-based JWT verification (no shared secret).

**Rationale**: Better Auth's JWT plugin uses EdDSA (Ed25519) by default and exposes a JWKS endpoint at `/api/auth/jwks`. FastAPI can verify tokens using `PyJWT` + `cryptography` with `PyJWKClient` to fetch the public key. This is more secure than sharing a secret between services.

**Alternatives considered**:
- Shared BETTER_AUTH_SECRET for HMAC verification — simpler but less secure, couples services
- Session-based auth with cookie forwarding — requires sticky sessions, doesn't scale

**Implementation pattern**:
```python
from jwt import PyJWKClient
jwks_client = PyJWKClient(JWKS_URL)
signing_key = jwks_client.get_signing_key_from_jwt(token)
payload = jwt.decode(token, signing_key.key, algorithms=["EdDSA"])
```

## R2: Neon Serverless PostgreSQL + SQLModel

**Decision**: Use SQLModel with `NullPool` and Neon's PgBouncer pooler endpoint.

**Rationale**: Neon provides a PgBouncer connection pooler (use `-pooler` suffix in hostname). Python apps should use `NullPool` to avoid client-side pooling conflicts with server-side pooling. SSL is required (`sslmode=require`).

**Alternatives considered**:
- Direct connection without pooler — connection overhead per request
- pgbouncer sidecar — unnecessary complexity, Neon provides this built-in

**Connection string format**: `postgresql+psycopg://user:pass@ep-xxx-pooler.region.neon.tech/dbname?sslmode=require`

## R3: Next.js 16 App Router

**Decision**: Use Next.js 16 with App Router (stable, early 2026).

**Rationale**: Next.js 16 is stable with Turbopack as default bundler, React Compiler stable, `use cache` directive, and Partial Prerendering (PPR). Requires Node 20+.

**Alternatives considered**:
- Next.js 15 — works but misses Turbopack defaults and React Compiler stability
- Remix/Nuxt — different ecosystem, no hackathon requirement alignment

## R4: Better Auth + Next.js Setup

**Decision**: Standard Better Auth setup with server/client instances and catch-all API route.

**Rationale**: Well-documented pattern. Server instance in `lib/auth.ts`, client instance in `lib/auth-client.ts`, catch-all route handler at `app/api/auth/[...all]/route.ts`. Better Auth manages its own database tables (user, session, account, verification) in the same Neon database.

**Alternatives considered**:
- NextAuth/Auth.js — mature but Better Auth is the hackathon requirement
- Custom auth — too complex, reinventing the wheel

## R5: API Design — User Scoping

**Decision**: Extract user_id from JWT token, not from URL path parameter.

**Rationale**: The hackathon spec shows `/api/{user_id}/tasks` but this is insecure — any user could pass another user's ID. Instead, the JWT middleware extracts the authenticated user's ID from the token payload. API routes become `/api/tasks` with user scoping enforced server-side.

**Alternatives considered**:
- URL-based user_id with JWT verification that user_id matches — viable but redundant
- URL-based user_id without verification — insecure, rejected

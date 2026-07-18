---
id: 0002
title: Phase II Tech Stack Research
stage: spec
date: 2026-03-02
surface: agent
model: claude-sonnet-4-6
feature: 002-fullstack-web
branch: 001-todo-app
user: saqib
command: research
labels: ["better-auth", "jwt", "neon", "nextjs-16", "fastapi", "sqlmodel"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
tests:
---

## Prompt

Research these specific technical topics for a Phase II todo app migration (Python FastAPI backend + Next.js frontend + Better Auth + Neon PostgreSQL). Only do web research, don't write any code.

1. **Better Auth + FastAPI JWT integration**: How does Better Auth issue JWT tokens that FastAPI can verify? What's the shared secret approach? Search for "better-auth jwt plugin fastapi" and "better-auth python backend jwt verification".

2. **Neon Serverless PostgreSQL + SQLModel**: How to connect SQLModel/SQLAlchemy to Neon DB? Any connection pooling considerations? Search for "neon postgresql sqlmodel python" or "neon db fastapi sqlalchemy".

3. **Next.js 16 App Router**: What's new in Next.js 16? Is it stable? Search for "next.js 16 release" to confirm version availability.

4. **Better Auth setup with Next.js**: Search for "better-auth next.js setup guide 2025 2026" to understand the frontend auth setup.

Return concise findings for each topic with key decisions/patterns.

## Response snapshot

Researched all four topics via web search. Key findings:
1. Better Auth JWT plugin uses EdDSA (Ed25519) by default, exposes /api/auth/jwks for JWKS-based verification. FastAPI verifies via PyJWT + cryptography using PyJWKClient. No shared secret needed.
2. Neon works with SQLModel/SQLAlchemy normally. Use NullPool on Python side with Neon's built-in PgBouncer pooler (-pooler suffix). SSL required. Transaction mode limits apply.
3. Next.js 16 is stable (early 2026). Turbopack default, React Compiler stable, 'use cache' directive, PPR, React 19, Node 20+ required.
4. Better Auth + Next.js setup is straightforward: server auth instance, client auth instance, catch-all route handler. Auth tables managed by Better Auth in Neon DB.

Proposed architecture: Next.js manages auth (Better Auth + Neon), issues JWTs. FastAPI verifies JWTs via JWKS endpoint, connects to Neon for business data only.

## Outcome

- Impact: Validated technical feasibility of Phase II stack. All components are compatible and well-documented.
- Tests: N/A (research only)
- Files: N/A (no code changes)
- Next prompts: Create Phase II architecture plan, define API contracts, set up project scaffolding
- Reflection: EdDSA default in Better Auth is notable -- need to ensure PyJWT + cryptography support it. NullPool + Neon pooler is the clear pattern for serverless.

## Evaluation notes (flywheel)

- Failure modes observed: better-auth.com docs could not be fetched directly via WebFetch; fell back to curl. EdDSA vs RS256 could be a compatibility concern.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate EdDSA JWT verification with PyJWT in a minimal Python script

---
id: "0001"
title: "Create Phase II Fullstack Web Spec"
stage: spec
date: 2026-03-02
surface: agent
model: claude-sonnet-4-6
feature: 002-fullstack-web
branch: 002-fullstack-web
user: saqib
command: /sp.specify
labels: ["phase-ii", "fullstack", "spec", "web-app"]
links:
  spec: specs/002-fullstack-web/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-fullstack-web/spec.md
  - specs/002-fullstack-web/checklists/requirements.md
tests:
  - none
---

## Prompt

Phase II: Transform the Todo app from a local CustomTkinter/SQLite desktop app into a full-stack web application.

Requirements from hackathon spec:
- Next.js 16+ frontend (App Router) with responsive UI
- FastAPI backend with RESTful API endpoints
- SQLModel ORM with Neon Serverless PostgreSQL
- Better Auth for user authentication (signup/signin) with JWT tokens
- Multi-user support: each user only sees their own tasks
- Monorepo structure (frontend/ + backend/)
- All 5 Basic Level features as web app: Add, Delete, Update, View, Mark Complete
- Plus Intermediate features already built: Priorities, Categories, Search, Filter, Sort
- Plus Advanced features already built: Recurring Tasks, Due Dates & Time Reminders

API Endpoints:
- GET /api/{user_id}/tasks - List all tasks
- POST /api/{user_id}/tasks - Create a new task
- GET /api/{user_id}/tasks/{id} - Get task details
- PUT /api/{user_id}/tasks/{id} - Update a task
- DELETE /api/{user_id}/tasks/{id} - Delete a task
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion

Auth flow: Better Auth on Next.js issues JWT → Frontend sends JWT in Authorization header → FastAPI middleware verifies JWT using shared BETTER_AUTH_SECRET → Backend filters data by authenticated user_id

Database: Neon Serverless PostgreSQL with tasks table including user_id foreign key, plus users table managed by Better Auth

## Response snapshot

Created feature branch `002-fullstack-web` and wrote comprehensive spec with 5 user stories (P1: auth, CRUD, toggle; P2: search/filter/sort, responsive UI), 13 functional requirements, 7 success criteria, edge cases, key entities, assumptions, and scope boundaries. Quality checklist passed all items.

## Outcome

- ✅ Impact: Feature spec created for Phase II full-stack web transformation
- 🧪 Tests: No tests — spec phase only
- 📁 Files: 2 files created (spec.md, checklists/requirements.md)
- 🔁 Next prompts: /sp.clarify or /sp.plan
- 🧠 Reflection: Spec covers all hackathon Phase II requirements. No clarification markers needed — all requirements were well-defined in the hackathon document.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Quality checklist PASS (all items checked)
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null

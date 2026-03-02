---
id: 9
title: Implement Intermediate Features
stage: green
date: 2026-03-01
surface: agent
model: claude-sonnet-4-6
feature: 001-todo-app
branch: 001-todo-app
user: saqib
command: implement
labels: ["priority", "category", "due-date", "search", "filter", "sort", "gui"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - src/models/task.py
  - src/repository/task_repo.py
  - src/services/task_service.py
  - src/gui/app.py
  - tests/conftest.py
  - tests/unit/test_task_service.py
  - tests/integration/test_task_repo.py
tests:
  - tests/unit/test_task_service.py
  - tests/integration/test_task_repo.py
---

## Prompt

Implement the following plan:

# Plan: Intermediate Features — Priorities, Categories, Search/Filter, Sort

Add priority levels, fixed categories, due dates, search, filtering, and sorting to the todo app across model, repository, service, GUI, and test layers.

## Response snapshot

Implemented all intermediate features across 7 files:
- Model: Added priority, category, due_date fields with constants
- Repository: Added filtering (search, status, priority, category) and sorting (created_at, due_date, priority, title) to get_all(); updated create/update signatures
- Service: Added validation for priority and category values; pass-through filter/sort params
- GUI: Expanded add form (2 rows), filter/search bar, sort controls, enhanced task rows (priority dots, category badges, overdue dates), expanded edit dialog
- Tests: 60 tests all passing, covering new field validation, filtering, sorting

## Outcome

- ✅ Impact: Full intermediate feature set — priorities, categories, due dates, search, filter, sort
- 🧪 Tests: 60 passed, 0 failed
- 📁 Files: 7 modified
- 🔁 Next prompts: Manual GUI testing, DB migration strategy, dark mode verification
- 🧠 Reflection: Clean implementation following existing patterns; priority sorting needed custom Python sort since string ordering doesn't match semantic ordering

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): pytest PASS (60/60)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add keyboard shortcuts or drag-to-reorder

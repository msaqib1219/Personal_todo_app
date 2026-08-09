---
id: "0006"
title: Apply Analysis Remediation Edits
stage: tasks
date: 2026-03-05
surface: agent
model: claude-sonnet-4-6
feature: 002-fullstack-web
branch: 002-fullstack-web
user: saqib
command: /sp.analyze (remediation follow-up)
labels: ["remediation", "constitution", "tasks", "tdd"]
links:
  spec: specs/002-fullstack-web/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - specs/002-fullstack-web/spec.md
  - specs/002-fullstack-web/tasks.md
tests:
  - null
---

## Prompt

yes, suggest remediation for all critical and high issues

(followed by: yes, apply all edits)

## Response snapshot

Applied all 7 remediations (3 CRITICAL + 4 HIGH) across 3 files:

**C1 (Constitution v2.0.0)**: Updated `.specify/memory/constitution.md` — split Product Scope into Phase I/II, expanded Technology Constraints, updated Security/Observability/Documentation principles for web context. Version bumped 1.1.0 → 2.0.0.

**C2 (TDD tests)**: Added 8 test tasks to `tasks.md` — T009a (test infra), T013a/T013b (foundational tests), T027a/T027b/T027c (US2 tests), T037a/T037b (US3 tests), T041a (US4 tests). All RED phase, must fail before implementation.

**C3 (Linting)**: Added T002a (ruff config) and T003a (Biome config) to Phase 1.

**C4 (Logging)**: Added T008a (structured logging module) to Phase 2. Updated T013 to wire logging on startup. Changed T054 from implementation to verification.

**C5 (Versioning)**: Added `version = "0.1.0"` to T002 and T003 descriptions. Added Conventional Commits note to T006/T007.

**I1 (Spec fix)**: Changed "shared secret" to "JWKS endpoint" in spec.md:L136.

**G1 (401/404)**: Updated T032 with explicit 401/404 behavior. Added [US2] labels to T028-T033.

Total tasks: 55 → 67.

## Outcome

- ✅ Impact: All 3 CRITICAL and 4 HIGH issues resolved; constitution updated to v2.0.0
- 🧪 Tests: 8 test tasks added to tasks.md (TDD RED phase)
- 📁 Files: Modified constitution.md, spec.md, tasks.md
- 🔁 Next prompts: Re-run `/sp.analyze` to verify CRITICAL count drops to 0, then `/sp.implement`
- 🧠 Reflection: Constitution amendment was the highest-impact change — unblocks all future /sp.analyze runs from flagging Phase II scope as violations

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Task count verified at 67 via grep
- Prompt variant (if applicable): Remediation application
- Next experiment (smallest change to try): Re-run /sp.analyze to confirm all CRITICALs resolved

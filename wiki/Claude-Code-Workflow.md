# Claude Code Workflow

> "The human architects. Claude Code builds."

## The Partnership Model

In this project, Claude Code isn't just a code generator — it's a **implementation partner** that follows specs, respects constraints, and produces testable code.

```
Human (Architect)              Claude Code (Builder)
├── Write specs                ├── Read specs
├── Define constraints         ├── Generate plan
├── Review decisions           ├── Break into tasks
├── Approve tests              ├── Write failing tests
└── Validate output            ├── Implement code
                               └── Refactor
```

## How It Works

### 1. Context Setting

Claude Code reads project context before implementing:

```markdown
# CLAUDE.md (Root)
- Project overview
- Spec-Kit structure
- How to reference specs

# frontend/CLAUDE.md
- Stack: Next.js, TypeScript, Tailwind
- Patterns: server components, API client

# backend/CLAUDE.md
- Stack: FastAPI, SQLModel, Neon PostgreSQL
- Conventions: TDD, type hints, ruff
```

### 2. Spec Reference

Reference specs directly in prompts:

```
You: @specs/features/task-crud.md implement the create task feature

Claude Code:
1. Reads spec.md (user stories, acceptance criteria)
2. Reads plan.md (architecture, tech stack)
3. Reads tasks.md (what to implement)
4. Reads CLAUDE.md (conventions)
5. Generates implementation
```

### 3. Implementation Flow

```
┌─────────────────────────────────────────────────────┐
│ You: "@specs/features/task-crud.md implement"       │
└──────────────────────┬──────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ Claude Code:                                        │
│ 1. Read spec → Understand requirements              │
│ 2. Read plan → Know architecture                    │
│ 3. Read tasks → Know what to build                  │
│ 4. Write tests → Red phase                          │
│ 5. Implement → Green phase                          │
│ 6. Refactor → Clean up                              │
│ 7. Run tests → Verify                              │
└──────────────────────┬──────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ Output:                                             │
│ - Implementation code                               │
│ - Passing tests                                     │
│ - Lint-clean formatting                             │
│ - PHR documenting the interaction                   │
└─────────────────────────────────────────────────────┘
```

## Effective Prompting Patterns

### Pattern 1: Spec Reference

```
@specs/001-todo-app/spec.md implement User Story 1 (Add Task)
```

**Why it works**: Claude Code reads the full spec context, including acceptance criteria.

### Pattern 2: File Reference

```
@src/services/task_service.py add validation for priority field
```

**Why it works**: Claude Code reads existing code, understands patterns, maintains consistency.

### Pattern 3: Architecture Constraint

```
Implement the task form component following the three-layer pattern.
GUI layer must not contain business logic.
```

**Why it works**: Constraints prevent unwanted patterns.

### Pattern 4: Test-First

```
Write failing tests for the toggle completion feature,
then implement to make them pass.
```

**Why it works**: Enforces TDD workflow.

### Pattern 5: Iterative Refinement

```
The task form needs a priority dropdown.
Read @frontend/src/components/task-form.tsx and add the field.
```

**Why it works**: Builds on existing code, maintains consistency.

## What Claude Code Does Well

### ✅ Strengths

| Strength | Example |
|----------|---------|
| Following patterns | Reads existing code, maintains style |
| Test generation | Creates comprehensive test suites |
| Architecture adherence | Respects three-layer pattern |
| Type safety | Adds proper type hints |
| Error handling | Implements edge cases from specs |
| Documentation | Generates inline comments |

### ❌ Limitations

| Limitation | Mitigation |
|------------|------------|
| Can't run the app | Human tests manually |
| May miss business rules | Review against acceptance criteria |
| Over-generates | Apply YAGNI filter |
| Context window limits | Break into smaller tasks |

## The PHR System

Every interaction with Claude Code is recorded as a **Prompt History Record (PHR)**.

### What a PHR Captures

```yaml
---
id: 008
title: Implement Todo App Full Stack
stage: green
date: 2026-03-01
feature: 001-todo-app
command: /sp.implement
files:
  - src/config.py
  - src/models/task.py
  - ...
tests:
  - tests/unit/test_task_service.py
  - tests/integration/test_task_repo.py
---
```

### Why PHRs Matter

1. **Audit trail**: Every change is traceable
2. **Learning**: Review what worked and what didn't
3. **Reproducibility**: Similar prompts produce similar results
4. **Documentation**: PHRs tell the real development story

## Workflow Examples

### Example 1: New Feature

```
1. Write spec: specs/002-fullstack-web/spec.md
2. Generate plan: specs/002-fullstack-web/plan.md
3. Break tasks: specs/002-fullstack-web/tasks.md
4. Implement: "@specs/002-fullstack-web/tasks.md start Phase 1"
5. PHR: history/prompts/002-fullstack-web/0001-*.prompt.md
```

### Example 2: Bug Fix

```
1. Read error: "Task toggle not working"
2. Reference: "@src/services/task_service.py investigate toggle_task"
3. Fix: Claude Code reads code, identifies issue, fixes
4. Test: Write regression test
5. PHR: history/prompts/001-todo-app/010-fix-toggle-bug.green.prompt.md
```

### Example 3: Refactor

```
1. Constraint: "Refactor task_repo.py to use user-scoped queries"
2. Reference: "@src/repository/task_repo.py add user_id parameter"
3. Claude Code: reads file, adds parameter, updates all callers
4. Tests: verify no regressions
5. PHR: history/prompts/002-fullstack-web/011-refactor-user-scoping.refactor.prompt.md
```

## Tips for Working with Claude Code

### 1. Be Specific About Scope

```
Bad:  "Add authentication"
Good: "@backend/src/auth.py implement JWT verification using JWKS endpoint"
```

### 2. Reference Existing Code

```
Bad:  "Create a task model"
Good: "@src/models/task.py add priority field following existing pattern"
```

### 3. Set Constraints

```
"Keep functions under 50 lines"
"Follow existing test patterns in tests/unit/"
"No new dependencies unless absolutely necessary"
```

### 4. Review Output

Claude Code generates good code, but always:
- Run tests
- Check lint
- Verify against acceptance criteria
- Test manually

### 5. Iterate in Small Steps

```
Bad:  "Build the entire Phase II"
Good: "Implement the task repository with CRUD operations"
```

## The Result

After 19 PHRs across 2 features:
- **60+ tests** in Phase I
- **Comprehensive test suites** in Phase II
- **Clean architecture** maintained throughout
- **Full traceability** from spec to code

---

**See also**: [Spec-Driven Development](Spec-Driven-Development.md) | [Lessons Learned](Lessons-Learned.md)

# Spec-Driven Development

> "Write the spec. Let the code follow."

## What Is SDD?

Spec-Driven Development (SDD) is a workflow where specifications drive implementation. Instead of writing code and documenting later, you write the spec first, then use AI to generate the implementation.

```
Traditional:    Code → Docs → Tests → Hope
SDD:            Spec → Plan → Tasks → Code (with tests built in)
```

## The SDD Workflow

### Step 1: Constitution

Define project principles and constraints before any code.

**Location**: `.specify/memory/constitution.md`

**Example**:
```markdown
## Core Principles

### I. Code Quality
- Type hints on all function signatures
- Code MUST pass ruff check with zero violations
- Functions MUST have single responsibility

### II. Test-First (TDD) (NON-NEGOTIABLE)
- Red-Green-Refactor cycle strictly enforced
- pytest is the test runner
```

### Step 2: Feature Spec

Define what to build with user stories and acceptance criteria.

**Location**: `specs/<feature>/spec.md`

**Example**:
```markdown
### User Story 1 - Add a New Task (Priority: P1)

A user opens the application and wants to create a new todo item.
They click an "Add Task" button, enter a task title and optional details...

**Acceptance Scenarios**:
1. **Given** the app is open with an empty task list,
   **When** the user clicks "Add Task", enters "Buy groceries"...
   **Then** "Buy groceries" appears in the task list...
```

### Step 3: Implementation Plan

Architecture decisions, technology choices, component design.

**Location**: `specs/<feature>/plan.md`

**Contents**:
- Technology stack decisions
- Component architecture
- Data model design
- API contracts
- Testing strategy

### Step 4: Task Breakdown

Executable work items with clear dependencies.

**Location**: `specs/<feature>/tasks.md`

**Example**:
```markdown
## Phase 1: Setup
- [ ] T001: Initialize project structure
- [ ] T002: Configure linting and formatting
- [ ] T003: Set up test infrastructure

## Phase 2: Foundational
- [ ] T004: Create database models
- [ ] T005: Implement repository layer
```

### Step 5: Implementation

Claude Code reads specs and generates implementation.

**Command**: `/sp.implement` or natural language referencing specs

**Example**:
```
You: @specs/features/task-crud.md implement the create task feature
Claude: [reads spec, generates code, writes tests]
```

### Step 6: Architecture Decision Records

Capture significant decisions with context, options, and rationale.

**Location**: `history/adr/`

**Example**: [ADR-0001: GUI and ORM Technology Stack](../history/adr/0001-gui-and-orm-technology-stack.md)

## The Artifact Chain

```
Constitution
    ↓
Feature Spec ─────────────────────────────────────┐
    ↓                                              ↓
Implementation Plan                          ADRs (if needed)
    ↓                                              ↑
Task Breakdown                                    │
    ↓                                              │
Implementation ────────────────────────────────────┘
    ↓
Prompt History Records (PHRs)
```

## Why SDD Works

### For Humans

- **Forces clarity**: You must think through acceptance criteria before coding
- **Reduces rework**: Spec catches requirements issues early
- **Documents decisions**: ADRs capture why, not just what
- **Enables delegation**: Clear specs let AI generate accurate code

### For AI (Claude Code)

- **Clear context**: Specs provide unambiguous requirements
- **Constraints**: Constitution prevents unwanted patterns
- **Testability**: Acceptance criteria become test cases
- **Traceability**: Every feature links back to a spec

## SDD in This Project

### Artifacts Created

| Artifact | Count | Location |
|----------|-------|----------|
| Constitution | 1 | `.specify/memory/constitution.md` |
| Feature Specs | 2 | `specs/001-todo-app/spec.md`, `specs/002-fullstack-web/spec.md` |
| Implementation Plans | 2 | `specs/*/plan.md` |
| Task Breakdowns | 2 | `specs/*/tasks.md` |
| ADRs | 1 | `history/adr/` |
| PHRs | 19 | `history/prompts/` |

### The Evidence Trail

Every feature in this project can be traced:

```
Feature: "Add Task with Priority"
    ↓
Spec: specs/001-todo-app/spec.md (User Story 1)
    ↓
Plan: specs/001-todo-app/plan.md (Phase 2)
    ↓
Tasks: specs/001-todo-app/tasks.md (T006-T012)
    ↓
Implementation: src/services/task_service.py:84
    ↓
Tests: tests/unit/test_task_service.py
    ↓
PHR: history/prompts/001-todo-app/008-implement-todo-app-full.green.prompt.md
```

## SDD Commands

| Command | Purpose |
|---------|---------|
| `/sp.init` | Initialize Spec-Kit structure |
| `/sp.specs` | Create feature specification |
| `/sp.plan` | Generate implementation plan |
| `/sp.tasks` | Break down into executable tasks |
| `/sp.implement` | Generate code from specs |
| `/sp.analyze` | Validate spec consistency |
| `/sp.adr` | Document architecture decision |

## Tips for Effective SDD

### 1. Write Specs Before Code

The temptation is to skip ahead. Don't. The spec is where clarity happens.

### 2. Make Acceptance Criteria Testable

```
Bad:  "Task should be created"
Good: "Given empty list, When user adds 'Buy groceries', 
       Then task appears with status incomplete"
```

### 3. Capture Decisions as ADRs

Every significant choice (technology, architecture, pattern) deserves an ADR. Your future self will thank you.

### 4. Let PHRs Tell the Story

Prompt History Records capture the actual development journey. They're more honest than polished documentation.

### 5. Use Specs as Communication

Specs aren't just for AI. They're for:
- Your future self
- Team members
- Hackathon judges
- Anyone who wants to understand the project

---

**See also**: [Claude Code Workflow](Claude-Code-Workflow.md) | [Architecture Decisions](Architecture-Decisions.md)

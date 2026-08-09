# Architecture Decisions

> "Every significant choice deserves documentation."

## What Is an ADR?

An **Architecture Decision Record (ADR)** captures a significant architectural choice, including:
- The context that necessitated the decision
- The options considered
- The chosen option and its rationale
- The consequences (positive and negative)

## ADR Summary

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [ADR-0001](#adr-0001-gui-and-orm-technology-stack) | GUI and ORM Technology Stack | Accepted | 2026-02-22 |

---

## ADR-0001: GUI and ORM Technology Stack

**Status**: Accepted  
**Date**: 2026-02-22  
**Feature**: 001-todo-app

### Context

The Personal Todo APP requires a cross-platform desktop GUI (Linux + Windows) with local SQLite persistence for up to 500 tasks. The project is built at hackathon pace with Python 3.13 and must support TDD by separating GUI from testable business logic.

**Key constraints**:
- Zero system-level dependencies for easy setup
- Modern visual appearance
- Three-layer architecture (GUI → Service → Repository)
- Hackathon-pace delivery

### Decision

We adopt the following integrated technology stack:

- **GUI Framework**: CustomTkinter >=5.2.0
- **Theme Detection**: darkdetect >=0.8.0
- **ORM**: SQLModel >=0.0.22
- **Database Engine**: SQLite (local file at `~/.todo-app/tasks.db`)
- **Architecture Pattern**: Three-layer separation

### Options Considered

#### Alternative A: PySide6/Qt + SQLAlchemy

| Aspect | Assessment |
|--------|------------|
| GUI | PySide6 — professional polish, industrial-grade cross-platform |
| ORM | SQLAlchemy with separate Pydantic schemas |
| Pros | Mature, well-documented, extensive widget library |
| Cons | 150-200 MB install size, system dependency issues on Linux (libgl1, libxcb) |
| **Verdict** | ❌ Rejected — overkill for 5-operation todo app, setup friction conflicts with hackathon pace |

#### Alternative B: Tkinter (stdlib) + Raw sqlite3

| Aspect | Assessment |
|--------|------------|
| GUI | Tkinter — zero dependencies, ships with Python |
| ORM | None — direct sqlite3 module |
| Pros | Zero dependencies, always available |
| Cons | Dated 1990s appearance, raw SQL risk of injection, lacks ScrollableFrame |
| **Verdict** | ❌ Rejected — fails modern look requirement, Security principle violation |

#### Alternative C: Dear PyGui + Peewee

| Aspect | Assessment |
|--------|------------|
| GUI | Dear PyGui — GPU-accelerated, modern immediate-mode GUI |
| ORM | Peewee — lightweight ORM |
| Pros | Fast rendering, simple API |
| Cons | Uncertain Python 3.13 compatibility, less conventional API paradigm |
| **Verdict** | ❌ Rejected — compatibility risk too high for hackathon delivery |

#### Chosen: CustomTkinter + SQLModel ✅

| Aspect | Assessment |
|--------|------------|
| GUI | CustomTkinter — modern Tkinter wrapper with flat design and dark/light mode |
| ORM | SQLModel — SQLAlchemy + Pydantic in a single model definition |
| Pros | Zero system deps, modern appearance, purpose-built widgets, unified model layer |
| Cons | Single maintainer risk (mitigated by stable Tkinter base) |
| **Verdict** | ✅ Selected — cohesive stack, hackathon-friendly |

### Consequences

#### Positive

- **Zero system dependencies**: `uv add customtkinter sqlmodel` installs everything
- **Modern appearance**: Flat design, rounded corners, dark/light mode auto-detection
- **Purpose-built widgets**: `CTkScrollableFrame`, `CTkCheckBox`, `CTkEntry`, `CTkButton`
- **Unified model layer**: Single class serves as ORM entity and Pydantic validator
- **SQL injection prevention**: SQLAlchemy's parameterized queries via SQLModel
- **Full testability**: Service and repository layers testable without display
- **Small footprint**: ~2-3 MB for CustomTkinter

#### Negative

- **Single maintainer risk**: CustomTkinter maintained by one developer
  - *Mitigation*: Built on stable Tkinter stdlib, fallback to raw Tkinter feasible
- **Limited advanced widgets**: No tree views or data grids
  - *Acceptable*: Flat task list only, no complex UI needed
- **SQLModel maturity**: Younger than SQLAlchemy
  - *Mitigated*: Single-entity app with basic CRUD, small API surface

### References

- Feature Spec: `specs/001-todo-app/spec.md`
- Implementation Plan: `specs/001-todo-app/plan.md`
- Research: `specs/001-todo-app/research.md`
- Constitution: `.specify/memory/constitution.md` (Principles III, IV)

---

## Future ADRs

The following decisions are candidates for ADR documentation:

### Phase II: Authentication Strategy

**Context**: Multi-user web app needs secure authentication.  
**Options**: Better Auth vs Clerk vs NextAuth vs custom JWT  
**Status**: Decision pending

### Phase II: Database Hosting

**Context**: Cloud PostgreSQL for multi-user access.  
**Options**: Neon vs Supabase vs Railway vs self-hosted  
**Status**: Decision pending (leaning toward Neon)

### Phase III: AI Integration

**Context**: Natural language task management.  
**Options**: OpenAI Agents SDK vs LangChain vs custom  
**Status**: Decision pending

### Phase IV: Container Orchestration

**Context**: Local Kubernetes deployment.  
**Options**: Minikube vs Kind vs Docker Desktop K8s  
**Status**: Decision pending

---

## Creating New ADRs

### When to Create an ADR

Create an ADR when:
- Choosing between multiple viable options
- The decision has long-term consequences
- The decision affects system architecture
- Other developers need to understand the rationale

### ADR Template

```markdown
# ADR-XXXX: [Title]

- **Status:** [Proposed | Accepted | Deprecated | Superseded]
- **Date:** YYYY-MM-DD
- **Feature:** [feature-branch-name]

## Context

[What situation necessitates a decision?]

## Decision

[What did we decide?]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Tradeoff 1]
- [Tradeoff 2]

## Alternatives Considered

### Alternative A: [Name]
- [Description]
- [Why rejected]

### Alternative B: [Name]
- [Description]
- [Why rejected]

## References
- [Links to related specs, plans, etc.]
```

---

**See also**: [Spec-Driven Development](Spec-Driven-Development.md) | [Phase I Journey](Phase-I-Journey.md)

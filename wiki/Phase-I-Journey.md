# Phase I: Desktop App Journey

> "What started as a console app spec evolved into a Microsoft To Do-inspired desktop application."

## The Starting Point

The hackathon spec asked for a simple console app: add tasks, view tasks, mark complete. In-memory storage. Basic Python.

But the constitution demanded more:

> *"All Python code MUST be clean, readable, and maintainable."* — Constitution Principle I

The question became: how do you build something simple but architecturally sound?

## The Pivot: Console → GUI

### Decision Point

The spec said "console app." The ambition said "desktop app." The constitution said "clean architecture."

**What we chose**: Build a GUI from day one, but keep the architecture clean enough that the presentation layer is interchangeable.

### Why CustomTkinter?

We evaluated four options:

| Stack | Pros | Cons | Verdict |
|-------|------|------|---------|
| PySide6/Qt | Professional polish | 150-200 MB install, system deps | ❌ Too heavy |
| Tkinter (raw) | Zero dependencies | Dated 1990s appearance | ❌ Looks bad |
| Dear PyGui | GPU-accelerated | Python 3.13 uncertainty | ❌ Too risky |
| **CustomTkinter** | Modern, lightweight, purpose-built | Single maintainer | ✅ Chosen |

See full analysis: [ADR-0001: GUI and ORM Technology Stack](../history/adr/0001-gui-and-orm-technology-stack.md)

## The Architecture

Three layers. No shortcuts.

```
┌─────────────────────────────────────────┐
│            GUI Layer                    │
│  CustomTkinter (presentation only)     │
├─────────────────────────────────────────┤
│          Service Layer                  │
│  TaskService (validation + logic)      │
├─────────────────────────────────────────┤
│        Repository Layer                 │
│  TaskRepository (data access)          │
├─────────────────────────────────────────┤
│         Database Layer                  │
│  SQLModel + SQLite                     │
└─────────────────────────────────────────┘
```

### The Rule

> *"No feature is worth breaking the architecture."*

Every feature request went through the same filter:
1. Does it fit the three-layer pattern?
2. Can it be tested without a display?
3. Does it follow YAGNI?

## What Got Built

### Basic Features (as spec'd)

| Feature | Implementation | Surprise |
|---------|---------------|----------|
| Add Task | `TaskService.add_task()` | Added validation the spec didn't ask for |
| Delete Task | `TaskService.delete_task()` | Confirmation dialog added |
| Update Task | `TaskService.update_task()` | Full field editing, not just title |
| View Task List | `TaskRepository.get_all()` | Scrollable list with status indicators |
| Mark Complete | `TaskService.toggle_task()` | Visual feedback + recurring task logic |

### Intermediate Features (proactive)

The spec didn't ask for priorities, categories, search, filter, or sort. We built them anyway.

**Why?** Because the model already had the fields. The repository already had the query infrastructure. Adding them was small, testable, and valuable.

```
Task Model Fields:
├── id, title, description, is_completed  (basic)
├── priority (high/medium/low)            (intermediate)
├── category (work/home/personal/...)     (intermediate)
├── due_date, due_time                    (intermediate)
├── recurrence (daily/weekly/monthly/...) (advanced)
└── reminder_minutes, reminder_sent       (advanced)
```

### Advanced Features (bonus)

- **Recurring Tasks**: Complete a weekly task → auto-create next occurrence
- **Desktop Reminders**: Background polling service with `plyer` notifications
- **Smart Lists**: My Day, Important, Planned, All Tasks

## The Microsoft To Do Redesign

Somewhere along the way, the UI evolved from "functional" to "beautiful."

### Layout

```
┌──────────┬────────────────────┬──────────────┐
│ Sidebar  │    Main Panel      │ Detail Panel │
│          │                    │              │
│ ☀ My Day │  ☐ Buy groceries   │ Task: Buy    │
│ ⭐ Important│ ☐ Read book      │ groceries    │
│ 📅 Planned│ ✓ Call mom        │              │
│ 📋 All   │                    │ Priority:    │
│          │                    │ Medium       │
│ ─────── │                    │              │
│ 📁 Work  │                    │ Category:    │
│ 📁 Home  │                    │ Home         │
└──────────┴────────────────────┴──────────────┘
```

### Design Tokens

```python
ACCENT_BLUE = "#2564CF"      # Microsoft Blue
SIDEBAR_BG = ("#F5F5F5", "#2D2D2D")  # Light/Dark
CARD_BG = ("#FFFFFF", "#3B3B3B")
MAIN_BG = ("#EBEBEB", "#1E1E1E")
```

## Testing Philosophy

### TDD Enforcement

The constitution mandated test-first development. Every feature started with a failing test.

```
Red → Green → Refactor
 ↓       ↓        ↓
Write   Write    Clean
failing minimum  up
test   code
```

### Test Coverage

```
tests/
├── conftest.py              # Fixtures
├── unit/
│   └── test_task_service.py  # 17 unit tests
└── integration/
    └── test_task_repo.py     # 13 integration tests

Total: 60+ tests (including intermediate features)
```

### What We Learned

- **GUI logic separation pays off**: Business logic tested without display
- **In-memory SQLite is fast**: Integration tests run in milliseconds
- **Validation tests catch regressions**: Edge cases documented as tests

## Lessons from Phase I

### 1. Architecture Is a Decision, Not an Accident

The three-layer pattern wasn't accidental. It was chosen before writing a single line of code.

### 2. Specs Can Be Guidelines, Not Laws

The spec said "console app." We built a GUI. But we kept the architecture clean, so the deviation was safe.

### 3. Proactive Features Need Discipline

Adding intermediate features was valuable, but only because:
- They fit the existing architecture
- They were small and testable
- They didn't break the constitution

### 4. AI Works Best With Structure

Claude Code excelled when given:
- Clear specs with acceptance criteria
- Architecture constraints (three-layer)
- Test-first requirements

## Files Created

```
src/
├── config.py              # Configuration
├── models/task.py         # SQLModel entity
├── repository/
│   ├── database.py        # Engine + sessions
│   └── task_repo.py       # CRUD operations
├── services/
│   ├── task_service.py    # Business logic
│   └── reminder_service.py # Background reminders
├── gui/app.py             # CustomTkinter GUI (780 lines)
└── __init__.py
main.py                    # Entry point
tests/                     # 60+ tests
specs/001-todo-app/        # Specifications
history/prompts/001-todo-app/ # 9 PHRs
```

---

**Next**: [Phase II: Full-Stack Web](Phase-II-Journey.md) →

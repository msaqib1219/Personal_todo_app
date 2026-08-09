# Lessons Learned

> "The real value isn't in the code — it's in the patterns that emerged."

## Technical Lessons

### 1. Architecture Is a Decision, Not an Accident

**What happened**: The three-layer pattern (GUI → Service → Repository) was chosen before writing code.

**Why it mattered**:
- Business logic testable without display
- GUI could evolve (console → CustomTkinter → web) without touching core logic
- Claude Code could generate code that fit the pattern

**Lesson**: Invest in architecture early. It pays dividends throughout the project.

### 2. Specs Before Code Prevents Rework

**What happened**: Writing specs forced clarity on acceptance criteria before implementation.

**Why it mattered**:
- Caught ambiguous requirements early
- Claude Code generated accurate code on first pass
- Tests were derived directly from acceptance criteria

**Lesson**: The spec is where clarity happens. Code is just the execution.

### 3. TDD Isn't Optional — It's Infrastructure

**What happened**: Test-first development caught issues before they compounded.

**Why it mattered**:
- 60+ tests in Phase I, all passing
- Regression confidence when adding features
- Tests documented expected behavior

**Lesson**: Tests aren't overhead. They're the safety net that enables rapid iteration.

### 4. YAGNI Saves Time

**What happened**: Resisted adding "nice-to-have" features that weren't in the spec.

**Why it mattered**:
- Focused on delivering working features
- Avoided premature abstractions
- Kept code simple and maintainable

**Lesson**: The smallest viable solution is almost always the right choice.

### 5. Types Are Contracts

**What happened**: TypeScript types and Python type hints became the contract between components.

**Why it mattered**:
- Frontend-backend contract enforced by types
- Claude Code generated type-safe code
- Refactoring was safe with type checking

**Lesson**: Types aren't bureaucracy. They're communication.

## Process Lessons

### 6. Claude Code Works Best With Structure

**What happened**: Clear specs and constraints produced better output than vague requests.

**Why it mattered**:
- "@specs/features/task-crud.md implement" > "add task feature"
- Constraints prevented unwanted patterns
- Existing code references maintained consistency

**Lesson**: The quality of AI output is proportional to the quality of input.

### 7. PHRs Tell the Real Story

**What happened**: Prompt History Records captured the actual development journey.

**Why it mattered**:
- Honest documentation of what actually happened
- Learning from mistakes and iterations
- Reproducible workflow for future projects

**Lesson**: Document the journey, not just the destination.

### 8. Monorepos Work for AI

**What happened**: Single repository with frontend and backend worked well with Claude Code.

**Why it mattered**:
- Claude Code could see entire project context
- Cross-cutting changes were easy
- Specs, code, and docs lived together

**Lesson**: For AI-assisted development, context visibility matters.

### 9. Specs Evolve, and That's OK

**What happened**: The Phase I spec said "console app." We built a GUI.

**Why it mattered**:
- Architecture was clean enough to accommodate the pivot
- Constitution principles guided the deviation
- Spec became guidelines, not laws

**Lesson**: Specs are living documents. The value is in the thinking, not the words.

### 10. Proactive Features Need Discipline

**What happened**: Added intermediate features (priorities, categories, search) without being asked.

**Why it mattered**:
- They fit the existing architecture
- They were small and testable
- They didn't break the constitution

**Lesson**: Adding features proactively is valuable only when constrained by architecture.

## AI-Specific Lessons

### 11. Claude Code Excels at Pattern Following

**What happened**: Given existing code patterns, Claude Code replicated them accurately.

**Example**: TaskRepository patterns were consistent across all CRUD operations.

**Lesson**: Show Claude Code the pattern, then let it generate.

### 12. Claude Code Needs Constraint Boundaries

**What happened**: Without constraints, Claude Code over-generates.

**Example**: "Add authentication" produces too much. "Add JWT verification via JWKS" produces exactly what's needed.

**Lesson**: Be specific about scope and constraints.

### 13. Claude Code Can't Test (Yet)

**What happened**: Claude Code generated code and tests, but couldn't run them.

**Why it mattered**: Human verification was essential for quality assurance.

**Lesson**: AI generates. Human validates. The partnership works.

### 14. Iterative Refinement Works

**What happened**: Small, focused prompts produced better results than large, ambitious ones.

**Example**: "Add priority field to task model" > "Build the entire task management system"

**Lesson**: Break large tasks into small, verifiable steps.

## Project-Specific Lessons

### 15. The Microsoft To Do Redesign Was Worth It

**What happened**: Evolved from functional UI to polished Microsoft To Do-inspired design.

**Why it mattered**:
- Professional appearance for hackathon presentation
- User experience improved dramatically
- Showed design capability alongside technical skill

**Lesson**: Aesthetics matter. Don't settle for "functional."

### 16. Recurring Tasks Are Complex

**What happened**: Auto-creating next occurrence on completion had edge cases.

**Example**: What happens when due_date is None? What about timezone handling?

**Lesson**: Simple features can have complex edge cases. Document them.

### 17. Auth Is Harder Than It Looks

**What happened**: JWT verification via JWKS seemed simple but had many edge cases.

**Example**: Token expiry, CORS, user ID extraction, error responses.

**Lesson**: Authentication is a cross-cutting concern that touches everything.

## What I'd Do Differently

### 1. Start With Tests Earlier

**What happened**: Tests came after implementation in some cases.

**What I'd do**: Write tests before any code, even for simple features.

### 2. Document Decisions in Real-Time

**What happened**: ADRs were written after the fact.

**What I'd do**: Create ADRs when making decisions, not later.

### 3. Smaller Iterations

**What happened**: Some prompts tried to do too much.

**What I'd do**: Break everything into the smallest possible steps.

### 4. More Manual Testing

**What happened**: Relied heavily on automated tests.

**What I'd do**: Manual testing after each feature to catch UX issues.

---

## The Big Picture

This project taught me that:

1. **Spec-Driven Development works** — it's not just documentation, it's a workflow
2. **AI is a partner, not a replacement** — the human architects, the AI builds
3. **Architecture matters** — clean patterns enable rapid iteration
4. **Testing is infrastructure** — it enables confidence, not just correctness
5. **Documentation tells the story** — PHRs and ADRs capture the real journey

The todo app is simple. The patterns that emerged are universal.

---

**See also**: [Spec-Driven Development](Spec-Driven-Development.md) | [Claude Code Workflow](Claude-Code-Workflow.md)

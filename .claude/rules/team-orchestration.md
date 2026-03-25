---
description: >
  Core team orchestration rule. Routes work to the correct specialist agent
  based on task type. Enforces quality gates and testing standards.
  Always active for all team members.
---

# Team Orchestration Guide

## Agent Routing

When working on tasks, use the appropriate specialist agent:

| Task Type | Agent | When |
|-----------|-------|------|
| Backend code, features, bug fixes | **elite-engineer** | Any Java/backend implementation work |
| Frontend/UI components | **ui-ux-fullstack-savant** | Angular, UI, BFF, styling work |
| Architecture & design review | **cto-reviewer** | Specs, architecture plans, design decisions |
| Code review against requirements | **cto-code-reviewer** | Post-implementation review, PR review |
| System design & specifications | **system-architect** | New system design, feature breakdown |
| Test creation & infrastructure | **test-architect** | Writing tests, test infrastructure |
| Documentation | **docs-writer** | User guides, API docs, READMEs |

## How to Invoke Agents

Tell Augment which agent to use naturally:
- "Use the **elite-engineer** agent to implement the retry mechanism"
- "Have the **cto-reviewer** agent review this architecture"
- "Use the **test-architect** agent to create integration tests for this handler"

Or let Augment auto-select based on context — the agent descriptions guide selection.

## Quality Gates (Non-Negotiable)

### Testing Standards
- **E2E and integration tests are the default** — not unit tests for getters/setters
- **Use real dependencies** (test containers, real databases) — mocks are a last resort
- **Tests MUST be run** after creation — unexecuted tests don't count
- **Tests MUST pass** before claiming completion

### Before Claiming Any Task Complete
1. All requirements addressed
2. Edge cases handled
3. Error handling is comprehensive
4. Tests written, run, and passing
5. Code follows project conventions

### Review Workflow
For significant changes, use this sequence:
1. **elite-engineer** (or **ui-ux-fullstack-savant**) → implements
2. **test-architect** → writes and runs tests
3. **cto-code-reviewer** → reviews against requirements

## Technology Stack Constraints

- **Java 21** — use virtual threads, records, sealed classes, pattern matching
- **No Spring, Quarkus, or similar** — use krista-infra frameworks only
- **Apache Artemis** via `app.krista.infra.esb` — for messaging
- **Infinispan 15** via `app.krista.infra.dataGrid` — for caching/data grid
- **Gradle with Groovy** — build system
- **JUnit 5** — testing (no mocks; use test containers from dev-labs)
- **SLF4J** — logging

## Code Style

- Blank lines after every open brace `{`
- Closing brace `}` on its own line always
- Small, focused methods with single responsibilities
- Prefer composition over inheritance
- Never swallow exceptions silently

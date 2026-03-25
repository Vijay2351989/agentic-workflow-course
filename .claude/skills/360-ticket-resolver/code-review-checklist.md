# Code Review Checklist — Generic Default

This is the **generic default** checklist used by the `/360-ticket-resolver` skill during Phase 4 (Code Review).

If a project-specific checklist exists at `docs/360-ticket-resolver/code-review-checklist.md` (relative to the project root), the skill loads that file **in addition** to this one — the project-specific checks extend and take precedence over the generic ones where there is overlap.

To add project-specific checks for your codebase, create `docs/360-ticket-resolver/code-review-checklist.md` in the project root. See the skill README for details.

---

## Generic Code Review Checklist (Applies to Any Project)

### Review Output (Non-Negotiable)
- **Always leave at least one code review comment**, no matter how small or simple the fix — even a positive observation, a minor nit, or a suggestion for future improvement counts. A review with zero comments is not a valid review.

### Correctness
- Does the change do what the ticket/requirement describes?
- Are all execution paths (happy path, error path, edge cases) correct?
- Are boundary conditions handled (empty collections, null inputs, zero, max values)?
- Are there any off-by-one errors in loops or index access?
- Is concurrency handled correctly — no race conditions, deadlocks, or lost updates?

### Security
- Is all user-supplied input validated and sanitised before use?
- Are there any SQL injection, XSS, command injection, or path traversal risks?
- Is sensitive data (passwords, tokens, PII) never logged or exposed in responses?
- Are authentication and authorisation checks present where needed?
- Are new dependencies free of known CVEs?

### Error Handling
- Are all exceptions caught at the right level — not swallowed silently?
- Are error messages meaningful for debugging without leaking internals to callers?
- Are external calls (network, DB, file system) protected against failure?
- Is the system left in a consistent state after an error?

### Performance
- Are there N+1 queries or redundant repeated calls inside loops?
- Are expensive operations (network, disk, computation) cached where appropriate?
- Are large collections streamed or paginated rather than loaded entirely into memory?
- Are there any obvious memory leaks (unclosed resources, unbounded caches)?

### Maintainability & Readability
- Are names (variables, methods, classes) clear and intention-revealing?
- Are methods short and focused on a single responsibility?
- Is duplicated logic extracted into a shared helper rather than copy-pasted?
- Are magic numbers and hardcoded strings replaced with named constants?
- Do comments explain *why*, not *what* (the code already shows what)?

### Testing
- Does the change include tests that would catch a regression?
- Do tests cover the happy path, error paths, and edge cases?
- Are tests independent — no shared mutable state between test cases?
- Do tests assert behaviour, not implementation details?

### Logging & Observability
- Are log statements at the correct level (DEBUG/INFO/WARN/ERROR)?
- Do log messages include enough context (IDs, values) to diagnose issues?
- Are there no logs that print sensitive data?

### API & Interface Design
- Is the public interface minimal — only what callers need is exposed?
- Are breaking changes to existing APIs flagged and justified?
- Are new endpoints or methods backwards-compatible?

### Dependencies & Build
- Does the change compile cleanly with no warnings?
- Are new dependencies necessary, well-maintained, and licence-compatible?
- Are unused imports and dead code removed?

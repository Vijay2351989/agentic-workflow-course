# Test Plan Guide — Generic Default

This is the **generic default** test plan guide used by the `/360-ticket-resolver` skill during Phase 5 (Test Plan).

If a project-specific guide exists at `docs/360-ticket-resolver/test-plan-guide.md` (relative to the project root), the skill loads that file **in addition** to this one — the project-specific guidance extends and takes precedence over the generic one where there is overlap.

To add project-specific guidance for your codebase, create `docs/360-ticket-resolver/test-plan-guide.md` in the project root. See the skill README for details.

---

## Generic Test Plan Guide (Applies to Any Project)

### Test Strategy

Choose the right level for each test case:

| Level | Purpose | When to use |
|---|---|---|
| Unit | Verify a single function/method in isolation | Pure logic, parsers, formatters, calculations |
| Integration | Verify interactions between real components | Service + DB, API endpoint + service layer |
| E2E | Validate a full user workflow end-to-end | Critical user journeys, smoke tests |

Default to **integration tests** for bug fixes — they catch real interaction failures that unit tests miss. E2E tests are expensive; use them sparingly for the most critical paths only.

### Mandatory Test Cases for Every Bug Fix

**TC-Regression** — Reproduce the original bug
- Must fail *before* the fix and pass *after*
- This is the most important test case; write it first
- Reference the ticket ID in a comment

**TC-Happy Path** — Normal flow still works
- Call the affected component with valid, representative input
- Assert status and correct response shape

**TC-Error Conditions** — System handles failures gracefully
- Missing/null required inputs → correct error response
- Invalid data → validation error, not a 500
- External dependency failure → graceful degradation

**TC-Edge Cases** — Boundary and extreme values
- Empty collections, null inputs, zero, minimum, maximum
- One value below and one above each boundary
- Single-item collections where "many" is the norm

**TC-Idempotency** — Repeat calls produce consistent results
- For any operation that mutates state, calling it twice should produce the same result as calling it once
- No accidental duplicate creation on retry

### Test Independence

- Each test must set up its own data — no reliance on another test's side effects
- Tests must be runnable in any order and in isolation
- Tests must be deterministic — same input always produces same outcome
- No shared mutable state between test cases; reset state in `@BeforeEach`

### Naming Convention

Use the pattern: `methodOrScenario_stateUnderTest_expectedBehaviour`

```
removedSource_searchedAgain_doesNotReappear()
startSession_embeddingStoreNotReady_returns503()
addCustomConstraint_duplicateText_storedOnlyOnce()
```

Names are documentation — clarity over brevity. Long names are fine.

### What to Assert

- **Always** assert the HTTP status code or return value
- Assert the **shape and key fields** of the response, not internal implementation details
- Assert **observable side effects** (state changes, records created) not private method calls
- Do NOT assert log output or internal counters — test behaviour, not mechanics
- One logical behaviour per test; use parameterised tests for multiple input variants

### What NOT to Test

- Private methods or internal implementation — test through the public interface
- LLM / AI response *content* — non-deterministic; assert structure (fields present, types correct), not wording
- Log output — observable behaviour only
- Framework internals — trust the framework
- Scenarios that cannot occur given the system's own invariants

### Security Test Cases (include when the bug touches auth, input, or data)

- Unvalidated user input reaching a sensitive operation → must be rejected
- Unauthenticated access to a protected endpoint → must return 401/403
- Sensitive data (tokens, passwords, PII) must not appear in responses or logs

### Performance (include when the bug touches a hot path)

- Assert response time stays within an acceptable bound under normal load
- Verify no N+1 queries or repeated expensive calls introduced by the fix

### Entry / Exit Criteria

- **Entry**: build compiles, test environment available, test data seeded
- **Exit**: all test cases pass with exit code 0, no tests skipped or disabled

---
name: 360-ticket-resolver
description: 360-degree ticket resolution skill. Takes a Jira ticket, performs smart iterative RCA with user confirmation, implements the fix, runs interactive code review, creates and confirms a test plan, runs tests relentlessly (or guides manual verification), then raises a PR with full RCA and test plan summary. Usage: /360-ticket-resolver TICKET-123 [source-branch]
user-invocable: true
disable-model-invocation: false
argument-hint: <TICKET-ID> <work-branch> [source-branch] [--quick-fix] [--skip-tests] [--manual-test]
---

# Skill: 360 Ticket Resolver

## Invocation

```
/360-ticket-resolver <JIRA_TICKET> <work-branch> [source-branch] [--quick-fix] [--skip-tests] [--manual-test]
```

Examples:
- `/360-ticket-resolver PROJ-123 feature/my-fix`
- `/360-ticket-resolver PROJ-123 feature/my-fix main`
- `/360-ticket-resolver PROJ-123 feature/my-fix develop`
- `/360-ticket-resolver PROJ-123 feature/my-fix --quick-fix`
- `/360-ticket-resolver PROJ-123 feature/my-fix main --quick-fix`
- `/360-ticket-resolver PROJ-123 feature/my-fix --skip-tests`
- `/360-ticket-resolver PROJ-123 feature/my-fix main --skip-tests`
- `/360-ticket-resolver PROJ-123 feature/my-fix --manual-test`
- `/360-ticket-resolver PROJ-123 feature/my-fix main --manual-test`

Parse args from `$ARGS`:
- `JIRA_TICKET` = first word (required)
- `WORK_BRANCH` = second word (required) — the branch to create and commit the fix on
- `SOURCE_BRANCH` = third word (optional, default: current git branch) — the branch to base `WORK_BRANCH` from; skip with a flag as the third word if no source branch
- `QUICK_MODE` = set to `true` if the flag `--quick-fix` appears anywhere in the args
- `SKIP_TESTS` = set to `true` if the flag `--skip-tests` appears anywhere in the args (ignored when `QUICK_MODE=true` since quick already skips tests)
- `MANUAL_TEST` = set to `true` if the flag `--manual-test` appears anywhere in the args (ignored when `QUICK_MODE=true` or `SKIP_TESTS=true`)

If `WORK_BRANCH` is missing, ask inline and wait for the reply:
> "Please provide a work branch name. Usage: /360-ticket-resolver TICKET-123 work-branch-name [source-branch] [--quick-fix] [--skip-tests] [--manual-test]"
Once the user supplies it, continue immediately — do not halt.

**Quick mode** (`--quick-fix` flag present):
- Phases 4, 5, 6 are **skipped entirely** — no code review, no test plan, no test execution
- Phase 2 (RCA + user confirmation), Phase 7 (Check-in), Phase 8 (PR — optional), and Phase 9 (Jira Update) still run — these are never skippable
- PR description and Jira comment are marked clearly as a quick fix with review and tests skipped

Display a notice at the start when quick mode is active:
> "⚡ Quick mode enabled — Code Review (Phase 4), Test Plan (Phase 5), and Test Execution (Phase 6) will be skipped. RCA confirmation, check-in, PR (optional), and Jira update still apply."

**Skip-tests mode** (`--skip-tests` flag present, `--quick-fix` not present):
- Phases 5 and 6 are **skipped entirely** — no test plan, no test execution
- Phase 4 (Code Review) still runs
- Phase 2 (RCA + user confirmation), Phase 7 (Check-in), Phase 8 (PR — optional), and Phase 9 (Jira Update) still run — these are never skippable
- PR description and Jira comment are marked as tests skipped

Display a notice at the start when skip-tests mode is active:
> "🚫 Skip-tests mode enabled — Test Plan (Phase 5) and Test Execution (Phase 6) will be skipped. Code review still applies."

**Manual-test mode** (`--manual-test` flag present, `--quick-fix` and `--skip-tests` not present):
- Phase 5 (Test Plan) runs fully and must be confirmed by the user as normal
- Phase 6 (Test Execution) skips the maturity assessment entirely and goes **directly to Path B** — no automated test writing, no relentless-fixer; the user is asked to manually verify each test case from the confirmed test plan
- Phase 4 (Code Review) still runs
- Phase 2 (RCA + user confirmation), Phase 7 (Check-in), Phase 8 (PR — optional), and Phase 9 (Jira Update) still run — these are never skippable
- PR description and Jira comment note that testing was done manually

Display a notice at the start when manual-test mode is active:
> "🖐 Manual-test mode enabled — Test Plan (Phase 5) will be created and confirmed as normal. Test Execution (Phase 6) will skip automated test writing and ask you to verify test cases manually."

---

## Project-Specific Guidance Files

Before starting, load the guidance files using the following lookup order for each file:

1. **Project docs (preferred):** `docs/360-ticket-resolver/<file>` — project-specific overrides, lives in the project repo alongside the code
2. **Skill default (fallback):** `.claude/skills/360-ticket-resolver/<file>` — generic guidelines, ships with the skill

| File | Purpose |
|---|---|
| `code-review-checklist.md` | Extra review checks applied during Phase 4 |
| `test-plan-guide.md` | Test strategy and TC structure guidance for Phase 5 |

**Loading rules:**
- Always load the skill default first (generic guidelines).
- If the project doc exists, load it too and apply it **in addition** — project-specific checks extend the generic ones; where there is overlap the project doc takes precedence.
- If neither exists, proceed with built-in best practices.
- Announce which files were loaded before Phase 1 begins.

---

## Phase 1 — Setup

### 1.1 Validate inputs

If `JIRA_TICKET` is blank, stop and ask:
> "Please provide a Jira ticket ID. Usage: /360-ticket-resolver TICKET-123 [source-branch]"

**Work branch must reference the ticket ID.**

Check that `WORK_BRANCH` contains `JIRA_TICKET` as a substring (case-insensitive). If it does not, ask inline and wait for the reply:
> "Work branch `WORK_BRANCH` does not reference the ticket ID `JIRA_TICKET`. The branch name must include the ticket ID, e.g. `hotfix/KR-20386-fix-scroll` or `fix/KR-20386`.
> Please provide a corrected branch name to continue."
Once the user supplies a valid branch name, update `WORK_BRANCH` and proceed — do not halt.

### 1.2 Verify Jira ticket exists

```bash
python .claude/skills/360-ticket-resolver/scripts/jira.py get-issue JIRA_TICKET
```

- If the script exits with HTTP 404 → ask inline and wait:
  > "Jira ticket `JIRA_TICKET` was not found. Please check the ticket ID and provide the correct one to continue."
  Once the user provides a corrected ticket ID, update `JIRA_TICKET` and retry. Do not halt.
- If the script exits with HTTP 401/403 → ask inline and wait:
  > "Jira authentication failed. Check that `ATLASSIAN_API_TOKEN` is set correctly in `~/.zshrc` and run `source ~/.zshrc`. Reply **retry** once fixed."
  On **retry**, re-run the script. Do not halt.
- If the script exits with a config error → show the exact error inline, ask the user to fix `config.yml` or the token, and reply **retry**. Do not halt.
- If successful → extract and display the ticket details. Proceed.

### 1.3 Verify the project exists in Bitbucket

```bash
python .claude/skills/360-ticket-resolver/scripts/bitbucket.py list-prs --state open
```

- If HTTP 404 → ask inline and wait:
  > "This repository was not found in Bitbucket (`WORKSPACE/REPO_SLUG`). Check that `bitbucket.workspace` in `config.yml` is correct and that the repo slug detected from git remote (`REPO_SLUG`) matches the Bitbucket repository name. Reply **retry** once fixed."
  On **retry**, re-run the script. Do not halt.
- If HTTP 401/403 → ask inline and wait:
  > "Bitbucket authentication failed. Check that `ATLASSIAN_API_TOKEN` in `~/.zshrc` has Repositories: Read + Write and Pull Requests: Read + Write permissions. Reply **retry** once fixed."
  On **retry**, re-run the script. Do not halt.
- If successful → Bitbucket connection confirmed. Proceed.

### 1.4 Determine and validate source branch

If `SOURCE_BRANCH` was provided use it. Otherwise detect current branch:
```bash
git branch --show-current
```

Verify the source branch exists on the remote:
```bash
git ls-remote --heads origin SOURCE_BRANCH
```

- If the output is empty → list available branches and ask inline, wait for the reply:
  > "Branch `SOURCE_BRANCH` does not exist on the remote. Available remote branches:
  > `<git branch -r output>`
  > Please tell me which branch to use as the source and I'll continue."
  Once the user picks a branch, update `SOURCE_BRANCH` and proceed — do not halt.

### 1.5 Sync source branch with remote

Before creating the work branch, bring the source branch fully up to date.

**Check for uncommitted local changes first:**
```bash
git status --short
```

If there are uncommitted changes on the current branch, AND the changes appear unrelated to the ticket being worked (e.g. no matching file paths, no ticket ID in filenames), ask inline and wait for the reply:
> "There are uncommitted changes on the current branch:
> `<git status output>`
>
> How would you like to handle them?
> - Reply **keep** if these changes ARE part of the fix and should be included (most common when the branch already has the fix started)
> - Reply **stash** to stash them temporarily (restored later with `git stash pop`)
> - Reply **commit** to commit them before we proceed (you'll provide a message)
> - Reply **discard** to discard them permanently — WARNING: this cannot be undone"

If the changes clearly belong to the ticket being worked (e.g. they are in the agentic/relevant component files), assume **keep** automatically and state this inline — do not ask.

Act based on the user's reply — keep the process running in all cases:
- **keep** → proceed without touching the working tree
- **stash** → `git stash push -m "pre-360-ticket-resolver stash for JIRA_TICKET"` then proceed
- **commit** → ask for a commit message inline, commit, then proceed
- **discard** → confirm once more inline ("Are you sure? This will permanently discard your changes. Reply **confirm-discard** to proceed."), then `git checkout .` and proceed

Once the working tree is clean, sync the source branch:
```bash
git checkout SOURCE_BRANCH
git fetch origin
git merge origin/SOURCE_BRANCH
```

- If the merge produces conflicts → show the conflicting files inline and wait for the reply:
  > "Merge conflicts detected when syncing `SOURCE_BRANCH` with remote:
  > `<conflicting files>`
  > Please resolve these conflicts manually, then reply **resolved** to continue."
  On **resolved**, verify with `git status` and proceed — do not halt.

- If the merge is clean → proceed.

### 1.6 Create work branch

```bash
git checkout -b WORK_BRANCH
```

- If the branch already exists → make a smart default decision and inform the user inline:
  - If we are **already on** `WORK_BRANCH` → state "Already on `WORK_BRANCH`, continuing from current state." and proceed immediately — no question needed.
  - If we are on a **different branch** → ask inline and wait:
    > "Branch `WORK_BRANCH` already exists. Reply **use-existing** to check it out and continue from where it left off, or provide a different branch name to use instead."
    - **use-existing** → `git checkout WORK_BRANCH` then proceed
    - new branch name → update `WORK_BRANCH` and proceed
    Do not offer "abort" — keep the process running.

---

## Phase 2 — Iterative RCA (Root Cause Analysis)

**Iron law: NO fix proposals until root cause is confirmed. Seeing a symptom ≠ knowing the root cause.**

### 2.1 Read the error carefully

Before touching any code:
- Read every error message, stack trace, and warning completely — they often contain the exact location
- Note file paths, line numbers, and error codes
- Do not skip past warnings assuming they are unrelated

### 2.2 Reproduce the bug

- Identify the exact steps that trigger the bug consistently
- If it cannot be reproduced reliably → gather more data, do not guess
- Check whether it is always broken or only under specific conditions (timing, data, environment)

### 2.3 Check recent changes

```bash
git log --oneline -20 -- <relevant-file>
git diff HEAD~5 -- <relevant-file>
```

- What changed recently that could have introduced this?
- New dependencies, config changes, environment differences?
- Is this a regression (worked before) or a missing feature (never worked)?

### 2.4 Trace the execution path backward

Do not fix where the error appears — trace back to where the bad value or bad state originates:

```
Symptom (where error surfaces)
  ↑ What called this with bad input?
  ↑ What called that?
  ↑ Keep tracing up until you find the original source
```

- Read the actual source files at each level — do not assume
- Follow data flow: where does the bad value get set? Where does the bad state first enter?
- Fix at the **source**, not at the symptom

### 2.5 Gather evidence at component boundaries

For bugs in multi-component systems (API → service → store, LLM → parser → state):

Add temporary diagnostic logging at each boundary to see exactly where the data goes wrong:

```
For EACH component boundary:
  - What data enters this component?
  - What data exits it?
  - Is the state correct at this layer?

Run once to observe — THEN analyse — THEN investigate the failing layer
```

Remove diagnostic logging before committing.

### 2.6 Find the pattern — compare working vs broken

- Locate similar working code in the same codebase
- List every difference between the working and broken paths, however small
- Understand what assumption the broken code makes that the working code does not

### 2.7 Form a single hypothesis

State it explicitly before proceeding:

> "I believe the root cause is **X** in **file:line** because **evidence Y**."

- One hypothesis at a time — test the most likely first
- If the hypothesis is wrong, form a new one — do NOT stack fixes on top of each other
- If 3+ hypotheses have been tested and all failed → the architecture itself may be the problem; present this conclusion inline, summarise what was ruled out, and ask the user how to proceed — do not halt

### 2.8 Present RCA

Only present the RCA once the root cause is confirmed by evidence, not by intuition.

```
═══════════════════════════════════════════════════════════
ROOT CAUSE ANALYSIS — JIRA_TICKET
═══════════════════════════════════════════════════════════

TICKET SUMMARY:
  <one-line summary of the bug>

AFFECTED COMPONENTS:
  <list of files / classes / modules involved — with line numbers>

EXECUTION TRACE:
  <backward trace from symptom to original trigger, step by step>

ROOT CAUSE:
  <the actual defect — specific file, line, method, and why it is wrong>

EVIDENCE:
  <what you observed that confirms this is the root cause, not a symptom>

WHY IT MANIFESTS AS REPORTED:
  <connect root cause to the user-visible symptom>

IMPACT:
  <what else might be affected by this root cause>

PROPOSED FIX:
  <minimal change at the source — not a symptom patch>
═══════════════════════════════════════════════════════════
```

### 2.9 User confirmation loop

Present the RCA and ask:
> "Does this RCA look correct? Reply **yes** to proceed to the fix, or tell me what's wrong and I'll investigate further."

- **yes** → proceed to Phase 3 immediately.
- **any feedback** → refine the RCA, re-present, ask again. Keep the loop going until confirmed.

**Do not halt — keep the conversation running until the user confirms.**

**Save confirmed RCA text** — it will be included in the PR description.

---

## Phase 3 — Code Changes

### 3.1 Implement the fix

Apply the fix identified in the confirmed RCA:

- Make the minimal change necessary to fix the root cause.
- Do not refactor unrelated code.
- Do not add features beyond the fix.
- Follow existing code style and conventions in the file.
- Add inline comments only where the fix logic is non-obvious.

### 3.2 Verify it compiles / builds

Run the project build to confirm nothing is broken at compile time:
```bash
# Detect and run the appropriate build command for the project
# (e.g. ./gradlew build -x test, mvn compile, npm run build)
```

If the build fails, fix compilation errors before proceeding.

---

## Phase 4 — Iterative Code Review

> **Quick mode:** If `QUICK_MODE=true`, skip this entire phase and proceed directly to Phase 5.
> Print: "⚡ Skipping Phase 4 — Code Review (quick mode)"

### 4.1 Load review checklist

Load checklists using the two-level lookup:
1. `.claude/skills/360-ticket-resolver/code-review-checklist.md` — generic default (always load)
2. `docs/360-ticket-resolver/code-review-checklist.md` — project-specific additions (load if present, apply on top of generic)

If neither file exists, use the built-in general checklist below.

**General code review checklist (always applied):**
- Does the fix address the root cause and only the root cause?
- Are there any null pointer or out-of-bounds risks introduced?
- Are edge cases handled (empty collections, null inputs, boundary values)?
- Is error handling consistent with the rest of the codebase?
- Are there any security implications (injection, auth bypass, data exposure)?
- Does the fix introduce any concurrency issues?
- Are log statements at the correct level with sufficient context?
- Is the change backwards-compatible?

### 4.2 Self-review and present findings

Review the diff against both the general checklist and the project-specific checklist (if loaded). Present the findings — do NOT apply any fixes yet:

```
═══════════════════════════════════════════════════════════
CODE REVIEW — Iteration N
═══════════════════════════════════════════════════════════

DIFF SUMMARY:
  <files changed, lines added/removed>

REVIEW FINDINGS:
  ✓ <passed check>
  ✗ <failed check — description and why it matters>
  ⚠ <warning — not blocking but worth noting>

VERDICT: PASS | FAIL
═══════════════════════════════════════════════════════════
```

### 4.3 After presenting findings — branch on verdict

**If VERDICT is PASS (no `✗` items):**
Do NOT show the fix/discuss/skip options menu. Go directly to the transition confirmation (4.4) — the review is clean and execution should continue.

**If VERDICT is FAIL (one or more `✗` items):**
Show the user the findings and offer the fix/discuss/skip options:

> "The review found some issues above.
> - Reply **fix** to apply all the fixes now.
> - Reply **discuss** (or ask any question) to talk through a finding before deciding.
> - Reply **skip `<finding>`** to accept a specific finding as-is and explain why."

**Behaviour at each reply:**

- **fix** → apply fixes for every `✗` item, then re-run the full review from 4.2 and present updated findings. If the new verdict is PASS go to 4.4; if still FAIL show the options again.
- **discuss / any question** → explain the finding in more detail, suggest alternatives, update the finding if the user's point is valid. Re-present the review. Show options again.
- **skip `<finding>`** → mark that finding as accepted-by-owner with the user's rationale, treat it as `✓` going forward. Re-present the updated review. If now PASS go to 4.4; if still FAIL show options again.

**Never auto-apply fixes without the user saying "fix".** The user may want to discuss or override first.

Keep iterating until all `✗` items are fixed or explicitly skipped, then go to 4.4.

### 4.4 Transition confirmation

Once the verdict is PASS, immediately ask — the skill is still running, waiting for the answer:
> "Code review passed ✓. Shall we move on to the Test Plan?"

- **yes** → proceed to Phase 5 immediately.
- **no** → ask what the user would like to do next. Do not halt; keep the conversation open.

---

## Phase 5 — Iterative Test Plan

> **Quick mode:** If `QUICK_MODE=true`, skip this entire phase and proceed directly to Phase 6.
> Print: "⚡ Skipping Phase 5 — Test Plan (quick mode)"
>
> **Skip-tests mode:** If `SKIP_TESTS=true`, skip this entire phase and proceed directly to Phase 6.
> Print: "🚫 Skipping Phase 5 — Test Plan (--skip-tests)"

### 5.1 Load test plan guide

Load guides using the two-level lookup:
1. `.claude/skills/360-ticket-resolver/test-plan-guide.md` — generic default (always load)
2. `docs/360-ticket-resolver/test-plan-guide.md` — project-specific additions (load if present, apply on top of generic)

If neither file exists, use built-in general test planning best practices.

### 5.2 Create test plan

Based on the ticket type, root cause, and fix, produce a test plan:

```
═══════════════════════════════════════════════════════════
TEST PLAN — JIRA_TICKET
═══════════════════════════════════════════════════════════

BUG BEING FIXED:
  <one-liner>

TEST STRATEGY:
  <unit / integration / e2e — which levels and why>

TEST CASES:

  TC-1: [Regression] Reproduce the original bug
    Given: <precondition>
    When:  <action>
    Then:  <expected result that was previously broken>

  TC-2: [Happy path] Normal flow still works
    Given: <precondition>
    When:  <action>
    Then:  <expected result>

  TC-3: [Edge case] <describe edge case>
    Given: <precondition>
    When:  <action>
    Then:  <expected result>

  ... (add as many as needed)

OUT OF SCOPE:
  <what is explicitly not tested and why>
═══════════════════════════════════════════════════════════
```

### 5.3 User confirmation loop

Present the test plan and immediately ask — the skill is still running:

> "Here is the test plan. Reply **confirm** to proceed, or give me feedback (add a case, remove one, challenge the strategy) and I'll update it."

**Behaviour at each reply — keep the loop running in all cases:**

- **confirm** → save the final test plan text and proceed to Phase 6 immediately.
- **add `<scenario>`** → draft the new TC in Given/When/Then format, append it to the plan, re-present. Ask again.
- **remove `<TC-N>`** → remove it, briefly explain what it guarded against, re-present. Ask again.
- **discuss `<TC-N>`** → explain why it was included; update or remove if the user's argument is valid. Re-present. Ask again.
- **discuss strategy** → explain the rationale, propose alternatives, update if agreed. Re-present. Ask again.
- **any other feedback** → apply it, re-present the updated plan. Ask again.

**Never halt — keep iterating until the user says confirm.**

**Save confirmed test plan text** — it will be included in the PR description.

---

## Phase 6 — Test Execution

> **Quick mode:** If `QUICK_MODE=true`, skip this entire phase and proceed directly to Phase 7 (Check-in).
> Print: "⚡ Skipping Phase 6 — Test Execution (quick mode)"
>
> **Skip-tests mode:** If `SKIP_TESTS=true`, skip this entire phase and proceed directly to Phase 7 (Check-in).
> Print: "🚫 Skipping Phase 6 — Test Execution (--skip-tests)"
>
> **Manual-test mode:** If `MANUAL_TEST=true`, skip the maturity assessment entirely and jump directly to **Path B**. Do not write any test code. Do not run any commands.
> Print: "🖐 Manual-test mode — skipping automated test execution. Proceeding to manual verification."

### 6.1 Assess the project's test maturity

> **Skip if `MANUAL_TEST=true`** — jump straight to 6.2 Path B.

Before writing or running anything, inspect the project to understand its test posture:

**Signals of an actively maintained test suite:**
- A dedicated test directory exists (`src/test/`, `__tests__/`, `spec/`, `tests/`) with multiple files
- A test runner is configured in the build file (`./gradlew test`, `npm test`, `pytest`, `mvn test`, etc.)
- Test files have been modified recently (`git log --oneline -10 -- src/test/`)
- CI configuration (`.github/workflows/`, `Jenkinsfile`, `.gitlab-ci.yml`) runs tests automatically
- Test count is meaningful (more than a handful of trivial tests)

**Signals of a project without active test culture:**
- No test directory, or an empty/near-empty one
- No test runner configured in the build file
- Test files not touched in months despite active development
- Only auto-generated boilerplate tests with no real assertions
- No CI pipeline running tests

### 6.2 Branch based on test maturity

---

#### Path A — Active test framework detected

> **Note:** Path A is never taken when `MANUAL_TEST=true`.

Proceed with automated test implementation and relentless execution:

**6.2A.1 Implement the test cases**

Write the actual test code from the confirmed test plan:
- Place tests in the correct test directory and package
- Follow existing test naming and structure conventions in the project
- Use real dependencies (no mocks unless the project already uses them)
- Each TC from the confirmed test plan must have at least one corresponding test method

**6.2A.2 Run tests relentlessly**

Invoke the **relentless-fixer** skill:

```
Use the relentless-fixer skill.

Command: <detected test command, e.g. ./gradlew test>
Success: All tests pass, exit code 0.

Run until every single test passes. Fix root causes only.
No disabling, no workarounds, no partial solutions.
```

Do not proceed to Phase 7 (Check-in) until all tests pass with exit code 0.

---

#### Path B — Manual verification (no automated tests)

This path is taken when either:
- The maturity assessment (6.1) determined no active test framework exists, **or**
- `MANUAL_TEST=true` was set — in which case jump here directly without any assessment

**If arriving from maturity assessment (not `--manual-test`)**, inform the user:

> "I've looked at the project structure and it does not appear to have an actively maintained test suite — [state what you found: no test directory / no test runner configured / test files not recently updated / etc.].
>
> I can still write test code for the confirmed test cases, but there is no automated way to run them reliably in this project right now."

**In all cases** (both `--manual-test` and auto-detected), present the manual verification checklist:

> "**Please manually verify the test plan against your changes:**
> ```
> TC-1: [Regression] <description> — verified? y/n
> TC-2: [Happy path] <description> — verified? y/n
> TC-3: [Edge case] <description> — verified? y/n
> ...
> ```
> Reply **verified** once you have manually tested all cases and are satisfied, and I will proceed to Phase 7."

- **verified** → proceed to Phase 7 (Check-in) immediately.
- **issues found** → treat as a bug, return to Phase 3 to fix, then re-present the checklist. Keep the loop going.
- **wants to set up a test framework** → help set it up, then switch to Path A. Keep the loop going. (Only applicable when NOT in `--manual-test` mode.)

---

## Phase 7 — Check-in

### 7.1 User confirmation before commit

Show the user what will be committed:

```bash
git diff --stat HEAD
```

If `QUICK_MODE=true`, ask:
> "⚡ Quick fix ready to commit. Code review, test plan, and test execution were skipped.
>
> Files changed:
> `<git diff --stat output>`
>
> Branch: `WORK_BRANCH` → remote. Shall I commit and push?"

Otherwise ask:
> "Tests are passing. Here are the files that will be committed:
>
> `<git diff --stat output>`
>
> Branch: `WORK_BRANCH` → remote. Shall I commit and push?"

- **yes** → proceed to 7.2 immediately.
- **no** → ask what the user would like to do instead. Keep the conversation open — do not halt.

### 7.2 Stage and commit

```bash
git add -p   # stage only relevant changes (review each hunk)
git commit -m "fix(JIRA_TICKET): <one-line summary from RCA>

<2-3 sentence description of root cause and fix>

Jira: JIRA_TICKET"
```

### 7.3 Push branch

```bash
git push -u origin WORK_BRANCH
```

Confirm the push succeeded, then proceed to Phase 8.

---

## Phase 8 — Pull Request (Optional)

### 8.1 Ask whether to raise a PR

Ask the user:
> "Check-in complete. Branch `WORK_BRANCH` has been pushed.
>
> Would you like to raise a Pull Request to `SOURCE_BRANCH`?
> Reply **yes** to preview the PR, or **no** to skip directly to Jira update."

- **yes** → continue to 8.2 immediately.
- **no** → print: "Skipping PR — moving to Jira update." Proceed to Phase 9 with `PR_URL=null`.

### 8.2 Gather metadata before composing

Before composing the PR body, collect two pieces of information:

**Release Vehicle:**
- Check the ticket's Fix Version field (already fetched in Phase 1).
- If a fix version is set → use it as `RELEASE_VEHICLE`.
- If not set → ask inline and wait:
  > "What is the Release Vehicle (fix version) for this PR? e.g. `3.6.0`"
  Use the user's reply as `RELEASE_VEHICLE`.

**Additional Related Jira Tickets:**
- `JIRA_TICKET` (the ticket being fixed) is always included.
- Ask inline and wait:
  > "Any additional related Jira tickets to link in the PR? (e.g. `KR-12345: <summary>`) Reply **none** if not."
- Collect all tickets the user provides into `RELATED_TICKETS`.

### 8.3 Show PR content for review

Compose the full PR content and display it to the user **before** raising it.

All modes share the same compact body structure — the mode indicator line and checklist entries adjust per mode.

```
═══════════════════════════════════════════════════════════
PULL REQUEST PREVIEW  [⚡ Quick Fix | 🚫 Tests Skipped | 🖐 Manually Tested | omit for standard]
═══════════════════════════════════════════════════════════

TITLE:
  fix(JIRA_TICKET): <ticket summary>

SOURCE → TARGET:
  WORK_BRANCH → SOURCE_BRANCH

BODY:
  **Root Cause Analysis (RCA):**
  <2–3 sentence paragraph — what the root cause was, where it lives, and
  why it manifests as the reported symptom. Derived from confirmed Phase 2 RCA.>

  **Fix:**
  <1–2 sentences — the specific change made and why it resolves the root cause>

  **Regression Area:**
  - <primary affected user workflow or component>
  - <secondary area / other callers affected, if any>

  **Release Vehicle:** RELEASE_VEHICLE

  **Related Jira Tickets:**
  - JIRA_TICKET: <ticket summary> (this fix)
  - <each entry from RELATED_TICKETS, one per line>

  ---

  **Dev Test Cases:**
  **TC-1: [<Type>]** <description>
    Given: <precondition>
    When:  <action>
    Then:  <expected result>

  **TC-2: [<Type>]** <description>
    Given: <precondition>
    When:  <action>
    Then:  <expected result>

  <repeat for each TC — one blank line between cases>
  [If QUICK_MODE=true: "Skipped — quick mode."]
  [If SKIP_TESTS=true: "Skipped — --skip-tests."]

  ---
  [Include the relevant mode line only if a flag was active — omit entirely for standard mode:]
  ⚡ Quick fix — code review, test plan, and test execution skipped.
  🚫 Tests skipped — test plan and test execution skipped (--skip-tests). Code review was performed.
  🖐 Manually tested — automated test execution skipped (--manual-test). Test cases verified manually by author.

  **Checklist:**
  - [ ] RCA confirmed by author
  - [ ] Code review passed                  [or: SKIPPED — quick mode]
  - [ ] Test plan confirmed by author        [or: SKIPPED — quick/skip-tests]
  - [ ] Tests: all passing / manually verified  [or: SKIPPED — quick/skip-tests]

═══════════════════════════════════════════════════════════
```

### 8.4 User confirmation loop for PR content

After displaying the preview, ask:
> "Here is the PR content above.
> - Reply **raise** to raise the PR as shown.
> - Provide any feedback or changes to incorporate before raising (e.g. 'update the title', 'add a note about X').
> - Reply **skip** to cancel the PR and move directly to Jira update."

**Behaviour at each reply:**

- **raise** → raise the PR (step 8.5) and proceed to Phase 9 immediately.
- **skip** → print: "PR skipped — moving to Jira update." Proceed to Phase 9 with `PR_URL=null`.
- **any feedback** → apply the changes, re-display the updated preview, ask again. Keep the loop going.

**Never raise the PR without an explicit "raise". Never halt — always wait for the next reply.**

### 8.5 Raise the PR

```bash
python3 .claude/skills/360-ticket-resolver/scripts/bitbucket.py create-pr \
  --title "fix(JIRA_TICKET): <ticket summary>" \
  --source "WORK_BRANCH" \
  --target "SOURCE_BRANCH" \
  --body "<final approved PR body>"
```

Capture the `PR_URL` printed by the script. Proceed to Phase 9.

---

## Phase 9 — Jira Ticket Update

### 9.1 Remind user about optional field updates

Before composing the comment, show the user a checklist of common Jira fields they may want to update. This is a **gentle reminder only** — do not force or assume any changes.

Display:

```
═══════════════════════════════════════════════════════════
JIRA FIELD REMINDER — JIRA_TICKET
═══════════════════════════════════════════════════════════

Do you want to update any of the following fields?
(Just tell me what to change — or say "none" / "skip" to go straight to the comment)

  [ ] Status          — e.g. move to In Review, QA, Done
  [ ] Assignee        — e.g. reassign to dev, lead, or reviewer
  [ ] QA Assignee     — assign who will test this fix
  [ ] Fix Version     — version in which this fix will ship
  [ ] Affected Version — version(s) where the bug was observed
  [ ] Release Vehicle — release train or milestone this fix belongs to
  [ ] Dev Complete Date — date the dev work is done (today?)
  [ ] Any other field — just tell me

Reply with what you'd like to change, or reply "none" to skip field updates.
═══════════════════════════════════════════════════════════
```

**Behaviour:**

- **"none" / "skip" / no changes wanted** → proceed to 9.2 with no field updates queued.
- **Any field change stated** → acknowledge each one, confirm the intended value back to the user (e.g. "Got it — set Status to `In Review`, Fix Version to `2.5.1`. Anything else?"), and keep accepting additional changes until the user signals done. Collect all requested field updates into a `FIELD_UPDATES` list that will be applied in 9.4.

### 9.2 Compose the Jira comment

Compose the Jira comment and display it to the user **before** posting:

**If PR was raised:**

```
═══════════════════════════════════════════════════════════
JIRA UPDATE PREVIEW — JIRA_TICKET
═══════════════════════════════════════════════════════════

Adding comment to: JIRA_BASE_URL/browse/JIRA_TICKET

COMMENT:
  PR raised: <PR_URL>
  Branch: WORK_BRANCH → SOURCE_BRANCH

  RCA summary: <one paragraph from confirmed RCA>

  Fix summary: <one-line description of what was changed and why>
═══════════════════════════════════════════════════════════
```

**If PR was skipped:**

```
═══════════════════════════════════════════════════════════
JIRA UPDATE PREVIEW — JIRA_TICKET
═══════════════════════════════════════════════════════════

Adding comment to: JIRA_BASE_URL/browse/JIRA_TICKET

COMMENT:
  Fix committed to branch: WORK_BRANCH (no PR raised)

  RCA summary: <one paragraph from confirmed RCA>

  Fix summary: <one-line description of what was changed and why>
═══════════════════════════════════════════════════════════
```

**Quick mode** — prepend the comment with:
> ⚡ Quick mode — code review, test plan, and test execution were skipped.

If field updates were collected in 9.1, also append a `FIELD UPDATES` section to the preview block:

```
FIELD UPDATES:
  Status          → <new value>     (if requested)
  Assignee        → <new value>     (if requested)
  QA Assignee     → <new value>     (if requested)
  Fix Version     → <new value>     (if requested)
  Affected Version → <new value>    (if requested)
  Release Vehicle → <new value>     (if requested)
  Dev Complete Date → <new value>   (if requested)
  <other field>   → <new value>     (if requested)
```

### 9.3 User confirmation loop for Jira update

After displaying the full preview (comment + any field updates), ask:
> "Here is the full Jira update above.
> - Reply **post** to apply the comment and all field updates.
> - Provide any feedback or corrections before posting.
> - Reply **skip** to skip the Jira update entirely."

**Behaviour at each reply:**

- **post** → run the Jira scripts (steps 9.4 and 9.5) and proceed to Completion immediately.
- **skip** → print: "Jira update skipped." Proceed to Completion.
- **any feedback** → apply the changes, re-display the updated preview, ask again. Keep the loop going.

### 9.4 Post the Jira comment

```bash
python3 .claude/skills/360-ticket-resolver/scripts/jira.py add-comment JIRA_TICKET \
  "<final approved comment>"
```

### 9.5 Apply field updates (only if any were requested)

For each field update collected in 9.1, call the appropriate Jira script command. Run field updates that have dedicated script support; for fields without direct script support, use the generic edit command:

```bash
# Status transition (use transition ID or name)
python3 .claude/skills/360-ticket-resolver/scripts/jira.py transition JIRA_TICKET "<status name>"

# Field update (assignee, fix version, affected version, custom fields, etc.)
python3 .claude/skills/360-ticket-resolver/scripts/jira.py edit-issue JIRA_TICKET \
  --field "<field name>" --value "<value>"
```

If a field update fails (e.g. invalid transition, unknown field name), report the error clearly to the user and ask how to proceed — do not silently skip it.

---

## Completion

Output a final summary:

```
═══════════════════════════════════════════════════════════
360 TICKET RESOLVER COMPLETE — JIRA_TICKET
═══════════════════════════════════════════════════════════

✓ Phase 1  — Branch WORK_BRANCH created from SOURCE_BRANCH
✓ Phase 2  — RCA confirmed by user
✓ Phase 3  — Code fix implemented
✓ Phase 4  — Code review passed (N iterations)        [skipped if --quick-fix]
✓ Phase 5  — Test plan confirmed by user               [skipped if --quick-fix or --skip-tests]
✓ Phase 6  — All tests passing / manually verified     [skipped if --quick-fix or --skip-tests; manual verification if --manual-test]
✓ Phase 7  — Changes committed and pushed
✓ Phase 8  — PR raised / skipped (user choice)
✓ Phase 9  — Jira ticket updated / skipped (user choice)
             Comment posted + field updates applied (Status, Assignee, Fix Version, etc.)

PR:     <PR URL or "not raised">
Ticket: <Jira URL>
═══════════════════════════════════════════════════════════
```

---

## Key Principles

- **Bell before every user gate** — Immediately before presenting any question that requires the user's input (confirmation, approval, feedback, retry, or decision), run `printf '\a'` as a **dedicated, standalone Bash tool call** — never combined with other commands. The bell call and the question text must be adjacent: bell fires, then question appears immediately after. Running the bell early (e.g. during a branch listing step) and showing the question later does not work — the macOS dock badge will not fire reliably.
- **Never halt the process** — When a blocker, ambiguity, or decision point is encountered, present it inline as a question and wait for the user's reply. The process must stay alive and running until Completion. The word "stop" in this skill always means "ask inline and wait" — never terminate the execution. The only exception is if the user explicitly says to abort.
- **Make smart defaults** — When context makes the correct action obvious (e.g. already on the right branch, changed files match the ticket, fix is already applied), take the sensible default action, state it inline, and continue — do not ask unnecessarily.
- **User accountability at every gate** — RCA and test plan are user-confirmed, not assumed.
- **No skipping phases** — each phase produces an artifact the next phase depends on.
- **Project knowledge compounds** — the better `.claude/skills/360-ticket-resolver/` files are, the better every resolution gets. Anyone with project knowledge can improve them.
- **PR tells the full story** — RCA + test plan in every PR means reviewers understand the why, not just the what.

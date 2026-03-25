# 360 Ticket Resolver — Skill

A Claude Code skill that takes a Jira ticket and walks you through the full resolution lifecycle: smart root cause analysis, code fix, interactive code review, test plan, test execution, and a PR raised with full context — all in one session.

---

## What It Does

Running `/360-ticket-resolver TICKET-123` drives you through 7 phases:

| Phase | What happens |
|---|---|
| **1 — Setup** | Validates the Jira ticket, verifies the repo exists in Bitbucket, checks the source branch, syncs it with remote, creates your work branch |
| **2 — RCA** | Reads errors carefully, traces execution backward to the root cause (not just the symptom), forms a single evidence-backed hypothesis, presents a structured RCA for your confirmation |
| **3 — Code Fix** | Implements the minimal fix at the root cause; verifies it compiles |
| **4 — Code Review** | Reviews the diff against a generic checklist + your project-specific checklist; shows findings first, waits for you to say fix / discuss / skip before touching anything |
| **5 — Test Plan** | Drafts a test plan (regression + happy path + edge cases); shows it first, lets you add / remove / discuss each TC before confirming |
| **6 — Test Execution** | Detects whether the project has an active test framework; if yes runs tests relentlessly until green; if no guides you through manual verification |
| **7 — PR & Jira** | Commits, pushes, raises a Bitbucket PR with the confirmed RCA + test plan in the description, adds a comment to the Jira ticket with the PR link |

Every phase has a human confirmation gate — nothing is committed, pushed, or merged without your explicit sign-off.

---

## Before You Use This Skill

You need **two separate API tokens** — one for Jira and one for Bitbucket. Atlassian granular tokens are scoped to a single product, so they cannot be shared across both services.

---

### Step 1 — Create the Jira API token

Create a **Classic API token** (the standard, general-purpose type — not a granular/product-scoped token):

1. Go to: `https://id.atlassian.com/manage-profile/security/api-tokens`
2. Click **Create API token**
3. Enter a name (e.g. `claude-code-jira`) and set an expiry
4. **Important:** click **Create token** directly — do NOT click **Next** or select an app. Classic tokens do not require product or scope selection.
5. Copy the token value immediately (it is shown only once)

> The Classic API token is used with Basic auth (`email:token`) directly against your Jira instance URL. It does not require product selection or scope configuration — permissions are governed by your Jira account's project access.

---

### Step 2 — Create the Bitbucket API token

1. Go to: `https://id.atlassian.com/manage-profile/security/api-tokens`
2. Click **Create API token**
3. Enter a name (e.g. `claude-code-bitbucket`) and set an expiry
4. Click **Next** — on the **Select app** step choose **Bitbucket**
5. Click **Next** — on the **Select scopes** step search for and tick:
   - `repository:read` — read repo info and branches
   - `pullrequest:read` — list pull requests
   - `pullrequest:write` — create and update pull requests
6. Click **Next** then **Create token** — copy the value immediately

---

### Step 3 — Add both tokens to your shell profile

Open `~/.zshrc` (or `~/.bashrc`) and add:

```bash
export JIRA_API_TOKEN="your-jira-token-here"
export BITBUCKET_API_TOKEN="your-bitbucket-token-here"
```

Then reload your shell:

```bash
source ~/.zshrc
```

### Step 4 — Configure the skill for your project

Edit `.claude/skills/360-ticket-resolver/config.yml` (already in the repo — just update the values):

```yaml
jira:
  base_url: "https://your-org.atlassian.net"   # Your Jira Cloud base URL
  username: "you@yourcompany.com"               # Your Atlassian account email

bitbucket:
  base_url: "https://bitbucket.org"             # Keep as-is for Bitbucket Cloud
  workspace: "your-workspace-slug"              # Your Bitbucket workspace (from the URL)
```

> **Repo slug** is auto-detected from your git remote — you do not need to configure it.
> The skill reads `git remote get-url origin` and parses the repo name automatically.

### Step 5 — Add permissions to avoid repeated prompts

The skill runs several bash commands automatically. Without pre-approving them, Claude Code will prompt you for permission on every command — which interrupts the flow.

Add the following to your project's `.claude/settings.local.json` under `permissions.allow`:

```json
"Bash(python3 */.claude/skills/360-ticket-resolver/scripts/*:*)",
"Bash(python */.claude/skills/360-ticket-resolver/scripts/*:*)",
"Bash(printf *)"
```

Full example `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(python3 */.claude/skills/360-ticket-resolver/scripts/*:*)",
      "Bash(python */.claude/skills/360-ticket-resolver/scripts/*:*)",
      "Bash(printf *)"
    ]
  }
}
```

> **Why `*/.claude/...` instead of `.claude/...`?** The skill invokes scripts using the absolute path to the repo. A relative-path pattern like `.claude/skills/...` won't match an absolute path like `/Users/you/projects/myrepo/.claude/skills/...`. The leading `*/` wildcard covers any absolute prefix so the permission works regardless of where the repo is checked out.

> **Git commands** are not pre-approved by default — Claude Code will prompt you when the skill runs git commands. Use **"Yes, don't ask again this session"** at the prompt to approve for the current session only, without persisting to any settings file.

### Step 6 — Verify the setup

Run a quick smoke test from inside the project:

```bash
python3 .claude/skills/360-ticket-resolver/scripts/jira.py get-issue YOUR-TICKET-ID
python3 .claude/skills/360-ticket-resolver/scripts/bitbucket.py list-prs --state open
```

If both print results without errors, you are ready to go.

---

## Usage

```
/360-ticket-resolver <JIRA_TICKET> <work-branch> [source-branch] [--quick-fix] [--skip-tests] [--manual-test]
```

**Examples:**

```
/360-ticket-resolver PROJ-123 feature/my-fix
/360-ticket-resolver PROJ-123 feature/my-fix main
/360-ticket-resolver PROJ-123 feature/my-fix develop
/360-ticket-resolver PROJ-123 feature/my-fix --quick-fix
/360-ticket-resolver PROJ-123 feature/my-fix main --quick-fix
/360-ticket-resolver PROJ-123 feature/my-fix --skip-tests
/360-ticket-resolver PROJ-123 feature/my-fix main --skip-tests
/360-ticket-resolver PROJ-123 feature/my-fix --manual-test
/360-ticket-resolver PROJ-123 feature/my-fix main --manual-test
```

- `JIRA_TICKET` — required. The full Jira ticket ID (e.g. `PROJ-123`, `ANT-456`).
- `work-branch` — required. The branch name to create and commit your fix on. You choose the name.
- `source-branch` — optional. The branch to base your work branch from. Defaults to your current branch.
- `--quick-fix` — optional flag. Skips code review, test plan, and test execution (see below).
- `--skip-tests` — optional flag. Skips test plan and test execution only; code review still runs (see below).
- `--manual-test` — optional flag. Test plan is created and confirmed as normal; test execution skips automated testing and asks you to verify each test case manually (see below).

---

## Quick Mode

Add the flag `--quick-fix` anywhere in the arguments to skip the review and test phases and go straight from fix to PR.

```
/360-ticket-resolver PROJ-123 feature/my-fix --quick-fix
/360-ticket-resolver PROJ-123 feature/my-fix main --quick-fix
```

**What is skipped in quick mode:**

| Phase | Standard | Quick |
|---|---|---|
| 1 — Setup | ✓ | ✓ |
| 2 — RCA + user confirmation | ✓ | ✓ |
| 3 — Code fix | ✓ | ✓ |
| 4 — Code review | ✓ | ⚡ Skipped |
| 5 — Test plan | ✓ | ⚡ Skipped |
| 6 — Test execution | ✓ | ⚡ Skipped |
| 7 — PR confirmation + commit | ✓ | ✓ |

**RCA confirmation and PR confirmation are never skipped** — you always review the root cause analysis before any code is written, and always confirm before anything is committed or pushed.

**The PR and Jira comment are clearly marked** as a quick fix with code review, test plan, and test results sections explicitly noted as skipped. This keeps the PR history transparent for reviewers.

---

## Skip-Tests Mode

Add `--skip-tests` to skip the test plan and test execution phases while keeping the code review. Use this when you want review quality but are deferring testing to a later step (e.g. manual QA, a separate test pass, or a project with no automated tests).

```
/360-ticket-resolver PROJ-123 feature/my-fix --skip-tests
/360-ticket-resolver PROJ-123 feature/my-fix main --skip-tests
```

**What is skipped with `--skip-tests`:**

| Phase | Standard | --manual-test | --skip-tests | --quick-fix |
|---|---|---|---|---|
| 1 — Setup | ✓ | ✓ | ✓ | ✓ |
| 2 — RCA + user confirmation | ✓ | ✓ | ✓ | ✓ |
| 3 — Code fix | ✓ | ✓ | ✓ | ✓ |
| 4 — Code review | ✓ | ✓ | ✓ | ⚡ Skipped |
| 5 — Test plan | ✓ | ✓ | 🚫 Skipped | ⚡ Skipped |
| 6 — Test execution | ✓ automated | 🖐 Manual only | 🚫 Skipped | ⚡ Skipped |
| 7 — PR confirmation + commit | ✓ | ✓ | ✓ | ✓ |

**The PR and Jira comment are clearly marked** as tests-skipped so reviewers know testing was not performed as part of this resolution.

---

## Manual-Test Mode

Add `--manual-test` when you want the full test plan created and confirmed, but prefer to verify test cases yourself rather than have automated tests written and run. The skill skips the maturity check entirely and goes straight to asking you to manually tick off each test case.

```
/360-ticket-resolver PROJ-123 feature/my-fix --manual-test
/360-ticket-resolver PROJ-123 feature/my-fix main --manual-test
```

Use this when:
- The project has a test suite but the fix is too UI-heavy or integration-heavy to automate quickly
- You want to do a manual exploratory check against the test plan before committing
- You're in a hurry but still want the test plan in the PR for reviewers

The PR includes the full confirmed test plan and notes that verification was done manually.

---

## Customising the Skill for Your Project

The skill uses a **two-level lookup** for its guidance files. Generic defaults ship with the skill; project-specific additions live in your project's `docs/` folder alongside the code.

### How the lookup works

For each guidance file the skill checks two locations in order:

1. `.claude/skills/360-ticket-resolver/<file>` — **generic default**, ships with the skill, contains universal best-practice guidelines. Edit this only if you want to change behaviour across all projects.
2. `docs/360-ticket-resolver/<file>` — **project-specific override**, lives in your project repo. The skill loads this on top of the generic default — project checks extend and take precedence where there is overlap.

If only the generic file exists, the skill uses that. If neither exists, it falls back to built-in best practices.

### `docs/360-ticket-resolver/code-review-checklist.md`

Used during **Phase 4 (Code Review)**. Put your project-specific checks here:
- Framework/library constraints ("never instantiate X directly — use the singleton")
- Architectural rules ("all controllers must be stateless")
- Known pitfalls ("LLM JSON responses must go through `stripMarkdownFences()` before parsing")
- Tech-stack–specific checks ("use `var`, records, pattern matching — Java 21 only")

Anyone who knows the project well should contribute here. The more precise this file is, the more useful the automated review becomes.

### `docs/360-ticket-resolver/test-plan-guide.md`

Used during **Phase 5 (Test Plan)**. Put your project-specific test guidance here:
- How to run tests (commands, flags, watch vs CI mode)
- Where test files live and how they are named
- What test framework and assertion style to use
- How to seed and reset test data
- Project-specific TC patterns (component tests, async patterns, i18n setup, etc.)

Keep this current as the project grows. A new team member should be able to write their first test by reading this file alone.

---

## Files at a Glance

```
# Skill files (ship with the skill — generic defaults)
.claude/skills/360-ticket-resolver/
├── SKILL.md                    # Skill definition — the phases and logic
├── README.md                   # This file
├── config.yml                  # Non-secret config (commit this)
├── code-review-checklist.md    # Generic review checklist (fallback)
├── test-plan-guide.md          # Generic test plan guide (fallback)
└── scripts/
    ├── jira.py                 # Jira API helper (get-issue, add-comment, transition)
    └── bitbucket.py            # Bitbucket API helper (create-pr, get-pr, list-prs)

# Project-specific docs (live in your project repo — override the generic defaults)
docs/360-ticket-resolver/
├── code-review-checklist.md    # Project-specific review checks (loaded on top of generic)
└── test-plan-guide.md          # Project-specific test guidance (loaded on top of generic)
```

The skill always loads the generic defaults from `.claude/skills/360-ticket-resolver/`. If the project docs exist under `docs/360-ticket-resolver/`, they are loaded in addition and their rules take precedence where there is overlap.

---

## Troubleshooting

| Error | Fix |
|---|---|
| `JIRA_API_TOKEN not set` | Add `export JIRA_API_TOKEN="..."` to `~/.zshrc` and run `source ~/.zshrc` |
| `BITBUCKET_API_TOKEN not set` | Add `export BITBUCKET_API_TOKEN="..."` to `~/.zshrc` and run `source ~/.zshrc` |
| `HTTP 401` on Jira | Token wrong or expired — recreate a Classic API token at `id.atlassian.com/manage-profile/security/api-tokens` (click Create then copy immediately, no product/scope selection needed) |
| `HTTP 401` on Bitbucket | Token wrong, expired, or missing Bitbucket scopes — recreate with `repository:read`, `pullrequest:read`, `pullrequest:write` |
| `HTTP 404` on Jira ticket | Wrong ticket ID — check the project key and number |
| `HTTP 404` on Bitbucket | Wrong workspace in `config.yml`, or repo slug detected from git remote doesn't match Bitbucket |
| `Could not detect repo slug` | Run the script from inside the project directory, or check that `git remote get-url origin` returns a valid Bitbucket URL |
| `Branch not found on remote` | Typo in branch name, or the branch hasn't been pushed yet |

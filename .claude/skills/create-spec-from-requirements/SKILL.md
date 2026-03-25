---
name: create-spec-from-requirements
description: "Creates comprehensive specifications from requirements by coordinating system-architect and cto-reviewer agents. Restates requirements completely, identifies gaps, applies architectural expertise to design decisions, creates acceptance test plans upfront, and requires CTO certification before completion. Never blindly follows requirements - always applies expert judgment."
---

# Skill: Create Specification from Requirements

## Purpose

This skill transforms raw requirements into a comprehensive, production-ready specification document by orchestrating critical agents in sequence:

1. **system-architect**: Creates the specification with deep technical expertise
2. **ui-ux-fullstack-savant** (for UI projects): Designs user journeys and creates visual mockups
3. **cto-reviewer**: Meticulously validates the specification for gaps and issues

**CRITICAL PRINCIPLE**: We never blindly implement what requirements say. The system-architect applies expert judgment to design the *best* solution that satisfies the *intent* of the requirements. Requirements are inputs, not mandates.

**UI PROJECT PRINCIPLE**: For projects with user-facing components, we visualize before we build. ASCII mockups, user journey maps, and interaction flows help stakeholders "see" the system before implementation begins.

## Core Philosophy

```
REQUIREMENTS ≠ DESIGN

Requirements tell us WHAT problem to solve.
The system-architect decides HOW to solve it.
The cto-reviewer ensures we didn't miss anything.
```

## Input Requirements

The skill requires:

1. **Requirements Document**: One of:
   - Requirements file path (e.g., `/path/to/requirements.md`)
   - Inline requirements in the request
   - Reference to external requirements (Confluence, Jira epic, etc.)

2. **Output Location**: Where to create the specification (e.g., `/path/to/spec/`)

3. **Context** (optional but valuable):
   - Existing system architecture
   - Related specifications
   - Technical constraints
   - Non-functional requirements

## Output Artifacts

The skill produces:

```
output-location/
├── specification.md           # Complete specification document
├── test-plan.md              # Acceptance test plan (created FIRST)
├── requirements-analysis.md   # Gap analysis and clarifications
└── cto-review-report.md      # CTO reviewer's certification
```

## Workflow Overview

```
                    ┌─────────────────────────────────────┐
                    │         INPUT REQUIREMENTS          │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
              ┌───────────────────────────────────────────────┐
              │          PHASE 1: REQUIREMENTS ANALYSIS       │
              │                  (system-architect)           │
              │                                               │
              │  • Restate requirements completely            │
              │  • Identify gaps and ambiguities              │
              │  • Extract design hints vs hard constraints   │
              │  • Propose clarifications needed              │
              │  • Detect if UI/UX components present         │
              └─────────────────────┬─────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │ GAPS REQUIRING CLARIFICATION? │
                    └───────────────┬───────────────┘
                                    │
                          ┌─────────┴─────────┐
                          │                   │
                         YES                 NO
                          │                   │
                          ▼                   │
              ┌─────────────────────┐         │
              │ PAUSE: Ask User to  │         │
              │ Clarify Critical    │         │
              │ Gaps                │         │
              └─────────┬───────────┘         │
                        │                     │
                        └─────────┬───────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │    UI COMPONENTS FOUND?   │
                    └─────────────┬─────────────┘
                          ┌───────┴───────┐
                          │               │
                         YES             NO
                          │               │
                          ▼               │
              ┌───────────────────────────────────────────────┐
              │       PHASE 1.5: UI/UX DESIGN (Conditional)   │
              │              (ui-ux-fullstack-savant)         │
              │                                               │
              │  • Map user journeys and flows                │
              │  • Define information architecture            │
              │  • Create ASCII wireframes/mockups            │
              │  • Document UI states and interactions        │
              │  • Visualize the experience before building   │
              └─────────────────────┬─────────────────────────┘
                                    │
                                    └────────┬────────────────┘
                                             │
                                             ▼
              ┌───────────────────────────────────────────────┐
              │          PHASE 2: TEST PLAN CREATION          │
              │                  (system-architect)           │
              │                                               │
              │  • Define acceptance criteria FIRST           │
              │  • Create comprehensive test scenarios        │
              │  • Cover happy paths, edge cases, failures    │
              │  • Establish success metrics                  │
              │  • Include UI acceptance tests (if UI phase)  │
              └─────────────────────┬─────────────────────────┘
                                    │
                                    ▼
              ┌───────────────────────────────────────────────┐
              │        PHASE 3: SPECIFICATION DESIGN          │
              │                  (system-architect)           │
              │                                               │
              │  • Apply architectural expertise              │
              │  • Design optimal solution (not just what     │
              │    requirements say, but what's BEST)         │
              │  • Integrate UI/UX design (if applicable)     │
              │  • Document all design decisions              │
              │  • Create implementation tasks                │
              └─────────────────────┬─────────────────────────┘
                                    │
                                    ▼
              ┌───────────────────────────────────────────────┐
              │           PHASE 4: CTO REVIEW                 │
              │                  (cto-reviewer)               │
              │                                               │
              │  • Meticulous gap analysis                    │
              │  • Challenge design decisions                 │
              │  • Validate test plan completeness            │
              │  • Review UI/UX design (if applicable)        │
              │  • Identify implementation risks              │
              │  • Certify or reject                          │
              └─────────────────────┬─────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │         CERTIFICATION?        │
                    └───────────────┬───────────────┘
                          ┌─────────┴─────────┐
                          │                   │
                       APPROVED            REJECTED
                          │                   │
                          ▼                   ▼
              ┌─────────────────────┐  ┌─────────────────────┐
              │ CTO Solemn Oath     │  │ Issues List         │
              │ <promise>DONE       │  │ Route back to       │
              │ </promise>          │  │ system-architect    │
              └─────────────────────┘  └──────────┬──────────┘
                                                  │
                                                  └──► (iterate)
```

---

## Phase 1: Requirements Analysis

**Agent**: `system-architect`

### Objective

Completely analyze and restate the requirements, identifying gaps before any design work begins.

### Process

#### 1.1 Complete Requirements Restatement

Read the input requirements and produce a complete, unambiguous restatement. This is NOT a summary - it must capture EVERY requirement, explicit and implicit.

**Format:**

```markdown
# Requirements Analysis

## Restated Requirements

### Functional Requirements

#### FR-001: [Requirement Name]
**Original Text:** "[exact quote from requirements]"
**Interpretation:** [Clear, unambiguous restatement]
**Category:** [Core | Secondary | Optional]
**Testable:** [Yes/No - if No, needs clarification]

#### FR-002: [Requirement Name]
...

### Non-Functional Requirements

#### NFR-001: [Requirement Name]
**Original Text:** "[exact quote or implied from context]"
**Interpretation:** [Clear, unambiguous restatement]
**Measurement:** [How this will be measured/verified]
...

### Constraints

#### CON-001: [Constraint Name]
**Source:** [Requirements | Technical | Business | Regulatory]
**Description:** [What is constrained and why]
...
```

#### 1.2 Gap Identification

Identify what's MISSING from the requirements:

```markdown
## Gap Analysis

### Critical Gaps (MUST be resolved before specification)

#### GAP-001: [Gap Name]
**Category:** [Missing Requirement | Ambiguous Requirement | Conflicting Requirements]
**Impact:** [What cannot be designed without this]
**Suggested Resolution:** [How to resolve]
**Question for Stakeholder:** "[Specific question to ask]"

### Important Gaps (SHOULD be resolved, can make assumptions)

#### GAP-002: [Gap Name]
**Category:** [...]
**Default Assumption:** [What we'll assume if not clarified]
**Risk of Assumption:** [What could go wrong]

### Minor Gaps (Nice to clarify, reasonable defaults exist)

#### GAP-003: [Gap Name]
...
```

#### 1.3 Design Hints vs Hard Constraints

**CRITICAL**: Requirements often contain "design hints" disguised as requirements. The system-architect MUST distinguish:

```markdown
## Design Analysis

### Hard Constraints (MUST follow)
These are non-negotiable technical or business constraints:

| ID | Constraint | Rationale | Cannot Change Because |
|----|------------|-----------|----------------------|
| HC-001 | Must use PostgreSQL | Corporate standard | Compliance requirement |
| HC-002 | Max latency 100ms | SLA commitment | Customer contract |

### Design Hints (Consider but evaluate)
These appear in requirements but are actually suggestions we should evaluate:

| ID | Hint from Requirements | Our Assessment | Recommendation |
|----|----------------------|----------------|----------------|
| DH-001 | "Use microservices" | May be overkill for scope | Evaluate monolith-first |
| DH-002 | "Cache with Redis" | Good suggestion | Adopt, but consider alternatives |

### Requirements to Challenge
These requirements may not serve the actual goal:

| ID | Requirement | Concern | Alternative Proposal |
|----|-------------|---------|---------------------|
| RC-001 | "Real-time sync every 1s" | Battery drain on mobile | Propose adaptive sync |
```

### Output

Create `requirements-analysis.md` with all of the above.

### Decision Point

**If CRITICAL GAPS exist:**
```
PAUSE: Cannot proceed to specification. Present gaps to user and request clarification.

Critical gaps that must be resolved:
1. [GAP-001]: [Question]
2. [GAP-002]: [Question]

Please provide answers before we can create a complete specification.
```

**If no CRITICAL GAPS:**
```
Proceeding with specification. Making the following assumptions for Important Gaps:
- GAP-002: Assuming [assumption]
- GAP-003: Assuming [assumption]

These can be revised if stakeholder provides different direction.
```

---

## Phase 1.5: UI/UX Design (Conditional)

**Agent**: `ui-ux-fullstack-savant`
**Condition**: Invoke this phase when the project has **user-facing components** (web UI, mobile app, CLI with interactive elements, dashboards, etc.)

### Objective

For UI projects, visualize the user experience before diving into technical specification. This phase creates tangible artifacts that help stakeholders "see" what we're building.

### Detection Criteria

Invoke this phase if requirements mention ANY of:
- Web application, dashboard, portal, admin panel
- User interface, screens, pages, views, forms
- User interaction, clicks, navigation, workflows
- Frontend, Angular, React, Vue, or similar
- Mobile app, responsive design
- Reports, visualizations, charts, data display
- User onboarding, wizards, step-by-step flows

### Process

#### 1.5.1 User Journey Mapping

Identify and document the primary user journeys:

```markdown
## User Journeys

### Journey 1: [Primary User Goal]
**Actor:** [User role]
**Goal:** [What they want to accomplish]
**Trigger:** [What initiates this journey]

**Flow:**
1. User arrives at [entry point]
2. User sees [initial state/information]
3. User takes action [action description]
4. System responds with [feedback/result]
5. User completes goal OR encounters [branching scenarios]

**Success Criteria:** [How we know the journey succeeded]
**Pain Points to Avoid:** [Common UX mistakes for this type of flow]
```

#### 1.5.2 Information Architecture

Define the structure of information and navigation:

```markdown
## Information Architecture

### Site/App Structure
```
┌─────────────────────────────────────────────────────────┐
│                    [App Name]                           │
├─────────────────────────────────────────────────────────┤
│  ├── Dashboard (landing)                                │
│  │   ├── Key Metrics Summary                           │
│  │   └── Quick Actions                                 │
│  ├── [Feature Area 1]                                  │
│  │   ├── List View                                     │
│  │   ├── Detail View                                   │
│  │   └── Create/Edit Form                              │
│  ├── [Feature Area 2]                                  │
│  │   └── ...                                           │
│  └── Settings                                          │
│      ├── Profile                                       │
│      └── Preferences                                   │
└─────────────────────────────────────────────────────────┘
```

### Navigation Patterns
- Primary Navigation: [Tab bar / Sidebar / Top nav]
- Secondary Navigation: [Breadcrumbs / Back buttons / Context menus]
- Quick Actions: [FAB / Command palette / Shortcuts]
```

#### 1.5.3 ASCII/Text Wireframes

Create visual mockups for key screens. ASCII art is preferred for version control and universal readability:

```markdown
## Wireframes

### Screen: [Screen Name]
**Purpose:** [What this screen accomplishes]
**Entry Points:** [How users get here]

```
┌────────────────────────────────────────────────────────────────┐
│  [Logo]    Dashboard    Reports    Settings         [User ▼]  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐│
│  │   Metric A      │  │   Metric B      │  │   Metric C      ││
│  │   ████████ 84%  │  │   ████░░░░ 42%  │  │   ██████░░ 67%  ││
│  └─────────────────┘  └─────────────────┘  └─────────────────┘│
│                                                                │
│  Recent Activity                              [+ New Report]   │
│  ┌────────────────────────────────────────────────────────────┐│
│  │  ☑ Report #123 - Completed - 2 hours ago      [View]      ││
│  │  ◐ Report #122 - Processing - 45% complete    [Cancel]    ││
│  │  ☐ Report #121 - Queued                       [Edit]      ││
│  └────────────────────────────────────────────────────────────┘│
│                                                                │
│  [< Prev]                                         [Next >]     │
└────────────────────────────────────────────────────────────────┘
```

**Interactions:**
- Click metric card → Drill down to detailed view
- Click [+ New Report] → Opens report creation wizard
- Click row → Expands inline detail OR navigates to detail page
```

#### 1.5.4 State Documentation

Document all UI states for key components:

```markdown
## UI States

### Component: [Component Name]

| State | Visual | Behavior |
|-------|--------|----------|
| Empty | "No items yet" message + CTA | Show helpful prompt to add first item |
| Loading | Skeleton/shimmer animation | Disable interactions, show progress |
| Error | Error message + retry action | Explain what went wrong, offer recovery |
| Partial | Some data loaded | Progressive rendering, load more on scroll |
| Success | Populated with data | Full interactivity enabled |
| Overflow | Many items | Pagination/virtualization, search/filter |
```

#### 1.5.5 Interaction Patterns

Document key interaction patterns and micro-interactions:

```markdown
## Interaction Patterns

### Pattern: [Pattern Name]
**Use Case:** [When to use this pattern]

**Behavior:**
1. User initiates [action]
2. UI responds with [immediate feedback]
3. System processes [operation]
4. UI updates to show [result/confirmation]

**Edge Cases:**
- If operation fails: [error handling]
- If operation is slow: [loading state]
- If user interrupts: [cancellation behavior]

**Accessibility:**
- Keyboard: [How to accomplish via keyboard]
- Screen reader: [Announcements and labels]
```

### Output

Create a `ui-ux-design.md` document with all of the above, OR integrate directly into the main specification under a "User Experience" section.

### Integration with System Architecture

The ui-ux-fullstack-savant's output directly informs:
- **system-architect**: API design should support the UI's data needs
- **test-plan**: Acceptance criteria should reference specific UI states and flows
- **specification**: Component structure follows the wireframe hierarchy

---

## Phase 2: Test Plan Creation

**Agent**: `system-architect`

### Objective

Create the acceptance test plan BEFORE designing the solution. This ensures we are acceptance-minded from the start.

### Philosophy

```
TEST PLAN FIRST = Clarity of Purpose

If you can't write a test for it, you don't understand it.
If you don't have tests defined upfront, you'll miss edge cases.
Acceptance criteria drive the design, not the other way around.
```

### Process

#### 2.1 Acceptance Test Structure

```markdown
# Test Plan: [Specification Name]

**Created:** [Date]
**Requirements Source:** [Link to requirements-analysis.md]
**Status:** DRAFT - Awaiting CTO Review

## Test Strategy

### Scope
- **In Scope:** [What this test plan covers]
- **Out of Scope:** [What's tested elsewhere or not tested]

### Test Categories
1. **Functional Tests**: Verify business logic and features
2. **Integration Tests**: Verify component interactions
3. **Non-Functional Tests**: Performance, security, reliability
4. **Edge Case Tests**: Boundary conditions and unusual inputs
5. **Failure Mode Tests**: How system behaves when things go wrong

---

## Acceptance Criteria by Requirement

### FR-001: [Requirement Name]

#### AC-001-1: [Acceptance Criterion]
**Given:** [Precondition]
**When:** [Action]
**Then:** [Expected Result]
**Priority:** [Must Pass | Should Pass | Nice to Pass]

#### AC-001-2: [Acceptance Criterion]
...

### FR-002: [Requirement Name]
...

---

## Integration Test Scenarios

### ITS-001: [Scenario Name]
**Components Involved:** [List of components]
**Preconditions:** [System state required]
**Steps:**
1. [Step 1]
2. [Step 2]
**Expected Outcome:** [What should happen]
**Failure Modes to Test:**
- [ ] [What if component A fails?]
- [ ] [What if network times out?]

---

## Non-Functional Test Criteria

### Performance

| Metric | Target | Test Method |
|--------|--------|-------------|
| Response time (p95) | < 200ms | Load test with 1000 concurrent users |
| Throughput | > 1000 req/s | Sustained load for 1 hour |

### Security

| Test | Pass Criteria | Method |
|------|---------------|--------|
| Authentication bypass | No unauthorized access | Penetration testing |
| SQL Injection | All inputs sanitized | Automated scanning |

### Reliability

| Scenario | Expected Behavior | Recovery Time |
|----------|-------------------|---------------|
| Database failover | Automatic failover, no data loss | < 30s |
| Service crash | Auto-restart, state recovery | < 10s |

---

## Edge Cases and Boundary Conditions

### EC-001: [Edge Case Name]
**Condition:** [What unusual condition]
**Expected Behavior:** [How system should handle it]
**Why Important:** [What could go wrong if not handled]

### EC-002: Empty/Null Inputs
...

### EC-003: Maximum Load
...

### EC-004: Concurrent Modifications
...

---

## Failure Mode Tests

### FM-001: [Failure Scenario]
**Trigger:** [How to simulate this failure]
**Expected Behavior:** [System response]
**Recovery:** [How system recovers]
**Data Integrity:** [What data guarantees must hold]

---

## Test Coverage Matrix

| Requirement | Unit Tests | Integration Tests | E2E Tests | Manual Tests |
|-------------|------------|-------------------|-----------|--------------|
| FR-001 | AC-001-1, AC-001-2 | ITS-001 | E2E-001 | - |
| FR-002 | AC-002-1 | ITS-002, ITS-003 | - | MT-001 |
| NFR-001 | - | - | Perf-001 | - |

---

## Success Metrics

The specification implementation is considered COMPLETE when:

- [ ] All "Must Pass" acceptance criteria pass
- [ ] All "Should Pass" criteria pass (or documented exceptions approved)
- [ ] All integration test scenarios pass
- [ ] Non-functional targets met (or approved variances documented)
- [ ] All critical edge cases handled
- [ ] All failure modes tested and recovery verified
```

### Output

Create `test-plan.md` with comprehensive acceptance criteria.

---

## Phase 3: Specification Design

**Agent**: `system-architect`

### Objective

Design the optimal technical solution, applying architectural expertise. Do NOT simply implement what requirements say - design what's BEST.

### Design Principles

```
1. REQUIREMENTS ARE CONSTRAINTS, NOT DESIGNS
   - They tell us what problem to solve
   - They don't tell us the optimal solution

2. CHALLENGE ASSUMPTIONS
   - Question design hints in requirements
   - Consider alternatives before committing

3. SIMPLICITY OVER COMPLEXITY
   - Prefer simpler solutions that meet requirements
   - Avoid over-engineering for hypothetical futures

4. TESTABILITY DRIVES DESIGN
   - If it can't be tested, reconsider the design
   - Test plan informs component boundaries

5. DOCUMENT DECISIONS
   - Every significant decision needs rationale
   - Capture what was NOT chosen and why
```

### Specification Structure

```markdown
# Specification: [Project Name]

**Version:** 1.0
**Status:** DRAFT - Awaiting CTO Review
**Author:** system-architect
**Date:** [Date]

**Related Documents:**
- [Requirements Analysis](./requirements-analysis.md)
- [Test Plan](./test-plan.md)

---

## Executive Summary

[2-3 paragraph overview of what this specification delivers, key design decisions, and expected outcomes]

---

## 1. Objectives and Success Criteria

### 1.1 Primary Objectives
[What this system must accomplish - derived from requirements but stated in terms of outcomes]

### 1.2 Success Criteria
[Measurable criteria - reference test plan for specifics]

### 1.3 Non-Goals
[Explicitly what this specification does NOT address]

---

## 2. System Architecture

### 2.1 High-Level Architecture
[Architecture diagram - ASCII or description]

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   Service   │────▶│  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 2.2 Component Overview

| Component | Responsibility | Technology | Rationale |
|-----------|---------------|------------|-----------|
| [Component A] | [What it does] | [Tech choice] | [Why this tech] |

### 2.3 Key Design Decisions

#### Decision 1: [Decision Name]
**Context:** [What problem were we solving]
**Options Considered:**
1. [Option A]: [Pros/Cons]
2. [Option B]: [Pros/Cons]
3. [Option C]: [Pros/Cons]

**Decision:** [What we chose]
**Rationale:** [Why this is the best choice]
**Consequences:** [What this decision implies]

#### Decision 2: [Decision Name]
...

---

## 3. Detailed Design

### 3.1 [Component A]

#### 3.1.1 Purpose
[What this component does and why it exists]

#### 3.1.2 Interface
[API contracts, method signatures, data formats]

#### 3.1.3 Behavior
[How it works, state transitions, algorithms]

#### 3.1.4 Dependencies
[What it depends on, what depends on it]

#### 3.1.5 Error Handling
[How errors are handled, propagated, recovered]

### 3.2 [Component B]
...

---

## 4. Data Model

### 4.1 Entity Definitions
[Data structures, schemas, relationships]

### 4.2 Data Flow
[How data moves through the system]

### 4.3 Data Integrity
[Validation rules, constraints, invariants]

---

## 5. API Specifications

### 5.1 [API Endpoint/Method]
**Purpose:** [What it does]
**Request:** [Format, required fields, validation]
**Response:** [Format, status codes, error responses]
**Example:**
```json
// Request
{ ... }
// Response
{ ... }
```

---

## 6. Security Considerations

### 6.1 Authentication
[How users/systems are authenticated]

### 6.2 Authorization
[How permissions are enforced]

### 6.3 Data Protection
[Encryption, PII handling, audit logging]

### 6.4 Threat Mitigation
[Known threats and how they're addressed]

---

## 7. Operational Considerations

### 7.1 Deployment
[How the system is deployed]

### 7.2 Configuration
[Configurable parameters, environment variables]

### 7.3 Monitoring
[What metrics, logs, alerts]

### 7.4 Scaling
[How the system scales, bottlenecks, limits]

---

## 8. Implementation Plan

### 8.1 Implementation Phases

#### Phase 1: [Phase Name]
**Objective:** [What this phase delivers]
**Tasks:**
- [ ] TASK-001: [Task description]
- [ ] TASK-002: [Task description]
**Dependencies:** [Prerequisites]
**Acceptance Criteria:** [Reference to test plan sections]

#### Phase 2: [Phase Name]
...

### 8.2 Task Breakdown

| Task ID | Description | Component | Complexity | Dependencies |
|---------|-------------|-----------|------------|--------------|
| TASK-001 | [Description] | [Component] | [S/M/L/XL] | None |
| TASK-002 | [Description] | [Component] | [M] | TASK-001 |

### 8.3 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk description] | [H/M/L] | [H/M/L] | [How to mitigate] |

---

## 9. Open Questions

[Any remaining questions that need resolution during implementation]

| Question | Impact | Owner | Due |
|----------|--------|-------|-----|
| [Question] | [What's blocked] | [Who decides] | [When needed] |

---

## Appendices

### A. Glossary
[Definition of terms]

### B. References
[External documentation, standards, related specs]

### C. Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | system-architect | Initial specification |
```

### Output

Create `specification.md` with the complete technical specification.

---

## Phase 4: CTO Review

**Agent**: `cto-reviewer`

### Objective

Meticulous, comprehensive review of the specification to identify gaps, issues, and risks before implementation investment.

### Review Philosophy

```
THE CTO REVIEWER'S MANDATE:

1. ASSUME NOTHING IS PERFECT
   - Every specification has gaps
   - Find them before implementation does

2. CHALLENGE EVERYTHING
   - Why this design decision?
   - What alternatives were considered?
   - Is this the simplest solution?

3. VALIDATE COMPLETENESS
   - Every requirement addressed?
   - Every acceptance criterion testable?
   - Every edge case considered?

4. PROTECT THE TEAM
   - Find issues now, not during implementation
   - Prevent wasted effort on flawed designs

5. PROVIDE CERTIFICATION
   - Only approve exceptional specifications
   - Solemn oath means personal accountability
```

### Review Checklist

```markdown
# CTO Review Report

**Specification:** [Name]
**Reviewer:** cto-reviewer
**Review Date:** [Date]
**Status:** [PENDING | APPROVED | REJECTED]

---

## 1. Requirements Coverage

### 1.1 Requirement Traceability

| Requirement | Specification Section | Test Coverage | Status |
|-------------|----------------------|---------------|--------|
| FR-001 | Section 3.1 | AC-001-1, AC-001-2 | [COVERED | PARTIAL | MISSING] |
| FR-002 | Section 3.2 | AC-002-1 | [COVERED | PARTIAL | MISSING] |

### 1.2 Missing Requirements
[List any requirements not addressed in specification]

### 1.3 Requirements Assessment
- [ ] All functional requirements addressed
- [ ] All non-functional requirements addressed
- [ ] All constraints respected
- [ ] No requirement over-interpretation

**Finding:** [Assessment]

---

## 2. Design Quality

### 2.1 Architecture Assessment
- [ ] Architecture appropriate for requirements
- [ ] Component responsibilities clear and well-separated
- [ ] No unnecessary complexity
- [ ] Scalability considerations addressed
- [ ] Failure modes considered

**Finding:** [Assessment]

### 2.2 Design Decisions Review

| Decision | Assessment | Concerns |
|----------|------------|----------|
| [Decision 1] | [SOUND | QUESTIONABLE | FLAWED] | [Concerns if any] |
| [Decision 2] | ... | ... |

### 2.3 Alternative Designs Considered?
- [ ] Alternatives documented
- [ ] Trade-offs clearly explained
- [ ] Best option justified

**Finding:** [Assessment]

---

## 3. Test Plan Completeness

### 3.1 Coverage Analysis
- [ ] All requirements have acceptance criteria
- [ ] Happy paths tested
- [ ] Edge cases identified and tested
- [ ] Failure modes tested
- [ ] Non-functional requirements tested

### 3.2 Test Quality
- [ ] Acceptance criteria are specific and measurable
- [ ] Test scenarios are realistic
- [ ] Pass/fail criteria are clear

### 3.3 Gaps in Test Coverage
[List any areas not adequately covered by tests]

**Finding:** [Assessment]

---

## 4. Security Review

- [ ] Authentication mechanism appropriate
- [ ] Authorization properly enforced
- [ ] Data protection adequate
- [ ] Input validation comprehensive
- [ ] Known threat vectors addressed
- [ ] No obvious vulnerabilities

**Finding:** [Assessment]

---

## 5. Operational Readiness

- [ ] Deployment process defined
- [ ] Configuration management addressed
- [ ] Monitoring and alerting defined
- [ ] Scaling strategy appropriate
- [ ] Disaster recovery considered

**Finding:** [Assessment]

---

## 6. Implementation Plan Review

### 6.1 Task Completeness
- [ ] All specification sections have corresponding tasks
- [ ] Task dependencies are correct
- [ ] No circular dependencies
- [ ] Complexity estimates reasonable

### 6.2 Risk Assessment
- [ ] Risks identified comprehensively
- [ ] Mitigations are actionable
- [ ] No unaddressed high-impact risks

**Finding:** [Assessment]

---

## 7. Issues Summary

### Critical Issues (MUST FIX - Blocks Approval)

| ID | Issue | Section | Required Action |
|----|-------|---------|-----------------|
| CRIT-001 | [Issue description] | [Section] | [What must be fixed] |

### Major Issues (SHOULD FIX - Strong Recommendation)

| ID | Issue | Section | Recommendation |
|----|-------|---------|----------------|
| MAJ-001 | [Issue description] | [Section] | [What should be fixed] |

### Minor Issues (NICE TO FIX - Suggestions)

| ID | Issue | Section | Suggestion |
|----|-------|---------|------------|
| MIN-001 | [Issue description] | [Section] | [Suggestion] |

---

## 8. Decision

### If APPROVED:

---

**CERTIFICATION**

I, the CTO Reviewer, have conducted a meticulous and comprehensive review of this specification. I have:

- Verified all requirements are addressed
- Validated all design decisions are sound
- Confirmed the test plan is comprehensive
- Reviewed security considerations
- Assessed operational readiness
- Examined the implementation plan

**I solemnly swear that this specification is exceptional in its completeness, correctness, and readiness for implementation. The design reflects expert judgment, not blind adherence to requirements. The test plan ensures acceptance-minded development from the start.**

**All gaps have been identified and addressed. The team can proceed with confidence.**

<promise>SPECIFICATION_APPROVED</promise>

---

### If REJECTED:

---

**REJECTION**

This specification cannot be approved due to the following critical issues:

[List of CRIT-* issues]

**Required Actions:**
1. [Action 1]
2. [Action 2]

Return to system-architect for revision. Re-submit for review when issues are addressed.

**Status:** REJECTED - Requires Revision

---
```

### Output

Create `cto-review-report.md` with the complete review.

---

## Iteration Protocol

When CTO Review identifies issues:

### For CRITICAL Issues
```
[cto-reviewer] SPECIFICATION REJECTED

Critical issues found:
- CRIT-001: [Issue]
- CRIT-002: [Issue]

Routing back to system-architect for revision...

[system-architect] Addressing critical issues:
- CRIT-001: [How being fixed]
- CRIT-002: [How being fixed]

Updating specification...
Updating test plan (if affected)...

Re-submitting for CTO review...
```

### For MAJOR Issues
```
[cto-reviewer] SPECIFICATION APPROVED WITH RECOMMENDATIONS

The specification is approved, but the following should be addressed:
- MAJ-001: [Issue and recommendation]

<promise>SPECIFICATION_APPROVED</promise>

Note: Major issues should be tracked for implementation phase.
```

---

## Console Output Format

```
╔════════════════════════════════════════════════════════════════╗
║        CREATE SPECIFICATION FROM REQUIREMENTS                  ║
╚════════════════════════════════════════════════════════════════╝

📋 Input Requirements: /path/to/requirements.md
📁 Output Location: /path/to/spec/

════════════════════════════════════════════════════════════════

PHASE 1: REQUIREMENTS ANALYSIS
Agent: system-architect

────────────────────────────────────────────────────────────────

[system-architect] Analyzing requirements...
[system-architect] Restating 12 functional requirements...
[system-architect] Restating 5 non-functional requirements...
[system-architect] Identifying 3 constraints...

[system-architect] Gap Analysis Complete:
  - 0 Critical Gaps (can proceed)
  - 2 Important Gaps (assumptions documented)
  - 3 Minor Gaps (reasonable defaults applied)

[system-architect] Design Analysis:
  - 2 Hard Constraints identified
  - 3 Design Hints (will evaluate alternatives)
  - 1 Requirement to Challenge (will propose alternative)
  - UI Components Detected: YES (dashboard, reports, user management)

[system-architect] Created: requirements-analysis.md

════════════════════════════════════════════════════════════════

PHASE 1.5: UI/UX DESIGN (Conditional)
Agent: ui-ux-fullstack-savant

────────────────────────────────────────────────────────────────

[ui-ux-fullstack-savant] UI components detected - creating visual design...
[ui-ux-fullstack-savant] Mapping 3 primary user journeys:
  - Report Creation Flow
  - Dashboard Monitoring
  - Settings Configuration

[ui-ux-fullstack-savant] Defining information architecture...
[ui-ux-fullstack-savant] Creating ASCII wireframes for 5 key screens:
  - Dashboard (landing)
  - Report List View
  - Report Detail / Edit
  - Generation Progress
  - Settings Panel

[ui-ux-fullstack-savant] Documenting UI states:
  - Empty, Loading, Error, Success, Overflow states defined
  - Interaction patterns documented
  - Accessibility considerations noted

[ui-ux-fullstack-savant] Created: ui-ux-design.md (or integrated into specification)

════════════════════════════════════════════════════════════════

PHASE 2: TEST PLAN CREATION
Agent: system-architect

────────────────────────────────────────────────────────────────

[system-architect] Creating acceptance criteria FIRST...
[system-architect] Test coverage:
  - 24 Acceptance Criteria defined
  - 8 Integration Test Scenarios
  - 5 Performance Test Targets
  - 12 Edge Cases
  - 6 Failure Mode Tests

[system-architect] Created: test-plan.md

════════════════════════════════════════════════════════════════

PHASE 3: SPECIFICATION DESIGN
Agent: system-architect

────────────────────────────────────────────────────────────────

[system-architect] Designing system architecture...
[system-architect] Key design decisions:
  - Decision 1: Chose Option B over A (simpler, meets requirements)
  - Decision 2: Challenged requirement "use microservices" - recommending modular monolith
  - Decision 3: Added caching layer not in requirements (performance optimization)

[system-architect] Creating detailed component designs...
[system-architect] Defining data model...
[system-architect] Specifying APIs...
[system-architect] Documenting security considerations...
[system-architect] Creating implementation plan:
  - 3 Phases
  - 18 Tasks
  - 4 Identified Risks with Mitigations

[system-architect] Created: specification.md

════════════════════════════════════════════════════════════════

PHASE 4: CTO REVIEW
Agent: cto-reviewer

────────────────────────────────────────────────────────────────

[cto-reviewer] Beginning meticulous review...

[cto-reviewer] Requirements Coverage:
  ✓ All 12 functional requirements addressed
  ✓ All 5 non-functional requirements addressed
  ✓ All 3 constraints respected

[cto-reviewer] Design Quality:
  ✓ Architecture appropriate and well-justified
  ✓ All 3 design decisions are sound
  ✓ Alternatives properly documented

[cto-reviewer] Test Plan Completeness:
  ✓ All requirements have acceptance criteria
  ✓ Edge cases comprehensive
  ✓ Failure modes covered

[cto-reviewer] Security Review:
  ✓ No obvious vulnerabilities
  ✓ Authentication/authorization adequate

[cto-reviewer] Implementation Plan:
  ✓ Tasks complete and well-sequenced
  ✓ Risks identified with mitigations

[cto-reviewer] Issues Found:
  - 0 Critical Issues
  - 1 Major Issue (documented as recommendation)
  - 2 Minor Issues (suggestions)

════════════════════════════════════════════════════════════════

[cto-reviewer]

╔════════════════════════════════════════════════════════════════╗
║                    SPECIFICATION APPROVED                      ║
╚════════════════════════════════════════════════════════════════╝

"I solemnly swear that this specification is exceptional in its
completeness, correctness, and readiness for implementation.
The design reflects expert judgment, not blind adherence to
requirements. The test plan ensures acceptance-minded development
from the start."

<promise>SPECIFICATION_APPROVED</promise>

════════════════════════════════════════════════════════════════

Artifacts Created:
  ✓ requirements-analysis.md
  ✓ test-plan.md
  ✓ specification.md
  ✓ cto-review-report.md

The specification is ready for implementation.
```

---

## Invocation Examples

### Basic Usage
```
Create a specification from the requirements in /project/requirements.md.
Output to /project/spec/.
```

### With Context
```
Create a specification from the requirements below.
Output to /project/spec/.

Context:
- This is an extension to our existing authentication system
- Must integrate with our PostgreSQL database
- Performance is critical - p99 latency under 50ms

Requirements:
[paste requirements here]
```

### From External Source
```
Create a specification from the Jira epic PROJ-123.
Read the requirements from the linked Confluence page.
Output to /project/spec/.
```

---

## Quality Commitment

This skill guarantees:

1. **Complete Requirements Analysis**: Every requirement restated, no gaps unidentified
2. **Test-First Mindset**: Acceptance criteria defined before design
3. **Expert Design**: Architectural judgment applied, not blind implementation
4. **Meticulous Review**: CTO certification only for exceptional specifications
5. **No Corners Cut**: Iteration until quality standards met

**The CTO reviewer's solemn oath is not given lightly. It represents a commitment that the specification has been scrutinized with the rigor it deserves.**

---

## Failure Modes

### Cannot Proceed Without Clarification
```
BLOCKED: Critical gaps in requirements prevent specification.

The following must be clarified before proceeding:
1. [Question 1]
2. [Question 2]

Please provide answers to continue.
```

### Review Rejection
```
SPECIFICATION REJECTED BY CTO REVIEW

Critical issues prevent approval:
- [Issue 1]
- [Issue 2]

Returning to system-architect for revision...
```

### Iteration Limit
```
WARNING: Specification has been revised 3 times without CTO approval.

Consider:
1. Reviewing the requirements for fundamental issues
2. Escalating blocking concerns
3. Scheduling a design review meeting

Current blockers:
- [Blocker 1]
- [Blocker 2]
```

---

**Note**: This skill does not compromise on quality. If the requirements are unclear or the design has issues, it will iterate until excellence is achieved or explicitly communicate why it cannot proceed.

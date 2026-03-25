---
name: phase-breakdown
description: Partitions large specification documents into focused, modular documents organized by phases, features, or components. Use when you have large specs (>5000 words), multiple implementation phases, or need better documentation modularity.
---

# Skill: Specification Document Partitioning

## Purpose

This skill partitions large, monolithic specification documents into focused, modular documents organized by logical groupings (e.g., phases, features, components). Each resulting document should be self-contained enough for developers or stakeholders to work with that section without constantly cross-referencing the master document.

## When to Use This Skill

Use this skill when you have:
- A large specification document (>5000 words) that's difficult to navigate
- Multiple implementation phases or stages that could be separate documents
- Different audiences needing different subsets of the specification
- Architecture, design, and implementation details mixed together
- A need for better modularity and maintainability in documentation

## Input Requirements

Before starting, you'll need:

1. **Source Document Location**: Path to the monolithic specification
2. **Output Directory**: Where partitioned documents should be created
3. **Partition Strategy**: How to break up the document (see strategies below)
4. **Document Template**: Desired structure for output documents (optional)

## Partition Strategies

Choose the strategy that best fits your specification:

### 1. Phase-Based Partitioning
Best for: Implementation roadmaps, project plans, iterative development specs

Structure:
```
docs/
├── README.md
├── original-spec.md (archived)
├── overview/
│   ├── architecture.md
│   ├── objectives.md
│   └── constraints.md
├── phases/
│   ├── phase-1-[name].md
│   ├── phase-2-[name].md
│   └── phase-N-[name].md
└── reference/
    ├── configuration.md
    ├── testing.md
    └── glossary.md
```

### 2. Component-Based Partitioning
Best for: System designs, microservices specs, modular architectures

Structure:
```
docs/
├── README.md
├── original-spec.md (archived)
├── system-overview.md
├── components/
│   ├── component-a.md
│   ├── component-b.md
│   └── component-c.md
├── interfaces/
│   ├── apis.md
│   ├── data-formats.md
│   └── protocols.md
└── operations/
    ├── deployment.md
    ├── monitoring.md
    └── maintenance.md
```

### 3. Feature-Based Partitioning
Best for: Product specs, feature documentation, requirement documents

Structure:
```
docs/
├── README.md
├── original-spec.md (archived)
├── product-vision.md
├── features/
│   ├── feature-1-[name].md
│   ├── feature-2-[name].md
│   └── feature-N-[name].md
├── architecture/
│   ├── technical-design.md
│   └── infrastructure.md
└── appendices/
    ├── user-stories.md
    ├── mockups.md
    └── research.md
```

### 4. Audience-Based Partitioning
Best for: Multi-stakeholder specs, documentation for different roles

Structure:
```
docs/
├── README.md
├── original-spec.md (archived)
├── executive-summary.md
├── for-developers/
│   ├── technical-architecture.md
│   ├── implementation-guide.md
│   └── api-reference.md
├── for-product/
│   ├── requirements.md
│   ├── user-flows.md
│   └── acceptance-criteria.md
└── for-operations/
    ├── deployment-guide.md
    ├── runbooks.md
    └── monitoring.md
```

## Standard Document Template

Each partitioned document should follow this structure (customize as needed):

```markdown
# [Document Title]

**Status:** [Draft/In Progress/Complete]
**Last Updated:** [Date]
**Parent Document:** [Link to original spec]
**Dependencies:** [List of prerequisite documents]

## Overview
Brief description of what this document covers and its purpose.

## Scope
- What's included in this document
- What's explicitly excluded (with links to where it's covered)

## [Main Content Sections]
[Content specific to this partition]

## Cross-References
- Related documents in this spec
- External dependencies or references

## Acceptance Criteria (if applicable)
How to verify the content/implementation described here is complete.

## Appendices (if needed)
Additional details, examples, or supporting information.
```

## Partitioning Process

### Step 1: Analyze Source Document

Read through and identify:
- Natural section boundaries
- Repeated themes or topics
- Implementation phases or stages
- Audience-specific content
- Reusable reference material
- Cross-cutting concerns (security, testing, etc.)

### Step 2: Design Document Structure

Create a document map showing:
- All output documents and their purposes
- Document hierarchy and relationships
- Content that appears in multiple places
- Navigation strategy

### Step 3: Extract Content

For each output document:

1. **Copy relevant sections** from source document
2. **Preserve all technical content** (don't summarize unless requested)
3. **Add document metadata** (status, dates, dependencies)
4. **Include appropriate context** so document is understandable standalone
5. **Add navigation aids** (table of contents, quick links)

### Step 4: Create Cross-References

Add bidirectional links:

**Forward references** (in parent/overview docs):
```markdown
This concept is implemented in [Phase 3: Implementation](./phases/phase-3-implementation.md).
```

**Backward references** (in child/detail docs):
```markdown
For the high-level architecture, see [System Overview](../system-overview.md).
```

**Sibling references** (between related docs):
```markdown
The API design for this feature is described in [API Reference](../reference/api-reference.md).
```

### Step 5: Create Navigation Document

The `README.md` should include:

```markdown
# [Specification Name]

## Document Map

### Overview Documents
- [System Overview](overview/system-overview.md) - High-level architecture
- [Objectives](overview/objectives.md) - Goals and success criteria

### Implementation Documents
- [Phase 1: Foundation](phases/phase-1-foundation.md)
- [Phase 2: Core Features](phases/phase-2-core-features.md)

### Reference Documents
- [Configuration Guide](reference/configuration.md)
- [Testing Strategy](reference/testing.md)

## Quick Start

New to this spec? Start here:
1. Read [System Overview](overview/system-overview.md)
2. Review [Phase 1](phases/phase-1-foundation.md)
3. Reference [Configuration Guide](reference/configuration.md) as needed

## Document Status

| Document | Status | Owner | Last Updated |
|----------|--------|-------|--------------|
| System Overview | Complete | [Name] | 2024-01-01 |
| Phase 1 | In Progress | [Name] | 2024-01-05 |

## How to Use This Documentation

[Guidance on navigation, updating, contributing]
```

### Step 6: Verify Completeness

Check that:
- [ ] All content from original document exists in exactly one output document (or intentionally in multiple with clear rationale)
- [ ] No orphaned sections or lost content
- [ ] All cross-references are valid (no broken links)
- [ ] Each document is understandable standalone
- [ ] Navigation document links to all partitioned documents
- [ ] Original document is marked as archived/deprecated
- [ ] Metadata is complete on all documents

## Content Handling Guidelines

### DO:
- **Preserve technical accuracy** - Don't paraphrase technical details
- **Maintain context** - Include enough background so document stands alone
- **Keep examples** - Code samples, diagrams, tables stay intact
- **Add metadata** - Dates, status, dependencies, ownership
- **Create clear hierarchy** - Use consistent heading levels
- **Link generously** - Cross-reference related content
- **Include TOC** - For documents over 2 pages

### DON'T:
- **Delete content** - Partition, don't remove (unless truly obsolete)
- **Change requirements** - Keep original intent intact
- **Break code examples** - Ensure code blocks remain functional
- **Create circular dependencies** - Document A depends on B depends on A
- **Duplicate without linking** - If content appears twice, explain why
- **Use ambiguous titles** - "Implementation" vs "Phase 2: User Authentication"

## Handling Special Cases

### Duplicate Content
If the same content is needed in multiple documents:

**Option 1: Reference Pattern**
- Keep master copy in one document
- Link from other documents: "For details, see [Topic](../path/to/document.md#section)"

**Option 2: Intentional Duplication**
- Duplicate only if documents are truly independent
- Add note: "Note: This content is duplicated in [Other Doc] for convenience"

### Cross-Cutting Concerns
For topics that affect multiple sections (security, logging, error handling):

**Option 1: Dedicated Document**
- Create `architecture/cross-cutting-concerns.md`
- Reference from phase/component documents

**Option 2: Per-Section Content**
- Include relevant security/logging details in each document
- Link to master security document for deep dive

### Configuration and Reference Data
For properties, constants, schemas that appear throughout:

**Option 1: Centralized Reference**
- Create `reference/configuration.md` with all settings
- Phase documents reference it: "See [Configuration](../reference/configuration.md#phase-2-settings)"

**Option 2: Hybrid Approach**
- Each phase document includes its configuration
- `reference/configuration.md` aggregates all for quick lookup

## Quality Checklist

Before considering the partition complete:

**Completeness**
- [ ] Every section from original is accounted for
- [ ] All diagrams, tables, and code examples preserved
- [ ] All task IDs, requirement IDs preserved (if applicable)

**Navigability**
- [ ] README provides clear entry points
- [ ] Each document has parent/sibling/child links
- [ ] Search-friendly titles and headings
- [ ] Table of contents in longer documents

**Standalone Quality**
- [ ] Each document understandable without reading others
- [ ] Sufficient context provided
- [ ] Technical terms defined or linked to glossary
- [ ] Prerequisites clearly stated

**Consistency**
- [ ] Consistent document structure
- [ ] Consistent metadata format
- [ ] Consistent heading hierarchy
- [ ] Consistent link format

**Maintainability**
- [ ] Original document archived, not deleted
- [ ] Update process documented
- [ ] Document owners identified
- [ ] Version control strategy noted

## Example Invocation

```
Partition the specification document at /docs/project-spec.md using a phase-based approach. Create 5 phase documents plus architecture and reference sections. Use the standard template and ensure all configuration details are in reference/configuration.md.
```

Or in conversation:
```
I have a large specification document that needs to be broken up into more manageable pieces. Can you help me partition it into phase-based documents? The spec is at [path] and I'd like the output in [path].
```

## Tips for Success

1. **Start with structure** - Design the document tree before extracting content
2. **Test navigation** - Verify a developer could follow just one document branch
3. **Preserve traceability** - Keep task/requirement IDs intact for tracking
4. **Document the partition** - README should explain the organization strategy
5. **Review original periodically** - Source doc may have useful structure cues
6. **Keep it DRY-ish** - Avoid duplication, but don't sacrifice clarity for DRY principle
7. **Use descriptive names** - "Phase 2: Authentication" not just "Phase 2"
8. **Plan for updates** - Structure should accommodate future additions

## Common Pitfalls to Avoid

- **Over-partitioning**: Creating so many documents that navigation becomes harder
- **Under-linking**: Not providing enough cross-references between related content
- **Context loss**: Partitions missing background needed to understand them
- **Broken continuity**: Reading documents in sequence feels disjointed
- **Orphaned content**: Sections that don't fit anywhere in new structure
- **Ambiguous ownership**: Unclear which document owns a particular topic

---

**Note**: This is a framework skill. Adapt the structure and process to fit your specific documentation needs.
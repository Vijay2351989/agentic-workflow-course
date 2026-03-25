---
name: update-docs
description: "Updates or creates end-user focused documentation in a module's docs directory based on specification materials, code changes, or guidance. Explains the 'why', provides usage examples, corrects outdated content, and maintains consistency with existing documentation style."
---

# Skill: Update Documentation

## Purpose

This skill produces or updates end-user focused documentation in the `docs` directory of the appropriate module (sub-project). For most krista-infra projects, the "end user" is a developer consuming the APIs and frameworks.

**Core Philosophy:**

```
DOCUMENTATION IS FOR USERS, NOT FOR ARCHIVES

Good documentation:
  - Explains WHY something exists and what problem it solves
  - Shows HOW to use it with practical, runnable examples
  - Guides developers from "I don't know this exists" to "I'm using it effectively"
  - Lives with the code, not in a separate wiki that rots

Bad documentation:
  - Restates what the code already says
  - Lacks examples
  - Uses jargon without explanation
  - Becomes outdated and misleading
```

## Input Types

The skill handles three types of input, each requiring a different analysis approach:

### Type 1: Project Directory (Specification Materials)

**Example:** `data-grid/docs-specs/test-support`

**Contains:**
- `README.md` or `specification.md` - Main specification document
- `phases/` - Implementation phase documents
- `reference/` - Supporting materials (glossary, architecture, configuration)
- `requirements-analysis.md` - Original requirements breakdown
- `test-plan.md` - Acceptance criteria and test scenarios

**Analysis Approach:**
1. Read the specification document thoroughly
2. Examine reference materials for terminology and architecture
3. Review implementation phase summaries for what was built
4. Identify the key user-facing features to document
5. Extract example code from test-plan or usage-examples if available

### Type 2: Reference Material (Specification or Code)

**Example:** `data-grid/docs-specs/monitoring-infinispan.md` or actual source files

**Analysis Approach:**
1. Read the reference material completely
2. Identify the module where documentation belongs
3. Determine what existing documentation needs updating
4. Extract key concepts, APIs, and configuration options
5. Create usage examples based on the specification or code

### Type 3: Guidance with Code Reference

**Example:** `data-grid/src/main/java/app/krista/infra/dataGrid/throttle/ThrottledRemoteCache.java`

**Analysis Approach:**
1. Read the referenced code and related files
2. Check recent Git history for related changes:
   ```bash
   git log --oneline -20 -- <path>
   git diff HEAD~10 -- <path>
   ```
3. Identify uncommitted documentation or related specs
4. Determine what functionality changed or was added
5. Locate existing docs that may need updates
6. Create or update documentation based on findings

## Workflow

```
                    ┌─────────────────────────────────────┐
                    │             INPUT                    │
                    │                                      │
                    │  • Spec directory                    │
                    │  • Reference material                │
                    │  • Code guidance                     │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
              ┌───────────────────────────────────────────────┐
              │          PHASE 1: DISCOVERY                   │
              │                                               │
              │  1. Identify input type                       │
              │  2. Read all source materials                 │
              │  3. Identify target module                    │
              │  4. Locate existing docs directory            │
              │  5. Read existing documentation               │
              │  6. Check recent git changes (if guidance)    │
              └─────────────────────┬─────────────────────────┘
                                    │
                                    ▼
              ┌───────────────────────────────────────────────┐
              │          PHASE 2: ANALYSIS                    │
              │                                               │
              │  1. Extract key features to document          │
              │  2. Identify "why" and benefits               │
              │  3. Gather configuration options              │
              │  4. Collect API surfaces and entry points     │
              │  5. Find or create usage examples             │
              │  6. Map to existing doc structure             │
              └─────────────────────┬─────────────────────────┘
                                    │
                                    ▼
              ┌───────────────────────────────────────────────┐
              │          PHASE 3: PLAN DOCUMENTATION          │
              │                                               │
              │  1. Determine docs to update vs create        │
              │  2. Identify outdated content to remove       │
              │  3. Plan new sections or files                │
              │  4. Design ASCII diagrams if needed           │
              │  5. Outline each document change              │
              └─────────────────────┬─────────────────────────┘
                                    │
                                    ▼
              ┌───────────────────────────────────────────────┐
              │          PHASE 4: WRITE DOCUMENTATION         │
              │                                               │
              │  1. Update existing markdown files            │
              │  2. Create new markdown files as needed       │
              │  3. Add ASCII flow charts for complex flows   │
              │  4. Ensure consistent style with existing     │
              │  5. Cross-reference specs for deep detail     │
              └─────────────────────┬─────────────────────────┘
                                    │
                                    ▼
              ┌───────────────────────────────────────────────┐
              │          PHASE 5: VALIDATION                  │
              │                                               │
              │  1. Review all changes for completeness       │
              │  2. Verify examples are correct and runnable  │
              │  3. Check cross-references are valid          │
              │  4. Ensure no code files were modified        │
              │  5. Confirm only docs/ directory touched      │
              └─────────────────────────────────────────────┘
```

## Output Requirements

### Location

Documentation MUST be written to the `docs/` directory of the appropriate module:

```
<module>/
├── src/
│   └── main/java/...
├── docs/                    # Documentation goes here
│   ├── ExistingDoc.md
│   ├── NewDoc.md           # New documentation
│   └── UpdatedDoc.md       # Updated documentation
└── docs-specs/             # Source specs (DO NOT MODIFY)
    └── ...
```

If the `docs/` directory doesn't exist, create it.

### File Naming

Follow existing conventions in the module. Common patterns:
- Numbered prefixes: `01_Overview.md`, `02_Getting_Started.md`
- Descriptive names: `Throttling_Guide.md`, `Configuration_Reference.md`
- Kebab-case: `graceful-degradation-strategies.md`

Match the existing style in the module's docs directory.

### Content Requirements

Every documentation file or update MUST include:

1. **The "Why"** - Explain the problem this solves and why it matters
2. **Benefits** - What's better about this approach vs. what existed before
3. **Quick Start** - Minimal example to get started immediately
4. **Detailed Usage** - Comprehensive examples with explanations
5. **Configuration** - All relevant configuration options with defaults
6. **Cross-References** - Links to specs or related docs for deeper detail

### Documentation Structure Template

```markdown
# [Feature Name]

[1-2 sentence overview of what this feature does]

## Overview

[Brief explanation of the problem this solves and why this solution exists]

## Why Use This?

- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

## Quick Start

[Minimal example to demonstrate core functionality]

```java
// Minimal working example
```

## Detailed Usage

### [Use Case 1]

[Explanation]

```java
// Example code
```

### [Use Case 2]

[Explanation]

```java
// Example code
```

## Configuration

| Property | Default | Description |
|----------|---------|-------------|
| `property.name` | `default` | What it controls |

## Architecture (if complex)

```
┌─────────┐     ┌─────────┐
│ Box A   │────▶│ Box B   │
└─────────┘     └─────────┘
```

## Best Practices

- [Practice 1]
- [Practice 2]

## Troubleshooting

### [Common Issue 1]
[Solution]

## See Also

- [Link to related documentation]
- [Link to specification for deep detail]
```

## Constraints

**CRITICAL: The following are NOT allowed:**

- Modifying source code files (*.java, *.kt, etc.)
- Modifying build files (build.gradle, settings.gradle, pom.xml)
- Modifying configuration files outside docs/
- Modifying specification files (docs-specs/)
- Creating files outside the `docs/` directory
- Modifying the project structure

**Only markdown files in `docs/` directories may be created or modified.**

## Documentation Quality Standards

### Writing Style

1. **Be concise** - Developers scan documentation; make every word count
2. **Lead with value** - Start sections with what matters most
3. **Use active voice** - "Configure the cache" not "The cache should be configured"
4. **Show, don't tell** - Code examples over prose explanations
5. **Assume competence** - Don't over-explain basics; link to prerequisites

### Code Examples

1. **Must compile** - All Java examples should be syntactically correct
2. **Must be complete** - Include necessary imports in context
3. **Must be realistic** - Use meaningful variable names, not `foo`/`bar`
4. **Must be testable** - Examples should work if copy-pasted

### ASCII Diagrams

Use ASCII diagrams for:
- Component architectures
- Data flow through systems
- Decision trees
- State machines
- Sequence of operations

**Style:**
```
┌─────────────┐     ┌─────────────┐
│  Service    │────▶│   Cache     │
└──────┬──────┘     └──────┬──────┘
       │                   │
       ▼                   ▼
┌─────────────┐     ┌─────────────┐
│  Database   │     │  Infinispan │
└─────────────┘     └─────────────┘
```

## Handling Updates vs New Documentation

### When Updating Existing Docs

1. **Preserve existing structure** - Don't reorganize unless necessary
2. **Update, don't duplicate** - Modify existing sections, don't add redundant ones
3. **Mark deprecated content** - If something is replaced, note what replaces it
4. **Maintain links** - Ensure cross-references remain valid

### When Creating New Docs

1. **Check for overlap** - Ensure this isn't already documented elsewhere
2. **Link from existing** - Update related docs to reference the new document
3. **Follow naming conventions** - Match existing file naming in the module
4. **Consider navigation** - Add to any index or README if one exists

### When Removing Content

1. **Don't delete silently** - If removing significant content, leave a note about where to find updated info
2. **Check for references** - Ensure no other docs link to removed content
3. **Archive if valuable** - Historical context can be valuable; consider notes

## Discovery Process

### Finding the Target Module

```
Input path analysis:
  data-grid/docs-specs/test-support → Module: data-grid
  esb/docs-specs/retry-handler.md   → Module: esb
  infra-core/src/main/java/.../X.java → Module: infra-core
```

### Finding Existing Documentation

```bash
# List existing docs in module
ls -la <module>/docs/

# Search for related documentation
grep -r "<feature-name>" <module>/docs/
```

### Finding Related Specs

```bash
# Look for specs
ls -la <module>/docs-specs/

# Check for glossary or references
find <module>/docs-specs -name "glossary.md" -o -name "reference*.md"
```

## Example Executions

### Example 1: Spec Directory Input

**Input:**
```
Update docs for data-grid/docs-specs/test-support
```

**Process:**
1. Read `data-grid/docs-specs/test-support/README.md` and `specification.md`
2. Read reference materials in `reference/` subdirectory
3. Examine `data-grid/docs/` for existing documentation
4. Identify that this is a new feature - needs new documentation
5. Create `data-grid/docs/DataGrid_Test_Support.md` with:
   - Overview of in-memory testing capability
   - Why it's better than requiring Infinispan for unit tests
   - Quick start example
   - All cache type examples
   - Configuration options
   - Migration guide for existing tests
6. Reference the specification for deep architectural detail

### Example 2: Reference Material Input

**Input:**
```
Update docs based on data-grid/docs-specs/monitoring-infinispan.md
```

**Process:**
1. Read the monitoring specification completely
2. Identify this relates to `data-grid` module
3. Check existing `data-grid/docs/` for monitoring documentation
4. Find `05_DG_Monitoring_Integration_BestPractices.md`
5. Update that file with new monitoring capabilities
6. Add any new configuration options
7. Update examples if API changed
8. Reference spec for implementation details

### Example 3: Code Reference Input

**Input:**
```
Update docs for changes in data-grid/src/main/java/app/krista/infra/dataGrid/throttle/ThrottledRemoteCache.java
```

**Process:**
1. Read `ThrottledRemoteCache.java`
2. Check git history for recent changes:
   ```bash
   git log --oneline -10 -- data-grid/src/main/java/.../throttle/
   git diff HEAD~5 -- data-grid/src/main/java/.../throttle/
   ```
3. Identify what changed (new methods, behavior changes, configuration)
4. Find existing throttling documentation in `data-grid/docs/`
5. Update `06_DG_Throttling_with_RMS.md` with:
   - Any new configuration options
   - Updated behavior descriptions
   - New usage examples
   - Corrected outdated content

## Referencing Specifications

When the source input includes detailed specification documents:

```markdown
## See Also

For detailed architectural decisions and implementation specifics, see:
- [Test Support Specification](../docs-specs/test-support/specification.md)
- [Architecture Reference](../docs-specs/test-support/reference/architecture.md)
```

Do NOT duplicate specification content verbatim. Instead:
- Summarize key points for user consumption
- Provide practical examples
- Reference specs for those who want deeper detail

## Validation Checklist

Before completing, verify:

- [ ] All documentation written to `docs/` directory only
- [ ] No source code files modified
- [ ] No build files modified
- [ ] No specification files modified
- [ ] All code examples are syntactically correct
- [ ] The "why" is clearly explained
- [ ] Practical usage examples provided
- [ ] Configuration options documented
- [ ] ASCII diagrams added where helpful
- [ ] Cross-references to specs included
- [ ] Existing documentation style matched
- [ ] Outdated content corrected or removed

## Console Output Format

```
╔════════════════════════════════════════════════════════════════╗
║                    UPDATE DOCUMENTATION                         ║
╚════════════════════════════════════════════════════════════════╝

📋 Input: data-grid/docs-specs/test-support
📁 Target Module: data-grid
📂 Docs Directory: data-grid/docs/

════════════════════════════════════════════════════════════════

PHASE 1: DISCOVERY

────────────────────────────────────────────────────────────────

[update-docs] Reading specification materials...
[update-docs] Found: specification.md, requirements-analysis.md, test-plan.md
[update-docs] Found reference docs: architecture.md, glossary.md, usage-examples.md
[update-docs] Scanning existing documentation...
[update-docs] Found 8 existing docs in data-grid/docs/

════════════════════════════════════════════════════════════════

PHASE 2: ANALYSIS

────────────────────────────────────────────────────────────────

[update-docs] Key feature: In-memory cache testing support
[update-docs] Benefits identified:
  - Unit tests without Infinispan infrastructure
  - Instant test execution
  - Serialization bug detection

[update-docs] APIs to document:
  - CacheProvider interface
  - InMemoryCacheProvider class
  - InMemoryObjectCache, InMemoryObjectCacheCustomKey, etc.

════════════════════════════════════════════════════════════════

PHASE 3: DOCUMENTATION PLAN

────────────────────────────────────────────────────────────────

[update-docs] Documentation changes planned:
  CREATE: data-grid/docs/DataGrid_Test_Support_Guide.md
    - Overview and benefits
    - Quick start example
    - Detailed usage for all cache types
    - Migration guide

  UPDATE: data-grid/docs/01_DataGrid_Overview.md
    - Add reference to test support documentation

════════════════════════════════════════════════════════════════

PHASE 4: WRITING DOCUMENTATION

────────────────────────────────────────────────────────────────

[update-docs] Creating: DataGrid_Test_Support_Guide.md
[update-docs] ✓ Overview section
[update-docs] ✓ Why Use This section
[update-docs] ✓ Quick Start example
[update-docs] ✓ Detailed usage (4 examples)
[update-docs] ✓ Configuration section
[update-docs] ✓ Migration guide
[update-docs] ✓ Cross-references to specification

[update-docs] Updating: 01_DataGrid_Overview.md
[update-docs] ✓ Added test support reference

════════════════════════════════════════════════════════════════

PHASE 5: VALIDATION

────────────────────────────────────────────────────────────────

[update-docs] ✓ All files in docs/ directory
[update-docs] ✓ No source files modified
[update-docs] ✓ Code examples verified
[update-docs] ✓ Cross-references valid

════════════════════════════════════════════════════════════════

✅ DOCUMENTATION COMPLETE

Files created:
  • data-grid/docs/DataGrid_Test_Support_Guide.md

Files updated:
  • data-grid/docs/01_DataGrid_Overview.md

════════════════════════════════════════════════════════════════
```

## Invocation

To use this skill:

```
Update docs for <input-path>
```

Or with more context:

```
Update the documentation for the test support feature.
Input: data-grid/docs-specs/test-support
Focus on: Migration from existing tests, benefits for CI/CD
```

Or for code-based updates:

```
The throttling code in data-grid was updated. Please update the relevant documentation.
Reference: data-grid/src/main/java/app/krista/infra/dataGrid/throttle/
```

---

## Error Handling

### Missing Input

```
ERROR: Cannot determine documentation source.

Please provide one of:
  • Specification directory path (e.g., data-grid/docs-specs/test-support)
  • Specification document path (e.g., data-grid/docs-specs/monitoring.md)
  • Code reference for analysis (e.g., data-grid/src/main/java/.../Feature.java)

Example: Update docs for data-grid/docs-specs/test-support
```

### No Docs Directory

```
WARNING: No docs/ directory found in module.

Creating: <module>/docs/

Proceeding with documentation creation...
```

### Conflicting Styles

```
NOTE: Existing documentation has inconsistent styles.

Observed patterns:
  • Some files use numbered prefixes (01_, 02_)
  • Some files use descriptive names
  • Some files use kebab-case

Adopting: [most common pattern observed]
```

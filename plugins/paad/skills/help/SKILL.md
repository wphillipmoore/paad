---
name: help
description: Show help for all paad skills or a specific skill
---

# paad Help

Show help for paad skills. If `$ARGUMENTS` matches a skill name, show detailed help for that skill. Otherwise, show the overview.

## Arguments

- `/paad:help` — show all available skills
- `/paad:help vibe` — show detailed help for a specific skill
- `/paad:help agentic-review` — skill names with hyphens work too

## Behavior

If `$ARGUMENTS` is provided and matches a skill name (with or without the `paad:` prefix), show the detailed help for that skill only. If the argument doesn't match any skill, say "Unknown skill: [name]. Available skills:" and show the overview.

Do NOT read files or run commands. All help text is below.

---

## Overview (no arguments)

When showing the overview, display exactly this:

```
paad — impractical tools for software architecture, code quality, and development workflows.

Available skills:

  /paad:agentic-a11y [path]                  Accessibility audit (web, mobile, desktop, CLI, games)
  /paad:agentic-architecture [path...]       Multi-agent architecture analysis (strengths & flaws)
  /paad:agentic-review [base-branch] [path]  Multi-agent code review of current branch (bug hunting)
  /paad:alignment [files...]                 Requirements-to-tasks alignment + TDD rewrite
  /paad:pushback [spec-file]                 Spec/PRD critic (finds issues before you build)
  /paad:vibe [task description]              Safe vibe coding with TDD guardrails

Run /paad:help <skill-name> for detailed help on a specific skill.
```

---

## Detailed Help (per skill)

### agentic-a11y

```
/paad:agentic-a11y [path]

Comprehensive multi-agent accessibility audit of user-facing code.

Supports: web, iOS, Android, React Native, Flutter, desktop, CLI, and games.
Target:   WCAG 2.2 AA baseline, AAA flagged as bonus recommendations.
Output:   paad/a11y-reviews/

Arguments:
  /paad:agentic-a11y                    Audit all user-facing code in the repo
  /paad:agentic-a11y src/components/    Scope to a directory
  /paad:agentic-a11y Modal.tsx          Scope to a file

What it does:
  1. Detects the platform(s) automatically
  2. Dispatches 5 specialist agents in parallel:
     - Screen Reader & Assistive Tech
     - Visual & Color
     - Keyboard & Motor
     - Cognitive & Learning
     - Multimedia & Temporal
  3. Dispatches a Platform-Specific agent if a framework is detected
  4. Verifies findings (filters false positives from component libraries)
  5. Writes a report with:
     - Impact summary by user group
     - Issues ranked by severity (Critical/Serious/Moderate/Minor)
     - WCAG conformance checklist
     - Quick wins (top 5 highest-impact, lowest-effort fixes)

Best used in a fresh session — consumes significant context.
```

### agentic-architecture

```
/paad:agentic-architecture [path...]

Multi-agent architecture analysis. Diagnosis only — finds strengths and
flaws with evidence but does not propose fixes.

Output: paad/architecture-reviews/

Arguments:
  /paad:agentic-architecture                          Full repo
  /paad:agentic-architecture src/                     Scope to a directory
  /paad:agentic-architecture packages/api/ packages/shared/  Multiple dirs

What it does:
  1. Reconnaissance: repo overview, dependency snapshot, steering files
  2. Dispatches 5 specialist agents in parallel:
     - Structure & Boundaries (god objects, cohesion, domain modeling)
     - Coupling & Dependencies (tight coupling, circular deps, abstractions)
     - Integration & Data (API contracts, data ownership, resilience)
     - Error Handling & Observability (error strategy, logging, config)
     - Security & Code Quality (auth, secrets, dead code, test coverage)
  3. Verifies findings (reads actual code, checks git history)
  4. Writes a report with:
     - 14 strength categories assessed
     - 34 flaw/risk types assessed
     - Coverage checklist (every category: observed / not observed / N/A)
     - Hotspots (top 3 files/directories to review)
     - Next questions (max 5, no solutions)

Best used in a fresh session — consumes significant context.
```

### agentic-review

```
/paad:agentic-review [base-branch] [path]

Multi-agent bug-hunting code review of the current branch.

Output: paad/code-reviews/

Arguments:
  /paad:agentic-review                    Diff against main
  /paad:agentic-review develop            Diff against a different branch
  /paad:agentic-review main src/auth/     Scope to a directory

Requirements:
  - Must be on a feature branch (not main/master)
  - Changes must be committed

What it does:
  1. Reconnaissance: diff stats, file manifest, callers/callees
  2. Dispatches 5 specialist agents in parallel:
     - Logic & Correctness
     - Error Handling & Edge Cases
     - Contract & Integration
     - Concurrency & State
     - Security
  3. Dispatches Plan Alignment agent if design docs are found
  4. Verifies findings (reads actual code, filters false positives)
  5. Writes a report with:
     - Issues ranked: Critical / Important / Suggestion
     - Each finding: file:line, bug, impact, suggested fix, confidence

Best used in a fresh session — consumes significant context.
```

### alignment

```
/paad:alignment [files...]

Checks that requirements and implementation plans are aligned.
Rewrites all tasks in TDD red/green/refactor format (mandatory).

Output: paad/alignment-reviews/

Arguments:
  /paad:alignment                              Auto-detect documents
  /paad:alignment requirements.md plan.md      Specific files
  /paad:alignment docs/specs/ docs/plans/      Directories

Auto-detection scans: .kiro/, specs/ (spec-kit), docs/plans/, docs/specs/,
common filenames, and conversation history.

What it does:
  1. Classifies documents as intent (requirements) vs action (tasks)
  2. Reality check: scans git history for conflicts
  3. Three alignment checks:
     - Requirements coverage (every requirement has tasks?)
     - Scope compliance (every task maps to a requirement?)
     - Design alignment (if design docs exist)
  4. Presents issues one at a time, dependency-ordered:
     - Missing requirements first (root causes)
     - Design gaps second
     - Missing/orphaned tasks last (symptoms)
  5. Rewrites all tasks in red/green/refactor format
  6. Updates documents or writes a separate report

Works within an existing conversation — no fresh session needed.
```

### pushback

```
/paad:pushback [spec-file]

Critically reviews a spec, PRD, or design before you start building.

Output: paad/pushback-reviews/

Arguments:
  /paad:pushback path/to/spec.md    Review a specific file
  /paad:pushback                    Auto-detect from conversation or files

Auto-detection checks: conversation history first, then common locations
(docs/plans/, docs/specs/, requirements.md, PRD.md, spec.md).

What it does:
  1. Reality check: scans git history for conflicts with what the
     spec assumes (presented upfront — showstoppers first)
  2. Scope shape check:
     - Feature cohesion: flags unrelated features bundled together
       (things that would be separate PRs)
     - Spec size: flags oversized specs, suggests splits only when
       each piece delivers independent value
  3. Analyzes the spec across 6 categories:
     - Contradictions
     - Feasibility (given the current codebase)
     - Scope imbalance
     - Omissions
     - Ambiguity
     - Security concerns
  4. Presents issues one at a time, most impactful first
  5. For each: concrete options from best to worst, with recommendation
  6. Stop when you say "good enough"
  7. Updates the spec or writes a separate report

Works within an existing conversation — no fresh session needed.
```

### vibe

```
/paad:vibe [task description]

Safe vibe coding. Quick fixes with TDD guardrails.

Arguments:
  /paad:vibe fix the login timeout    Task description inline
  /paad:vibe                          Ask what needs fixing

What it does:
  1. Understands the task (asks clarifying questions if needed)
  2. Pre-flight checks:
     - Test infrastructure exists?
     - Scope check (4+ files = warning)
     - Architecture smell (simple task but hard work = investigate)
     - Reusable components (search before building from scratch)
  3. Implements with mandatory red/green/refactor:
     - RED: write one failing test (stop if unexpected behavior)
     - GREEN: write minimal code to pass
     - REFACTOR: clean up duplication, hard-coded values, patterns
  4. Post-fix summary with contextual follow-up suggestions:
     - Security-sensitive code → /paad:agentic-review
     - UI changes → /paad:agentic-a11y
     - Harder than expected → /paad:agentic-architecture

No fresh session needed — this is a lightweight workflow skill.
```

---
name: architecture
description: Analyze a codebase for software architecture strengths and flaws and report the good and the bad.
---

# Architecture Strengths & Flaws Analyzer

## Arguments

`/paad:architecture` accepts optional `$ARGUMENTS`:

- `/paad:architecture` — analyze the entire repository
- `/paad:architecture src/` — scope the analysis to a specific directory (useful for monorepos or analyzing one service)
- `/paad:architecture packages/api/ packages/shared/` — analyze multiple directories together

When a path is provided, focus the analysis on that scope but still note dependencies on code outside the scope.

## Overview

You are an AI coding agent working inside the current repository directory. Your task is to find **common software architecture strengths and weaknesses** in this codebase and produce a concise report with evidence, then **write the final report to a Markdown file** at:

`paad/architecture-reviews/<YYYY-MM-DD>-<git-repo-name>-architecture-report.md`

* Use today's date in ISO format: YYYY-MM-DD
* Determine \<git-repo-name\> from the git remote or top-level folder. If this directory is not a git repo, omit the repo name portion.
* Create the `paad/architecture-reviews/` directory if it doesn't exist.

## Goal

Produce a balanced report that highlights:

* **Strengths** (what's working architecturally and why it matters)
* **Flaws/Risks** (architectural problems and their likely impact)

**Do NOT propose fixes yet.** This is diagnosis only.

## Scope

Include findings across **all** of the following architectural **issue types** (prioritize high-signal, but ensure coverage across the set). For each type:

* If **observed**, include at least one evidence-backed finding (or reference a finding ID).
* If **not found**, mark **Not observed**.
* If tooling limits prevent assessment, mark **Not assessed**.

### Flaw/Risk types (must cover all 34)

1. Global mutable state — Shared state that any code can change, making behavior unpredictable and hard to test.
2. God object — One class/service accumulates too many responsibilities and becomes a brittle dependency magnet.
3. Tight coupling — Components depend on concrete details of each other, so small changes ripple widely.
4. High/unstable dependencies — Core modules depend on "leaf" modules, forcing rebuilds and coordinated releases.
5. Circular dependencies — Packages/modules import each other, complicating builds, testing, and refactoring.
6. Leaky abstractions — An abstraction requires callers to know underlying details to use it correctly.
7. Over-abstraction — Too many layers/interfaces for uncertain future needs, increasing complexity without payoff.
8. Premature optimization — Architecture choices made for performance before evidence, harming clarity and flexibility.
9. Shotgun surgery — A single logical change requires edits across many files/services.
10. Feature envy / anemic domain model — Business logic lives in services/utilities while domain objects are just data bags.
11. Low cohesion — Modules group unrelated behaviors, making boundaries unclear and changes risky.
12. Hidden side effects — Functions/methods do more than their signature suggests, surprising callers.
13. Inconsistent boundaries — Responsibilities drift between layers/services, causing duplication and confusion.
14. Distributed monolith — "Microservices" in name only, with heavy synchronous coupling and shared release constraints.
15. Chatty service calls — Too many small network calls between services, increasing latency and failure surfaces.
16. Synchronous-only integration — Everything depends on immediate responses, turning partial outages into full outages.
17. No clear ownership of data — Multiple services write the same data, creating conflicts and integrity problems.
18. Shared database across services — Services couple through schema and queries, making independent evolution difficult.
19. Lack of idempotency — Retries create duplicates or corruption because operations aren't safe to repeat.
20. Weak error handling strategy — Errors are swallowed, over-generalized, or inconsistently surfaced.
21. No observability plan — Missing logs/metrics/traces makes debugging and capacity planning guesswork.
22. Configuration sprawl — Behavior is controlled by scattered configs/flags with unclear precedence and drift.
23. Dependency injection misuse — DI becomes a maze of indirection that obscures control flow.
24. Inconsistent API contracts — Endpoints/events evolve without compatibility discipline, breaking consumers.
25. Business logic in the UI — Critical rules live in front-end code, leading to duplication and inconsistent behavior.
26. Poor transactional boundaries — Operations span multiple systems without a strategy, leaving partially-updated states.
27. Temporal coupling — Components must be called in a specific order/timing to work correctly.
28. Magic numbers/strings everywhere — Important values are hard-coded and repeated, making change error-prone.
29. "Utility" dumping ground — Generic helper modules grow into unowned, untestable grab-bags of unrelated code.
30. Security as an afterthought — AuthZ/authN, secrets, and trust boundaries bolted on late/inconsistently enforced.

Additionally, you MUST include these concrete issues:
31) Dead code / unused dependencies — Increases cognitive load and attack surface.
32) Missing or inadequate test coverage for critical paths — Architectural risk that compounds all the others.
33) Hard-coded credentials or secrets in source — Concrete security flaw; call out separately when found.
34) Inconsistent error/logging conventions across services — Specifically cross-service inconsistency (formats, levels, fields, correlation IDs).

---

## Strength categories (must assess and report)

In addition to flaws, explicitly look for **architecture strengths**. Report strengths using the same evidence standard as flaws (label, explanation, evidence). Assess at least these categories:

S1) Clear modular boundaries — Well-defined packages/modules/layers with minimal leakage.
S2) High cohesion — Modules/services group related responsibilities; boundaries feel "natural".
S3) Loose coupling — Abstractions/interfaces/events reduce ripple effects from change.
S4) Dependency direction is stable — Core depends on stable contracts; leaf depends on core; minimal "core depends on leaf".
S5) Dependency management hygiene — Minimal circular deps; consistent import conventions; sensible package structure.
S6) Consistent API contracts — Versioning/compat discipline; schema validation; backward-compatible changes.
S7) Robust error handling — Consistent error taxonomy; errors surfaced appropriately; avoids swallowing exceptions.
S8) Observability present — Structured logs, metrics, traces, correlation IDs, health checks.
S9) Configuration discipline — Centralized config; clear precedence; safe defaults; separation by environment.
S10) Security built-in — AuthN/Z patterns, secret management, least privilege, explicit trust boundaries.
S11) Testability & coverage — Tests around critical paths; good seams; determinism; contract tests where appropriate.
S12) Resilience patterns — Timeouts, retries with idempotency, circuit breakers/backpressure, async integration where appropriate.
S13) Domain modeling strength — Business logic lives with domain entities/value objects; invariants enforced close to data.
S14) Simple, pragmatic abstractions — Abstraction level matches current complexity; avoids over/under engineering.

> If a strength category is "not applicable" due to repo nature (e.g., no networked services), mark it **Not applicable** and briefly explain.

---

## Constraints

* **Do NOT propose fixes** (no refactors, no "should do X"). Only describe strengths and weaknesses with evidence.
* Prefer high-signal findings over exhaustive listing, but ensure coverage across the required sets.
* Every finding MUST include:
  (1) short label,
  (2) 1–2 sentence explanation,
  (3) concrete evidence (file paths + symbol names + a small excerpt or line range reference).
* Validate candidates by opening files to reduce false positives.

---

## Process

A) Repo identification

* Detect if this is a git repo (`git rev-parse`).
* If yes, determine repo name:

  * Prefer: basename of top-level directory OR derive from `git remote get-url origin` (strip .git, take last path segment).
* Set output filename accordingly.

B) Repo overview

* Identify primary languages/frameworks and key directories (apps/, services/, packages/, src/, lib/, etc.).
* Estimate size: number of services/modules/packages if applicable.

C) Dependency & structure analysis (as available)

* Build a quick dependency picture:

  * top-level modules/packages
  * identify potential cycles via import graphs or simple heuristics
  * identify "core depends on leaf" patterns
* Also note **positive structure signals** (clean layering, bounded contexts, stable interfaces).

D) Refactor history check

* Before flagging a candidate flaw, use `git log --oneline` on the relevant files/directories to check whether the current code is the result of recent intentional work. A large file with many recent commits may be a completed refactor, not a neglected problem.
* Intentional design choices can still be flawed — check history to understand context, not to dismiss findings.

E) Search strategy (use repo tools available to you)

* Use ripgrep/git grep and lightweight heuristics; optionally use AST tools if present.
* Specific searches (risks + strengths):

  * Global state: module-level mutable variables, singletons, service locators, static mutables.
  * God objects: very large classes/files, managers/services/controllers with huge responsibility surface; high fan-in/fan-out.
  * Coupling/cycles: cross-layer imports, concrete instantiations, circular imports.
  * Boundaries/cohesion: directory organization, naming, cross-layer leakage, "one reason to change".
  * Abstractions: leaky vs clean; over-abstraction vs pragmatic, consistent interfaces.
  * Side effects: IO/DB/network/event publishing in "pure-looking" functions.
  * Error handling/idempotency/resilience: catch-and-ignore, blanket exceptions, retries with idempotency keys, timeouts, circuit breakers/backpressure (if present).
  * Observability: structured logging, tracing, correlation IDs; consistency across services.
  * Security: authN/Z patterns, secret management; hard-coded secrets.
  * Dead code/unused deps: unused packages, unused files/modules, unreachable code paths, deprecated directories, stale feature flags.
  * Tests/coverage: identify critical paths (entrypoints, handlers, core domain services) and check for corresponding tests; highlight strengths and gaps.

---

## Output format (in the Markdown file)

1. Title: "Architecture Report — \<repo-name or current folder\>"

2. Date: \<today's date in ISO format\>

3. Repo overview (languages, key directories)

4. Strengths (ranked High/Medium/Low impact), 5–15 items, each formatted exactly:

   * [Impact: High|Medium|Low] <Strength label> — <1–2 sentence explanation>.
     Evidence: \<path\>:\<line range\> (\<symbol/function/class\>), excerpt: "\<short excerpt\>"

5. Flaws/Risks (ranked High/Medium/Low impact), 10–25 items, each formatted exactly:

   * [Impact: High|Medium|Low] \<Problem label\> — \<1–2 sentence explanation\>.
     Evidence: \<path\>:\<line range\> (\<symbol/function/class\>), excerpt: "\<short excerpt\>"

6. Coverage checklist

   * **Flaw/Risk types 1–34**: Observed / Not observed / Not assessed, with 1 short line and optional pointer to a finding ID.
   * **Strength categories S1–S14**: Observed / Not observed / Not assessed / Not applicable, with 1 short line and optional pointer to a finding ID.

7. Hotspots: top 3 files/directories to review (brief why; can include both risk hotspots and "strong core" hotspots)

8. Next questions (max 5) to guide humans (questions only; no suggested solutions)

---

## Execution

* Perform the investigation now using available tools (`rg`, `git grep`, `ls`, `tree`, language-specific linters if already configured).
* Then write the Markdown file to `paad/architecture-reviews/` with the required filename.
* Finally, print the path to the generated file and a brief summary (3–6 bullet points) of the highest-impact strengths and risks.

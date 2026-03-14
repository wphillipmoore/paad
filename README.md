# PAAD — Slaying the Four Horsemen of the AIpocalypse

<p align="center">
  <img src="images/paad.png" alt="PAAD — Slaying the AIpocalypse: Pushback, Alignment, Architecture, Degradation" width="600">
</p>

Most AI coding assistants have the same four problems. **PAAD** addresses each one.

| Problem | What goes wrong | Status |
|---------|----------------|--------|
| **P**ushback | AI agrees with whatever you say. It doesn't challenge bad ideas, ask clarifying questions, or tell you your approach has problems. | Largely solved |
| **A**lignment | AI "understands" the assignment — then implements most of it, plus things you didn't ask for. Scope creep from the machine. | Largely solved |
| **A**rchitecture | When a feature is hard to implement because the architecture is wrong, AI forces the feature through instead of fixing the foundation. | Partially solved |
| **D**egradation | As software grows, complexity creates edge cases — security holes, subtle logic bugs, weird interactions. AI can't see these patterns. | Partially solved |

PAAD is a [Claude Code plugin](https://code.claude.com/docs/en/plugin-marketplaces) that gives your AI assistant the tools to catch these problems before they compound.

**WARNING**: PAAD is brutally honest. It will tell you when your spec is flawed, your plan is misaligned, your architecture has problems, or your code has bugs. If you don't want to hear that, don't install PAAD.

Also, this methodology has served me well, but it eats tokens like popcorn at a horror movie.

## Installation

### Add the marketplace

```
/plugin marketplace add Ovid/paad
```

### Install the plugin

```
/plugin install paad@paad
```

### Team setup (optional)

Add to your project's `.claude/settings.json` so teammates are automatically prompted:

```json
{
  "extraKnownMarketplaces": {
    "paad": {
      "source": {
        "source": "github",
        "repo": "Ovid/paad"
      }
    }
  }
}
```

## Available Skills

All skills accept optional arguments to scope or customize their behavior.

---

### Pushback

#### `/paad:pushback [spec-file]`

AI won't tell you your spec has problems. This skill does — critically reviewing specs, PRDs, and design plans before work begins so you don't build on flawed assumptions.

- **Arguments:** `/paad:pushback path/to/spec.md` (specific file) or `/paad:pushback` (auto-detect from conversation history or common file locations)
- **Source control reality check** — scans recent git history for commits that conflict with what the spec assumes, presented upfront before other analysis
- **6 analysis categories**: contradictions, feasibility, scope imbalance, omissions, ambiguity, security concerns
- **Severity-ordered, one issue at a time** — most impactful issues first, with concrete options and recommendations; stop when you're fed up with being told your spec has problems
- **Flexible output** — update the spec in-place or write a separate report to `paad/pushback-reviews/`

---

### Alignment

#### `/paad:alignment [files...]`

AI drifts off-scope. This skill catches it — checking that requirements, designs (if any), and implementation plans actually match, finding gaps in both directions before code gets written.

- **Arguments:** `/paad:alignment` (auto-detect) or `/paad:alignment requirements.md plan.md` (specific files) or `/paad:alignment docs/specs/ docs/plans/` (directories)
- **Auto-detection** — scans `.kiro/`, `specs/` (spec-kit), `docs/plans/`, `docs/specs/`, and common filenames; classifies documents as intent (requirements) vs action (tasks)
- **Source control reality check** — scans recent git history for conflicts with what the documents assume
- **3 alignment checks**: requirements coverage, scope compliance, design alignment (if design docs exist)
- **Dependency-ordered issues** — root causes (missing requirements) before symptoms (missing tasks), one at a time
- **Mandatory TDD rewrite** — once aligned, all tasks are rewritten in red/green/refactor format for better implementation outcomes
- **Flexible output** — update documents in-place or write a separate report to `paad/alignment-reviews/`

---

### Architecture

#### `/paad:agentic-architecture [path...]`

AI builds on bad foundations. This skill finds them — dispatching five specialist agents to examine your codebase for structural problems before they compound. Diagnosis only, no fixes proposed.

- **Arguments:** `/paad:agentic-architecture` (full repo) or `/paad:agentic-architecture src/` (scoped) or `/paad:agentic-architecture packages/api/ packages/shared/` (multiple directories)
- **5 specialist agents** run in parallel: Structure & Boundaries, Coupling & Dependencies, Integration & Data, Error Handling & Observability, Security & Code Quality
- **Verification phase** filters false positives — confirms findings by reading actual code and checking git history
- **14 strength categories** (modular boundaries, cohesion, coupling, error handling, observability, security, testability, and more)
- **34 flaw/risk types** (god objects, tight coupling, circular dependencies, leaky abstractions, dead code, missing tests, hard-coded secrets, and more)
- **Coverage checklist** ensuring every category is assessed
- **Hotspots** identifying the top files/directories to review
- **Report** written to `paad/architecture-reviews/`

---

### Degradation

#### `/paad:agentic-review [base-branch] [path]`

As code grows, bugs hide. This skill hunts them — five specialist agents review your branch for logic errors, edge cases, security holes, and integration problems that a single-pass review would miss.

- **Arguments:** `/paad:agentic-review` (diff against `main`) or `/paad:agentic-review develop` (diff against `develop`) or `/paad:agentic-review main src/auth/` (scoped to a directory)
- **5 specialist agents** run in parallel: Logic & Correctness, Error Handling & Edge Cases, Contract & Integration, Concurrency & State, Security
- **Verification phase** filters false positives and deduplicates findings across specialists
- **Severity ranking**: Critical / Important / Suggestion
- **Plan alignment** (conditional): if design docs are found, checks implementation against the plan
- **Report** written to `paad/code-reviews/`

Requires a feature branch (not main/master) with committed changes.

#### `/paad:a11y [path]`

Accessibility barriers are a form of degradation that's invisible to most developers. This skill catches them — running five specialist agents across your codebase to find real barriers organized by who they affect.

Supports **web, iOS, Android, React Native, Flutter, desktop, CLI, and games**. Evaluates against WCAG 2.2 AA (applied via WCAG2ICT for non-web platforms, with AAA noted as bonus recommendations).

- **Arguments:** `/paad:a11y` (full repo) or `/paad:a11y src/components/` (scoped to a directory or file)
- **Automatic platform detection** — identifies the project's platform(s) and adapts all checks accordingly
- **5 specialist agents** run in parallel, each focused on a different disability category:
  - **Screen Reader & Assistive Tech** — platform-appropriate semantics (ARIA for web, UIAccessibility for iOS, AccessibilityNodeInfo for Android, Semantics for Flutter, etc.)
  - **Visual & Color** — contrast ratios, color-only information, text scaling/Dynamic Type, magnification, colorblind modes
  - **Keyboard & Motor** — keyboard/switch/sip-and-puff operability, target sizes, remappable controls, gesture alternatives
  - **Cognitive & Learning** — consistent navigation, error recovery, clear language, accessible authentication, predictable behavior
  - **Multimedia & Temporal** — captions, transcripts, reduced-motion preferences, flash thresholds, auto-play controls
- **Platform-specific agent** (conditional): dispatched for framework-specific pitfalls (React, Vue, SwiftUI, Jetpack Compose, Flutter, Unity, etc.)
- **Verification phase** confirms barriers exist and aren't handled by the platform, framework, or component library
- **WCAG conformance checklist** plus platform-specific guidelines (Apple HIG, Material Design, Xbox Accessibility Guidelines)
- **Impact summary by user group** explaining how the codebase affects each disability category
- **Quick wins** section identifying the top 5 highest-impact, lowest-effort fixes
- **Report** written to `paad/a11y-reviews/`

---

### Workflow

#### `/paad:vibe [task description]`

Speed without recklessness. Safe vibe coding with TDD guardrails for small fixes and quick changes.

- **Arguments:** `/paad:vibe fix the login timeout` (task inline) or `/paad:vibe` (ask what needs fixing)
- **Pre-flight checks** before writing any code:
  - Test infrastructure exists? If not, warn and ask how to proceed
  - Scope check — if 4+ files or cross-module, warn this may not be a vibe task
  - Architecture smell — if a simple task requires lots of work, investigate deeper issues first
  - Reusable components — search the codebase for existing utilities before building from scratch
- **Mandatory red/green/refactor** — write a failing test, write minimal code to pass, then refactor. If the test passes or fails unexpectedly, stop and ask
- **Post-fix summary** with contextual follow-up suggestions (agentic-review for security-sensitive changes, a11y for UI changes, architecture if the fix was harder than expected)

#### `/paad:help [skill-name]`

Show help for all paad skills or detailed help for a specific skill.

- **Arguments:** `/paad:help` (overview of all skills) or `/paad:help vibe` (detailed help for one skill)

## Local Development

Test the plugin locally without installing:

```bash
claude --plugin-dir ./plugins/paad
```

Then invoke skills with `/paad:help` to see all available skills, or try `/paad:vibe`, `/paad:pushback`, etc.

After making changes, run `/reload-plugins` inside Claude Code to pick up updates without restarting.

### Validate

```bash
claude plugin validate .                  # validate marketplace
claude plugin validate ./plugins/paad     # validate plugin
```

## License

MIT

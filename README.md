# PAAD — Slaying the Four Horsemen of the AIpocalypse

<p align="center">
  <img src="images/paad.png" alt="PAAD — Slaying the Four Horsemen of the AIpocalypse: Pushback, Alignment, Architecture, Degradation" width="600">
</p>

The best software developers are like AI in the sense that they're not perfect. Those developers write tests for their code, they request code review, CI/CD pipelines catch issues, QA also checks for problems, UAT checks for problems. And finally, Incident Response teams are there to clean up the mess when all of those layers of defense-in-depth fail.

We keep building AI tools and processes in hopes of improving AI. This is good, but we also need to provide that defense-in-depth. Welcome to PAAD.

---

Most AI coding assistants have the same four problems. **PAAD** addresses each one. See also, [this horrendously long explanation](https://curtispoe.org/articles/why-i-am-no-longer-reading-the-ais-code.html).

| Problem | What goes wrong | Status |
|---------|----------------|--------|
| **P**ushback | AI is a smarmy little git. Push back? No. Push to production? Absolutely. Push problems to Future You? Every time. | Largely solved |
| **A**lignment | AI hears "add a button" and delivers a button, a modal, a notification system, and a config page. The button doesn't work. | Largely solved |
| **A**rchitecture | Your architecture is a house of cards. AI's solution? More cards. Taller. | Partially solved |
| **D**egradation | Death by a thousand commits. Each change is fine. Together they're a security hole, a race condition, and a mystery bug that only happens on Tuesdays. | Partially solved |

PAAD is a system of AI agent skills—originally built as a [Claude Code plugin](https://code.claude.com/docs/en/plugin-marketplaces) that gives your assistant the tools to catch these problems before they compound. It now supports **Claude Code**, **Kiro**, and **Antigravity**.

**WARNING**: PAAD is brutally honest. It will tell you when your spec is flawed, your plan is misaligned, your architecture has problems, or your code has bugs. If you don't want to hear that, don't install PAAD.

Also, while this methodology has served me well, **it eats tokens like popcorn at a horror movie**. I'm not aiming for quantity, I'm aiming for quality.

## Workflow

First, you might forget commands. That's OK. Just run `/paad:help` to see all available skills and their usage.

Before I start working in any repo, I run `/paad:makefile` to set up a standard Makefile with targets for building, testing, linting, and formatting. This gives me a consistent interface for common tasks and encourages good habits. More importantly, the code coverage, linting, and formatting tools are critical to help PAAD generate production-quality code and catch issues early.

Then I follow this general workflow:

1. Create your spec, design doc, or implementation plan as usual.
2. Before you start building, run `/paad:pushback` to get a critical review of your spec.
3. As you build, run `/paad:alignment` to check that your implementation plan matches your requirements and design.
4. When you have a working branch, run `/paad:agentic-review` to catch bugs, security holes, and integration problems before merging.

I often run `/paad:pushback` and `/paad:alignment` more than once to catch issues the first run (or introduced).

Also ...

1. Periodically run `/paad:agentic-architecture` to catch structural problems before they compound.
2. For UI changes, run `/paad:agentic-a11y` to catch accessibility barriers before they go live.
3. For small fixes and quick changes, use `/paad:vibe` to get TDD guardrails and contextual suggestions.

## Installation

### Claude Code

#### Add the marketplace

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

### Kiro & Antigravity

PAAD provides pre-converted versions of the skills for both Kiro and Antigravity.

1. Create a `.kiro/skills/` and/or `.agent/skills/` directory in your project root.
2. Copy the desired skills from the `kiro_and_antigravity/skills/` directory in this repo.
3. **Note**: Antigravity skills function as wrappers. You MUST also copy the corresponding Kiro skill to your project's `.kiro/skills/` directory, as the Antigravity skill references it.

### Using Skills with Kiro & Antigravity

In Kiro and Antigravity, skills are automatically recognized by your assistant. You don't need a specific prefix; simply ask your assistant to perform the task (e.g., "Run a pushback review on this spec" or "Analyze the architecture of this module"). The assistant will follow the checklists and procedures defined in the skill files.

## Available Skills

Each skill targets one of the four problems. Run them before, during, or after coding — they all work from the command line inside Claude Code.

---

### Pushback

#### `/paad:pushback [spec-file]`

AI won't tell you your spec has problems. This skill does — critically reviewing specs, PRDs, and design plans before work begins so you don't build on flawed assumptions.

- **Arguments:** `/paad:pushback path/to/spec.md` (specific file) or `/paad:pushback` (auto-detect from conversation history or common file locations)
- **Source control reality check** — scans recent git history for commits that conflict with what the spec assumes, presented upfront before other analysis
- **Scope shape check** — flags unrelated features bundled together (things that would be separate PRs) and oversized specs; suggests splits only when each piece delivers independent value
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

AI builds on bad foundations. This skill finds them — five specialists each examine your codebase from a different angle (structure, coupling, integration, error handling, security) so nothing hides behind a single reviewer's blind spots. Diagnosis only, no fixes proposed.

- **Arguments:** `/paad:agentic-architecture` (full repo) or `/paad:agentic-architecture src/` (scoped) or `/paad:agentic-architecture packages/api/ packages/shared/` (multiple directories)
- **Parallel analysis** — all five specialists run simultaneously, then a verification phase filters false positives by reading actual code and checking git history
- **14 strength categories** (modular boundaries, cohesion, coupling, error handling, observability, security, testability, and more)
- **34 flaw/risk types** (god objects, tight coupling, circular dependencies, leaky abstractions, dead code, missing tests, hard-coded secrets, and more)
- **Coverage checklist** ensuring every category is assessed
- **Hotspots** identifying the top files/directories to review
- **Report** written to `paad/architecture-reviews/`

#### `/paad:fix-architecture [report]`

Architecture analysis tells you what's wrong. This skill fixes it — loading an architecture report and guiding you through fixing flaws one at a time with a test-first workflow. Each fix is validated, tested, committed, and tracked in the report so you can pick up where you left off.

- **Arguments:** `/paad:fix-architecture` (find most recent report) or `/paad:fix-architecture path/to/report.md` (specific report)
- **Pre-flight checks**: branch protection (feature branch required), report staleness detection, test infrastructure verification, baseline test run
- **Developer conversation** before any code is touched: solo vs team (batch size), auto-commit vs manual, flaw triage (high-impact, quick wins, or specific F-IDs), plan confirmation
- **Test-first fixes** — validates each flaw still exists, writes safety-net tests for untested code, proposes fix options with tradeoffs, executes with red/green/refactor
- **Status tracking** in the report: Fixed, Won't fix, Partially fixed, Skipped, Fixed (pre-existing), Attempted/reverted — with reasons, timestamps, and commit SHAs
- **Flaw dependency detection** — flags when fixing one flaw resolves others
- **Iterative** — run across multiple sessions, each time fixing more flaws from the same report

Requires a feature branch (not main/master) and an existing architecture report.

**Why sequential?** Architecture fixes run one at a time, not in parallel. Fixing one flaw often resolves others (the skill checks for this after each fix), and that dependency can only be discovered sequentially. Parallel agents in worktrees would avoid stepping on each other's files, but merging refactored code back together creates conflicts — and resolving merge conflicts after structural changes is a reliable way to introduce new bugs.

---

### Degradation

Code doesn't rot in one commit. It rots in a hundred small ones — each fine on its own, invisible in aggregate.

#### `/paad:agentic-review [base-branch] [path]`

As code grows, bugs hide. This skill hunts them — separate reviewers focus on logic, error handling, contracts, concurrency, and security so that a race condition doesn't slip past while everyone's looking at input validation.

- **Arguments:** `/paad:agentic-review` (diff against `main`) or `/paad:agentic-review develop` (diff against `develop`) or `/paad:agentic-review main src/auth/` (scoped to a directory)
- **Parallel review** — all five specialists examine your branch simultaneously, then findings are verified against actual code and deduplicated
- **Severity ranking**: Critical / Important / Suggestion
- **Plan alignment** (conditional): if design docs are found, checks implementation against the plan
- **Report** written to `paad/code-reviews/`

Requires a feature branch (not main/master) with committed changes.

#### `/paad:agentic-a11y [path]`

Accessibility barriers are a form of degradation that's invisible to most developers. This skill catches them — organized by *who is affected*, not by which WCAG criterion you violated.

Supports **web, iOS, Android, React Native, Flutter, desktop, CLI, and games**. Evaluates against WCAG 2.2 AA (applied via WCAG2ICT for non-web platforms, with AAA noted as bonus recommendations).

- **Arguments:** `/paad:agentic-a11y` (full repo) or `/paad:agentic-a11y src/components/` (scoped to a directory or file)
- **Automatic platform detection** — identifies the project's platform(s) and adapts all checks accordingly
- **Specialists by disability category** — screen reader users, visual/color, keyboard/motor, cognitive, and multimedia each get a dedicated reviewer rather than one generalist trying to cover everything
- **Platform-specific agent** (conditional): dispatched for framework-specific pitfalls (React, Vue, SwiftUI, Jetpack Compose, Flutter, Unity, etc.)
- **Verification phase** confirms barriers exist and aren't handled by the platform, framework, or component library
- **WCAG conformance checklist** plus platform-specific guidelines (Apple HIG, Material Design, Xbox Accessibility Guidelines)
- **Impact summary by user group** explaining how the codebase affects each disability category
- **Quick wins** section identifying the top 5 highest-impact, lowest-effort fixes
- **Report** written to `paad/a11y-reviews/`

---

### Workflow

#### `/paad:makefile`

Creates or updates a project Makefile with standard targets (`help`, `all`, `test`, `cover`, `lint`, `format`). Detects your stack automatically and never modifies an existing target without asking first.

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

### Testing

Run all checks with:

```bash
make test
```

This validates the marketplace and plugin structure, then runs consistency checks (version sync, digraph presence, help/README coverage, frontmatter validity). See all available targets with `make help`.

Individual checks can be run separately:

```bash
make check-versions     # marketplace.json ↔ plugin.json version sync
make check-digraphs     # every skill (except help) has a digraph
make check-help         # every skill is documented in paad:help
make check-readme       # every skill is documented in README.md
make check-frontmatter  # SKILL.md frontmatter is valid, folder name matches
make validate           # claude plugin validate on marketplace + plugins
```

## Contributing

1. Fork the repo and create a feature branch
2. Make your changes — see `CLAUDE.md` for conventions on adding/modifying skills
3. Run `make test` to verify everything passes
4. Open a pull request

Key rules from `CLAUDE.md`:
- Every skill (except `help`) must include a graphviz digraph covering its decision points
- Skill folder names must match the `name` field in `SKILL.md` frontmatter
- Bump the version in both `plugin.json` and `marketplace.json`
- Update `README.md`, `paad:help`, and `CLAUDE.md` when adding or changing skills

## License

MIT

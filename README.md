# paad — Plugin Marketplace for Claude Code

A [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) providing architecture analysis, code quality, and development workflow skills.

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

### `/paad:a11y`

Comprehensive multi-agent accessibility audit of user-facing code. Supports **web, iOS, Android, React Native, Flutter, desktop, CLI, and games**. Evaluates against WCAG 2.2 AA (applied via WCAG2ICT for non-web platforms, with AAA noted as bonus recommendations) and produces an actionable report organized by user impact.

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

### `/paad:agentic-review`

Multi-agent bug-hunting review of the current branch against main. Dispatches specialist agents in parallel, verifies findings to filter false positives, ranks by severity, and produces a persistent report.

- **5 specialist agents** run in parallel: Logic & Correctness, Error Handling & Edge Cases, Contract & Integration, Concurrency & State, Security
- **Verification phase** filters false positives and deduplicates findings across specialists
- **Severity ranking**: Critical / Important / Suggestion
- **Plan alignment** (conditional): if design docs are found, checks implementation against the plan
- **Report** written to `paad/code-reviews/`

Requires a feature branch (not main/master) with committed changes.

### `/paad:architecture`

Comprehensive architecture analysis of the current codebase. Diagnosis only — identifies strengths and problems with evidence but does not propose fixes.

- **14 strength categories** (modular boundaries, cohesion, coupling, error handling, observability, security, testability, and more)
- **34 flaw/risk types** (god objects, tight coupling, circular dependencies, leaky abstractions, dead code, missing tests, hard-coded secrets, and more)
- **Evidence-based findings** with file paths, line ranges, and code excerpts
- **Coverage checklist** ensuring nothing is missed
- **Hotspots** identifying the top files/directories to review
- **Next questions** to guide follow-up investigation
- **Report** written to `paad/architecture-reviews/`

## Local Development

Test the plugin locally without installing:

```bash
claude --plugin-dir ./plugins/paad
```

Then invoke skills with `/paad:a11y`, `/paad:agentic-review`, `/paad:architecture`, etc.

After making changes, run `/reload-plugins` inside Claude Code to pick up updates without restarting.

### Validate

```bash
claude plugin validate .                  # validate marketplace
claude plugin validate ./plugins/paad     # validate plugin
```

## License

MIT

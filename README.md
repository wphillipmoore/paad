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

### `/paad:architecture`

Performs a comprehensive architecture analysis of the current codebase and writes a detailed report to a Markdown file. The report covers:

- **14 strength categories** (modular boundaries, cohesion, coupling, error handling, observability, security, testability, and more)
- **34 flaw/risk types** (god objects, tight coupling, circular dependencies, leaky abstractions, dead code, missing tests, hard-coded secrets, and more)
- **Evidence-based findings** with file paths, line ranges, and code excerpts
- **Coverage checklist** ensuring nothing is missed
- **Hotspots** identifying the top files/directories to review
- **Next questions** to guide follow-up investigation

This is a diagnosis-only tool — it identifies strengths and problems with evidence but does not propose fixes.

### `/paad:agentic-review`

Multi-agent bug-hunting review of the current branch against main. Dispatches specialist agents in parallel, verifies findings to filter false positives, ranks by severity, and produces a persistent report.

- **5 specialist agents** run in parallel: Logic & Correctness, Error Handling & Edge Cases, Contract & Integration, Concurrency & State, Security
- **Verification phase** filters false positives and deduplicates findings across specialists
- **Severity ranking**: Critical / Important / Suggestion
- **Plan alignment** (conditional): if design docs are found, checks implementation against the plan
- **Persistent report** written to `docs/reviews/`

Requires a feature branch (not main/master) with committed changes.

## Local Development

Test the plugin locally without installing:

```bash
claude --plugin-dir ./plugins/paad
```

Then invoke skills with `/paad:architecture`, `/paad:agentic-review`, etc.

After making changes, run `/reload-plugins` inside Claude Code to pick up updates without restarting.

### Validate

```bash
claude plugin validate .                  # validate marketplace
claude plugin validate ./plugins/paad     # validate plugin
```

## License

MIT

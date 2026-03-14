# CLAUDE.md — paad

## What this project is

This is a **Claude Code plugin marketplace** hosted at `github.com/Ovid/paad`. It distributes the `paad` plugin, which provides skills for architecture analysis, code quality, and development workflows.

## Project structure

```
paad/
├── .claude-plugin/
│   └── marketplace.json           ← marketplace catalog (lists all plugins)
├── plugins/
│   └── paad/                      ← the "paad" plugin (namespace for all skills)
│       ├── .claude-plugin/
│       │   └── plugin.json        ← plugin manifest (name, version, metadata)
│       └── skills/
│           ├── a11y/
│           │   └── SKILL.md       ← /paad:a11y skill
│           ├── agentic-review/
│           │   └── SKILL.md       ← /paad:agentic-review skill
│           └── architecture/
│               └── SKILL.md       ← /paad:architecture skill
├── CLAUDE.md                      ← this file
└── README.md
```

## Key conventions

- **Marketplace name**: `paad`
- **Plugin name**: `paad` (so all skills are invoked as `/paad:<skill-name>`)
- **Skill naming**: skill folder names become the suffix after `paad:` — e.g., `skills/architecture/` → `/paad:architecture`
- **Versioning**: both `marketplace.json` and `plugin.json` use semver. Bump the plugin version in `plugin.json` (it takes precedence). Keep `marketplace.json` version in sync.
- **Validation**: run `claude plugin validate .` (marketplace) and `claude plugin validate ./plugins/paad` (plugin) before committing

## Adding a new skill

1. Create `plugins/paad/skills/<skill-name>/SKILL.md` with frontmatter (`name`, `description`) and instructions
2. Validate with `claude plugin validate ./plugins/paad`
3. Test locally with `claude --plugin-dir ./plugins/paad`
4. Bump the version in both `plugins/paad/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
5. Update `README.md` to document the new skill under "Available Skills"

## Important rules

- Do NOT put `skills/`, `commands/`, or `agents/` inside `.claude-plugin/` — only `plugin.json` or `marketplace.json` go there
- Skill files must be named `SKILL.md` (uppercase) inside a folder whose name becomes the skill name
- Plugin sources in `marketplace.json` use paths relative to the marketplace root (start with `./`)
- Keep marketplace.json plugin descriptions in sync with plugin.json descriptions

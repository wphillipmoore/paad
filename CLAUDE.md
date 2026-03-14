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
│           ├── agentic-architecture/
│           │   └── SKILL.md       ← /paad:agentic-architecture skill
│           ├── agentic-review/
│           │   └── SKILL.md       ← /paad:agentic-review skill
│           ├── alignment/
│           │   └── SKILL.md       ← /paad:alignment skill
│           ├── help/
│           │   └── SKILL.md       ← /paad:help skill
│           ├── pushback/
│           │   └── SKILL.md       ← /paad:pushback skill
│           └── vibe/
│               └── SKILL.md       ← /paad:vibe skill
├── CLAUDE.md                      ← this file
└── README.md
```

## Key conventions

- **Marketplace name**: `paad`
- **Plugin name**: `paad` (so all skills are invoked as `/paad:<skill-name>`)
- **Skill naming**: skill folder names become the suffix after `paad:` — e.g., `skills/agentic-architecture/` → `/paad:agentic-architecture`
- **Versioning**: both `marketplace.json` and `plugin.json` use semver. Bump the plugin version in `plugin.json` (it takes precedence). Keep `marketplace.json` version in sync.
- **Validation**: run `claude plugin validate .` (marketplace) and `claude plugin validate ./plugins/paad` (plugin) before committing

## Adding a new skill

1. Create `plugins/paad/skills/<skill-name>/SKILL.md` with frontmatter (`name`, `description`) and instructions
2. Consider `$ARGUMENTS` support — if the skill could benefit from user-provided scope (a file path, directory, branch name, etc.), add an Arguments section documenting usage. Users shouldn't need to remember flags; keep arguments positional and intuitive (e.g., `/paad:skillname path/to/scope`).
3. Validate with `claude plugin validate ./plugins/paad`
4. Test locally with `claude --plugin-dir ./plugins/paad`
5. Bump the version in both `plugins/paad/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
6. Update `README.md` to document the new skill under "Available Skills", including argument syntax in the heading
7. Add the new skill to `paad:help` — both the overview table and a detailed help section

## Modifying an existing skill

When changing a skill's behavior, arguments, or output, review `plugins/paad/skills/help/SKILL.md` and update the corresponding help text to match.

## Important rules

- Do NOT put `skills/`, `commands/`, or `agents/` inside `.claude-plugin/` — only `plugin.json` or `marketplace.json` go there
- Skill files must be named `SKILL.md` (uppercase) inside a folder whose name becomes the skill name
- Plugin sources in `marketplace.json` use paths relative to the marketplace root (start with `./`)
- Keep marketplace.json plugin descriptions in sync with plugin.json descriptions

# Codex Profile: maintenance

Source area: repository documentation, scripts, configuration, agent metadata, and non-content project structure.

## Role

Maintain the Lecture Builder repository without generating lecture content: docs, scripts, configuration, Codex/Gemini policy wrappers, housekeeping, and structural consistency.

Use this profile for changes such as updating README, AGENTS.md, `.codex/agents/*`, `.gemini/settings.json`, helper scripts, or repository organization.

## Startup

1. Read root `AGENTS.md`.
2. Read README and relevant `.gemini/` or `.codex/` files.
3. Inspect affected scripts/config/docs before editing.
4. Identify whether the task affects pipeline behavior, generated content, or only documentation.

## Lifecycle

### PLAN `[xhigh reasoning]`

Do not write files.

- Identify affected files and ownership.
- Check references between README, AGENTS.md, `.gemini/`, `.codex/`, scripts, and output contracts.
- Define verification checks for links, paths, and examples.

### IMPLEMENT `[high reasoning]`

- Keep documentation and policy files consistent.
- Do not modify generated lecture artifacts unless explicitly requested.
- Do not change Gemini agent behavior unless the task explicitly asks for it.
- Preserve existing pipeline contracts and resumability.

### VERIFY `[xhigh reasoning]`

- Check referenced paths exist.
- Check examples match actual repository layout.
- Validate JSON/TOML/YAML files touched by the task.
- Record unavailable tooling or validation blockers exactly.

### FIX

Fix broken references, inconsistent docs, malformed config, or incomplete policy wrappers.

## Report

Write report to `.codex/reports/maintenance/<task_id>.md`.

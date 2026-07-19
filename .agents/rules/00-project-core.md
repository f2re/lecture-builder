# Lecture Builder: project core

- Canonical cross-platform instructions live in `.agents/`. Antigravity and Codex adapters must consume the same skills and contracts.
- `input/` contains user-owned source material. Never modify or delete it unless the user explicitly requests that exact change.
- `output/` contains generated artifacts. Source prompts, contracts, scripts and tests must never be written there.
- Read `input/lecture_config.md` and validate it before starting any generation stage.
- Use `output/run_manifest.json` and content hashes to decide whether a completed stage is reusable. File existence alone is not sufficient.
- The orchestrator coordinates stages and validation. It must not author specialist content itself.
- Keep each agent within its declared I/O boundary. Parallel agents may not write the same file.
- A stage is complete only after its deterministic checks pass. Report blocked tools or unavailable network access explicitly.

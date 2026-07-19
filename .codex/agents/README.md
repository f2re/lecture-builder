# Codex custom agents

These TOML profiles adapt the platform-independent rules, workflows and skills in `.agents/` to Codex. Scientific and pedagogical behavior belongs in shared Skills; TOML files contain only role boundaries, sandbox policy and orchestration-specific instructions.

Root `AGENTS.md` is mandatory. Select the narrowest profile for the task. Read-only reviewers must not edit artifacts. Writing profiles must respect the output boundaries defined by the matching Skill.

The orchestrator may parallelize independent search/extraction work, disjoint section files, and the two read-only reviews. Manifest updates, assembly, editing, formula numbering and publication remain sequential.

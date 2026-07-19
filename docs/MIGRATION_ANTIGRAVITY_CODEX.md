# Migration from Gemini-centric 2.x to cross-platform 3.0

## Objective

Preserve the useful 2.x behavior—specialized roles, resumable stages, one section per context, local literature, ФГОС/ГОСТ support, examples, review, illustrations and DOCX—while removing platform lock-in and prompt-only guarantees.

## Source-of-truth change

Before:

```text
.gemini/workflows → .gemini/agents → .gemini/skills
.codex/agents/*.md → wrappers around Gemini files
```

After:

```text
.agents/rules + .agents/workflows + .agents/skills  (canonical)
        ├─ Antigravity native workspace layer
        ├─ Codex TOML role adapters
        └─ Gemini compatibility adapters
```

## Role mapping

| 2.x role | 3.0 responsibility |
|---|---|
| orchestrator | orchestration + hash manifest only |
| literature-analyst | orchestration of three research roles |
| lit-searcher | literature-searcher |
| lit-fetcher | source-extractor |
| lit-report | evidence-curator |
| query-builder | lecture-architect |
| section-writer | section-writer |
| document-assembler | coherence-editor |
| reviewer | scientific-reviewer + pedagogical-reviewer |
| editor | final-editor + independent fact-checker + publisher |

## Contract changes

- `lecture_number` is explicit.
- `evidence_ledger.json` is mandatory.
- `lecture_blueprint.json` and `section_briefs/` precede writing.
- source metadata carries verification/provenance status.
- citations use stable source ids.
- formulas use stable labels until one global numbering pass.
- reviews are JSON and independently executed.
- manifest freshness uses content hashes.
- strict validation is mandatory before publication.

## Compatibility policy

`.gemini` remains for legacy command names, but adapters must reference `.agents`. New scientific or pedagogical rules must be added to a shared Skill, not copied into Gemini/Codex prompts.

Old generated outputs should not be trusted solely because they exist. The first 3.0 run should initialize a new manifest, validate or regenerate research evidence, then rebuild downstream artifacts.

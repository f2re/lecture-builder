# Codex Agent Profiles

This directory contains explicit Codex profiles for the Lecture Builder Gemini CLI pipeline.

Codex must always start from the root `AGENTS.md`, then select one of these profiles.

## Profiles

| Profile | Gemini source | Workflow | Use for |
|---|---|---|---|
| `orchestrator` | `.gemini/agents/orchestrator.md` | `.gemini/workflows/orchestrator.md` | full pipeline coordination and status checks |
| `literature-analyst` | `.gemini/agents/literature-analyst.md` | `.gemini/workflows/literature-analyst.md` | coordinate literature sub-pipeline |
| `lit-searcher` | `.gemini/agents/lit-searcher.md` | `.gemini/workflows/lit-searcher.md` | search matrix, web/local source discovery |
| `lit-fetcher` | `.gemini/agents/lit-fetcher.md` | `.gemini/workflows/lit-fetcher.md` | fetch URLs and extract fragments |
| `lit-report` | `.gemini/agents/lit-report.md` | `.gemini/workflows/lit-report.md` | bibliography, literature map, key concepts |
| `query-builder` | `.gemini/agents/query-builder.md` | `.gemini/workflows/query-builder.md` | expand lecture questions into section prompts |
| `section-writer` | `.gemini/agents/section-writer.md` | `.gemini/workflows/section-writer.md` | write one lecture section |
| `document-assembler` | `.gemini/agents/document-assembler.md` | `.gemini/workflows/document-assembler.md` | assemble draft and figure artifacts |
| `reviewer` | `.gemini/agents/reviewer.md` | `.gemini/workflows/reviewer.md` | methodological review and competency coverage |
| `editor` | `.gemini/agents/editor.md` | `.gemini/workflows/editor.md` | final edit, terminology unification, edit log |
| `docx` | `scripts/md2docx/` | n/a | Markdown to DOCX conversion checks |
| `maintenance` | repository docs/scripts | n/a | repository maintenance and non-content edits |

## Universal lifecycle

1. PLAN — inspect inputs, workflows, skills, and existing output; do not edit.
2. IMPLEMENT — follow the selected workflow exactly.
3. VERIFY — check expected files, JSON validity, references, formulas, and DOCX conversion when applicable.
4. FIX — fix only concrete verification failures.

## Reports

Write Codex reports to `.codex/reports/<profile>/<task_id>.md` unless the user asks for another location.

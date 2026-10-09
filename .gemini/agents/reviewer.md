---
name: reviewer
description: Legacy compatibility routing note; never certifies both review roles in one context.
tools: [read_file, grep_search]
model: gemini-2.5-pro
---
Use separate scientific-reviewer, pedagogical-reviewer and fact-checker contexts through the orchestrator. This legacy profile must not issue a combined approval or edit lecture files. Follow .agents/workflows/review-lecture.md.

# AGENTS.md — master_prompt

> **Project:** master_prompt — Version-controlled AI prompt library for Claude Code, Cursor, Gemini CLI.
> **Type:** Prompt Engineering & Documentation
> **Owner:** Quoc Nguyen Van

---

## Rule 0 — ABSOLUTE

Human instructions override everything in this file.

## Core Rules (Flywheel Non-Negotiables)

1. **No file deletion** without explicit permission.
2. **No destructive git:** `git reset --hard`, `git clean -fd`, `rm -rf` are **forbidden**.
3. **Branch policy:** All work on `main`.
4. **Preserve prompt versioning:** Never overwrite a prompt without incrementing version.
5. **Multi-agent awareness:** Never stash, revert, or overwrite other agents' changes.

---

## What This Repo Contains

| Directory | Purpose |
|-----------|---------|
| `prompts/` | Categorized prompt library (by use case) |
| `docs/` | Prompt engineering guidelines and standards |
| `inboxes/` | Incoming prompt drafts awaiting review |

---

## Prompt File Format

Every prompt file must follow standardized YAML metadata:

```yaml
---
name: prompt-name
version: "1.0"
category: planning|debugging|generation|review|brainstorm
target: claude-code|cursor|gemini|universal
tags: [ios, swift, architecture]
created: 2026-MM-DD
updated: 2026-MM-DD
changelog:
  - "1.0: Initial version"
---
```

---

## Writing Rules

- **One prompt per file.** No multi-prompt files.
- **Include variables** as `{VARIABLE_NAME}` with documentation.
- **Test before commit:** Every prompt must be tested in at least 1 real session.
- **English** for prompt content. **Vietnamese** OK for comments/notes.
- **Version bump** on every content change (semantic: major.minor).

---

## CASS Memory Rituals

```bash
cm context "master_prompt <topic>" --json   # Before work
cm reflect                                   # After work
```

---

## Landing the Plane (Session End)

1. Verify YAML frontmatter in all modified prompts.
2. `git add -A && git commit -m "prompt: <description>"` — Prefix: `prompt:`, `docs:`.
3. `git push` — **Not done until pushed.**

---

## Anti-Patterns (DO NOT)

- ❌ Copy prompts between files — reference/import instead.
- ❌ Create prompts without testing in a real session first.
- ❌ Skip version bumps when modifying prompt content.
- ❌ Duplicate prompts already in `.claude/commands/` or `.agent/workflows/`.


---

## Operational Memory

Daily logs khi làm việc trên repo này được lưu tại:

```
../ios-memory/platform/master_prompt/memory/4-operational/daily/
```

- **Đầu session:** Đọc daily gần nhất + `../ios-memory/portfolio/decisions/DECISIONS.md`
- **Cuối session:** Ghi daily mới tại path trên
- **Memory hub:** `../ios-memory/SITE.md`

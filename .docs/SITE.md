# Tooling map — `master_prompt`

**Owner:** Quoc Nguyen Van  
**Last verified:** 2026-04-02 · `HEAD` in this repo (refresh with `git rev-parse HEAD`)

## Responsibility

| Area | Role |
|------|------|
| Prompt library | Versioned prompts “as code” for agents and workflows |
| Packs | `prompts/agents/`, `prompts/skills/`, `prompts/workflows/`, `prompts/experiments/` |
| Meta | `docs/`, `.templates/PROMPT_TEMPLATE.md`, `inboxes/` (raw logs — low signal for agents) |

## Key paths / artifacts

| Path | Purpose |
|------|---------|
| `prompts/agents/` | Personas / system prompts |
| `prompts/skills/` | Task-sized prompt fragments |
| `prompts/workflows/` | Chained automation |
| `prompts/experiments/` | A/B / sandbox |
| `docs/` | Human guidelines & meta |
| `.templates/PROMPT_TEMPLATE.md` | New prompt scaffold |

## Link canon

Moboco portfolio doc standard (tiers, drift, L0-T): sibling or clone **`ios-knowledge`** → `docs/moboco-portfolio-dot-docs-standard.md`.

## Reading order

1. This `SITE.md`  
2. Root `README.md` (repo layout summary)  
3. `docs/` for deep guidelines  

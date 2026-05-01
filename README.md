# 🧠 Exocortex Agentic OS: Prompt Routing & Skill Database

Welcome to the **Master Prompt Library** — the centralized "Brain & Skill Routing Layer" of the **BKPlus Exocortex Agentic OS**. 

This repository serves as a version-controlled prompt engineering and routing database. It ensures consistent, high-precision AI Agent behavior across our entire 13-repository workspace, acting as the primary skill provider for AI IDEs (Cursor, VSCode) and terminal interfaces (Gemini CLI, Claude Code).

## 🚀 Architecture Context

Our Agentic OS operates within a massive `knowledge.code-workspace`, autonomously managing an entire multi-platform iOS app portfolio. This prompt library is specifically designed to feed AI orchestrators with immense context.

- **Unified Intelligence:** Provides meta-prompts, specialist personas, and workflow standard operating procedures (SOPs) to autonomous AI agents.
- **Massive Context Integration:** Built to leverage large context window models (up to 1M tokens, such as MiMo-v2.5-pro). Agents actively use this repository to ingest architectural rules before executing massive codebase refactoring across 13 concurrent production projects.
- **Agent Map:** Refer to [`.docs/SITE.md`](.docs/SITE.md) for agent responsibilities, execution paths, and deep integration with the Moboco portfolio canon (`ios-hub` and `ios-memory`).

## 🗺 Repository Structure

Every prompt in this repository is strictly managed using a **Prompt-as-Code** philosophy, complete with mandatory Versioning and YAML Metadata.

Core components include:
*   **`prompts/meta/`**: Meta-prompts used to generate sub-prompters, digital twins, and interactive agent structures.
*   **`prompts/roles/`**: Specialist Personas (e.g., Lead Systems Architect, Mobile Performance Expert, Code Reviewer).
*   **`prompts/workflows/`**: Step-by-step SOPs, Research Pipelines, and internal CI/CD logic flows.
*   **`prompts/tasks/`**: Highly specific, single-shot execution tasks.
*   **`prompts/guidelines/`**: Global rules, tone of voice, and AI-friendly formatting standards.
*   **`prompts/components/`**: Reusable context blocks (e.g., Agency Context Loaders).
*   **`inboxes/`**: Raw agent logs, CSV data, and Archive buffers.
*   **`docs/`**: Master guidelines, architectural definitions, and metadata mapping.

## ⚙️ Contribution & Agent Rules

All autonomous agents and human engineers must adhere to the standardized YAML Metadata format defined in `AGENTS.md` (Version 1.1) to maintain absolute consistency.

To integrate with our Obsidian PKM workflow and persistent memory ecosystem, refer to `prompts/guidelines/obsidian-prompt-guide.md`.

# Changelog

All notable changes to the `master_prompt` library will be documented in this file.

## [2026-04-10] - Prompt Library V2 Migration & Standardization

### Added
- **Obsidian Integration:** Added `obsidian-prompt-guide.md` in `prompts/guidelines/` for native Templater/Dataview workflow.
- **Mentorship Prompts:** Added `solopreneur-mentor`, `sme-owner-mentor`, `marketing-executive-mentor`, `freelancer-mentor` to `prompts/roles/`.
- **Specialist Roles:** Added `seo-specialist`, `performance-marketing-specialist`, `social-media-strategist`, `content-marketing-manager`, `notion-style-illustrator` to `prompts/roles/`.
- **Tasks & Contexts:** Added `social-campaign-30day`, `paid-ads-campaign`, `image-architect`, `marketing-campaign-generator` to `prompts/tasks/`. Added `context-wave-agency` to `prompts/components/`.
- **Tone Guidelines:** Added 4 tone formats (`thought-leader`, `storytelling`, `casual`, `corporate`) into `prompts/guidelines/`.

### Changed
- **YAML Frontmatter:** Enforced standard YAML metadata version "1.1" on all 33 migrated files (name, category, version, tags).
- **Directory Hierarchy:** Re-architected core library structure to use `meta/`, `roles/`, `workflows/`, `tasks/`, `guidelines/`, and `components/`.
- **Catalog Update:** Refreshed `prompts/catalog.md` to reflect all new Marketing, Mentorship, and Creative Design agents.

### Removed
- **Legacy Files:** Cleaned up unused variations of AI command guides, Notion formatting templates, and multi-stage SOPs to prevent context collision in Swarm workflows.

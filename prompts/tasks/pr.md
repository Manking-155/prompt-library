---
description: Create a pull request
argument-hint: [to-branch] [from-branch]
version: "1.0.0"
category: Tasks
target: universal
tags: []
created: 2026-04-10
updated: 2026-04-10
changelog:
  - "1.0.0: MIGRATION - Metadata standardized"
---
## Variables

TO_BRANCH: $1 (defaults to `main`)
FROM_BRANCH: $2 (defaults to current branch)

## Workflow
- Use `gh` command to create a pull request from {FROM_BRANCH} to {TO_BRANCH} branch.

## Notes
- If `gh` command is not available, instruct the user to install and authorize GitHub CLI first.
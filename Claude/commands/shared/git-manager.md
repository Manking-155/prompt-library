 # Git Manager (Shared)
 
 Purpose: Handle commits, branches, and PRs cleanly without AI attribution spam.
 
 CHECKLIST:
 - Review changes: git status; git diff; git diff --cached
 - Scan for secrets before commit (env, keys)
 - Commit style: type(scope): summary; focus on why; max 72 chars
 - Link issues in PR; include checklist and risks
 
 WORKFLOW:
 1) Branch: feat|fix|chore/<slug>
 2) Stage selective changes; avoid noisy files
 3) Commit message (Conventional):
    - feat: new feature
    - fix: bug fix
    - docs|chore|refactor|perf|test
 4) Create PR: summary, change list, test evidence, rollout plan
 5) Address review; squash/merge per repo policy
 
 OUTPUT:
 - Proposed commit message
 - PR description with checklist and test results
 

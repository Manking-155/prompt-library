---
name: beads-optimizer
version: "1.0"
category: planning
target: universal
tags: [beads, optimization, deduplication, testing, planning]
created: 2026-04-13
updated: 2026-04-13
changelog:
  - "1.0: Initial version for beads plan-space optimization."
---

> 📖 **Flywheel Playbook Reference:** 
> Before executing this workflow, ensure you align with the strategies defined in the [Universal Flywheel Playbook](/Users/djv033/Downloads/iOS_Post/ios-memory/docs/playbooks/universal-flywheel-playbook.md)

# Beads Lifecycle & Plan-Space Optimizer

## Phase 1: Critical Verification & Unit Testing Injection
Reread `AGENTS.md` so it's still fresh in your mind. Check over each bead super carefully-- are you sure it makes sense? Is it optimal? Could we change anything to make the system work better for users? If so, revise the beads. It's a lot easier and faster to operate in "plan space" before we start implementing these things!

DO NOT OVERSIMPLIFY THINGS! DO NOT LOSE ANY FEATURES OR FUNCTIONALITY!

Also, make sure that as part of these beads, we include comprehensive unit tests and e2e test scripts with great, detailed logging so we can be sure that everything is working perfectly after implementation. Remember to ONLY use the `br` tool to create and modify the beads and to add the dependencies to beads. Use ultrathink.

## Phase 2: System Validation post-Markdown Translation
We recently transformed a markdown plan file into a bunch of new beads. I want you to very carefully review and analyze these using `br` and `bv`. Check over each bead super carefully-- are you sure it makes sense? Is it optimal? Could we change anything to make the system work better for users? If so, revise the beads. It's a lot easier and faster to operate in "plan space" before we start implementing these things! Use ultrathink.

## Phase 3: Deduplication & Canonicalization
Reread `AGENTS.md` so it's still fresh in your mind. Check over ALL open beads. Make sure none of them are duplicative or excessively overlapping... try to intelligently and cleverly merge them into single canonical beads that best exemplify the strengths of each.

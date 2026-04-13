---
name: investigation
version: "1.0"
category: brainstorm
target: universal
tags: [greenfield, brownfield, ideation, improvement, planning, evaluation]
created: 2026-04-13
updated: 2026-04-13
changelog:
  - "1.0: Initial version mapping investigation prompts across greenfield and brownfield axes"
---

> 📖 **Flywheel Playbook Reference:** 
> Before executing this workflow, ensure you align with the strategies defined in the [Universal Flywheel Playbook](/Users/djv033/Downloads/iOS_Post/ios-memory/docs/playbooks/universal-flywheel-playbook.md)

# Deep Investigation & Ideation Generator

Come up with your very best ideas for {INVESTIGATION_GOAL}.

First generate a list of 30 ideas (brief one-liner for each).

Then go through each one systematically and critically evaluate it, rejecting the ones that are not excellent choices for good reasons and keeping the ones that pass your scrutiny.

Then, for each idea that passed your test, explain in detail exactly what the idea is (in the form of a concrete, specific, actionable plan with detailed code snippets where relevant), why it would be a good improvement, what are the possible downsides, and how confident you are that it actually improves the project (0-100%). Make sure to actually implement the top ideas now.

## 🎯 Variables

### `{INVESTIGATION_GOAL}` 
Choose the phrase that fits your current project state (Greenfield vs. Brownfield) and focus area:

#### 🟩 Greenfield Focus (New Projects, Initial Scope, Feature Expansion)
*   **New Features:** `new features for this project`
*   **Initial Documentation/Specs:** `improving this document`
*   **Architecture/Implementation Plans:** `improving this plan`

#### 🟫 Brownfield Focus (Existing Projects, Technical Debt, Workflows)
*   **General Project Improvement:** `improving this project`
*   **Core Systems Optimization:** `improving the core of the project (skills, commands…)`
*   **Legacy Process Refinement:** `my workflow - “Tạo lại file cập nhật quy trình phát triển phần mềm phù hợp nhất với tôi”`

## 💡 Usage Notes
This prompt is heavily designed to force the AI out of its "first-idea bias" by requiring it to generate a large volume of ideas (30) before applying critical thinking filters. This ensures only the most high-value, actionable, and rigorously evaluated plans are returned and implemented.

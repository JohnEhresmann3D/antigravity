---
description: Atlas Project Manager workflow - planning and review
---

# Atlas PM Workflow

This workflow guides the **Project Manager (PM)** role through planning and review activities.

## Role Constraints

The PM:
- Defines WHAT is being built and WHY
- Creates product specs and task plans
- Reviews execution and issues verdicts
- **DOES NOT** write code or propose implementations

## Workflow Steps

### 1. Create Product Specification

When starting new work:

1. Copy the product spec template:
   ```powershell
   Copy-Item docs/specs/product-spec-template.txt docs/specs/SPEC-[DATE]-[NAME].txt
   ```

2. Fill out all sections:
   - Problem statement
   - Goals and non-goals
   - Functional requirements (MUST/SHOULD/MAY)
   - Constraints
   - Success criteria
   - Open questions

3. Save the spec in `docs/specs/`

### 2. Create Task Plan

Once the spec is complete:

1. Copy the task plan template:
   ```powershell
   Copy-Item artifacts/pm/task-plan-template.txt artifacts/pm/PLAN-[DATE]-[NAME].txt
   ```

2. Break down work into small tasks:
   - Prefer micro/small task sizes
   - Maximum 12 tasks unless requested
   - Define dependencies
   - Set acceptance criteria
   - Define verification steps

3. Identify the next task to execute

4. Save the plan in `artifacts/pm/`

### 3. Hand Off to Engineer

Once the task plan is approved:

1. Inform the engineer which task to execute
2. Reference the task plan ID
3. Ensure all constraints are clear

### 4. Review Execution

After the engineer completes work:

1. Copy the reasoning review template:
   ```powershell
   Copy-Item artifacts/reviews/reasoning-review-template.txt artifacts/reviews/REVIEW-[DATE]-[NAME].txt
   ```

2. Review the execution report:
   - Was evidence sufficient?
   - Does execution match the plan?
   - Were constraints respected?
   - Are acceptance criteria met?
   - Are verification results acceptable?

3. Assess risks and assumptions

4. Issue verdict:
   - **PROCEED** - Move to next task
   - **BLOCKED** - List blocking issues
   - **NEEDS CLARIFICATION** - List questions

5. Save the review in `artifacts/reviews/`

## Stop Conditions

The PM must halt if:
- Required documentation is missing
- Constraints are ambiguous
- Requirements conflict
- Execution would require assumptions

**Stopping is correct behavior.**

## Key Principles

- Documentation is authoritative, chat is not
- Block rather than guess
- Keep scope intentionally small
- Alignment matters more than speed

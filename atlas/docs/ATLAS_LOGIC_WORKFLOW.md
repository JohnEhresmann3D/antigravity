# Atlas Logic Workflow (Authoritative)

This workflow is mandatory for any non-trivial task involving code, scripts,
planning, or tooling.

---

## 0) Clarify the Objective
- Restate the goal in one sentence.
- Define success criteria that are observable or testable.

---

## 1) Gather Evidence (No Guessing)
- Inspect existing code using read/search tools.
- Identify constraints, conventions, and patterns.
- Separate facts, unknowns, and assumptions.

Rules:
- If it wasn’t read or verified, it’s an assumption.
- Prefer inspecting both call sites and implementations.

---

## 2) Form a Hypothesis
- State what is likely needed or wrong.
- Explain why this hypothesis fits the evidence.
- Provide at least one alternative hypothesis for non-trivial work.

---

## 3) Plan the Work (Project Management Required)
Break the task into a small, actionable mini-backlog:
- Milestones
- Small tasks (micro/small preferred)
- Dependencies
- Acceptance criteria
- Verification steps

Rules:
- Do not over-plan (≤12 tasks unless requested).
- Always identify the next task to execute.

---

## 4) Pre-Flight Safety & Scope Check
Before writing code or running commands:
- Ensure all paths are within workspace.
- Ensure no secrets or credentials are introduced.
- Ensure commands are allowlisted and non-destructive.
- Ensure scope matches the plan.

If risk is detected:
- Stop.
- Explain the risk.
- Propose a safer alternative.

---

## 5) Apply Changes (Patch Discipline)
- All edits must be patch-based.
- One intention per patch.
- Keep diffs small and reviewable.
- No drive-by refactors.

---

## 6) Verification (Required)
After code changes:
- Run relevant checks (tests/build/execution).
- If checks fail, fix or rollback.
- Do not declare success without verification unless explicitly approved.

---

## 7) Double-Check (Independent Review)
- Review reasoning and evidence.
- Ensure acceptance criteria are met.
- High-risk findings must be mitigated before completion.

---

## 8) Report
End with:
- What changed
- Why it works
- What was verified
- Remaining risks or next steps

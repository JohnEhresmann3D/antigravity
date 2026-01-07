# Atlas Integration Guide

## Overview

This Godot project uses the **Atlas** framework for AI-assisted development. Atlas is a documentation-first, constraint-driven collaboration system that enforces strict role separation and auditable workflows.

## Core Principles

1. **Documentation is authoritative** - Chat history is volatile
2. **Roles are constrained** - PM plans, Engineer executes, Docs renders
3. **Stop when unclear** - Blocking is correct behavior
4. **Evidence over assumptions** - If it wasn't verified, it's an assumption
5. **Minimal changes** - Smallest change that solves the problem

## Directory Structure

```
d:/GameDevelopment/Godot/Games/antigravity/
├── atlas/                  # Atlas framework documentation (imported)
│   ├── README.md          # Framework overview
│   └── docs/              # Authoritative rules
│       ├── ATLAS_LOGIC_WORKFLOW.md
│       ├── ATLAS_ENGINEERING_RULES.md
│       ├── ATLAS_PM_RULES.md
│       └── AI_CONTEXT.md
├── artifacts/              # All non-code outputs (evidence, not authority)
│   ├── pm/                # PM task plans and spec snapshots
│   ├── eng/               # Engineer execution reports and logs
│   ├── reviews/           # Reasoning reviews and verdicts
│   ├── docs/              # Rendered documentation
│   └── decisions/         # Durable decision logs
├── docs/
│   └── specs/             # Product specifications (authoritative)
└── .agent/
    └── workflows/         # Agent-specific workflows
        ├── atlas-pm.md    # PM workflow
        └── atlas-eng.md   # Engineer workflow
```

## Roles

### Project Manager (PM) - Product Owner

**Responsibilities:**
- Defines WHAT is being built and WHY
- Creates product specifications
- Creates task plans
- Reviews execution and issues verdicts

**Prohibitions:**
- Does NOT write code
- Does NOT propose implementations
- Does NOT fill in gaps by guessing

**Workflow:** `/atlas-pm`

### Engineer (ENG) - Code Owner

**Responsibilities:**
- Executes PM-approved task plans
- Gathers evidence before making changes
- Produces code and execution reports
- Runs verification checks

**Prohibitions:**
- Does NOT infer requirements
- Does NOT modify specs
- Does NOT proceed without a plan

**Workflow:** `/atlas-eng`

## Quick Start

### Starting New Work

1. **Create a Product Spec** (PM Role)
   ```powershell
   Copy-Item docs/specs/product-spec-template.txt docs/specs/SPEC-2026-01-06-[NAME].txt
   # Edit the spec with your requirements
   ```

2. **Create a Task Plan** (PM Role)
   ```powershell
   Copy-Item artifacts/pm/task-plan-template.txt artifacts/pm/PLAN-2026-01-06-[NAME].txt
   # Break down work into small tasks
   ```

3. **Execute Tasks** (Engineer Role)
   - Follow the `/atlas-eng` workflow
   - Gather evidence first
   - Make minimal changes
   - Verify everything
   - Create execution report

4. **Review Execution** (PM Role)
   ```powershell
   Copy-Item artifacts/reviews/reasoning-review-template.txt artifacts/reviews/REVIEW-2026-01-06-[NAME].txt
   # Review execution and issue verdict
   ```

## Authority Chain

```
Product Spec (authoritative)
    ↓
PM Task Plan (authoritative)
    ↓
Engineer Execution (facts)
    ↓
Documentation Renderer (presentation only)
    ↓
Non-authoritative docs
```

**If documents conflict, the highest artifact in the chain wins.**

## Common Commands

### Using Workflows

- `/atlas-pm` - Run Project Manager workflow
- `/atlas-eng` - Run Engineer workflow

### Creating Artifacts

```powershell
# Product Spec
Copy-Item docs/specs/product-spec-template.txt docs/specs/SPEC-[DATE]-[NAME].txt

# Task Plan
Copy-Item artifacts/pm/task-plan-template.txt artifacts/pm/PLAN-[DATE]-[NAME].txt

# Execution Report
Copy-Item artifacts/eng/execution-report-template.txt artifacts/eng/ENG-[DATE]-[NAME].txt

# Reasoning Review
Copy-Item artifacts/reviews/reasoning-review-template.txt artifacts/reviews/REVIEW-[DATE]-[NAME].txt
```

## Stop Conditions

Atlas **must halt** if:
- Required documentation is missing
- Constraints are ambiguous or violated
- A PM task plan does not exist
- Role rules are violated
- Execution would require assumptions
- Security risks are detected

**Stopping is correct behavior.**

## Memory Model

- Chat history is **non-authoritative**
- Atlas retains memory **only** through repository artifacts
- If it isn't written down, it doesn't exist

## Getting Help

1. **Read the authoritative docs** in `atlas/docs/`
2. **Use the templates** in `docs/specs/` and `artifacts/`
3. **Follow the workflows** in `.agent/workflows/`
4. **When in doubt, stop and ask**

## Key Reminders

- **PM**: Define the problem, not the solution
- **Engineer**: Gather evidence, don't guess
- **Both**: Keep scope small, verify everything
- **Always**: Documentation over chat, blocking over guessing

---

*Atlas operates like a junior engineer on a disciplined team. Correctness and alignment matter more than speed.*

# IBVAP — Intelligent Border Video Analytics Platform

Smart India Hackathon 2026. Problem Statement ID: 26187.

## 1. Project Purpose

Build IBVAP according to the exact SIH problem statement recorded in
[docs/problem-statement.md](docs/problem-statement.md).

The goal is an AI-driven software platform that transforms existing IP-based CCTV
infrastructure at Border Out Posts (BOPs), check posts, and border roads into an
intelligent surveillance network — without requiring dedicated FRS, ANPR, or
smart-camera hardware — by performing real-time video analytics using AI and
computer vision.

## 2. Where work happens

Discovery and delivery run continuously and in parallel, governed by
**which of four homes a piece of work belongs in** — decided by one
question: *does this change when the code changes?*

| Home | Holds | Because |
|---|---|---|
| **This repo** | Code, ADRs, architecture, RFCs, CI, contributing rules | Changes with the code |
| **[Notion](https://app.notion.com/p/3c986dda46e28132a92fef10b9d75132?pvs=204)** | Vision & Scope, PRD, research | Product and discovery, stable across code changes |
| **[Figma](https://www.figma.com/files/team/1549054683813925758/project/645637828?fuid=1549054681745812988)** | Screen flow, wireframes, UI kit | The design itself |
| **GitHub Issues** | Tasks, bugs | Work items to track |

Each artifact has exactly one home — never mirrored across two. The
rationale is recorded as an ADR in [docs/adr/](docs/adr/README.md); see
[CONTRIBUTING.md](CONTRIBUTING.md) for how work moves through the repo
(branching, PRs, Definition of Ready/Done).

Within the repo: an **ADR** ([docs/adr/](docs/adr/README.md)) records a
decision already made; an **RFC** ([docs/rfcs/](docs/rfcs/README.md))
proposes a non-trivial implementation, reviewed before code.

## 3. Rules

1. The official SIH problem statement in
   [docs/problem-statement.md](docs/problem-statement.md) is immutable. Do not
   rewrite, simplify, reinterpret, remove, or add to it.
2. Do not invent requirements. Every product feature must trace back to the
   official problem statement.
3. Do not make major technical decisions before research (Notion) supports
   them.
4. Each artifact has exactly one home — repo, Notion, Figma, or GitHub
   Issues (§2). Don't restate or mirror one in another; link to it instead.
5. Preserve the existing CCTV access/testing setup, under `src/dvr/`
   (`dvr.py`, `dvr.env`, `backups/`, `requirements.txt`). These belong to the
   developer's home CCTV setup used for development and testing. Do not
   modify, replace, refactor, or delete their contents.

## 4. Where the project is

[ROADMAP.md](ROADMAP.md) holds the phase-by-phase status — per §3 rule 4,
it is not duplicated here. Phases 1–3 are done; Phase 4 (writing GitHub task
issues) is unblocked but not yet started. Every issue's Definition of Ready
traces to the [System Design Document](docs/architecture/system-design/README.md),
an ADR, or a PRD requirement, per [CONTRIBUTING.md](CONTRIBUTING.md).

One thing is genuinely open, tracked in the System Design Document's
[Risks and Open Items](docs/architecture/system-design/10-risks-and-open-items.md):
the detailed sequence/state diagrams still owed.

## 5. AI Engineering & Coding Standards

Act as a Principal Software Engineer. Adhere to the following industry-standard
practices, derived from Google, Microsoft, and Airbnb style guides, for every
line of implementation code written in this repository (Phase 5 onward).

### 5.1 Architectural boundaries & modularity

- **Single Responsibility Principle.** Each file, class, and function has
  exactly one reason to change.
- **Strict layering.** Never mix HTTP/API routing logic with business logic
  or database queries. Keep layers isolated: `types/` (data shapes and
  interfaces), `db/` or `repositories/` (database interactions only),
  `services/` (core business logic), `controllers/` or `routes/`
  (HTTP/input handling).
- **Size limits.** Target 150–250 lines per file; treat 300 as a hard limit.
  Break larger files into smaller, composable modules. Keep functions under
  30 lines.

### 5.2 Code clarity & simplicity

- **Clarity over cleverness.** Write code that is easy to read, not just easy
  to write. Avoid dense one-liners, complex ternary chains, or nested loops.
- **KISS, DRY, YAGNI.** Extract duplicated logic into shared utilities, but do
  not build speculative abstractions for features that don't exist yet in the
  accepted RFCs.
- **Guard clauses first.** Use early returns to handle invalid states,
  permissions, or missing data at the top of a function. Don't nest
  `if`/`else` logic deeper than two levels.

### 5.3 Defensive programming & error handling

- **Never swallow errors.** No empty `except`/`catch` blocks. Handle, log, or
  escalate every error explicitly.
- **Fail fast.** Validate inputs and fail as early in the execution path as
  possible, rather than let corrupted state propagate.
- **Explicit typing.** No `Any`/`any`, no untyped dicts, no `unknown` without
  a narrowing check. Define exhaustive types for every parameter and return
  value — Pydantic models on the backend, TypeScript interfaces on the
  frontend, matching what the accepted RFCs already specify.

### 5.4 Naming conventions

- **Descriptive over short.** A name states its exact purpose —
  `fetch_active_user_profile()`, not `get_data()`.
- **Boolean naming.** Prefix with `is`, `has`, `should`, or `can` (e.g.
  `is_valid`, `has_permission`).
- **Casing follows the language, not one convention repo-wide** — this
  project has both a Python backend and a TypeScript frontend, and the
  accepted RFCs already fix which is which:
  - **Python** (backend, per [ADR 0033](docs/adr/0033-backend-framework-packaging-and-auth.md)):
    `snake_case` for variables, functions and module names — PEP 8 — matching
    every dataclass and Pydantic model already in RFCs 0001–0006;
    `PascalCase` for classes; `UPPER_SNAKE_CASE` for module-level constants.
  - **TypeScript** (frontend, per [ADR 0035](docs/adr/0035-operator-console-stack-and-video-transport.md)):
    `camelCase` for variables, functions and object properties; `PascalCase`
    for components, classes, interfaces and types; `UPPER_SNAKE_CASE` for
    global constants and environment variables.

### 5.5 Execution protocol

Before generating implementation code:

1. Outline the file structure being modified or created.
2. Verify the planned files won't exceed the 300-line limit (§5.1).
3. State the layered architectural approach being followed.
4. Output the code file-by-file.

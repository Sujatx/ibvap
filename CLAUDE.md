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

Discovery and delivery run continuously and in parallel — there is no
research → product → design → architecture → engineering waterfall. What
governs a piece of work is not which stage it's "in", but **which of four
homes it belongs in**, decided by one question: *does this change when the
code changes?*

| Home | Holds | Because |
|---|---|---|
| **This repo** | Code, ADRs, architecture, RFCs, CI, contributing rules | Changes with the code |
| **[Notion](https://app.notion.com/p/3c986dda46e28132a92fef10b9d75132?pvs=204)** | Vision & Scope, PRD, research | Product/discovery — doesn't change with the code |
| **[Figma](https://www.figma.com/files/team/1549054683813925758/project/645637828?fuid=1549054681745812988)** | Screen flow, wireframes, UI kit | *Is* the design, not a description of it |
| **GitHub Issues** | Tasks, bugs | Work, not a document |

Each artifact has exactly one home — never mirrored across two. The
rationale is recorded as an ADR in [docs/adr/](docs/adr/README.md); see
[CONTRIBUTING.md](CONTRIBUTING.md) for how work moves through the repo
(branching, PRs, Definition of Ready/Done).

Within the repo: an **ADR** ([docs/adr/](docs/adr/README.md)) records a
decision already made; an **RFC** ([docs/rfcs/](docs/rfcs/README.md))
proposes a non-trivial implementation not yet decided, reviewed before code.

## 3. Rules

1. The official SIH problem statement in
   [docs/problem-statement.md](docs/problem-statement.md) is immutable. Do not
   rewrite, simplify, reinterpret, remove, or add to it.
2. Do not invent requirements. Every product feature must trace back to the
   official problem statement.
3. Do not implement product features before they are defined in the
   [Notion PRD](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204).
4. Do not make major technical decisions before research (Notion) supports
   them.
5. Each artifact has exactly one home — repo, Notion, Figma, or GitHub
   Issues (§2). Don't restate or mirror one in another; link to it instead.
6. Preserve the existing CCTV access/testing setup (`dvr.py`, `dvr.env`,
   `backups/`, `requirements.txt`). These belong to the developer's home CCTV
   setup used for development and testing. Do not modify, replace, refactor, or
   delete them.
7. In every research/product/design/architecture document, make clear which
   claims are verifiable/sourced fact, which are unverified assumptions, and
   which are hypotheses still to be tested — through plain, naturally hedged
   wording (e.g. "is inferred from...", "not independently verified",
   "plausibly"), not repeated inline labels or a legend. A **DECISION** is
   different: it is a choice actually made, and must be recorded as its own
   file in [docs/adr/](docs/adr/README.md), one file per decision, numbered
   sequentially, in the standard ADR (Nygard/MADR) format — `Status`,
   `Context`, `Decision`, `Consequences`. Never appended to a running log,
   never split by which stage was active when the decision was made; a
   change of mind is a new numbered file that supersedes the old one, not an
   edit to it. A non-trivial implementation not yet decided gets an RFC in
   [docs/rfcs/](docs/rfcs/README.md) first, reviewed before code — see
   [CONTRIBUTING.md](CONTRIBUTING.md).
8. Any document of more than a few sections opens with a short, positive
   statement of what it is and records — not a paragraph or blockquote of
   what it is not or does not do — followed by a `## Contents` list linking
   to its top-level headings. State a genuine scope boundary once, in plain
   prose, where it matters; don't restate it as a standalone disclaimer.
9. Every code change traces to a GitHub issue. Branch names are
   `<type>/<issue#>-<slug>` (e.g. `feat/42-live-view-detection-overlay`); PRs
   stay under ~400 lines changed. See [CONTRIBUTING.md](CONTRIBUTING.md).

## 4. Open before engineering starts

Design and architecture/engineering-design work is not finished. Do not
write implementation-ready GitHub issues (the task-level part of step 5)
until this list clears — check it back in on return.

- **Figma UI kit not built.** The design file has only `01 Wireframes` — no
  `02 UI Kit` page exists: no variables, no components, no type system, no
  foundations doc. **Includes picking a real colour palette** — nothing
  beyond "dark-first, Night default" has been decided.
- **Wireframes haven't been reviewed.** Review the 5 screens on
  `01 Wireframes` before treating them as locked.
- **[RFC 0001](docs/rfcs/0001-video-ingest-and-analytics-pipeline.md) is
  still Draft.** Review it and accept or send back for revision — ingest/
  capability-measurement tasks aren't "ready" (per CONTRIBUTING.md) until
  it is.
- **RFCs still missing** for the rule engine, event store, web
  application/API, and egress publisher.
- **[docs/architecture/README.md](docs/architecture/README.md) §4–7**
  (Solution Strategy, Building Block View, Runtime View, Deployment View)
  stay "Not yet decided" until the RFCs above land.
- Then: Step 6 (ADR recording the four-homes split) and the rest of Step 5
  (GitHub Issues — labels and milestones now; task issues, seeded from the
  PRD's acceptance criteria, only once the above clears).

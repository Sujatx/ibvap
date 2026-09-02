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
   `<type>/<issue#>-<slug>` (e.g. `feat/42-live-view-detection-overlay`);  See [CONTRIBUTING.md](CONTRIBUTING.md).

## 4. Where the project is

[ROADMAP.md](ROADMAP.md) is the order of work — five phases, of which Phase 1
(the technology stack) is done. It supersedes the ordering this section used
to carry. What is open, at the time of writing:

- **Phase 2 — Task 1 is done; `03 Hi-fi` has not started.** `01 Wireframes`
  holds 37 frames across five screens and a shell section, at 1440 and 1280,
  every state either drawn or annotated and proved on the State matrix board
  ([ADR 0039](docs/adr/0039-state-coverage-evidenced-three-ways.md)); the
  focused-camera view carries the historical timeline
  ([ADR 0038](docs/adr/0038-historical-timeline-on-the-focused-camera-view.md)).
  `02 UI Kit` is built (three variable collections, nine text styles, close to
  forty components; palette settled in [ADR 0030](docs/adr/0030-dark-console-palette-no-severity-colour.md),
  control grammar in [ADR 0031](docs/adr/0031-component-grammar-chip-states-fact-segmented-control-chooses.md)),
  but its `Kit gaps` board lists fifteen components missing outright, six
  needing new variants and two needing changes. Building those is the first
  work of Task 2. `03 Hi-fi` is empty.
- **Phase 3 — no RFC exists yet.** All five are still to be written: ingest and
  analytics pipeline, rule engine, event store and alert state, web
  application and API contracts, egress publisher.
  [docs/architecture/README.md](docs/architecture/README.md) §4–7 stay "not yet
  decided" until they land.
- **Phase 4 — no task issues.** Do not write implementation-ready GitHub issues
  until Phase 3 clears; a task isn't "ready" (per
  [CONTRIBUTING.md](CONTRIBUTING.md)) while the capability it depends on has no
  accepted RFC. Labels and milestones can be created now.
- **Still owed: an ADR recording the four-homes split** described in §2.

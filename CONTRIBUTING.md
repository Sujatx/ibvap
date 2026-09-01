# Contributing to IBVAP

This is how work moves through this repository — branching, review, and the
bar an issue has to clear before and after it's built. Product and design
work is not done here; see the [README](README.md) for where each artifact
actually lives.

## Contents

- [Where things live](#where-things-live)
- [Branching](#branching)
- [Pull requests](#pull-requests)
- [Definition of Ready](#definition-of-ready)
- [Definition of Done](#definition-of-done)
- [Decisions and design docs](#decisions-and-design-docs)

## Where things live

Four homes, decided by one question — does this change when the code
changes?

| Home | Holds | Question |
|---|---|---|
| **This repo** | Code, ADRs, architecture, RFCs, CI, this file | Changes with the code |
| **[Notion](https://app.notion.com/p/3c986dda46e28132a92fef10b9d75132?pvs=204)** | [Vision & Scope](https://app.notion.com/p/3c986dda46e281269e61cedb44f3eb3e?pvs=204), [PRD](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204), [research](https://app.notion.com/p/3c986dda46e281b1af56fe54bfbe813d?pvs=204) | Product/discovery — doesn't change with the code |
| **[Figma](https://www.figma.com/files/team/1549054683813925758/project/645637828?fuid=1549054681745812988)** | [Screen flow](https://www.figma.com/board/IyOcjBnBVh3ID2uxmrxRdT/IBVAP-%E2%80%94-Screen-Flow?t=crzSM6HZroTo7LFV-6), [wireframes, UI kit](https://www.figma.com/design/ZDrrYveQkuzTFD9VufbQZO/IBVAP-%E2%80%94-Product-Design?m=auto&t=crzSM6HZroTo7LFV-6) | *Is* the design, not a description of it |
| **GitHub Issues** | Tasks, bugs | Work, not a document |

Each artifact has exactly one home — no mirroring. The rationale is recorded
as an ADR in [docs/adr/](docs/adr/README.md).

## Branching

`<type>/<issue#>-<slug>`, e.g. `feat/42-live-view-detection-overlay`.

| Type | For |
|---|---|
| `feat` | New product-facing capability |
| `fix` | Bug fix |
| `chore` | Non-product-facing change (tooling, structure, docs) |
| `spike` | Time-boxed investigation, may not ship code |

Every branch traces to a GitHub issue. If there isn't one yet, open it first.

## Pull requests

- Split larger work into a stack rather
  than opening one large PR.
- Link the issue it closes (`Closes #NNNN`).
- Fill in the PR template — it asks for the same information reviewers
  always need first.
- A PR implementing something non-trivial links the RFC it follows.

## Definition of Ready

A task is ready to pick up when:

- It traces to a specific PRD clause or ADR (not invented — see
  [CLAUDE.md](CLAUDE.md) rule 2).
- Acceptance criteria are written on the issue.
- Any capability it depends on (a rule engine, an ingest pipeline) either
  exists or has an accepted RFC.

## Definition of Done

- Acceptance criteria on the issue are met.
- Tests exist for the behaviour described in the issue.
- CI is green.
- Docs that describe *how the code works* are updated in the same PR
  (architecture, RFC status, this file) — docs that describe *what the
  product does* are updated in
  [Notion](https://app.notion.com/p/3c986dda46e28132a92fef10b9d75132?pvs=204)/[Figma](https://www.figma.com/files/team/1549054683813925758/project/645637828?fuid=1549054681745812988)
  separately, not here.
- The issue is closed by the merging PR, not manually beforehand.

## Decisions and design docs

- A **decision actually made** — a choice with a Context, a Decision, and
  Consequences — is an ADR: [docs/adr/](docs/adr/README.md).
- A **non-trivial implementation not yet decided** is worked out as an RFC,
  reviewed before code: [docs/rfcs/](docs/rfcs/README.md).
- Neither is a place to restate what the
  [PRD](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204) or
  [Figma](https://www.figma.com/files/team/1549054683813925758/project/645637828?fuid=1549054681745812988)
  already say — link to them instead of copying them.

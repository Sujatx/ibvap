# Contributing to IBVAP

This is how work moves through this repository — branching, review, and the
bar an issue has to clear before and after it's built. Product and design
work happens in Notion and Figma; see the [README](README.md) for where each
artifact lives.

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
| **[Notion](https://app.notion.com/p/3c986dda46e28132a92fef10b9d75132?pvs=204)** | [Vision & Scope](https://app.notion.com/p/3c986dda46e281269e61cedb44f3eb3e?pvs=204), [PRD](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204), [research](https://app.notion.com/p/3c986dda46e281b1af56fe54bfbe813d?pvs=204) | Product and discovery, stable across code changes |
| **[Figma](https://www.figma.com/files/team/1549054683813925758/project/645637828?fuid=1549054681745812988)** | [Screen flow](https://www.figma.com/board/IyOcjBnBVh3ID2uxmrxRdT/IBVAP-%E2%80%94-Screen-Flow?t=crzSM6HZroTo7LFV-6), [wireframes, UI kit](https://www.figma.com/design/ZDrrYveQkuzTFD9VufbQZO/IBVAP-%E2%80%94-Product-Design?m=auto&t=crzSM6HZroTo7LFV-6) | The design itself |
| **GitHub Issues** | Tasks, bugs | Work items to track |

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

## Definition of Ready

A task is ready to pick up when:

- It traces to the [System Design Document](docs/architecture/system-design/README.md),
  an ADR, or a PRD requirement (not invented — see
  [CLAUDE.md](CLAUDE.md) rule 2).
- Acceptance criteria are written on the issue.
- Any capability it depends on is specified in the System Design Document.

## Definition of Done

- Acceptance criteria on the issue are met.
- Tests exist for the behaviour described in the issue.
- CI is green.
- Docs that describe *how the code works* are updated in the same PR
  (architecture, this file). Docs that describe *what the
  product does* are updated separately, in
  [Notion](https://app.notion.com/p/3c986dda46e28132a92fef10b9d75132?pvs=204)/[Figma](https://www.figma.com/files/team/1549054683813925758/project/645637828?fuid=1549054681745812988).
- The merging PR closes the issue automatically.

## Decisions and design docs

- A **decision actually made** — a choice with a Context, a Decision, and
  Consequences — is an ADR: [docs/adr/](docs/adr/README.md).
- The accepted technical design lives in the
  [System Design Document](docs/architecture/system-design/README.md),
  synthesised from the six accepted RFCs in [docs/rfcs/](docs/rfcs/README.md).
- Neither is a place to restate what the
  [PRD](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204) or
  [Figma](https://www.figma.com/files/team/1549054683813925758/project/645637828?fuid=1549054681745812988)
  already say — link to them instead of copying them.

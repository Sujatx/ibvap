# 49. Four homes for project artefacts, decided by one question

**Date:** 2026-09-03
**Status:** Accepted

## Context

The project produces artefacts of very different kinds: a problem statement, a
PRD, research notes, a screen flow, a UI kit, hi-fi screens, architecture
decisions, design docs, code, CI configuration, and the tasks that turn all of it
into software. Early on these were all heading into the repository, on the
reasoning that one place is simpler than four.

That reasoning does not survive contact with what actually happens. A wireframe
committed as a PNG is stale the moment somebody moves a component in Figma, and
nobody notices until a developer builds the old one. A PRD section pasted into
`docs/` diverges from the Notion page it was copied from within a week, and then
two documents disagree with no way to tell which is current. A task list in a
markdown file is a task list nobody closes.

The failure in every case is the same: an artefact with two homes has no home.
Somebody has to keep them in sync, and that somebody is always busy.

[0001](0001-project-setup-and-documentation-structure.md) set up a `docs/` folder
per SDLC stage, which organised the repository by *when work happened* rather
than by *what changes with the code*.
[0029](0029-decision-log-restructured-as-one-adr-per-file.md) already retired part of that
scheme. [CLAUDE.md](../../CLAUDE.md) §2 and
[CONTRIBUTING.md](../../CONTRIBUTING.md) both describe the four-homes split as
current practice, and both point at `docs/adr/` for the rationale — which has not
existed until now. This ADR is that rationale.

## Decision

**Every artefact has exactly one home, and which home is decided by a single
question: does this change when the code changes?**

| Home | Holds | Because |
|---|---|---|
| This repository | Code, ADRs, architecture, RFCs, CI, contributing rules | Changes with the code |
| [Notion](https://app.notion.com/p/3c986dda46e28132a92fef10b9d75132?pvs=204) | Vision & Scope, PRD, research | Product and discovery — does not change with the code |
| [Figma](https://www.figma.com/files/team/1549054683813925758/project/645637828) | Screen flow, wireframes, UI kit, hi-fi screens | *Is* the design, not a description of one |
| GitHub Issues | Tasks, bugs | Work, not a document |

Three rules follow, and they are the operative part:

**Never mirror.** An artefact is not copied, summarised, or restated in a second
home. Where one needs another, it links.

**Link across, do not paste.** An ADR that depends on a PRD clause cites the
clause and does not reproduce its numbers. A wireframe is referenced by frame
name, not exported and committed.

**The home decides the format.** A decision is a numbered ADR file here; a
requirement is a PRD section in Notion; a screen is a frame in Figma; a piece of
work is an issue. An artefact that does not fit any of the four is a sign the
artefact is wrong, not that a fifth home is needed.

The single exception is `docs/problem-statement.md`, which lives in the
repository despite being product input, because it is immutable and external —
it is copied verbatim from SIH, never edited, and having it in the repo means
every rule that traces to it can link to a file rather than a login.

## Consequences

The obvious cost is that reading the project requires four accounts. That is
real, and it is the price of each artefact being current wherever it is read. The
alternative — one place, four stale copies — costs more, and costs it silently.

A second cost is that the repository cannot be self-contained. A reader who
cannot open the Figma file cannot see the screens, and an ADR that cites "PRD
§5.2" is opaque to them. This is accepted deliberately: a self-contained
repository is achievable only by copying, and copying is the failure this
decision exists to prevent.

The rule is enforceable by review rather than by tooling. A pull request that
adds a screenshot of a wireframe, restates a PRD requirement, or opens a
markdown task list is rejected on this ADR — which is why it needed to exist as
a citable decision rather than a paragraph in a contributing guide.

It also settles what *this* repository is for, which sharpens every later
question about where something belongs. Architecture, RFCs and ADRs are here
because they change when the code changes. Research is not here because it does
not. That test has been applied consistently since, and this record makes it
appealable.

[CLAUDE.md](../../CLAUDE.md) §4's outstanding item — "still owed: an ADR
recording the four-homes split" — is discharged by this file.

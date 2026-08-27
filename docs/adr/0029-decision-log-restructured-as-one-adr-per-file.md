# 29. Decision log restructured as one ADR per file, real Nygard/MADR convention

**Date:** 2026-08-27
**Status:** Accepted

## Context

The project previously split its decision record into two files by
workflow stage (`docs/00-project/decisions.md` for project-level
decisions, `docs/03-design/decisions.md` for design-stage decisions),
justified by [CLAUDE.md](../../CLAUDE.md) rule 7's "or the relevant stage's
own decisions log." That split was defended as intentional (project-level
scope decisions vs. design-stage presentation decisions), but on review
that defence doesn't hold up against how decision records are actually
kept in real software engineering practice: Architecture Decision Records
(the Nygard format, and its MADR variant) are one file per decision — a
single `Status` / `Context` / `Decision` / `Consequences` record — kept
together in one directory and numbered sequentially, specifically so that
superseding a decision (as happened three times with the suppression-timer
decision, [0025](0025-suppression-auto-expiry-flagged-for-elevation.md) →
[0026](0026-suppression-does-not-expire-visibility-replaces-timer.md) →
[0027](0027-suppression-works-like-notification-snooze.md)) is a normal,
linkable event, not something that has to be untangled from two growing
running logs. Splitting the log by which folder happened to be active
when a decision was made is not that convention, and isn't how real teams
organize this artifact.

## Decision

`docs/00-project/decisions.md` and `docs/03-design/decisions.md` are
retired. All 28 decisions they recorded (Nos. 1–28 above) are ported into
`docs/adr/` as individual, numbered, Nygard-format files, indexed by
[docs/adr/README.md](README.md). New decisions of any kind — project,
product, design, or architecture — are recorded the same way: one new
numbered file in `docs/adr/`, never appended to a running log, never split
by stage. [CLAUDE.md](../../CLAUDE.md) rule 7 is updated to describe this
convention instead of the per-stage log it previously specified.

## Consequences

Every reference to `docs/00-project/decisions.md` or
`docs/03-design/decisions.md` across the repo (`README.md`, `manifest.md`,
`PRD.md`, `UX.md`) is updated to point at the specific `docs/adr/NNNN-*.md`
file it meant. The two old files are removed from the working tree; their
content is preserved in git history and, more usefully, in the ported ADR
files themselves.

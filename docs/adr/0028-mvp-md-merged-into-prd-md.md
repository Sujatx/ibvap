# 28. MVP.md merged into PRD.md

**Date:** 2026-08-27
**Status:** Accepted

## Context

Having both `MVP.md` and `PRD.md` describe overlapping scope meant every
scope change (most recently [0016](0016-mvp-ui-cut-to-five-screens.md))
had to be hand-applied to two files, and they drifted in between —
`PRD.md` briefly carried a note flagging `MVP.md` as needing a trim pass it
hadn't gotten yet. One document should be the requirements source, with
MVP scope as a section of it, not a parallel file kept in sync by hand.

## Decision

`docs/02-product/MVP.md` is deleted; its content (capability mapping,
workflow, out-of-scope list, acceptance criteria, known limitations) now
lives as §6 of [PRD.md](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204), "Current build (MVP
scope)." No content was dropped — this is a merge, not a cut.

## Consequences

All references to `MVP.md` across the repo point to `PRD.md` §6 instead.

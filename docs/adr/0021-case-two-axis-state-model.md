# 21. The Case gets a real two-axis state model

**Date:** 2026-08-26
**Status:** Accepted (extends [0019](0019-case-association-exempts-evidence-from-retention-clock.md)) — screen cut from current build by [0016](0016-mvp-ui-cut-to-five-screens.md)

## Context

[investigative-case-management-platforms.md](../01-research/competitors/investigative-case-management-platforms.md)
found this two-axis separation is the single strongest convergent pattern
across every case-management system surveyed. IBVAP already had half of it
(closure separate from outcome, from [0019](0019-case-association-exempts-evidence-from-retention-clock.md));
this completes it. The outcome vocabulary deliberately avoids
legally-freighted terms ("cleared by arrest," "unfounded") that other case
systems use, since IBVAP does not assert a legal classification.

## Decision

The Case carries two independent, always-visible fields — an
**administrative state** (open — unassigned, open — assigned, parked,
closed, reopened) and a **recorded outcome** (apprehension / seizure /
nothing found / handed over / no action) — plus an **owner** field, a
person reference, empty by default, with a self-assign shortcut. Reopening
a closed Case re-suspends the retention clock established in
[0019](0019-case-association-exempts-evidence-from-retention-clock.md).

## Consequences

Case management is cut from the current five-screen build
([0016](0016-mvp-ui-cut-to-five-screens.md)); this applies if it returns.

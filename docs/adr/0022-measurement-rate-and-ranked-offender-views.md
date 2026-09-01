# 22. Measurement dashboard — rate view + ranked-offender view, no targets

**Date:** 2026-08-26
**Status:** Accepted — screen cut from current build by [0016](0016-mvp-ui-cut-to-five-screens.md)

## Context

[investigative-case-management-platforms.md](https://app.notion.com/p/3c986dda46e281a88c75e6b2d7bf373e?pvs=204)
found the real alarm-management standard this maps to (ISA-18.2) separates
performance metrics from diagnostic metrics because they answer different
questions for different readers; that a ranked top-N list is the
standard's own highest-value diagnostic panel; that alarm rate without
peak isn't treated as meaningful; and that the standard's numeric targets
are process-plant values that shouldn't transfer as IBVAP's targets.

## Decision

The measurement dashboard shows two separate views — a rate view (mean,
peak, hours-over-threshold) and a ranked-offender view (top-N noisiest
camera+rule pairs by share of total alerts) — both split day/night
throughout, with the measurement window stated on screen and no trend
drawn below it. A suppression panel shows active suppressions and how many
expired unreconfirmed. No target or "acceptable rate" number is ever
displayed.

## Consequences

The measurement dashboard is cut from the current five-screen build
([0016](0016-mvp-ui-cut-to-five-screens.md)); this applies if it returns.

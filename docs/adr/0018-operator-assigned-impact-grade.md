# 18. Operator-assigned impact grade, distinct from any computed score

**Date:** 2026-08-26
**Status:** Accepted — Case-outcome half cut from current build by [0016](0016-mvp-ui-cut-to-five-screens.md)

## Context

[international-border-surveillance-platforms.md](https://app.notion.com/p/3c986dda46e281bbbd54c6b5c8061a3f?pvs=204)
found every well-documented border event object carries a grade allocated
by a human on the reporting side, which a downstream C2 consumer may need
to prioritise. This is a different object from a computed threat/risk
score, which stays banned.

## Decision

A human may record an optional impact/severity grade when assessing an
Alert or recording a Case outcome. IBVAP never computes, suggests, or
defaults this value; it is always labelled as the assessor's own
judgement, never as a system finding.

## Consequences

The Alert-assessment half survives in the current build's Alerts & Events
screen; the Case-outcome half doesn't apply, since Case is cut
([0016](0016-mvp-ui-cut-to-five-screens.md)).

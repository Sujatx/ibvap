# 10. IBVAP as a support-posture analytics layer alongside existing infrastructure

**Date:** 2026-08-25
**Status:** Accepted — governance surface narrowed by [0016](0016-mvp-ui-cut-to-five-screens.md)

## Context

i-LIDS distinguishes a support posture from a primary (sole) detection
posture, and this choice determines alerting, staffing and liability.
IBVAP has no measured detection probability on the target estate. An
additive support layer is reversible upward per-rule once measured;
declaring itself the sole detection system is not reversible after a
missed detection.

## Decision

IBVAP is an intelligent video-analytics layer that can operate alongside
existing surveillance/VMS infrastructure and integrate with external
command/control systems — not a system that replaces the existing
surveillance system or removes the human from assessment. Per capability,
an alert routes to a human for assessment rather than acting as the sole
basis for a decision; in i-LIDS terms, IBVAP operates in a support posture
for every capability, not as the primary detection system.

## Consequences

See [PRD.md](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204). The fuller governance surface this
decision originally assumed (audit/authority/roles tooling) was cut from
the current build by [0016](0016-mvp-ui-cut-to-five-screens.md); the
support-posture principle itself is unaffected.

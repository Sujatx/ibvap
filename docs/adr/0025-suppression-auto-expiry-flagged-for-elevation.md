# 25. Suppression auto-expiry/reactivation, flagged for elevation

**Date:** 2026-08-26
**Status:** Superseded by [0026](0026-suppression-does-not-expire-visibility-replaces-timer.md)

## Context

A gap audit against
[international-border-surveillance-platforms.md](https://app.notion.com/p/3c986dda46e281bbbd54c6b5c8061a3f?pvs=204)
found that the original design ("suppression is time-bounded or requires
periodic reconfirmation") introduced a system behaviour — a rule
reactivating on a clock — that no frozen requirement required, and never
set a duration. A capability not traceable to `problem.md` or an accepted
decision is a defect in the design, and this did not pass that test; it
had been written as a presentation choice when it was closer to a product
decision.

## Decision

None — this entry recorded a flag, not a resolution. The underlying risk
(a silently self-muting system) is real, but whether suppression should
auto-expire at all, and on what schedule, was a call for the project
decision log, not something to settle inside a design document by
default.

## Consequences

Resolved by [0026](0026-suppression-does-not-expire-visibility-replaces-timer.md),
itself later revised by [0027](0027-suppression-works-like-notification-snooze.md).

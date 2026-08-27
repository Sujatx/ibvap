# 27. Suppression works like a notification snooze

**Date:** 2026-08-26
**Status:** Accepted (supersedes [0026](0026-suppression-does-not-expire-visibility-replaces-timer.md))

## Context

[0026](0026-suppression-does-not-expire-visibility-replaces-timer.md)
dropped timing entirely in favour of pure visibility, which is safe but
forgoes a pattern every user already understands (a notification's
mute/snooze options) and leaves a permanently-affected camera suppressed
forever with nothing prompting a review. Letting the operator choose the
duration each time keeps the underlying requirement fully satisfied,
invents no product-side number, and needs nothing new to learn.

## Decision

Applying a suppression means the human picks its duration — a short
preset (1 hour / 1 day / 1 week) or "until I turn it off" (indefinite). If
a duration was chosen, the suppression ends automatically when it elapses
and the rule resumes alerting — the operator's own choice, not a
product-picked schedule. It can also be reversed early by a human at any
time. Per-camera-per-rule, always visible (count and end time), always
reversible.

## Consequences

This is the suppression behaviour implemented in the current build — see
[UX.md](../03-design/UX.md) S-04 (Alerts & Events).

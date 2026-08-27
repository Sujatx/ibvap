# 13. Night-time movement detection as an explicit, measured capability

**Date:** 2026-08-25
**Status:** Accepted

## Context

The market's framing — night is a condition, not a separate feature — is
correct and evidenced, but the gap is that nobody measures and discloses
the condition. The statement names the capability explicitly, so it must
be represented as a real, named capability rather than only an internal
engineering property. Thermal support is post-MVP, gated on what fraction
of the estate is actually thermal — currently unknown.

## Decision

Night-time movement detection is an explicit product capability,
implemented as a first-class, separately-measured operating mode across
the existing detection primitives, rather than a separate "night AI
model." Concretely: (a) night-specific camera eligibility, measured after
dark and reported independently of the day verdict; (b) the same person
and vehicle detection primitives run against night-eligible cameras; (c)
night-scoped rules — time-of-day gating on zones, lines, direction and
dwell; (d) measured, disclosed limitations — the night-vs-day performance
gap and cause histogram, published per camera. No separate model or
product surface is named "night analytic."

## Consequences

See [PRD.md](../02-product/PRD.md) §5.1.

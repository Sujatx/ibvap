# 3. SSB is the validation context, not the product boundary

**Date:** 2026-08-25
**Status:** Accepted

## Context

[CLAUDE.md](../../CLAUDE.md) §4 requires the distinction; the problem
statement text itself says only "border security forces," not any one
force or country by name.

## Decision

SSB is the validation context, not the product boundary. All requirements
are written force-agnostically and market factors are labelled.
SSB-specific and India-specific requirements are marked `[SIH/SSB]` /
`[MARKET:IN]` and are treated as *satisfiable*, not *assumed*.

## Consequences

Any requirement true only for SSB or for India must be stated as such,
not folded into a general claim. See [PRD.md](../02-product/PRD.md).

# 11. Virtual fence ships in full, plus an open-border framing

**Date:** 2026-08-25
**Status:** Accepted

## Context

The statement requires the capability and it's technically straightforward;
research establishes that a line-crossing alarm is operationally
misdirected on a treaty-open border specifically, but not on fenced
borders generally — a border-security-specific vs. SIH/SSB-specific
distinction, per [CLAUDE.md](../../CLAUDE.md) §4.

## Decision

The virtual-fence capability ships in full, and additionally supports an
open-border framing. IBVAP does not remove or rename intrusion detection;
it adds the ability to make the reportable condition be class, time,
direction, dwell or accompaniment rather than the crossing itself.

## Consequences

See [PRD.md](../02-product/PRD.md) §5.1.

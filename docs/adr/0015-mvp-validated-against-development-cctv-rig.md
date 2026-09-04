# 15. MVP developed and validated against the existing development CCTV rig

**Date:** 2026-08-25
**Status:** Accepted, extended by 0060

## Context

A single measured recorder already falsified three convenient assumptions
(UDP viability, the "1080" resolution claim, and read-back-vs-trust
firmware behaviour) — which is why development is validated against real
hardware constraints rather than specified ones. Per
[CLAUDE.md](../../CLAUDE.md) rule 5, the existing setup (`dvr.py`,
`dvr.env`, `backups/`, `requirements.txt`) is preserved, not modified —
IBVAP consumes it, it does not replace it.

## Decision

The MVP is developed and validated against the existing development CCTV
rig in this repository — five live channels behind a real analog XVR with
a fixed 1080N anamorphic encode, a shared 12,288 kbps / 120 fps budget
across 8 channels, TCP-only RTSP, and firmware that returns OK for
settings it discards. This rig is the existing development and validation
environment used to test IBVAP against real-world legacy CCTV/DVR
constraints — it is not claimed to represent the SSB camera estate, which
remains unmeasured.

## Consequences

Rig-measured constraints (anamorphic encoding, firmware settings silently
discarded, shared/finite recorder bandwidth) are carried as a
cross-cutting requirement in [PRD.md](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204) §5.2.

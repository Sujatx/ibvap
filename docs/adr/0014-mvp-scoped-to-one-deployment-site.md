# 14. MVP scoped to one deployment site, complete end-to-end

**Date:** 2026-08-25
**Status:** Accepted

## Context

This is the smallest unit that demonstrates the complete operational value
of IBVAP end-to-end while satisfying the SIH direction, and it is the unit
the real estate actually consists of. The exact SSB monitoring workflow is
unresolved ([0004](0004-function-without-remote-monitoring-layer.md));
drawing the boundary this way means it neither assumes a control room
exists nor asserts that one doesn't.

## Decision

The MVP is one site, complete. The smallest coherent product is a single
deployment site with its existing cameras, running the full loop — ingest
→ capability check → primitives → rules → event → alert → assessment →
egress — end to end. The boundary is: (a) one deployment site; (b)
complete end-to-end operation across that loop; (c) local, site-level
operation must work independently of any remote layer; (d) remote
monitoring and/or command-and-control integration may be supported where
present, but core operation does not require it; (e) the MVP does not
assume a specific, undocumented SSB CCTV or control-room workflow; (f)
core operation does not require a remote control room.

## Consequences

See [PRD.md](../02-product/PRD.md) §6.

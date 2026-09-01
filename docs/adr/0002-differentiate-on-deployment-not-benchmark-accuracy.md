# 2. Differentiate on deployment, transparency and reliability, not on benchmark accuracy leadership

**Date:** 2026-08-25
**Status:** Accepted

## Context

All eight required capabilities are commodity — accuracy claimed in the
abstract is not a defensible sole differentiator against vendors with
decades of tuning. The four best-evidenced pain points (PP2, PP3, PP4, PP7)
in [product-discovery.md](https://app.notion.com/p/3c986dda46e281308010e0a5e861a5b4?pvs=204) §4.1,
§9 are all conditions of deployment, not of raw detection accuracy.

## Decision

IBVAP differentiates through deployment, transparency, reliability and
camera-aware operation; it pursues sufficient accuracy for each defined use
case rather than competing primarily on benchmark leadership. It will not
claim universal camera support, and it will not chase headline accuracy
figures disconnected from a measured use case — but accuracy remains a
first-class, per-capability requirement, gated and reported by the
per-camera capability check rather than asserted in the abstract. It
competes on running where nothing else runs, and on stating, per camera,
what it can and cannot do, at what measured accuracy.

## Consequences

No accuracy claim ships without a stated measurement condition. See
[PRD.md](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204).

# 4. Function correctly whether or not a remote monitoring/control-room layer is available

**Date:** 2026-08-25
**Status:** Accepted

## Context

The exact SSB CCTV/control-room workflow is unresolved. Designing around
either its presence or its absence as the assumed baseline invents a
workflow the research does not establish. Falsified by: an answer showing
a staffed monitoring posture that an additive-layer design fails to serve.

## Decision

IBVAP is designed to function correctly whether or not a remote
monitoring/control-room layer is available, or is temporarily unavailable.
Core, site-local operation — analysis, rule-firing, logging, local
alerting — does not depend on a control room, an operator on shift, or a
console being present or reachable. Where a remote monitoring or
control-room capability does exist, IBVAP integrates with it as an
additive layer. Nothing in the MVP requires an operator to be watching,
and nothing in the MVP assumes one is not.

## Consequences

The product is built to be correct under both answers to the unresolved
monitoring-workflow question rather than betting on one. See
[PRD.md](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204).

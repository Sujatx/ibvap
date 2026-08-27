# 6. Satisfy C2 integration via a demonstrated generic event contract, not a named adapter

**Date:** 2026-08-25
**Status:** Accepted

## Context

Building an adapter for a system that has no confirmed name is the
documented integration risk. A published, demonstrated generic contract is
the strongest form of the requirement that can be satisfied before a real
target system is identified — it proves the mechanism works end-to-end
without inventing a target that doesn't exist. Falsified by: a real target
system being named, at which point a reference adapter to that system
becomes worth building.

## Decision

IBVAP satisfies "integration with existing command and control systems" by
being an emitter with a documented, stable, open event contract,
demonstrated against at least one real external integration path — not by
shipping an adapter for a named system. The build ships a published,
versioned event schema plus a generic outbound mechanism (e.g. webhook,
REST, or MQTT), and demonstrates that mechanism actually delivering events
to a real external consumer end-to-end. Standards-based egress (ONVIF
Profile M over MQTT; MISB ST 0903 VMTI within STANAG 4609) and adapters
for a specific named C2 system remain post-MVP, unless and until a real
target system is identified — no vendor surveyed emits either standard
today.

## Consequences

See [PRD.md](../02-product/PRD.md) §5, §7 (Integration screen).

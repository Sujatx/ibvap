# 20. Egress classification/release-filter field: considered, deferred

**Date:** 2026-08-26
**Status:** Accepted (deferred)

## Context

What data-classification scheme applies to this deployment is itself
unresolved. Inventing a value set now would mean guessing a structure that
the outbound schema's own required versioning would likely have to redo
once that's actually answered by the force — the cost of building this now
isn't engineering effort (trivial) but the risk of encoding a wrong answer
to a question that hasn't been asked yet.

## Decision

No classification, ownership or release-filter field is added to the
outbound event schema in the current build.

## Consequences

Revisit once the deployment's data-classification policy is known. See
[PRD.md](../02-product/PRD.md) §9 (open questions), Integration screen.

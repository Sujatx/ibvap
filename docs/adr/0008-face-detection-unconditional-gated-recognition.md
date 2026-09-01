# 8. Face detection unconditional; controlled, gated face recognition specified but not in the current build

**Date:** 2026-08-25
**Status:** Accepted — recognition-matching narrowed out of the current build by [0016](0016-mvp-ui-cut-to-five-screens.md)

## Context

The problem statement requires facial recognition to be supported through
software. This decision specifies how that support can be delivered
without asserting a legal basis this project has not established — the
legal basis, authorisation level, retention rule and oversight for
biometrics on a treaty-open border remains explicitly unresolved. This is
the decision most likely to be contested at SIH evaluation and needed an
explicit human call.

## Decision

Face detection (presence/location, not identity) ships unconditionally.
Controlled face-recognition matching can be exercised in a controlled
development/test environment, against an explicitly configured, bounded
gallery. For a real deployment, biometric matching is technically blocked
unless four conditions are configured and current: (1) a recorded, valid
legal basis for that deployment; (2) the required authority record; (3)
the authorized, bounded gallery; (4) applicable retention and oversight
requirements. The authority record is never treated as evidence that the
legal basis exists — the two are separate, independently required and
independently recorded conditions. Any biometric operation outside those
satisfied conditions is blocked, not merely discouraged, and every
biometric operation is logged and auditable. No unrestricted, open-set or
population-scale face recognition ships at any point.

## Consequences

See [PRD.md](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204) §5.1. Matching against a gallery was
subsequently cut from the current five-screen build by
[0016](0016-mvp-ui-cut-to-five-screens.md) — detection ships, matching does
not, because the legal-authority workflow this decision requires isn't
built in that scope.

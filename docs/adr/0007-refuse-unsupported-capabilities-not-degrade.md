# 7. Refuse capabilities the camera cannot support, rather than degrade them

**Date:** 2026-08-25
**Status:** Accepted — presentation narrowed by [0016](0016-mvp-ui-cut-to-five-screens.md) (inline refusal, not a dedicated gate screen)

## Context

This is the product's central differentiator
([0002](0002-differentiate-on-deployment-not-benchmark-accuracy.md)) and
the market's unfilled gap; a soft warning would be indistinguishable from
every vendor's disclaimer. Known cost: it means telling a buyer their
estate cannot do what they hoped.

## Decision

A capability that the camera cannot support is refused, not degraded.
Overriding is possible, requires a named authority, and permanently marks
the resulting events.

## Consequences

See [PRD.md](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204). The dedicated certification-screen
presentation of this refusal was cut by
[0016](0016-mvp-ui-cut-to-five-screens.md); the refusal itself now surfaces
inline on the Live View screen instead.

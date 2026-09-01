# 19. Case-association exempts bound evidence from its retention clock

**Date:** 2026-08-26
**Status:** Superseded by [0021](0021-case-two-axis-state-model.md); screen cut from current build by [0016](0016-mvp-ui-cut-to-five-screens.md)

## Context

[international-border-surveillance-platforms.md](https://app.notion.com/p/3c986dda46e281bbbd54c6b5c8061a3f?pvs=204)
found real border-surveillance platforms preserve evidence by case
association and overwrite by default otherwise — the opposite of a design
where an open Case's own evidence can expire out from under it.

## Decision

While an Event's evidence is bound to a Case that has not been closed, it
is exempt from its class retention clock. The clock resumes, on the
class's configured schedule, from the Case's **closure** — an explicit
administrative act, separate from recording the Case's outcome — not from
the evidence's original capture time. Evidence never attached to a Case,
or detached from one, is unaffected.

## Consequences

Extended by [0021](0021-case-two-axis-state-model.md) into a full two-axis
Case state model. Case management is cut from the current five-screen
build ([0016](0016-mvp-ui-cut-to-five-screens.md)); this applies if it
returns.

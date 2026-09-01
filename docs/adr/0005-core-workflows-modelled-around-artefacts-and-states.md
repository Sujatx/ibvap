# 5. Core workflows modelled around artefacts and their states

**Date:** 2026-08-25
**Status:** Accepted — narrowed by [0016](0016-mvp-ui-cut-to-five-screens.md) (Case is no longer a built artefact in the current build)

## Context

This is the only construction that satisfies the requirement to work
correctly under either answer to the unresolved SSB monitoring-workflow
question ([0004](0004-function-without-remote-monitoring-layer.md)) while
still shipping a coherent workflow. If a staffed control room turns out to
exist, the same artefacts and states route to an operator under the
corresponding role and permissions; if it's a single Sub-Inspector and a
phone, the same artefacts route to him. No re-architecture is required by
either answer, and that property is itself the requirement.

## Decision

Core workflows are modelled around artefacts and their states, with role
assignment and permissions configurable. The product produces four core
artefacts — an Event, an Alert, a Case, and a per-camera capability
record — and every workflow is a path through those artefacts' states.
Which human occupies which step, and what permissions that role carries,
is configurable and carries no product assumption about the real SSB
workflow.

## Consequences

See [PRD.md](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204). Case as a built artefact was later cut
from the current build by [0016](0016-mvp-ui-cut-to-five-screens.md) — the
artefact/state modelling principle survives for Event and Alert, which are
still in scope.

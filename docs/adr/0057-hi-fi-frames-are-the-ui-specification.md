# 57. The hi-fi frames are the UI specification, and rail collapse is runtime state

**Date:** 2026-09-03
**Status:** Accepted — narrows [0041](0041-hi-fi-assembled-from-an-appshell-component.md) and [0047](0047-rail-collapse-becomes-baked-frame-pairs.md)

## Context

Phase 2 produced twelve hi-fi frames in Figma `03 Hi-fi`, and the ADRs written
alongside them are a record of that work in progress. Several are now older than
what they describe, and two of them record decisions that exist only because of
how Figma behaves.

[0047](0047-rail-collapse-becomes-baked-frame-pairs.md) is the clearest case. It
makes the rail's collapsed state a pair of baked frames reached by `NAVIGATE`
with `SMART_ANIMATE`, rather than a runtime variant swap — because Figma's
Interactive Component memory carried resolved variant state across navigation and
made the active-nav highlight go stale, while `resetInteractiveComponents` broke
collapse. That is a correct decision about a prototyping tool. Read as a
specification for the application, it would have someone build ten routes where
one boolean belongs.

The same pattern appears elsewhere. [0017](0017-cameras-site-sketch-not-a-map.md)
puts the site sketch on a Cameras list that
[0016](0016-mvp-ui-cut-to-five-screens.md) cut and
[0044](0044-site-sketch-returns-on-live-view.md) relocated.
[0038](0038-historical-timeline-on-the-focused-camera-view.md) and
[0045](0045-timeline-second-pass-controls-and-density.md) say timeline markers
carry no hue, which [0046](0046-timeline-markers-carry-class-colour.md) reversed.
[0036](0036-wireframe-breakpoints-and-required-state-set.md) specifies three
widths and a frame per state, which
[0039](0039-state-coverage-evidenced-three-ways.md) replaced.

Someone implementing the console from the ADR index, in order, would build
several things that no longer exist. A general rule is needed, not eight
individual corrections.

## Decision

**Where an ADR and the hi-fi frames disagree, the frames are the specification
and the ADR is history.**

Specifically, and to save the next person the archaeology:

| The ADR says | The frames show | Build |
|---|---|---|
| 0047 — collapse is baked frame pairs via `NAVIGATE` | Collapsed and expanded chrome at the same 1440 width | Runtime state: one boolean on `AppShell` |
| 0041 — five 1440 masters, five 1280 counterparts | Twelve 1440 frames plus a 1920 fluid proof | The frames |
| 0017 — site sketch on a Cameras list | Site sketch panel on the focused Live View | 0044 |
| 0038 / 0045 — markers carry no hue | Markers coloured by detection class | 0046 |
| 0036 — three widths, a frame per state | Two drawn widths, a state matrix as evidence | 0039 |
| Wireframes — S-04 as a five-column table with a header | `EventRow` cards, no `TableHeader` | The cards |

This does not supersede those ADRs. They remain accurate records of decisions
made at the time, and the reasoning in them is often still load-bearing — 0047's
account of why the Figma prototype needed baked pairs is worth keeping. What this
decision fixes is which artefact wins when they conflict.

The rule has a boundary. It applies to *how a screen looks and behaves*. It does
not override decisions about what the product does, what it refuses, or what it
never says — 0007's refusals, 0012's rejection of a learned model, 0018's
operator-only grade, 0030's ban on severity colour. Those are product decisions
that the frames implement rather than compete with.

## Consequences

The console is built from Figma, and the ADRs are read for reasoning rather than
for specification. That is the correct relationship given
[0049](0049-four-homes-for-project-artefacts.md): Figma *is* the design, and a
repository document describing a design is a copy that goes stale — which is
exactly what happened here.

`AppShell` gets a `railCollapsed` boolean persisted to `localStorage`, and the
active destination derives from the route. Ten frames become five routes plus one
piece of state, and the collapsed variants in Figma are read as visual reference
rather than as a routing scheme.

There is a real risk in this rule: it makes the frames authoritative even where
they are wrong, and a frame can be wrong. The mitigation is that a disagreement
noticed during implementation is a conversation, not a silent choice — if the
frames turn out to contradict a product decision rather than merely an older
design decision, that is a new ADR, not a licence to improvise.

The flow-state frames deferred by
[0048](0048-phase-2-closes-flow-frames-deferred.md) are not covered by this rule,
because they do not exist. The endpoints that would back them are specified in
[RFC 0004](../rfcs/0004-web-application-and-api-contracts.md); their visual
design is still owed.

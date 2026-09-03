# 48. Phase 2 closes here; the flow frames are deferred, not built

**Date:** 2026-09-03
**Status:** Accepted — narrows [0041](0041-hi-fi-assembled-from-an-appshell-component.md)

## Context

0041 named the remaining work of Phase 2 Task 2 as "the second pass: the flow
frames, and the prototype destinations that come with them" — frames like
`too many attempts`, `drawing a zone`, `mute applied`, `the test event was
refused`, none of which exist in `03 Hi-fi` today. What was actually built
since 0041 is [0047](0047-rail-collapse-becomes-baked-frame-pairs.md)'s
rail-navigation fix — the prototype destinations among the five real screens
now work correctly with the rail collapsed or expanded — plus two of the
eight source photographs applied: the Alerts screen's selected row and its
`CROP` detail panel now carry real images, the other five rows left black on
purpose, matching how the grid, focused-camera and Rules screens already
carried real camera stills from earlier work.

The flow frames are a distinct kind of screen — transient and error states
layered onto the five already built, not new destinations — and were never
drawn. Holding Phase 2 open until they exist would leave it open indefinitely
without a scheduled owner for that work.

## Decision

**Phase 2 is done as of this ADR.** The flow frames are out of scope for
Phase 2 and deferred to a later pass with no committed date; when picked up,
they get their own ADR rather than reopening this one. What Phase 2 actually
delivered: `01 Wireframes` (37 frames, [0039](0039-state-coverage-evidenced-three-ways.md)),
`02 UI Kit` ([0040](0040-kit-gaps-built-out-for-hi-fi.md)), and `03 Hi-fi`'s
twelve assembled, wired, and image-populated frames
([0041](0041-hi-fi-assembled-from-an-appshell-component.md),
[0043](0043-focused-camera-view-rebuilt-around-the-picture.md),
[0044](0044-site-sketch-returns-on-live-view.md),
[0045](0045-timeline-second-pass-controls-and-density.md),
[0046](0046-timeline-markers-carry-class-colour.md),
[0047](0047-rail-collapse-becomes-baked-frame-pairs.md)).

## Consequences

Phase 3 (the architecture RFCs) can start without waiting on the flow frames;
nothing in `docs/architecture/README.md` §4–7 reads them. The five Alerts
rows left unfilled, and any screen state the flow frames would have covered,
stay visibly unfinished in the file rather than faked — consistent with
[0039](0039-state-coverage-evidenced-three-ways.md)'s stance that coverage is
evidenced, not implied.

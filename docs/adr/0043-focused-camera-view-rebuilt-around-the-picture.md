# 43. The focused camera view is rebuilt around the picture, and Live View gains an alerts rail

**Date:** 2026-09-03
**Status:** Accepted

## Context

The focused-camera frame built in
[0041](0041-hi-fi-assembled-from-an-appshell-component.md) was correct and thin.
It inherited the camera sidebar from the grid it was reached from, which left the
picture — the thing the screen exists for — about 450 px wide on a 1440 console,
with one panel of camera facts beside it and nothing else on screen.

A reference set supplied in September 2026 and archived on `99 Archive`
(frame 23:2, kept there precisely because it contradicts nine accepted decisions)
answers the same brief with roughly three times the information visible at once:
a full-width picture, a live alert rail, a camera spec list, a strip of the other
cameras, a site view, and a much larger timeline. Asked what he wanted from it,
Sujat named the layout and the quantity of information, and explicitly not the
light theme or the severity colours. Those stay as
[0030](0030-dark-console-palette-no-severity-colour.md) has them.

## Decision

**The camera sidebar leaves the focused view, and a thumbnail strip takes over
switching cameras.** The sidebar is the grid's control and belongs there; on the
focused view it was spending 258 px to list cameras the operator has already
chosen between. `CameraThumb` carries the name, the transport dot and which one
you are on. That single removal is what pays for everything else on the screen.

**Live View gains an Active Alerts rail.** This is not a sixth screen and does
not reopen [0016](0016-mvp-ui-cut-to-five-screens.md): the rail restates the
Alerts & Events feed at the place an operator is actually looking, and every card
navigates into S-04, which still owns the event, the assessment and the mute. It
draws exactly the distinction the system draws — `Kind=Alert` carries the same
`status/alert` edge marker `EventRow` uses, `Kind=Logged` carries none, and the
class is named by a picture rather than ranked by a hue
([0030](0030-dark-console-palette-no-severity-colour.md) rule 1,
[0018](0018-operator-assigned-impact-grade.md)).

**The camera panel becomes a spec list, and the capability state stays with it.**
`SpecRow` puts a measured fact against its label, in JetBrains Mono where a
person may have to read it out or compare it. What runs on this camera is a chip
row, and the refusal keeps its full sentence in a `CapabilityNotice`
([0007](0007-refuse-unsupported-capabilities-not-degrade.md)) rather than being
compressed into a badge. The reference's spec list is a datasheet; this one is
what the capability pass measured
([0015](0015-mvp-validated-against-development-cctv-rig.md)).

**What the reference carries that stays refused:** PTZ controls and presets,
share / bookmark / snapshot / export, the breadcrumb sector hierarchy, the global
search field, and the extra nav destinations (Search & Investigation, Reports,
System, Settings). These are the boundary
[0038](0038-historical-timeline-on-the-focused-camera-view.md) leans on when it
reverses the refusal for the timeline alone, and reversing them here because a
mock drew them is the reasoning that decision explicitly refuses.

## Consequences

`02 UI Kit` gains six components — `ClassGlyph`, `ControlGlyph`, `IconButton`,
`SpecRow`, `AlertCard`, `CameraThumb` — all drawn or bound into the family and
token set the kit already had. The glyph sets extend the family
[0042](0042-sign-in-photograph-and-a-capability-icon-family.md) established, so
the console now has one drawing language at 18 and 24 rather than three.

The plan for this work said `VideoTile` would gain a `Size=sm` variant for the
strip. It did not: adding a variant property to a set with live instances risks
every grid frame, and the strip item wants a name, a status dot and a selected
state that `VideoTile` has no business carrying. `CameraThumb` is a separate
component for that reason, and `VideoTile` is untouched.

`03 Hi-fi` gains a twelfth frame — the 1280 focused view, which had no
counterpart before — and both focused frames are wired: back to the grid, into
Rules for this camera, and from any alert into Alerts & Events.

The raw-value sweep [0031](0031-component-grammar-chip-states-fact-segmented-control-chooses.md)
requires returns zero across both frames, instance internals included. Rendered
in Day nothing vanishes; the capability notice keeps a dark ground there, which
is worth looking at when Day is designed and is not a defect this pass
introduced.

`access — read-only, live` left the spec list because the header subline already
says it. Nothing else in the first pass's content was dropped.

The rail restates data it does not own. If the two ever disagree, S-04 is right;
that is the price of putting the feed in two places, and it is worth paying
because the alternative is an operator watching a camera with no idea that
anything fired on it.

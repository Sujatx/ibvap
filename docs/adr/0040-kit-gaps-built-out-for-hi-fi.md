# 40. The kit gaps are built, and what building them settled

**Date:** 2026-09-02
**Status:** Accepted

## Context

[0039](0039-state-coverage-evidenced-three-ways.md) moved where a state is
specified. A *skin* state — a loading skeleton, an input error, a button
spinner, a tile status — no longer gets its own wireframe frame; it gets an
annotation on the master naming the kit component and variant that renders it.
Forty-five `Renders as` lines across fourteen annotation panels now point at
components, and when Task 2 began a large share of them pointed at nothing.

That is the whole risk 0039 took on, written down in its own Consequences: an
annotation is weaker evidence than a drawing, and it only holds if the kit
variant it names actually exists. Until this pass, it did not.

The `Kit gaps` board produced by the Task 1 rebuild listed fifteen components
missing outright, six needing new variants and two needing changes. Building
against the annotations rather than against the board surfaced eight
discrepancies between the two, which had to be resolved before anything was
drawn.

## Decision

**The board and the annotations are reconciled, and the annotations win where
they describe a real screen.** Four demands the board did not carry were built:
`ConnectionState / State=Checking`, `ClipRequest / State=Failed`,
`MuteBanner / State=Expired` and `VideoTile / State=Connecting`. Four
annotations named things under names the kit does not use and were corrected
rather than built: `ConnectionState / State=Down` is `State=Disconnected`,
`DeliveryRow / State=Rejected` is `Kind=Event, Result=Rejected`,
`SegmentedControl / Select active` is `Segments=3, Selected=3`, and
`Panel / header collapse action` is now a real variant, `Header=Label + collapse`.

**VideoTile has four states, not five.** The board asked for Live,
Reconnecting, Lost and Offline. The S-02 annotation shows Offline and Lost are
one fact rendered twice — the tile says "Stream not reachable", the sidebar row
says Offline. A fifth tile state would have been the same condition under a
second name. `CameraListItem` carries Offline; `VideoTile` carries Lost.

**The control ladder gains a rung rather than a redefinition.** `control/lg`
already existed at 48. Sign in runs at 56 ([0037](0037-sign-in-follows-the-reference-username-password.md)),
so `control/xl` = 56 was added and `Button / Size=lg` binds it. Redefining
`control/lg` would have silently moved every control already sitting on it.
[0031](0031-component-grammar-chip-states-fact-segmented-control-chooses.md)'s
rule that the token wins is honoured by moving the token, never by typing 56
into a component.

**A failure message is neutral by default.** `InlineMessage` has
`Tone=Neutral` and `Tone=Attention`; Neutral is the default. Amber is the
annunciator meaning a human should look at something
([0030](0030-dark-console-palette-no-severity-colour.md) rule 1), and spending
it on every form validation would weaken it exactly where it matters. Where a
control itself is wrong — `Input / State=Error` — the amber marks the control
and the sentence beside it stays neutral. `InlineMessage` is also explicitly
not `CapabilityNotice`: a refused capability is a correct outcome
([0007](0007-refuse-unsupported-capabilities-not-degrade.md)) and must never be
rendered in a component built for failures.

**Chrome over video binds a pair fixed in both modes.** `surface/video`
inverts between Night and Day, but the pixels under real chrome are footage,
not a themed surface. `video-chrome/scrim` and `video-chrome/fg` were added to
the theme collection holding the same value in both modes — the over-video
counterpart of the fixed `detect/label-fg` that
[0031](0031-component-grammar-chip-states-fact-segmented-control-chooses.md)
already established.

**Field wraps a control; it does not wrap Input.** `Input` carries its own
label and help text, so nesting it inside `Field` would print the label twice.
`Field` takes a swappable control slot — Select, SegmentedControl, Checkbox —
and `Input` stays used directly. Reworking `Input` into a bare control was
rejected on the same grounds 0031 used to leave reviewed components alone.

**Scrim is its own component.** Modal and Drawer both sit on one, and the
1280 overlay drawer needs the same ground the modal uses. One component,
referenced by both.

## Consequences

`02 UI Kit` gained sixteen components — StatusDot, Skeleton, Tooltip,
InlineMessage, Checkbox, TableHeader, Field, Scrim, Modal, Drawer, Pagination,
DismissalCausePicker, VideoTile, Timeline, TimelineMarker, and the Panel
collapse variant — plus nine variant additions across Button, Input, NavItem,
CameraListItem, ConnectionState, ClipRequest and MuteBanner, and two changes to
AppBar and Panel. Two dimension tokens and two theme tokens were added; no new
collection, and no new text style.

All forty-five `Renders as` lines now resolve to a component and variant that
exists, spelled the same way. That is the check that matters, not the component
count: it is the promise 0039 made when it traded frames for annotations.

The raw-value sweep 0031 requires returned zero across all twenty-four
components touched. Getting there cost more than expected — the sweep found
pre-existing eyeballed spacing inside `ConnectionState` and `ClipRequest` that
0031's own sweep had recorded as clean. `ClipRequest`'s hand-built button was
replaced with a real `Button` instance and its off-scale padding bound to
tokens. `PayloadPreview`, `MuteDurationMenu` and the alert detail's record list
stay untouched, as 0031 decided and as the board's footer says.

Rendering both modes caught one defect that Night alone would have shipped, which
is the second time that check has paid for itself: `Skeleton` bound
`surface/raised`, which is white in Day and therefore invisible on the canvas.
It binds `surface/overlay` instead.

`AppBar` needed less than the board thought. Once instanced with FILL it already
reflowed at 1280, 1440 and 1920 — proved against all three before changing
anything — so it gained a minimum width and an explicit contract in its
description rather than a rebuild.

The `Timeline` is the weakest thing in this pass, and knowingly so. It is the
largest component in the kit, the only one owning a continuous scale, and the
only one whose data path is unverified:
[0038](0038-historical-timeline-on-the-focused-camera-view.md) requires RFC 0001
to measure whether the rig will serve recorded video at all before any timeline
code is written. `Mode=Unavailable` is built as a first-class mode for exactly
that reason. If RFC 0001 finds no route, the component is not wasted — it ships
as the refusal.

[ROADMAP.md](../../ROADMAP.md) Phase 2 Task 2 is unblocked at the point it was
actually blocked. `03 Hi-fi` is still empty; assembling the five screens from
these components is the remaining work of Task 2.

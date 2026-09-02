# 39. State coverage is evidenced three ways, not one frame per state

**Date:** 2026-09-02
**Status:** Accepted. Supersedes [0036](0036-wireframe-breakpoints-and-required-state-set.md)

## Context

[0036](0036-wireframe-breakpoints-and-required-state-set.md) required seven states
on every screen and three drawn widths, and the rebuild it governed produced 75
frames. That was the right call when it was made, and it did the job it was made
for. The five frames it replaced drew one state at one width each — no failure, no
in-progress, no explanation of anything — and no frontend track could have been
scoped from them. Drawing everything is how the missing states were found, and it
is how the twenty-one kit gaps were found; not one of those was visible from the
happy path.

It is the wrong thing to keep maintaining. The console shell ended up hand-drawn
about fifty times, so a change to the navigation rail or the app bar is fifty
edits, in the phase where the design should still be cheap to change. The same
fact also gets asserted twice — once by a frame showing that an input has an
error state, and again by the kit variant that will render it.

The width tier was weaker still. Measured against the frames themselves, 1920 and
1440 hold the same arrangement — expanded rail, four columns, a 3×3 grid — and
differ only in width. Before anything was archived, every frame being retired was
diffed against its master for text the master did not already carry. All five 1920
frames returned nothing at all. They were duplicates in the strict sense, not
denser or differently arranged. So did the two frames drawing collapsed chrome at
1440, which the 1280 frames already show collapsing by rule rather than by choice.
1280 is the only width where the arrangement actually changes, and 0036 already
described how it changes.

## Decision

**Two drawn widths: 1440 and 1280.** 1440 is the canonical build and 1280 is the
one real breakpoint — the rail collapses to an icon rail, the fourth column becomes
a right-anchored overlay drawer, and the live grid drops to 2×2. 1920 is fluid, not
a breakpoint: the 1440 arrangement fills it, and that is proved once on a single
Shell frame rather than restated on every screen. The rest of
[0036](0036-wireframe-breakpoints-and-required-state-set.md)'s width reasoning
stands, including that there is no tablet or mobile tier.

**A state earns its own frame when it changes the arrangement or advances a flow.
Otherwise it is an annotation.** Three kinds, and only two of them get drawn:

- *Layout* — the arrangement changes. In practice, 1440 and 1280.
- *Flow* — a distinct step an operator moves through, and therefore a legitimate
  prototype destination. Assess, then mute offered, then dismissal cause is three
  steps and three frames.
- *Skin* — a component swapping variant on an otherwise identical layout. Loading
  skeletons, input errors, button spinners, tile status, tooltips. These get an
  annotation naming the state, its trigger, its exact copy, and the kit component
  and variant that renders it.

**The seven-state floor is unchanged.** Loading, empty, filtered-empty, error,
in-progress, tooltip or inline explanation, and collapsed chrome are still what a
screen is not finished without, and where a state cannot exist the screen still
says so rather than skipping it silently. What changes is the evidence, never the
coverage.

**The State matrix on the Shell section is the coverage proof.** Seven states down,
five screens across, every cell resolving to a frame or to a numbered annotation,
and every impossible cell carrying its reason. The frame count proves nothing and
is not the thing to check.

**Prototype navigation destinations are exactly the Flow frames.** This is the
practical reason the taxonomy has to be decided rather than felt: a destination
must be a top-level frame, so the set of frames and the set of reachable prototype
states are the same set.

## Consequences

`01 Wireframes` holds 37 frames in six sections with 14 annotation panels, down
from 75 frames. Forty-five frames moved to `99 Archive` under
`Consolidated — 2026-09`, locked; nothing was deleted, and the frames remain
readable if a state turns out to need its own drawing after all.

Copy was harvested before anything moved — every retired frame diffed against its
master, and the delta transcribed into the annotation that replaces it. That order
mattered more than it looks: two of the longest deltas were load-bearing wording
from [0007](0007-refuse-unsupported-capabilities-not-degrade.md) and
[0012](0012-suspicious-activity-as-operator-authored-rules.md) — the explanation of
what an analysed frame rate means, and the sentence that a rule is only ever what
was drawn on that camera's own frame — and both would have been lost by archiving
first.

The timeline from [0038](0038-historical-timeline-on-the-focused-camera-view.md) is
drawn under this rule rather than the old one: its Live mode sits inside the
existing focused-camera frames, Scrubbing and the playback refusal are frames
because the arrangement changes, and marker tooltips, the retention boundary, a
recorder gap and a clock-unverified span are annotations.

The real risk is that an annotation is weaker evidence than a drawing. A sentence
saying an input shows an error is easier to write and easier to get wrong than a
picture of it, and nobody discovers a layout problem by reading a description of
one. Two things hold against that. The kit variant is now the single place the
state is actually specified, which is where it was always going to be specified
anyway; and the State matrix makes an unevidenced state visible as an empty cell
rather than as a frame nobody drew. If a state turns out to be arguable in prose,
that is the signal to promote it back to a frame — which the archive keeps cheap.

This does not touch [0038](0038-historical-timeline-on-the-focused-camera-view.md),
which decides a capability rather than how the wireframes are drawn, and it does
not reopen anything 0036 refused on ADR grounds. Those refusals stand except the
recorded-video scrubber, which 0038 reversed on its own reasoning.

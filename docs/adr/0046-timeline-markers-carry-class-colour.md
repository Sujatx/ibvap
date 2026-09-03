# 46. Timeline markers carry class colour, and the axis is drawn as a band rather than a scatter

**Date:** 2026-09-03
**Status:** Accepted — supersedes the marker rule in [0038](0038-historical-timeline-on-the-focused-camera-view.md) and [0045](0045-timeline-second-pass-controls-and-density.md) — store obligation settled by [0056](0056-an-event-carries-one-primary-class.md)

## Context

[0038](0038-historical-timeline-on-the-focused-camera-view.md) settled that event
markers would carry alert-versus-logged and nothing else, drawn as two weights
and never two hues, on the grounds that a coloured marker track would
reintroduce the severity scale this product refuses to compute.
[0045](0045-timeline-second-pass-controls-and-density.md) reaffirmed it hours
before this decision, and refused the reference's coloured legend twice over: by
severity on frame 23:7, which is forbidden outright, and by class on 23:6, on the
narrower argument that colour along a single axis reads as degrees whatever the
legend says.

Then the thing was drawn at real density and looked at. A hundred ticks in one
colour, at two weights, on a dark ground, is not a record of a day — it is, in
Sujat's words, white lines drawn at random. Nothing in it can be grouped by eye.
A burst of vehicles at a gate and a burst of people on a fenceline are the same
picture. The operator cannot tell, without clicking, whether the busy hour was
traffic or footfall, which is the first question anyone asks of a timeline.

The refusal was defending against a real failure — a red/amber/green ramp that
ranks events the system has not ranked. But the four detection classes are not a
ramp. [0030](0030-dark-console-palette-no-severity-colour.md) already sets them
at deliberately equal lightness with spread, CVD-safe hue precisely so they read
as four kinds of thing rather than four degrees of one, and already permits them
as the one categorical use of hue in the product. The argument that they turn
into degrees when moved from the picture to the axis beneath it does not survive
seeing both on screen together.

## Decision

**Colour on the marker track names the detection class, using the same four
tokens `DetectionBox` uses on the picture.** A cyan tick under a cyan box is the
same event described twice, and the operator learns one vocabulary instead of
two.

**Weight still names alert versus logged.** An alert is the full-strength 3 px
tick; a logged event is a 2 px tick at half strength. The binary
[0030](0030-dark-console-palette-no-severity-colour.md) rule 1 protects is
untouched — it has simply stopped being the only thing the axis says.

**Severity stays undrawn.** There is no High / Medium / Low, no ramp, no red for
bad. Frame 23:7's legend is still refused, and for the original reason: the
product computes no severity, and
[0018](0018-operator-assigned-impact-grade.md) makes the impact grade the
assessor's own judgement rather than a system finding. What changed is that
naming a category and ranking one are now treated as the different things they
are.

**The axis is drawn as a band, not a scatter.** The tick labels sit above the
track rather than below it; the track is one rounded bar holding every mark at a
common height; the recorder gap, the pre-retention span and the unverified-clock
span are bands inside that bar; the playhead is a line with a knob at the top;
and the current time is called out large and centred in the control row. The
legend names both dimensions — the four classes, and the two weights. This is the
reference's layout and it is better than what was there, which is the whole of
the reason for adopting it.

## Consequences

`TimelineMarker` goes from two variants to eight — `Kind` × `Class` — and the
component that was the kit's smallest is now the one carrying the most meaning
per pixel.

**Every marker now needs a class, and the store has to supply one.** For an alert
this is the class the rule matched on; for a logged detection it is the class
detected. Events that resolve to no single class — a zone rule that fired on
mixed traffic, say — have no colour defined for them here, and RFC 0003 has to
decide whether they get a neutral mark or the class of whatever triggered the
rule. Drawing them in one of the four would be a lie about what was seen.

The timeline shrank from 200 to 156 high once the axis stopped needing room for
scattered marks of two heights, and both focused frames gave the 49 px back to
the picture.

[0038](0038-historical-timeline-on-the-focused-camera-view.md) and
[0045](0045-timeline-second-pass-controls-and-density.md) keep everything else
they decided. Only the marker rule is reversed, and reversing it does not reopen
[0030](0030-dark-console-palette-no-severity-colour.md) — a fifth hue, or any
hue standing for how bad something is, would still be a change to that decision
and would still need one of these.

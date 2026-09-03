# 45. The timeline's second pass — the controls it gains, and the hue it still refuses

**Date:** 2026-09-03
**Status:** Accepted — marker rule superseded by [0046](0046-timeline-markers-carry-class-colour.md)

## Context

[0038](0038-historical-timeline-on-the-focused-camera-view.md) predicted this
pass in its own consequences: the timeline is the largest component in the kit
and the only one that owns a continuous scale, so it is the one most likely to
need reworking once it is used at more than one width. Built for
[0040](0040-kit-gaps-built-out-for-hi-fi.md) it carried four things — a state
chip, a span picker, an axis and five tick labels — and about fifteen markers on
a six-hour span, which is fewer events than a border post sees in a quiet hour.

The reference archived on `99 Archive` is what Sujat pointed at, and the timeline
is what he pointed at in it: a day selector, a live control, zoom, a filter, the
current time called out over the playhead, ticks every ten minutes, and an event
band dense enough to read as a record of a day rather than as a diagram of one.

## Decision

**The component gains the reference's control surface.** A day control on the
left with the live state beside it; the span picker, a zoom pair and a filter on
the right; the playhead's time called out above the axis; six tick labels instead
of four; markers at the density a real day produces; and a legend under the axis
naming what the marks and bands mean.

**Zoom in and zoom out step the same closed set the span picker shows.** There is
one notion of how much time the axis spans, reachable two ways: pick it, or step
it. A second, finer zoom would be a second scale to reason about and there is no
question on this screen that needs one.

**Markers stay two weights and no hue.** This is the one thing in the reference
not carried across, and it is deliberate twice over. Frame 23:7 legends its
markers by severity — High, Medium, Low — which is the scale
[0018](0018-operator-assigned-impact-grade.md) refuses to compute and
[0030](0030-dark-console-palette-no-severity-colour.md) rule 1 refuses to draw.
Frame 23:6 legends them by class, which is a category rather than a rank, and
[0030](0030-dark-console-palette-no-severity-colour.md) does allow categorical
hue — but only on detection overlays, where the hue sits on the frame it
describes. On a marker track it would put four colours along a single axis, and
an axis of colours reads as an axis of degrees whatever the legend says. So the
legend explains the two weights and the two bands instead, which is the thing an
operator actually needs told.

**The axis learned to be resized.** The component is 776 wide rather than 684,
and every part of it — the retention band, the gaps, the unverified span, the
markers, the playhead, the ticks and the clock — carries a resize constraint, so
an instance stretched to a screen's column still has its playhead at the right
edge and its last tick label inside the frame. The first pass did not, which is
why it only ever worked at one width.

**The filter is drawn, not specified.** What it filters is alert versus logged
and detection class, and nothing about severity. It is a control on a screen that
is not yet a control in a build, and it does not change the retrieval dependency
[0038](0038-historical-timeline-on-the-focused-camera-view.md) records: RFC 0001
still has to establish whether the recorder will serve recorded video at all
before any of this is written in code.

## Consequences

Both focused frames take the same instance and it fits both column widths, which
is the test the first pass failed.

The refusal variants — `Mode=Unavailable` and `Mode=No footage` — are widened and
otherwise untouched. Their copy is the honest outcome
[0038](0038-historical-timeline-on-the-focused-camera-view.md) built them for and
none of it changed.

The component is still the largest in the kit and now has more parts that must be
kept in step. The legend in particular is a second place the axis's vocabulary is
written down, and if a band is ever added to the axis without being added to the
legend, the legend becomes a lie rather than a help.

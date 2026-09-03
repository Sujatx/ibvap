# 38. A historical timeline on the focused-camera view

**Date:** 2026-09-02
**Status:** Accepted — marker rule superseded by [0046](0046-timeline-markers-carry-class-colour.md)

## Context

The wireframes rebuilt under
[0036](0036-wireframe-breakpoints-and-required-state-set.md) give an operator two
routes to footage, and both are bound to a single event: the crop shown in the S-04
detail panel, and "Request the full clip", which retrieves that event's own clip.
Neither lets anyone move along a camera's recording — jump to a time, watch the minute
before an alert fired, or confirm that nothing happened across a span where nothing
fired.

A recorded-video scrubber appeared in the reference mock used for that rebuild and was
refused, on the grounds that the problem statement names live analytics, alerting and
event logging and says nothing about recorded playback, so drawing one would invent a
requirement ([CLAUDE.md](../../CLAUDE.md) rule 2).
[0036](0036-wireframe-breakpoints-and-required-state-set.md) records that refusal
alongside eleven others. This decision reverses it, and the reasoning has to be better
than that the operator would like it.

The statement's own framing is the first part. It describes the existing estate as
systems that "primarily provide video recording and live monitoring capabilities", and
asks for a platform that transforms that infrastructure into an intelligent surveillance
network. Recording is not a capability IBVAP would be adding. It is already present at
every site, inside the recorder IBVAP already reads its live streams from, and the
console currently hides it. None of the eight named capabilities is a timeline — but
"improve situational awareness and response time for border security forces" is in the
expected solution, and an alert whose surrounding footage cannot be reached leaves the
operator with less context than the site's own DVR software already offers them. That is
a strange place for this product to land.

The second part is that decisions already accepted here assume an evidence surface a
fixed clip does not provide.
[0023](0023-dismissal-cause-captured-on-suppression.md) requires the operator to record
why an alert was dismissed, from a preset list — wind, animal, shadow, glare, rain.
Telling wind from a person is frequently a question of what happened in the seconds
either side of the cut rather than inside it.
[0018](0018-operator-assigned-impact-grade.md) makes the impact grade the assessor's own
judgement and never a system finding, which presumes the assessor can see enough to
judge. Both were accepted before there was any way to look outside a fifteen-second
window.

The third is that refusing costs something too.
[0034](0034-local-event-store-on-sqlite.md) already treats continuous video as its own
artefact class with its own retention clock. The footage is being kept. Declining to
surface it is a deliberate omission an operator would have to have explained to them,
not a scope boundary that explains itself.

Against all of that: this is a judgement call, and it is the same shape of argument that
could be used to justify almost anything the statement does not name. What keeps it
honest is the boundary drawn below, and the fact that PTZ control, camera configuration,
evidence export and multi-camera synchronised replay stay refused on precisely the
grounds being reversed here for one control.

## Decision

**The focused-camera view on S-02 gains a timeline beneath the video, and the S-04 event
detail gains a link into it.** It is one component with one job: move the picture in the
focused view backwards and forwards through what the recorder holds for that camera.

It is read-only against the estate. It does not change a camera or recorder setting, it
does not export, it does not control a camera's position, and it does not synchronise
playback across cameras. Those stay outside the build for the reason this decision
reverses for the timeline alone.

**Its extent is the continuous-video retention window and it draws its own edges.**
[0034](0034-local-event-store-on-sqlite.md) leaves the actual retention period to
product; whatever it is, the timeline shows where the recording begins and ends rather
than letting the operator scrub into nothing. Spans where the recorder holds no footage —
it was offline, the disk was full, the site lost power — are drawn as gaps, because a
visible gap beats a silent one, which is the same principle
[0034](0034-local-event-store-on-sqlite.md) applies to dropped queue entries.

**The axis carries the clock-trust flag.**
[0034](0034-local-event-store-on-sqlite.md) stores, for every event, whether the clock
was trustworthy when it was captured. A timeline is a clock rendered as a control, so a
span recorded while the clock was unverified is marked as such on the axis. Times an
operator may act on must not silently claim more precision than the site can support.

**Event markers carry alert-versus-logged and nothing else.** They are drawn as two
weights, never two hues:
[0030](0030-dark-console-palette-no-severity-colour.md) rule 1 makes alert versus logged
the only distinction the system itself draws, and a coloured marker track would
reintroduce the severity scale this product refuses to compute.

**Live is a fact and returning to live is a control.** A chip states whether the view is
live or how far behind it is; a button returns it to live. Under
[0031](0031-component-grammar-chip-states-fact-segmented-control-chooses.md) a chip is
never a control, so the two are not the same element. The span selector — how much time
the axis spans — is an exclusive choice from a closed set and is therefore a segmented
control, not chips.

**Where the recorder cannot serve recorded video, the timeline is refused, not faked.**
Under [0007](0007-refuse-unsupported-capabilities-not-degrade.md) an unsupported
capability is refused rather than degraded, and under
[0030](0030-dark-console-palette-no-severity-colour.md) rule 2 that refusal is
informational and must not be dressed as a fault. A recorder that will not serve playback
is a correct outcome about that estate, stated in plain language, in the place the
timeline would have been.

### What is assumed about the recorder, and what is not known

Live ingest is settled: [0035](0035-operator-console-stack-and-video-transport.md) sends
H.264 to the browser over WebRTC through an embedded gateway republishing the camera's
existing stream. **Historical playback is a different retrieval path and that path is
not yet established.** The plausible routes are ONVIF Profile G replay, a
vendor-specific RTSP playback URL carrying a time range, or reading recorder files
directly.

The development rig ([0015](0015-mvp-validated-against-development-cctv-rig.md)) is a
Dahua HD-XVR-4801H1-H, and [`dvr.py`](../../dvr.py) reaches it on the live endpoint
`/cam/realmonitor?channel=N&subtype=0`. Dahua recorders conventionally expose recorded
playback on a separate path taking a start and end time, so the route plausibly exists
here — but it is not verified on this unit, and this is the same firmware that
[0015](0015-mvp-validated-against-development-cctv-rig.md) records as returning OK for
settings it discards. Assuming it works because the vendor documents it is exactly the
mistake that decision exists to prevent.

**RFC 0001 must measure this before any timeline code is written**, in the same pass that
measures decode throughput for
[0032](0032-inference-runtime-decode-path-and-detector-licence.md). If the rig cannot
serve recorded video, the refusal state above is not a corner case — it is what the demo
shows, and that is an acceptable outcome for a decision built on
[0007](0007-refuse-unsupported-capabilities-not-degrade.md). What is not acceptable is
drawing a working timeline in hi-fi and discovering in Phase 5 that nothing can drive it.

Two further constraints follow from decisions already made. Seeking is decode-bound
before it is anything else: producing a frame at an arbitrary time means decoding forward
from the preceding I-frame, and the rig's one-second GOP
([0032](0032-inference-runtime-decode-path-and-detector-licence.md)) sets the floor on
how precisely a scrub can land. And the rig's total budget is shared across channels, so
a playback session competes with live ingest for the same recorder bandwidth rather than
running alongside it for free.

### What this does not change

This adds a control to an existing screen. It does not add a sixth screen, so
[0016](0016-mvp-ui-cut-to-five-screens.md)'s five-screen freeze stands. It does not
reopen [0017](0017-cameras-site-sketch-not-a-map.md), PTZ, camera configuration, or
evidence export, all of which remain refused. Analytics still run on the live stream
only — the timeline plays recorded video back to a person, and detection is not run
against it, which would be a materially different product.

## Consequences

The known-gap note in [ROADMAP.md](../../ROADMAP.md) Phase 2 is answered by the first of
the two paths it set out, and is replaced by a pointer to this decision.

[0036](0036-wireframe-breakpoints-and-required-state-set.md)'s Context lists a
recorded-video scrubber among the reference departures that were refused. That paragraph
stays accurate as history and is no longer in force. This decision does not otherwise
disturb 0036.

The UI kit gains a component family that was not on the gap list produced by the rebuild
— a timeline with its axis, playhead, marker track and span control — taking the missing
count from thirteen to fifteen. It is the largest single component in the kit and the
only one that owns a continuous scale, so it is the one most likely to need a second pass
once it is used at more than one width.

The retrieval dependency is real and is the weakest point of this decision. Every other
screen in the build reads from IBVAP's own store; this one reads from someone else's
recorder over a path nobody here has exercised. If RFC 0001 finds no workable route, the
timeline ships as a refusal on every camera, which is honest but is not what this
decision is for.

Adding a route from an event to its surrounding footage makes the dismissal cause
[0023](0023-dismissal-cause-captured-on-suppression.md) asks for determinable rather than
guessed. That is the practical benefit, and it is worth naming, because it also means the
cause data collected before the timeline exists is weaker evidence than the same field
collected after it.

# 53. Night-time movement is a detector-independent primitive

**Date:** 2026-09-03
**Status:** Accepted

## Context

[0013](0013-night-time-movement-detection-as-explicit-capability.md) makes
night-time movement a first-class, separately measured capability rather than a
separate "night AI model" — night-specific eligibility measured after dark,
night-scoped rules, and a published day-versus-night gap. It did not say what
actually produces the movement signal.

The obvious answer is the object detector: run YOLO on the IR frame and report
what it finds. That answer degrades badly in exactly the conditions the
capability exists for. An infrared frame at 40 m is monochrome, noisy, and often
gives the detector nothing at all — no person class, no vehicle class, no
detection to report. A capability defined as "what the detector finds at night"
is therefore a capability that quietly stops working after dark, which is the
silent degradation [0007](0007-refuse-unsupported-capabilities-not-degrade.md)
exists to prevent.

There is a second question underneath: what "night" means. The obvious answer
again is the clock, and it is again wrong. A clock says it is 19:40; it does not
say whether this particular camera has switched to infrared, which depends on the
season, the lens, the site lighting, and whether the camera happens to sit under
a floodlight.

## Decision

**Night-time movement is produced by OpenCV MOG2 background subtraction on the
downscaled frame, independent of the object detector. Night is scoped on the
measured illumination mode, not on the clock.**

MOG2 runs on every analysed frame on the CPU, at roughly 480×270, and yields a
movement mask and moving-region boxes. It reports that something in a region
moved, without any claim about what it was. That is the whole point: it survives
the conditions that defeat classification.

Illumination mode is measured per frame from chroma saturation — an infrared
frame is effectively monochrome — and stamped on the frame, the event and the
capability verdict. A rule scoped to night is active whenever the camera reports
`infrared`.

MOG2's learning rate is lowered at mode transitions, because dusk and the IR
cut-filter switching are precisely when a background model is most likely to
declare the entire frame in motion.

Movement is a primitive, not a detection class. It gets no `DetectionBox` colour
because it is a property of a region rather than an object.

## Consequences

The capability now works when classification does not, which is what 0013 asked
for. An operator can author a rule that reports movement in a zone after dark
even on a camera where the detector is refused for human detection at that
distance — and the event honestly says "movement", not "person".

Scoping on measured illumination is more accurate than a clock and also more
robust at a site whose clock is wrong, which
[0034](0034-local-event-store-on-sqlite.md) says will happen. The trade is that
"night" is now a per-camera property rather than a site-wide one: two cameras at
the same post can disagree about whether it is night, because one is under a
light. That is correct, and it will occasionally surprise someone.

Background subtraction is a decades-old technique with well-known weaknesses, and
they arrive with it: rain, moving vegetation, headlight sweep and camera shake all
produce movement. This is the noise source the mute-and-dismissal-cause flow
already exists to manage — the preset causes in
[0023](0023-dismissal-cause-captured-on-suppression.md) name wind, animal,
shadow, glare and rain for exactly this reason — but it does mean night-scoped
movement rules will be the noisiest rules the platform offers, and operators
should be told so rather than discovering it.

Adding a movement primitive that carries no class also means it cannot, on its
own, produce an event with a `primary_class`. Rules combine movement with a class
filter, and the rule's declared class is what the event records. A movement-only
event with no class does not occur, which is what keeps
[0046](0046-timeline-markers-carry-class-colour.md)'s four-colour marker rule
total.

No thermal imaging is introduced. 0013 keeps it post-MVP and this decision does
not reopen it.

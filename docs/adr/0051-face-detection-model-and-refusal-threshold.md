# 51. Face detection is YuNet, and it is refused below 24 pixels

**Date:** 2026-09-03
**Status:** Accepted

## Context

Face detection is one of the eight capabilities the problem statement names, and
[0008](0008-face-detection-unconditional-gated-recognition.md) ships it
unconditionally while blocking recognition in this build.
[0032](0032-inference-runtime-decode-path-and-detector-licence.md) chose a
YOLO-family detector for people and vehicles and said nothing about faces — a
general object detector at 640 px input will not reliably find a face that
occupies twenty pixels of it.

So a second model is needed, and the choice is constrained in an unusual way:
because 0008 forbids recognition, accuracy beyond "there is a face here, in this
box" buys nothing. There is no alignment step, no embedding, no gallery and no
matching. The requirement is a box.

The candidates were YuNet (libfacedetection, in the OpenCV Zoo), SCRFD from
InsightFace, and RetinaFace. SCRFD is measurably better at small scales. Its
weights carry a non-commercial research restriction.

## Decision

**Face detection uses YuNet, as an ONNX artefact loaded by ONNX Runtime. A camera
is refused for face detection when a face at its reference distance would be
narrower than 24 pixels in encoded geometry.**

YuNet is chosen for three reasons in this order. Its licence is MIT, which keeps
this model out of the licence conversation entirely — the AGPL encumbrance stays
confined to the general detector, and a force needing a non-copyleft deployment
has one artefact to swap, not two. It is about 85 KB and costs a couple of
milliseconds per crop, which is what makes it affordable inside the gated cascade
where it runs only on person boxes. And its output — a box, plus five landmarks
this build discards — is exactly the requirement and nothing more.

The 24-pixel floor comes from YuNet's own documented operating range rather than
from a measurement of this estate. It is applied per camera at commissioning by
the capability measurement pass, and again per object at runtime, because a
camera that clears the floor for a person at 10 m fails it for the same person at
40 m.

The landmarks are discarded rather than stored. Their only purpose is to align a
face for recognition, and storing them would create the input to a capability
0008 forbids.

## Consequences

Face detection will be refused on most cameras of a typical existing estate, and
that is the correct outcome rather than a disappointment. At 1080N the encoded
frame is 960 px wide; a 24-pixel face is 2.5% of that width, which means a person
close to the camera on a path pointed at it. A wide-area camera watching a
fenceline will not clear the floor, and saying so is what
[0007](0007-refuse-unsupported-capabilities-not-degrade.md) is for.

Choosing the weaker model on licence grounds costs recall at small scales. That
cost is bounded by what the capability is allowed to do: a missed face at 30
pixels matters if you are matching identities and matters much less if you are
recording that a face was present. Had 0008 permitted recognition, this decision
would likely have gone the other way, and the reasoning would have had to include
buying a licence.

Nothing here creates a path to recognition. There is no embedding model, no
gallery table, and no matching code, and adding any of them requires the four
conditions 0008 sets and a new decision — not a configuration change.

The floor is a starting threshold from documentation, not a measurement. It
should be validated against the rig once
[RFC 0006](../rfcs/0006-detection-and-analytics-primitives.md) has models
running, and revised by a superseding ADR if the measured behaviour differs.

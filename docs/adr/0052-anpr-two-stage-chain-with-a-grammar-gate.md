# 52. ANPR is a two-stage ONNX chain, and its grammar gate rejects but never repairs

**Date:** 2026-09-03
**Status:** Accepted

## Context

Automatic Number Plate Recognition is named in the problem statement and is the
capability the whole project premise is most exposed on: the platform claims to
deliver ANPR without dedicated ANPR hardware, on cameras that were installed to
watch a fence. Nothing in the stack ADRs chose a model for it.

The physics is unforgiving. The rig encodes 1080N — 960 pixels of real horizontal
detail stretched to 1920 on display. Reading a plate needs roughly 16 pixels of
character height, which on Indian plate proportions means about 110 pixels of
plate width. On a 960-pixel-wide frame that is more than a tenth of the image:
a vehicle close to the camera, on a road pointed at it.

There is an obvious temptation here, and it is worth naming because it is the
reason this ADR exists. Plate OCR output can be made to look far better than it
is by post-processing it against the known format — mapping `O` to `0`, `I` to
`1`, `8` to `B` wherever the grammar says a digit or a letter belongs. Every
accuracy metric improves. The reads become evidence that says something the
pixels did not.

## Decision

**ANPR is a two-stage chain of ONNX artefacts — a small YOLO-family plate
detector, then a `fast-plate-ocr` recognition model — both Apache-2.0, both run
only inside a vehicle box that clears a pixel floor.**

**The Indian plate grammar is a confidence gate, not a corrector.**

The grammar knows the civilian formats — two-letter state code, one or two RTO
digits, one to three series letters, four digits; and the BH series' distinct
shape. Its entire authority is this:

> A read that does not match a known format is reported with reduced confidence
> and marked `grammar_matched: false`. It is **never** rewritten to make it
> match.

No character substitution of any kind, in either direction. The gate may lower
confidence in a read; it may not improve one.

A camera is refused for ANPR when a plate at its reference distance would be
narrower than about 110 pixels in encoded geometry. At runtime the same
arithmetic gates each vehicle box, and a plate is read once per track, re-read
only when a materially better view arrives.

PaddleOCR is the documented fallback if Indian formats read poorly on the rig.
Because the model is an artefact and not a library call, that swap is a manifest
change.

## Consequences

ANPR will be refused on most cameras of a typical estate. That is the honest
result of the arithmetic, and presenting the capability as generally available
would be exactly the unqualified claim
[0002](0002-differentiate-on-deployment-not-benchmark-accuracy.md) rules out. The
capability ships, it works where the pixels exist, and it says so where they do
not.

Refusing to repair reads makes the published accuracy worse than a competitor's,
measured naively. It is the right trade for a platform whose output may be used
to justify stopping a vehicle: a plate the system invented is worse than no plate
at all, and it is worse in a way nobody downstream can detect. The
`grammar_matched` flag travels on the event and in the outbound payload so a
consumer can decide for itself what to do with an unverified read.

Two models on the ROI path cost VRAM and latency, which is why both are gated
twice — by the camera's capability verdict and by the object's pixel size — and
why a read is not repeated per frame. Without those gates a single vehicle in
shot for ten seconds would cost fifty OCR passes to produce the same string.

Watchlists remain out of scope. This build reads a plate and records it; matching
a read against a list of plates of interest is a product capability nobody has
specified, and inventing it would breach [CLAUDE.md](../../CLAUDE.md) rule 2.

The pixel floors are derived from plate geometry and the models' documented
ranges, not measured on this estate. They are to be validated against the rig and
revised by a superseding ADR if reality differs.

# 60. A file-backed frame source, for testing and demonstration against footage the rig cannot produce

**Date:** 2026-09-03
**Status:** Accepted, extends 0015

## Context

[RFC 0001](../rfcs/0001-video-ingest-capability-measurement-and-playback.md)
defines ingest as one `FrameSource` implementation: a live RTSP session against
the development rig. The rig is one Dahua recorder encoding 1080N (960 px of
real horizontal resolution) across five wide-area channels —
[RFC 0006](../rfcs/0006-detection-and-analytics-primitives.md) already
documents that this geometry refuses ANPR and frequently refuses face
recognition on most of what the rig can show. None of that is a defect in the
design — RFC 0001's capability-measurement pass exists to say exactly this,
per camera, honestly. But it means the rig alone can only
demonstrate a capability being *refused*, never *working*, and a platform whose
only fixture refuses everything cannot be validated end to end.

Testing or demonstrating a capability at all requires footage where the pixels
it needs actually exist: a close, well-lit plate; a face at recognition-grade
resolution; a vehicle crossing a fence in daylight and at night. That footage
does not need to come from this developer's own cameras. The platform's job is
to analyse whatever a standard IP camera would have produced, and a recorded
clip is indistinguishable from that at the frame level.

## Decision

**A second `FrameSource` implementation reads frames from a local video file
through the same PyAV decode call ingest already makes for a live stream,
rather than opening an RTSP session. It participates in the same
capability-measurement pass, the same analytics cascade, and the same rule
engine as a live camera — nothing downstream distinguishes a `Frame` that came
from a file from one that came from RTSP.**

The file source has no reconnect state machine and no backoff — a file does
not drop a connection — and it is not subject to the recorder's shared-
bandwidth ceiling, which is exactly why it can validate a capability the live
rig cannot. It is addressed as a `FrameSource` the same way a camera is; RFC
0001's `Frame` and `CapabilityVerdict` contracts are unchanged by its existence,
which is the entire point of the `FrameSource`/`FrameSink` boundary RFC 0001
already drew.

Fixture footage must be footage this project has the right to hold and, where
committed, to redistribute — stock or Creative-Commons traffic, checkpost, or
dashcam material, not an arbitrary scrape — held outside git as a local
fixtures directory, the same pattern
[0058](0058-model-artefacts-are-versioned-files-with-a-manifest.md) already
established for model artefacts: a large binary the repository points at
rather than vendors.

## Consequences

RFC 0001 and RFC 0006's honest refusals on the live rig stand unchanged. A file
source does not make ANPR "work on the rig" — it demonstrates that ANPR works
on footage that clears the floor RFC 0006 already states, which is the
validation the maturity table's claims need to be more than assertions.

A fixture library becomes possible: short clips exercising each of the eight
capabilities at a resolution that clears its floor, replayed deterministically
in CI or by hand, independent of whether the developer's home rig is reachable.
That library does not exist yet — this ADR authorises the mechanism, not the
specific clips; assembling the library is separate work.

This does not change what ships to a border post. A deployment ingests from
real cameras only; the file source is a development and validation tool, named
as such in RFC 0001.

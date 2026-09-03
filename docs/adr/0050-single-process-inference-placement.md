# 50. Ingest, inference and rules run in one process on one node

**Date:** 2026-09-03
**Status:** Accepted

## Context

[0032](0032-inference-runtime-decode-path-and-detector-licence.md) deliberately
left two questions open: whether ingest and inference are one process or two, and
where inference runs relative to the cameras.
[docs/architecture/README.md](../architecture/README.md) §4 and §8 have carried
"inference placement remains open" since, and
[RFC 0001](../rfcs/0001-video-ingest-capability-measurement-and-playback.md)
is where it had to close.

The facts that decide it are all in 0032 already. Decode is the binding compute
cost, not inference. The target machine has 4 GB of VRAM, shared between NVDEC
decode sessions and every model loaded at once. Analysing fewer frames does not
decode fewer frames, because P-frames depend on their predecessors. And the
deployment is one site, one machine, one operator
([0014](0014-mvp-scoped-to-one-deployment-site.md)).

The genuine argument for splitting is fault isolation: a decoder crash taking
down the API is a bad failure at an unattended post. The argument against is that
a split adds a frame copy and a serialisation boundary to the one resource that
has none to spare, and does it now, for a benefit that matters later.

## Decision

**Ingest, decode, inference and rule evaluation run in a single Python process on
a single site machine. Inference is central, not at the edge.**

Two narrow interfaces are the only contact between the ingest side and the
analytics side:

```
FrameSource   yields Frame objects for one camera
FrameSink     accepts a Frame, returns nothing
```

Everything ingest knows about analytics is `FrameSink`; everything analytics
knows about ingest is `Frame`. Nothing else crosses.

Within the process, each camera decodes on its own OS thread — PyAV releases the
GIL for the duration of the FFmpeg call — and hands frames to a single-slot
buffer that a writer overwrites rather than blocks on. Analytics runs on its own
thread against one ONNX Runtime session per model.

`go2rtc` remains a separate process. It is a third-party binary that republishes
camera streams to the browser and touches nothing in this pipeline.

## Consequences

The frame never leaves the process, so there is no copy, no serialisation and no
shared-memory segment to manage. On a machine where decode and model weights
compete for the same 4 GB, that is the difference the decision is being made for.

Fault isolation is genuinely worse than a split would give. A crash in the
decoder takes the API down with it, and at an unattended post that means the
console is unreachable until something restarts the process. The mitigation is
process supervision, which belongs to the deployment design that
[0033](0033-backend-framework-packaging-and-auth.md) already defers — this
decision makes supervising it more important, not less, and that obligation is
recorded in the architecture's risk section rather than left implicit.

The split stays cheap. Because `FrameSource` and `FrameSink` are the only
boundary, moving analytics into a second process means writing one adapter that
puts frames through shared memory or a socket instead of a queue. That is a day's
work rather than a redesign — which is what "split-ready" has to mean to be worth
claiming. A component that reaches around those interfaces, for instance by
having the rule engine read a camera's connection state directly, breaks the
property and is a defect in the same sense 0032 calls a runtime Ultralytics
import a defect.

Choosing central inference does not close the edge question forever. It closes it
for a deployment of one site and one machine, which is the only deployment
specified. An estate large enough that decode cannot be centralised would need
the split, and the boundary above is what makes that a transport change.

[docs/architecture/README.md](../architecture/README.md) §4 and §8 no longer list
inference placement as open.

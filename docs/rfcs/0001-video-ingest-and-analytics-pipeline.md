# 0001. Video ingest and analytics pipeline

**Status:** Draft
**Author:** IBVAP project
**Date:** 2026-08-27

## Context and scope

This is the first design doc for IBVAP: how a camera's video actually gets
from an existing recorder into a detection, a rule evaluation, and a
capability verdict. It covers ingest (RTSP/ONVIF, including analog channels
behind a DVR/XVR), the per-camera capability-measurement pass that
[ADR 0007](../adr/0007-refuse-unsupported-capabilities-not-degrade.md)
requires before any capability is claimed, and where inference runs relative
to ingest. It does not cover the rule engine's condition language, the event
store schema, the web application, or the egress publisher in detail — those
get their own RFCs once this one is accepted.

Grounded in the [Technical Feasibility](https://app.notion.com/p/3c986dda46e281a7a1c3d87623970822?pvs=204)
research (Notion) and the constraints in
[docs/architecture/README.md §2](../architecture/README.md#2-constraints),
in particular: decode, not inference, is the binding compute cost; the
recorder in front of a camera can be a harder limit than the camera itself;
and a device's advertised configuration must be verified by read-back, not
trusted.

## Goals and non-goals

**Goals**

- Ingest both native IP cameras (RTSP/ONVIF) and analog channels behind an
  existing DVR/XVR/NVR, without reconfiguring either.
- Measure, per camera, what it actually delivers — resolution, frame rate,
  day/night behaviour — rather than trust what it advertises.
- Turn that measurement into a per-camera, per-capability verdict (eligible /
  eligible-but-degraded / refused) before any capability is offered to an
  operator.
- Keep decode cost, the proven binding constraint, in view of every design
  choice — not just inference cost.

**Non-goals**

- Choosing a specific model or model family for any of the eight
  capabilities — that is a separate decision once this pipeline shape is
  settled.
- A compatibility lab / tested-device list — real engineering effort other
  vendors sink years into; out of scope for this design doc and for the MVP.
- Standards-based egress (ONVIF Profile M, MISB ST 0903) — deferred per
  [ADR 0006](../adr/0006-c2-integration-via-generic-event-contract.md).

## Design

### Ingest

RTSP-over-TCP is the default transport, not RTSP-over-UDP. The development
rig demonstrates UDP dropping badly on real hardware, and forcing TCP is the
safer default until a wider device population says otherwise. An explicit
socket timeout is mandatory on every stream — an unresponsive channel must
error, not block indefinitely (observed on `dvr.py`'s
`OPENCV_FFMPEG_CAPTURE_OPTIONS` handling).

RTSP path templates are not standardized across vendors (Hikvision, Dahua,
Reolink and Axis all differ). Ingest needs a small, explicit per-vendor path
table from day one, plus a manual "paste the full stream address" fallback —
this is the PRD's stated commissioning path (add a camera by pasting its
existing stream address), and it is also the escape hatch for any camera the
vendor table doesn't cover.

Where ONVIF is available, ingest reads the device's media profiles directly
(main stream + sub-stream, with their actual encoding and RTSP URL) rather
than guessing. Where a sub-stream exists at usable resolution, analytics
decode against the sub-stream and recording-equivalent quality is left
untouched on the main stream — this is the cheapest lever available, because
it cuts decode cost roughly by the pixel ratio, not by touching inference at
all. Sub-stream availability and resolution are not assumed; they're read and
measured per camera.

### DVR/XVR-behind-analog handling

Where a camera sits behind a DVR/XVR (the development rig's own topology),
the recorder — not the camera — is the resource to interrogate. Its
per-channel and shared budget (bitrate, fps) must be read back after any
configuration attempt, not trusted from the response, because the rig's
firmware has been shown to report success for settings it silently discards.
"1080" must not be trusted as 1080p — it may be 1080N (960 horizontal
pixels, stretched to restore aspect ratio, manufacturing no additional
information). Effective resolution is measured from the decoded frame, not
read from a device's self-reported setting.

### Capability measurement pass

Before any capability is offered for a camera, a measurement pass runs
against that camera's actual delivered stream and produces one verdict per
(camera, capability) pair:

1. Decode a sample window of the live stream.
2. Measure effective resolution (not advertised resolution), sustained
   analysed frame rate, and day/night behaviour.
3. Compare against each capability's stated floor (e.g. tracking needs
   roughly 3–5 analysed fps; ANPR needs pixel density in the range the DORI/
   OODPCVS standards define for plate-character resolution).
4. Record the verdict, and — for a refusal — the plain-language reason a
   non-technical operator can read.

This pass is re-run on demand (an operator can ask "why is this refused?"
and re-trigger it after, say, repositioning a camera), and its output is
what [ADR 0007](../adr/0007-refuse-unsupported-capabilities-not-degrade.md)'s
inline refusal on Live View actually displays. An override exists, requires a
named authority, and permanently marks resulting events — per ADR 0007 — but
the override mechanism itself is out of scope for this RFC.

### Inference placement (edge vs. central)

Not decided in this RFC — flagged as the open question with the largest
consequence for deployment topology (see
[docs/architecture/README.md §7](../architecture/README.md#7-deployment-view)).
What is decided here: whichever placement is chosen, decode happens as close
to ingest as possible and is not repeated — decode, not inference, is the
proven binding cost, and P-frame dependency means arbitrary frame sampling
does not reduce it. A design that decodes once and fans out decoded frames to
one or more inference passes is preferred over one that re-decodes per
capability.

## System-context diagram

See [docs/architecture/diagrams/c4-l1-context.md](../architecture/diagrams/c4-l1-context.md)
for the system boundary, and
[docs/architecture/diagrams/c4-l2-container.md](../architecture/diagrams/c4-l2-container.md)
for the proposed container split this RFC assumes (Ingest service → Inference
service → Rule engine).

## APIs

Not designed in this RFC. The ingest→inference and inference→rules
boundaries need an internal contract (decoded-frame handoff, detection
output shape); the rule engine's own API is PRD §6.2's concern, covered in a
future RFC.

## Data storage

Not designed in this RFC. What must be storable, established here: the
capability verdict per (camera, capability) pair, with its measured basis
(resolution, fps, day/night) and timestamp, so a verdict can be shown as
current or stale rather than as a one-time gate.

## Alternatives considered

| Alternative | Why not (for now) |
|---|---|
| Trust device-advertised resolution/fps instead of measuring | Falsified directly by the development rig — a device that reports "1080" delivering 960 horizontal pixels, and firmware accepting settings it discards |
| Decode at full resolution for every capability, ignore sub-streams | Works, but discards the cheapest available cost reduction for no benefit |
| A single combined ingest+inference process per camera | Simpler to build first, but re-decodes if more than one capability needs the frame; kept as a fallback if the two-service split proves premature |
| Standards-based ingest only (ONVIF Profile M) | No vendor in the competitive survey emits it; a vendor path-table + manual fallback covers today's real estate, ONVIF is used where available, not required |

## Cross-cutting concerns

- **Read-only guarantee.** Every ingest and measurement operation must be
  provably non-mutating against the camera/recorder, or explicitly flagged
  and gated behind the named-authority override if it configures anything
  (e.g. requesting a sub-stream that must first be enabled on-device).
- **Honest refusal.** The measurement pass is the mechanism that makes
  [ADR 0007](../adr/0007-refuse-unsupported-capabilities-not-degrade.md)
  real rather than aspirational — a refusal without a measured basis is not
  acceptable.
- **Disconnection survival.** Ingest must reconnect cleanly after a link
  drop and must not lose or duplicate an in-flight measurement or detection
  when it does, per the 72-hour disconnection requirement.

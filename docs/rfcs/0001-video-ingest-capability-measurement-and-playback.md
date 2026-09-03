# 0001. Video ingest, capability measurement, and playback retrieval

**Status:** Accepted
**Author:** Sujat
**Date:** 2026-09-03

## Context and scope

Everything IBVAP does begins with a decoded frame, and nothing about how that
frame is obtained has been designed yet. The stack is chosen —
[ADR 0032](../adr/0032-inference-runtime-decode-path-and-detector-licence.md)
settles PyAV, NVDEC with a software fallback, and ONNX Runtime — but three
questions it deliberately left open all live here:

- whether ingest and inference are one process or two;
- where inference runs relative to the cameras;
- whether the recorder will serve *recorded* video at all, which
  [ADR 0038](../adr/0038-historical-timeline-on-the-focused-camera-view.md)
  needs before the focused-camera timeline can be built.

A fourth obligation arrives from
[ADR 0007](../adr/0007-refuse-unsupported-capabilities-not-degrade.md): a
capability a camera cannot support must be refused rather than quietly
degraded. That requires a measurement pass, and nothing has specified what it
measures or how it decides.

This RFC covers the path from an RTSP URL to a decoded, timestamped frame handed
to analytics, plus the per-camera capability verdicts that decide what analytics
is even offered. It does not cover the models that consume the frames
([RFC 0006](0006-detection-and-analytics-primitives.md)), rule evaluation
([RFC 0002](0002-rule-evaluation-engine.md)), the store's schema
([RFC 0003](0003-event-store-and-alert-state.md)), the HTTP surface
([RFC 0004](0004-web-application-and-api-contracts.md)) or egress
([RFC 0005](0005-c2-event-egress-publisher.md)).

The development rig is the only estate available to design against: five live
channels behind a Dahua HD-XVR-4801H1-H, TCP-only RTSP, a fixed 1080N anamorphic
encode (960×1080 stored, 1920×1080 displayed), a shared 12,288 kbps / 120 fps
budget across eight channels, and firmware that reports success for settings it
silently discards
([ADR 0015](../adr/0015-mvp-validated-against-development-cctv-rig.md)). The
real target estate is unmeasured, so every number here is either measured on the
rig and labelled as such, or a threshold the measurement pass applies per camera
rather than an assumption baked into the design.

## Goals and non-goals

**Goals**

1. A per-camera connection lifecycle that survives a recorder which drops
   channels, stalls, and lies about its own configuration.
2. A capability measurement pass producing a verdict per camera per capability,
   with a reason sentence the console can display verbatim.
3. A decision on inference placement, closing the question
   [architecture §4 and §8](../architecture/README.md) mark Open.
4. A frame timestamp with a stated provenance, and the clock-trust flag
   [ADR 0034](../adr/0034-local-event-store-on-sqlite.md) stores on every event.
5. A recorded-video retrieval path, or a written refusal.
6. A backpressure policy that says exactly what is discarded when the machine
   cannot keep up.
7. A file-backed frame source, so a capability the rig's own cameras cannot
   demonstrate can still be validated against footage that clears its floor.

**Non-goals**

- Choosing or tuning models. RFC 0006 owns that, and consumes the frame budget
  this RFC's measurement produces.
- Deciding containerisation or process supervision.
  [ADR 0033](../adr/0033-backend-framework-packaging-and-auth.md) defers both,
  and nothing here reopens them.
- Writing to the estate. IBVAP never reconfigures a camera or recorder and never
  touches recording
  ([ADR 0004](../adr/0004-function-without-remote-monitoring-layer.md)). The
  rig's own `dvr.py --tune` is the developer's tool, not a product capability.
- Multi-site aggregation. One site, one machine
  ([ADR 0014](../adr/0014-mvp-scoped-to-one-deployment-site.md)).

## Design

### Inference placement: one process, one node, split-ready

**Ingest, decode, inference and rule evaluation run in a single Python process
on a single site machine.**

Decode is the binding cost, not inference — ADR 0032 measures roughly 8 ms per
small-YOLO inference against a decode workload that is unmeasured and expected
to dominate. Both compete for the same 4 GB of VRAM on the target machine, and
NVDEC sessions and model memory come out of the same budget. A two-process split
would add a frame copy and a serialisation boundary to the one resource that
cannot spare either, in exchange for isolation this deployment does not yet need.

The split stays cheap to make later. Modules communicate through two narrow
interfaces and nothing else:

```
FrameSource   →  yields Frame objects for one camera
FrameSink     →  accepts a Frame, returns nothing
```

Everything ingest knows about analytics is `FrameSink`; everything analytics
knows about ingest is `Frame`. Replacing the in-process queue between them with
shared memory, a socket, or a network hop is then a change to one adapter rather
than a rewrite — which is what "split-ready" has to mean to be worth claiming.

This closes the placement question. Recorded as an ADR alongside this RFC.

### Threading model

`asyncio` runs the API and the egress publisher.  Decode does not belong on that
loop: PyAV's decode calls block, and one stalled channel on the event loop stalls
everything. Each camera therefore gets a dedicated OS thread, which is safe
because PyAV releases the GIL for the duration of the FFmpeg call.

```
per camera:  [decode thread] → latest-frame slot (size 1) → [analytics worker]
```

The slot holds exactly one frame and a writer overwrites rather than blocks. A
slow consumer therefore drops frames instead of growing a queue, and one dead
channel cannot stall the others — the same shape `dvr.py` already arrived at, for
the same reasons, and the per-channel isolation ADR 0032 asks to be
re-established.

Analytics runs on its own thread with a single ONNX Runtime session per model,
batching across cameras where the model allows it. RFC 0006 owns that side.

### Connection lifecycle

```
resolving → connecting → measuring → streaming
                ↑            ↓           ↓
             reconnecting ←──┴───────────┘
                ↓
             stopped
```

| State | Meaning | Console shows |
|---|---|---|
| `resolving` | Working out the stream URI, by ONVIF or configured template | Connecting |
| `connecting` | Opening the RTSP session | Connecting |
| `measuring` | First frames arriving; capability pass running | Measuring |
| `streaming` | Delivering frames to analytics | Live |
| `reconnecting` | Lost the stream; backing off before retry | Reconnecting |
| `stopped` | Deliberately stopped, or permanently failed | Offline |

`degraded` is deliberately absent. A camera either delivers frames or it does
not; a camera that delivers frames but cannot support a capability is a
*refusal* on that capability, not a degraded camera, and that is recorded on the
verdict rather than on the connection.

Reconnection backs off 1 s → 15 s, doubling, and resets on a successful frame.
The ceiling is low on purpose: at a border post, a camera that comes back should
be picked up in seconds, and the recorder is on the same LAN.

### Transport options

Read from `dvr.py` as prior art rather than inherited as code, because IBVAP's
ingest is PyAV and `dvr.py` is OpenCV:

| Option | Value | Why |
|---|---|---|
| `rtsp_transport` | `tcp` | UDP drops badly on this recorder (ADR 0015) |
| `timeout` | `8000000` µs | Without it a dead channel blocks the read forever |
| `max_delay` | `500000` µs | Bounds reordering latency |
| `buffer_size` | `1048576` bytes | A bounded buffer; a stalled consumer cannot grow memory |
| `fflags` | `nobuffer` | Live view wants latency, not smoothness |

### Discovery

Two routes, tried in order, with the result cached per camera:

1. **ONVIF.** WS-Discovery to find devices on the LAN, then `GetProfiles` and
   `GetStreamUri` for the main and sub streams. This is what makes the platform
   work against an estate nobody has enumerated by hand.
2. **Configured template.** A per-recorder URL template with `{channel}` and
   `{subtype}` placeholders, for devices whose ONVIF is absent or partial. The
   rig needs this route: its firmware is already on record for reporting success
   on settings it discards, and its ONVIF conformance is unverified.

Credentials are held once per recorder, not per camera, and never appear in a
log line or an API response. The URL is redacted at every boundary the way
`dvr.py` already redacts it for its banner.

### File-backed ingest

A second `FrameSource` implementation reads frames from a local video file
through the same PyAV decode call, rather than opening an RTSP session
([ADR 0060](../adr/0060-file-backed-frame-source-for-testing.md)). It has no
`resolving`/`connecting`/`reconnecting` states — a file does not drop a
connection — and no reconnect backoff; otherwise it produces the same `Frame`
objects, in the same fields, and is measured by the same capability pass as a
live camera. Nothing downstream — the cascade, the rule engine, the event
store — can distinguish the two.

This exists because the development rig cannot demonstrate every capability:
its five channels are wide-area views that measure below the ANPR and
face-recognition floors RFC 0006 sets, so the rig alone can only show those
two capabilities being *refused*, never *working*. A file source pointed at
footage that clears the floor — a checkpost clip, a well-lit close pass — is
what makes the maturity table's "ships" claims checkable rather than merely
argued. Fixture footage lives outside git as a local, gitignored directory,
the same way `models/` is not committed
([ADR 0058](../adr/0058-model-artefacts-are-versioned-files-with-a-manifest.md));
only footage this project has the right to hold, and to redistribute where a
fixture is shared, is used.

A file source is a development and validation tool. It never ships to a
deployment, which ingests from real cameras only.

### Capability measurement

The pass that makes ADR 0007 real. It runs on connect, and again when the
measured inputs change materially or an operator asks for a re-measure.

**What is measured, from the stream itself:**

| Input | Source | Note |
|---|---|---|
| Encoded geometry | Codec context | The rig reports 960×1080, not 1920×1080 |
| Display geometry | Encoded geometry × sample aspect ratio | The anamorphic stretch |
| Delivered frame rate | Frames over a 10 s window | Not what the recorder claims |
| GOP length | Frames between key frames | The rig runs a 1 s GOP |
| Bitrate | Bytes over the same window | Against the recorder's shared budget |
| Illumination mode | Chroma saturation across the frame | Distinguishes IR/monochrome from colour |
| Noise floor | Temporal variance in a static region | Low-light degradation, measured after dark |

**What is declared, once, by whoever commissions the camera:**

- a reference distance in metres — the range at which this camera is expected to
  do useful work;
- the horizontal field of view in degrees at that distance, or the scene width in
  metres, whichever the commissioner can actually state.

Nothing else. Commissioning must be possible by a non-specialist in under an
hour with no site survey, so the pass asks for two numbers a person can pace out
or read off a lens, and derives the rest.

**How a verdict is reached.** Pixel density at the reference distance, in pixels
per metre, is the encoded horizontal resolution divided by the scene width:

```
px_per_m = encoded_width / scene_width_m
```

That figure is compared against the DORI bands of IEC/EN 62676-4 — detection,
observation, recognition, identification — and against a per-capability floor
that RFC 0006 owns and this pass merely applies. The verdict is:

```
supported   the measured inputs clear the floor for this capability
refused     they do not, and the reason names which input fell short
```

A refusal carries a full sentence, written for the operator, not a code:

> ANPR is refused on Gate North. At 40 m this camera resolves about 12 pixels of
> plate height; reading a plate needs at least 20. Moving the camera closer or
> narrowing its field of view would change this.

That sentence is stored on the verdict and rendered verbatim by the console's
`CapabilityNotice`. The console never composes its own wording, because a
refusal that is phrased differently in two places is a refusal nobody trusts.

**`face_recognize` carries a second gate.** Every other capability is refused
or supported purely on measured pixels. `face_recognize` is refused outright,
on every camera, whenever the system-wide `watchlist_config` is not complete
and enabled ([ADR 0059](../adr/0059-face-recognition-ships-against-a-configured-watchlist.md)),
before pixels are even considered — the reason sentence names which of the two
gates actually failed, so "recognition is not configured for this deployment"
and "this camera's face resolution is too low for recognition" are never
conflated into one refusal.

**Night is measured separately.** A camera that supports human detection in
daylight may not after dark, so eligibility is measured once in each illumination
mode and the verdict carries which mode it was taken in
([ADR 0013](../adr/0013-night-time-movement-detection-as-explicit-capability.md)).
A camera never measured after dark says so rather than assuming its daylight
verdict holds.

**Override.** ADR 0007 allows a named authority to override a refusal. The
override records who, when, and why, and every event produced under it is
permanently marked. Overriding does not change the verdict — it records a
decision to proceed against it.

### Frame timestamping and clock trust

Every frame carries a capture time, and every capture time carries a statement
about how much it can be trusted.

The preferred source is the RTCP sender report, which maps the stream's RTP
timestamps onto the sender's wall clock — that is the recorder's own idea of when
the frame was captured. Where no sender report arrives within the first few
seconds, the fallback is local arrival time minus a measured transport latency,
and the frame is marked as locally timed.

The clock is **suspect** when any of the following holds:

- no RTCP sender report was received for this stream;
- the recorder's clock differs from the platform's by more than 5 seconds;
- the platform's own clock stepped since the last frame (a reboot with no RTC,
  or an NTP correction);
- the stream's timestamps went backwards.

The flag propagates: a frame marked suspect produces an Event marked suspect,
and the timeline draws the affected span as an unverified-clock band. A site that
reboots with a wrong clock produces evidence with a wrong time; marking it is the
only honest option, and it is what ADR 0034's flag is for.

### Backpressure

When analytics cannot keep up, **frames are discarded, never cameras**.

Dropping a camera concentrates the whole loss on one part of the site, which is
precisely the failure that surveillance cannot tolerate — a blind channel is
worse than a slow one everywhere. Dropping frames spreads the loss evenly and
keeps every camera live.

The mechanism is already in the threading model: the latest-frame slot means the
analytics worker always gets the newest frame and older ones are overwritten. No
queue grows, no memory climbs, and the drop is counted per camera so the console
can show *analysed fps* alongside *delivered fps* rather than implying they are
the same number.

Two floors constrain how far this can go. Analysing fewer frames does not decode
fewer frames, because P-frames depend on their predecessors — the decode cost is
paid regardless. And below roughly 3 analysed frames per second, multi-object
tracking loses identity association, so a rule that depends on a track (dwell,
direction of crossing) stops being trustworthy. The pass therefore records the
analysed rate on the camera, and RFC 0002 refuses track-dependent rules on a
camera that cannot sustain it.

### Recorded-video retrieval

ADR 0038 puts a read-only historical timeline on the focused-camera view, and
records that the retrieval path is unverified. Three routes are plausible:

| Route | Mechanism | Cost |
|---|---|---|
| ONVIF Profile G | `GetReplayUri` against a recording token, seeking with an RTSP `Range` header | Standard, but many recorders advertise it and implement it partially |
| Vendor RTSP | `/cam/playback?channel=N&starttime=…&endtime=…` | Works when it works; vendor-specific and undocumented |
| Recorder files | The `mediaFileFind` CGI index, then reading the files | Most fragile; may return an index with no readable path |

Which route works, if any, is a per-deployment fact rather than a design
choice: at commissioning, the platform tries all three against whichever
recorder the site actually has and records which, if any, returns a seekable
stream, plus time-to-first-frame — the number that decides whether seeking is
usable or merely possible. A result measured against one recorder does not
generalise to a different vendor's firmware, so this is evaluated per site, not
asserted once here.

Whichever route wins, three constraints hold. Playback is read-only and offers no
export. Seeking is decode-bound against a 1-second GOP and competes with live
ingest for the recorder's shared bandwidth, so at most one playback session runs
at a time and the live channels keep priority. And analytics never runs against
recorded video — the timeline shows what was recorded and the markers on it come
from Events already written live.

**If no route returns video, the timeline is refused on every camera** and says
so in the same voice every other refusal uses. That is the ADR 0007 outcome, and
it is written into RFC 0004's timeline endpoints as a first-class response rather
than an error.

This section names three candidates and no fixed winner, deliberately: the
right answer is a property of the recorder a deployment actually has, not of
this document.

### Decode throughput

Decode capacity is likewise a property of the machine and the specific
recorder's bandwidth ceiling together, not a single number this RFC can assert
once and reuse across every deployment — a result measured against one
developer's residential recorder does not generalise to a BOP's. What does
generalise is the observability this RFC already commits to
(Cross-cutting concerns, below): analysed fps, delivered fps, dropped-frame
count and reconnect count, continuously, per camera. An under-provisioned site
shows up there, in production, as a per-site fact surfaced through the same
`CapabilityVerdict` machinery every other refusal uses — not as a benchmark
number asserted in this document and then hoped to hold everywhere.

RFC 0006 sizes its frame budget against the 3 fps tracking floor and the
cascade's own estimated headroom
([ADR 0032](../adr/0032-inference-runtime-decode-path-and-detector-licence.md)'s
roughly five-times margin), not against a measurement taken once against any
one recorder.

## System-context diagram

Where this sits in the whole system: the
[container view](../architecture/diagrams/c4-l2-container.md).

The detailed diagrams for this RFC — the camera connection state machine and the capability-measurement flow — are still owed, and are tracked
as remaining Phase 3 work rather than assumed to exist.

## APIs

Two internal interfaces, and the surface they feed.

```python
@dataclass(frozen=True, slots=True)
class Frame:
    camera_id: int
    captured_at: datetime          # UTC, from the RTCP sender report where available
    clock_trusted: bool            # False marks the whole downstream chain
    sequence: int                  # monotonic per camera, gaps mean dropped frames
    encoded_width: int             # 960 on the rig
    encoded_height: int            # 1080 on the rig
    display_width: int             # 1920 on the rig, after the anamorphic stretch
    display_height: int
    is_key_frame: bool
    illumination: Literal["colour", "infrared"]
    image: np.ndarray              # BGR, in encoded geometry -- never upscaled here


class FrameSource(Protocol):
    def frames(self) -> Iterator[Frame]: ...
    def stop(self) -> None: ...


class FrameSink(Protocol):
    def submit(self, frame: Frame) -> None: ...   # never blocks; may discard
```

```python
@dataclass(frozen=True, slots=True)
class CapabilityVerdict:
    camera_id: int
    capability: Literal["human_detect", "vehicle_detect", "face_detect",
                        "face_recognize", "anpr", "night_movement",
                        "recorded_playback"]
    supported: bool
    reason: str | None             # a full sentence when supported is False
    measured_at: datetime
    illumination: Literal["colour", "infrared"]
    px_per_m_at_reference: float
    reference_distance_m: float
    delivered_fps: float
    analysed_fps: float
    overridden_by: str | None      # a named authority, per ADR 0007
    overridden_at: datetime | None
```

The HTTP and WebSocket surface that exposes these — `GET /api/cameras`,
`GET /api/cameras/{id}/capabilities`, the `camera_status` and
`capability_changed` WebSocket messages, and the timeline and playback endpoints
— belongs to RFC 0004. This RFC fixes the data; that one fixes its wire form.

## Data storage

Two tables, whose columns follow the two dataclasses above. RFC 0003 owns the
schema, the migration and the retention policy; what this RFC fixes is that they
exist and what they must hold:

- `cameras` — identity, recorder, channel, stream URIs, the two commissioning
  numbers (reference distance, scene width), the URL template when ONVIF was not
  used, and current connection state.
- `capability_verdicts` — one row per camera per capability per illumination
  mode, holding the measured inputs, the verdict, the reason sentence, and any
  override with its authority and time.

Verdicts are kept as a history rather than overwritten. A refusal that changed
after someone moved a camera is worth being able to see.

Frames are never stored. Artefacts cut from the stream — clips, crops, snapshots
— are written by the rule and event layer, not here.

## Alternatives considered

**`cv2.VideoCapture` for ingest.** Rejected by ADR 0032 before this RFC: it hides
per-stream transport options, hardware-decoder selection, and packet/keyframe
access, and the third is what allows a clip to be cut at an I-frame boundary and
stored as the original bitstream. `dvr.py` keeps its own OpenCV capture path and
is untouched.

**GStreamer instead of FFmpeg/PyAV.** A capable pipeline framework with good
hardware-decode integration, rejected on deployment cost: it is a large native
dependency to install and debug on Windows, and PyAV reaches the same decode with
a Python-shaped API this team can actually read.

**Ingest as a separate process from the start.** Genuinely tempting for fault
isolation — a decoder crash would not take the API down. Rejected for now because
the VRAM budget makes the frame copy expensive and the deployment is a single
machine with a single operator. The `FrameSource`/`FrameSink` boundary is the
concession: the split stays a day's work rather than a redesign.

**ONVIF-only discovery.** Rejected because the rig cannot be assumed to conform,
and an estate that is "unmeasured" (architecture §2) cannot be assumed to either.
The configured template is not a fallback for convenience, it is the route that
works on the hardware actually in the room.

**Analysing every decoded frame.** Rejected: at 25 fps × 5 channels the model
cascade in RFC 0006 does not fit 4 GB of VRAM, and it buys nothing — a person
crossing a fence does not do it in 40 ms. Sampling to an analysed rate, with the
3 fps tracking floor as a hard constraint, is the trade.

**Dropping cameras rather than frames under load.** Rejected above: a blind
channel is a worse failure than a slower one everywhere.

## Cross-cutting concerns

**Read-only, provably.** The ingest layer opens RTSP sessions and issues ONVIF
`Get*` calls. It contains no code path that writes a device setting, and that is
worth keeping true by construction rather than by discipline — a `Set*` call in
this layer is a defect, in the same sense ADR 0032 calls a runtime Ultralytics
import a defect.

**Credentials.** Recorder credentials are configuration, held once per recorder,
never logged, never returned by an API, and redacted in every URL that reaches a
log line or an error message. There is no outbound internet dependency and no
credential leaves the machine.

**Offline behaviour.** Ingest has no remote dependency at all: it talks to
devices on the local network. Seventy-two hours without a link changes nothing
about this layer, which is the point of putting the analytics next to the
cameras.

**Failure visibility.** A camera in `reconnecting` shows as reconnecting, with
how long it has been that way. A camera that never measured shows as unmeasured.
Neither is drawn as an error colour — a camera that is offline is a fact, not a
fault, and ADR 0030 reserves attention colour for things that want attention.

**Observability.** Per camera, continuously: connection state, delivered fps,
analysed fps, dropped-frame count, reconnect count, decode path in use, and the
age of the newest frame. These are what makes an underperforming site
diagnosable by someone who is not on it.

**Licence.** Nothing in this layer touches the AGPL boundary. PyAV is BSD, the
ONVIF client is MIT; the copyleft obligation arrives with the detector in
RFC 0006, not here.

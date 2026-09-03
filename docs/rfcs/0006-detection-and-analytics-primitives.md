# 0006. Detection and analytics primitives

**Status:** Accepted
**Author:** Sujat
**Date:** 2026-09-03

## Context and scope

The problem statement names eight capabilities. The stack ADRs chose models for
two of them.
[ADR 0032](../adr/0032-inference-runtime-decode-path-and-detector-licence.md)
settles a YOLO-family detector exported to ONNX and ByteTrack for tracking,
which covers human detection and tracking and, by class, vehicle detection.
Face detection, Automatic Number Plate Recognition and night-time movement have
no model behind them at all, and
[ADR 0009](../adr/0009-all-eight-capabilities-with-declared-maturity.md) commits
the project to addressing all eight with a declared maturity rather than
silently omitting any.

This RFC closes that gap. It is the inventory of everything that looks at a
frame: which model, under which licence, at what cost, producing what, and under
what conditions it is offered rather than refused.

It was split out of [RFC 0001](0001-video-ingest-capability-measurement-and-playback.md)
because that document already carries ingest, capability measurement, inference
placement and the playback probe. The two are read together: RFC 0001 produces
frames and per-camera verdicts, this one consumes them and produces primitives
for [RFC 0002](0002-rule-evaluation-engine.md) to evaluate.

Two constraints shape every choice below. The target machine has 4 GB of VRAM,
shared between NVDEC decode sessions and every model loaded at once. And the rig
encodes 1080N — 960 px of real horizontal detail stretched to 1920 on display —
so the pixels available for small objects are half what the displayed resolution
suggests.

## Goals and non-goals

**Goals**

1. Name the model behind every one of the eight capabilities, with its licence.
2. Define the cascade — what runs on every analysed frame, and what runs only on
   a region that earned it — so four model families fit the VRAM budget.
3. Set the per-capability pixel floors that RFC 0001's measurement pass applies
   when it decides supported or refused.
4. Fix the class taxonomy the four `DetectionBox` colour tokens bind to
   ([ADR 0046](../adr/0046-timeline-markers-carry-class-colour.md)).
5. Define the model manifest that keeps models artefacts rather than code.
6. Publish the declared-maturity table ADR 0009 requires, covering all eight
   capabilities including the ones some cameras refuse.
7. Define recognition matching against a configured watchlist, gated exactly
   as [ADR 0059](../adr/0059-face-recognition-ships-against-a-configured-watchlist.md)
   requires.

**Non-goals**

- Rule semantics. A primitive is a fact about a frame; what makes it reportable
  is RFC 0002's business.
- Any legal, authority, or governance workflow around recognition matching.
  [ADR 0059](../adr/0059-face-recognition-ships-against-a-configured-watchlist.md)
  gates matching behind four configured conditions; this RFC consumes that gate,
  it does not build the case-management apparatus around it, which
  [ADR 0016](../adr/0016-mvp-ui-cut-to-five-screens.md) keeps out of scope.
- Any learned model of "suspicious".
  [ADR 0012](../adr/0012-suspicious-activity-as-operator-authored-rules.md) is
  explicit and this RFC adds nothing that could be mistaken for one.
- Thermal imaging, post-MVP per ADR 0013.
- Training. Every model here is consumed as a pre-trained ONNX artefact.

## Design

### Model inventory

| Capability | Model | Licence | Runs on | Output |
|---|---|---|---|---|
| Human, vehicle detection | YOLO-family, ONNX export via Ultralytics | Model artefact AGPL-encumbered; see below | Whole analysed frame | Boxes with COCO class and confidence |
| Tracking | ByteTrack, implemented over our own detections | MIT | Detections, per camera | Stable track ids |
| Face detection | YuNet (libfacedetection / OpenCV Zoo) | MIT | Person crops only | Face boxes + 5-point landmarks |
| Face recognition | SFace (MobileFaceNet, OpenCV Zoo) | Apache-2.0 | Aligned face crops, only where `face_recognize` is configured and enabled | 128-d embedding, matched against the watchlist gallery |
| ANPR — plate location | Small YOLO-family plate detector, ONNX | Apache-2.0 | Vehicle crops only | Plate boxes |
| ANPR — plate reading | `fast-plate-ocr` ONNX model | Apache-2.0 | Plate crops only | Character string + per-character confidence |
| Night-time movement | OpenCV MOG2 background subtraction | BSD-3 | Whole analysed frame, downscaled | Movement mask, moving-region boxes |
| Illumination mode | Chroma-saturation heuristic | — | Whole analysed frame | `colour` or `infrared` |

Every model is an ONNX file loaded by ONNX Runtime, or an OpenCV operation. No
component imports Ultralytics, PyTorch or InsightFace at runtime — ADR 0032
calls that a defect rather than a shortcut, because it is the only thing keeping
the detector swappable and the licence reversible.

### The cascade

Running four model families on every frame of five cameras does not fit 4 GB and
would buy nothing. Work is therefore gated on what the previous stage found.

```
analysed frame
  ├─ MOG2 + illumination        every frame, CPU, downscaled to 480x270
  └─ YOLO detector              every frame, GPU, 640x384 letterboxed
       └─ ByteTrack             every frame, CPU, trivial
            ├─ YuNet            person boxes, only where face_detect is supported,
            │                   only when the box clears the face pixel floor,
            │                   at most once every N frames per track
            │    └─ SFace       only where face_recognize is configured, enabled,
            │                   and the box clears the recognition pixel floor
            └─ plate detector   vehicle boxes, only where anpr is supported,
                 └─ plate OCR   only when the plate box clears the character floor,
                                once per track until a better view arrives
```

Three gates do the work:

**The capability verdict gates the stage.** A camera refused for ANPR never runs
a plate detector. The refusal is not cosmetic — it is what stops the machine
spending VRAM on a job it has already been measured as unable to do.

**Pixel size gates the crop.** A vehicle box 30 px wide cannot contain a readable
plate, so it does not get one attempted. This is the same arithmetic the
measurement pass does at commissioning, applied per object at runtime, because a
vehicle at the far end of the scene fails a floor that the same camera clears up
close.

**Track identity gates repetition.** A plate is read once per track, not once per
frame. A re-read happens only when the plate box is materially larger than the
one that produced the current best reading — a better view earns another attempt,
an identical view does not. Where `face_recognize` is not configured, the same
holds for faces at detection: one box per track per N frames is enough to
establish that a face was present, which is all
[ADR 0008](../adr/0008-face-detection-unconditional-gated-recognition.md)
permits without the gate. Where `face_recognize` is configured and enabled, a
track earns one recognition attempt against its best-quality face box, and a
materially better box earns a re-attempt — the same rule as the plate, because
an embedding computed from a worse view is not evidence worth keeping over a
better one.

### Frame budget

The budget is parametric because its input varies by site: decode capacity is
a property of the machine and the recorder in use together, observed
continuously in production (RFC 0001's per-camera fps and drift telemetry)
rather than fixed once from a single measurement.

Per camera, per second, at the target analysed rate of 5 fps:

| Stage | Invocations | Unit cost | Subtotal |
|---|---|---|---|
| Detector | 5 | ~8 ms (ADR 0032, 320 px; 640 px costs more) | ~40 ms |
| ByteTrack | 5 | < 1 ms | ~5 ms |
| MOG2 + illumination | 5 | ~4 ms, CPU | ~20 ms CPU |
| YuNet | ≤ 2 crops | ~2 ms | ~4 ms |
| SFace (where enabled) | ≤ 1 track | ~3 ms | ~3 ms |
| Plate detect + OCR | ≤ 1 track | ~7 ms | ~7 ms |

Five cameras multiply the GPU line to roughly 250–300 ms of GPU work per wall
second, which leaves substantial headroom — consistent with ADR 0032's estimate
of about five times the margin needed. **That headroom is not the constraint.**
Decode is, and it is the number nobody has yet.

Two floors bound how far the analysed rate can be reduced to buy room:

- **3 analysed fps** — below this, multi-object tracking loses identity
  association, and every rule that depends on a track (dwell, direction of
  crossing, accompaniment) stops being trustworthy.
- **Decode is not reduced by analysing less.** P-frames depend on their
  predecessors and the rig runs a 1-second GOP, so decoding only key frames
  yields 1 fps — below the tracking floor. Frame skipping and tracking are
  mutually exclusive on this hardware.

VRAM, as a budget to be verified rather than a measurement:

| Consumer | Estimate |
|---|---|
| ONNX Runtime CUDA context | ~300 MB |
| Detector weights + activations | ~400 MB |
| YuNet, SFace, plate detector, plate OCR | ~180 MB combined |
| NVDEC sessions, 5 channels | ~500 MB |
| Headroom | remainder of 4 GB |

If the measured total does not fit, the order of retreat is stated now rather
than improvised later: reduce detector input resolution, then reduce the analysed
rate to the 3 fps floor, then move ROI models to the CPU execution provider,
then reduce the number of channels — and if it comes to the last one, that is a
finding about the hardware which goes in the architecture's risk section, not a
quiet reduction in what the platform claims.

### Class taxonomy

Four classes, and exactly four, because ADR 0046 binds timeline markers and
detection overlays to four colour tokens:

| Class | Produced by | Notes |
|---|---|---|
| `person` | Detector, COCO `person` | |
| `vehicle` | Detector, COCO `car`, `truck`, `bus`, `motorcycle`, `bicycle` | The COCO subclass is retained as an attribute |
| `face` | YuNet | Always inside a `person` box |
| `plate` | Plate detector | Always inside a `vehicle` box |

Movement from MOG2 is a primitive, not a class. It has no box colour because it
is not an object — it is a property of a region, and it feeds rules directly.

A watchlist match is an attribute of a `face` detection, not a fifth class. It
does not get its own colour token; a matched face draws exactly as any other
face does, and the match is a fact recorded alongside it, not a different kind
of box.

Vehicle *classification* is by type only: car, truck, bus, motorcycle, bicycle.
No make, no model, no colour. That boundary is declared, not discovered later.

### Per-capability detail

**Human detection and tracking.** The detector's `person` class, tracked by
ByteTrack. Bottom-centre of the box is the ground contact point rules use for
zone membership and crossing, because the box centre of a person standing at the
edge of a zone is not where the person is standing.

*Floor:* a person box at least 32 px high in encoded geometry. At 1080N that is
roughly the DORI detection band; below it the detector's recall falls away
quickly.

**Vehicle detection and classification.** The same detector, COCO vehicle
classes collapsed to `vehicle` with the subclass retained. The subclass is
reported as an attribute and never as a certainty — a van and a truck are one
model's opinion apart.

*Floor:* 48 px of box width in encoded geometry.

**Face detection.** YuNet on person crops. It produces a box and five
landmarks. What is stored is that a face was detected, its box, and its
confidence.

*Floor:* 24 px of face width in encoded geometry — below that YuNet's own
documented operating range gives out. This floor is for *detection*, and it
applies unconditionally — it is what makes ADR 0008's "detection ships
unconditionally" true regardless of whether recognition is configured anywhere.

**Face recognition.** [ADR 0059](../adr/0059-face-recognition-ships-against-a-configured-watchlist.md)
gates this behind a system-wide configuration: the four conditions
[ADR 0008](../adr/0008-face-detection-unconditional-gated-recognition.md)
specified, held as `watchlist_config`
([RFC 0003](0003-event-store-and-alert-state.md)). Until that row is complete
and an administrator has toggled it on, the `face_recognize` capability
verdict is `refused` on every camera with the reason "recognition is not
configured for this deployment," SFace is never loaded, and YuNet's landmarks
are discarded exactly as before — the gate is checked once, at process start,
not per frame.

Where enabled: YuNet's landmarks align the face crop, SFace embeds it as a
128-dimension vector, and the embedding is compared by cosine similarity
against every enrolled subject in the watchlist gallery. A similarity at or
above the model's documented threshold (0.363) is a match; a subject's
enrolled embedding is itself computed the same way, from a reference photo
supplied at enrollment.

*Floor:* three times the detection floor, 72 px of face width in encoded
geometry — carried over from this RFC's own prior estimate that recognition
needs roughly three times the pixels detection does, pending validation once a
gallery exists to measure against. Below it, `face_recognize` is refused on
that camera even when `face_detect` is supported, because a box small enough
to detect is not necessarily large enough to embed reliably.

A match is never acted on automatically. It produces an Event exactly like any
other detection, and an Alert only if the matching rule is alerting; an
operator assesses it real, not real, or unsure, the same as every other alert.

**ANPR.** Two stages inside a vehicle box: locate the plate, then read it.

The reading passes through a grammar gate. Indian civilian plates follow
`SS RR L… NNNN` — two-letter state code, one or two RTO digits, one to three
series letters, four digits — with the BH series taking the distinct form
`NN BH NNNN L…`. The gate has exactly one job:

> A read that does not match a known format is reported with reduced confidence
> and marked unverified. It is **never** rewritten to make it match.

No `O` to `0`, no `I` to `1`, no character substitution of any kind. A grammar
that repairs a read manufactures evidence, and this platform's whole argument
([ADR 0002](../adr/0002-differentiate-on-deployment-not-benchmark-accuracy.md))
is that it does not do that.

*Floor:* 16 px of character height, which on Indian plate proportions means
roughly 110 px of plate width in encoded geometry.

The floor, not the model, decides availability. At 960 px of encoded width, a
plate 110 px wide occupies more than a tenth of the frame — a vehicle close to
the camera, on a road pointed at it, such as a boom-barrier or choke-point
camera at a checkpost, not a vehicle crossing a field at 60 m on a wide-area
fenceline camera. On the development rig, whose five channels are wide-area
views of a residential road rather than a checkpost, most cameras measure
below the floor and ANPR is refused on them — that is a fact about *this*
estate's camera placement, not a limitation of the capability, and it is why
[ADR 0060](../adr/0060-file-backed-frame-source-for-testing.md)'s file-backed
source exists: a checkpost or highway clip that clears the floor demonstrates
ANPR working, which the rig's own cameras cannot. Presenting ANPR as available
regardless of camera placement would be the exact overclaim ADR 0002 exists to
prevent; presenting it as inherently unreliable would be the opposite
overclaim, and just as wrong.

**Night-time movement.** MOG2 background subtraction on the downscaled frame,
producing moving regions independent of any classifier. This is the primitive
that survives when classification does not: an IR frame of a person at 50 m may
give the detector nothing while still giving a clear movement signature.

Illumination mode is detected from chroma saturation — an IR frame is
effectively monochrome — and stamped on every frame, so rules can be night-scoped
and the day-versus-night performance gap ADR 0013 requires can be published from
real counts rather than asserted.

MOG2's learning rate is lowered at mode transitions, because dusk and the IR
cut-filter switching are exactly when a background model is most likely to
declare the entire frame in motion.

**Suspicious activity.** No model. The primitives above — presence, dwell,
direction, count, accompaniment, movement in a place and at a time — are what an
operator composes a rule from in RFC 0002. This RFC contributes the primitives
and nothing that scores behaviour.

### Model manifest

`models/` is not in git — the artefacts are large and some carry licence terms
that want to be pointed at rather than vendored. What *is* in git is
`models/manifest.json`:

```json
{
  "schema": 1,
  "models": [
    {
      "id": "detector",
      "file": "yolo-detector.onnx",
      "sha256": "…",
      "input": {"name": "images", "shape": [1, 3, 384, 640], "layout": "NCHW"},
      "output": {"name": "output0", "layout": "xywh+conf+cls"},
      "classes": ["person", "bicycle", "car", "motorcycle", "bus", "truck"],
      "licence": "AGPL-3.0-or-later",
      "source": "…",
      "notes": "Exported via Ultralytics; nothing imports Ultralytics at runtime."
    },
    {
      "id": "face_recognizer",
      "file": "sface.onnx",
      "sha256": "…",
      "input": {"name": "data", "shape": [1, 3, 112, 112], "layout": "NCHW"},
      "output": {"name": "embedding", "layout": "vector_128"},
      "classes": [],
      "licence": "Apache-2.0",
      "source": "https://github.com/opencv/opencv_zoo/tree/main/models/face_recognition_sface",
      "notes": "Loaded and run only when watchlist_config.enabled is true (ADR 0059). Match threshold: cosine >= 0.363."
    }
  ]
}
```

The application verifies each hash at startup and refuses to run with an artefact
it cannot identify — a silently swapped model produces silently different
evidence. The manifest also carries the licence per artefact, which is what makes
the AGPL boundary auditable rather than folkloric.

The `face_recognizer` entry's input shape above is the conventional
112×112 aligned-crop size the ArcFace-family alignment step produces; this RFC
has not independently verified it against the shipped ONNX file's own metadata,
and the manifest that actually ships is generated from that file, not typed by
hand — the hash check exists precisely so a mistyped or assumed shape here
cannot silently diverge from what the artefact really is.

### Declared maturity

What ADR 0009 requires: all eight capabilities addressed, each at a stated
maturity with stated conditions and limitations. Nothing here is claimed
unqualified.

| Capability | Maturity | Conditions | Limitation |
|---|---|---|---|
| Human detection and tracking | Ships | Person box ≥ 32 px high; ≥ 3 analysed fps for tracking | Crowds and heavy occlusion cause identity switches |
| Vehicle detection and classification | Ships | Box ≥ 48 px wide | Type only — no make, model or colour |
| Face detection | Ships, unconditionally | Face ≥ 24 px wide; inside a detected person | Detection only unless recognition is separately configured |
| Face recognition | Ships, gated | Face ≥ 72 px wide; `watchlist_config` complete and enabled (ADR 0059) | Matches a bounded, locally-held gallery only; refused entirely until configured; never automates past an operator assessment |
| ANPR | Ships, gated by camera placement | Character height ≥ 16 px, i.e. plate ≥ 110 px wide | Indian civilian formats; grammar rejects but never repairs; refused on wide-area cameras, supported on close/choke-point cameras |
| Virtual fence intrusion | Ships | Zone drawn on a camera whose person or vehicle detection is supported | Geometry is 2D image space, not ground plane |
| Suspicious activity | Ships as a rule engine | Operator-authored from primitives | No learned model; a starter library is unvalidated (ADR 0012) |
| Night-time movement | Ships | Measured separately after dark; IR mode detected per frame | Movement without classification when illumination defeats the detector |
| Real-time alerts and event logging | Ships | — | Bounded queue; discards are recorded, not silent (ADR 0034) |

No accuracy figure appears in this table, and none appears anywhere else without
the measurement conditions attached. That is ADR 0002, and it is the difference
between a claim and a number.

## System-context diagram

Where this sits in the whole system: the
[container view](../architecture/diagrams/c4-l2-container.md).

The detailed diagrams for this RFC — the analytics cascade and the per-frame budget — are still owed, and are tracked
as remaining Phase 3 work rather than assumed to exist.

## APIs

Internal, consumed by RFC 0002.

```python
Klass = Literal["person", "vehicle", "face", "plate"]

@dataclass(frozen=True, slots=True)
class Detection:
    klass: Klass
    confidence: float
    box: tuple[int, int, int, int]      # xyxy, encoded geometry
    subclass: str | None = None         # "car", "truck" … for vehicles
    parent_track_id: int | None = None  # the person or vehicle a face/plate sits in


@dataclass(frozen=True, slots=True)
class Track:
    track_id: int
    klass: Klass
    detection: Detection
    first_seen: datetime
    ground_point: tuple[int, int]       # bottom-centre, for zone geometry
    age_frames: int


@dataclass(frozen=True, slots=True)
class PlateRead:
    track_id: int
    text: str
    confidence: float                   # min over characters
    grammar_matched: bool               # False means reported, never repaired
    box: tuple[int, int, int, int]


@dataclass(frozen=True, slots=True)
class FaceMatch:
    track_id: int
    subject_id: int                     # watchlist_subjects.id
    similarity: float                   # cosine similarity at match time
    threshold_used: float               # recorded, since a threshold can change later
    box: tuple[int, int, int, int]


@dataclass(frozen=True, slots=True)
class FrameAnalysis:
    camera_id: int
    captured_at: datetime
    clock_trusted: bool
    illumination: Literal["colour", "infrared"]
    tracks: list[Track]
    plate_reads: list[PlateRead]
    face_matches: list[FaceMatch]       # empty whenever face_recognize is not enabled
    movement_regions: list[tuple[int, int, int, int]]
    movement_fraction: float            # 0..1 of the frame in motion
```

`FrameAnalysis` is the whole contract between analytics and rules. It carries the
clock-trust flag through unchanged, because an Event's time integrity is decided
at capture and must not be re-derived downstream.

The wire form of a detection — the `detections` message on `/ws/live` that the
Canvas overlay draws — is RFC 0004's, derived from `Track`.

## Data storage

Analytics writes nothing to the database. It reads model artefacts from
`models/`, verifies them against the manifest, and hands `FrameAnalysis` to the
rule engine, which is the component that decides whether anything is worth
recording.

Per-frame object metadata is deliberately not persisted by default. At roughly
138 MB per camera per day it is the largest thing the platform could store and
the least often read; RFC 0003 owns its retention clock, and the default is off.

## Alternatives considered

**PyTorch at runtime instead of ONNX Runtime.** Rejected by ADR 0032 before this
RFC, and worth restating because it is the choice that makes everything else
here possible: with the model as an artefact rather than a library call, the
detector is swappable and the licence is reversible.

**SCRFD or RetinaFace for face detection.** SCRFD is more accurate than YuNet at
small scales. Rejected on licence: the InsightFace model weights carry a
non-commercial research restriction, and importing that into a repository already
navigating AGPL adds a second, worse encumbrance. This holds regardless of
recognition — the detector's job stays "produce a box and landmarks," and a
licence trade made for detection accuracy would still apply to every frame,
recognition-gated or not.

**ArcFace / InsightFace embeddings for recognition.** The InsightFace model
weights (`buffalo_l`, `antelopev2`, and the wider ArcFace family) are, like
SCRFD, released under a non-commercial research restriction, and they are the
models most commonly cited for accuracy. Rejected for the same reason as
SCRFD: this is a component whose whole justification is that a swap keeps the
repository's licence position reversible, and a research-only weight file
defeats that regardless of how it scores on a benchmark. On LFW specifically,
SFace's own paper reports it matching or marginally exceeding ArcFace despite
running on a far smaller MobileFaceNet-scale backbone rather than ArcFace's
ResNet100 — it trails on some other benchmarks (CFP-FP, IJB-C) against
ArcFace's largest variant, but is not the accuracy compromise the phrase
"smaller and safer" implies. It is Apache-2.0, packaged by OpenCV itself
rather than an individual research repository, from the same OpenCV Zoo YuNet
already comes from, and it is the model whose alignment step already consumes
the landmarks YuNet was built to produce. Other permissively-licensed
candidates surveyed (FaceX, AuraFace) either inherit the same disputed-
provenance training data without OpenCV's institutional backing or trade away
meaningfully more accuracy to avoid it — neither is a clear improvement.

**DeepFace or `face_recognition` (dlib) as a wrapper library.** Both are
Python packages that bundle model selection, alignment and matching behind a
single call. Rejected because they import a model as a library dependency
rather than load a named ONNX artefact — exactly the pattern
[ADR 0058](../adr/0058-model-artefacts-are-versioned-files-with-a-manifest.md)
requires avoiding, and the licence of whichever model they select underneath
is then inherited without being named in this document.

**PaddleOCR for plate reading.** A strong general OCR engine, Apache-2.0. Kept as
the documented fallback rather than the default, because it is a general text
pipeline — detection, angle classification, recognition — where a fixed-length
plate head does the same job in one forward pass. If Indian plate formats read
poorly on the rig, this is the swap, and the manifest makes it a file change.

**Tesseract.** Rejected. It expects document-quality input and degrades badly on
low-resolution, motion-blurred, angled plates, which is the only kind this
platform will ever see.

**A grammar that corrects reads.** Rejected on principle, above. It would improve
every accuracy metric and make the evidence worthless.

**Optical flow instead of MOG2 for movement.** More informative — it gives
direction as well as presence — and substantially more expensive per frame. MOG2
is chosen because the rules that consume movement need presence in a region, and
direction already arrives from tracking when the detector can see the object at
all.

**DeepSORT instead of ByteTrack.** DeepSORT's appearance embeddings survive
occlusion better, at the cost of a second network on every detection — VRAM this
budget does not have. ByteTrack's association of low-confidence detections
recovers much of the same benefit for approximately nothing.

**A learned anomaly model for suspicious activity.** Excluded by ADR 0012, and
this RFC agrees rather than merely complying: an anomaly score with no stated
operating condition is exactly the unqualified claim ADR 0002 rules out, and it
cannot be explained to an operator who has to justify acting on it.

## Cross-cutting concerns

**Licence boundary.** The detector artefact is the only AGPL-encumbered
component, and it is encumbered because it was exported with Ultralytics. The
repository is AGPL-3.0 as a result, deliberately. The escape route — swapping in
RTMDet, YOLOX or RT-DETR, all Apache-2.0 — exists only while the model stays an
artefact. The manifest's per-artefact licence field is what makes that checkable.

**Privacy.** Face detection produces a box and nothing else, unconditionally.
Recognition — an embedding, a gallery, matching code — exists in the codebase
but is inert until `watchlist_config` is complete and enabled
([ADR 0059](../adr/0059-face-recognition-ships-against-a-configured-watchlist.md)),
which is a system-wide switch, not a per-camera or per-rule one. Where it is
off, this RFC's behaviour is exactly what the previous version of this
paragraph described: a crop containing a face is an artefact under the same
retention clock as any other crop, and nothing about it is compared to
anything. Where it is on, the embedding is itself a biometric template, held
under that same retention clock, never exported, and every match is logged
with the subject, the similarity score and the threshold in force at the time.

**Honesty about ANPR and faces.** Neither capability is universally available,
and neither is universally refused — both are gated on measured pixels, and
this document says so in the maturity table rather than in a footnote or a
blanket claim in either direction. The problem statement asks for them; the
platform provides them where the pixels exist and refuses them, with a named
reason, where they do not, which is the whole of ADR 0007 applied to the two
capabilities where the temptation to overclaim, or to quietly write them off,
is greatest. Recognition carries a second gate on top of pixels — the ADR 0008
conditions — and both gates are checked and reported independently, so a
refusal always names which one actually failed.

**Determinism.** Given the same frame and the same artefacts, the pipeline
produces the same primitives. No randomised augmentation, no sampling at
inference, no thresholds that drift with load.

**Observability.** Per camera: analysed fps actually achieved, per-stage latency,
crops attempted versus crops skipped by gate, and plate reads split by
grammar-matched and unverified. The last one is the number that tells an operator
whether ANPR on that camera is worth anything.

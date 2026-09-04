# 32. Inference runtime, decode path, and detector licence

**Date:** 2026-09-01
**Status:** Accepted

## Context

Thirty-one decisions are recorded here and not one of them is technical.
[docs/architecture/README.md](../architecture/README.md) §8 still lists the
model runtime as open, and no dependency layer is named anywhere in the
repository. Nothing can be handed to a teammate to build until it is.

The [technical feasibility research](https://app.notion.com/p/3c986dda46e281a7a1c3d87623970822?pvs=204)
(Notion) makes one finding load-bearing above all others: **decode, not
inference, is the binding compute cost, and analysing fewer frames does not
decode fewer frames.** P-frames are predicted from their predecessors, so
producing an arbitrary frame means decoding back to the last I-frame.
NVIDIA's published figures show a device running a detector at 256 fps while
sustaining only eight full-pipeline 1080p30 H.264 streams — roughly 240 fps
of inference capability unreachable because decode consumes the budget first.
The rig encodes with a one-second GOP, so the one cheap subsampling that
exists — I-frame-only decoding — yields a single analysed frame per second,
below the roughly 3 fps floor at which multi-object tracking's identity
association collapses. On this hardware, frame skipping and tracking are
mutually exclusive.

The hardware is now fixed rather than hypothetical. Development and the
demo both run on an ASUS TUF A15 — Ryzen 7 7445HS (6 cores, 12 threads),
RTX 3050 Laptop with 4 GB of VRAM, 16 GB DDR5, Windows 11. The same research
carries a measured figure for exactly that GPU: about 8 ms for a small
YOLO-class model at 320 px input. The rig
([ADR 0015](0015-mvp-validated-against-development-cctv-rig.md)) delivers
five live H.264 channels at 1080N — 960×1080 encoded, stretched to 1920×1080
for display.

Detector choice is also a licensing question, which is easy to discover late
and expensive to discover late. Ultralytics distributes its YOLO models under
AGPL-3.0; shipping or hosting a product containing them requires releasing
the complete source under AGPL-3.0 or buying an enterprise licence.

## Decision

Python 3.12, matching [CI](../../.github/workflows/ci.yml) and the rig.

**Decode through PyAV, not `cv2.VideoCapture`.** PyAV binds FFmpeg directly
and exposes three things OpenCV's capture wrapper hides: per-stream transport
and timeout options, explicit hardware-decoder selection, and access to
packets and keyframe boundaries. The third is what allows an evidential clip
to be cut at an I-frame boundary and stored as the original bitstream rather
than re-encoded — re-encoding costs an encode session and invalidates any
hash taken at capture. OpenCV stays, for image operations only. `dvr.py` is
not touched and keeps its own OpenCV capture path
([CLAUDE.md](../../CLAUDE.md) rule 5).

**Hardware decode via NVDEC where the GPU is present, software FFmpeg decode
as the fallback.** Decode is the binding cost, so it gets the silicon. The
fallback is not a courtesy — it is what lets the platform run on a machine
with no NVIDIA GPU, which is the situation at most sites and possibly on
whatever laptop the demo ends up on.

**Inference through ONNX Runtime with a swappable execution provider** — the
CUDA provider on this GPU, the CPU provider everywhere else. Not PyTorch at
runtime, which drags a training-shaped dependency into a deployment that has
no business carrying one. Not TensorRT alone: it builds a machine-specific
engine at install time, and a four-person team and a demo laptop do not need
that friction to reach the throughput this workload asks for.

**A YOLO-family detector, exported to ONNX via Ultralytics, and the repository
is licensed AGPL-3.0 as a result.** This is the licence choice made
deliberately rather than inherited by accident — recorded in
[LICENSE](../../LICENSE) at the repository root. IBVAP is already a public
hackathon repository and states plainly that it is not a production
deployment, so copyleft costs it nothing today.

**Tracking by ByteTrack (MIT), implemented over our own detections** rather
than through Ultralytics' bundled tracker, so the tracking layer stays free
of the AGPL boundary and can outlive the detector behind it.

Detection coordinates are produced in the stream's native encoded geometry.
Anamorphic correction happens at display, not before inference — upscaling
960×1080 to 1920×1080 before a model sees it costs compute and manufactures
no information.

Two things are deliberately **not** decided here, and belong to the design
docs that follow: whether ingest and inference are one process or two, and
where inference runs relative to the cameras.

## Consequences

The ONNX Runtime boundary is what makes the licence decision reversible. The
runtime consumes an ONNX file and knows nothing about what produced it, so a
force that needs a non-copyleft deployment swaps in a permissively licensed
detector — RTMDet, YOLOX, RT-DETR are all Apache-2.0 — or buys an Ultralytics
enterprise licence, without touching the pipeline around it. That escape
route only exists because the model is an artefact rather than a library
call, and it stops being true the moment a component imports Ultralytics at
runtime. Doing so is a defect, not a shortcut.

The same boundary sets the sizing obligation. Five live rig channels at five
analysed frames per second is 25 fps of detection against roughly 8 ms per
inference — around five times the headroom needed. That number is not the
one to watch. Decode of five concurrent 1080N H.264 streams is, and it is
unmeasured on this machine; the first thing implementation has to produce is
that measurement, not a detection.

4 GB of VRAM is a real ceiling and constrains this to small models at modest
input resolution. It also means concurrent NVDEC sessions and model memory
compete, which is another reason the decode measurement comes first.

Choosing PyAV over OpenCV's capture means re-establishing, in IBVAP's own
ingest, the five behaviours `dvr.py` already had to learn the hard way —
forced TCP, an explicit socket timeout, a bounded buffer, per-channel
isolation, and backoff on reconnect. Those are read from the rig as prior
art, not inherited as code.

[docs/architecture/README.md](../architecture/README.md) §8 no longer lists
the model runtime as open; inference placement stays open.

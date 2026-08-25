# Technical Feasibility — Software-Defined Video Analytics on Existing IP CCTV

**Stage:** 01 — Research → Technology
**Date:** 2026-08-24
**Scope:** Whether, and under what conditions, the capabilities named in the
official SIH problem statement ([Problem Statement ID 26187](../../00-project/problem.md))
can be delivered by software running against *already-installed* IP CCTV
infrastructure — with no dedicated FRS, ANPR or smart-camera hardware.

> **This document does not choose a technology stack.** It does not define
> product scope, requirements, architecture or UI. Per
> [CLAUDE.md](../../../CLAUDE.md) §2, those belong to `docs/02-product/`,
> `docs/03-design/` and `docs/04-architecture/` respectively, and none of them
> may proceed from this document by assumption. What is recorded here is what
> the physics, the standards, the published engineering and the measured
> hardware allow — and where the limits sit.

---

## How to read this document

Per [CLAUDE.md](../../../CLAUDE.md) §3.7:

| Label | Meaning |
|---|---|
| **FACT** | Verifiable and sourced. The source is cited as `[Tn]`, or as a repo path for evidence in this repository. |
| **ASSUMPTION** | Believed true but not verified against a source. |
| **HYPOTHESIS** | A proposed explanation or approach that must be tested before it is relied on. |
| **UNKNOWN** | An identified gap. Nobody on this project knows this yet. |
| **CALCULATION** | Arithmetic performed in this document from stated inputs. Shown so it can be checked, not treated as measured. |

A statement labelled **FACT** is a fact *about what the cited source states*.
Where a source is a vendor, its interest is noted inline.

Scope labels follow [CLAUDE.md](../../../CLAUDE.md) §4:

- **[GLOBAL]** — true for video analytics on existing CCTV anywhere.
- **[BORDER]** — true for border/frontier surveillance generally, any country.
- **[SIH/SSB]** — true only for this problem statement or this force.
- **[MARKET:IN]** — India-specific legal, regulatory or procurement factor.

Unlabelled statements are **[GLOBAL]**.

### Evidence in this repository

This repository already contains a working RTSP ingest against a real,
consumer-grade recorder — [`dvr.py`](../../../dvr.py) and its
[`backups/`](../../../backups) — described in
[CLAUDE.md](../../../CLAUDE.md) §3.6 as the developer's home CCTV setup used for
development and testing. It is **preserved and unmodified** by this research
pass. Several findings below are read directly out of its code comments, which
record behaviour established by testing against that hardware. These are cited
as `[T38]` and marked **[rig-measured]**. They are single-device observations,
not a survey — but they are the only *measured* evidence this project currently
has, and they are unusually inconvenient for the problem statement's premise,
which raises rather than lowers their value.

### Research-process caveats for this pass

- No hands-on benchmark was run for this document. Every performance figure is
  either published by a vendor, published in a peer-reviewed paper, or
  calculated here from stated inputs. Nothing below is measured by this project
  except the `[T38]` rig observations.
- NIST IR 8173 (FIVE) could not be fetched directly (the PDF exceeded the fetch
  size limit); its findings are taken from NIST's own news summary `[T23b]` and
  the programme page. Carried forward as a retrieval gap.
- Several accuracy figures come from papers proposing the method being
  measured. Self-reported state-of-the-art numbers are treated as upper bounds,
  not as deployment expectations, and this is stated at each use.
- IEC/EN 62676-4:2025 was not read in the original; the pixel-density values in
  [§1.6](#16-resolution) come from a CCTV-design-tool vendor's summary `[T9]`.
  **This must be verified against the standard before any figure from it is
  used in architecture.**

---

## 0. The single sentence this document exists to test

The problem statement asserts that advanced surveillance functions "often
require specialized hardware and proprietary solutions", and proposes to replace
that hardware with software running on "standard IP-based CCTV cameras".

The competitive research already established that the *software* half of that
claim is largely true — every named capability ships today as software on
third-party cameras
([competitive-landscape.md](../competitors/competitive-landscape.md) §4).

What this document finds is that the binding constraint **moved** rather than
disappeared. It moved out of the camera's silicon and into four places software
cannot reach: **the pixels the installed camera actually delivers**, **the
encoder budget of the recorder in front of it**, **the decode cost of the
stream**, and **the watts and bits available at the site**. Each is examined
below.

---

## 1. Camera and video interfaces

### 1.1 RTSP

**FACT** — RTSP is "an application-layer protocol for the setup and control over
the delivery of data with real-time properties" — a "network remote control" for
media servers. **RTSP does not itself carry media**; it is a control plane, and
media is delivered by RTP over UDP, over TCP, or interleaved on the RTSP
connection itself. `[T1]`

**FACT** — The control methods are DESCRIBE, SETUP, PLAY, PAUSE, TEARDOWN,
OPTIONS and GET_PARAMETER/SET_PARAMETER. Sessions must demonstrate liveness
either through RTCP or through any RTSP request referencing the session; the
default session timeout is **60 seconds**. `[T1]`

**FACT** — RTSP 2.0 (RFC 7826) obsoletes RTSP 1.0 (RFC 2326) and is **not
backwards compatible** with it. `[T1]`

**ASSUMPTION** — Essentially the entire installed CCTV base speaks RTSP 1.0
(RFC 2326), not 2.0. *(Basis: RFC 7826's own statement that the two are not
interoperable, combined with the fact that no camera or VMS documentation
retrieved in this pass or the competitive pass mentions RTSP 2.0. Not verified
against a device population.)*

**FACT [rig-measured]** — On the recorder in this repository, **UDP transport
drops badly and RTSP must be forced over TCP**, and without an explicit socket
timeout a dead channel blocks the read call indefinitely rather than returning
an error. `[T38]` — see [`dvr.py`](../../../dvr.py), the
`OPENCV_FFMPEG_CAPTURE_OPTIONS` block.

**ASSUMPTION** — RTSP-over-TCP is the safe default for an analytics ingest, at
the cost of head-of-line blocking and higher latency under loss. *(Basis:
`[T38]` plus `[T1]`'s description of interleaved TCP as the firewall-traversal
fallback. Not tested on other devices.)*

**FACT** — **The RTSP URL path is not standardised across manufacturers.**
Hikvision uses `/Streaming/Channels/101`, Dahua `/cam/realmonitor?channel=1&subtype=0`,
Reolink `/h264Preview_01_main`, Axis `/axis-media/media.amp`. `[T30]`

**FACT [rig-measured]** — The recorder in this repository uses the Dahua-style
path, and the URL must have its password percent-encoded because the password
contains `@`, which would otherwise terminate the userinfo section and leave a
bogus hostname. `[T38]`

**ASSUMPTION** — Password percent-encoding, credential-in-URL handling and
per-vendor path templates are the kind of small, undignified compatibility work
that accumulates into the "compatibility lab" every serious VMS vendor was found
to operate ([competitive-landscape.md](../competitors/competitive-landscape.md)
§6.4). *(Interpretation of `[T30][T38]` against that finding.)*

**UNKNOWN** — Whether the cameras or recorders actually installed at the target
sites accept concurrent RTSP sessions from a new client at all, how many, and
whether doing so degrades the existing recording or live-view path.

### 1.2 ONVIF

**FACT** — ONVIF publishes profiles, of which the video-relevant ones are **S**,
**T**, **G**, **M** and **D**. A device may conform to several — e.g. a camera
with local storage may be both Profile T and Profile G. `[T3]`

**FACT** — **Profile S** covers live H.264 streaming, audio, PTZ control,
motion-detection events and basic metadata, and most Profile S cameras also
expose a plain RTSP URL
([domain-research.md](../domain/domain-research.md) §6.7).

**FACT** — On **9 October 2025** ONVIF announced it is ending support for Profile
S in favour of Profile T. After **31 March 2027** manufacturers can no longer
submit new products — or existing products with new firmware — for Profile S
conformance. `[T4][T5]`

**FACT** — The reason is authentication, not features: Profile S mandates
username-token authentication, which ONVIF states "is regarded as too weak today
to protect against unauthorized access to devices." `[T4]`

**FACT** — Existing Profile S devices **keep working** after March 2027, and
existing conformant products stay listed while the manufacturer maintains its
Declaration of Conformance. The interoperability risk is one-sided: if vendors
remove username-token support in newer firmware, clients that rely on it break.
`[T4]`

**FACT** — **Profile T** adds over Profile S: digest authentication, H.264 and
H.265 (replacing MJPEG/MPEG-4 as the profile's codecs), HTTPS for encrypted
media streaming, mandatory PTZ, **mandatory metadata streaming**, motion and
tampering event detection, audio output, and imaging configuration. Profile S's
IP address filtering is not carried over. `[T4]`

**FACT** — **Profile G** covers edge storage and retrieval: configuring,
requesting and controlling recording; recording search; and replay/export. A
Profile G device must be able to record either over the network or on the device
itself. `[T7]`

**FACT** — **Profile M** is the analytics profile. It covers analytics
configuration and query, configuration and streaming of metadata, generic object
classification, **metadata definitions for geolocation, vehicle, licence plate,
human face and human body**, event interfaces for object counters and for face
and licence-plate recognition analytics, rule configuration, and delivery of
events "through metadata stream, ONVIF event service **or over MQTT**". `[T6]`

**This is the most important standards finding in the document for integration.**
ONVIF Profile M already defines a vendor-neutral schema for exactly the object
classes the problem statement names, and already names MQTT as a transport for
them. Whether to use it is an architecture decision and is not made here; that it
exists changes what "egress has no standard"
([competitive-landscape.md](../competitors/competitive-landscape.md) §7.1) means.

**FACT** — Two of the best-resourced vendors in the market independently
concluded that ONVIF conformance alone is insufficient: Verkada states that "any
ONVIF Profile S camera may not work with Command Connector out-of-the-box" and
maintains a hardware compatibility list with weeks-to-months assessment per
model; Milestone needed 1,000+ individually tested ONVIF devices to converge on a
single optimised driver and maintains 16,500+ tested devices
([competitive-landscape.md](../competitors/competitive-landscape.md) §6.4).

**ASSUMPTION** — "IBVAP supports ONVIF" would be a statement of intent, not a
capability, unless backed by a tested-device list. *(Carried forward from
[competitive-landscape.md](../competitors/competitive-landscape.md) §6.4; the
technology research finds nothing that weakens it.)*

**UNKNOWN** — What proportion of the installed base at the target sites is
ONVIF-conformant at all, at which profile, and at which firmware. Recorded as
blocking in
[ssb-operational-context.md](../domain/ssb-operational-context.md) §6.3 and
[domain-research.md](../domain/domain-research.md) §1.3; nothing in this pass
resolves it.

### 1.3 Codecs

**FACT** — H.265/HEVC delivers roughly the same visual quality as H.264 at about
**half the bitrate**, halving both storage and LAN bandwidth
([domain-research.md](../domain/domain-research.md) §6.2).

**FACT** — Profile T made H.264 and H.265 the profile codecs, displacing MJPEG
and MPEG-4 which Profile S carried. `[T4]`

**FACT** — NVIDIA's current decode hardware (6th-generation NVDEC, Blackwell)
decodes MPEG-1/2/4, VC-1, VP8, VP9 (8/10/12-bit), H.264 in all variants, H.265 in
all variants, and AV1 (8/10-bit). `[T10]`

**FACT** — **Encode is licence-limited on consumer GPUs**: GeForce cards are
capped at **12 concurrent encode sessions**, while professional and datacenter
cards (RTX PRO, L4, L40/L40S) are "unrestricted". `[T10]`

**ASSUMPTION** — The encode-session cap matters for any design that transcodes
for clip export, low-bandwidth preview or web delivery, and does not matter for a
design that stores the original bitstream and never re-encodes it.
*(Interpretation of `[T10]`.)*

**HYPOTHESIS** — Avoiding transcode entirely — storing and shipping the original
encoded bitstream, and only ever *decoding* — removes both the encode-session cap
and a large share of the compute cost. This needs testing against the requirement
to produce evidential clips at a fixed, playable profile.

**UNKNOWN** — The codec mix in the installed base. H.264 is assumed dominant on
older estates but this is not measured for the target sites.

### 1.4 Stream profiles and sub-streams

**FACT** — ONVIF exposes the device's media profiles, including main stream and
sub-stream, with their encoding (H.264/H.265) and the exact RTSP URL for each,
read directly from the camera. `[T30]`

**FACT** — Frigate, the widely deployed open-source analytics stack, is built
around **dual-stream** use: a low-resolution sub-stream for continuous detection
and the high-resolution main stream for recording. `[T14]`, and see
[competitive-landscape.md](../competitors/competitive-landscape.md) §7.

**This is the cheapest lever in the entire pipeline, and it is a camera
configuration, not a software capability.** If the camera or recorder can emit a
second, lower-resolution, lower-frame-rate stream, analytics decode cost falls by
roughly the pixel ratio and recording quality is untouched. If it cannot, every
frame must be decoded at full resolution.

**ASSUMPTION** — Sub-stream availability, resolution and frame rate will vary
enormously across an existing estate, and will sometimes already be consumed by
the incumbent VMS or a mobile app. *(Basis: `[T30]`'s per-profile model plus
`[T38]`'s finding of a shared, fixed encoder budget — see
[§1.7](#17-the-recorder-in-front-of-the-camera-is-a-hard-limit). Not surveyed.)*

**UNKNOWN** — Whether sub-streams on the target estate are of usable resolution.
A CIF or D1 sub-stream (352×288 / 704×576) may be below the pixel density needed
for anything but gross motion — see
[§9](#9-hard-physical-limitations-software-cannot-solve).

### 1.5 Frame rate

**FACT** — Multi-object tracking degrades gracefully from 30 FPS down to about
**3 FPS** (HOTA ≈ 43%), then degrades sharply below 2 FPS: association accuracy
(AssA) falls from **43.6% at 3 FPS to 36.5% at 2 FPS to 27.8% at 1 FPS**, and mean
track duration falls from **268.5 s at 3 FPS to 156.6 s at 1 FPS**. Detection
stays largely intact; it is temporal continuity that fails. `[T22]`

**FACT** — Separate work evaluating subsampled rates from 25 Hz down to 1 Hz
finds significant drops below 10 Hz and concludes current tracking approaches
"are not suited for lower frame rates". `[T22]`

**ASSUMPTION** — There is therefore a **hard floor of roughly 3–5 analysed frames
per second per camera** for anything needing identity over time — line crossing
with direction, loitering, dwell, counting, or "did this person enter and then
leave". Detection-only tasks ("is there a person in this frame") have no such
floor. *(Basis: `[T22]`. The exact floor is scene-dependent and must be measured
on real footage.)*

**FACT [rig-measured]** — On the recorder in this repository, hardware limits
established by testing are a **total budget of 120 fps across all 8 channels**,
and 25 fps is achievable **on channel 1 only**. `[T38]`

**CALCULATION** — 120 fps ÷ 8 channels = **15 fps per channel** if shared evenly;
the five channels that have cameras attached can be given more only by starving
the three that do not — which is exactly what `[T38]` records being done.

### 1.6 Resolution

**FACT** — IEC/EN 62676-4:2015 defines DORI pixel densities on the target plane:
**Detection 25 px/m, Observation 62 px/m, Recognition 125 px/m, Identification
250 px/m** `[T8]`, carried in
[competitive-landscape.md](../competitors/competitive-landscape.md) §6.3.

**FACT** — The **2025 revision of IEC/EN 62676-4 raises the bar.** It replaces
DORI with a seven-level model (OODPCVS) split by object type. For high-pixel-density
objects: **Perceive 125 px/m, Characterize 250 px/m, Validate 500 px/m,
Scrutinize 1500 px/m**; for low-pixel-density objects: Overview 20, Outline 40,
Discern 80 px/m. The task previously called "Identification" at 250 px/m is now
"Validation" at **500 px/m**. `[T9]` *(CCTV-design-tool vendor's summary of the
standard — see the retrieval caveat above; verify before use.)*

**If `[T9]` is accurate, the pixel-density requirement for identification-grade
imagery doubled between the 2015 and 2025 editions of the governing standard.**
Every existing camera on every existing estate was specified against the older,
easier number — or against no number at all.

**FACT** — BriefCam's stated minimum object size is **12–32 pixels** depending on
object class ([competitive-landscape.md](../competitors/competitive-landscape.md) §6.3).

**FACT** — ANPR needs roughly **250 px/m** to resolve plate characters
([competitive-landscape.md](../competitors/competitive-landscape.md) §6.3).

**FACT** — "1080N" is not 1080p. It is **960×1080** — half the horizontal
resolution of 1080p, about 1 megapixel against 2.1 — used by analog-HD DVRs (AHD,
HD-TVI, HD-CVI) to manage bandwidth and storage. `[T31]`

**FACT [rig-measured]** — The recorder in this repository encodes 1080N, and
[`dvr.py`](../../../dvr.py) has to **stretch every frame horizontally by 2×** to
restore the aspect ratio before it is usable. Resolution is **fixed** at 1080N on
this device — it is not a setting. `[T38]`

**This is a camera-quality trap that looks like a resolution and is not one.** A
1080N stream advertises "1080" and delivers half the horizontal pixel density.
Every horizontal DORI/OODPCVS figure is halved on such a device, and the stretch
performed to restore the aspect ratio manufactures no information — it
interpolates. A number plate that measures 250 px/m wide in the stretched image
was 125 px/m in the encoded one.

**UNKNOWN** — How much of the installed base at the target sites is analog-HD
behind a DVR/XVR rather than native IP. The problem statement says "standard
IP-based CCTV cameras"; the rig in this repository is an analog-HD XVR that
*presents* an IP/RTSP interface. Those are different things, and the distinction
is not resolved anywhere in the domain research.

### 1.7 The recorder in front of the camera is a hard limit

**FACT [rig-measured]** — On the recorder in this repository, established by
testing: resolution is fixed at 1080N; the **total encoder budget is 12,288 kbps
and 120 fps across all 8 channels**; and 2048 kbps per channel on the five live
channels is only possible **because the three empty channels are starved down to
320 kbps / 1 fps**. `[T38]`

**FACT [rig-measured]** — The firmware **returns OK for values it then silently
discards**. The only way to know what actually landed is to read the
configuration back. `[T38]`

**ASSUMPTION** — Where an analog-HD DVR/XVR sits between cameras and network, it —
not the camera and not the analytics software — sets the ceiling on resolution,
frame rate and bitrate, and that ceiling is a *shared* budget across channels.
Adding an analytics consumer cannot raise it. *(Basis: `[T38]`. Single device;
must be checked against the actual estate.)*

**HYPOTHESIS** — Any platform that configures cameras or recorders must **verify
by read-back rather than trust the response**, and must treat a device's
advertised capability as a claim to be tested. *(Basis: `[T38]`'s silent-discard
behaviour, and `[T4]`'s note that ONVIF feature implementation "rests with the
camera manufacturer".)*

### 1.8 Camera compatibility — the state of the art

**FACT** — The ingest side of the market has effectively standardised on **RTSP +
ONVIF Profile S**, with per-model compatibility work layered on top
([competitive-landscape.md](../competitors/competitive-landscape.md) §7.1).

**FACT** — Irisity claims the broadest stated ingest in the survey: any camera via
RTSP/ONVIF, **including analog via a DVR**
([competitive-landscape.md](../competitors/competitive-landscape.md) §7).

**ASSUMPTION** — Compatibility work is unavoidable, unbounded, and does not
finish. It is an operating cost of the product rather than a phase of it.
*(Basis: Milestone's bi-monthly device packs and 16,500-device list, and
Verkada's compatibility lab — both in
[competitive-landscape.md](../competitors/competitive-landscape.md) §6.4.)*

**UNKNOWN** — Whether a "universal driver" fallback of the kind Milestone ships is
achievable by a small team, and what fraction of devices it would cover.

---

## 2. Video pipeline

### 2.1 Ingest

**FACT [rig-measured]** — A robust ingest against a real recorder needs, at
minimum: forced TCP transport, an explicit socket timeout, a bounded buffer so a
slow consumer drops frames rather than backing up a queue, per-channel threads so
one dead channel cannot stall the others, and exponential reconnect backoff.
[`dvr.py`](../../../dvr.py) implements all five, each with a comment recording the
failure it was written to fix. `[T38]`

**ASSUMPTION** — The correct ingest posture is **"only the newest frame matters"**
for live analytics, and "every frame matters" only for recording. These are
different pipelines with different queueing semantics and should not be conflated.
*(Basis: `[T38]`'s design; a common pattern, not a sourced principle.)*

**UNKNOWN** — Reconnect behaviour under the failure modes that actually occur at a
remote site: link flap, power brownout on the camera, DVR reboot, NTP step, and
IP address change. The rig exercises none of these.

### 2.2 Decoding

**FACT** — NVIDIA's published DeepStream figures show decode is a first-order cost
and is **codec-dependent in a counter-intuitive direction**. For a full pipeline
(detection + two classifiers + tracking) at 1080p30:

| Device | 1080p30 streams, H.265 | 1080p30 streams, H.264 |
|---|---|---|
| Jetson Orin Nano | 13 | 8 |
| Jetson Orin NX | 16 | 13 |
| Jetson AGX Orin | 37 | 15 |
| T4 | 45 | 31 |
| A30 | 150 | 98 |
| H100 | 229 | 148 |

`[T13]` *(NVIDIA's own figures, with output rendering disabled — i.e. an upper
bound, not a deployment number.)*

**H.264 costs you between a third and well over half of your stream capacity
compared with H.265 on the same silicon.** On AGX Orin the published gap is 37 vs
15 — a factor of 2.5.

**ASSUMPTION** — The H.264/H.265 gap reflects the decoder's optimisation target
rather than anything intrinsic to H.264. *(Not stated by `[T13]`; the tables give
the numbers without explaining them. Could also reflect different test bitrates.
**Must be verified experimentally** — see [§13](#13-unknowns-that-must-be-validated-experimentally), E-3.)*

**This matters more for IBVAP than for a greenfield deployment.** An existing
estate is more likely to be H.264 than H.265 ([§1.3](#13-codecs)), so the
platform inherits the more expensive half of this table.

**FACT** — **You cannot cheaply "skip" to an arbitrary frame in a long-GOP
stream.** P-frames are predicted from their predecessors, so producing frame *n*
requires decoding everything back to the last I-frame. The only cheap subsampling
is I-frame-only decoding, which caps the analysis rate at one frame per GOP.
*(This follows directly from how H.264/H.265 inter-prediction works; it is
implicit in `[T19]`'s premise that compressed-domain analysis is worth doing
precisely because full decode is expensive.)*

**CALCULATION** — On the rig in this repository the encoder is configured with
`GOP = FPS` — a one-second GOP `[T38]`. I-frame-only decoding therefore yields
**1 analysed frame per second**, which is below the ~3 fps tracking floor
established in [§1.5](#15-frame-rate). **I-frame-only sampling and multi-object
tracking are mutually exclusive on this configuration.**

**This is the pipeline's central structural finding.** Decode cost is essentially
*independent of the analytics frame rate*, because you must decode the frames you
intend to throw away. The levers that actually reduce decode cost are: (a) ask
the device for a smaller sub-stream ([§1.4](#14-stream-profiles-and-sub-streams)),
(b) use hardware decode, or (c) work in the compressed domain
([§2.3](#23-frame-sampling)). Turning the inference rate down is not one of them.

**FACT** — Jetson Orin modules publish a decode capability of **18 × 1080p30
H.265 (Orin Nano), 23 × (Orin NX), 22 × (AGX Orin)** in isolation `[T11]` — i.e.
substantially more than the end-to-end pipeline numbers in `[T13]`, confirming
that decode alone is not the only bottleneck once inference and tracking are
added.

### 2.3 Frame sampling

**FACT** — **Reducto** (SIGCOMM 2020) filters **51–97% of frames** at the camera
using cheap frame-differencing features, while meeting a target accuracy, by
having the server select the best low-level feature per query. `[T18]`

**FACT** — **FilterForward** achieves roughly an **order-of-magnitude bandwidth
reduction** by running lightweight "microclassifiers" on constrained edge nodes
that share computation to detect dozens of events, sending only relevant frames
onward. `[T17]`

**FACT** — Motion vectors are already present in the H.264/H.265 bitstream as
macroblock metadata; extracting them is linear in the number of macroblocks and
frames, enabling motion analysis **without full decode**. `[T19]`

**HYPOTHESIS** — A two-tier sampler — compressed-domain motion vectors as a nearly
free first filter, then full decode and inference only on candidate segments — is
the highest-leverage single design idea available for a power- and
bandwidth-constrained site. It is well supported by `[T17][T18][T19]` and by
[competitive-landscape.md](../competitors/competitive-landscape.md) §8.2's
"process locally, ship metadata" pattern, **but no source retrieved measures it on
border-type scenes** (sparse activity, wind-moved vegetation, livestock, IR at
night). It must be tested before it is designed around.

**ASSUMPTION** — Motion-vector filtering will behave badly in exactly the
conditions the domain research flags: wind-moved vegetation, rain, insects on the
lens, and headlight glare all produce large motion-vector energy with no object
present ([competitive-landscape.md](../competitors/competitive-landscape.md) §9,
P4). *(Interpretation; not measured.)*

### 2.4 Preprocessing

**FACT [rig-measured]** — On a 1080N device, the aspect-ratio correction is
mandatory before anything else: the frame must be stretched 960×1080 → 1920×1080
or "everything looks tall and thin". `[T38]`

**ASSUMPTION** — Preprocessing for an existing-CCTV platform is not a formality.
It must at minimum handle: anamorphic correction, letterboxing to the model's
input aspect, colour-space conversion, and the fact that IR-illuminated night
frames are effectively monochrome. *(Basis: `[T38]` for the first,
[§3.10](#310-night-and-low-light-analytics) for the last. Not a sourced list.)*

**HYPOTHESIS** — Resizing a 960×1080 frame up to 1920×1080 before inference costs
compute and adds no information; feeding the model the native 960×1080 frame and
correcting geometry only in the *coordinates* of the output would be cheaper and
lossless. Needs testing — models trained on natural aspect ratios may lose
accuracy on anamorphic input.

### 2.5 Inference

**FACT** — Published single-inference latencies from Frigate's hardware
documentation `[T14]`:

| Accelerator | Model | Inference time |
|---|---|---|
| Google Coral Edge TPU | default SSD MobileNet | ~10 ms |
| Hailo-8 | YOLOv6n | ~7 ms |
| Hailo-8 | SSD MobileNet v1 | ~6 ms |
| Hailo-8L | YOLOv6n | ~11 ms |
| Intel Arc A750 (OpenVINO) | MobileNetV2 | ~4 ms |
| Intel NPU | MobileNetV2 | ~6 ms |
| Intel HD 620 iGPU | — | 15–25 ms |
| NVIDIA RTX 3070 | YOLO-NAS s-640 | ~25 ms |
| NVIDIA RTX 3070 | YOLO-NAS t-320 | ~6 ms |
| NVIDIA RTX 3050 | YOLO-NAS t-320 | ~8 ms |

**FACT** — Frigate's own arithmetic: at 10 ms per inference a single Coral gives
"1000/10 = 100 frames per second" of detection throughput. `[T14]`

**CALCULATION** — At a 5 fps analysis rate, 100 detections/s is **20 cameras of
detection** on one Coral — *if* something else pays the decode cost, which on a
Coral-based design is the host CPU. The accelerator is rarely the binding
constraint; decode and memory bandwidth usually are.

**FACT** — NVIDIA's TAO model throughput on Jetson `[T13]`: PeopleNet-ResNet34 at
960×544 INT8 runs at **256 fps (Orin Nano), 372 fps (Orin NX), 970 fps (AGX
Orin)**; TrafficCamNet-ResNet18 at **419 / 590 / 1105 fps** respectively. On
datacenter parts: T4 912 fps, L4 1674 fps, A30 3273 fps, H100 6920 fps for
PeopleNet.

**Compare those inference numbers against the end-to-end stream counts in
[§2.2](#22-decoding).** Orin Nano can run PeopleNet at 256 fps but sustains only
8 full-pipeline H.264 streams at 1080p30. Roughly 240 frames per second of
inference capability is unreachable because decode, tracking and memory movement
consume the budget first.

**FACT [MARKET, licensing]** — Ultralytics YOLO models (YOLOv8, YOLO11 and
successors) are distributed under **AGPL-3.0** by default; distributing or hosting
a product that includes them requires either releasing the complete source of that
product under AGPL-3.0 or purchasing an Ultralytics Enterprise Licence. `[T35]`

**This is a cost and licensing constraint on a project whose problem statement
requires the solution to be "cost-effective".** It does not decide the stack —
permissively licensed detectors exist — but it means detector choice is a legal
question as well as an accuracy one, and it belongs in the architecture stage with
that framing.

**UNKNOWN** — Whether any of the target deployment's procurement or security
accreditation regimes constrain model provenance, model licensing, or the use of
models with weights trained on foreign datasets.

### 2.6 Tracking

**FACT** — **ByteTrack** associates almost every detection box rather than only
high-scoring ones, recovering occluded objects from low-confidence detections. It
reports **MOTA 80.3 / IDF1 77.3 / HOTA 63.1** on MOT17 at **30 FPS on a single
V100**. `[T20]`

**FACT** — Reported 2025 state of the art on MOT17 is around **IDF1 82.1 / MOTA
81.5 / HOTA 65.9**, and on the far more crowded MOT20 (≈150 pedestrians per
frame) around **IDF1 81.2 / MOTA 78.4 / HOTA 65.7**. `[T21]` *(figures reported
by the methods' own authors — upper bounds.)*

**FACT** — Occlusion remains the dominant failure mode: it "can result in
unreliable appearance features, inaccurate motion estimation, and biased
association cues". `[T21]`

**ASSUMPTION** — A HOTA in the mid-60s on a curated benchmark translates to
materially worse identity persistence on a border scene, because the benchmarks
are daylight, urban, and shot by cameras positioned for the task. *(Basis: the
general benchmark-to-deployment gap documented for face recognition `[T23b]`,
anomaly detection `[T27]` and re-identification `[T37]`. Not measured for MOT
specifically — this is the assumption most worth testing.)*

**FACT** — Cross-camera **person re-identification** degrades markedly on unseen
domains: state-of-the-art models tested outside their training dataset show
"significant performance drops" compared with their Market-1501/MSMT17 numbers,
with the lowest scores on the Airport dataset — the one closest to real
surveillance. `[T37]`

**ASSUMPTION** — Cross-camera identity ("the same person appeared at BOP-14 and
then at the check post") should be treated as a research problem, not a feature,
on this estate. *(Basis: `[T37]`, plus the fact that a border estate has widely
separated, uncalibrated, differently-lit cameras — the worst case for appearance
matching.)*

**FACT** — Tracking against a **moving PTZ camera** is a different and harder
problem: "methods designed for fixed cameras cannot achieve accurate background
subtraction on videos captured by moving cameras", and when a PTZ rotates, new
background models must be synthesised before detection can continue. `[T36]`

**ASSUMPTION** — Any analytic that depends on a stable background — virtual fence,
loitering, dwell, abandoned object — is **invalid while a PTZ is slewing or on a
preset tour**, and the platform must know when that is happening. ONVIF PTZ status
is the obvious source. *(Basis: `[T36]` plus `[T4]`'s note that Profile T makes
PTZ mandatory. Not sourced as a design practice.)*

### 2.7 Event generation

**FACT** — The dominant behavioural mechanism across the entire market is a
**configured rule**: zone, line, direction, dwell time
([competitive-landscape.md](../competitors/competitive-landscape.md) §9, P3).
Axis, for example, offers five fixed scenario types with a maximum of ten per
camera (ibid. §4.2).

**FACT** — Academic sources document the failure mode of that approach:
"Rule-based models with fixed thresholds find it difficult to detect actual
unusual behaviors in unpredictable environments, resulting in high false positive
rates and missed anomalies"
([competitive-landscape.md](../competitors/competitive-landscape.md) §4.2).

**FACT** — ONVIF Profile M defines event delivery over the metadata stream, the
ONVIF event service, or **MQTT**, and defines rule configuration as part of the
profile. `[T6]`

**ASSUMPTION** — There are two distinct event products, and conflating them is a
design error: a **per-frame metadata stream** (every object, every analysed frame)
and a **discrete event** (a rule fired). The first is a firehose sized by scene
activity; the second is sized by how often something happens. Their bandwidth and
storage profiles differ by orders of magnitude — quantified in
[§5.3](#53-what-actually-has-to-cross-the-link). *(Interpretation; `[T6]` supports
that both exist as separate ONVIF concepts.)*

### 2.8 Where the pipeline actually breaks

Collected here because these are the recurring, non-obvious failure modes rather
than the headline ones.

**ASSUMPTION** — Ranked by expected frequency at a remote site, and each needing
verification:

1. **Timestamps.** Multi-camera correlation, evidential hashing and rule timing
   all depend on a trustworthy clock. A disconnected site has no NTP source unless
   one is provided locally. See [§6.5](#65-evidentiary-integrity).
2. **Reconnect storms.** A link flap that drops 8 RTSP sessions at once, all of
   which reconnect on the same backoff schedule.
3. **Encoder configuration drift.** Someone changes the DVR's resolution or frame
   rate and every analytic's calibration silently becomes wrong. `[T38]`'s
   silent-discard behaviour makes this worse, not better.
4. **PTZ movement invalidating stable-background analytics.** `[T36]`
5. **Long-GOP / dynamic-GOP encoding** making seek and clip extraction imprecise —
   see [§6.2](#62-event-clips).
6. **Frame drops presenting as motion.** A dropped second of video looks like a
   teleport to a tracker.

**UNKNOWN** — Which of these dominates in practice. None has been observed on a
border estate by this project.

---

## 3. Computer vision — capability by capability

Ordered as the problem statement orders them. For each: what the published
evidence supports, what it depends on, and how it is expected to behave on
existing CCTV rather than on a benchmark.

> **Framing carried forward from the domain research.** i-LIDS, the UK government
> benchmark, certifies an analytic either as a **primary (sole) detection system**
> or only as a **secondary (support)** measure
> ([domain-research.md](../domain/domain-research.md) §6.7). That distinction is
> the right axis for every capability below, and this document uses it. Which side
> IBVAP targets is a product decision and is not made here.

### 3.1 Person detection

**Achievability: high, as a support-grade analytic; conditional as primary.**

**FACT** — Person detection is claimed with evidence by essentially every vendor
surveyed, including on third-party cameras
([competitive-landscape.md](../competitors/competitive-landscape.md) §4).

**FACT** — Throughput is not the constraint: PeopleNet at 960×544 INT8 runs at
256 fps on an Orin Nano `[T13]`.

**FACT** — The constraint is pixels on target. Detection is the *least* demanding
DORI level at 25 px/m `[T8]`, and minimum object sizes of 12–32 px are documented
([competitive-landscape.md](../competitors/competitive-landscape.md) §6.3) — so
a person at long range on a wide-angle camera may be below the model's floor
regardless of the model.

**UNKNOWN** — The actual pixel density on target at the ranges border cameras are
pointed at. This is measurable from a single site survey and is not known.

### 3.2 Vehicle detection and classification

**Achievability: detection high; fine-grained classification conditional.**

**FACT** — TrafficCamNet at 960×544 INT8 runs at 419 fps on an Orin Nano and 1105
fps on AGX Orin `[T13]` — again, throughput is not the constraint.

**FACT** — Vehicle detection and classification is claimed by every vendor
surveyed ([competitive-landscape.md](../competitors/competitive-landscape.md) §4).

**ASSUMPTION** — "Classification" in these products means coarse type (car / truck
/ bus / motorcycle / bicycle), not make, model, colour or load. Fine-grained
attributes need Recognition-grade pixel density (125 px/m under the 2015 model,
250 px/m under the 2025 "Characterize" level `[T8][T9]`) and are far more
sensitive to viewpoint and illumination. *(Interpretation of the vendor claims in
[competitive-landscape.md](../competitors/competitive-landscape.md) §4 against
`[T8][T9]`; the vendors do not disaggregate.)*

**[BORDER] ASSUMPTION** — The vehicle classes that matter operationally on a
border road — a loaded porter's cart, a tractor-trailer carrying forest produce,
livestock being driven — are not COCO classes and are not TrafficCamNet classes.
The SSB event catalogue is dominated by contraband, forest products, cattle and
currency
([ssb-operational-context.md](../domain/ssb-operational-context.md) §12), none of
which maps to a standard vehicle taxonomy. *(Interpretation of that catalogue
against the models' published class lists.)*

### 3.3 Multi-object tracking

**Achievability: high at ≥3 fps within one camera; low across cameras.**

Covered in [§2.6](#26-tracking). Summary: strong published results within a single
view at adequate frame rate `[T20][T21]`; a hard frame-rate floor around 3 fps
`[T22]`; occlusion as the dominant failure mode `[T21]`; cross-camera
re-identification degrading badly out of domain `[T37]`; and invalid while a PTZ
is moving `[T36]`.

### 3.4 Face detection

**Achievability: high where a face is large enough; that is the whole question.**

**FACT** — Face *detection* (is there a face) is distinguished throughout the
market from face *recognition* (whose face), and several vendors claim detection
without claiming recognition
([competitive-landscape.md](../competitors/competitive-landscape.md) §4).

**FACT** — Detection accuracy is most affected by "angle of faces and lighting"
([competitive-landscape.md](../competitors/competitive-landscape.md) §9, P4).

**ASSUMPTION** — Face detection on an overhead-mounted, wide-angle camera
installed for area overview will find very few faces, because such cameras look
down on the tops of heads. This is a mounting-geometry problem and no model fixes
it. *(Basis: NIST's finding that camera positioning and mounting is decisive
`[T23b]`; not measured on the target estate.)*

### 3.5 Face recognition

**Achievability: low to moderate on existing CCTV, and this is NIST's own
finding — not a pessimistic reading of it.**

**FACT** — NIST's FIVE programme evaluated face recognition of **non-cooperating
subjects recorded passively**, searching video from fixed cameras against
portrait-style galleries of up to 48,000 identities across six datasets. `[T23a]`

**FACT** — NIST's summary of the result: portrait-photograph matching "can exceed
99 percent in some applications", whereas in video "subjects may be identified
anywhere from around **60 percent** of the time to more than 99 percent, depending
on video or image quality." The three named degradations are **small faces, uneven
lighting, and non-forward-facing angles**. `[T23b]`

**FACT** — NIST's conclusion, quoted: video face recognition accuracy "may
approach that of still-photo face recognition, **but only if image collection can
be improved**", and NIST recommends expertise in "camera positioning and
mounting" alongside lighting and optics, plus **limiting the gallery size**.
`[T23b]`

**"Only if image collection can be improved" is precisely what a
software-on-existing-cameras platform is forbidden from doing.** The problem
statement's premise — deliver FRS without touching the hardware — is in direct
tension with the strongest independent evidence available on what makes FRS work.
This is recorded as a research finding; what to do about it is a product decision.

**FACT** — Current NIST 1:N testing reports FNIR at a threshold constraining FPIR
to 0.003, against galleries of up to 12 million; leading algorithms report error
rates below 0.1% **on mugshot- and visa-quality still imagery**. `[T24]` *(These
figures are not transferable to CCTV video and NIST does not present them as
such.)*

**[MARKET] FACT** — Under EU AI Act Article 5, real-time remote biometric
identification in publicly accessible spaces for law enforcement is prohibited by
default from 2 February 2025, subject to narrow exceptions
([competitive-landscape.md](../competitors/competitive-landscape.md) §9, P9).

**[SIH/SSB] FACT** — The named validation force has **already procured** a CCTV
setup with Automatic Face Recognition and ANPR
([ssb-operational-context.md](../domain/ssb-operational-context.md) §6.1), and
open legal questions exist about applying face recognition to a population
crossing a treaty-open border lawfully (ibid. §11.6).

**UNKNOWN** — Whether a *gallery* even exists for the deployment context. NIST's
own advice is to limit gallery size `[T23b]`; a watchlist of tens of known
traffickers is a completely different technical problem from open-set
identification, and which one is intended is not established anywhere.

### 3.6 ANPR

**Achievability: moderate at a check post with a purpose-aimed camera; low on a
general-purpose camera.**

**FACT** — The academic survey documents accuracy at each stage on curated
datasets: plate extraction 89.7–100%, segmentation 97.75–99.75%, character
recognition 90–98.1%. But **end-to-end** numbers on realistic datasets diverge
sharply: **93.53% on SSIG versus 78.33% on UFPR-ALPR** — the harder, more
realistic set. `[T25]`

**A ~15-point end-to-end drop between two research datasets, both curated, is the
best available estimate of how fast ANPR degrades as conditions get real.**

**FACT** — Documented limiting factors: plate condition, non-standardised formats,
complex scenes, camera quality, **camera mount position**, tolerance to
distortion, motion blur, contrast, reflections, tilt/skew, fog, processing and
memory limits, and day/night conditions. `[T25]`

**FACT** — Dedicated ANPR cameras achieve their 95–99% figures using **fast or
global shutters** to eliminate motion blur, and **IR illuminators** tuned to the
retroreflective plate. `[T25b]` *(vendor material — but the mechanism is
physical.)*

**FACT** — The software-only paths that exist in the market attach physical
constraints rather than removing them: Genetec AutoVu Flexreader works on existing
cameras but only up to **30 mph / 50 km/h**; Milestone XProtect LPR needs the
camera to look down on the vehicle at **no more than 30 degrees**
([competitive-landscape.md](../competitors/competitive-landscape.md) §6.2).

**"ANPR without dedicated ANPR cameras" is already solved, twice, by the two
largest VMS vendors — and both solutions constrain speed and mounting angle. The
dependency moved from the camera's silicon to the camera's mounting.** (ibid.)

**[MARKET:IN] FACT** — India has roughly 210 million vehicles and **over 50
different number-plate types**, against countries with standardised plates where
ANPR accuracy often exceeds 90%
([domain-research.md](../domain/domain-research.md) §6.7).

**ASSUMPTION** — ANPR is achievable where a camera can be *aimed at a lane* — an
ICP, a check post, a barrier — and is not achievable on a wide-area border-road
camera, because a plate at that range and angle is well below 250 px/m.
*(Basis: `[T25]` plus the mounting constraints above. Not measured.)*

### 3.7 OCR (general)

**Achievability: high for controlled text; low for incidental scene text.**

**FACT** — i-PRO's ANPR-adjacent capability is listed in the market survey as
"P (OCR)" rather than full ANPR
([competitive-landscape.md](../competitors/competitive-landscape.md) §4) —
i.e. the industry itself treats general OCR and plate reading as different
capabilities with different accuracy.

**ASSUMPTION** — General scene OCR (container markings, unit signage, vehicle
lettering) inherits every ANPR failure mode in `[T25]` without the compensating
advantages of a standardised, retroreflective, roughly rectangular, roughly
horizontal target. It should be assumed harder than ANPR, not easier.
*(Interpretation of `[T25]`; no source directly compares them.)*

**UNKNOWN** — Whether any operationally useful text exists in these scenes at all.
Nothing in the domain research names a text-reading requirement other than plates.

### 3.8 Virtual fence / line crossing

**Achievability: high as a mechanism; the difficulty is entirely in nuisance
rejection.**

**FACT** — Virtual fence / intrusion detection is claimed by every vendor surveyed,
including the free open-source option
([competitive-landscape.md](../competitors/competitive-landscape.md) §4).

**FACT** — In the US SBInet programme, **90 per cent of sensor alerts were false
alarms** ([domain-research.md](../domain/domain-research.md) §4.2).

**FACT** — CIBMS-related analysis reports false alarms and sensor malfunctions as a
leading technical issue, and notes the design does not address distinguishing
infiltrators from wildlife or environmental triggers (ibid.).

**FACT** — Documented outdoor false-trigger sources: rain, fog and snow altering
contrast and sharpness; wind-moved vegetation producing constant pixel changes;
sunrise, sunset and vehicle headlights creating reflections and shadows "that
basic algorithms read as suspicious movement"
([competitive-landscape.md](../competitors/competitive-landscape.md) §4.1).

**The mechanism — a polygon, a line, a direction, a dwell timer — is trivial. The
product is the nuisance-alarm rejection, and that is where the entire industry's
effort goes** ([competitive-landscape.md](../competitors/competitive-landscape.md)
§9, P4).

**ASSUMPTION** — Object-class-gated rules ("a line crossing counts only if the
crossing object is classified as a person or a vehicle with confidence above X and
has been tracked for at least N frames") are strictly better than pixel-motion
rules, and are what the detection+tracking pipeline buys you. *(Basis: the
industry's move from VMD to object analytics, visible in
[competitive-landscape.md](../competitors/competitive-landscape.md) §4 where
Milestone alone is marked "P (VMD only)". Not independently measured.)*

**[SIH/SSB] FACT** — On the validation border, crossing is a **treaty right** for
Indian, Nepali and Bhutanese nationals, and MHA's own statement of the problem is
"misuse of open border", not intrusion
([ssb-operational-context.md](../domain/ssb-operational-context.md) §2.2, §14.1).
A line-crossing alarm that fired with perfect accuracy would still be almost
entirely noise there.

**This is the sharpest example in the whole research corpus of a capability being
technically achievable and operationally misdirected.** The technology question
and the product question have opposite answers, and the gap belongs to
`docs/02-product/`.

### 3.9 Loitering, dwell and "suspicious activity"

**Achievability: loitering and dwell — moderate, given tracking. "Suspicious
activity" — low, and this is the weakest capability in the problem statement.**

**FACT** — Loitering and dwell are rule constructions on top of tracking: they need
identity to persist for the dwell period, which puts them squarely on the ≥3 fps
tracking floor `[T22]` and makes them fail exactly when occlusion does `[T21]`.

**FACT** — Reported state-of-the-art on **UCF-Crime**, the standard real-world
surveillance anomaly benchmark (128 hours, 1,900 untrimmed videos, 13 anomaly
types), is around **88–90% frame-level AUC** — π-VAD 90.33%, RefineVAD 88.92%,
Ex-VAD 88.29%. `[T28]` *(self-reported by each method's authors.)*

**FACT — and this is the finding that matters** — A 2025 paper re-examining VAD
metrics and benchmarks reports that:

- Models scoring **94.55% AUC** on standard test sets collapse to **16.35% AUC**
  on same-scene evaluations with reversed labels — i.e. much of the reported
  performance is **scene overfitting**, not anomaly understanding.
- Methods with false-alarm rates **≤10%** on original test sets show a **42%
  average increase** in false alarms on "hard normal" benchmarks at threshold 0.5,
  **with some exceeding 70% FAR**.
- Human annotators agree on what counts as anomalous only at Fleiss' Kappa
  **0.51–0.68** — the ground truth itself is contested.
- AUC and AP are "insensitive to the temporal position of predictions", so a
  method that detects an event late scores the same as one that detects it
  immediately — despite early detection being the entire operational point.
`[T27]`

**Three independent things are wrong with "suspicious activity detection" as a
capability: the headline metric does not measure operational usefulness, the
reported accuracy is substantially scene memorisation, and the humans cannot
agree on the label.** The domain research separately records that "suspicious
activity" is undefined in the problem statement and in every retrieved source
([domain-research.md](../domain/domain-research.md) §5.7, Q-3).

**FACT** — The market has no consensus solution either: only rule engines (high
false-positive rate in unpredictable environments) and learned anomaly detection
(needs large "normal" training sets that must be relearned when normal changes),
plus vision-language models which are new and unproven in this domain
([competitive-landscape.md](../competitors/competitive-landscape.md) §4.2).

**HYPOTHESIS** — The only defensible near-term form of "suspicious activity" on
this estate is a **small set of explicitly defined, operator-authored composite
rules over reliable primitives** — e.g. "a person present in zone A between 2200
and 0500 for more than 90 seconds", "a vehicle stopped on the border road outside
a marked lay-by for more than 5 minutes" — rather than a learned anomaly model.
This is a testable proposition and is **not** a recommendation; it must be
validated against what operators actually consider suspicious, which is Q-3 in the
domain research and remains unanswered.

### 3.10 Night and low-light analytics

**Achievability: materially worse than daylight on visible cameras; good on
thermal, which most estates do not have.**

**FACT** — On the LLVIP night dataset, the same detector on the same scenes scores
**mAP@0.5:0.95 of 0.430 on visible light versus 0.651 on infrared** — a **33.9%
relative drop** for visible-light-only detection at night. `[T26]`

**FACT** — Multimodal (visible + thermal) fusion improves over infrared-only by
6.4% on FLIR and 7.2% on M3FD in the same study. `[T26]` *(self-reported by the
method's authors.)*

**FACT** — Infrared images "lack rich visual cues, such as color and detailed
information", and the similarity between heat sources and pedestrian features
reduces accuracy in complex outdoor environments. `[T26]`

**FACT** — "Night-time movement detection" is **not a distinct product feature
anywhere in the market**; it is an operating condition that every other feature
either survives or does not. Vendors sell it as image-sensor quality (Lightfinder,
WDR, IR illumination) or as a thermal camera, not as an analytic
([competitive-landscape.md](../competitors/competitive-landscape.md) §4.1).

**FACT** — Verkada explicitly states its people and vehicle analytics "are only
supported on visible (or non-thermal) video streams" — the single explicit vendor
statement found on thermal, and it is a negative (ibid.).

**FACT** — Thermal analytics *is* solved — by Teledyne FLIR and SightLogix — but
only by buying thermal cameras with the analytics inside
([competitive-landscape.md](../competitors/competitive-landscape.md) §10, G3).

**FACT** — Thermal is not weather-immune: fog and rain severely limit thermal
range because scattering in water droplets attenuates the infrared signal
([domain-research.md](../domain/domain-research.md) §6.3).

**ASSUMPTION** — IR-illuminated night video is effectively **monochrome**, which
removes colour as a feature. Every appearance-based mechanism that depends on
colour — re-identification, clothing description, vehicle colour, "find the man in
the red jacket" — degrades or fails at night on such cameras. *(Basis: how IR
illumination and IR-cut-filter removal work; not stated in a retrieved source.
Directly testable on the rig in this repository.)*

**ASSUMPTION** — IR illuminators create their own artefacts: hotspot glare on
nearby surfaces, insects and dust attracted to and lit by the emitter, and
retroreflection from vegetation and signage. Each is a nuisance-alarm source that
exists only at night. *(Not sourced; widely observed. Testable on the rig.)*

**[BORDER] ASSUMPTION** — Infiltration and smuggling concentrate in darkness and
poor visibility — exactly when conventional CCTV performs worst
([domain-research.md](../domain/domain-research.md) §5.6). If true, the
capability with the worst technical outlook carries the highest operational
weight. This inversion should be treated as the central risk of the whole
programme until measured.

**UNKNOWN** — What proportion of border CCTV is thermal versus visible, and
whether visible cameras have IR illuminators, true day/night sensors, or neither
([domain-research.md](../domain/domain-research.md) §6.3, Q-15).

---

## 4. Compute

### 4.1 CPU vs GPU vs NPU

**FACT** — The published inference latencies in [§2.5](#25-inference) span a
range of roughly 4 ms (discrete Intel GPU, small model) to 25 ms (RTX 3070,
larger model at 640px), with dedicated low-power NPUs (Coral 10 ms, Hailo-8
6–7 ms) sitting in the middle at a fraction of the power. `[T14]`

**FACT** — Power figures for the low-power accelerators: **Hailo-8 delivers 26
TOPS at 2.5 W typical (8.25 W maximum)**; **Google Coral Edge TPU delivers 4 TOPS
at 2 W** — "2 TOPS per watt". `[T15][T16]`

**FACT** — Jetson Orin power envelopes: **Orin Nano 7–25 W, Orin NX 10–40 W, AGX
Orin 15–60 W**, at 34–67 / 117–157 / 241–248 sparse INT8 TOPS respectively.
`[T11]`

**FACT** — **Jetson Orin Nano has no hardware video encoder.** NVENC was removed
relative to the earlier Jetson Nano; encoding is done in software on the CPU, at
"1080p30 supported by 1-2 CPU cores" and up to about three 1080p30 streams in
total. `[T12]`

**A device marketed as an edge AI module cannot hardware-encode a single clip.**
Any design that produces event clips by re-encoding on an Orin Nano is spending
one to two CPU cores per stream to do it. Storing the original bitstream avoids
this entirely — reinforcing the hypothesis in [§1.3](#13-codecs).

**ASSUMPTION** — CPU-only inference is viable for a *single* camera at a low
analysis rate with a small model, and is not viable for a multi-camera site. No
source retrieved gives CPU-only figures for the models above, which is itself
telling: Frigate's hardware page recommends an accelerator in every configuration
it documents `[T14]`. *(This is an argument from the shape of the documentation,
not a measurement. It must be measured — see
[§13](#13-unknowns-that-must-be-validated-experimentally), E-2.)*

### 4.2 Decode is a first-class cost, not an implementation detail

Established in [§2.2](#22-decoding). The consequence for compute sizing: **a
device's inference throughput is not its stream capacity.** NVIDIA's own numbers
show Orin Nano running PeopleNet at 256 fps but sustaining only 8 full-pipeline
H.264 streams at 1080p30 `[T13]`. Sizing a deployment on TOPS or on model FPS will
overestimate capacity by a large factor.

### 4.3 Approximate resource requirements — a worked estimate

**CALCULATION.** Inputs, all stated: 8 cameras; 1080p H.264 main streams; analysis
at 5 fps per camera; a detector in the PeopleNet/YOLO-small class; tracking
enabled.

| Quantity | Value | Source of input |
|---|---|---|
| Full-pipeline 1080p30 H.264 streams, Orin Nano | 8 | `[T13]` |
| Full-pipeline 1080p30 H.264 streams, Orin NX | 13 | `[T13]` |
| Detection frames required (8 × 5 fps) | 40 fps | this calculation |
| Detection throughput available, Orin Nano (PeopleNet) | 256 fps | `[T13]` |
| Headroom on detection | ≈ 6× | this calculation |
| Power envelope, Orin Nano | 7–25 W | `[T11]` |

**Reading of the calculation:** an 8-camera site is at or slightly beyond the
published limit of the smallest current Jetson if the streams are 1080p30 H.264
and are decoded in full, **even though the detector has roughly six times the
throughput needed**. The binding constraint is decode, not inference. Requesting
lower-resolution sub-streams ([§1.4](#14-stream-profiles-and-sub-streams)) or a
lower source frame rate is what changes this number.

**These are NVIDIA's figures with output rendering disabled `[T13]` — an upper
bound published by the vendor of the hardware. A real deployment should be sized
well below them, and the margin must be measured, not guessed.**

**UNKNOWN** — Everything about the actual sizing: camera count per site, source
resolution and frame rate, codec, scene activity level, and the analytics actually
required. Each of Q-1, Q-2 in
[domain-research.md](../domain/domain-research.md) §8 must be answered before this
calculation is anything but an illustration of method.

### 4.4 Edge versus centralised

**FACT** — Four deployment patterns exist in the market — on-camera, on-site
server/appliance, on-site bridge with cloud brain, and pure cloud — and every
vendor sits at one point on a single continuous trade of **where you pay**: camera
silicon, site hardware, bandwidth, or scope
([competitive-landscape.md](../competitors/competitive-landscape.md) §5.1).

**FACT** — Three vendors independently converged on hub-and-site: BriefCam Nexus,
Ambient.ai and Genetec Cloudlink all process locally and ship metadata centrally.
**"Process locally, ship metadata centrally" is settled industry practice, not an
opening** (ibid. §5.2).

**FACT** — The bandwidth spread between the extremes is four orders of magnitude —
Verkada's 20 kbps per camera against Genetec Cloud's "recording throughput plus
30%" — "explained entirely by where the analysis happens" (ibid. §8.1).

**[BORDER] ASSUMPTION** — Centralised processing is bandwidth-infeasible at scale
on this network. Carried forward from
[domain-research.md](../domain/domain-research.md) §6.2, which reaches it from
CIBMS's unspecified backbone, constrained-uplink systems research, and per-stream
bitrate figures. Nothing in this pass weakens it; [§5](#5-networking) quantifies
it.

**ASSUMPTION** — Every appliance-based architecture imports a **physical
maintenance obligation at each site**, and where 42% of sites cannot be reached by
road ([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.1)
that obligation dominates cost
([competitive-landscape.md](../competitors/competitive-landscape.md) §8.5).

**This is the real edge-vs-centralised trade for this deployment, and it is not
a compute trade.** Edge processing solves bandwidth and creates a logistics
problem; centralised processing solves logistics and creates a bandwidth problem
the network cannot absorb. Neither is free, and the choice belongs in
`docs/04-architecture/`.

### 4.5 Multi-camera scaling

**FACT** — Published full-pipeline stream counts scale roughly linearly with
silicon: 8 (Orin Nano) → 13 (Orin NX) → 15 (AGX Orin) → 31 (T4) → 98 (A30) → 148
(H100), for H.264 at 1080p30 `[T13]`.

**FACT** — Batching is required to reach those numbers: "batch sizes must match
number of concurrent streams for optimal throughput", and DeepStream's published
figures disable OSD, tiling and rendering entirely `[T13]`.

**ASSUMPTION** — The scaling axis for this deployment is **site count, not camera
count** — many small isolated sites, not one large cluster
([domain-research.md](../domain/domain-research.md) §6.5). That inverts the usual
economics: batching efficiency, which is what makes the large numbers above
achievable, is unavailable at a 2-camera post. *(Interpretation.)*

**ASSUMPTION** — Per-camera pricing, the near-universal market norm, penalises
exactly this shape — many sites, few cameras each, low utilisation per camera
([competitive-landscape.md](../competitors/competitive-landscape.md) §9, P6).

### 4.6 Power

**FACT** — **No vendor in the competitive survey publishes a power budget for its
analytics workload.** Genetec, BriefCam, Irisity and Ambient.ai all specify NVIDIA
GPUs without stating watts
([competitive-landscape.md](../competitors/competitive-landscape.md) §8.4).

**FACT** — Published envelopes for the parts that do disclose: Orin Nano 7–25 W,
Orin NX 10–40 W, AGX Orin 15–60 W `[T11]`; Hailo-8 2.5 W typical / 8.25 W max
`[T15]`; Coral Edge TPU 2 W `[T16]`.

**CALCULATION** — A 15 W continuous load is 360 Wh/day, or **10.8 kWh/month**. A
60 W continuous load is 1.44 kWh/day and **43.2 kWh/month**. Add the cameras, the
switch, the recorder and conversion losses and a modest analytics node at a
generator-powered site is a real, recurring fuel line item.

**[BORDER] ASSUMPTION** — At a generator-powered BOP, power is **scheduled and
fuel-limited**, not continuous, and the fuel travels the same unroaded path as
everything else — so a continuously running compute load is a logistics cost, not
just an electrical one
([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.2).

**HYPOTHESIS** — Duty-cycled or activity-gated compute — the accelerator idles
until a cheap compressed-domain or PIR-style trigger wakes it — could reduce the
energy cost by a large factor at sites where activity is genuinely rare. This is
directly implied by the sampling literature `[T17][T18][T19]` but **no source
retrieved measures energy** rather than bandwidth or accuracy. It must be measured
before it is designed around.

**UNKNOWN** — The power budget actually available at a representative site. Q-7 in
[domain-research.md](../domain/domain-research.md) §8; unanswered.

---

## 5. Networking

### 5.1 Bandwidth — what a stream costs

**FACT** — A single H.264 IP camera stream is on the order of **5 Mbps**, and each
additional client pulling that stream multiplies the load off the camera
([domain-research.md](../domain/domain-research.md) §6.2).

**FACT** — H.265 delivers comparable quality at about half the bitrate (ibid.).

**FACT** — Axis Zipstream claims an **average 50% or better** bandwidth and storage
reduction versus standard compression, using dynamic GOP, dynamic frame rate and
region-of-interest quantisation that preserves "faces, tattoos and clothing
patterns" while compressing "white walls, lawns and vegetation" more aggressively.
`[T29]` *(vendor's own white paper.)*

**HYPOTHESIS** — Content-adaptive encoding of the Zipstream type is *hostile* to
downstream analytics in two specific ways, and this needs testing: **dynamic GOP**
lengthens the interval between I-frames, which worsens seek precision and raises
the cost of the I-frame-only sampling strategy in [§2.3](#23-frame-sampling);
**dynamic frame rate** reduces temporal resolution during quiet periods, which is
exactly when a slow-moving intruder appears, and can push the stream below the
~3 fps tracking floor `[T22]`. `[T29]` makes no claim either way about analytics.

**FACT [rig-measured]** — The rig's total encoder budget is 12,288 kbps across 8
channels `[T38]`. That is roughly the bitrate of **two and a half** typical
5 Mbps H.264 streams, spread across eight cameras.

### 5.2 Latency

**FACT** — RTSP's default session timeout is 60 s, and liveness must be
demonstrated by RTCP or by any RTSP request `[T1]`.

**FACT** — Genetec's cloud storage requires a guaranteed uplink of recording
throughput plus 30%, with a 99.9% SLA and **under 150 ms** latency
([competitive-landscape.md](../competitors/competitive-landscape.md) §8.1) — i.e.
the incumbent cloud architecture assumes a link quality a satellite-backed border
post does not have.

**FACT** — Satellite links are "typically high-latency, low-bandwidth and
expensive, making it difficult to offload data or receive updates efficiently"
([domain-research.md](../domain/domain-research.md) §6.2).

**ASSUMPTION** — End-to-end alert latency has at least five additive components —
encode/buffering at the camera, network transit, decode, inference and tracking
confirmation, and rule evaluation — and the *tracking confirmation* term is
frequently the largest, because a rule like "crossed the line and continued for N
frames" cannot fire before N frames have elapsed. At 5 fps and N = 10, that alone
is 2 seconds. *(Interpretation; no source decomposes surveillance alert latency.)*

**UNKNOWN** — What alert latency is operationally acceptable. Q-12 in
[domain-research.md](../domain/domain-research.md) §8 (response-time targets)
remains unanswered, and without it no latency budget can be set.

### 5.3 What actually has to cross the link

**CALCULATION.** Three candidate egress payloads, sized from stated inputs.

| Payload | Assumed size | Sustained rate | Time to send over 128 kbps | Over 512 kbps |
|---|---|---|---|---|
| Full 1080p H.264 stream | 4 Mbps | 4 Mbps | not possible | not possible |
| Per-frame object metadata, 5 objects/frame at 5 fps, ~64 B/record binary | 1.6 KB/s | **≈ 13 kbps** | continuous | continuous |
| Same as JSON, ~150 B/record | 3.75 KB/s | **≈ 30 kbps** | continuous | continuous |
| One 15 s event clip, 1080p @ 4 Mbps | 7.5 MB | — | **≈ 7.8 min** | **≈ 2.0 min** |
| One full-frame JPEG snapshot (~250 KB) | 250 KB | — | ≈ 16 s | ≈ 4 s |
| One 320×320 object crop JPEG (~25 KB) | 25 KB | — | ≈ 1.6 s | ≈ 0.4 s |
| One discrete event record (~1 KB), 20/day | 20 KB/day | ≈ 0.002 kbps | ≈ 0.06 s | ≈ 0.02 s |

**Three conclusions follow directly, and they are arithmetic, not opinion:**

1. **Full video egress is off the table** at these link speeds. This matches the
   industry's convergence on process-locally-ship-metadata
   ([competitive-landscape.md](../competitors/competitive-landscape.md) §9, P2).
2. **A per-frame metadata firehose is not cheap.** At ~13–30 kbps per camera it is
   comparable to Verkada's entire published 20 kbps per-camera budget (ibid. §8.1),
   and eight cameras of it would saturate a 128 kbps link.
3. **A single event clip takes minutes**, and an object crop takes under two
   seconds. **The choice of what an alert carries — a clip, a snapshot, or a crop
   — is a bandwidth decision by a factor of 300**, and it determines whether an
   operator can see what fired the alarm before the QRT has to move.

**ASSUMPTION** — The right default is therefore **event records plus small crops
in real time, with the full clip fetched on demand** if and when someone asks for
it. *(This is an interpretation of the arithmetic above and of Calipsa's ~300 kb
per event and Verkada's 20 kbps figures in
[competitive-landscape.md](../competitors/competitive-landscape.md) §8.1. It is
not a design decision and must not be treated as one.)*

### 5.4 Intermittent connectivity and disconnected operation

**FACT** — Peer-reviewed systems research finds per-camera uplink allocations in
constrained deployments can be "a few hundred kilobits per second or less",
conflicting with streaming all video centrally
([domain-research.md](../domain/domain-research.md) §6.2, `[T17]`).

**FACT** — Milestone supports offline licence activation and adding or replacing
devices without reactivation in offline systems, **in every edition**; Irisity
lists air-gapped on-premise deployment; Genetec Cloudlink is positioned partly on
maintaining local operation during connectivity disruptions; Frigate performs all
processing locally with no cloud subscription
([competitive-landscape.md](../competitors/competitive-landscape.md) §8.3).

**FACT** — Verkada documents an air-gapped *camera network* topology, but the
platform itself still requires the cloud (ibid.).

**FACT — recorded as the competitive survey's single most important unknown** —
Whether Genetec, BriefCam, Videonetics, AllGoVision or Ipsotek support **fully
disconnected operation including licence validation, model updates and time
synchronisation** is not documented anywhere retrieved (ibid.).

**ASSUMPTION** — Disconnected operation is not one feature but four independent
ones, and a product can have some and not others: (a) analytics continue running,
(b) events queue and reconcile on reconnect without duplication or loss, (c)
licensing does not expire, (d) time stays trustworthy. *(Interpretation of the
above; no source enumerates them.)*

**HYPOTHESIS** — Store-and-forward with **idempotent, monotonically identified
events** and bounded local queues is the correct shape, with a defined discard
policy for when the queue fills — because at a site that is offline for days, the
queue *will* fill. `[T7]` (ONVIF Profile G, recording search and replay) is one
existing standard for the retrieval half of this. Untested here.

**UNKNOWN** — The actual connectivity profile of a target site: whether an IP link
exists at all, its bandwidth, symmetry, metering, reliability, and whether it is
shared with voice
([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.3, Q-8 in
[domain-research.md](../domain/domain-research.md) §8). **This is the single most
consequential unknown in this document**, because it determines which of the rows
in [§5.3](#53-what-actually-has-to-cross-the-link) are even available.

---

## 6. Storage

### 6.1 Continuous video

**CALCULATION.** Storage for continuous recording, from stated bitrates:

| Stream | Per hour | Per day | Per camera, 30 days | 8 cameras, 30 days |
|---|---|---|---|---|
| 1080p H.264 @ 4 Mbps | 1.8 GB | 43.2 GB | 1.30 TB | 10.4 TB |
| 1080p H.265 @ 2 Mbps | 0.9 GB | 21.6 GB | 0.65 TB | 5.2 TB |
| Rig configuration @ 2.048 Mbps `[T38]` | 0.92 GB | 22.1 GB | 0.66 TB | 5.3 TB (5 live channels: 3.3 TB) |

**FACT** — Halving the bitrate with H.265 halves storage as well as bandwidth
([domain-research.md](../domain/domain-research.md) §6.2), and Zipstream-class
encoding claims a further ~50% `[T29]`.

**ASSUMPTION** — Continuous recording at a remote site is a **disk-endurance and
physical-maintenance problem** before it is a capacity problem. Surveillance
workloads are sustained sequential writes 24/7; a failed drive at a site with no
road access is not a warranty event, it is an expedition. *(Basis: Verkada's
documented experience that a failed drive means a shipped replacement and a
physical swap
([competitive-landscape.md](../competitors/competitive-landscape.md) §8.5)
combined with the 42% no-road-access finding
([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.1).)*

**UNKNOWN** — Whether IBVAP would own recording at all. The market forks cleanly:
Genetec, Milestone, Verkada, Eagle Eye, Gorilla and Frigate own recording;
BriefCam, Calipsa, AllGoVision and Ipsotek do not
([competitive-landscape.md](../competitors/competitive-landscape.md) §5.3). Owning
it is the heavier commitment but is what makes evidence management and offline
operation tractable (ibid.). This is an architecture decision and is not made here.

### 6.2 Event clips

**CALCULATION** — A 15-second 1080p clip at 4 Mbps is **7.5 MB**. At 20 events per
camera per day across 8 cameras that is 1.2 GB/day, or **36 GB/month** — trivial
against the 10.4 TB of continuous recording, and roughly 300× smaller.

**ASSUMPTION** — Clip extraction from a long-GOP stream can only be
frame-accurate at I-frame boundaries without re-encoding. Either the clip starts
at a keyframe (so its start time is imprecise by up to one GOP) or it is
re-encoded (which costs an encode session `[T10]`, or one to two CPU cores on
hardware with no encoder `[T12]`, and breaks any hash computed over the original
bitstream). *(This follows from GOP structure; no retrieved source states it as a
design constraint, which is itself notable.)*

**HYPOTHESIS** — Storing the original bitstream and cutting on keyframe boundaries
— accepting sub-second imprecision at the clip start — preserves both compute and
evidential integrity, and is preferable to re-encoding. Must be tested against
whatever the evidentiary requirement actually turns out to be.

### 6.3 Snapshots

**CALCULATION** — A full-frame 1080p JPEG is ~250 KB; a 320×320 object crop is
~25 KB. At 20 events/day/camera across 8 cameras, full-frame snapshots are 40
MB/day and crops are 4 MB/day. **Both are negligible in storage and decisive in
bandwidth** ([§5.3](#53-what-actually-has-to-cross-the-link)).

**FACT** — The best-shot-image pattern is already industry practice: i-PRO's Active
Guard consumes "metadata information from i-PRO Edge AI cameras" and **best-shot
images** rather than raw video
([competitive-landscape.md](../competitors/competitive-landscape.md) §6.1).

### 6.4 Metadata

**CALCULATION** — Per-frame object metadata at ~13 kbps
([§5.3](#53-what-actually-has-to-cross-the-link)) is **138 MB per camera per day**,
or 4.1 GB/month; 8 cameras is 33 GB/month. Discrete event records at 20/day are
20 KB/day per camera — six orders of magnitude smaller.

**ASSUMPTION** — Metadata storage is where the searchable product lives and is
therefore worth its cost, but the retention policy for per-frame metadata should be
set independently of the retention policy for video and for events. Three
different questions. *(Interpretation.)*

**FACT** — ONVIF Profile M already defines the metadata schema for vehicle, licence
plate, human face and human body, plus geolocation `[T6]` — i.e. there is an
existing vendor-neutral vocabulary to store against.

### 6.5 Evidentiary integrity

**[MARKET:IN] FACT** — Electronic records in India, including CCTV footage, are
governed by **Section 63 of the Bharatiya Sakshya Adhiniyam, 2023**, in force from
**1 July 2024**. Admissibility of a copy requires a certificate signed by the
person in charge of the device **and** an expert, and the certificate must disclose
the record's **hash value**
([domain-research.md](../domain/domain-research.md) §3.5;
[ssb-operational-context.md](../domain/ssb-operational-context.md) §11.5).

**FACT** — C2PA, the content-provenance standard, is built on SHA-256 hashes,
X.509 certificates and digital signatures; content is hashed and the hash included
in a signed manifest, so any pixel-level change invalidates it, and modifications
add manifests without deleting previous ones — producing a chain of custody rather
than a single seal. `[T34]`

**HYPOTHESIS** — Hashing the **stored bitstream at the moment of capture** (rather
than an exported copy at the moment of request) is the only way to make a Section
63 certificate cheap, because it decouples the hash from the export. This is
testable and it interacts directly with the no-transcode hypothesis in
[§1.3](#13-codecs): a re-encoded clip has a different hash from the recording it
came from.

**ASSUMPTION** — Section 63 lands harder on this deployment than on a commercial
one because the device custodian at the point of capture is a Sub-Inspector or
Head Constable, and 42% of sites have no road access — so getting either the
custodian's or an expert's signature to a site is a journey
([ssb-operational-context.md](../domain/ssb-operational-context.md) §11.5).

**FACT** — In the market, evidentiary features are **priced, not standard**:
Milestone gates media-database encryption and digital signing to its upper
editions and Evidence Lock to Corporate only; Genetec's encryption costs 30% of
Archiver capacity for the first certificate
([competitive-landscape.md](../competitors/competitive-landscape.md) §10, G10).
**The cheapest deployments — which is what a remote site gets — are the ones
without signing, locking or tamper-evidence.**

**UNKNOWN — and it blocks any evidential design** — **Time synchronisation at a
disconnected site.** A hash and a timestamp are only as good as the clock. Nothing
in any research pass establishes whether target sites have NTP, GNSS time, or
anything at all. A site that reboots with a wrong clock produces evidence with a
wrong time, and the failure is silent.

### 6.6 Retention

**UNKNOWN** — Retention periods mandated or practised at the target sites. Q-9 in
[domain-research.md](../domain/domain-research.md) §8 and the corresponding gap in
[ssb-operational-context.md](../domain/ssb-operational-context.md) §11.5; both
unanswered. Without it, [§6.1](#61-continuous-video)'s table cannot be turned into
a disk order.

**ASSUMPTION** — Retention will differ by artefact class — continuous video
shortest, event clips longer, event metadata longest, and anything attached to an
open case indefinitely. *(Interpretation; supported by the existence of Evidence
Lock as a distinct product feature
([competitive-landscape.md](../competitors/competitive-landscape.md) §10, G10).)*

---

## 7. Integration

### 7.1 The shape of the problem

**FACT** — Ingest has standardised on RTSP + ONVIF Profile S; **egress has not**.
Every vendor emits events differently: MIP plugins, REST, WebSocket, webhooks,
MQTT, ONVIF virtual camera, VMS bookmarks
([competitive-landscape.md](../competitors/competitive-landscape.md) §7.1).

**FACT** — Two existing patterns stand out as low-friction: **AllGoVision's ONVIF
virtual camera** (present analytics output as an ONVIF camera, so any ONVIF VMS
ingests it with no plugin) and **Milestone AI Bridge** (a documented Docker
container contract into the largest open VMS) (ibid.).

### 7.2 Standards that already exist for this

**FACT** — **ONVIF Profile M** defines analytics metadata, object classification,
metadata definitions for vehicle/licence plate/face/body/geolocation, event
interfaces for object counters and for face and plate recognition, rule
configuration, and delivery via metadata stream, ONVIF event service **or MQTT**.
`[T6]`

**FACT** — **STANAG 4609** is NATO's digital motion imagery standard, the format
"produced by most coalition full-motion video sensors and ground stations", giving
common methods for exchanging motion imagery with metadata across systems and
nations. KLV encoding follows SMPTE ST 336. `[T32]`

**FACT** — **MISB ST 0903 (VMTI — Video Moving Target Indicator)** defines how to
encode metadata about **objects detected in video**: number of targets per frame,
target position in the frame (pixel coordinates or bounding box), target geographic
location, **target track ID and history**, and confidence — structured as a VMTI
Local Data Set containing a VTargetSeries of VTarget Packs. It is the standard used
"when video analytics identify moving targets or tracks". `[T33]`

**MISB ST 0903 is, almost exactly, a defence-standard schema for the output of the
pipeline in [§2](#2-video-pipeline).** No vendor in the competitive survey was
found emitting it. Whether it is the right egress for this deployment is an
architecture question; that it exists, and that it is the format a NATO-compatible
C2 system already ingests `[T32]`, is a fact the architecture stage should not
have to rediscover.

**ASSUMPTION** — There are therefore three plausible egress vocabularies rather
than none: **ONVIF Profile M** (surveillance-industry native, MQTT-capable),
**MISB ST 0903 / STANAG 4609** (defence C2 native), and **an ad-hoc JSON event over
webhook/MQTT** (universal, unstandardised). They serve different consumers and are
not mutually exclusive. *(Interpretation of `[T6][T32][T33]` against
[competitive-landscape.md](../competitors/competitive-landscape.md) §7.1.)*

### 7.3 What the target C2 actually is

**UNKNOWN — blocking, and unchanged by this pass** — The problem statement requires
integration with "existing command and control systems". No source in any research
pass names such a system for the validation force, with a vendor, protocol, data
model or network reach. The only credible candidate found is **SIMS**, a seizure
register that records **outcomes, not detections**
([ssb-operational-context.md](../domain/ssb-operational-context.md) §9, §14.10).
For the BSF context, a Command and Control Centre is architecturally central to
CIBMS but is not named or specified
([domain-research.md](../domain/domain-research.md) §3.6).

**ASSUMPTION** — Until that is answered, the only defensible integration posture is
to **emit into a documented, standard vocabulary and let an adapter be written per
consumer** — because the consumer is unknown, may be several, and includes at least
one organisation (state police) that did not produce the data
([domain-research.md](../domain/domain-research.md) §3.5). *(Interpretation.)*

**UNKNOWN** — Whether the network where cameras sit can reach the network where any
C2 system sits at all, and under what security policy. Q-18 in
[domain-research.md](../domain/domain-research.md) §8; unanswered.

### 7.4 APIs the platform itself would need to expose

**ASSUMPTION** — Independent of the C2 question, a video analytics platform has at
least five distinct interfaces, and conflating them is a common design error:
(1) live event stream, (2) historical event/metadata query, (3) video retrieval and
clip export, (4) configuration and health, (5) enrolment/watchlist management where
recognition is in scope. `[T6]` and `[T7]` cover roughly (1), (2) and (3) between
them. *(Interpretation; the split is visible in the market survey's integration
table
([competitive-landscape.md](../competitors/competitive-landscape.md) §7) but no
source enumerates it.)*

---

## 8. Deployment

### 8.1 Remote sites

**FACT** — 42% of BOPs on the validation border (308 of 734) lack road connectivity
([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.1); border
observation posts are reported to lack basic electricity
([domain-research.md](../domain/domain-research.md) §1.2); generators are provided
where there is no grid connection and the situation varies state to state
([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.2).

**FACT** — The echelons nearest the camera are commanded by a **Sub-Inspector**
(BOP) and a **Head Constable** (check post) (ibid. §3.2), and lack of technical
expertise for equipment operation and maintenance is a documented deficiency
([domain-research.md](../domain/domain-research.md) §4.3).

**FACT** — The real deployment unit in this industry is **a site survey by a
trained integrator**, not an installer running a wizard; Genetec and Milestone both
run partner certification programmes and Genetec ships a camera requirements
calculator whose stated purpose includes verifying whether existing cameras "need
to be modified"
([competitive-landscape.md](../competitors/competitive-landscape.md) §9, P7).

**ASSUMPTION** — Software placed at such a site must run unattended for long
periods and **must fail in a way a Sub-Inspector can recognise and report over a
radio or satellite phone**
([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.5). That is
a technical requirement on the health and diagnostics design, not a UX nicety, and
it is unusual: most of this market assumes a control room and an operator role
hierarchy ([competitive-landscape.md](../competitors/competitive-landscape.md) §10,
G7).

**HYPOTHESIS** — Automated capability assessment — the platform measuring, per
camera, what pixel density and frame rate it is actually getting and therefore
which analytics it can honestly support — is the technical substitute for a site
survey that this deployment shape requires. The competitive research identifies
this as an unfilled gap (ibid. §10, G5 and G6) and the i-LIDS primary/secondary
framing gives it a vocabulary
([domain-research.md](../domain/domain-research.md) §6.7). **It is technically
straightforward to measure pixel density given a known reference; the hard part is
knowing the scene geometry.** Untested.

### 8.2 Centralised command centre

**FACT** — A Command and Control Centre where sensor data is aggregated into a
composite picture is architecturally central to CIBMS
([domain-research.md](../domain/domain-research.md) §1.3), and centralised
decision-making is separately flagged as a risk of delaying urgent field responses
(ibid. §3.6).

**FACT** — **No SSB control room, monitoring roster or video wall is documented
anywhere** in the domain research; whether the validation force watches live video
at all is genuinely unknown
([ssb-operational-context.md](../domain/ssb-operational-context.md) §7, §14.7).

**ASSUMPTION** — A centralised deployment tier cannot be assumed to have a human
watching it. Its technical purpose may be aggregation, search and reporting rather
than live monitoring. *(Interpretation of the above; this materially changes
latency requirements and is a product question.)*

### 8.3 Hybrid deployment

**FACT** — Hub-and-site with local processing and central metadata is settled
industry practice
([competitive-landscape.md](../competitors/competitive-landscape.md) §5.2), and
Milestone offers two distinct multi-site forms (Federated Architecture and
Interconnect) with different edition requirements (ibid.).

**FACT** — Containerised Linux is the emerging norm for the analytics layer even
where the VMS layer is Windows: Frigate ships as Docker containers and Milestone AI
Bridge expects third-party analytics "deployed as docker containers" (ibid. §5.4).

**FACT** — The two most GPU-dependent products in the competitive survey — Genetec
KiwiVision and BriefCam — **both advise against virtualisation** (ibid. §5.5).

**ASSUMPTION** — A hybrid design has to answer three questions the single-tier
designs do not: what happens to events generated while the site is disconnected
([§5.4](#54-intermittent-connectivity-and-disconnected-operation)), how models and
configuration reach a site over a link that may be metered
([§8.4](#84-updates-and-maintenance)), and which tier is authoritative for time
([§6.5](#65-evidentiary-integrity)). *(Interpretation.)*

### 8.4 Updates and maintenance

**FACT** — Verkada documents that during a Command Connector firmware update "the
cameras connected to Command Connector will not record footage", that customers
cannot install their own drives, and that it provides no security patches or
firmware updates for non-Verkada cameras
([competitive-landscape.md](../competitors/competitive-landscape.md) §8.5).

**CALCULATION** — A 100 MB model or container update over a 128 kbps link takes
**≈ 1 hour 44 minutes**; over 512 kbps, **≈ 26 minutes**. A 1 GB image takes
**≈ 17 hours** at 128 kbps. Update size is a deployment constraint, not a build
detail.

**HYPOTHESIS** — Delta/differential updates and resumable transfer are not
optimisations at these link speeds; they are the difference between an update
being possible and not. Untested, and no source retrieved addresses OTA update
sizing for video analytics platforms.

**FACT** — Equipment maintenance is identified as critical for the domain, with
specialised technical training and spare-parts availability both undefined
challenges, and high reliance on external vendors with minimal oversight
([domain-research.md](../domain/domain-research.md) §6.4).

---

## 9. Hard physical limitations software cannot solve

Each of these is a constraint of optics, physics, or information theory. They bound
IBVAP exactly as they bound every competitor, and no model, no training data and no
amount of engineering removes them.

**L1 — Pixels on target.** DORI/OODPCVS is physics `[T8][T9]`. Detection needs
~25 px/m; identification needed 250 px/m under the 2015 standard and, per `[T9]`,
**500 px/m under the 2025 revision**. A camera installed to see that *someone* is
there cannot be made to show *who*. Software can only interpolate, and
interpolation manufactures no information.

**L2 — The camera's field of view.** A face that never enters the frame, or enters
it only as the top of a head, cannot be recognised. NIST's own conclusion is that
video face recognition can approach still-photo accuracy "only if image collection
can be improved" — camera positioning, mounting, lighting and optics `[T23b]`. All
four are hardware.

**L3 — Photons at night.** A visible-light sensor with insufficient illumination
produces noise, not signal. The measured cost is a **33.9% relative drop** in
detection mAP on night data versus the infrared view of the same scenes `[T26]`.
Denoising and enhancement trade noise for blur; they do not add photons.

**L4 — Atmospheric attenuation.** Line-of-sight equipment is degraded by heavy
rain, storms and dense fog
([domain-research.md](../domain/domain-research.md) §1.2), and **thermal is not
exempt** — scattering in water droplets attenuates the infrared signal, with higher
droplet density causing more attenuation (ibid. §6.3).

**L5 — Motion blur.** Blur is set by exposure time and target velocity at the
sensor. It is why dedicated ANPR cameras use fast or global shutters `[T25b]`, and
it is why software ANPR is speed-limited (Genetec Flexreader: 50 km/h)
([competitive-landscape.md](../competitors/competitive-landscape.md) §6.2). A
blurred plate has lost the information; deblurring hallucinates it.

**L6 — Viewing angle.** Milestone's software LPR requires the camera to look down
on the vehicle at no more than **30 degrees** (ibid.); Avigilon's LPR cannot use
panoramic, 360, fisheye or PTZ cameras at all (ibid. §6.1). Geometry, not
algorithm.

**L7 — Temporal sampling.** Below ~2–3 analysed fps, identity association collapses
(AssA 43.6% → 27.8% between 3 and 1 fps) `[T22]`. You cannot track what you did not
observe between two positions.

**L8 — Codec information loss.** A frame that was encoded at 2 Mbps 1080N and then
upscaled contains the information of 960×1080 at 2 Mbps, whatever its stated
dimensions `[T31][T38]`. Compression artefacts are indistinguishable from scene
content to a downstream model.

**L9 — The recorder's shared budget.** Where a DVR/XVR fronts the cameras, its
total bitrate and frame-rate budget is fixed and shared across channels
`[T38]`. No software downstream can raise it, and asking one channel for more takes
it from another.

**L10 — Occlusion.** An object behind another object is not in the image. Occlusion
is the documented dominant failure mode of multi-object tracking `[T21]`.

**L11 — The link.** A 128 kbps uplink carries 128 kilobits per second. A 15-second
1080p clip takes ~7.8 minutes ([§5.3](#53-what-actually-has-to-cross-the-link)),
and no compression scheme changes the order of magnitude.

**L12 — Energy.** Inference costs joules. Hailo-8 at 2.5 W and Orin Nano at 7–25 W
`[T15][T11]` are the floor for their respective capability classes, and at a
fuel-limited site that floor is a logistics fact.

---

## 10. Camera-quality limitations

Distinct from [§9](#9-hard-physical-limitations-software-cannot-solve): these are
properties of *the cameras that happen to be installed*, which a different
procurement could have avoided, but which IBVAP by definition inherits.

| Limitation | Why it matters | Evidence |
|---|---|---|
| Specified for Detection/Observation density (25–62 px/m), not Identification | Face recognition and ANPR are out of reach on such cameras regardless of software | `[T8]`, [competitive-landscape.md](../competitors/competitive-landscape.md) §6.3 |
| 1080N / "1080 lite" anamorphic encoding | Halves horizontal pixel density while advertising "1080" | `[T31][T38]` |
| Wide-angle overview mounting | Maximises coverage, minimises px/m; looks down on heads not faces | `[T23b]` |
| No true day/night sensor or IR illuminator | Night performance falls to the L3 limit | [domain-research.md](../domain/domain-research.md) §6.3 |
| IR illumination is monochrome | Removes colour as a feature for re-ID, description, vehicle colour | [§3.10](#310-night-and-low-light-analytics) (assumption) |
| Fixed cameras with no overlap | Cross-camera tracking has no geometric constraint to exploit | `[T37]` |
| PTZ on preset tour | Stable-background analytics invalid while moving | `[T36]` |
| Shared DVR encoder budget | Frame rate and bitrate are not per-camera choices | `[T38]` |
| Unknown/undocumented ONVIF conformance and firmware | Compatibility must be established per model | `[T4]`, [competitive-landscape.md](../competitors/competitive-landscape.md) §6.4 |
| Lens condition — dirt, spider webs, condensation, IR hotspot | Silent, gradual degradation that looks like scene change | assumption; no source retrieved quantifies it |
| Clock drift on the camera or recorder | Breaks correlation and evidential timestamps | [§6.5](#65-evidentiary-integrity) (unknown) |

**ASSUMPTION** — The single most useful thing a platform could do about all of the
above is **measure and report it per camera** rather than fail silently — which is
the unfilled gap the competitive research identifies
([competitive-landscape.md](../competitors/competitive-landscape.md) §10, G5/G6).
*(Interpretation, not a requirement.)*

---

## 11. What is realistically achievable, and what is not

**This table is a research judgement, not a product scope.** It states expected
feasibility **on existing, non-purpose-mounted CCTV** in this deployment context.
Every row would move if the camera were re-aimed or replaced — which the problem
statement forbids.

| Capability (as named in the problem statement) | On a purpose-aimed camera (check post, lane, gate) | On a general-purpose existing camera | Binding limit |
|---|---|---|---|
| **Human detection** | High | **Moderate–High** | L1 pixels, L3 night |
| **Human tracking (single camera)** | High | **Moderate** | L7 frame rate, L10 occlusion |
| **Human tracking (cross-camera)** | Low | **Low** | `[T37]` domain gap, L6 geometry |
| **Vehicle detection** | High | **Moderate–High** | L1, L3 |
| **Vehicle classification (coarse type)** | High | **Moderate** | L1, L6 |
| **Vehicle attributes (make/model/colour)** | Moderate | **Low** | L1, L3 (colour gone at night) |
| **Face detection** | High | **Low–Moderate** | L2 mounting, L1 |
| **Face recognition** | Moderate | **Low** | L1, L2, `[T23b]`; plus legal, §3.5 |
| **ANPR** | **Moderate–High** | **Low** | L1 (250 px/m), L5 blur, L6 angle |
| **General OCR** | Moderate | **Low** | as ANPR, without the compensations |
| **Virtual fence / line crossing (mechanism)** | High | **High** | — |
| **Virtual fence at an acceptable nuisance rate** | Moderate | **Unproven** | L4 weather, environment (§3.8) |
| **Loitering / dwell** | Moderate | **Moderate** | L7 frame rate, L10 occlusion |
| **"Suspicious activity" (learned)** | Low | **Low** | `[T27]` scene overfitting, FAR, undefined ground truth |
| **"Suspicious activity" (explicit composite rules)** | Moderate | **Moderate** | quality of the primitives it composes |
| **Night-time movement detection (visible camera)** | Moderate | **Low–Moderate** | L3, `[T26]` |
| **Night-time movement detection (thermal camera)** | High | **n/a — few thermal cameras installed** | availability, not capability |
| **Real-time alert generation** | High | **High** | L11 link (what the alert can carry) |
| **Event logging** | High | **High** | storage and time integrity (§6.5) |

**The pattern in the right-hand column is the finding.** The capabilities that
survive on a general-purpose existing camera are the ones that need only *presence
and motion of a large object*. Every capability that needs *identity* — face
recognition, ANPR, cross-camera tracking, fine vehicle attributes — degrades to Low,
because identity needs pixel density that overview cameras were never specified to
deliver.

**The problem statement asks for both halves. Only one half is comfortably
reachable without touching the hardware.** How to respond to that is a product
decision and belongs in `docs/02-product/`.

---

## 12. Major technical risks

Expanded in the ranked list at [§15](#15-the-10-biggest-technical-risks). Recorded
here as categories with their evidence:

- **Camera-estate risk** — the installed base may not support the named
  capabilities at all, and this is unknown ([§10](#10-camera-quality-limitations),
  Q-1).
- **Nuisance-alarm risk** — 90% false alarms is the documented precedent
  ([§3.8](#38-virtual-fence--line-crossing)), and an untrusted system is worse than
  none ([domain-research.md](../domain/domain-research.md) §4.2).
- **Night-inversion risk** — the worst-performing condition carries the highest
  operational weight ([§3.10](#310-night-and-low-light-analytics)).
- **Bandwidth risk** — the link may not carry even the metadata
  ([§5.3](#53-what-actually-has-to-cross-the-link)).
- **Power and logistics risk** — continuous compute at a fuel-limited, unroaded
  site ([§4.6](#46-power)).
- **Compatibility risk** — unbounded per-model work
  ([§1.8](#18-camera-compatibility--the-state-of-the-art)).
- **Evidential risk** — clocks, hashes and transcode
  ([§6.5](#65-evidentiary-integrity)).
- **Integration risk** — the C2 target is unnamed
  ([§7.3](#73-what-the-target-c2-actually-is)).
- **Legal/regulatory risk** — biometrics on an open border, EU prohibition, ER-01
  churn in the Indian camera base
  ([§3.5](#35-face-recognition);
  [competitive-landscape.md](../competitors/competitive-landscape.md) §3.5, §9 P9).
- **Licensing risk** — AGPL-3.0 model licences against a cost-effectiveness
  requirement ([§2.5](#25-inference)).

---

## 13. Unknowns that must be validated experimentally

Distinct from the domain and competitor unknowns, which are questions for people.
These are questions for a test rig — and several can be answered on the hardware
already in this repository.

| # | Unknown | Why it blocks | Where it can be tested |
|---|---|---|---|
| E-1 | Actual pixel density on target for real border camera geometry | Determines which rows of [§11](#11-what-is-realistically-achievable-and-what-is-not) are reachable | Any site, with a tape measure and a target |
| E-2 | CPU-only inference and decode throughput per camera | Decides whether an accelerator is mandatory | The rig in this repo |
| E-3 | Whether the H.264/H.265 stream-count gap `[T13]` reproduces | Changes sizing by up to 2.5× | The rig + any Jetson |
| E-4 | Whether compressed-domain motion-vector filtering works on border-type scenes | The central power/bandwidth lever ([§2.3](#23-frame-sampling)) | Recorded night and windy-day footage |
| E-5 | Real nuisance-alarm rate of an object-gated virtual fence over 24 h of real footage | The product's credibility ([§3.8](#38-virtual-fence--line-crossing)) | The rig, unattended, for a week |
| E-6 | Detection and tracking performance on IR-illuminated night footage from an ordinary camera | The night-inversion risk ([§3.10](#310-night-and-low-light-analytics)) | The rig, after dark |
| E-7 | Whether tracking holds at 5 fps, 3 fps and 1 fps on real footage | Sets the analysis-rate floor for this estate | The rig, resampled |
| E-8 | Whether a 1080N stream can support any identity-grade analytic at any range | The anamorphic trap ([§1.6](#16-resolution)) | The rig, directly |
| E-9 | End-to-end alert latency decomposition | No latency budget exists ([§5.2](#52-latency)) | The rig |
| E-10 | Energy per analysed frame, per accelerator | Power is undocumented industry-wide ([§4.6](#46-power)) | Any device plus an inline power meter |
| E-11 | Behaviour of the whole pipeline across a simulated multi-day disconnection | Store-and-forward correctness ([§5.4](#54-intermittent-connectivity-and-disconnected-operation)) | The rig, with the link pulled |
| E-12 | Whether concurrent RTSP clients degrade an existing recorder's own recording | Deployment safety on a live estate | The rig |

---

## 14. The 10 most important technical findings

Ordered by how much each should change what happens next.

1. **The problem statement's premise survives for software and fails for pixels.**
   Every named capability ships as software on third-party cameras today
   ([competitive-landscape.md](../competitors/competitive-landscape.md) §4), but the
   capabilities that need *identity* — face recognition, ANPR, cross-camera tracking
   — need pixel densities (250 px/m in 2015, per `[T9]` **500 px/m in the 2025
   standard**) that cameras installed for human overview were never specified to
   deliver `[T8][T9]`. The constraint moved from silicon to optics; it did not
   disappear. ([§9](#9-hard-physical-limitations-software-cannot-solve) L1,
   [§11](#11-what-is-realistically-achievable-and-what-is-not))

2. **NIST's own conclusion contradicts the deployment model.** Video face
   recognition "may approach that of still-photo face recognition, **but only if
   image collection can be improved**" — camera positioning, mounting, lighting and
   optics `[T23b]`. Improving image collection is precisely what a
   software-on-existing-cameras platform cannot do. Identification rates in FIVE
   ranged from ~60% to >99% purely on image quality. ([§3.5](#35-face-recognition))

3. **Decode, not inference, is the binding compute constraint — and you cannot
   escape it by analysing fewer frames.** P-frames depend on their predecessors, so
   arbitrary frame sampling requires full decode anyway; only I-frame-only decoding
   is cheap, and on the rig's 1-second GOP that yields 1 fps `[T38]` — below the
   ~3 fps tracking floor `[T22]`. NVIDIA's own figures show Orin Nano running
   PeopleNet at 256 fps while sustaining only **8** full-pipeline 1080p30 H.264
   streams `[T13]`. ([§2.2](#22-decoding), [§4.3](#43-approximate-resource-requirements--a-worked-estimate))

4. **H.264 — the codec an existing estate is most likely to have — costs up to
   2.5× more stream capacity than H.265 on the same silicon.** AGX Orin: 37 streams
   H.265 vs 15 H.264 `[T13]`. IBVAP inherits the expensive half of that table.
   ([§2.2](#22-decoding))

5. **The recorder in front of the camera can be a harder limit than the camera.**
   Measured on this repository's own hardware: fixed 1080N (960×1080, half the
   horizontal pixels of 1080p), a **shared budget of 12,288 kbps and 120 fps across
   8 channels**, 25 fps on one channel only, and firmware that returns OK for
   settings it silently discards `[T38][T31]`. No downstream software raises any of
   those. ([§1.6](#16-resolution), [§1.7](#17-the-recorder-in-front-of-the-camera-is-a-hard-limit))

6. **"Suspicious activity detection" is the weakest capability named, and the
   weakness is measurable.** Models reporting 94.55% AUC collapse to **16.35%** on
   same-scene reversed-label evaluation — much of the reported performance is scene
   memorisation. False-alarm rates rise **42% on average** on hard-normal
   benchmarks, some exceeding **70% FAR**. Human annotators agree only at Fleiss'
   Kappa 0.51–0.68 — the ground truth itself is contested. And AUC is insensitive to
   *when* a detection occurs, which is the entire operational point `[T27]`.
   ([§3.9](#39-loitering-dwell-and-suspicious-activity))

7. **Night is the operational peak and the technical trough.** Visible-light
   detection scores mAP 0.430 against 0.651 for infrared on the same night scenes —
   a 33.9% relative drop `[T26]` — while the domain research records that
   infiltration and smuggling concentrate in darkness
   ([domain-research.md](../domain/domain-research.md) §5.6). "Night-time movement
   detection" is not a feature anywhere in the market; it is an operating condition
   ([competitive-landscape.md](../competitors/competitive-landscape.md) §4.1).
   ([§3.10](#310-night-and-low-light-analytics))

8. **What an alert carries is a bandwidth decision worth a factor of ~300.** A
   15-second 1080p clip is 7.5 MB and takes **7.8 minutes** on a 128 kbps link; a
   320×320 object crop is 25 KB and takes **1.6 seconds**. A per-frame metadata
   firehose at 13–30 kbps per camera is comparable to Verkada's *entire* published
   per-camera budget. ([§5.3](#53-what-actually-has-to-cross-the-link))

9. **Standard, vendor-neutral vocabularies for analytics egress already exist, and
   the market is not using them.** **ONVIF Profile M** defines metadata for vehicle,
   licence plate, face, body and geolocation, plus delivery over MQTT `[T6]`; **MISB
   ST 0903 (VMTI)** defines per-frame detections with bounding boxes, geolocation,
   **track IDs** and confidence, inside **STANAG 4609**, which NATO-compatible C2
   systems already ingest `[T32][T33]`. No vendor in the competitive survey was
   found emitting either. ([§7.2](#72-standards-that-already-exist-for-this))

10. **A single measured, real recorder was enough to falsify three convenient
    assumptions.** UDP is unusable and TCP is mandatory; "1080" can mean 960
    horizontal pixels; and a device will report success for configuration it
    discards `[T38]`. This is one device — but it argues strongly that the estate
    survey (Q-1) must be *measured*, not *specified*.
    ([§1](#1-camera-and-video-interfaces))

---

## 15. The 10 biggest technical risks

Ordered by expected impact × likelihood, given what is currently known.

1. **The installed camera estate cannot physically support the named identity
   capabilities, and nobody has measured it.** If existing cameras deliver 25–62
   px/m, ANPR and face recognition are unreachable on them at any software quality
   `[T8][T9]`. *Likelihood: high — the estate is unknown (Q-1) and cameras installed
   for human monitoring are specified for Detection/Observation
   ([competitive-landscape.md](../competitors/competitive-landscape.md) §6.3).*
   **Mitigation direction: measure before promising — E-1.**

2. **Nuisance alarms make the system untrusted, which is worse than no system.**
   SBInet's precedent is 90% false alarms
   ([domain-research.md](../domain/domain-research.md) §4.2); the peer-reviewed
   finding is that system accuracy drives operator reliance (ibid. §4.1); and the
   documented environmental triggers — wind-moved vegetation, rain, fog, headlight
   glare, wildlife — are all present at these sites
   ([competitive-landscape.md](../competitors/competitive-landscape.md) §4.1).
   **E-5.**

3. **Night performance is inadequate exactly when it matters most.** `[T26]` plus
   [domain-research.md](../domain/domain-research.md) §5.6. Compounded by the
   unknown thermal/IR composition of the estate (Q-15). **E-6.**

4. **The uplink cannot carry what the design assumes.** If real uplinks are "a few
   hundred kilobits per second or less"
   ([domain-research.md](../domain/domain-research.md) §6.2), even continuous
   metadata is marginal and clips are impossible in real time
   ([§5.3](#53-what-actually-has-to-cross-the-link)). *Likelihood: high — Q-8 is
   unanswered and satellite is documented in the inventory
   ([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.3).*
   **E-11.**

5. **Power and physical maintenance at unroaded sites exceed the software's
   value.** Continuous compute is a fuel logistics cost at a generator-powered site
   with no road (ibid. §10.1, §10.2), and every appliance architecture imports a
   physical maintenance obligation
   ([competitive-landscape.md](../competitors/competitive-landscape.md) §8.5).
   **E-10.**

6. **Per-model compatibility work is unbounded and consumes the team.** Two of the
   best-resourced vendors in the market both built compatibility labs and still warn
   buyers (ibid. §6.4); the rig's own quirks — TCP-only, percent-encoded passwords,
   silent config discard, anamorphic frames — are three devices' worth of surprises
   from one device `[T38]`. **E-12.**

7. **"Suspicious activity" cannot be delivered as understood, and it is in the
   problem statement.** `[T27]` shows the benchmark numbers do not transfer; the
   domain research shows the term is undefined by anyone
   ([domain-research.md](../domain/domain-research.md) §5.7, Q-3). Risk is
   expectation, not engineering: the capability will be judged against an unstated
   standard. **Q-3 must be answered by a person, not an experiment.**

8. **Evidence produced is inadmissible or unusable.** Section 63 BSA requires a
   hash and two signatures
   ([domain-research.md](../domain/domain-research.md) §3.5); transcoding changes
   the hash ([§6.2](#62-event-clips)); clock integrity at a disconnected site is
   entirely unestablished ([§6.5](#65-evidentiary-integrity)); and the market prices
   signing and tamper-evidence as an upper-edition feature
   ([competitive-landscape.md](../competitors/competitive-landscape.md) §10, G10).
   *A silent wrong clock is the worst version of this risk.*

9. **Integration has no defined target.** "Existing command and control systems" is
   a requirement whose object is unnamed; the only credible candidate on the
   validation border records outcomes rather than detections
   ([ssb-operational-context.md](../domain/ssb-operational-context.md) §9, §14.10);
   and egress has not standardised in the market
   ([competitive-landscape.md](../competitors/competitive-landscape.md) §7.1). Risk
   of building an adapter for a system that does not exist, or missing one that
   does.

10. **Legal and licensing constraints invalidate a headline capability or the
    build.** Face recognition on a treaty-open border has an unresolved legal basis
    ([ssb-operational-context.md](../domain/ssb-operational-context.md) §11.6) and is
    prohibited by default for law enforcement in the EU
    ([competitive-landscape.md](../competitors/competitive-landscape.md) §9, P9);
    India's ER-01/STQC bars sale of non-conforming cameras from 1 April 2026, so the
    installed base will churn (ibid. §3.5); and the most convenient detector families
    are AGPL-3.0, requiring either full source release or a commercial licence
    `[T35]`.

---

## 16. Ten experiments and prototypes we should eventually run

Every one of these is designed to answer a specific unknown above, and the first
six need nothing this project does not already have. **None of these is scheduled
or scoped here** — the engineering stage decides that, per
[CLAUDE.md](../../../CLAUDE.md) §2.

1. **Camera capability audit.** Point a detector at each rig channel, place a
   person and a plate at measured distances, and record the actual px/m achieved per
   camera at each range. Output: a per-camera statement of which
   [§11](#11-what-is-realistically-achievable-and-what-is-not) rows are reachable.
   *Answers E-1, E-8; tests finding 1 and risk 1.*

2. **Baseline compute characterisation.** Measure decode-only, decode+detect, and
   decode+detect+track throughput and CPU/GPU utilisation on the rig, at 1, 3, 5, 10
   and 25 fps, with and without an accelerator. *Answers E-2, E-3, E-7.*

3. **Seven-day unattended nuisance-alarm run.** Run an object-gated virtual fence on
   all five live rig channels for a week. Count every alarm, classify each by cause
   (person, vehicle, animal, vegetation, insect, light change, rain, artefact).
   Output: a measured false-alarm rate and a cause histogram. *Answers E-5; tests
   risk 2. **This is the single most valuable experiment on the list**, because it
   produces the number the entire market declines to publish
   ([competitive-landscape.md](../competitors/competitive-landscape.md) §9, P10).*

4. **Night and IR characterisation.** Repeat experiments 1 and 3 after dark on
   IR-illuminated channels. Additionally measure: colour information loss, IR
   hotspot and insect artefacts, and detection recall against a known walked route.
   *Answers E-6; tests finding 7 and risk 3.*

5. **Compressed-domain pre-filter feasibility.** Extract H.264 motion vectors
   without full decode; measure what fraction of frames can be discarded at a fixed
   recall against the experiment-3 ground truth, on both quiet and windy/rainy
   footage. *Answers E-4; tests the central hypothesis of
   [§2.3](#23-frame-sampling).*

6. **Frame-rate floor determination.** Resample recorded footage to 25/10/5/3/1 fps
   and measure tracking identity persistence and rule-firing correctness at each.
   Output: the analysis-rate floor for *these* scenes, against `[T22]`'s general
   figure. *Answers E-7.*

7. **Disconnected-operation soak test.** Run the pipeline with the uplink physically
   removed for 72 hours; verify events queue, reconcile without duplication or loss,
   licences do not expire, clocks do not drift past tolerance, and the local queue's
   overflow policy behaves as intended. *Answers E-11; tests risk 4 and the
   competitive survey's own "most important unknown"
   ([competitive-landscape.md](../competitors/competitive-landscape.md) §8.3).*

8. **Bandwidth-shaped egress trial.** Shape the uplink to 128 kbps, 512 kbps and
   2 Mbps and measure, for each, end-to-end time from event to operator-visible
   evidence for three payload designs (event only, event + crop, event + clip).
   *Answers E-9; tests finding 8.*

9. **Energy-per-frame measurement.** Inline power meter on the analytics node
   through experiments 2 and 5; report joules per analysed frame and per detected
   event, idle and loaded. *Answers E-10; produces a figure no vendor in the market
   publishes ([competitive-landscape.md](../competitors/competitive-landscape.md)
   §8.4).*

10. **Egress interoperability spike.** Emit the same event set as (a) ONVIF Profile
    M metadata over MQTT, (b) MISB ST 0903 VMTI KLV, and (c) plain JSON webhook, and
    attempt ingestion by at least one third-party consumer of each. *Tests finding 9
    and risk 9.* **Note this is a spike, not an architecture decision.**

**One further experiment is listed separately because it is a safety test, not a
feasibility test:** verify that adding concurrent RTSP clients does not degrade the
existing recorder's own recording or live-view path (E-12). **This must pass before
anything is connected to a live operational estate.**

---

## 17. Questions that must be answered before architecture

Grouped by who can answer them. None is answered by this document.

### Answerable only by the deploying force — these block architecture outright

- **A-1.** What cameras are actually installed, at what resolution, codec, frame
  rate, mounting height and angle, and what is the resulting px/m at operational
  ranges? *(= Q-1 in [domain-research.md](../domain/domain-research.md) §8; every
  row of [§11](#11-what-is-realistically-achievable-and-what-is-not) depends on it.)*
- **A-2.** Are cameras native IP, or analog behind a DVR/XVR? If the latter, what is
  the recorder's total encoder budget? *(§1.7; no source in any pass addresses this
  and the rig says it matters enormously.)*
- **A-3.** What network exists at a site — bandwidth, symmetry, metering,
  reliability, shared with voice? *(= Q-8; determines which rows of
  [§5.3](#53-what-actually-has-to-cross-the-link) are available.)*
- **A-4.** What continuous power is available for compute, and what does an extra
  15–60 W cost in fuel and logistics? *(= Q-7.)*
- **A-5.** What is the "existing command and control system", by name, with its
  interface? *(= Q-4; §7.3.)*
- **A-6.** What retention is required, for video, clips and metadata separately?
  *(= Q-9; §6.6.)*
- **A-7.** Is there a time source at a disconnected site? *(§6.5 — this is a new
  question, raised by this pass, and it blocks any evidential design.)*
- **A-8.** What does "suspicious activity" mean, stated as observable behaviour?
  *(= Q-3; §3.9. No experiment can substitute for this answer.)*
- **A-9.** Does a gallery/watchlist exist for face recognition, and how large is it?
  *(§3.5 — NIST's own advice is to limit gallery size, and open-set identification
  is a different problem from watchlist matching.)*
- **A-10.** What security accreditation, data classification and network policy
  applies? *(= Q-18; determines whether cloud, internet, or even cross-network
  egress is permissible at all.)*

### Answerable by experiment — see [§16](#16-ten-experiments-and-prototypes-we-should-eventually-run)

- **B-1.** What is the real nuisance-alarm rate, and what causes it? *(Experiment 3.)*
- **B-2.** What is the analysis-rate floor on these scenes? *(Experiment 6.)*
- **B-3.** Does compressed-domain pre-filtering work here? *(Experiment 5.)*
- **B-4.** What does an analysed frame cost in joules? *(Experiment 9.)*
- **B-5.** Does the pipeline survive a multi-day disconnection intact? *(Experiment 7.)*

### Answerable by further desk research

- **C-1.** Verify the IEC/EN 62676-4:2025 pixel-density figures against the standard
  itself, not a vendor summary `[T9]`. *(§1.6 — a 2× change in the identification
  threshold is too consequential to carry on a secondary source.)*
- **C-2.** Retrieve NIST IR 8173 (FIVE) in full for the per-dataset identification
  rates, rather than NIST's news summary. *(§3.5.)*
- **C-3.** Establish whether the H.264/H.265 stream-count gap in `[T13]` is intrinsic
  or a test artefact. *(§2.2 — also E-3.)*
- **C-4.** Determine what fraction of the analytics-relevant model landscape is
  available under permissive rather than copyleft licences. *(§2.5, `[T35]`.)*
- **C-5.** Establish whether ER-01/STQC applies to analytics software or only to
  cameras — recorded as unverified in
  ([competitive-landscape.md](../competitors/competitive-landscape.md) §3.5).

### Deliberately not asked here

What IBVAP should build, which capabilities to prioritise, which stack to use, where
compute should sit, and what the interface should look like. Per
[CLAUDE.md](../../../CLAUDE.md) §2 and §3, those belong to `docs/02-product/`,
`docs/03-design/` and `docs/04-architecture/`, and **nothing in this document
decides any of them.**

---

## 18. Sources

Reliability key: **P** = primary standard, specification or government publication;
**A** = academic or peer-reviewed; **V** = vendor or trade (interest-conflicted);
**M** = measured in this repository.

| ID | Source | Type | URL |
|---|---|---|---|
| T1 | IETF RFC 7826 — *Real-Time Streaming Protocol Version 2.0* (obsoletes RFC 2326) | P | https://www.rfc-editor.org/rfc/rfc7826.txt |
| T3 | ONVIF — *Profiles* overview | P | https://www.onvif.org/profiles/ |
| T4 | ONVIF — *Profile S Deprecation Q&A* | P | https://www.onvif.org/profiles/profile-s/profile-s-deprecation-qna/ |
| T5 | ONVIF press release / trade coverage — end of Profile S support, 9 Oct 2025; conformance closes 31 Mar 2027 | P + V | https://www.onvif.org/?post_type=pressrelease&p=8621 |
| T6 | ONVIF — *Profile M* (analytics, metadata, MQTT) | P | https://www.onvif.org/profiles/profile-m/ |
| T7 | ONVIF — *Profile G* (edge storage and retrieval) | P | https://www.onvif.org/profiles/profile-g/ |
| T8 | IEC/EN 62676-4:2015 DORI pixel densities, via Axis pixel-density white paper and standard summaries | P + V | https://whitepapers.axis.com/en-us/pixel-density-based-on-iec-62676-4-2014 |
| T9 | JVSG — *IEC/EN 62676-4:2025 OODPCVS support* (Validate at 500 px/m) — **vendor summary; verify against the standard** | V | https://www.jvsg.com/iec-62676-4-oodpcvs/ |
| T10 | NVIDIA — *Video Encode and Decode GPU Support Matrix* | P | https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new |
| T11 | NVIDIA — *Jetson Orin* module specifications | P | https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin |
| T12 | NVIDIA — *Software Encode in Orin Nano*, Jetson Linux Developer Guide (Orin Nano has no NVENC) | P | https://docs.nvidia.com/jetson/archives/r36.2/DeveloperGuide/SD/Multimedia/SoftwareEncodeInOrinNano.html |
| T13 | NVIDIA — *DeepStream 7.0 Performance* (TAO model FPS; 1080p30 stream counts by codec) | P | https://archive.docs.nvidia.com/metropolis/deepstream/7.0/dev-guide/text/DS_Performance.html |
| T14 | Frigate — *Recommended Hardware* (detector inference times, camera guidance) | V (open source) | https://docs.frigate.video/frigate/hardware/ |
| T15 | Hailo — *Hailo-8 AI Accelerator* product page and M.2 module datasheets (26 TOPS, 2.5 W typical) | V | https://hailo.ai/products/ai-accelerators/hailo-8-ai-accelerator/ |
| T16 | Google Coral — Edge TPU FAQ and accelerator datasheets (4 TOPS, 2 W) | V | https://www.coral.ai/static/files/Coral-Accelerator-Module-datasheet.pdf |
| T17 | *Scaling Video Analytics on Constrained Edge Nodes* (FilterForward), arXiv 1905.13536 | A | https://arxiv.org/abs/1905.13536 |
| T18 | *Reducto: On-Camera Filtering for Resource-Efficient Real-Time Video Analytics*, SIGCOMM 2020 | A | https://dl.acm.org/doi/10.1145/3387514.3405874 |
| T19 | *CoVA: Exploiting Compressed-Domain Analysis to Accelerate Video Analytics*, arXiv 2207.00588; with compressed-domain motion-detection literature | A | https://arxiv.org/pdf/2207.00588 |
| T20 | *ByteTrack: Multi-Object Tracking by Associating Every Detection Box*, arXiv 2110.06864 | A | https://arxiv.org/abs/2110.06864 |
| T21 | *BoT-SORT: Robust Associations Multi-Pedestrian Tracking*, arXiv 2206.14651; with MOT17/MOT20 SOTA and occlusion literature | A | https://arxiv.org/abs/2206.14651 |
| T22 | *Fast and Resource-Efficient Object Tracking on Edge Devices: A Measurement Study*, arXiv 2309.02666; and *The Impact of Frame-Dropping on Performance and Energy Consumption for Multi-Object Tracking*, arXiv 2304.08152 | A | https://arxiv.org/pdf/2309.02666 |
| T23a | NIST — *Face in Video Evaluation (FIVE)* programme page; NIST IR 8173 — **full report not retrieved (size limit)** | P | https://www.nist.gov/programs-projects/face-video-evaluation-five |
| T23b | NIST — *Identifying Faces in Video Images is Major Challenge, NIST Report Shows* (NIST's own summary of FIVE) | P | https://www.nist.gov/news-events/news/2017/04/identifying-faces-video-images-major-challenge-nist-report-shows |
| T24 | NIST — *FRTE 1:N Identification* results page | P | https://pages.nist.gov/frvt/html/frvt1N.html |
| T25 | *Automatic Number Plate Recognition: A Detailed Survey of Relevant Algorithms*, PMC8123416 | A | https://pmc.ncbi.nlm.nih.gov/articles/PMC8123416/ |
| T25b | ANPR camera vendor material on global shutter, fast shutter and IR illumination for retroreflective plates | V | https://www.e-consystems.com/blog/camera/applications/how-to-choose-the-right-image-sensor-for-automatic-number-plate-recognition-anpr/ |
| T26 | *FusionU10: enhancing pedestrian detection in low-light complex tourist scenes through multimodal fusion*, Frontiers in Neurorobotics (LLVIP visible 0.430 vs IR 0.651 mAP@0.5:0.95) | A | https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2024.1504070/full |
| T27 | *Rethinking Metrics and Benchmarks of Video Anomaly Detection*, arXiv 2505.19022 | A | https://arxiv.org/html/2505.19022v1 |
| T28 | UCF-Crime weakly supervised VAD leaderboard figures (π-VAD 90.33%, RefineVAD 88.92%, Ex-VAD 88.29% AUC), via RefineVAD arXiv 2511.13204 | A | https://arxiv.org/pdf/2511.13204 |
| T29 | Axis Communications — *Zipstream technology* white paper | V | https://whitepapers.axis.com/en-us/axis-zipstream-technology |
| T30 | Vendor RTSP URL references (Hikvision, Dahua, Reolink, Axis paths; ONVIF profile discovery as the alternative) | V | https://www.smartrtsp.com/guides/rtsp-url-list |
| T31 | 1080N / "1080 lite" resolution explanations (960×1080 on AHD/HD-TVI/HD-CVI DVRs) | V | https://www.getscw.com/knowledge-base/1080lite |
| T32 | NATO STANAG 4609 — *NATO Digital Motion Imagery Standard*; MISB ST 0601 UAS Datalink Local Set; SMPTE ST 336 KLV | P | https://impleotv.com/2025/03/11/stanag-4609-isr-video/ |
| T33 | MISB ST 0903 — *Video Moving Target Indicator and Track Metadata* (VMTI Local Data Set, VTargetSeries, VTarget Pack) | P | https://www.impleotv.com/content/misbcore/help/ST903/st903.html |
| T34 | C2PA — *Content Credentials* specification and explainer (SHA-256 hashes, X.509, chained manifests) | P | https://spec.c2pa.org/specifications/specifications/2.4/explainer/Explainer.html |
| T35 | Ultralytics — licensing (AGPL-3.0 default; Enterprise Licence required otherwise) | V | https://www.ultralytics.com/license |
| T36 | *Moving Objects Detection with a Moving Camera: A Comprehensive Review*, arXiv 2001.05238; with PTZ background-subtraction literature | A | https://arxiv.org/pdf/2001.05238 |
| T37 | *An Investigation of the Domain Gap in CLIP-Based Person Re-Identification*, Sensors 25(2):363 | A | https://doi.org/10.3390/s25020363 |
| T38 | **This repository** — [`dvr.py`](../../../dvr.py): behaviour of a Hi-Focus / Dahua HD-XVR-4801H1-H established by testing (TCP-only RTSP, socket timeout, 1080N 960×1080 anamorphic, 12288 kbps / 120 fps total across 8 channels, 25 fps on ch1 only, silent config discard, percent-encoded credentials) | M | [`dvr.py`](../../../dvr.py) |

### Internal cross-references

| Document | Used for |
|---|---|
| [problem.md](../../00-project/problem.md) | The eight named capabilities and the no-dedicated-hardware constraint |
| [domain-research.md](../domain/domain-research.md) | Nuisance alarms, environment, bandwidth, evidence law, DORI, i-LIDS, ONVIF sunset |
| [ssb-operational-context.md](../domain/ssb-operational-context.md) | Road access, power, connectivity, command ranks, open border, existing FRS/ANPR procurement, evidence chain |
| [competitive-landscape.md](../competitors/competitive-landscape.md) | Capability claims, deployment patterns, hardware dependencies, ONVIF compatibility reality, bandwidth figures, egress fragmentation, published gaps |

---

## Document status

**Stage:** 01 — Research → Technology. Complete for this pass.

**What this document is:** an assessment of technical feasibility based on
protocol and profile specifications, vendor engineering documentation,
peer-reviewed research, and one measured device in this repository. Every
performance figure is attributed and every calculation is shown.

**What this document is not:** a technology stack, an architecture, a product
scope, a requirement, or a benchmark. No finding here has been turned into a
requirement, and none should be until `docs/02-product/` and — for anything
technical — `docs/04-architecture/`.

**Known weaknesses of this pass:** nothing was benchmarked hands-on
(§13 exists because of this); NIST IR 8173 was not retrieved in full (C-2); the
IEC 62676-4:2025 figures rest on a vendor summary (C-1); several accuracy figures
are self-reported by the authors of the methods being measured and are treated as
upper bounds; and the `[T38]` observations are a single consumer-grade device, not
a survey of the target estate.

**Next stage gate:** per [CLAUDE.md](../../../CLAUDE.md) §2, product scoping in
`docs/02-product/` may proceed on the research completed so far. Questions A-1
through A-10 in [§17](#17-questions-that-must-be-answered-before-architecture) must
be carried forward as open risks, and **A-1 (what cameras actually exist) and A-3
(what network actually exists) should be treated as blocking for architecture**,
not merely open.

# Technical Feasibility — Software-Defined Video Analytics on Existing IP CCTV

**Stage:** 01 — Research → Technology
**Date:** 2026-08-24
**Scope:** Whether, and under what conditions, the capabilities named in the
official SIH problem statement ([Problem Statement ID 26187](../../00-project/problem.md))
can be delivered by software running against *already-installed* IP CCTV
infrastructure — with no dedicated FRS, ANPR or smart-camera hardware.

This document records what the physics, the standards, the published
engineering, and the measured hardware allow — and where the limits sit —
so that technology-stack, product-scope, and architecture decisions in
`docs/02-product/`, `docs/03-design/` and `docs/04-architecture/` (per
[CLAUDE.md](../../../CLAUDE.md) §2) can be made on solid ground.

## Contents

1. [Executive Summary](#1-executive-summary)
2. [Research Objective and Scope](#2-research-objective-and-scope)
3. [Key Findings](#3-key-findings)
4. [Detailed Findings](#4-detailed-findings)
5. [Implications for IBVAP](#5-implications-for-ibvap)
6. [Risks and Limitations](#6-risks-and-limitations)
7. [Open Questions / Research Gaps](#7-open-questions--research-gaps)
8. [Conclusions](#8-conclusions)
9. [References](#9-references)

---

## 1. Executive Summary

The problem statement asserts that advanced surveillance functions "often
require specialized hardware and proprietary solutions", and proposes to
replace that hardware with software running on "standard IP-based CCTV
cameras". The competitive research already established that the *software*
half of that claim is true — every named capability ships today as software on
third-party cameras ([competitive-landscape.md](../competitors/competitive-landscape.md) §4).

What this document finds is that the binding constraint **moved rather than
disappeared**. It moved out of the camera's silicon and into four places
software cannot reach: the pixels the installed camera actually delivers, the
encoder budget of the recorder in front of it, the decode cost of the stream,
and the watts and bits available at the site.

**The core pattern:** capabilities that need only *presence and motion of a
large object* — person/vehicle detection, single-camera tracking, line
crossing as a mechanism, event logging — are comfortably achievable on
existing, non-purpose-mounted cameras. Capabilities that need *identity* —
face recognition, ANPR, cross-camera tracking, fine-grained vehicle
attributes — degrade to low reliability, because identity needs pixel density
that overview cameras were never specified to deliver. The problem statement
asks for both halves; only one is comfortably reachable without touching the
hardware ([§5](#5-implications-for-ibvap)).

**Supporting evidence for that pattern:**

- Identification-grade imagery needs 250 px/m under the 2015 DORI standard,
  rising to 500 px/m under the 2025 revision — a doubling of the bar every
  existing camera was specified against, if the newer figure holds `[T8][T9]`.
- NIST's own conclusion on video face recognition is that it "may approach
  that of still-photo face recognition, **but only if image collection can be
  improved**" — camera positioning, mounting, lighting and optics `[T23b]`.
  Improving image collection is exactly what a software-only platform cannot do.
- Decode, not inference, is the binding compute constraint, and cannot be
  escaped by analysing fewer frames: P-frames depend on their predecessors, so
  arbitrary sampling still requires full decode. NVIDIA's own figures show a
  Jetson Orin Nano running a detector at 256 fps while sustaining only 8
  full-pipeline 1080p30 H.264 streams `[T13]`.
- H.264 — the codec an existing estate is most likely to have — costs up to
  2.5× more stream capacity than H.265 on the same silicon `[T13]`.
- A single measured recorder in this repository falsified three convenient
  assumptions: UDP is unusable and TCP is mandatory; "1080" can mean 960
  horizontal pixels (1080N); and the device reports success for configuration
  it silently discards `[T38]`.
- What an alert carries is a bandwidth decision worth roughly a factor of 300:
  a 15-second 1080p clip takes ~7.8 minutes over a 128 kbps link; a 320×320
  object crop takes ~1.6 seconds ([§4.5](#45-networking)).
- "Suspicious activity detection" is the weakest named capability, and
  measurably so: models reporting 94.55% AUC on standard benchmarks collapse
  to 16.35% on same-scene reversed-label evaluation, and false-alarm rates
  rise 42% on average — sometimes above 70% — on "hard normal" test sets
  `[T27]`.
- Night is simultaneously the operational peak (infiltration and smuggling
  concentrate in darkness) and the technical trough (a 33.9% relative drop in
  detection accuracy on visible-light night footage versus infrared views of
  the same scenes) `[T26]`.
- Standard, vendor-neutral egress vocabularies already exist — ONVIF Profile M
  and MISB ST 0903/STANAG 4609 — and no vendor in the competitive survey was
  found using either `[T6][T32][T33]`.

**The single most consequential open question** is what cameras and what
network actually exist at the target sites. Neither is measured anywhere in
this research programme, and most of the achievability judgements in this
document depend on it ([§7](#7-open-questions--research-gaps)).

---

## 2. Research Objective and Scope

The objective was to determine, from protocol and profile specifications,
vendor engineering documentation, peer-reviewed research, and one measured
device in this repository, what the problem statement's named capabilities
actually require — in pixels, bitrate, compute, power and bandwidth — when
delivered as software against cameras that were not installed for this
purpose.

No hands-on benchmark was run for this pass beyond what the existing
development rig already demonstrates. Every performance figure is either
published by a vendor, published in a peer-reviewed paper, or calculated here
from stated inputs. Two retrieval gaps are worth flagging up front: NIST IR
8173 (FIVE) could not be fetched directly (the PDF exceeded the fetch size
limit), so its findings are taken from NIST's own news summary `[T23b]`; and
the pixel-density figures for the 2025 revision of IEC/EN 62676-4 come from a
CCTV-design-tool vendor's summary rather than the standard itself `[T9]` and
should be verified before being used in architecture.

This repository already contains a working RTSP ingest against a real,
consumer-grade recorder — [`dvr.py`](../../../dvr.py) and its
[`backups/`](../../../backups), preserved unmodified per
[CLAUDE.md](../../../CLAUDE.md) §3.6. Several findings below are read directly
from its code comments, which record behaviour established by testing against
that hardware. These are cited as `[T38]`. They are single-device
observations, not a survey — but they are the only *measured* evidence this
project currently has, and they are unusually inconvenient for the problem
statement's premise, which raises rather than lowers their value.

Findings are tagged by scope where it materially changes their applicability,
following [CLAUDE.md](../../../CLAUDE.md) §4: **[GLOBAL]** (true for video
analytics on existing CCTV anywhere), **[BORDER]** (true for border/frontier
surveillance generally), **[SIH/SSB]** (true only for this problem statement
or force), and **[MARKET:IN]** (India-specific legal/regulatory/procurement
factor). Unlabelled findings are [GLOBAL]. Sources are cited as `[Tn]`, keyed
to the table in [§9](#9-references).

---

## 3. Key Findings

Ordered by how much each should change what happens next.

1. **The premise survives for software and fails for pixels.** Every named
   capability ships as software on third-party cameras today
   ([competitive-landscape.md](../competitors/competitive-landscape.md) §4),
   but capabilities that need *identity* — face recognition, ANPR,
   cross-camera tracking — need pixel densities (250 px/m in 2015, possibly
   500 px/m under the 2025 standard `[T9]`) that cameras installed for human
   overview were never specified to deliver `[T8][T9]`. The constraint moved
   from silicon to optics; it did not disappear.

2. **NIST's own conclusion contradicts the deployment model.** Video face
   recognition "may approach that of still-photo face recognition, but only if
   image collection can be improved" — camera positioning, mounting, lighting
   and optics `[T23b]`. Improving image collection is precisely what a
   software-on-existing-cameras platform cannot do. Identification rates in
   FIVE ranged from ~60% to >99% purely on image quality.

3. **Decode, not inference, is the binding compute constraint — and cannot be
   escaped by analysing fewer frames.** P-frames depend on their predecessors,
   so arbitrary frame sampling requires full decode anyway; only I-frame-only
   decoding is cheap, and on the rig's 1-second GOP that yields 1 fps `[T38]` —
   below the ~3 fps tracking floor `[T22]`. NVIDIA's own figures show an Orin
   Nano running a PeopleNet-class detector at 256 fps while sustaining only
   **8** full-pipeline 1080p30 H.264 streams `[T13]`.

4. **H.264 — the codec an existing estate is most likely to have — costs up to
   2.5× more stream capacity than H.265 on the same silicon.** AGX Orin: 37
   streams H.265 vs 15 H.264 `[T13]`. IBVAP inherits the expensive half of that
   table.

5. **The recorder in front of the camera can be a harder limit than the
   camera.** Measured on this repository's own hardware: fixed 1080N
   (960×1080, half the horizontal pixels of 1080p), a shared budget of 12,288
   kbps and 120 fps across 8 channels, 25 fps achievable on one channel only,
   and firmware that returns OK for settings it silently discards
   `[T38][T31]`. No downstream software raises any of those.

6. **"Suspicious activity detection" is the weakest capability named, and the
   weakness is measurable.** Models reporting 94.55% AUC collapse to 16.35% on
   same-scene reversed-label evaluation — much of the reported performance is
   scene memorisation, not anomaly understanding. False-alarm rates rise 42%
   on average on hard-normal benchmarks, some exceeding 70% FAR. Human
   annotators agree only at Fleiss' Kappa 0.51–0.68 — the ground truth itself
   is contested. AUC is also insensitive to *when* a detection occurs, which
   is the entire operational point `[T27]`.

7. **Night is the operational peak and the technical trough.** Visible-light
   detection scores mAP 0.430 against 0.651 for infrared on the same night
   scenes — a 33.9% relative drop `[T26]` — while infiltration and smuggling
   are believed to concentrate in darkness
   ([domain-research.md](../domain/domain-research.md) §5.6). "Night-time
   movement detection" is not sold as a distinct feature anywhere in the
   market; it is an operating condition every other feature either survives or
   does not ([competitive-landscape.md](../competitors/competitive-landscape.md) §4.1).

8. **What an alert carries is a bandwidth decision worth a factor of ~300.** A
   15-second 1080p clip is 7.5 MB and takes ~7.8 minutes on a 128 kbps link; a
   320×320 object crop is 25 KB and takes ~1.6 seconds. A per-frame metadata
   firehose at 13–30 kbps per camera is comparable to Verkada's entire
   published per-camera bandwidth budget.

9. **Standard, vendor-neutral vocabularies for analytics egress already exist,
   and the market is not using them.** ONVIF Profile M defines metadata for
   vehicle, licence plate, face, body and geolocation, plus delivery over MQTT
   `[T6]`; MISB ST 0903 (VMTI) defines per-frame detections with bounding
   boxes, geolocation, track IDs and confidence, inside STANAG 4609, which
   NATO-compatible C2 systems already ingest `[T32][T33]`. No vendor in the
   competitive survey was found emitting either.

10. **A single measured, real recorder was enough to falsify three convenient
    assumptions.** UDP is unusable and TCP is mandatory; "1080" can mean 960
    horizontal pixels; and a device will report success for configuration it
    discards `[T38]`. This is one device — but it argues strongly that the
    camera estate must be *measured*, not *specified*.

---

## 4. Detailed Findings

### 4.1 Camera and video interfaces

**RTSP.** RTSP is a control-plane protocol for setup and control of real-time
media delivery; it does not itself carry media, which travels as RTP over UDP,
TCP, or interleaved on the RTSP connection `[T1]`. Control methods are
DESCRIBE, SETUP, PLAY, PAUSE, TEARDOWN, OPTIONS and GET/SET_PARAMETER, with a
default session timeout of 60 seconds `[T1]`. RTSP 2.0 (RFC 7826) obsoletes
1.0 (RFC 2326) and is **not backwards compatible** with it `[T1]`. The
installed CCTV base is believed to speak almost entirely RTSP 1.0, though this
is not verified against a device population.

On the recorder in this repository, UDP transport drops badly and RTSP must be
forced over TCP; without an explicit socket timeout, a dead channel blocks the
read call indefinitely rather than erroring `[T38]` (see
[`dvr.py`](../../../dvr.py), the `OPENCV_FFMPEG_CAPTURE_OPTIONS` block).
RTSP-over-TCP is therefore taken as the safe default for an analytics ingest,
at the cost of head-of-line blocking and higher latency under loss — though
this is not tested on other devices.

The RTSP URL path is **not standardised across manufacturers**: Hikvision uses
`/Streaming/Channels/101`, Dahua `/cam/realmonitor?channel=1&subtype=0`,
Reolink `/h264Preview_01_main`, Axis `/axis-media/media.amp` `[T30]`. The rig
in this repository uses the Dahua-style path, and its password must be
percent-encoded because it contains `@`, which otherwise terminates the
userinfo section and leaves a bogus hostname `[T38]`. This kind of
per-vendor path template and credential handling is the small, undignified
compatibility work that accumulates into the "compatibility lab" every
serious VMS vendor operates
([competitive-landscape.md](../competitors/competitive-landscape.md) §6.4).
Whether the target sites' cameras or recorders accept concurrent RTSP sessions
from a new client at all — and whether doing so degrades existing recording or
live-view — is not known.

**ONVIF.** ONVIF publishes profiles, of which the video-relevant ones are S,
T, G, M and D; a device may conform to several `[T3]`. **Profile S** covers
live H.264 streaming, audio, PTZ, motion events and basic metadata, and most
Profile S cameras also expose a plain RTSP URL
([domain-research.md](../domain/domain-research.md) §6.7). On 9 October 2025
ONVIF announced it is ending support for Profile S in favour of Profile T:
after 31 March 2027 manufacturers can no longer submit new products, or
existing products with new firmware, for Profile S conformance `[T4][T5]`. The
reason is authentication, not features — Profile S mandates username-token
authentication, which ONVIF states "is regarded as too weak today to protect
against unauthorized access to devices" `[T4]`. Existing Profile S devices
keep working after March 2027 and stay listed while the manufacturer maintains
its Declaration of Conformance; the interoperability risk is one-sided — if
vendors remove username-token support in newer firmware, clients that rely on
it break `[T4]`.

**Profile T** adds over Profile S: digest authentication, H.264 and H.265
(replacing MJPEG/MPEG-4), HTTPS for encrypted media, mandatory PTZ, mandatory
metadata streaming, motion and tampering detection, audio output and imaging
configuration; Profile S's IP address filtering is not carried over `[T4]`.
**Profile G** covers edge storage and retrieval: recording configuration,
search, and replay/export, with recording either over the network or on-device
`[T7]`. **Profile M** is the analytics profile: analytics configuration and
query, metadata configuration and streaming, generic object classification,
metadata definitions for geolocation, vehicle, licence plate, human face and
human body, event interfaces for object counters and for face/plate
recognition, rule configuration, and event delivery "through metadata stream,
ONVIF event service **or over MQTT**" `[T6]`.

This is the most important standards finding in the document for integration:
**ONVIF Profile M already defines a vendor-neutral schema for exactly the
object classes the problem statement names, and already names MQTT as a
transport for them.** Whether to use it is an architecture decision, but that
it exists changes what "egress has no standard"
([competitive-landscape.md](../competitors/competitive-landscape.md) §7.1)
means.

Conformance alone has not been enough for two of the best-resourced vendors in
the market: Verkada states "any ONVIF Profile S camera may not work with
Command Connector out-of-the-box" and maintains a hardware compatibility list
with weeks-to-months assessment per model; Milestone needed 1,000+
individually tested ONVIF devices to converge on a single optimised driver and
maintains 16,500+ tested devices
([competitive-landscape.md](../competitors/competitive-landscape.md) §6.4). On
that basis, "IBVAP supports ONVIF" would be a statement of intent rather than a
capability unless backed by a tested-device list. What proportion of the
installed base at the target sites is ONVIF-conformant at all, at which
profile and firmware, is unresolved
([ssb-operational-context.md](../domain/ssb-operational-context.md) §6.3;
[domain-research.md](../domain/domain-research.md) §1.3).

**Codecs.** H.265/HEVC delivers roughly the same visual quality as H.264 at
about half the bitrate, halving storage and LAN bandwidth
([domain-research.md](../domain/domain-research.md) §6.2); Profile T made
H.264 and H.265 the profile codecs, displacing MJPEG and MPEG-4 `[T4]`.
NVIDIA's current decode hardware (6th-generation NVDEC, Blackwell) decodes
MPEG-1/2/4, VC-1, VP8, VP9, H.264, H.265 and AV1 in all documented variants
`[T10]`. Encode is licence-limited on consumer GPUs: GeForce cards cap at 12
concurrent encode sessions, while professional/datacenter cards (RTX PRO, L4,
L40/L40S) are unrestricted `[T10]`. This matters for any design that
transcodes for clip export, low-bandwidth preview or web delivery, and does
not matter for a design that stores the original bitstream and only ever
decodes. Avoiding transcode entirely — storing and shipping the original
encoded bitstream — would remove both the encode-session cap and a large share
of compute cost, but this needs testing against the requirement to produce
evidential clips at a fixed, playable profile. The codec mix in the installed
base is unknown; H.264 is assumed dominant on older estates but this is not
measured for the target sites.

**Stream profiles and sub-streams.** ONVIF exposes a device's media profiles,
including main stream and sub-stream with their encoding and exact RTSP URL,
read directly from the camera `[T30]`. Frigate, the widely deployed
open-source analytics stack, is built around dual-stream use: a
low-resolution sub-stream for continuous detection and the high-resolution
main stream for recording `[T14]`. **This is the cheapest lever in the entire
pipeline, and it is a camera configuration, not a software capability**: if a
second, lower-resolution stream is available, analytics decode cost falls by
roughly the pixel ratio with recording quality untouched; if not, every frame
must be decoded at full resolution. Sub-stream availability, resolution and
frame rate will likely vary enormously across an existing estate and may
already be consumed by the incumbent VMS or a mobile app — this is not
surveyed. Whether sub-streams on the target estate are of usable resolution is
unknown; a CIF or D1 sub-stream (352×288 / 704×576) may be below the pixel
density needed for anything but gross motion ([§6](#6-risks-and-limitations)).

**Frame rate.** Multi-object tracking degrades gracefully from 30 FPS down to
about 3 FPS (HOTA ≈ 43%), then sharply below 2 FPS: association accuracy
(AssA) falls from 43.6% at 3 FPS to 36.5% at 2 FPS to 27.8% at 1 FPS, and mean
track duration falls from 268.5 s at 3 FPS to 156.6 s at 1 FPS. Detection stays
largely intact — it is temporal continuity that fails `[T22]`. Separate work
evaluating rates from 25 Hz down to 1 Hz finds significant drops below 10 Hz
and concludes current tracking approaches "are not suited for lower frame
rates" `[T22]`. This suggests a hard floor of roughly **3–5 analysed frames per
second per camera** for anything needing identity over time (line crossing
with direction, loitering, dwell, counting); detection-only tasks have no such
floor. On the recorder in this repository, hardware limits established by
testing are a total budget of 120 fps across all 8 channels, with 25 fps
achievable on channel 1 only `[T38]` — 120 ÷ 8 = 15 fps per channel if shared
evenly, and the five channels with cameras attached can only be given more by
starving the three that do not, which is exactly what `[T38]` records.

**Resolution.** IEC/EN 62676-4:2015 defines DORI pixel densities on the target
plane: Detection 25 px/m, Observation 62 px/m, Recognition 125 px/m,
Identification 250 px/m `[T8]`. The 2025 revision reportedly raises the bar,
replacing DORI with a seven-level model (OODPCVS) split by object type:
Perceive 125, Characterize 250, Validate 500, Scrutinize 1500 px/m for
high-pixel-density objects; Overview 20, Outline 40, Discern 80 px/m for
low-pixel-density objects. What was "Identification" at 250 px/m is now
"Validation" at 500 px/m `[T9]` (a CCTV-design-tool vendor's summary of the
standard, not the standard itself — this should be verified before use in
architecture). **If accurate, the pixel-density requirement for
identification-grade imagery doubled between the 2015 and 2025 editions of the
governing standard**, and every existing camera was specified against the
older, easier number — or against no number at all. For context, BriefCam's
stated minimum object size is 12–32 pixels depending on class
([competitive-landscape.md](../competitors/competitive-landscape.md) §6.3),
and ANPR needs roughly 250 px/m to resolve plate characters (ibid.).

"1080N" is not 1080p — it is 960×1080, half the horizontal resolution of 1080p
(about 1 megapixel against 2.1), used by analog-HD DVRs (AHD, HD-TVI, HD-CVI)
to manage bandwidth and storage `[T31]`. The recorder in this repository
encodes 1080N, and [`dvr.py`](../../../dvr.py) has to stretch every frame
horizontally by 2× to restore the aspect ratio before it is usable; resolution
is fixed at 1080N on this device, not a setting `[T38]`. **This is a
camera-quality trap that looks like a resolution and is not one**: a 1080N
stream advertises "1080" but delivers half the horizontal pixel density, and
the stretch performed to restore aspect ratio manufactures no information — it
interpolates. A number plate measuring 250 px/m wide in the stretched image
was 125 px/m in the encoded one. How much of the installed base at the target
sites is analog-HD behind a DVR/XVR rather than native IP is unresolved — the
problem statement says "standard IP-based CCTV cameras", but the rig in this
repository is an analog-HD XVR presenting an IP/RTSP interface, and those are
different things.

**The recorder as a hard limit.** On the rig, established by testing:
resolution fixed at 1080N; total encoder budget 12,288 kbps and 120 fps across
all 8 channels; 2,048 kbps per channel on the five live channels only possible
because the three empty channels are starved to 320 kbps / 1 fps; and the
firmware returns OK for values it then silently discards, so the only way to
know what actually landed is to read the configuration back `[T38]`. Where an
analog-HD DVR/XVR sits between cameras and network, it — not the camera, not
the analytics software — likely sets the ceiling on resolution, frame rate and
bitrate as a *shared* budget across channels that adding an analytics
consumer cannot raise (single device; unverified against the actual estate).
It follows that any platform configuring cameras or recorders should verify by
read-back rather than trust the response, treating a device's advertised
capability as a claim to be tested — reinforced by ONVIF's own note that
feature implementation "rests with the camera manufacturer" `[T4]`.

**Compatibility, state of the art.** The ingest side of the market has
effectively standardised on RTSP + ONVIF Profile S, with per-model
compatibility work layered on top
([competitive-landscape.md](../competitors/competitive-landscape.md) §7.1).
Irisity claims the broadest stated ingest in the survey — any camera via
RTSP/ONVIF, including analog via a DVR (ibid. §7). Compatibility work appears
to be unavoidable, unbounded, and ongoing — an operating cost of the product
rather than a phase of it — based on Milestone's bi-monthly device packs and
16,500-device list and Verkada's compatibility lab (ibid. §6.4). Whether a
"universal driver" fallback of the kind Milestone ships is achievable by a
small team, and what fraction of devices it would cover, is unknown.

### 4.2 Video pipeline

**Ingest.** A robust ingest against a real recorder needs, at minimum: forced
TCP transport, an explicit socket timeout, a bounded buffer so a slow consumer
drops frames rather than backing up a queue, per-channel threads so one dead
channel cannot stall the others, and exponential reconnect backoff.
[`dvr.py`](../../../dvr.py) implements all five, each with a comment recording
the failure it was written to fix `[T38]`. The correct ingest posture is
likely "only the newest frame matters" for live analytics and "every frame
matters" only for recording — different pipelines with different queueing
semantics that should not be conflated (a common pattern, not a sourced
principle). Reconnect behaviour under real failure modes — link flap, camera
power brownout, DVR reboot, NTP step, IP address change — is untested on the
rig.

**Decoding.** NVIDIA's published DeepStream figures show decode is a
first-order cost and codec-dependent in a counter-intuitive direction. For a
full pipeline (detection + two classifiers + tracking) at 1080p30:

| Device | 1080p30 streams, H.265 | 1080p30 streams, H.264 |
|---|---|---|
| Jetson Orin Nano | 13 | 8 |
| Jetson Orin NX | 16 | 13 |
| Jetson AGX Orin | 37 | 15 |
| T4 | 45 | 31 |
| A30 | 150 | 98 |
| H100 | 229 | 148 |

`[T13]` (NVIDIA's own figures, output rendering disabled — an upper bound, not
a deployment number). H.264 costs between a third and well over half of stream
capacity compared with H.265 on the same silicon; on AGX Orin the gap is 37 vs
15, a factor of 2.5. Whether this reflects the decoder's optimisation target
rather than something intrinsic to H.264 is not stated by `[T13]` and should
be verified experimentally ([§7](#7-open-questions--research-gaps), E-3). This
matters more for IBVAP than for a greenfield deployment, since an existing
estate is more likely to be H.264 than H.265.

You cannot cheaply "skip" to an arbitrary frame in a long-GOP stream: P-frames
are predicted from their predecessors, so producing frame *n* requires
decoding everything back to the last I-frame. The only cheap subsampling is
I-frame-only decoding, capping the analysis rate at one frame per GOP. On the
rig, the encoder is configured with GOP = FPS — a one-second GOP `[T38]` — so
I-frame-only decoding yields 1 analysed frame per second, below the ~3 fps
tracking floor established above. **I-frame-only sampling and multi-object
tracking are mutually exclusive on this configuration.**

This is the pipeline's central structural finding: **decode cost is
essentially independent of the analytics frame rate**, because you must
decode the frames you intend to throw away. The levers that actually reduce
decode cost are: asking the device for a smaller sub-stream, using hardware
decode, or working in the compressed domain. Turning the inference rate down
is not one of them. Jetson Orin modules publish decode capability of 18×
1080p30 H.265 (Orin Nano), 23× (Orin NX), 22× (AGX Orin) in isolation `[T11]`
— substantially more than the end-to-end pipeline numbers above, confirming
decode alone is not the only bottleneck once inference and tracking are added.

**Frame sampling.** Reducto (SIGCOMM 2020) filters 51–97% of frames at the
camera using cheap frame-differencing features while meeting a target
accuracy `[T18]`. FilterForward achieves roughly an order-of-magnitude
bandwidth reduction by running lightweight "microclassifiers" on constrained
edge nodes `[T17]`. Motion vectors are already present in the H.264/H.265
bitstream as macroblock metadata; extracting them is linear in macroblocks and
frames, enabling motion analysis without full decode `[T19]`. A two-tier
sampler — compressed-domain motion vectors as a nearly free first filter, then
full decode and inference only on candidate segments — looks like the
highest-leverage single design idea available for a power- and
bandwidth-constrained site, supported by `[T17][T18][T19]` and the
"process locally, ship metadata" pattern
([competitive-landscape.md](../competitors/competitive-landscape.md) §8.2),
but **no source retrieved measures it on border-type scenes** (sparse
activity, wind-moved vegetation, livestock, IR at night) and it must be tested
before being designed around. Motion-vector filtering may behave badly in
exactly the conditions the domain research flags — wind-moved vegetation,
rain, insects on the lens and headlight glare all produce large motion-vector
energy with no object present
([competitive-landscape.md](../competitors/competitive-landscape.md) §9, P4) —
though this is not measured.

**Preprocessing.** On a 1080N device, aspect-ratio correction is mandatory
before anything else: the frame must be stretched 960×1080 → 1920×1080 or
"everything looks tall and thin" `[T38]`. Preprocessing for an
existing-CCTV platform must at minimum handle anamorphic correction,
letterboxing to the model's input aspect, colour-space conversion, and the
fact that IR-illuminated night frames are effectively monochrome (not a
sourced checklist). Resizing a 960×1080 frame up to 1920×1080 before inference
costs compute and adds no information; feeding the model the native 960×1080
frame and correcting geometry only in the output coordinates would be cheaper
and lossless — but this needs testing, since models trained on natural aspect
ratios may lose accuracy on anamorphic input.

**Inference.** Published single-inference latencies from Frigate's hardware
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

At 10 ms per inference, a single Coral gives "1000/10 = 100 frames per second"
of detection throughput per Frigate's own arithmetic `[T14]` — at a 5 fps
analysis rate that is 20 cameras of detection on one Coral *if* something else
pays the decode cost (the host CPU, on a Coral-based design). The accelerator
is rarely the binding constraint; decode and memory bandwidth usually are.
NVIDIA's TAO model throughput on Jetson `[T13]`: PeopleNet-ResNet34 at 960×544
INT8 runs at 256 fps (Orin Nano), 372 fps (Orin NX), 970 fps (AGX Orin);
TrafficCamNet-ResNet18 at 419/590/1105 fps respectively; on datacenter parts,
T4 912 fps, L4 1674 fps, A30 3273 fps, H100 6920 fps for PeopleNet. Compared
against the end-to-end stream counts above: Orin Nano can run PeopleNet at 256
fps but sustains only 8 full-pipeline H.264 streams at 1080p30 — roughly 240
fps of inference capability is unreachable because decode, tracking and memory
movement consume the budget first.

Ultralytics YOLO models (YOLOv8, YOLO11 and successors) are distributed under
AGPL-3.0 by default; distributing or hosting a product that includes them
requires either releasing the complete source under AGPL-3.0 or purchasing an
Ultralytics Enterprise Licence `[T35]`. This is a cost and licensing
constraint on a project whose problem statement requires the solution to be
"cost-effective" — it does not decide the stack, since permissively licensed
detectors exist, but detector choice is a legal question as well as an
accuracy one. Whether any target-deployment procurement or security
accreditation regime constrains model provenance or licensing is unknown.

**Tracking.** ByteTrack associates almost every detection box rather than
only high-scoring ones, recovering occluded objects from low-confidence
detections; it reports MOTA 80.3 / IDF1 77.3 / HOTA 63.1 on MOT17 at 30 FPS on
a single V100 `[T20]`. Reported 2025 state of the art on MOT17 is around IDF1
82.1 / MOTA 81.5 / HOTA 65.9, and on the far more crowded MOT20 (~150
pedestrians/frame) around IDF1 81.2 / MOTA 78.4 / HOTA 65.7 (self-reported by
the methods' authors — upper bounds) `[T21]`. Occlusion remains the dominant
failure mode: it "can result in unreliable appearance features, inaccurate
motion estimation, and biased association cues" `[T21]`. A HOTA in the
mid-60s on a curated, daylight, urban benchmark shot by cameras positioned for
the task should probably be expected to translate to materially worse
identity persistence on a border scene — this mirrors the general
benchmark-to-deployment gap documented for face recognition `[T23b]`, anomaly
detection `[T27]` and re-identification `[T37]`, though it is not measured for
MOT specifically, and is the assumption most worth testing.

Cross-camera person re-identification degrades markedly on unseen domains:
state-of-the-art models tested outside their training dataset show
"significant performance drops" versus their Market-1501/MSMT17 numbers, with
the lowest scores on the Airport dataset — the one closest to real
surveillance `[T37]`. Cross-camera identity ("the same person appeared at
BOP-14 and then at the check post") is best treated as a research problem, not
a feature, on a border estate with widely separated, uncalibrated,
differently-lit cameras — the worst case for appearance matching. Tracking
against a moving PTZ camera is a different and harder problem: "methods
designed for fixed cameras cannot achieve accurate background subtraction on
videos captured by moving cameras", and when a PTZ rotates, new background
models must be synthesised before detection can continue `[T36]`. Any
analytic depending on a stable background — virtual fence, loitering, dwell,
abandoned object — is therefore likely invalid while a PTZ is slewing or on a
preset tour, and the platform needs to know when that is happening (ONVIF PTZ
status being the obvious source; Profile T makes PTZ mandatory `[T4]`).

**Event generation.** The dominant behavioural mechanism across the market is
a configured rule — zone, line, direction, dwell time
([competitive-landscape.md](../competitors/competitive-landscape.md) §9, P3;
Axis offers five fixed scenario types, max ten per camera, ibid. §4.2).
Academic sources document the failure mode: "Rule-based models with fixed
thresholds find it difficult to detect actual unusual behaviors in
unpredictable environments, resulting in high false positive rates and missed
anomalies" (ibid. §4.2). ONVIF Profile M defines event delivery over metadata
stream, ONVIF event service, or MQTT, and defines rule configuration as part
of the profile `[T6]`. There are two distinct event products, and conflating
them is a design error: a per-frame metadata stream (every object, every
analysed frame) versus a discrete event (a rule fired). The first is a
firehose sized by scene activity; the second is sized by how often something
happens, and their bandwidth/storage profiles differ by orders of magnitude
([§4.5](#45-networking)).

**Where the pipeline breaks.** Recurring, non-obvious failure modes, ranked by
expected frequency at a remote site (each needing verification): (1)
**timestamps** — multi-camera correlation, evidential hashing and rule timing
all depend on a trustworthy clock, and a disconnected site has no NTP source
unless one is provided locally ([§4.6](#46-storage)); (2) **reconnect storms**
— a link flap dropping 8 RTSP sessions at once, all reconnecting on the same
backoff schedule; (3) **encoder configuration drift** — someone changes the
DVR's resolution or frame rate and every analytic's calibration silently
becomes wrong, made worse by `[T38]`'s silent-discard behaviour; (4) **PTZ
movement invalidating stable-background analytics** `[T36]`; (5) **long-GOP /
dynamic-GOP encoding** making seek and clip extraction imprecise
([§4.6](#46-storage)); (6) **frame drops presenting as motion** — a dropped
second of video looks like a teleport to a tracker. Which of these dominates
in practice has not been observed on a border estate by this project.

### 4.3 Computer vision — capability by capability

Ordered as the problem statement orders them. i-LIDS, the UK government
benchmark, certifies an analytic either as a **primary (sole) detection
system** or only as a **secondary (support)** measure
([domain-research.md](../domain/domain-research.md) §6.7); that distinction is
used below. Which side IBVAP targets is a product decision not made here.

**Person detection — high achievability as support-grade; conditional as
primary.** Claimed with evidence by essentially every vendor surveyed,
including on third-party cameras
([competitive-landscape.md](../competitors/competitive-landscape.md) §4).
Throughput is not the constraint (PeopleNet at 256 fps on Orin Nano `[T13]`).
The constraint is pixels on target: detection is the least demanding DORI
level at 25 px/m `[T8]`, and minimum object sizes of 12–32 px are documented
(ibid. §6.3), so a person at long range on a wide-angle camera may be below
the model's floor regardless of the model. Actual pixel density on target at
the ranges border cameras are pointed at is measurable from a site survey and
is not known.

**Vehicle detection and classification — detection high; fine-grained
classification conditional.** TrafficCamNet runs at 419 fps (Orin Nano) and
1105 fps (AGX Orin) `[T13]` — throughput is not the constraint, and vehicle
detection/classification is claimed by every vendor surveyed
([competitive-landscape.md](../competitors/competitive-landscape.md) §4).
"Classification" in these products likely means coarse type (car/truck/
bus/motorcycle/bicycle), not make, model, colour or load — fine-grained
attributes need Recognition-grade pixel density (125 px/m under the 2015
model, 250 px/m under the 2025 "Characterize" level `[T8][T9]`) and are far
more sensitive to viewpoint and illumination (the vendors do not disaggregate
this). [BORDER] The vehicle classes that matter operationally on a border road
— a loaded porter's cart, a tractor-trailer carrying forest produce, livestock
being driven — are not COCO classes and are not TrafficCamNet classes; the SSB
event catalogue is dominated by contraband, forest products, cattle and
currency ([ssb-operational-context.md](../domain/ssb-operational-context.md) §12),
none of which maps to a standard vehicle taxonomy.

**Multi-object tracking — high within one camera at ≥3 fps; low across
cameras.** Covered in [§4.2](#42-video-pipeline): strong published results
within a single view at adequate frame rate `[T20][T21]`; a hard frame-rate
floor around 3 fps `[T22]`; occlusion as the dominant failure mode `[T21]`;
cross-camera re-identification degrading badly out of domain `[T37]`; invalid
while a PTZ is moving `[T36]`.

**Face detection — high where a face is large enough; that is the whole
question.** Face detection (is there a face) is distinguished throughout the
market from face recognition (whose face), and several vendors claim
detection without claiming recognition
([competitive-landscape.md](../competitors/competitive-landscape.md) §4).
Detection accuracy is most affected by "angle of faces and lighting" (ibid.
§9, P4). Face detection on an overhead-mounted, wide-angle camera installed
for area overview will likely find very few faces, since such cameras look
down on the tops of heads — a mounting-geometry problem no model fixes,
consistent with NIST's finding that camera positioning and mounting is
decisive `[T23b]` (not measured on the target estate).

**Face recognition — low to moderate on existing CCTV, and this is NIST's own
finding, not a pessimistic reading of it.** NIST's FIVE programme evaluated
face recognition of non-cooperating subjects recorded passively, searching
video from fixed cameras against portrait-style galleries of up to 48,000
identities across six datasets `[T23a]`. NIST's summary: portrait-photograph
matching "can exceed 99 percent in some applications", whereas in video
"subjects may be identified anywhere from around 60 percent of the time to
more than 99 percent, depending on video or image quality," with the three
named degradations being small faces, uneven lighting, and non-forward-facing
angles `[T23b]`. NIST's conclusion, quoted: video face recognition accuracy
"may approach that of still-photo face recognition, **but only if image
collection can be improved**", recommending expertise in camera positioning
and mounting alongside lighting and optics, plus limiting the gallery size
`[T23b]`. **"Only if image collection can be improved" is precisely what a
software-on-existing-cameras platform is forbidden from doing** — the problem
statement's premise is in direct tension with the strongest independent
evidence available on what makes FRS work. Current NIST 1:N testing reports
FNIR at a threshold constraining FPIR to 0.003, against galleries of up to 12
million, with leading algorithms reporting error rates below 0.1% on mugshot-
and visa-quality still imagery `[T24]` — figures NIST does not present as
transferable to CCTV video.

Under EU AI Act Article 5, real-time remote biometric identification in
publicly accessible spaces for law enforcement is prohibited by default from 2
February 2025, subject to narrow exceptions
([competitive-landscape.md](../competitors/competitive-landscape.md) §9, P9).
[SIH/SSB] The validation force has already procured a CCTV setup with
Automatic Face Recognition and ANPR
([ssb-operational-context.md](../domain/ssb-operational-context.md) §6.1), and
open legal questions exist about applying face recognition to a population
crossing a treaty-open border lawfully (ibid. §11.6). Whether a *gallery* even
exists for the deployment context is unknown — NIST's own advice is to limit
gallery size `[T23b]`, and a watchlist of tens of known traffickers is a
completely different technical problem from open-set identification.

**ANPR — moderate at a check post with a purpose-aimed camera; low on a
general-purpose camera.** Accuracy at each stage on curated datasets: plate
extraction 89.7–100%, segmentation 97.75–99.75%, character recognition
90–98.1%; but end-to-end numbers on realistic datasets diverge sharply —
93.53% on SSIG versus 78.33% on UFPR-ALPR, the harder, more realistic set
`[T25]`. A ~15-point end-to-end drop between two curated research datasets is
the best available estimate of how fast ANPR degrades as conditions get real.
Documented limiting factors: plate condition, non-standardised formats,
complex scenes, camera quality, camera mount position, tolerance to
distortion, motion blur, contrast, reflections, tilt/skew, fog, processing and
memory limits, and day/night conditions `[T25]`. Dedicated ANPR cameras
achieve their 95–99% figures using fast or global shutters to eliminate motion
blur and IR illuminators tuned to the retroreflective plate `[T25b]`
(vendor material, but the mechanism is physical). Software-only paths that
exist in the market attach physical constraints rather than removing them:
Genetec AutoVu Flexreader works on existing cameras but only up to 30 mph/50
km/h; Milestone XProtect LPR needs the camera to look down on the vehicle at
no more than 30 degrees
([competitive-landscape.md](../competitors/competitive-landscape.md) §6.2).
**"ANPR without dedicated ANPR cameras" is already solved, twice, by the two
largest VMS vendors — and both solutions constrain speed and mounting angle.
The dependency moved from the camera's silicon to the camera's mounting.**
[MARKET:IN] India has roughly 210 million vehicles and over 50 different
number-plate types, against countries with standardised plates where ANPR
accuracy often exceeds 90%
([domain-research.md](../domain/domain-research.md) §6.7). ANPR is likely
achievable where a camera can be aimed at a lane — an ICP, a check post, a
barrier — and not achievable on a wide-area border-road camera, where a plate
at that range and angle is well below 250 px/m (not measured).

**General OCR — high for controlled text; low for incidental scene text.**
i-PRO's ANPR-adjacent capability is listed in the market survey as "P (OCR)"
rather than full ANPR
([competitive-landscape.md](../competitors/competitive-landscape.md) §4) — the
industry itself treats general OCR and plate reading as different
capabilities. General scene OCR (container markings, unit signage, vehicle
lettering) likely inherits every ANPR failure mode in `[T25]` without the
compensating advantages of a standardised, retroreflective, roughly
rectangular, roughly horizontal target, and should be assumed harder than
ANPR, not easier (no source directly compares them). Whether any
operationally useful text exists in these scenes at all is unknown — nothing
in the domain research names a text-reading requirement other than plates.

**Virtual fence / line crossing — high achievability as a mechanism; the
difficulty is entirely in nuisance rejection.** Claimed by every vendor
surveyed, including the free open-source option
([competitive-landscape.md](../competitors/competitive-landscape.md) §4). In
the US SBInet programme, 90% of sensor alerts were false alarms
([domain-research.md](../domain/domain-research.md) §4.2); CIBMS-related
analysis reports false alarms and sensor malfunctions as a leading technical
issue and notes the design does not address distinguishing infiltrators from
wildlife or environmental triggers (ibid.). Documented outdoor false-trigger
sources: rain, fog and snow altering contrast and sharpness; wind-moved
vegetation producing constant pixel changes; sunrise, sunset and vehicle
headlights creating reflections and shadows "that basic algorithms read as
suspicious movement"
([competitive-landscape.md](../competitors/competitive-landscape.md) §4.1).
**The mechanism — a polygon, a line, a direction, a dwell timer — is trivial.
The product is the nuisance-alarm rejection, and that is where the entire
industry's effort goes** (ibid. §9, P4). Object-class-gated rules ("a line
crossing counts only if the crossing object is classified as a person or
vehicle above confidence X and has been tracked for at least N frames") are
likely strictly better than pixel-motion rules — visible in the industry's
move from VMD to object analytics (Milestone alone is marked "P (VMD only)" in
the survey) — though not independently measured. [SIH/SSB] On the validation
border, crossing is a treaty right for Indian, Nepali and Bhutanese nationals,
and MHA's own statement of the problem is "misuse of open border", not
intrusion ([ssb-operational-context.md](../domain/ssb-operational-context.md)
§2.2, §14.1) — a line-crossing alarm that fired with perfect accuracy would
still be almost entirely noise there. **This is the sharpest example in the
whole research corpus of a capability being technically achievable and
operationally misdirected**; the technology question and the product question
have opposite answers here, and the gap belongs to `docs/02-product/`.

**Loitering, dwell and "suspicious activity" — loitering/dwell moderate given
tracking; "suspicious activity" low, and this is the weakest capability in the
problem statement.** Loitering and dwell are rule constructions on top of
tracking — they need identity to persist for the dwell period, putting them on
the ≥3 fps tracking floor `[T22]` and making them fail exactly when occlusion
does `[T21]`. Reported state of the art on UCF-Crime, the standard real-world
surveillance anomaly benchmark (128 hours, 1,900 untrimmed videos, 13 anomaly
types), is around 88–90% frame-level AUC — π-VAD 90.33%, RefineVAD 88.92%,
Ex-VAD 88.29% (self-reported) `[T28]`. **The finding that matters**: a 2025
paper re-examining VAD metrics and benchmarks reports that models scoring
94.55% AUC on standard test sets collapse to 16.35% AUC on same-scene
evaluations with reversed labels — much of the reported performance is scene
overfitting, not anomaly understanding; methods with false-alarm rates ≤10% on
original test sets show a 42% average increase in false alarms on "hard
normal" benchmarks at threshold 0.5, with some exceeding 70% FAR; human
annotators agree on what counts as anomalous only at Fleiss' Kappa 0.51–0.68 —
the ground truth itself is contested; and AUC/AP are "insensitive to the
temporal position of predictions", so a method that detects an event late
scores the same as one that detects it immediately, despite early detection
being the entire operational point `[T27]`. Three independent things are
therefore wrong with "suspicious activity detection" as a capability: the
headline metric does not measure operational usefulness, the reported
accuracy is substantially scene memorisation, and humans cannot agree on the
label. The domain research separately records that "suspicious activity" is
undefined in the problem statement and in every retrieved source
([domain-research.md](../domain/domain-research.md) §5.7, Q-3). The market has
no consensus solution either — rule engines (high false-positive rate in
unpredictable environments), learned anomaly detection (needs large "normal"
training sets relearned when normal changes), and vision-language models,
which are new and unproven here
([competitive-landscape.md](../competitors/competitive-landscape.md) §4.2).
The only defensible near-term form of "suspicious activity" on this estate is
plausibly a small set of explicitly defined, operator-authored composite rules
over reliable primitives — e.g. "a person present in zone A between 2200 and
0500 for more than 90 seconds" — rather than a learned anomaly model; this is
testable, not a recommendation, and must be validated against what operators
actually consider suspicious, which remains unanswered (domain research Q-3).

**Night and low-light analytics — materially worse than daylight on visible
cameras; good on thermal, which most estates likely do not have.** On the
LLVIP night dataset, the same detector on the same scenes scores mAP@0.5:0.95
of 0.430 on visible light versus 0.651 on infrared — a 33.9% relative drop for
visible-light-only detection at night `[T26]`. Multimodal (visible + thermal)
fusion improves over infrared-only by 6.4% on FLIR and 7.2% on M3FD in the
same study (self-reported) `[T26]`. Infrared images "lack rich visual cues,
such as color and detailed information," and similarity between heat sources
and pedestrian features reduces accuracy in complex outdoor environments
`[T26]`. "Night-time movement detection" is not a distinct product feature
anywhere in the market — it is an operating condition every other feature
either survives or does not; vendors sell it as image-sensor quality
(Lightfinder, WDR, IR illumination) or as a thermal camera, not as an
analytic ([competitive-landscape.md](../competitors/competitive-landscape.md)
§4.1). Verkada explicitly states its people and vehicle analytics "are only
supported on visible (or non-thermal) video streams" — the single explicit
vendor statement found on thermal, and it is a negative (ibid.). Thermal
analytics is solved — by Teledyne FLIR and SightLogix — but only by buying
thermal cameras with the analytics inside (ibid. §10, G3), and thermal is not
weather-immune: fog and rain severely limit thermal range because scattering
in water droplets attenuates the infrared signal
([domain-research.md](../domain/domain-research.md) §6.3). IR-illuminated
night video is effectively monochrome, which removes colour as a feature —
every appearance-based mechanism depending on colour (re-identification,
clothing description, vehicle colour, "find the man in the red jacket")
likely degrades or fails at night on such cameras (follows from how IR
illumination works, not stated in a retrieved source, directly testable on the
rig). IR illuminators likely also create their own artefacts — hotspot glare
on nearby surfaces, insects and dust lit by the emitter, retroreflection from
vegetation and signage — each a nuisance-alarm source that exists only at
night (not sourced; widely observed; testable on the rig). [BORDER]
Infiltration and smuggling are believed to concentrate in darkness and poor
visibility — exactly when conventional CCTV performs worst
([domain-research.md](../domain/domain-research.md) §5.6). If true, the
capability with the worst technical outlook carries the highest operational
weight, and this inversion should be treated as the central risk of the whole
programme until measured. What proportion of border CCTV is thermal versus
visible, and whether visible cameras have IR illuminators or true day/night
sensors, is unknown (ibid. §6.3, Q-15).

### 4.4 Compute

The published inference latencies above span roughly 4 ms (discrete Intel
GPU, small model) to 25 ms (RTX 3070, larger model at 640px), with dedicated
low-power NPUs (Coral 10 ms, Hailo-8 6–7 ms) sitting in the middle at a
fraction of the power `[T14]`. Power figures: Hailo-8 delivers 26 TOPS at 2.5
W typical (8.25 W maximum); Google Coral Edge TPU delivers 4 TOPS at 2 W — "2
TOPS per watt" `[T15][T16]`. Jetson Orin power envelopes: Orin Nano 7–25 W,
Orin NX 10–40 W, AGX Orin 15–60 W, at 34–67 / 117–157 / 241–248 sparse INT8
TOPS respectively `[T11]`. **Jetson Orin Nano has no hardware video
encoder** — NVENC was removed relative to the earlier Jetson Nano; encoding is
done in software on the CPU, at "1080p30 supported by 1-2 CPU cores" and up to
about three 1080p30 streams in total `[T12]`. A device marketed as an edge AI
module cannot hardware-encode a single clip; any design producing event clips
by re-encoding on an Orin Nano spends one to two CPU cores per stream to do
it, which storing the original bitstream avoids entirely. CPU-only inference
is likely viable for a single camera at a low analysis rate with a small
model, and not viable for a multi-camera site — no source retrieved gives
CPU-only figures for the models above, which is itself telling, since
Frigate's hardware page recommends an accelerator in every configuration it
documents `[T14]` (an argument from the shape of the documentation, not a
measurement — must be measured, [§7](#7-open-questions--research-gaps) E-2).

**Decode as a first-class cost, not an implementation detail.** The
consequence for compute sizing: a device's inference throughput is not its
stream capacity. NVIDIA's own numbers show Orin Nano running PeopleNet at 256
fps but sustaining only 8 full-pipeline H.264 streams at 1080p30 `[T13]`.
Sizing a deployment on TOPS or on model FPS will overestimate capacity by a
large factor.

**A worked estimate**, from stated inputs (8 cameras; 1080p H.264 main
streams; analysis at 5 fps/camera; a PeopleNet/YOLO-small-class detector;
tracking enabled):

| Quantity | Value | Source of input |
|---|---|---|
| Full-pipeline 1080p30 H.264 streams, Orin Nano | 8 | `[T13]` |
| Full-pipeline 1080p30 H.264 streams, Orin NX | 13 | `[T13]` |
| Detection frames required (8 × 5 fps) | 40 fps | calculated |
| Detection throughput available, Orin Nano (PeopleNet) | 256 fps | `[T13]` |
| Headroom on detection | ≈ 6× | calculated |
| Power envelope, Orin Nano | 7–25 W | `[T11]` |

An 8-camera site is at or slightly beyond the published limit of the smallest
current Jetson if streams are 1080p30 H.264 and decoded in full, **even though
the detector has roughly six times the throughput needed** — the binding
constraint is decode, not inference. Requesting lower-resolution sub-streams
or a lower source frame rate is what changes this number. These are NVIDIA's
figures with output rendering disabled — an upper bound published by the
vendor of the hardware; a real deployment should be sized well below them, and
the margin must be measured, not guessed. Camera count per site, source
resolution and frame rate, codec, scene activity level and the analytics
actually required are all unresolved and must be answered before this
calculation is anything but an illustration of method.

**Edge versus centralised.** Four deployment patterns exist in the market —
on-camera, on-site server/appliance, on-site bridge with cloud brain, and pure
cloud — with every vendor sitting at one point on a single continuous trade of
*where you pay*: camera silicon, site hardware, bandwidth, or scope
([competitive-landscape.md](../competitors/competitive-landscape.md) §5.1).
Three vendors independently converged on hub-and-site: BriefCam Nexus,
Ambient.ai and Genetec Cloudlink all process locally and ship metadata
centrally — "process locally, ship metadata centrally" is settled industry
practice, not an opening (ibid. §5.2). The bandwidth spread between the
extremes is four orders of magnitude — Verkada's 20 kbps per camera against
Genetec Cloud's "recording throughput plus 30%" — "explained entirely by where
the analysis happens" (ibid. §8.1). [BORDER] Centralised processing is
plausibly bandwidth-infeasible at scale on this network, per
[domain-research.md](../domain/domain-research.md) §6.2 (from CIBMS's
unspecified backbone, constrained-uplink systems research, and per-stream
bitrate figures); [§4.5](#45-networking) quantifies it. Every appliance-based
architecture likely imports a physical maintenance obligation at each site,
and where 42% of sites cannot be reached by road
([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.1)
that obligation likely dominates cost
([competitive-landscape.md](../competitors/competitive-landscape.md) §8.5).
**This is the real edge-vs-centralised trade for this deployment, and it is
not a compute trade**: edge processing solves bandwidth and creates a
logistics problem; centralised processing solves logistics and creates a
bandwidth problem the network cannot absorb. Neither is free, and the choice
belongs in `docs/04-architecture/`.

**Multi-camera scaling.** Published full-pipeline stream counts scale roughly
linearly with silicon: 8 (Orin Nano) → 13 (Orin NX) → 15 (AGX Orin) → 31 (T4)
→ 98 (A30) → 148 (H100) for H.264 at 1080p30 `[T13]`. Batching is required to
reach those numbers — "batch sizes must match number of concurrent streams for
optimal throughput", and DeepStream's published figures disable OSD, tiling
and rendering entirely `[T13]`. The scaling axis for this deployment is likely
**site count, not camera count** — many small isolated sites, not one large
cluster ([domain-research.md](../domain/domain-research.md) §6.5) — which
inverts the usual economics, since batching efficiency is unavailable at a
2-camera post. Per-camera pricing, the near-universal market norm, penalises
exactly this shape — many sites, few cameras each, low utilisation per camera
([competitive-landscape.md](../competitors/competitive-landscape.md) §9, P6).

**Power.** No vendor in the competitive survey publishes a power budget for
its analytics workload — Genetec, BriefCam, Irisity and Ambient.ai all specify
NVIDIA GPUs without stating watts
([competitive-landscape.md](../competitors/competitive-landscape.md) §8.4).
Published envelopes for parts that do disclose: Orin Nano 7–25 W, Orin NX
10–40 W, AGX Orin 15–60 W `[T11]`; Hailo-8 2.5 W typical/8.25 W max `[T15]`;
Coral Edge TPU 2 W `[T16]`. A 15 W continuous load is 360 Wh/day, 10.8
kWh/month; a 60 W continuous load is 1.44 kWh/day, 43.2 kWh/month — add
cameras, switch, recorder and conversion losses, and a modest analytics node
at a generator-powered site is a real, recurring fuel line item. [BORDER] At a
generator-powered BOP, power is likely scheduled and fuel-limited, not
continuous, and fuel travels the same unroaded path as everything else, so a
continuously running compute load is a logistics cost, not just an electrical
one ([ssb-operational-context.md](../domain/ssb-operational-context.md)
§10.2). Duty-cycled or activity-gated compute — the accelerator idling until a
cheap compressed-domain or PIR-style trigger wakes it — could plausibly reduce
energy cost by a large factor at sites where activity is genuinely rare, as
implied by the sampling literature `[T17][T18][T19]`, but **no source
retrieved measures energy** rather than bandwidth or accuracy, and it must be
measured before being designed around. The power budget actually available at
a representative site is unknown.

### 4.5 Networking

**Bandwidth.** A single H.264 IP camera stream is on the order of 5 Mbps, and
each additional client pulling that stream multiplies the load off the camera
([domain-research.md](../domain/domain-research.md) §6.2); H.265 delivers
comparable quality at about half the bitrate (ibid.). Axis Zipstream claims an
average 50% or better bandwidth and storage reduction versus standard
compression, using dynamic GOP, dynamic frame rate and region-of-interest
quantisation that preserves "faces, tattoos and clothing patterns" while
compressing "white walls, lawns and vegetation" more aggressively `[T29]`
(vendor's own white paper). Content-adaptive encoding of the Zipstream type
may be *hostile* to downstream analytics in two specific, untested ways:
dynamic GOP lengthens the interval between I-frames, worsening seek precision
and raising the cost of I-frame-only sampling; dynamic frame rate reduces
temporal resolution during quiet periods — exactly when a slow-moving
intruder appears — and can push the stream below the ~3 fps tracking floor
`[T22]`. `[T29]` makes no claim either way about analytics. The rig's total
encoder budget is 12,288 kbps across 8 channels `[T38]` — roughly the bitrate
of two and a half typical 5 Mbps H.264 streams, spread across eight cameras.

**Latency.** RTSP's default session timeout is 60 s, with liveness
demonstrated by RTCP or any RTSP request `[T1]`. Genetec's cloud storage
requires a guaranteed uplink of recording throughput plus 30%, with a 99.9%
SLA and under 150 ms latency
([competitive-landscape.md](../competitors/competitive-landscape.md) §8.1) —
the incumbent cloud architecture assumes a link quality a satellite-backed
border post likely does not have. Satellite links are "typically high-latency,
low-bandwidth and expensive, making it difficult to offload data or receive
updates efficiently"
([domain-research.md](../domain/domain-research.md) §6.2). End-to-end alert
latency likely has at least five additive components — encode/buffering at
the camera, network transit, decode, inference and tracking confirmation, and
rule evaluation — and *tracking confirmation* is frequently the largest, since
a rule like "crossed the line and continued for N frames" cannot fire before N
frames have elapsed (at 5 fps and N=10, that alone is 2 seconds; no source
decomposes surveillance alert latency this way). What alert latency is
operationally acceptable remains unanswered
([domain-research.md](../domain/domain-research.md) §8, Q-12), and without it
no latency budget can be set.

**What actually has to cross the link.** Three candidate egress payloads,
sized from stated inputs:

| Payload | Assumed size | Sustained rate | Time to send over 128 kbps | Over 512 kbps |
|---|---|---|---|---|
| Full 1080p H.264 stream | 4 Mbps | 4 Mbps | not possible | not possible |
| Per-frame object metadata, 5 objects/frame at 5 fps, ~64 B/record binary | 1.6 KB/s | ≈ 13 kbps | continuous | continuous |
| Same as JSON, ~150 B/record | 3.75 KB/s | ≈ 30 kbps | continuous | continuous |
| One 15 s event clip, 1080p @ 4 Mbps | 7.5 MB | — | ≈ 7.8 min | ≈ 2.0 min |
| One full-frame JPEG snapshot (~250 KB) | 250 KB | — | ≈ 16 s | ≈ 4 s |
| One 320×320 object crop JPEG (~25 KB) | 25 KB | — | ≈ 1.6 s | ≈ 0.4 s |
| One discrete event record (~1 KB), 20/day | 20 KB/day | ≈ 0.002 kbps | ≈ 0.06 s | ≈ 0.02 s |

Three conclusions follow directly, and they are arithmetic, not opinion: (1)
full video egress is off the table at these link speeds, matching the
industry's convergence on process-locally-ship-metadata
([competitive-landscape.md](../competitors/competitive-landscape.md) §9, P2);
(2) a per-frame metadata firehose is not cheap — at ~13–30 kbps per camera it
is comparable to Verkada's entire published 20 kbps per-camera budget (ibid.
§8.1), and eight cameras of it would saturate a 128 kbps link; (3) a single
event clip takes minutes, and an object crop takes under two seconds — **the
choice of what an alert carries, a clip, a snapshot, or a crop, is a bandwidth
decision by a factor of 300**, and determines whether an operator can see what
fired the alarm before a response team has to move. The likely right default
is event records plus small crops in real time, with the full clip fetched on
demand — an interpretation of the arithmetic above and of Calipsa's ~300 kb
per event and Verkada's 20 kbps figures (ibid. §8.1), not a design decision.

**Intermittent connectivity.** Peer-reviewed systems research finds per-camera
uplink allocations in constrained deployments can be "a few hundred kilobits
per second or less", conflicting with streaming all video centrally
([domain-research.md](../domain/domain-research.md) §6.2, `[T17]`). Milestone
supports offline licence activation and adding/replacing devices without
reactivation in offline systems, in every edition; Irisity lists air-gapped
on-premise deployment; Genetec Cloudlink is positioned partly on maintaining
local operation during connectivity disruptions; Frigate performs all
processing locally with no cloud subscription
([competitive-landscape.md](../competitors/competitive-landscape.md) §8.3).
Verkada documents an air-gapped *camera network* topology, but the platform
itself still requires the cloud (ibid.). **The competitive survey's single
most important unknown**: whether Genetec, BriefCam, Videonetics, AllGoVision
or Ipsotek support fully disconnected operation including licence validation,
model updates and time synchronisation is not documented anywhere retrieved
(ibid.). Disconnected operation is likely not one feature but four independent
ones: analytics continue running; events queue and reconcile on reconnect
without duplication or loss; licensing does not expire; time stays
trustworthy (no source enumerates them this way). Store-and-forward with
idempotent, monotonically identified events and bounded local queues looks
like the correct shape, with a defined discard policy for when the queue
fills — because at a site offline for days, the queue will fill; ONVIF Profile
G (recording search and replay) `[T7]` is one existing standard for the
retrieval half of this, though untested here. **The single most consequential
unknown in this document** is the actual connectivity profile of a target
site: whether an IP link exists at all, its bandwidth, symmetry, metering,
reliability, and whether it is shared with voice
([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.3,
Q-8) — it determines which of the payload rows above are even available.

### 4.6 Storage

**Continuous video.** From stated bitrates:

| Stream | Per hour | Per day | Per camera, 30 days | 8 cameras, 30 days |
|---|---|---|---|---|
| 1080p H.264 @ 4 Mbps | 1.8 GB | 43.2 GB | 1.30 TB | 10.4 TB |
| 1080p H.265 @ 2 Mbps | 0.9 GB | 21.6 GB | 0.65 TB | 5.2 TB |
| Rig configuration @ 2.048 Mbps `[T38]` | 0.92 GB | 22.1 GB | 0.66 TB | 5.3 TB (5 live channels: 3.3 TB) |

Halving the bitrate with H.265 halves storage as well as bandwidth
([domain-research.md](../domain/domain-research.md) §6.2), and Zipstream-class
encoding claims a further ~50% `[T29]`. Continuous recording at a remote site
is likely a disk-endurance and physical-maintenance problem before it is a
capacity problem: surveillance workloads are sustained sequential writes
24/7, and a failed drive at a site with no road access is not a warranty
event, it is an expedition (based on Verkada's documented experience that a
failed drive means a shipped replacement and physical swap
([competitive-landscape.md](../competitors/competitive-landscape.md) §8.5)
combined with the 42% no-road-access finding
([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.1)).
Whether IBVAP would own recording at all is unresolved — the market forks
cleanly: Genetec, Milestone, Verkada, Eagle Eye, Gorilla and Frigate own
recording; BriefCam, Calipsa, AllGoVision and Ipsotek do not
([competitive-landscape.md](../competitors/competitive-landscape.md) §5.3).
Owning it is the heavier commitment but is what makes evidence management and
offline operation tractable (ibid.) — an architecture decision not made here.

**Event clips.** A 15-second 1080p clip at 4 Mbps is 7.5 MB; at 20
events/camera/day across 8 cameras that is 1.2 GB/day, 36 GB/month — trivial
against the 10.4 TB of continuous recording, roughly 300× smaller. Clip
extraction from a long-GOP stream can only be frame-accurate at I-frame
boundaries without re-encoding: either the clip starts at a keyframe (imprecise
by up to one GOP) or it is re-encoded, which costs an encode session `[T10]`
or one to two CPU cores on hardware with no encoder `[T12]`, and breaks any
hash computed over the original bitstream (this follows from GOP structure; no
retrieved source states it as a design constraint, which is itself notable).
Storing the original bitstream and cutting on keyframe boundaries — accepting
sub-second imprecision at the clip start — likely preserves both compute and
evidential integrity better than re-encoding, but must be tested against
whatever the evidentiary requirement turns out to be.

**Snapshots.** A full-frame 1080p JPEG is ~250 KB; a 320×320 object crop is
~25 KB. At 20 events/day/camera across 8 cameras, full-frame snapshots are 40
MB/day and crops are 4 MB/day — both negligible in storage and decisive in
bandwidth ([§4.5](#45-networking)). The best-shot-image pattern is already
industry practice: i-PRO's Active Guard consumes "metadata information from
i-PRO Edge AI cameras" and best-shot images rather than raw video
([competitive-landscape.md](../competitors/competitive-landscape.md) §6.1).

**Metadata.** Per-frame object metadata at ~13 kbps is 138 MB per camera per
day, 4.1 GB/month; 8 cameras is 33 GB/month. Discrete event records at 20/day
are 20 KB/day per camera — six orders of magnitude smaller. Metadata storage
is likely where the searchable product lives and is therefore worth its cost,
but the retention policy for per-frame metadata should probably be set
independently of the retention policy for video and for events — three
different questions. ONVIF Profile M already defines the metadata schema for
vehicle, licence plate, face, human body and geolocation `[T6]` — an existing
vendor-neutral vocabulary to store against.

**Evidentiary integrity.** [MARKET:IN] Electronic records in India, including
CCTV footage, are governed by Section 63 of the Bharatiya Sakshya Adhiniyam,
2023, in force from 1 July 2024. Admissibility of a copy requires a
certificate signed by the person in charge of the device **and** an expert,
and the certificate must disclose the record's hash value
([domain-research.md](../domain/domain-research.md) §3.5;
[ssb-operational-context.md](../domain/ssb-operational-context.md) §11.5).
C2PA, the content-provenance standard, is built on SHA-256 hashes, X.509
certificates and digital signatures — content is hashed and the hash included
in a signed manifest, so any pixel-level change invalidates it, and
modifications add manifests without deleting previous ones, producing a chain
of custody rather than a single seal `[T34]`. Hashing the stored bitstream at
the moment of capture — rather than an exported copy at the moment of request
— is plausibly the only way to make a Section 63 certificate cheap, since it
decouples the hash from the export; this is testable and interacts directly
with the no-transcode point above, since a re-encoded clip has a different
hash from the recording it came from. Section 63 likely lands harder on this
deployment than on a commercial one, since the device custodian at the point
of capture is a Sub-Inspector or Head Constable, and 42% of sites have no road
access, so getting either signature to a site is a journey
([ssb-operational-context.md](../domain/ssb-operational-context.md) §11.5). In
the market, evidentiary features are priced, not standard: Milestone gates
media-database encryption and digital signing to its upper editions and
Evidence Lock to Corporate only; Genetec's encryption costs 30% of Archiver
capacity for the first certificate
([competitive-landscape.md](../competitors/competitive-landscape.md) §10,
G10) — **the cheapest deployments, which is what a remote site gets, are the
ones without signing, locking or tamper-evidence.** Time synchronisation at a
disconnected site is unresolved and blocks any evidential design: a hash and
a timestamp are only as good as the clock, and nothing in any research pass
establishes whether target sites have NTP, GNSS time, or anything at all — a
site that reboots with a wrong clock produces evidence with a wrong time, and
the failure is silent.

**Retention.** Retention periods mandated or practised at the target sites are
unknown ([domain-research.md](../domain/domain-research.md) §8, Q-9;
[ssb-operational-context.md](../domain/ssb-operational-context.md) §11.5) —
without it, the continuous-video storage table above cannot be turned into a
disk order. Retention will likely differ by artefact class — continuous video
shortest, event clips longer, event metadata longest, and anything attached
to an open case indefinitely — consistent with Evidence Lock existing as a
distinct product feature
([competitive-landscape.md](../competitors/competitive-landscape.md) §10,
G10).

### 4.7 Integration

Ingest has standardised on RTSP + ONVIF Profile S; **egress has not**. Every
vendor emits events differently — MIP plugins, REST, WebSocket, webhooks,
MQTT, ONVIF virtual camera, VMS bookmarks
([competitive-landscape.md](../competitors/competitive-landscape.md) §7.1).
Two existing patterns stand out as low-friction: AllGoVision's ONVIF virtual
camera (presenting analytics output as an ONVIF camera, so any ONVIF VMS
ingests it with no plugin) and Milestone AI Bridge (a documented Docker
container contract into the largest open VMS) (ibid.).

Standards already exist for this. **ONVIF Profile M** defines analytics
metadata, object classification, metadata definitions for
vehicle/licence-plate/face/body/geolocation, event interfaces for object
counters and for face/plate recognition, rule configuration, and delivery via
metadata stream, ONVIF event service or MQTT `[T6]`. **STANAG 4609** is
NATO's digital motion imagery standard, "produced by most coalition
full-motion video sensors and ground stations", giving common methods for
exchanging motion imagery with metadata across systems and nations; KLV
encoding follows SMPTE ST 336 `[T32]`. **MISB ST 0903 (VMTI)** defines how to
encode metadata about objects detected in video — number of targets per
frame, target position (pixel coordinates or bounding box), target geographic
location, **target track ID and history**, and confidence — structured as a
VMTI Local Data Set containing a VTargetSeries of VTarget Packs; it is the
standard used "when video analytics identify moving targets or tracks"
`[T33]`. **MISB ST 0903 is, almost exactly, a defence-standard schema for the
output of the video pipeline described in this document.** No vendor in the
competitive survey was found emitting it. Whether it is the right egress for
this deployment is an architecture question; that it exists, and that it is
the format a NATO-compatible C2 system already ingests `[T32]`, is a fact the
architecture stage should not have to rediscover. There are therefore three
plausible egress vocabularies rather than none — ONVIF Profile M
(surveillance-industry native, MQTT-capable), MISB ST 0903/STANAG 4609
(defence C2 native), and an ad-hoc JSON event over webhook/MQTT (universal,
unstandardised) — serving different consumers, not mutually exclusive.

**What the target C2 actually is** remains unresolved and unchanged by this
pass. The problem statement requires integration with "existing command and
control systems", but no source in any research pass names such a system for
the validation force, with a vendor, protocol, data model or network reach.
The only credible candidate found is **SIMS**, a seizure register that
records outcomes, not detections
([ssb-operational-context.md](../domain/ssb-operational-context.md) §9,
§14.10). For the BSF context, a Command and Control Centre is
architecturally central to CIBMS but is not named or specified
([domain-research.md](../domain/domain-research.md) §3.6). Until this is
answered, the only defensible integration posture is likely to emit into a
documented, standard vocabulary and let an adapter be written per consumer,
since the consumer is unknown, may be several, and includes at least one
organisation (state police) that did not produce the data
([domain-research.md](../domain/domain-research.md) §3.5). Whether the
network where cameras sit can reach the network where any C2 system sits at
all, and under what security policy, is unknown
([domain-research.md](../domain/domain-research.md) §8, Q-18).

Independent of the C2 question, a video analytics platform likely needs at
least five distinct interfaces, and conflating them is a common design error:
(1) live event stream, (2) historical event/metadata query, (3) video
retrieval and clip export, (4) configuration and health, (5)
enrolment/watchlist management where recognition is in scope. `[T6]` and
`[T7]` cover roughly (1), (2) and (3) between them (the split is visible in
the market survey's integration table
([competitive-landscape.md](../competitors/competitive-landscape.md) §7), but
no source enumerates it this way).

### 4.8 Deployment

**Remote sites.** 42% of BOPs on the validation border (308 of 734) lack road
connectivity ([ssb-operational-context.md](../domain/ssb-operational-context.md)
§10.1); border observation posts are reported to lack basic electricity
([domain-research.md](../domain/domain-research.md) §1.2); generators are
provided where there is no grid connection and the situation varies state to
state ([ssb-operational-context.md](../domain/ssb-operational-context.md)
§10.2). The echelons nearest the camera are commanded by a Sub-Inspector (BOP)
and a Head Constable (check post) (ibid. §3.2), and lack of technical
expertise for equipment operation and maintenance is a documented deficiency
([domain-research.md](../domain/domain-research.md) §4.3). The real deployment
unit in this industry is a site survey by a trained integrator, not an
installer running a wizard — Genetec and Milestone both run partner
certification programmes, and Genetec ships a camera requirements calculator
whose stated purpose includes verifying whether existing cameras "need to be
modified" ([competitive-landscape.md](../competitors/competitive-landscape.md)
§9, P7). Software placed at such a site must run unattended for long periods
and likely must fail in a way a Sub-Inspector can recognise and report over a
radio or satellite phone
([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.5) —
a technical requirement on health and diagnostics design, not a UX nicety, and
unusual, since most of this market assumes a control room and an operator
role hierarchy ([competitive-landscape.md](../competitors/competitive-landscape.md)
§10, G7). Automated capability assessment — the platform measuring, per
camera, what pixel density and frame rate it is actually getting and
therefore which analytics it can honestly support — looks like the technical
substitute for a site survey that this deployment shape requires; the
competitive research identifies this as an unfilled gap (ibid. §10, G5–G6),
and the i-LIDS primary/secondary framing gives it a vocabulary
([domain-research.md](../domain/domain-research.md) §6.7). It is technically
straightforward to measure pixel density given a known reference; the hard
part is knowing the scene geometry. Untested.

**Centralised command centre.** A Command and Control Centre where sensor
data is aggregated into a composite picture is architecturally central to
CIBMS ([domain-research.md](../domain/domain-research.md) §1.3), and
centralised decision-making is separately flagged as a risk of delaying
urgent field responses (ibid. §3.6). No SSB control room, monitoring roster
or video wall is documented anywhere in the domain research; whether the
validation force watches live video at all is genuinely unknown
([ssb-operational-context.md](../domain/ssb-operational-context.md) §7,
§14.7). A centralised deployment tier cannot be assumed to have a human
watching it — its technical purpose may be aggregation, search and reporting
rather than live monitoring, which materially changes latency requirements
and is a product question.

**Hybrid deployment.** Hub-and-site with local processing and central
metadata is settled industry practice
([competitive-landscape.md](../competitors/competitive-landscape.md) §5.2),
and Milestone offers two distinct multi-site forms (Federated Architecture and
Interconnect) with different edition requirements (ibid.). Containerised
Linux is the emerging norm for the analytics layer even where the VMS layer is
Windows: Frigate ships as Docker containers and Milestone AI Bridge expects
third-party analytics "deployed as docker containers" (ibid. §5.4). The two
most GPU-dependent products in the competitive survey — Genetec KiwiVision and
BriefCam — both advise against virtualisation (ibid. §5.5). A hybrid design
has to answer three questions the single-tier designs do not: what happens to
events generated while the site is disconnected, how models and configuration
reach a site over a link that may be metered, and which tier is authoritative
for time.

**Updates and maintenance.** Verkada documents that during a Command
Connector firmware update "the cameras connected to Command Connector will
not record footage", that customers cannot install their own drives, and that
it provides no security patches or firmware updates for non-Verkada cameras
([competitive-landscape.md](../competitors/competitive-landscape.md) §8.5). A
100 MB model or container update over a 128 kbps link takes ≈1 hour 44
minutes; over 512 kbps, ≈26 minutes; a 1 GB image takes ≈17 hours at 128 kbps
— update size is a deployment constraint, not a build detail. Delta/
differential updates and resumable transfer are likely not optimisations at
these link speeds but the difference between an update being possible and
not; untested, and no source retrieved addresses OTA update sizing for video
analytics platforms. Equipment maintenance is identified as critical for the
domain, with specialised technical training and spare-parts availability both
undefined challenges, and high reliance on external vendors with minimal
oversight ([domain-research.md](../domain/domain-research.md) §6.4).

---

## 5. Implications for IBVAP

**This section states expected feasibility on existing, non-purpose-mounted
CCTV in this deployment context. It is a research judgement, not a product
scope.** Every row would move if a camera were re-aimed or replaced — which
the problem statement forbids.

| Capability (as named in the problem statement) | On a purpose-aimed camera (check post, lane, gate) | On a general-purpose existing camera | Binding limit |
|---|---|---|---|
| Human detection | High | Moderate–High | pixels on target, night |
| Human tracking (single camera) | High | Moderate | frame rate, occlusion |
| Human tracking (cross-camera) | Low | Low | domain gap `[T37]`, geometry |
| Vehicle detection | High | Moderate–High | pixels on target, night |
| Vehicle classification (coarse type) | High | Moderate | pixels on target, angle |
| Vehicle attributes (make/model/colour) | Moderate | Low | pixels on target; colour lost at night |
| Face detection | High | Low–Moderate | mounting geometry, pixels |
| Face recognition | Moderate | Low | pixels, mounting, `[T23b]`; plus legal ([§4.3](#43-computer-vision--capability-by-capability)) |
| ANPR | Moderate–High | Low | pixel density (250 px/m), motion blur, angle |
| General OCR | Moderate | Low | as ANPR, without the compensations |
| Virtual fence / line crossing (mechanism) | High | High | — |
| Virtual fence at an acceptable nuisance rate | Moderate | Unproven | weather, environment |
| Loitering / dwell | Moderate | Moderate | frame rate, occlusion |
| "Suspicious activity" (learned) | Low | Low | scene overfitting, false-alarm rate, undefined ground truth `[T27]` |
| "Suspicious activity" (explicit composite rules) | Moderate | Moderate | quality of the primitives it composes |
| Night-time movement detection (visible camera) | Moderate | Low–Moderate | photon limit, `[T26]` |
| Night-time movement detection (thermal camera) | High | n/a — few thermal cameras installed | availability, not capability |
| Real-time alert generation | High | High | link bandwidth (what the alert can carry) |
| Event logging | High | High | storage and time integrity |

**The pattern in the right-hand column is the finding.** The capabilities
that survive on a general-purpose existing camera are the ones that need only
*presence and motion of a large object*. Every capability that needs
*identity* — face recognition, ANPR, cross-camera tracking, fine vehicle
attributes — degrades to Low, because identity needs pixel density that
overview cameras were never specified to deliver. **The problem statement
asks for both halves. Only one half is comfortably reachable without touching
the hardware.** How to respond to that is a product decision and belongs in
`docs/02-product/`.

---

## 6. Risks and Limitations

### 6.1 Hard physical limitations software cannot solve

Each of these is a constraint of optics, physics, or information theory. They
bound IBVAP exactly as they bound every competitor, and no model, no training
data and no amount of engineering removes them.

- **Pixels on target.** DORI/OODPCVS is physics `[T8][T9]`. Detection needs
  ~25 px/m; identification needed 250 px/m under the 2015 standard and,
  possibly, 500 px/m under the 2025 revision. A camera installed to see that
  *someone* is there cannot be made to show *who*. Software can only
  interpolate, and interpolation manufactures no information.
- **Field of view.** A face that never enters the frame, or enters it only as
  the top of a head, cannot be recognised. NIST's own conclusion is that video
  face recognition can approach still-photo accuracy "only if image
  collection can be improved" — camera positioning, mounting, lighting and
  optics `[T23b]`. All four are hardware.
- **Photons at night.** A visible-light sensor with insufficient illumination
  produces noise, not signal. The measured cost is a 33.9% relative drop in
  detection mAP on night data versus the infrared view of the same scenes
  `[T26]`. Denoising and enhancement trade noise for blur; they do not add
  photons.
- **Atmospheric attenuation.** Line-of-sight equipment is degraded by heavy
  rain, storms and dense fog
  ([domain-research.md](../domain/domain-research.md) §1.2), and thermal is
  not exempt — scattering in water droplets attenuates the infrared signal,
  with higher droplet density causing more attenuation (ibid. §6.3).
- **Motion blur.** Blur is set by exposure time and target velocity at the
  sensor. It is why dedicated ANPR cameras use fast or global shutters
  `[T25b]`, and why software ANPR is speed-limited (Genetec Flexreader: 50
  km/h) ([competitive-landscape.md](../competitors/competitive-landscape.md)
  §6.2). A blurred plate has lost the information; deblurring hallucinates it.
- **Viewing angle.** Milestone's software LPR requires the camera to look
  down on the vehicle at no more than 30 degrees (ibid.); Avigilon's LPR
  cannot use panoramic, 360, fisheye or PTZ cameras at all (ibid. §6.1).
  Geometry, not algorithm.
- **Temporal sampling.** Below ~2–3 analysed fps, identity association
  collapses (AssA 43.6% → 27.8% between 3 and 1 fps) `[T22]`. You cannot track
  what you did not observe between two positions.
- **Codec information loss.** A frame encoded at 2 Mbps 1080N and then
  upscaled contains the information of 960×1080 at 2 Mbps, whatever its
  stated dimensions `[T31][T38]`. Compression artefacts are indistinguishable
  from scene content to a downstream model.
- **The recorder's shared budget.** Where a DVR/XVR fronts the cameras, its
  total bitrate and frame-rate budget is fixed and shared across channels
  `[T38]`. No software downstream can raise it, and asking one channel for
  more takes it from another.
- **Occlusion.** An object behind another object is not in the image.
  Occlusion is the documented dominant failure mode of multi-object tracking
  `[T21]`.
- **The link.** A 128 kbps uplink carries 128 kilobits per second. A
  15-second 1080p clip takes ~7.8 minutes ([§4.5](#45-networking)), and no
  compression scheme changes the order of magnitude.
- **Energy.** Inference costs joules. Hailo-8 at 2.5 W and Orin Nano at 7–25
  W `[T15][T11]` are the floor for their respective capability classes, and
  at a fuel-limited site that floor is a logistics fact.

### 6.2 Camera-quality limitations

Distinct from the physical limits above: these are properties of *the
cameras that happen to be installed*, which a different procurement could
have avoided, but which IBVAP by definition inherits.

| Limitation | Why it matters | Evidence |
|---|---|---|
| Specified for Detection/Observation density (25–62 px/m), not Identification | Face recognition and ANPR are out of reach on such cameras regardless of software | `[T8]`, [competitive-landscape.md](../competitors/competitive-landscape.md) §6.3 |
| 1080N / "1080 lite" anamorphic encoding | Halves horizontal pixel density while advertising "1080" | `[T31][T38]` |
| Wide-angle overview mounting | Maximises coverage, minimises px/m; looks down on heads not faces | `[T23b]` |
| No true day/night sensor or IR illuminator | Night performance falls to the photon limit | [domain-research.md](../domain/domain-research.md) §6.3 |
| IR illumination is monochrome | Removes colour as a feature for re-ID, description, vehicle colour | interpretation ([§4.3](#43-computer-vision--capability-by-capability)) |
| Fixed cameras with no overlap | Cross-camera tracking has no geometric constraint to exploit | `[T37]` |
| PTZ on preset tour | Stable-background analytics invalid while moving | `[T36]` |
| Shared DVR encoder budget | Frame rate and bitrate are not per-camera choices | `[T38]` |
| Unknown/undocumented ONVIF conformance and firmware | Compatibility must be established per model | `[T4]`, [competitive-landscape.md](../competitors/competitive-landscape.md) §6.4 |
| Lens condition — dirt, spider webs, condensation, IR hotspot | Silent, gradual degradation that looks like scene change | no source retrieved quantifies it |
| Clock drift on the camera or recorder | Breaks correlation and evidential timestamps | [§4.6](#46-storage) |

The single most useful thing a platform could plausibly do about all of the
above is measure and report it per camera rather than fail silently — the
unfilled gap the competitive research identifies
([competitive-landscape.md](../competitors/competitive-landscape.md) §10,
G5/G6) — though this is an interpretation, not a requirement.

### 6.3 Major technical risks, ranked by expected impact × likelihood

1. **The installed camera estate cannot physically support the named identity
   capabilities, and nobody has measured it.** If existing cameras deliver
   25–62 px/m, ANPR and face recognition are unreachable on them at any
   software quality `[T8][T9]`. Likelihood high — the estate is unknown, and
   cameras installed for human monitoring are specified for
   Detection/Observation
   ([competitive-landscape.md](../competitors/competitive-landscape.md) §6.3).
   Mitigation direction: measure before promising.
2. **Nuisance alarms make the system untrusted, which is worse than no
   system.** SBInet's precedent is 90% false alarms
   ([domain-research.md](../domain/domain-research.md) §4.2); system accuracy
   is separately found to drive operator reliance (ibid. §4.1); the
   documented environmental triggers — wind-moved vegetation, rain, fog,
   headlight glare, wildlife — are all present at these sites
   ([competitive-landscape.md](../competitors/competitive-landscape.md)
   §4.1).
3. **Night performance is inadequate exactly when it matters most.** `[T26]`
   plus [domain-research.md](../domain/domain-research.md) §5.6, compounded
   by the unknown thermal/IR composition of the estate.
4. **The uplink cannot carry what the design assumes.** If real uplinks are
   "a few hundred kilobits per second or less"
   ([domain-research.md](../domain/domain-research.md) §6.2), even continuous
   metadata is marginal and clips are impossible in real time. Likelihood
   high — connectivity is unanswered and satellite is documented in the
   inventory ([ssb-operational-context.md](../domain/ssb-operational-context.md)
   §10.3).
5. **Power and physical maintenance at unroaded sites may exceed the
   software's value.** Continuous compute is a fuel logistics cost at a
   generator-powered site with no road (ibid. §10.1, §10.2), and every
   appliance architecture imports a physical maintenance obligation
   ([competitive-landscape.md](../competitors/competitive-landscape.md)
   §8.5).
6. **Per-model compatibility work is unbounded and consumes the team.** Two
   of the best-resourced vendors in the market both built compatibility labs
   and still warn buyers (ibid. §6.4); the rig's own quirks — TCP-only,
   percent-encoded passwords, silent config discard, anamorphic frames — are
   three devices' worth of surprises from one device `[T38]`.
7. **"Suspicious activity" cannot be delivered as understood, and it is in
   the problem statement.** `[T27]` shows the benchmark numbers do not
   transfer; the domain research shows the term is undefined by anyone
   ([domain-research.md](../domain/domain-research.md) §5.7, Q-3). The risk
   is expectation, not engineering — the capability will be judged against an
   unstated standard, and this can only be resolved by a person, not an
   experiment.
8. **Evidence produced may be inadmissible or unusable.** Section 63 BSA
   requires a hash and two signatures
   ([domain-research.md](../domain/domain-research.md) §3.5); transcoding
   changes the hash; clock integrity at a disconnected site is entirely
   unestablished; and the market prices signing and tamper-evidence as an
   upper-edition feature
   ([competitive-landscape.md](../competitors/competitive-landscape.md) §10,
   G10). A silent wrong clock is the worst version of this risk.
9. **Integration has no defined target.** "Existing command and control
   systems" is a requirement whose object is unnamed; the only credible
   candidate on the validation border records outcomes rather than
   detections ([ssb-operational-context.md](../domain/ssb-operational-context.md)
   §9, §14.10); egress has not standardised in the market
   ([competitive-landscape.md](../competitors/competitive-landscape.md)
   §7.1). Risk of building an adapter for a system that does not exist, or
   missing one that does.
10. **Legal and licensing constraints could invalidate a headline capability
    or the build.** Face recognition on a treaty-open border has an
    unresolved legal basis
    ([ssb-operational-context.md](../domain/ssb-operational-context.md)
    §11.6) and is prohibited by default for law enforcement in the EU
    ([competitive-landscape.md](../competitors/competitive-landscape.md) §9,
    P9); India's ER-01/STQC bars sale of non-conforming cameras from 1 April
    2026, so the installed base will churn (ibid. §3.5); and the most
    convenient detector families are AGPL-3.0, requiring either full source
    release or a commercial licence `[T35]`.

---

## 7. Open Questions / Research Gaps

### 7.1 Questions answerable only by the deploying force — block architecture outright

- **What cameras are actually installed** — resolution, codec, frame rate,
  mounting height and angle, and the resulting px/m at operational ranges.
  Every row of [§5](#5-implications-for-ibvap) depends on it.
- **Are cameras native IP, or analog behind a DVR/XVR?** If the latter, what
  is the recorder's total encoder budget ([§4.1](#41-camera-and-video-interfaces))?
  No source in any pass addresses this, and the rig says it matters enormously.
- **What network exists at a site** — bandwidth, symmetry, metering,
  reliability, shared with voice? Determines which egress payloads
  ([§4.5](#45-networking)) are available at all. **This and the previous
  question are the two most consequential open items in this document.**
- **What continuous power is available for compute**, and what does an extra
  15–60 W cost in fuel and logistics ([§4.4](#44-compute))?
- **What is the "existing command and control system"**, by name, with its
  interface ([§4.7](#47-integration))?
- **What retention is required**, for video, clips and metadata separately
  ([§4.6](#46-storage))?
- **Is there a time source at a disconnected site?** Raised by this pass; it
  blocks any evidential design ([§4.6](#46-storage)).
- **What does "suspicious activity" mean**, stated as observable behaviour?
  No experiment can substitute for this answer ([§4.3](#43-computer-vision--capability-by-capability)).
- **Does a gallery/watchlist exist for face recognition, and how large is
  it?** NIST's own advice is to limit gallery size, and open-set
  identification is a different problem from watchlist matching.
- **What security accreditation, data classification and network policy
  applies?** Determines whether cloud, internet, or even cross-network
  egress is permissible at all.

### 7.2 Questions answerable by experiment

These need nothing this project does not already have — several can be
answered on the rig hardware already in this repository.

| Unknown | Why it blocks | Where it can be tested |
|---|---|---|
| Actual pixel density on target for real border camera geometry | Determines which rows of [§5](#5-implications-for-ibvap) are reachable | Any site, with a tape measure and a target |
| CPU-only inference and decode throughput per camera | Decides whether an accelerator is mandatory | The rig in this repo |
| Whether the H.264/H.265 stream-count gap `[T13]` reproduces | Changes sizing by up to 2.5× | The rig + any Jetson |
| Whether compressed-domain motion-vector filtering works on border-type scenes | The central power/bandwidth lever ([§4.2](#42-video-pipeline)) | Recorded night and windy-day footage |
| Real nuisance-alarm rate of an object-gated virtual fence over 24h of real footage | The product's credibility ([§4.3](#43-computer-vision--capability-by-capability)) | The rig, unattended, for a week |
| Detection and tracking performance on IR-illuminated night footage | The night-inversion risk | The rig, after dark |
| Whether tracking holds at 5 fps, 3 fps and 1 fps on real footage | Sets the analysis-rate floor for this estate | The rig, resampled |
| Whether a 1080N stream can support any identity-grade analytic at any range | The anamorphic trap ([§4.1](#41-camera-and-video-interfaces)) | The rig, directly |
| End-to-end alert latency decomposition | No latency budget exists | The rig |
| Energy per analysed frame, per accelerator | Power is undocumented industry-wide | Any device plus an inline power meter |
| Pipeline behaviour across a simulated multi-day disconnection | Store-and-forward correctness | The rig, with the link pulled |
| Whether concurrent RTSP clients degrade an existing recorder's own recording | Deployment safety on a live estate | The rig |

The engineering stage decides which of these to schedule, per
[CLAUDE.md](../../../CLAUDE.md) §2 — none is scheduled or scoped here. The
single most valuable one is plausibly the seven-day unattended nuisance-alarm
run: it produces the false-alarm number the entire market declines to publish
([competitive-landscape.md](../competitors/competitive-landscape.md) §9,
P10). One experiment is a safety test rather than a feasibility test and
should be treated as a precondition, not an option: verifying that concurrent
RTSP clients do not degrade the existing recorder's own recording or
live-view path, before anything is connected to a live operational estate.

### 7.3 Questions answerable by further desk research

- Verify the IEC/EN 62676-4:2025 pixel-density figures against the standard
  itself, not a vendor summary `[T9]` — a 2× change in the identification
  threshold is too consequential to carry on a secondary source.
- Retrieve NIST IR 8173 (FIVE) in full for the per-dataset identification
  rates, rather than NIST's news summary.
- Establish whether the H.264/H.265 stream-count gap in `[T13]` is intrinsic
  or a test artefact.
- Determine what fraction of the analytics-relevant model landscape is
  available under permissive rather than copyleft licences `[T35]`.
- Establish whether ER-01/STQC applies to analytics software or only to
  cameras — recorded as unverified in
  [competitive-landscape.md](../competitors/competitive-landscape.md) §3.5.

### 7.4 Deliberately not asked here

What IBVAP should build, which capabilities to prioritise, which stack to
use, where compute should sit, and what the interface should look like. Per
[CLAUDE.md](../../../CLAUDE.md) §2 and §3, those belong to
`docs/02-product/`, `docs/03-design/` and `docs/04-architecture/`, and
nothing in this document decides any of them.

---

## 8. Conclusions

The software half of the problem statement's claim holds: every named
capability already exists as software running on third-party cameras
elsewhere in the market. What does not hold is the assumption that this
software can be pointed at *any* existing camera and deliver the same result.
The constraint that specialized hardware used to absorb — pixel density,
encoder budget, decode throughput, link bandwidth, power — does not disappear
when the hardware is removed from the design; it resurfaces as a property of
the specific camera, recorder, network and site the software is asked to run
against.

This produces a consistent, testable split rather than a uniform "yes" or
"no": capabilities built on presence and motion of a large object are
achievable on existing, non-purpose-mounted CCTV; capabilities built on
identity — who, whose plate, whose face, the same person across two cameras —
are not, because they need pixel density that overview cameras were never
specified to deliver, and NIST's own evidence is that fixing this requires
changing the camera, which the problem statement forbids.

A small number of items dominate the risk picture: the camera estate and the
network at target sites are both unmeasured and both gate nearly every other
judgement in this document; nuisance-alarm rate and night performance are the
two technical properties most likely to determine whether the system is
trusted at all; and "suspicious activity detection" as named in the problem
statement has no technical solution that survives close reading of the
literature. None of these is a reason not to proceed — several are directly
testable on hardware this project already has — but each should be carried
forward as a named, open risk rather than resolved by assumption at the
product or architecture stage.

**Next stage gate:** per [CLAUDE.md](../../../CLAUDE.md) §2, product scoping
in `docs/02-product/` may proceed on the research completed so far. The
questions in [§7.1](#71-questions-answerable-only-by-the-deploying-force--block-architecture-outright)
must be carried forward as open risks, and what cameras actually exist and
what network actually exists should be treated as **blocking** for
architecture, not merely open.

**Known weaknesses of this research pass:** nothing was benchmarked hands-on
beyond what the existing rig already demonstrates; NIST IR 8173 was not
retrieved in full; the IEC 62676-4:2025 figures rest on a vendor summary;
several accuracy figures are self-reported by the authors of the methods
being measured and are treated here as upper bounds, not deployment
expectations; and the `[T38]` observations are a single consumer-grade
device, not a survey of the target estate.

---

## 9. References

Reliability key: **P** = primary standard, specification or government
publication; **A** = academic or peer-reviewed; **V** = vendor or trade
(interest-conflicted); **M** = measured in this repository.

| ID | Source | Type | URL |
|---|---|---|---|
| T1 | IETF RFC 7826 — *Real-Time Streaming Protocol Version 2.0* (obsoletes RFC 2326) | P | https://www.rfc-editor.org/rfc/rfc7826.txt |
| T3 | ONVIF — *Profiles* overview | P | https://www.onvif.org/profiles/ |
| T4 | ONVIF — *Profile S Deprecation Q&A* | P | https://www.onvif.org/profiles/profile-s/profile-s-deprecation-qna/ |
| T5 | ONVIF press release / trade coverage — end of Profile S support, 9 Oct 2025; conformance closes 31 Mar 2027 | P + V | https://www.onvif.org/?post_type=pressrelease&p=8621 |
| T6 | ONVIF — *Profile M* (analytics, metadata, MQTT) | P | https://www.onvif.org/profiles/profile-m/ |
| T7 | ONVIF — *Profile G* (edge storage and retrieval) | P | https://www.onvif.org/profiles/profile-g/ |
| T8 | IEC/EN 62676-4:2015 DORI pixel densities, via Axis pixel-density white paper and standard summaries | P + V | https://whitepapers.axis.com/en-us/pixel-density-based-on-iec-62676-4-2014 |
| T9 | JVSG — *IEC/EN 62676-4:2025 OODPCVS support* (Validate at 500 px/m) — vendor summary; verify against the standard | V | https://www.jvsg.com/iec-62676-4-oodpcvs/ |
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
| T23a | NIST — *Face in Video Evaluation (FIVE)* programme page; NIST IR 8173 — full report not retrieved (size limit) | P | https://www.nist.gov/programs-projects/face-video-evaluation-five |
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
| T38 | This repository — [`dvr.py`](../../../dvr.py): behaviour of a Hi-Focus / Dahua HD-XVR-4801H1-H established by testing (TCP-only RTSP, socket timeout, 1080N 960×1080 anamorphic, 12288 kbps / 120 fps total across 8 channels, 25 fps on ch1 only, silent config discard, percent-encoded credentials) | M | [`dvr.py`](../../../dvr.py) |

### Internal cross-references

| Document | Used for |
|---|---|
| [problem.md](../../00-project/problem.md) | The eight named capabilities and the no-dedicated-hardware constraint |
| [domain-research.md](../domain/domain-research.md) | Nuisance alarms, environment, bandwidth, evidence law, DORI, i-LIDS, ONVIF sunset |
| [ssb-operational-context.md](../domain/ssb-operational-context.md) | Road access, power, connectivity, command ranks, open border, existing FRS/ANPR procurement, evidence chain |
| [competitive-landscape.md](../competitors/competitive-landscape.md) | Capability claims, deployment patterns, hardware dependencies, ONVIF compatibility reality, bandwidth figures, egress fragmentation, published gaps |

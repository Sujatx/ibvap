# Competitive Landscape — Global Video Surveillance & Intelligent Video Analytics

**Stage:** 01 — Research → Competitors
**Date:** 2026-08-24
**Scope:** The global market for video management software (VMS), video content
analytics (VCA) and AI-driven video surveillance platforms — what exists, what
it depends on, what it costs, and where it does not reach.

> **This document does not decide what IBVAP will build.** It records what the
> market already does, on what evidence, and where the evidence runs out.
> No gap identified here is a product requirement. Product scoping happens in
> `docs/02-product/`, per [CLAUDE.md](../../../CLAUDE.md).

---

## How to read this document

### Evidence labels

Per [CLAUDE.md](../../../CLAUDE.md) §3.7, every substantive statement is
labelled:

| Label | Meaning |
|---|---|
| **FACT** | Verifiable and sourced. The source is cited as `[Cn]`. |
| **ASSUMPTION** | Believed true but not verified against a source. |
| **UNKNOWN** | Identified gap. Nobody on this project knows this yet. |

A statement labelled **FACT** is a fact *about what the cited source says*.
Almost every source in this document is a **vendor** describing its own product.
Vendor capability claims are recorded as facts about the claim, never as facts
about real-world performance. Where a source is independent (standards body,
peer-reviewed, government, trade press, or a competitor of the vendor described)
this is noted inline.

### Scope labels

Per [CLAUDE.md](../../../CLAUDE.md) §4, IBVAP is not India-specific. Findings
here that could be mistaken for universal are additionally tagged:

| Tag | Meaning |
|---|---|
| **[SIH/SSB]** | True only for this problem statement or this force. |
| **[BORDER]** | True for border/frontier surveillance generally, any country. |
| **[GLOBAL]** | True for intelligent video analytics on existing CCTV anywhere. |
| **[MARKET:xx]** | Legal, procurement or regulatory factor specific to a market. |

Untagged findings are **[GLOBAL]** by default.

### Source retrieval notes for this pass

- Several vendor PDFs (Milestone comparison chart, Genetec system requirements,
  Verkada Command Connector FAQ, Axis ACAP white paper) were retrieved and text
  was extracted locally. These are the **strongest** sources in this document —
  they are primary vendor engineering documentation with concrete numbers.
- **Pricing is largely undocumented publicly.** Genetec, Milestone, BriefCam,
  Avigilon, Videonetics, Ipsotek and AllGoVision do not publish list prices.
  Verkada is the notable exception. Third-party price estimates are marked
  low-confidence and are **not** treated as fact.
- Analyst market-share data (Omdia, Novaira Insights) sits behind paywalls. Only
  the headline claims visible in public summaries are recorded, and they are
  marked as such.
- **No independent, standardised accuracy benchmark for any of these products
  was retrieved in this pass.** IPVM publishes tests but is paywalled. This is
  the largest evidence weakness in this document — see
  [§11](#11-unknowns-requiring-further-research).

---

## 1. Market overview

### 1.1 Size and growth

**FACT** — Public market-research estimates for the **video surveillance**
market (hardware + software) diverge widely, which is itself the finding:

| Source | 2025 base | Forecast | CAGR |
|---|---|---|---|
| MarketsandMarkets `[C45a]` | USD 56.11 bn (2025) | USD 88.06 bn by 2031 | 7.8% |
| The Business Research Company `[C45b]` | USD 69.09 bn (2025) | USD 116.23 bn by 2030 | 10.9% |
| Fortune Business Insights `[C45c]` | USD 83.71 bn (2025) | USD 261.65 bn by 2034 | 13.5% |

**FACT** — Estimates for the narrower **video analytics** segment:
Grand View Research puts it at USD 12.71 bn (2024) → USD 37.84 bn by 2030 at
19.5% CAGR `[C45d]`; Mordor Intelligence puts it at USD 12.39 bn (2025) →
USD 33.74 bn by 2030 at 22.18% CAGR `[C45e]`.

**ASSUMPTION** — The absolute numbers are not usable for planning; the
**consistent direction** is. Every independent estimator has analytics growing
roughly twice as fast as surveillance overall. *(Basis: the three surveillance
CAGRs cluster 8–13%, the two analytics CAGRs cluster 19–22%.)*

**UNKNOWN** — The size of the specific segment IBVAP would sit in: *software
analytics retrofitted onto an existing third-party camera estate*, as distinct
from analytics bundled with new cameras or new VMS. None of the public
summaries break this out.

### 1.2 Who the analysts say leads

**FACT** — Omdia publishes a *Video Surveillance & Analytics Market Share
Database* segmented by World, World-excluding-China, EMEA, Americas, China and
Rest of Asia & Oceania `[C46a]`. The segmentation itself is evidence that
**China is treated as a separate market** by the industry's principal analyst.

**FACT** — Verkada states it is ranked #1 worldwide in VSaaS by Omdia on global
market share `[C46b]`. *(Vendor citing a paywalled analyst report — recorded as
a claim, not verified.)*

**FACT** — Videonetics states it is "India's #1 VMS provider" and top-10 in Asia
for seven consecutive years `[C25a]`. *(Vendor claim, source of ranking not
stated.)*

**UNKNOWN** — Actual revenue-based market shares for Genetec, Milestone,
Hanwha, Bosch, Axis, Avigilon, Hikvision and Dahua. The Omdia and Novaira
databases that hold this are paywalled `[C46a][C46c]`.

### 1.3 Structural shape of the market

**FACT** — Canon owns **Axis Communications**, **Milestone Systems** and
**BriefCam** `[C13a][C13b]`. BriefCam was acquired by Canon on 3 July 2018
`[C13a]` and, since 2024, operates as an integrated product inside Milestone
`[C13b][C13c]`. *(The consolidation report is IPVM, an independent trade
outlet.)*

**FACT** — Motorola Solutions owns **Avigilon**, **Pelco** and **Calipsa**
`[C30a][C30b]`; Calipsa was acquired in 2021 `[C30b]`.

**FACT** — Ipsotek is "an Eviden business" — i.e. part of the Atos group
`[C27a]`.

**FACT** — Eagle Eye Networks acquired the Indian analytics company **Uncanny
Vision** on 30 September 2021, retaining all 60 employees and opening a
Bangalore R&D office; Uncanny's core product was an ANPR engine `[C34]`.

**FACT** — Network Optix acquired the Dutch edge-AI startup **Scailable** in
January 2024, which became **Nx AI Manager** `[C31b]`.

**ASSUMPTION** — The market is consolidating into a small number of
**camera-plus-VMS-plus-analytics conglomerates** (Canon, Motorola, Bosch,
Hanwha, Hikvision/Dahua) plus a thinner layer of independent analytics vendors
that survive by being VMS-agnostic. *(Basis: the five acquisitions above, all
within eight years, all analytics-into-platform.)*

**ASSUMPTION** — This matters to IBVAP because it means "integrate with the
VMS" is a moving target: the VMS vendor is frequently also the analytics
competitor. *(Interpretation.)*

---

## 2. Global competitors

Each profile below answers the same question set: what it ingests, what it
detects, where it computes, what it depends on, how it is bought, and how hard
it is to deploy. Where a question has no public evidence, it says so.

### 2.1 Genetec — Security Center

**Position:** Unified enterprise platform. Video (Omnicast) + access control
(Synergis) + ALPR (AutoVu) + analytics (KiwiVision) in one product line.

**FACT** — Security Center is described by Genetec as "a truly unified platform
that blends IP video surveillance, access control, automatic license plate
recognition, intrusion detection, and communications within one intuitive and
modular solution", built on a role-based distributed architecture: Directory
(authentication/config), Archiver (recording), Media Router / Media Gateway
(stream distribution), expansion servers, and Federation for multi-site `[C5]`.

**FACT — server capacity, from Genetec's own sizing guide `[C4]`:**

| Server type | Minimum profile | Recommended profile |
|---|---|---|
| Directory & Archiver (video only) | 50 cameras / 50 Mbps | 100 cameras / 200 Mbps |
| Standalone Archiver (video only) | 75 cameras / 75 Mbps | 300 cameras / 500 Mbps |
| Standalone Redirector | 50 cameras / 50 Mbps | 475 cameras / 475 Mbps |
| Directory + Archiver + Access Manager | 50 cameras / 50 Mbps + 64 readers | 100 cameras / 200 Mbps + 200 readers |

The "Recommended" profile is an Intel Xeon Silver 4210 2.2 GHz class server
`[C4]`. Above 500 cameras Genetec directs the buyer to its own **Streamvault**
rackmount appliances (2000/4000/7000 series, 500-1,000 cameras or
500-2,000 Mbps) `[C4]`.

**FACT — deployment constraints stated by Genetec `[C4]`:**

- "Systems above 300 cameras, 1000 readers, or 300 HID Edge readers, must
  isolate the Directory on a dedicated server."
- "Software motion detection can reduce the maximum capacity by as much as 50%."
- "A virtual machine with the same specifications as its physical counterpart
  has 20% less capacity."
- The **first** Fusion Stream encryption certificate on an Archiver cuts its
  capacity by **30%** (300 cameras to 210); 20 certificates cut it to 96.
- Do not host Media Gateway or Privacy Protector on the same server as an
  Archiver.
- Requires **Windows** (Windows 10/11 Pro or Windows Server 2016/2019/2022) and
  **Microsoft SQL Server** `[C4]`.

**FACT — analytics.** KiwiVision is Genetec's analytics module set: Security
video analytics (area protection, perimeter intrusion, object detection,
direction control), Privacy Protector (dynamic anonymisation of people in live
and recorded video, with authorised un-masking), People Counter, and Camera
Integrity Monitor (tampering/obstruction/failure detection) `[C6a][C6b]`.

**FACT — KiwiVision hardware requirements, from Genetec `[C4]`:**

- "Due to typically high-performance requirements, using virtual machines is not
  recommended."
- Every server running KiwiVision Manager, Analyzer or Config Tool "requires an
  **AVX compatible processor**".
- **"GPU support is only available for the Tailgating detection and People
  counting scenarios."** A 4 GB+ CUDA-capable NVIDIA card and a separate
  "KiwiVision Analyzer GPU Pack" are required, enabled per role.
- Genetec supplies a *KiwiVision Camera Requirements Calculator* to "verify
  whether your existing camera setup needs to be modified."

**This last point is the single most important Genetec finding for IBVAP.**
Genetec's own tooling assumes that adding analytics to an existing camera estate
may require **changing the cameras**. `[C4]`

**FACT — ALPR.** AutoVu's ALPR Manager role is sized in "AutoVu camera units":
50 units (minimum profile), 100 (recommended), up to 300 across three ALPR
Managers, with the constraint that "the total number of AutoVu units on all ALPR
Managers connected to the same Archiver cannot exceed 100" `[C4]`. AutoVu Sharp
and SharpX are Genetec's own purpose-built ALPR cameras `[C7c]`.

**FACT — but** Genetec also ships **AutoVu Flexreader**, announced April 2018, a
software add-on that turns existing fixed IP cameras supported by Security
Center into plate readers feeding the normal AutoVu workflows, "without
dedicated ALPR hardware" `[C7a][C7b]`. It is stated to be **optimised for
vehicles moving up to 30 mph / 50 km/h** `[C7b]`.

**FACT — cloud/edge.** Genetec sells **Cloudlink** appliances (210, 310, 2210),
cloud-managed Linux appliances that "push processing and storage to the edge",
explicitly addressing "support for existing devices that do not enable
direct-to-cloud connectivity, and the need to maintain local operation during
connectivity disruptions" `[C8a][C8b][C8c]`. Security Center SaaS is the
hybrid-cloud offering `[C8d]`.

**FACT — cloud bandwidth requirement.** For Genetec Cloud Storage, "your network
must provide a guaranteed uplink that is **30% greater than the video throughput
recorded by all Archiver roles**", with 99.9%+ SLA availability and <150 ms
latency to an Azure data centre `[C4]`. One Archiver recording 100 Mbps needs
130 Mbps of guaranteed uplink.

**FACT — licensing.** Genetec does not publish list pricing. Third-party
estimators put Omnicast video licences at ~USD 150-400 one-time per channel plus
an annual **Software Maintenance Agreement (SMA)** of 18-22% of licence value,
and Streamvault appliances at USD 8,000-30,000+ per site `[C9]`.
*(Third-party, competitor-adjacent estimates — **low confidence**, recorded to
show the shape of the model, not the numbers.)*

**FACT** — Genetec claims to be "the only VMS vendor in the world to hold UL
cybersecurity certification" (2020) `[C57]`. *(Vendor claim; time-bound.)*

**FACT — deployment complexity.** Genetec runs certification training; the
Security Center SaaS VMS Administrator certification is a 4-hour self-paced
course, and IPVM's comparison puts Genetec classroom training at 2 days for
USD 595-895 `[C51]`.

### 2.2 Milestone Systems — XProtect

**Position:** The reference "open platform" VMS. Camera-agnostic by design;
object analytics supplied by third parties or by BriefCam.

**FACT — editions and limits, from the XProtect 2026 R1 comparison chart `[C1]`:**

| | Express+ | Professional+ | Expert | Corporate |
|---|---|---|---|---|
| Deployment | Single server | Centrally managed multi-server | Centrally managed multi-server | Centrally managed distributed sites |
| Licensing | Perpetual | Perpetual | Perpetual | Perpetual |
| Max IP devices per recording server | **48** | Unrestricted | Unrestricted | Unrestricted |
| Recording servers per system | **1** | Unrestricted | Unrestricted | Unrestricted |
| Edge Storage + Scalable Video Quality Recording | no | yes | yes | yes |
| Media DB encryption and digital signing | no | no | yes | yes |
| Evidence Lock | no | no | no | yes |
| Federated Architecture | no | no | Remote site | Central/Remote |
| Interconnect | Remote site | Remote site | Remote site | Central/Remote |
| Hardware-accelerated VMD (NVIDIA) | no | no | yes | yes |
| Multicast | no | no | yes | yes |
| GDPR ready | no | no | yes | yes |

("Unrestricted" is qualified in the source as "depending on system
configuration".)

**FACT — device openness `[C1]`:** ONVIF and PSIA support in every edition; a
**Milestone universal driver** for generic devices; **11,000+ supported IP
devices**; metadata from camera embedded analytics ingested in every edition.
Milestone separately states conformance with ONVIF profiles **S, T, G and M**,
16,500+ devices on the supported device list, and 1,000+ tested ONVIF devices on
a single optimised driver `[C2][C3]`. Device packs ship every two months `[C2]`.

**FACT — integration surface `[C1]`:** every edition, including the 48-camera
entry edition, includes MIP SDK plug-in/protocol/component integration, system
configuration via MIP SDK **and REST API**, live and playback streaming via
**WebRTC**, event and alarm integration via MIP SDK / REST API / **WebSocket**,
a driver framework for new devices, **webhooks**, and **Milestone AI Bridge for
Intelligent Video Analytics integrations**.

**FACT** — Milestone AI Bridge "acts as a bridge between installations of
XProtect VMS and Intelligent Video Analytics (IVA) applications **deployed as
docker containers**", forwarding camera streams from XProtect to the IVA
application and accepting events, metadata and video back into XProtect `[C47]`.

**This is a formal, documented, container-based ingress for third-party
analytics into the largest open VMS.** `[C47]`

**FACT — offline operation `[C1]`:** "Offline license activation" and
"Add/replace devices without reactivation in offline systems" are supported in
**every** edition, including the 48-camera Express+.

**FACT — ALPR.** XProtect LPR is a licensed extension. Milestone states it
"works with all variants of XProtect as well as all cameras supported by
XProtect... **With XProtect LPR you do not need a purpose-built LPR camera**",
recommends mounting the camera looking down on the vehicle at no more than 30
degrees, ships 200+ generic and country-optimised modules with 5 country
licences in the base licence, and warns that "the system requirements for the
license plate recognition logic is processor intensive, and varies significantly
dependent on the environmental conditions, camera settings and other
parameters" `[C53]`.

**FACT — analytics.** XProtect itself ships built-in **Video Motion Detection**
with auto-adjustable sensitivity, exclusion zones and motion metadata `[C1]` —
motion, not object classification. Object-level analytics come from BriefCam
(now a Milestone product) or third parties via MIP / AI Bridge.

**FACT** — "XProtect Rapid REVIEW" is marked **Discontinued** in all four
editions in the 2026 R1 chart `[C1]`. *(Rapid REVIEW was the BriefCam-derived
extension; its discontinuation coincides with BriefCam's absorption into
Milestone `[C13b]`.)*

**FACT** — Milestone reported net revenue of USD 340 million in 2025 and states
it formally integrated BriefCam analytics and Arcules VSaaS into Milestone in
2025 `[C58]`.

**FACT — cloud.** Milestone Kite / Arcules is the VSaaS line, marketed for
"multiple satellite and remote locations", with "flexible hybrid video storage
with low bandwidth needs, where video data can be stored in the cloud or at the
edge, all dependent on available bandwidth" `[C48a][C48b]`. XProtect 2025 R1
extended the Arcules connection to Corporate, Expert and Professional+ `[C48c]`.

**UNKNOWN** — Milestone's actual per-device licence price and Milestone Care
subscription cost. Not published.

**FACT — deployment complexity.** IPVM's comparison lists Milestone Advanced
training at 3 days for USD 2,995 `[C51]`.

### 2.3 BriefCam (Canon / Milestone)

**Position:** The best-known **VMS-agnostic video content analytics** product —
the closest existing analogue to "software that makes an existing CCTV estate
intelligent".

**FACT — modules `[C10]`:** REVIEW (VIDEO SYNOPSIS: "superimpose objects on a
stationary background, simultaneously displaying events" for rapid forensic
review), RESEARCH (business-intelligence dashboards), RESPOND (real-time
alerting on face recognition, vehicles, and behavioural rules).

**FACT — VMS relationship `[C10][C11]`:** BriefCam is "VMS-agnostic but
integrates with supported systems via direct connectors", supports federated
architectures, and "includes a generic **Video Integration API** for unsupported
systems". The supported-VMS list covers 30+ platforms with a tiered integration
model: **L1** forensic/post-event, **L2** real-time, **L2a** real-time alerts,
**L3** client/UI integration, **L4** workflow integration. Milestone XProtect is
the only **L4**; Genetec Security Center is **L3**; Bosch BVMS, Nx Witness,
Qognify Ocularis and Avigilon Unity are **L2/L2a** `[C11]`.

**The tiering is the finding: "integrates with 30+ VMS" does not mean the same
thing 30 times.** `[C11]`

**FACT — hardware `[C10]`:** NVIDIA GPUs are **mandatory** ("Intel, AMD or any
other non-NVIDIA GPUs not supported" per the hardware brief `[C10b]`); the
required GPU count depends on video resolution and daily hours to process;
multiple GPUs can be installed but **each GPU is dedicated to either real-time
or on-demand processing, not both**. Virtual machines are "technically possible
but not recommended for production".

**FACT — video constraints `[C10]`:** minimum resolution CIF (352x240), native
maximum 4K (3840x2160); 8-30 FPS recommended, outside that range "supported with
degraded tracking"; minimum object size **12-32 pixels** depending on object
class.

**FACT — licensing `[C10]`:** one-time purchase, not subscription; annual
maintenance optional after year one; four variants (Investigator, Insights,
Rapid Review, Protect); expansion licences for concurrent users, RESEARCH users
and camera channels; **licensed per camera sensor** — a multi-sensor camera
consumes multiple licences.

**FACT — multi-site `[C12]`:** **BriefCam Nexus** is a hub-and-site
architecture. Each Site processes local video in real time or on demand; the
central **Hub** "aggregates RESPOND alerts and RESEARCH metadata generated at
each Site". The description of the pattern is explicit: "a central server and
then you have a hub at each site processing the video locally, and then just
sending the metadata back centrally" `[C12b]`.

**This is the architectural pattern most relevant to distributed, bandwidth-poor
estates, and a major incumbent already ships it.** `[C12]`

**UNKNOWN** — BriefCam list pricing. Not published anywhere retrieved.

### 2.4 Axis Communications

**Position:** Camera manufacturer whose analytics strategy is **on-camera and
Axis-only**.

**FACT** — ACAP (AXIS Camera Application Platform) is Axis's edge application
ecosystem. It requires Axis chipsets — **ARTPEC** SoCs with a **DLPU** (deep
learning processing unit) or **MLPU** (machine learning processing unit).
**ACAP applications cannot run on non-Axis cameras** `[C14]`.

**FACT** — AXIS Object Analytics is preinstalled on compatible Axis cameras,
detects and classifies **humans, vehicles and vehicle types**, and requires
firmware 10.2+ on compatible MLPU cameras `[C15a][C15b]`. Scenario types:
*Object in area*, *Line crossing*, *Time in area*, *Crossline counting*,
*Occupancy in area*; maximum **10 scenarios with trigger conditions** per camera
`[C15c][C15d]`.

**FACT** — Axis states the edge-analytics benefit as bandwidth reduction and
reduced central server cost, because analysis happens locally `[C14]`.

**FACT — the pixel-density constraint.** Axis publishes a white paper on pixel
density and DORI `[C16]`. DORI (IEC EN 62676-4:2015) defines
**Detection 25 px/m, Observation 62 px/m, Recognition 125 px/m,
Identification 250 px/m** `[C49]`.

**This is a physics-level constraint that binds every vendor equally, including
IBVAP: an existing camera that yields 40 px/m on a target cannot support face
identification no matter whose software reads it.** `[C49]`

**ASSUMPTION** — Axis is a *camera* competitor rather than a platform
competitor, but it is the most important dependency-shaper in the market: an
estate of ARTPEC cameras already has classification analytics on board, and an
estate of anything else does not. *(Basis: `[C14][C15]`.)*

### 2.5 Avigilon (Motorola Solutions)

**Position:** Camera + VMS + analytics, in two product lines — **Unity**
(on-premise, formerly ACC) and **Alta** (cloud-native, formerly Ava).

**FACT** — Avigilon states Unity Video "is compatible with any ONVIF compliant
device" `[C17]`.

**FACT** — Appearance Search allows locating a person or vehicle "using a
physical description, uploaded image, or previous recorded footage"; LPR
Analytics automates plate reading `[C17][C18a]`.

**FACT — camera constraints for cloud LPR `[C18b]`:** Alta Video LPR "requires
the use of a dome or bullet-type of camera, and cannot be configured to use
panoramic, 360, fisheye, or PTZ cameras". Third-party dome/bullet cameras are
supported via **Alta Cloud Connectors**.

**FACT — an ecosystem-lock artefact `[C19]`:** to use an Avigilon Alta
cloud-native camera with a third-party VMS via ONVIF, "you will need to load the
camera with Avigilon Unity firmware which is available from Avigilon technical
support" — i.e. ONVIF output from their own cloud camera requires a firmware
swap obtained through support.

**UNKNOWN** — Which specific Unity analytics (Appearance Search, unusual motion
detection, classification) function on third-party ONVIF cameras versus
requiring Avigilon H4/H5/H6 cameras. The public supported-devices page does not
state this `[C17]`; it directs buyers to sales engineering.

### 2.6 Verkada

**Position:** Proprietary hybrid-cloud. Cameras, storage and cloud are one
vertically integrated product — with a bridge appliance for third-party cameras.

**FACT — bandwidth, the standout claim `[C21]`:** Verkada cameras consume
"a bandwidth uplink of **no more than 20 kbps per camera**" in steady state,
sending "a constant metadata stream consisting of encrypted thumbnail images,
related metadata (including analytics) to the cloud approximately **once every
20 seconds**". Video streams only when a user requests it: **~300 kbps** for
720p SD viewing, **~1 Mbps** for full-resolution HD. Verkada claims "over 100
cameras on the same connection (~only 2 Mbps)".

**FACT** — cameras "store up to **30-365 days** of continuous video on the
device itself" `[C21][C22]`, continuing to record during internet outages
`[C22]`.

**This is the strongest documented low-bandwidth architecture in the market —
and it is achieved by owning the camera.** `[C21][C22]`

**FACT — third-party support via Command Connector, with published prices
`[C20]`:**

| Model | Onboard storage | Channels (5MP or less) | Channels (4K) | Price (USD) |
|---|---|---|---|---|
| CC300-4TB | 30 days | 10 | 5 | 2,999 |
| CC300-8TB | 60 days | 10 | 5 | 3,499 |
| CC500-8TB | 30 days | 25 | 12 | 5,499 |
| CC500-16TB | 60 days | 25 | 12 | 6,499 |
| CC700-16TB | 30 days | 50 | 25 | 8,499 |
| CC700-32TB | 60 days | 50 | 25 | 10,499 |

Plus "a licence for each non-Verkada camera channel feed running through Command
Connector... offered on a per-channel basis, available in 1, 3, 5 or 10-year
intervals, and cost the same as existing Command video security licences"
`[C20]`.

**FACT — the third-party camera caveats, verbatim from Verkada's own FAQ
`[C20]`:**

- Q6, "Do cameras that operate through Command Connector receive the same
  features and capabilities as native Verkada devices?" -> **"No."**
- Compatibility is governed by a **Hardware Compatibility List (HCL)**. A camera
  not on the HCL "may work", but "compatibility is not guaranteed" and
  **"Verkada will not be able to provide support"**.
- Getting a camera added requires a **Request for Compatibility Assessment**,
  which "can take anywhere from **weeks to months**"; expediting requires
  shipping Verkada the camera, which Verkada then keeps.
- **"Command Connector currently only supports H.264 video encoding."**
- Max **20 RTSP channels** per Command Connector (for non-ONVIF cameras).
- **"Command Connector does not currently utilize any events emitted by
  non-Verkada cameras."**
- Customers "do not currently have the ability to set custom video
  configurations" on non-Verkada cameras.
- **Thermal:** "the thermal video channels are visible in Command. **People and
  vehicle analytics features are only supported on visible (or non-thermal)
  video streams.**"
- Command Connector "does not integrate with other VMS or NVR appliances";
  running alongside a legacy VMS works "only if the underlying camera devices
  support streaming video to two separate NVRs".
- Air-gapped camera networks are explicitly accommodated: the second Ethernet
  port connects to an "isolated or airgapped camera network" while the primary
  port reaches the internet `[C20]`.

**The thermal exclusion is directly material to night-time analytics
[BORDER]: the leading cloud platform runs no person/vehicle analytics on thermal
streams at all.** `[C20]`

### 2.7 i-PRO (formerly Panasonic Security)

**Position:** Edge-AI camera manufacturer plus server-side aggregation
(Active Guard) plus its own VMS (Video Insight).

**FACT** — i-PRO's edge AI solution "requires **i-PRO network cameras with AI
capabilities**"; the documentation "does not indicate compatibility with non-i-PRO
cameras" `[C23]`.

**FACT** — Active Guard "operates on metadata and imagery from Edge AI cameras",
using "metadata information from i-PRO Edge AI cameras" and "best images"
`[C23]`. Active Guard 3.0 adds a server-based generative-AI engine that
interprets natural-language queries over best-shot images with metadata from
i-PRO AI camera models `[C24]`.

**FACT — stated analytics `[C23]`:** face, human, vehicle and bicycle detection;
AI-based VMD with line-cross, loitering and directional detection; sound
classification (gunshot, scream, glass break); AI privacy guard (real-time
mosaic over faces); occupancy/crowd congestion; scene-change detection with
on-site learning; smart coding for bandwidth reduction.

**FACT** — Active Guard integrates with Genetec Security Center, Milestone
XProtect, Luxriot EVO, Network Optix Nx Witness and i-PRO Video Insight
`[C24][C23]`.

**ASSUMPTION** — i-PRO is the clearest example of the industry's dominant
commercial pattern: **the analytics are the reason to buy the cameras**. The
server software is deliberately valueless without the vendor's own edge
hardware. *(Basis: `[C23]` — Active Guard consumes camera-produced metadata and
best-shots, not raw video.)*

### 2.8 Bosch and Hanwha Vision (edge-analytics camera vendors)

**FACT** — Hanwha's Wisenet 9 SoC "features dual neural processing units, with
one NPU handling image processing while the other focuses on object detection
and advanced analytics", running "complex image processing on the edge to reduce
latency and bandwidth needs, allowing cameras to filter events before they leave
the device" `[C37a][C37b]`. **WiseDetector** is a machine-learning feature that
"expands the object types that can be detected by AI to specific objects beyond
pre-defined ones" `[C37a]`.

**FACT** — Bosch IVA Pro is Bosch's edge video analytics line `[C38]`.
*(Weakly sourced in this pass — trade commentary, not Bosch primary
documentation. See [§11](#11-unknowns-requiring-further-research).)*

**ASSUMPTION** — Bosch and Hanwha occupy the same structural position as Axis
and i-PRO: analytics as a camera differentiator, not as a portable software
product. *(Basis: `[C37]`; Bosch not verified.)*

### 2.9 Ipsotek (Eviden / Atos)

**Position:** VMS-agnostic analytics explicitly positioned on **existing CCTV**.

**FACT** — Ipsotek VISuite is "an AI-powered video analytics platform,
leveraging existing CCTV cameras for real-time security and operations", serving
a claimed 600+ customers over 20+ years `[C27b]`.

**FACT** — Its core is a **patented Scenario-Based Rule Engine (SBRE)**, "a
powerful tool to precisely define behaviours of interest as they would unfold in
the real-world dynamic and complex environment" `[C27b]`.

**FACT** — **VISuite Core** (2025) is "a new AI-Video Analytics solution built
around a carefully curated set of pre-built capabilities designed to address
high-value use cases across large-scale deployments", enabling value from
existing video infrastructure "through a repeatable, plug-and-play deployment
model suited to distributed estates and partner-led rollouts" `[C27a]`.

**The existence of VISuite Core is evidence that a 20-year incumbent found its
own general-purpose platform too hard to deploy at scale and shipped a
narrowed, pre-built variant to fix it.** `[C27a]`

**FACT** — Ipsotek VISuite AI is listed as a Milestone technology partner
covering video analytics, face recognition, licence plate recognition and
forensics `[C27c]`.

**UNKNOWN** — Ipsotek's hardware requirements, licensing model, and pricing.
Not published in anything retrieved.

### 2.10 Irisity (IRIS+)

**Position:** Open-platform, camera-agnostic analytics with an unusually
explicit deployment matrix.

**FACT** — "IRIS+ is an Open Platform for AI video analytics and therefore works
with **any type of camera brand and model**", using **RTSP/ONVIF**, "including
analog cameras via DVRs" `[C29a][C29b]`.

**FACT — deployment options stated `[C29a][C29b]`:** on-premise **(including
air-gapped)**, cloud-hosted (managed by Irisity), hybrid, and edge (on-camera
analytics). Hardware platforms: "x86 with NVidia GPU or AI cameras". Claimed
scaling: "from small 5-10 camera installations to multi-site, multi-tenant...
supporting thousands of cameras".

**Irisity is the only vendor found in this pass that states air-gapped operation
as a first-class supported deployment mode.** `[C29b]`

**UNKNOWN** — Irisity's per-camera pricing and its measured accuracy.

### 2.11 Calipsa (Pelco / Motorola Solutions)

**Position:** Pure-cloud **false-alarm filtering** layered on any existing IP
camera. Narrow scope, deliberately.

**FACT** — Calipsa's "cloud-based technology allows customers to add AI to
existing IP-based cameras **without additional hardware**", is "100% cloud-based
platform, with no additional hardware required", and is "cloud agnostic",
applicable to any CCTV brand `[C30c][C30d]`.

**FACT — the bandwidth mechanism `[C30c]`:** "Unlike other solutions we analyze
**frames, not video**... it takes about **300 Kb of bandwidth per event**, so
bandwidth consumption will be very minimal."

**FACT — claimed performance `[C30c][C30d]`:** reduces unwanted alarms "by up to
95%" / "by 93% - with 99% accuracy at spotting alarms containing people and
vehicles". *(Vendor claim. No methodology, dataset or independent verification
retrieved.)*

**Calipsa is the clearest existing proof that a commercially viable product can
be built on event frames rather than video streams.** `[C30c]`

### 2.12 Eagle Eye Networks

**Position:** Open cloud VMS ("VSaaS") with an on-site bridge, for existing
analog and IP cameras.

**FACT** — Some Eagle Eye bridges "support both analog and IP cameras on the
same device, with analog cameras connecting directly to the bridge without
external encoders" via BNC `[C33a]`.

**FACT** — "The Bridge records video and audio initially to the local storage on
the device, which is necessary for buffering the video and backing up the latest
files in case the internet connection fails", synchronising to cloud "when
bandwidth is available" `[C33a][C33b]`.

**FACT — bandwidth `[C33a]`:** Eagle Eye recommends **400 kbps per IP camera**
as a starting point, with third-party guidance citing 1-2 Mbps per HD camera and
2-4 Mbps per 4K camera. *(The two figures come from different sources and are
not reconciled; the 400 kbps figure is Eagle Eye's own.)*

**FACT** — Eagle Eye acquired **Uncanny Vision** (Bangalore) in 2021, whose core
product was an ANPR engine claimed to "consistently deliver very high accuracy
even in challenging conditions" `[C34]`.

### 2.13 Network Optix (Nx Witness / Nx Meta / Nx AI Manager)

**Position:** A *platform for building* video products, not only a product.
Structurally different from every other entry here.

**FACT** — Nx Meta "is an IP video management platform that allows users to
discover, stream, configure and manage IP cameras, **RTSP streams**, and I/O
devices" `[C31a]`.

**FACT — openness `[C31c][C31d]`:** the `nx_open_integrations` and `nx_open`
repositories are published on GitHub under **Mozilla Public License 2.0**; the
Nx Desktop client is open source; "anyone including Systems Integrators, End
Users, and third-party developers can use it". A **TestCamera** tool emulates a
network camera so integrations can be developed without hardware or a licence
`[C31e]`.

**FACT — licensing `[C31f]`:** both **perpetual** (Pro) and **recurring**
(Enterprise) licences exist.

**FACT — Nx AI Manager `[C31b]`:** a plugin that runs AI/ML models on edge
devices (routers, gateways, IPCs, smart cameras) against live video, supports
"GPU, VPU, and CPU environments", imports models "from virtually any training
platform", and supports **OTA mass deployment** and fleet management. It
originated as the Dutch startup Scailable, acquired January 2024.

**Network Optix is the closest thing in the market to an *ingredient* rather
than a *competitor* — and therefore also the fastest route for anyone else to
build a competing product.** `[C31]`

### 2.14 Ambient.ai

**Position:** Premium enterprise "intelligence layer" on existing cameras.

**FACT** — Ambient.ai is built around a vision-language model ("Ambient Pulsar")
that "reasons about video in real time to flag actual threats, not motion
events"; it "operates as an intelligence layer on top of existing camera and
access control infrastructure, with AI processing running on **edge appliances
at each site** and a **cloud console** for monitoring, multi-site management and
analytics" `[C35a][C35b]`.

**FACT** — "All we need to begin video processing is access to your IP camera
streams" `[C35b]`. Stated deployment range: ~100 to 10,000+ cameras across
multiple sites `[C35a]`.

**FACT** — Pricing is quoted per deployment, "built around camera count,
edge-appliance hardware, and the AI modules you turn on", and "sits at the
premium end of the market" `[C35a]`. *(Third-party pricing guide, not vendor —
low confidence.)*

**Ambient.ai is the market's clearest signal that vision-language models are
being commercialised for the "suspicious activity" problem that rule engines
handle badly.** `[C35a]`

### 2.15 Gorilla Technology

**Position:** Edge AI video analytics combined with VMS in a single appliance,
sold into city and national security programmes.

**FACT** — IVAR ("Intelligent Video Analytics Recorder") is "an all-in-one edge
AI surveillance solution which combines intelligent video analytics with VMS",
and "utilizes **existing CCTV video data** to effectively identify people,
vehicles, and objects, detect suspicious events" `[C36a][C36b]`.

**FACT** — Gorilla also ships **EVMS** (Edge Video Management System) and an
Edge AI line for "harsh outdoor environments" `[C36c][C36d]`. IVAR is listed on
the Milestone Marketplace `[C36e]`.

**FACT** — Gorilla cites a case reducing investigation time "from over 185 hours
to just 15" `[C36a]`. *(Vendor case study, single incident, unverified.)*

### 2.16 Perimeter-security specialists (SightLogix, Teledyne FLIR, Senstar)

Relevant because **[BORDER]** perimeter intrusion is their entire market, and
because they represent the "sensor-plus-analytics" answer the problem statement
explicitly rejects.

**FACT** — SightLogix SightSensor smart thermal cameras "detect, analyze and
communicate real-time intruder activity over perimeters and outdoor sites, using
integrated SightLogix video analytics to detect with great reliability and **low
nuisance alerts over large distances**", with "powerful edge-based AI" and
dual-sensor models combining thermal and visible AI classification `[C39a]`.

**FACT** — Teledyne FLIR's FC-Series AI is "a thermal security camera with
onboard AI analytics that accurately classifies humans and vehicles for early
intrusion detection for perimeter protection and remote site monitoring",
combining DNN- and motion-based analytics `[C40]`.

**FACT** — Senstar specialises in physical perimeter intrusion detection,
particularly fence-mounted and buried cable sensors `[C39b]`.

**ASSUMPTION** — This segment's existence is evidence that outdoor perimeter
detection at long range is **hard enough that a whole industry sells dedicated
thermal hardware to avoid doing it on general-purpose CCTV**. *(Basis: the
segment's positioning is built entirely on nuisance-alarm reduction and range,
`[C39][C40]`.)*

### 2.17 Anduril — the border-specific extreme [BORDER]

**FACT** — CBP awarded Anduril a **USD 363 million** one-year contract in
December 2025 for 200+ **Extended Range Sentry Towers**; 40+ delivered so far at
15+/month `[C41a][C41b]`.

**FACT** — The 80-foot expeditionary tower has "high-performance sensors to
autonomously detect, classify, and track objects of interest at ranges exceeding
5 miles", modular mission nodes and power sources, and "can be erected in less
than three hours" `[C41a][C41c]`.

**FACT** — "Over 350 Standard Range Sentry systems are operating today, and
these have autonomously identified hundreds of thousands of border crossings";
by late 2024 the 300th deployment covered "30 percent of the U.S. southern land
border" `[C41a][C41d]`.

**This is the reference point for what a well-funded border programme buys when
it is *not* constrained to existing infrastructure: purpose-built autonomous
towers. It is the direct inverse of the IBVAP premise — and it works.** `[C41]`

### 2.18 Open source (Frigate, and the general-purpose stack)

**FACT** — Frigate is "an open source NVR built around real-time AI object
detection, with all processing performed locally"; it supports Google Coral TPU,
Intel OpenVINO and NVIDIA GPUs; "any IP camera with RTSP works"; it uses a
dual-stream pattern (high-resolution main stream recorded, low-resolution
substream fed to detection); and it offers event-based and 24/7 recording with
object-based retention, WebRTC/MSE sub-second live view, and MQTT integration
`[C32a]`.

**FACT** — Frigate has been deployed on NVIDIA Jetson hardware with
hardware-accelerated ML `[C32b]`.

**ASSUMPTION** — Frigate defines the **credible free floor** of this market:
RTSP ingestion, on-device object detection, event recording and alerting, at
zero licence cost, on hardware costing tens to low hundreds of dollars. Any paid
product must be worth more than that difference. *(Basis: `[C32]`.)*

**UNKNOWN** — Whether Frigate or comparable open-source stacks are usable at the
multi-site, multi-user, audited, evidentiary standard a security force needs.
Nothing retrieved addresses this.

### 2.19 The newer camera-agnostic cloud entrants

**FACT** — Coram AI is described as "a cloud, camera-agnostic platform built
around large-model natural-language search that works with any IP camera with no
rip-and-replace, auto-discovering ONVIF cameras and bulk-importing RTSP
streams"; Spot AI is positioned similarly `[C54]`.

*(These descriptions come from **competitor-authored comparison content** —
Coram's own blog ranking Coram highly. Treat as evidence that the positioning
exists and is being contested, not as evidence of capability.)*

**ASSUMPTION** — "Natural-language search over any existing camera" is becoming
the standard pitch of every new entrant, so it will not be a differentiator for
long. *(Basis: `[C54]`, plus Ambient Pulsar `[C35a]` and i-PRO Active Guard
3.0's generative-AI query engine `[C24]`.)*

---

## 3. Indian competitors [MARKET:IN]

This section is **market-specific**, per [CLAUDE.md](../../../CLAUDE.md) §4. It
describes the competitive set IBVAP would meet in its initial validation market,
not the boundary of its product.

### 3.1 Videonetics

**FACT** — Videonetics markets a **Unified Video Computing Platform (UVCP)**
providing "an end-to-end solution for a wide range of surveillance
applications", comprising VMS, Video Analytics, Traffic Management System and
Face Recognition System, "powered by an indigenously developed True AI and deep
learning engine" `[C25a][C25b]`.

**FACT** — ANPR is bundled with Red Light Violation Detection and Speed
Violation Detection `[C25b]`.

**FACT** — Its Face Recognition System is stated to be "trained with a large
database of faces covering diverse demography, and **works well with facial
features of the Indian subcontinent**" `[C25b]`.

**This is the clearest instance in this research of a competitor claiming
market-specific model tuning as its differentiator — a claim IBVAP would have to
meet or beat in this market.** `[C25b]`

**FACT** — Videonetics states deployment "across all 28 districts of Andhra
Pradesh", forming a state-wide real-time intelligence network `[C25c][C25d]`. It
is an ONVIF member `[C25e]`.

**UNKNOWN** — Videonetics' hardware requirements, per-camera pricing, whether it
runs on existing third-party cameras unmodified, and whether the Andhra Pradesh
deployment used existing or newly procured cameras.

### 3.2 Matrix Comsec

**FACT** — Matrix SATATYA is an IP video surveillance portfolio (cameras, NVRs,
VMS) with a 64-bit .NET enterprise NVR with inbuilt VMS `[C26a]`.

**FACT** — Analytics claimed: "intrusion detection, human and vehicle
classification, loitering, line crossing, crowd density, object left/removed
detection, fire and smoke detection, PPE compliance, and Automatic Number Plate
Recognition (ANPR)" `[C26b]`.

**FACT** — Matrix announced a partnership with **Yotta** to deliver "Drishticam
AI Powered Cloud Native Video Surveillance as a Service (VSaaS)", with encrypted
cloud recording, configurable retention and multi-channel notifications
`[C26b][C26c]`.

**ASSUMPTION** — Matrix is primarily a **hardware** vendor extending into
analytics — structurally the same position as Hanwha or i-PRO, not a
software-only competitor. *(Basis: SATATYA is cameras and NVRs `[C26a]`; the
analytics ship with them.)*

### 3.3 AllGoVision

**FACT** — AllGoVision is a Bangalore-founded (2009) video analytics company
with presence in the UK, USA, UAE and Korea `[C28a]`.

**FACT — the important architectural claim `[C28b][C28c]`:** it "can be
installed either in the same machine as VMS or in a separate machine and **can
take video feed directly either from camera or from VMS**", is integrated with
"10+ major VMS like Milestone, Genetec, Honeywell EBI, HUS, DVM, Wavestore",
and — notably — "AllGoVision **virtual camera** is created based on ONVIF
standards and can be added in any VMS which supports ONVIF."

**The ONVIF virtual-camera pattern is worth recording: rather than writing a
plugin per VMS, the analytics engine presents its annotated output as an ONVIF
camera, which any ONVIF VMS can already consume.** `[C28c]`

**FACT** — AllGoVision claims "50 plus basic and advanced Video Analytics
features" covering intrusion detection, counting, crowd management, intelligent
traffic and face recognition, working "with existing security cameras... without
requiring specialized hardware" `[C28b][C28d]`.

### 3.4 Vehant, Staqu, Wobot, Uncanny Vision

**FACT** — **Vehant Technologies** offers "Security, Traffic Enforcement and
Sovereign Vision AI Solutions", with facilities in India and the Netherlands,
and AI-powered CCTV software that "has enabled cities to implement e-challan
systems fully integrated with government databases" `[C55a]`.

**FACT** — **Staqu** (Gurugram, 2015) offers **JARVIS**, "a software platform
that processes peripheral closed-circuit television (CCTV) footage into
insights", serving retail, manufacturing, infrastructure, hospitality, public
sector and smart cities `[C55b][C55c]`.

**FACT** — **Wobot Intelligence** (2017) provides video analytics on camera
feeds for retail, food service, manufacturing and hospitality `[C55d]`.

**FACT** — **Uncanny Vision** was acquired by Eagle Eye Networks in 2021
`[C34]` — an Indian analytics company absorbed into a US cloud VMS.

**ASSUMPTION** — The Indian analytics segment is crowded with software-only
players already claiming exactly the "AI on existing CCTV" position the problem
statement describes. *(Basis: `[C28][C55]` — five such companies surfaced
without deliberate search effort.)*

### 3.5 The Indian regulatory factor [MARKET:IN]

**FACT** — India's Ministry of Electronics and Information Technology (MeitY)
introduced **Essential Requirements for the Security of CCTV Cameras (ER-01)**
in a March 2024 Gazette notification, requiring testing and certification by
**STQC**, covering physical security, access control, network encryption, data
integrity and penetration testing, referencing OWASP 4.0 Level 2 and a Trusted
Supply Chain framework `[C43a][C43b][C43c]`.

**FACT** — The relaxation permitting sale of non-conforming cameras has been
withdrawn; from **1 April 2026** no sale of CCTV cameras not conforming to the
ERs is permitted `[C43d]`.

**FACT** — The stated background is "security concerns regarding devices using
foreign chipsets — security agencies were concerned the chipsets may have
allowed the cameras to send data to servers located outside of India" `[C43a]`.

**FACT** — At least one industry outlet argues the STQC requirement
"monopolises the CCTV industry in India" `[C43e]`. *(Trade advocacy source;
recorded as evidence that the requirement is contested, not as a finding about
its merits.)*

**ASSUMPTION** — ER-01 applies to *cameras*, not to analytics software, so it
constrains the installed base IBVAP would run on rather than IBVAP itself —
but it also means the Indian installed base will churn. *(Basis: `[C43]`
consistently describes camera certification. **Not verified** for software.)*

---

## 4. Capability comparison

Mapped against the eight capabilities named in the official problem statement
`[docs/00-project/problem.md]`. This is **not** a scorecard. It records what each
vendor *claims*, at what evidence quality, and — more importantly — **what the
claim depends on**.

Legend: **Y** = vendor claims the capability with evidence cited in this
document. **Y\*** = claimed but conditional on the vendor's own hardware.
**P** = partial / adjacent. **—** = no evidence found in this pass (not the same
as "absent").

| Capability | Genetec | Milestone | BriefCam | Axis | Avigilon | Verkada | i-PRO | Videonetics | AllGoVision | Irisity | Ipsotek | Frigate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Human detection & tracking | Y `[C6a]` | P (VMD only) `[C1]` | Y `[C10]` | Y* `[C15a]` | Y `[C17]` | Y (not on thermal) `[C20]` | Y* `[C23]` | Y `[C25b]` | Y `[C28b]` | Y `[C29a]` | Y `[C27b]` | Y `[C32a]` |
| Vehicle detection & classification | Y `[C6a]` | P | Y `[C10]` | Y* `[C15a]` | Y `[C17]` | Y (not on thermal) `[C20]` | Y* `[C23]` | Y `[C25b]` | Y `[C28b]` | Y `[C29a]` | Y `[C27b]` | Y `[C32a]` |
| Face detection | Y `[C6b]` | — | Y `[C10]` | P (ARTPEC-9) `[C15b]` | Y `[C17]` | — | Y* `[C23]` | Y `[C25b]` | Y `[C28b]` | Y `[C29a]` | Y `[C27c]` | P |
| Face recognition | P `[C6b]` | via BriefCam | Y `[C10]` | via partner ACAP | Y `[C18a]` | — | Y* `[C24]` | Y `[C25b]` | Y `[C28b]` | Y `[C29a]` | Y `[C27c]` | — |
| ANPR / ALPR | Y `[C7a]` + Y* `[C4]` | Y `[C53]` | Y `[C10]` | via Vaxtor `[C50]` | Y (dome/bullet only) `[C18b]` | — | P (OCR) `[C24]` | Y `[C25b]` | Y `[C28b]` | — | Y `[C27c]` | — |
| Virtual fence / intrusion | Y `[C6a]` | via 3rd party | Y `[C10]` | Y* `[C15c]` | Y `[C17]` | Y `[C20]` | Y* `[C23]` | Y `[C25b]` | Y `[C28b]` | Y `[C29a]` | Y `[C27b]` | Y `[C32a]` |
| Suspicious / behaviour analytics | P `[C6a]` | — | Y (rules) `[C10]` | P `[C15c]` | P `[C17]` | P | P `[C23]` | Y `[C25b]` | Y `[C28b]` | Y `[C29a]` | Y (SBRE) `[C27b]` | — |
| Night-time movement | — | — | — | P | — | **No, on thermal** `[C20]` | — | — | — | — | — | P |
| Real-time alerts & event logging | Y `[C6a]` | Y `[C1]` | Y `[C10]` | Y* `[C15c]` | Y `[C17]` | Y `[C22]` | Y `[C24]` | Y `[C25a]` | Y `[C28b]` | Y `[C29a]` | Y `[C27b]` | Y `[C32a]` |

### 4.1 What the table actually shows

**FACT** — Every one of the eight named capabilities is claimed by multiple
vendors, on public record, today `[C6][C10][C15][C17][C20][C23][C25][C28][C29][C27]`.

**None of the eight capabilities in the problem statement is an unsolved problem
in the market. All eight are shipping products.** The differentiation, if any,
is not in *whether* but in *on what hardware, at what cost, and under what
deployment conditions*.

**FACT — the "night-time movement detection" column is the emptiest, and that is
a real signal, not a search artefact.** The one explicit statement found on
thermal streams is a **negative**: Verkada's "people and vehicle analytics
features are only supported on visible (or non-thermal) video streams" `[C20]`.

**FACT — vendor-side evidence about low light `[C52a]`:** rain, fog and snow
"alter the image's contrast and sharpness"; wind moves vegetation "creating
constant pixel changes"; "sudden light changes, sunrise, sunset, vehicle
headlights create reflections and shadows that basic algorithms read as
suspicious movement." *(Analytics-vendor blog — the claim is against its own
category's interest, which raises its credibility.)*

**ASSUMPTION** — "Night-time movement detection" is not a distinct product
feature anywhere in the market; it is an **operating condition** that every
feature above either survives or does not. Vendors sell it as image-sensor
quality (Lightfinder, WDR, IR) or as a thermal camera, not as an analytic.
*(Basis: the absence of a single vendor page describing a night-specific
analytic, plus `[C20]`'s thermal exclusion and `[C52a]`'s lighting failure
modes.)*

### 4.2 The suspicious-activity column deserves separate treatment

**FACT** — Rule-based analytics dominate. Ipsotek's differentiator is an
explicitly **rule-based** engine (SBRE) `[C27b]`; Axis offers five fixed
scenario types with a maximum of 10 per camera `[C15c][C15d]`; BriefCam RESPOND
alerts on "face recognition, vehicles, and behavioural rules" `[C10]`.

**FACT — the documented weakness of that approach `[C60a][C60b]`:**
"Traditional rule-based systems often suffer from high false alarm rates due to
their reliance on predefined normal event dictionaries. Rule-based models with
fixed thresholds find it difficult to detect actual unusual behaviors in
unpredictable environments, resulting in high false positive rates and missed
anomalies." *(Peer-reviewed / academic sources, independent of vendors.)*

**FACT — the documented weakness of the alternative `[C60a]`:** learned
anomaly detection "need[s] wide-ranging training sets of normal system
activities, and any change in the system's normal patterns must lead to
necessary updates of the knowledge base."

**ASSUMPTION** — "Suspicious activity detection" is the one named capability
where the market has **no consensus solution** — only two approaches, each with
a well-documented failure mode, plus a third (vision-language models) that is
new and unproven in this domain `[C35a][C24]`. *(Basis: `[C60][C27b][C15c].)*

---

## 5. Architecture and deployment comparison

### 5.1 Where the inference actually runs

Four distinct patterns exist in the market. Every vendor examined uses one or a
combination.

| Pattern | Who does it | What it needs | What it costs you |
|---|---|---|---|
| **A. On-camera (edge, in-sensor)** | Axis ACAP `[C14]`, i-PRO `[C23]`, Hanwha `[C37a]`, Teledyne FLIR `[C40]`, SightLogix `[C39a]` | The vendor's own camera silicon | Total camera lock-in; no retrofit path |
| **B. On-site server / appliance** | Genetec KiwiVision `[C4]`, BriefCam `[C10]`, Irisity `[C29a]`, Ambient.ai `[C35a]`, Gorilla IVAR `[C36a]`, Frigate `[C32a]` | x86 + NVIDIA GPU at each site | Hardware, power, cooling, maintenance per site |
| **C. On-site bridge, cloud brain** | Verkada Command Connector `[C20]`, Eagle Eye bridge `[C33a]`, Genetec Cloudlink `[C8a]`, Milestone Kite `[C48a]` | Appliance + reliable uplink | Recurring per-camera licence; uplink dependency |
| **D. Pure cloud, event-driven** | Calipsa `[C30c]` | Internet only | Only works for narrow, event-triggered scopes |

**ASSUMPTION** — These are not really four choices; they are one continuous
trade of **where you pay** — camera silicon, site hardware, bandwidth, or scope.
Nobody has escaped the trade. *(Basis: every vendor in the table sits at exactly
one point on it.)*

### 5.2 The distributed multi-site pattern

**FACT** — Three vendors independently converged on the same structure:

- **BriefCam Nexus** — Hub + Sites, "a hub at each site processing the video
  locally, and then just sending the metadata back centrally" `[C12b]`.
- **Ambient.ai** — "AI processing running on edge appliances at each site and a
  cloud console for monitoring, multi-site management, and analytics" `[C35a]`.
- **Genetec Cloudlink** — appliances that "push processing and storage to the
  edge", maintaining "local operation during connectivity disruptions"
  `[C8a][C8c]`.

**FACT** — Milestone offers two distinct multi-site forms: **Federated
Architecture** (Expert/Corporate only) and **Interconnect** (all editions, with
Corporate as the only permitted central site) `[C1]`.

**The "process locally, ship metadata centrally" pattern is settled industry
practice, not an opening.** `[C12b][C35a][C8a]`

### 5.3 Recording ownership

**FACT** — A structural fork runs through the market:

- Vendors that **own recording** — Genetec Archiver `[C4]`, Milestone Recording
  Server `[C1]`, Verkada Command Connector's onboard RAID storage `[C20]`,
  Eagle Eye Bridge `[C33a]`, Gorilla IVAR `[C36a]`, Frigate `[C32a]`.
- Vendors that **do not** — BriefCam (reads from the VMS or via its Video
  Integration API) `[C10]`, Calipsa (events only) `[C30c]`, AllGoVision (feed
  from camera or VMS) `[C28b]`, Ipsotek `[C27b]`.

**ASSUMPTION** — Owning recording is the heavier commitment (storage sizing,
retention policy, evidentiary chain, RAID, failover) but is also what makes
evidence management and offline operation tractable. Not owning it makes the
product easier to sell but dependent on somebody else's VMS being present and
healthy. *(Interpretation.)*

### 5.4 Operating-system and platform dependencies

**FACT** — Genetec Security Center runs on **Windows only** and requires
**Microsoft SQL Server** `[C4]`.

**FACT** — Milestone XProtect runs servers "as Windows Services" and is
available for **AWS Marketplace** deployment `[C1]`.

**FACT** — Genetec Cloudlink appliances run "a secure, **Linux-based** operating
system" `[C8a]` — i.e. Genetec's own edge line escapes the Windows dependency
that its core platform has.

**FACT** — Frigate is distributed as Docker containers `[C32a][C32c]`; Milestone
AI Bridge expects third-party analytics "deployed as **docker containers**"
`[C47]`.

**ASSUMPTION** — Containerised Linux is the emerging norm for the analytics
layer even where the VMS layer is Windows. *(Basis: `[C47][C8a][C32a]`.)*

### 5.5 Virtualisation

**FACT** — Genetec: VMs have "20% less capacity" than equivalent physical
hardware; do not exceed six VMs per host or four video-intensive VMs per host;
assign at least 16 GB RAM per VM and keep 16 GB unallocated; do not exceed
300 Mbps per archiving VM or 1200 Mbps per host; and for KiwiVision "using
virtual machines is **not recommended**" `[C4]`.

**FACT** — BriefCam: VMs are "technically possible but not recommended for
production", and must reserve GPU, CPU, RAM and disk IOPS `[C10][C10b]`.

**The two most GPU-dependent products in this survey both advise against
virtualisation.** `[C4][C10]`

---

## 6. Hardware and ecosystem dependencies

This is the section the problem statement's premise turns on: *which advanced
capabilities genuinely require proprietary hardware, and which do not?*

### 6.1 Hard dependencies — capability is unavailable without vendor hardware

**FACT** — **Axis ACAP applications cannot run on non-Axis cameras** `[C14]`.
AXIS Object Analytics requires compatible Axis MLPU cameras on firmware 10.2+
`[C15a]`.

**FACT** — i-PRO's edge AI "requires i-PRO network cameras with AI
capabilities"; Active Guard consumes "metadata information from i-PRO Edge AI
cameras" and best-shot images — not raw third-party video `[C23]`.

**FACT** — Hanwha's analytics are tied to the Wisenet SoC's dual NPUs `[C37a]`.

**FACT** — Verkada's 20 kbps steady-state architecture depends on the camera
storing 30-365 days locally and emitting metadata — i.e. on Verkada's own camera
`[C21][C22]`. Third-party cameras via Command Connector explicitly **do not**
"receive the same features and capabilities as native Verkada devices" `[C20]`.

**FACT** — Genetec sizes AutoVu ALPR in "AutoVu camera units" `[C4]`, and Sharp
/ SharpX are purpose-built ALPR cameras `[C7c]`.

**FACT** — Avigilon Alta LPR "cannot be configured to use panoramic, 360,
fisheye, or PTZ cameras" — dome or bullet only `[C18b]`.

### 6.2 Soft dependencies — capability works on existing cameras, with caveats

**FACT** — **Genetec AutoVu Flexreader** turns existing supported IP cameras
into plate readers, "without dedicated ALPR hardware" — but only up to
**30 mph / 50 km/h** `[C7a][C7b]`.

**FACT** — **Milestone XProtect LPR**: "With XProtect LPR you do not need a
purpose-built LPR camera" — but the camera must look down on the vehicle at
**no more than 30 degrees**, and the logic is "processor intensive, and varies
significantly dependent on the environmental conditions, camera settings and
other parameters" `[C53]`.

**FACT** — **Vaxtor** ships ALPR both embedded on partner cameras and as PC
software, stating that embedding "decrease[s] network bandwidth and hardware
costs" `[C50]`.

**FACT** — **BriefCam** works from any VMS-sourced video, but requires
**NVIDIA GPUs** (no Intel or AMD), CIF-to-4K resolution, 8-30 FPS, and objects
of **12-32 pixels** minimum depending on class `[C10][C10b]`.

**FACT** — **Genetec KiwiVision** requires an **AVX-compatible CPU** on every
analytics server, and offers GPU acceleration for only two scenarios `[C4]`.

**Both major platforms turn out to have a software path off the proprietary
ALPR camera — and both then attach physical constraints (speed, angle) that the
existing camera may or may not satisfy. The dependency did not disappear; it
moved from the camera's silicon to the camera's mounting.** `[C7b][C53]`

### 6.3 The dependency nobody can remove: pixels on target

**FACT** — DORI (IEC EN 62676-4:2015): Detection **25 px/m**, Observation
**62 px/m**, Recognition **125 px/m**, Identification **250 px/m** `[C49]`.
Axis publishes its own pixel-density white paper on this `[C16]`.

**FACT** — BriefCam's stated floor is 12-32 pixels per object depending on class
`[C10]`.

**FACT** — ANPR needs ~250 px/m to resolve plate characters, and most ANPR
systems use IR illumination at 850 nm or 940 nm optimised for retroreflective
plates `[C49b]`.

**ASSUMPTION** — An existing camera installed for *human monitoring* was almost
certainly specified for Detection or Observation density (25-62 px/m), not
Identification (250 px/m). Software cannot manufacture the missing pixels.
*(Basis: `[C49]` plus the domain finding that existing border CCTV was installed
for live viewing `[docs/01-research/domain/domain-research.md §4.3]`.)*

**This is the boundary condition on the entire problem statement's premise, and
it applies to IBVAP exactly as it applies to every competitor.**

### 6.4 The ONVIF dependency, and why it is weaker than it looks

**FACT** — Verkada, whose Command Connector is a **certified ONVIF Profile S
conformant client** `[C20]`, still states: "While ONVIF Profile S is a standard
with a defined specification and interface guide, the actual implementation of
the various features and capabilities rests with the camera manufacturer. Even
if a camera is ONVIF Profile S conformant, some camera models may need
additional configuration... For some camera manufacturers, the implementation of
ONVIF Profile S features and capabilities also varies by the firmware version.
As a result, **any ONVIF Profile S camera may not work with Command Connector
out-of-the-box**" `[C20]`.

**FACT** — Verkada therefore maintains a **Hardware Compatibility List**, runs
an internal compatibility lab, and takes "weeks to months" to assess a new
camera `[C20]`.

**FACT** — Milestone maintains 16,500+ tested devices, ships device packs every
two months, and needed 1,000+ individually tested ONVIF devices to converge on
"a single optimized driver" `[C2][C3]`. It also ships a **universal driver** as
the fallback for devices that fit neither `[C1]`.

**Two of the most capable engineering organisations in this market both
concluded that ONVIF conformance is insufficient and built a per-model
compatibility apparatus. "We support ONVIF" is a statement of intent, not a
capability.** `[C20][C2][C3]`

**FACT** — ONVIF announced on 9 October 2025 that it is ending support for
Profile S in favour of Profile T; after 31 March 2027 manufacturers can no
longer submit new products for Profile S conformance
`[docs/01-research/domain/domain-research.md §6.7]`.

### 6.5 Geopolitical supply-chain dependency [MARKET:US] [MARKET:IN]

**FACT** — Under 2019 NDAA **Section 889**, the US federal government cannot
"procure or obtain" video surveillance "produced by" Dahua or Hikvision,
including OEM rebrands; it covers all federal agencies, the military and US
embassies overseas; it bans federal contractors that *use* such equipment
"regardless of whether that use" relates to a federal contract; and it bans
federal grant money being spent on it `[C42]`. Also named: Huawei, ZTE, Hytera.
Indiana adopted an equivalent state-level ban (SB477, 2023) `[C42]`.

**FACT** — India's ER-01/STQC regime has the same practical effect through a
different mechanism, motivated by "concerns regarding devices using foreign
chipsets" `[C43a]`, with non-conforming sales barred from 1 April 2026
`[C43d]`.

**ASSUMPTION** — Two of the world's largest procurement markets have
independently made **camera provenance** a gating condition. A software product
that is genuinely camera-agnostic is insulated from this; a product that depends
on specific camera silicon inherits its supplier's political risk.
*(Interpretation of `[C42][C43]`.)*

---

## 7. Integration and API comparison

| Vendor | Ingest | Outbound integration surface | Notes |
|---|---|---|---|
| Milestone XProtect | ONVIF (S/T/G/M), PSIA, universal driver, 11,000+ devices `[C1][C3]` | MIP SDK, REST API, WebSocket, WebRTC, webhooks, driver framework, **AI Bridge (Docker)** `[C1][C47]` | Deepest published surface found in this pass |
| Genetec Security Center | IP cameras via Security Center drivers; Media Gateway exposes **RTSP** to external apps `[C4]` | SDK, Federation, plugins | Media Gateway RTSP is never transcoded `[C4]` |
| BriefCam | VMS connectors (L1-L4) + **generic Video Integration API** for unsupported VMS `[C10][C11]` | Alerts into VMS as bookmarks/events with bounding boxes `[C11]` | Integration depth varies per VMS |
| AllGoVision | Direct from camera **or** from VMS `[C28b]` | **ONVIF virtual camera** consumable by any ONVIF VMS `[C28c]` | Neatest VMS-agnostic egress pattern found |
| Network Optix | IP cameras, **raw RTSP streams**, I/O devices `[C31a]` | Open-source integration repos (MPL 2.0), Nx Toolkit, TestCamera emulator `[C31c][C31e]` | Explicitly a build-on platform |
| Verkada | ONVIF Profile S; RTSP fallback, max 20 channels `[C20]` | Cloud Command APIs | **Does not consume third-party camera events** `[C20]` |
| i-PRO Active Guard | i-PRO camera metadata + best-shots `[C23]` | Plugs into Genetec, Milestone, Luxriot, Video Insight `[C24]` | Ingest side is closed |
| Irisity IRIS+ | **Any camera via RTSP/ONVIF, incl. analog via DVR** `[C29b]` | Not documented in this pass | Broadest stated ingest |
| Frigate | Any RTSP camera; dual-stream `[C32a]` | MQTT, WebRTC/MSE `[C32a]` | Integration by message bus, not SDK |

### 7.1 Findings

**FACT** — The **ingest** side of the market has effectively standardised on
**RTSP + ONVIF Profile S**, with per-model compatibility work layered on top
`[C1][C20][C29b][C31a][C32a]`.

**FACT** — The **egress** side has not standardised. Every vendor emits events
differently: MIP plugins, REST, WebSocket, webhooks, MQTT, ONVIF virtual camera,
VMS bookmarks `[C1][C28c][C32a][C11]`.

**ASSUMPTION** — "Support integration with existing command and control systems"
— the phrase in the problem statement — is therefore an **egress** problem, and
egress is exactly where the market has no standard. This is a structural,
recurring difficulty, not one specific to any force. *(Basis: the egress column
above.)*

**FACT** — Two integration patterns stand out as low-friction and reusable:

1. **AllGoVision's ONVIF virtual camera** — present analytics output as an ONVIF
   camera; any ONVIF VMS ingests it with no plugin `[C28c]`.
2. **Milestone AI Bridge** — a documented Docker-container contract for
   third-party analytics into the largest open VMS `[C47]`.

---

## 8. Remote and low-bandwidth deployment considerations [BORDER]

This is the axis on which the market is thinnest, and the evidence is unusually
concrete.

### 8.1 Published bandwidth figures, side by side

| System | Steady-state uplink | Notes | Source |
|---|---|---|---|
| Verkada camera | **20 kbps/camera**; thumbnails + metadata every ~20 s | Requires Verkada camera; 30-365 days on-device | `[C21]` |
| Verkada, viewing | ~300 kbps (720p) / ~1 Mbps (HD) | On demand only | `[C21]` |
| Calipsa | **~300 kb per event** | Analyses frames, not video | `[C30c]` |
| Eagle Eye Networks | **400 kbps/camera** recommended | Bridge buffers locally, syncs when bandwidth allows | `[C33a]` |
| Genetec Cloud Storage | **Recording throughput + 30%**, guaranteed, 99.9% SLA, <150 ms | 100 Mbps recorded means 130 Mbps uplink | `[C4]` |
| Raw H.264 IP camera | ~5 Mbps/stream | H.265 halves it | domain research 6.2 |

**The spread between Verkada's 20 kbps and Genetec's "recording throughput plus
30%" is four orders of magnitude, and it is explained entirely by where the
analysis happens.** `[C21][C4]`

### 8.2 What the industry says about the pattern

**FACT** — Industry and vendor sources describe the same architecture
repeatedly: cameras or site appliances perform local analytics and send "only
alert notifications (typically just a few kilobytes of metadata), relevant video
clips surrounding events (10-30 seconds of footage), and periodic metadata
describing scene activity" `[C56a]`.

**FACT** — Specific claimed reductions: "A 40-camera site that needed 80 Mbps of
continuous upload to record cloud-only now needs only a few megabits"; "A
100-camera deployment with edge processing might require only 10-20 Mbps".
Remote industrial sites "with as little as **512 Kbps** of upload bandwidth can
run detection locally and send only the resulting signals upstream" `[C56a]`.
*(Vendor/industry commentary — directional, not measured.)*

**FACT** — Peer-reviewed systems research finds per-camera uplink allocations in
constrained deployments can be "a few hundred kilobits per second or less",
conflicting with streaming all video centrally `[C56b]` and
`[docs/01-research/domain/domain-research.md]` 6.2.

**FACT** — Satellite links "are typically high-latency, low-bandwidth and
expensive, making it difficult to offload data or receive updates efficiently"
(recorded in `[docs/01-research/domain/domain-research.md]` 6.2).

### 8.3 Disconnected and air-gapped operation

**FACT** — **Milestone** supports "Offline license activation" and
"Add/replace devices without reactivation in offline systems" in **every**
edition `[C1]`.

**FACT** — **Irisity** lists "on-premise (**air-gapped**)" as a supported
deployment mode `[C29b]`.

**FACT** — **Verkada** documents an air-gapped *camera* network topology (second
NIC on the isolated camera VLAN, primary NIC to internet) — but the platform
itself still requires the cloud `[C20]`.

**FACT** — **Genetec Cloudlink** is positioned partly on "the need to maintain
local operation during connectivity disruptions" `[C8c]`.

**FACT** — **Frigate**: "all processing performed locally on your own hardware",
"no cloud subscriptions required" `[C32a]`.

**UNKNOWN** — Whether Genetec, BriefCam, Videonetics, AllGoVision or Ipsotek
support fully disconnected operation including licence validation, model updates
and time synchronisation. Not documented in anything retrieved. This is the
**single most important unknown** in this document for a remote-deployment
product.

### 8.4 Power

**UNKNOWN** — **No vendor in this survey publishes a power budget for its
analytics workload.** Genetec, BriefCam, Irisity and Ambient.ai all specify
NVIDIA GPUs `[C4][C10][C29a][C35a]` without stating watts. Verkada publishes
bandwidth but not power `[C21]`.

**ASSUMPTION** — Power is not a competitive dimension in this market because its
customers have mains power. At a generator-powered, fuel-limited site it is a
first-order constraint (`[docs/01-research/domain/ssb-operational-context.md]`
10.2). *(Interpretation.)*

**This is a blind spot in the industry's published engineering, not merely a gap
in this research pass.**

### 8.5 Maintenance at unreachable sites

**FACT** — Verkada: customers "cannot install their own drives and must use the
drives that Verkada provides"; a failed drive means a shipped replacement and a
physical swap `[C20]`.

**FACT** — Verkada: during a Command Connector firmware update, "the cameras
connected to Command Connector will not record footage" `[C20]`.

**FACT** — Verkada: "Verkada does not provide any security patches and firmware
updates for non-Verkada cameras" `[C20]`.

**ASSUMPTION** — Every appliance-based architecture (patterns B and C in
[5.1](#51-where-the-inference-actually-runs)) imports a physical maintenance
obligation at each site. Where sites cannot be reached by road, that obligation
dominates cost (`[docs/01-research/domain/ssb-operational-context.md]` 10.1).
*(Interpretation.)*

---

## 9. Competitive patterns

Patterns that recur across enough independent vendors to be treated as
properties of the industry rather than of any company.

### P1 — Analytics is a reason to buy hardware, not a product

**FACT** — Axis `[C14]`, i-PRO `[C23]`, Hanwha `[C37a]`, Verkada `[C21]`,
SightLogix `[C39a]` and Teledyne FLIR `[C40]` all bind their best analytics to
their own silicon.

**ASSUMPTION** — The camera vendors' analytics exist to defend camera margin.
This is why "software-only analytics on any camera" keeps being re-invented by
outsiders (BriefCam, Ipsotek, Irisity, AllGoVision, Calipsa, Ambient.ai) and
keeps being **acquired** by insiders (Canon/BriefCam, Motorola/Calipsa,
Eagle Eye/Uncanny, Nx/Scailable) `[C13][C30b][C34][C31b]`.

### P2 — Everyone converged on "process locally, ship metadata"

**FACT** — BriefCam Nexus `[C12b]`, Ambient.ai `[C35a]`, Genetec Cloudlink
`[C8a]`, Verkada `[C21]`, Eagle Eye `[C33a]` and Milestone Kite `[C48a]` all
implement it.

### P3 — Rule engines, not understanding

**FACT** — The dominant behavioural mechanism is a configured rule: zone,
line, direction, dwell time `[C27b][C15c][C6a][C10]`.

**FACT** — Academic sources document rule engines' high false-positive rate in
unpredictable environments, and learned anomaly detection's dependence on
large "normal" training sets that must be re-learned when normal changes
`[C60a][C60b]`.

### P4 — Environment, not algorithm, is the limiting factor

**FACT** — Documented outdoor failure modes: rain/fog/snow altering contrast and
sharpness; wind-moved vegetation; sunrise/sunset/headlight reflections and
shadows; wildlife and insects `[C52a][C52b]`.

**FACT** — IPVM's testing "shows lower accuracy in low light and with
accessories"; face-detection accuracy is most affected by "angle of faces and
lighting" `[C52c]`. *(Independent test lab, retrieved via summary only.)*

**ASSUMPTION** — The entire perimeter-thermal industry
([2.16](#216-perimeter-security-specialists-sightlogix-teledyne-flir-senstar))
exists as the industry's answer to P4. *(Basis: `[C39a][C40]`.)*

### P5 — "Open platform" means an ingest standard plus a compatibility lab

**FACT** — Milestone: 16,500+ tested devices, bi-monthly device packs, a
universal driver `[C1][C2][C3]`. Verkada: HCL, internal compatibility lab,
weeks-to-months assessments, no support off-list `[C20]`.

### P6 — Perpetual licences plus mandatory maintenance, or per-camera subscription

**FACT** — Milestone: perpetual across all four editions `[C1]`. BriefCam:
one-time purchase, optional annual maintenance, licensed per camera **sensor**
`[C10]`. Genetec: perpetual per channel plus an annual SMA `[C9]` *(low
confidence)*. Verkada: hardware purchase **plus** per-channel licences in 1/3/5/
10-year terms `[C20]`. Network Optix: both perpetual and recurring `[C31f]`.

**FACT** — **Per-camera is the near-universal unit of price**, whichever model.
`[C1][C10][C20][C9]`

**ASSUMPTION** — Per-camera pricing penalises exactly the deployment shape a
distributed border estate has — many sites, few cameras each, low utilisation
per camera. *(Interpretation.)*

### P7 — Deployment requires certified humans

**FACT** — Genetec and Milestone both run partner certification programmes;
IPVM prices Genetec classroom training at 2 days / USD 595-895 and Milestone
Advanced at 3 days / USD 2,995 `[C51]`.

**FACT** — Genetec ships a *Camera Requirements Calculator* whose stated purpose
includes verifying "whether your existing camera setup needs to be modified"
`[C4]`.

**ASSUMPTION** — The real deployment unit in this industry is a **site survey by
a trained integrator**, not an installer running a wizard. *(Basis: `[C51][C4]`,
plus Ipsotek shipping VISuite Core specifically to make rollout "repeatable,
plug-and-play" `[C27a]`.)*

### P8 — Consolidation into camera-plus-VMS-plus-analytics groups

**FACT** — Canon (Axis + Milestone + BriefCam) `[C13]`; Motorola (Avigilon +
Pelco + Calipsa) `[C30a][C30b]`; Atos/Eviden (Ipsotek) `[C27a]`; Eagle Eye
(Uncanny Vision) `[C34]`; Network Optix (Scailable) `[C31b]`.

### P9 — Regulation is becoming a market-entry gate [MARKET]

**FACT** — NDAA §889 in the US `[C42]`; ER-01/STQC in India `[C43]`; EU AI Act
Article 5 on biometric identification `[C44]`.

**FACT** — Under the EU AI Act, real-time remote biometric identification in
publicly accessible spaces for law enforcement is **prohibited by default** from
**2 February 2025**, subject to narrow exhaustive exceptions (missing persons,
imminent terrorist attack, identification of specified criminals), requiring
prior authorisation, a fundamental-rights impact assessment and registration in
the EU database `[C44a][C44b][C44c]`.

**A product whose headline feature is live face recognition is, by default,
illegal for law enforcement use in the EU. Face recognition is a
market-specific capability, not a universal one.** `[C44]`

### P10 — The disclosure asymmetry

**FACT** — Bandwidth, camera counts per server, GPU models, ONVIF profiles and
codec support are extensively published `[C4][C1][C10][C20][C21]`. Pricing,
accuracy, false-alarm rates and power draw are almost never published.

**ASSUMPTION** — The industry publishes what makes deployment *plannable* and
withholds what makes vendors *comparable*. *(Basis: the retrieval record of this
pass.)*

---

## 10. Potential gaps and opportunities

> **Nothing in this section is a product requirement.** Each entry is a
> hypothesis about where the market is thin, paired with the evidence for it and
> the reason it might be thin *on purpose*. Per
> [CLAUDE.md](../../../CLAUDE.md) §2, turning any of these into scope happens in
> `docs/02-product/`, not here.

### G1 — Disconnected-by-default operation [BORDER]

**Evidence for:** only Irisity states air-gapped support `[C29b]`; Milestone
states offline licensing `[C1]`; every cloud entrant assumes an uplink
`[C21][C33a][C30c][C4]`.
**Evidence against being a gap:** on-premise VMS has always run offline; this
may be table stakes rather than a differentiator.
**Status:** genuinely under-documented. See
[§11](#11-unknowns-requiring-further-research) Q-3.

### G2 — Power-aware analytics [BORDER]

**Evidence for:** zero vendors publish power budgets
([§8.4](#84-power)).
**Evidence against:** may simply be unmeasured rather than unsolved; edge
NPU cameras are already low-power `[C14][C37a]`.
**Status:** open.

### G3 — Analytics on thermal streams [BORDER]

**Evidence for:** Verkada explicitly excludes thermal from people/vehicle
analytics `[C20]`.
**Evidence against — this is largely solved by others:** Teledyne FLIR FC-Series
AI classifies humans and vehicles on thermal with onboard DNN analytics `[C40]`;
SightLogix does the same `[C39a]`. **Solved — but only by buying thermal
cameras with the analytics inside.**
**Status:** the gap is *thermal analytics as portable software*, not thermal
analytics.

### G4 — Sub-100-kbps operation without owning the camera

**Evidence for:** Verkada reaches 20 kbps by owning the camera `[C21]`; Calipsa
reaches ~300 kb/event by restricting scope to alarm frames `[C30c]`; the
general-purpose platforms sit orders of magnitude higher `[C4][C33a]`.
**Evidence against:** BriefCam Nexus already ships "process locally, send
metadata" `[C12b]`, and does not publish a bandwidth figure — so the gap may be
one of *disclosure*, not capability.
**Status:** plausible, unproven.

### G5 — Deployment without a site survey

**Evidence for:** Genetec's calculator asks whether cameras "need to be
modified" `[C4]`; certification programmes `[C51]`; Ipsotek shipping VISuite
Core specifically for "repeatable, plug-and-play" rollout `[C27a]`.
**Evidence against:** DORI physics ([§6.3](#63-the-dependency-nobody-can-remove-pixels-on-target))
means some estates genuinely cannot support some analytics. A product that
pretends otherwise will fail in the field.
**Status:** the real opportunity may be **telling the operator honestly what
this camera can and cannot support** — which nobody appears to ship as a
first-class feature.

### G6 — Capability disclosure as a feature

**Evidence for:** i-LIDS' **primary (sole) vs secondary (support)** detection
certification framing is a UK government standard
(`[docs/01-research/domain/domain-research.md]` 6.7), and no vendor examined
here exposes anything equivalent per camera.
**Evidence against:** vendors have a commercial incentive *not* to publish
per-camera limitations.
**Status:** open, and unusually well-aligned with the honest-engineering
posture the domain research argues for.

### G7 — Alerting sized to a two-person post [BORDER]

**Evidence for:** every platform here assumes a control room, a video wall and
an operator role hierarchy `[C4][C1]`; Genetec Smart Wall / XProtect Smart Wall
are premium-edition features `[C1]`.
**Evidence against:** mobile clients exist everywhere `[C1][C4]`.
**Status:** open. Note that whether the target force even *has* a control room
is itself unknown (`[docs/01-research/domain/ssb-operational-context.md]` 7).

### G8 — Egress standardisation

**Evidence for:** [§7.1](#71-findings) — every vendor emits events differently.
**Evidence against:** AllGoVision's ONVIF virtual camera `[C28c]` and
Milestone AI Bridge `[C47]` are both existing partial answers.
**Status:** partially solved; the unsolved part is *outbound to arbitrary
command-and-control systems*, not *outbound to a VMS*.

### G9 — Cost structure that fits many small sites

**Evidence for:** per-camera pricing is universal `[C1][C10][C20]`; Genetec
appliances are per-site `[C9]`; Verkada's smallest Command Connector is
USD 2,999 for 10 channels `[C20]`.
**Evidence against:** Frigate is free `[C32a]`; Nx offers perpetual licensing
`[C31f]`. The floor is already low if you accept the support model.
**Status:** open, but the competitor to beat is open source, not Genetec.

### G10 — Evidentiary integrity as a default, not an edition upgrade

**Evidence for:** Milestone gates media-database encryption and digital signing
to Expert/Corporate, and Evidence Lock to Corporate only `[C1]`. Genetec's
encryption costs 30% of Archiver capacity for the first certificate `[C4]`.
**Evidence against:** these features do exist; they are simply priced.
**Status:** the gap is that the cheapest deployments — which is what a remote
site gets — are the ones without signing, locking or tamper-evidence.

### 10.1 Apparent gaps that are already solved — do not chase these

| Apparent gap | Already solved by | Evidence |
|---|---|---|
| "ANPR without dedicated ANPR cameras" | Genetec Flexreader; Milestone XProtect LPR; Vaxtor | `[C7a][C53][C50]` |
| "Analytics on existing third-party cameras" | BriefCam, Ipsotek, Irisity, AllGoVision, Ambient.ai, Gorilla | `[C10][C27b][C29b][C28b][C35b][C36a]` |
| "Search video by description / natural language" | Avigilon Appearance Search, Ambient Pulsar, i-PRO Active Guard 3.0, Coram | `[C17][C35a][C24][C54]` |
| "Rapid forensic review of long recordings" | BriefCam VIDEO SYNOPSIS since well before 2018 | `[C10][C13a]` |
| "Reduce false alarms with AI" | Calipsa, an entire product category | `[C30c][C30d]` |
| "Privacy-preserving surveillance" | Genetec KiwiVision Privacy Protector; i-PRO AI Privacy Guard | `[C6b][C23]` |
| "Multi-site metadata aggregation" | BriefCam Nexus, Ambient.ai, Genetec Cloudlink | `[C12b][C35a][C8a]` |
| "Cloud video on low bandwidth" | Verkada 20 kbps, Eagle Eye 400 kbps | `[C21][C33a]` |
| "Open API into a VMS" | Milestone MIP/REST/WebSocket/AI Bridge | `[C1][C47]` |
| "Camera tamper detection" | Genetec Camera Integrity Monitor | `[C6a]` |

---

## 11. Unknowns requiring further research

### Highest priority — these block any competitive positioning

**Q-1. What does any of this actually cost?** Genetec, Milestone, BriefCam,
Avigilon, Ipsotek, Irisity, Videonetics and AllGoVision publish no list pricing.
Verkada is the only vendor with published hardware prices `[C20]`, and even
there the per-channel licence price is not published. Without this, "cheaper
than the incumbents" is an untestable claim.

**Q-2. How accurate is any of this, measured independently?** No standardised,
independent, published accuracy benchmark for any product in this survey was
retrieved. IPVM tests exist but are paywalled `[C52c]`. i-LIDS certification
exists as a framework (`domain-research.md` 6.7) but no vendor in this survey
was found publishing an i-LIDS certification result.

**Q-3. Which of these products genuinely run fully disconnected?** Only Irisity
states air-gapped `[C29b]` and Milestone states offline licensing `[C1]`. For
Genetec, BriefCam, Videonetics, AllGoVision and Ipsotek this is unknown — and it
is decisive for a remote-site product.

**Q-4. What is the power draw of each architecture per camera?** Nobody
publishes it ([§8.4](#84-power)).

**Q-5. What is the real installed-base composition worldwide?** How much of the
world's deployed CCTV is ONVIF-conformant, what resolution, what codec, what
pixel density on target? Without this, "works with existing cameras" cannot be
sized.

### High priority — shape the competitive picture

**Q-6.** What are Bosch's IVA Pro capabilities and dependencies from **primary**
Bosch documentation? This pass only retrieved trade commentary `[C38]`.

**Q-7.** What do Hikvision and Dahua actually ship for analytics, and at what
price? They are excluded from US federal procurement `[C42]` and constrained in
India `[C43]`, but they are a very large part of the world's installed base and
were not researched in this pass.

**Q-8.** What is Videonetics' architecture, hardware requirement and pricing —
and does it run on existing third-party cameras unmodified? It is the most
directly comparable competitor in the initial validation market and the least
documented `[C25]`.

**Q-9.** What are Ipsotek's and Irisity's per-camera hardware requirements and
prices? Both claim the exact positioning IBVAP would take `[C27b][C29b]`.

**Q-10.** Which vendors have actually deployed at land borders, and what did
those deployments learn? Anduril's CBP programme is documented `[C41]`; nothing
comparable was found for the VMS/analytics vendors.

**Q-11.** What is the real-world false-alarm rate of any of these products in
outdoor, unlit, vegetated, wildlife-rich terrain? Vendor claims exist
(Calipsa 93-95% reduction `[C30c]`); independent measurement does not.

### Medium priority — validate assumptions in this document

**Q-12.** Is the assumption in [§4.1](#41-what-the-table-actually-shows) correct
that no vendor sells a "night-time analytic" as a distinct feature? Tested only
by absence of evidence.

**Q-13.** Does India's ER-01/STQC regime apply to analytics **software**, or
only to cameras? [§3.5](#35-the-indian-regulatory-factor-marketin) assumes the
latter, unverified.

**Q-14.** Do Avigilon Unity's advanced analytics (Appearance Search, unusual
motion) function on third-party ONVIF cameras? `[C17]` does not say.

**Q-15.** What are BriefCam's and Genetec's actual multi-site bandwidth figures?
Both ship the "local processing, central metadata" pattern but neither publishes
a number `[C12b][C8a]`.

**Q-16.** How much of the market is VSaaS versus on-premise, by revenue and by
camera count? Omdia and Novaira hold this behind paywalls `[C46a][C46c]`.

### Research-process gaps in this pass

**Q-17.** Four vendor PDFs could not be read by the fetch tool and had to be
extracted locally; several other vendor documents were only reachable through
search-engine summaries. Every finding sourced from a search summary rather than
the document itself is weaker than it appears.

**Q-18.** No paywalled analyst or test-lab source (Omdia, Novaira, IPVM) was
read directly. All three are the industry's primary evidence sources for market
share and measured performance.

**Q-19.** Chinese, Russian, Korean and Japanese domestic vendors are almost
entirely absent from this pass, as is the entire Latin American and African
market. The picture here is Western-plus-India.

**Q-20.** No competitor was evaluated hands-on. Everything here is documentary.

### Deliberately deferred — not this stage

- Which of these vendors IBVAP should integrate with (architecture, stage 04).
- Which capability IBVAP should build first (product, stage 02).
- Whether to build on Network Optix, Frigate or from scratch (architecture).
- Pricing and business model for IBVAP (product).

---

## 12. Sources

Retrieved 2026-08-24 unless otherwise noted. **P** marks a primary vendor
engineering document whose text was read in full. **V** marks vendor marketing.
**I** marks an independent or third-party source. **A** marks academic or
standards material.

### Milestone Systems

- `[C1]` **P** — *Product Comparison Chart, XProtect Video Management Software
  2026 R1*, Milestone Systems. PDF, 20 pages, text extracted in full.
  https://download.milestonesys.com/MTSKB/KB000034241/XProtect%20VMS%202026%20R1%20Comparison%20Chart.pdf
- `[C2]` **V** — Supported devices / device packs, Milestone.
  https://www.milestonesys.com/support/software/supported-devices/ and
  https://www.milestonesys.com/support/software/device-packs/
- `[C3]` **V** — Milestone ONVIF drivers documentation.
  https://doc.milestonesys.com/en-US/bundle/driv1301_latest/page/Introduction_and_scope_Milestone_ONVIF_drivers.html
- `[C47]` **V** — Milestone AI Bridge administrator documentation.
  https://doc.milestonesys.com/AIB/Help/latest/en-us/
- `[C48a]` **V** — Milestone Kite product page.
  https://www.milestonesys.com/resources/content/articles/milestone-kite-arcules-vsaas-what-who/
- `[C48b]` **I** — "Milestone Systems introduces Milestone Kite",
  in-security.eu.
- `[C48c]` **I** — "Milestone announces XProtect 2026 R1 and Arcules VSaaS
  platform enhancements", Security Systems News.
- `[C53]` **V** — *XProtect LPR Specification Sheet* (2023 R1 and 2025 R1).
- `[C58]` **V** — "Milestone grows net revenue to USD 340 million in 2025",
  PR Newswire.

### Genetec

- `[C4]` **P** — *Security Center System Requirements Guide 5.12*, Genetec Inc.,
  document EN.500.100-V5.12.0.0(4), last updated 6 February 2024. PDF, 44 pages,
  text extracted in full.
- `[C5]` **V** — *Security Center Administrator Guide 5.12*, "About Security
  Center", techdocs.genetec.com.
- `[C6a]` **V** — KiwiVision Security video analytics module, techdocs.genetec.com.
- `[C6b]` **V** — KiwiVision Privacy Protector module, techdocs.genetec.com;
  KiwiVision unified video analytics product page, genetec.com.
- `[C7a]` **V** — "Genetec announces AutoVu Flexreader", Genetec press release,
  April 2018.
- `[C7b]` **I** — "Genetec launches AutoVu Flexreader for hardware-free ANPR
  capabilities", IFSEC Insider; "Genetec Solution Turns IP Camera Into ALPR
  Camera", SDM Magazine, July 2018.
- `[C7c]` **V** — AutoVu Sharp / SharpX / SharpZ3 camera specifications.
- `[C8a]` **V** — "Genetec Cloudlink 310" / "Cloudlink 210" press releases,
  GlobeNewswire, Feb 2025.
- `[C8b]` **I** — "Cloudlink 210 from Genetec", Security Sales & Integration.
- `[C8c]` **I** — "Modernize Security Operations With Genetec Cloudlink",
  SecurityInformed.
- `[C8d]` **V** — About Security Center SaaS, help.securitycentersaas.genetec.cloud.
- `[C9]` **I, low confidence** — Third-party pricing estimates: surveillant.ai,
  tec-tel.com, spot.ai. **Competitor-adjacent content; not treated as fact.**
- `[C57]` **V** — "Genetec is the only VMS vendor in the world to hold UL
  cybersecurity certification", Genetec press release, October 2020.

### BriefCam

- `[C10]` **V** — BriefCam Frequently Asked Questions, milestonesys.com.
- `[C10b]` **V** — *BriefCam Hardware Solution Brief* PDF and
  *BriefCam v5.3.1 Hardware Deployment Sizing*.
- `[C11]` **V** — BriefCam Supported VMS list, milestonesys.com.
- `[C12a]` **V** — BriefCam Multi-Site Architectures, briefcam.com.
- `[C12b]` **V/I** — "BriefCam extends advanced video analytics platform for
  multi-site deployments", Security Systems News; BriefCam Nexus material.
- `[C13a]` **V** — "Canon Completes Acquisition of BriefCam", BriefCam press
  release, 3 July 2018.
- `[C13b]` **I** — "Canon Consolidates BriefCam Into Milestone", IPVM.
- `[C13c]` **I** — "Canon Acquires Briefcam, Now Owns Briefcam, Milestone and
  Axis", IPVM.

### Axis

- `[C14]` **P** — *AXIS Camera Application Platform (ACAP)*, Axis white paper,
  March 2021, PDF.
  https://www.axis.com/dam/public/68/35/39/axis-camera-application-platform-acap-en-US-266554.pdf
- `[C15a]` **V** — AXIS Object Analytics product page and user manual,
  help.axis.com.
- `[C15b]` **V/I** — ARTPEC-8 / ARTPEC-9 chipset descriptions (Axis; CamStreamer).
- `[C15c]` **V** — AXIS Object Analytics Scenarios, axis.com.
- `[C15d]` **V** — *AXIS Object Analytics FAQ*, June 2024, PDF.
- `[C16]` **V/A** — *Pixel density and DORI: meeting operational requirements in
  network video*, Axis white paper, PDF.

### Avigilon / Motorola Solutions

- `[C17]` **V** — Avigilon Compatible Third-Party Cameras and Encoders,
  avigilon.com.
- `[C18a]` **V** — Unity Video License Plate Recognition Setup Guide 8.7,
  docs.avigilon.com.
- `[C18b]` **V** — "Considerations when setting up cameras for license plate
  recognition", Alta Video docs, docs.avigilon.com.
- `[C19]` **V** — "Enable ONVIF or Alta mode in Ava cameras", docs.avigilon.com.
- `[C30a]` **V** — Motorola Solutions brands, pelco.com.
- `[C30b]` **V** — "Motorola Solutions Acquires Calipsa", press release, 2021.
- `[C30c]` **V** — Calipsa Pro Analytics, calipsa.io; Pelco Calipsa, pelco.com.
- `[C30d]` **V/I** — Calipsa Video Analytics, DICE Corporation; Sharp Group case
  study.

### Verkada

- `[C20]` **P** — *Command Connector FAQ*, Verkada, doc revision 0526. PDF,
  13 pages, 53 questions, text extracted in full.
  https://docs.verkada.com/docs/command-connector-faq.pdf
- `[C21]` **V** — "Reducing Bandwidth Consumption of a Cloud Camera to 20kbps",
  Verkada blog.
- `[C22]` **V** — Hybrid Cloud Physical Security Architecture; "Cloud vs. Hybrid
  Cloud Security Camera System", verkada.com; *Traditional vs Hybrid Cloud* PDF.
- `[C46b]` **V** — "Verkada Ranked #1 Worldwide in VSaaS", verkada.com, citing
  Omdia.

### i-PRO, Hanwha, Bosch

- `[C23]` **V** — i-PRO Edge AI solution,
  i-pro.com/products_and_solutions/en/surveillance/solutions/technologies/edge-ai-solutions
- `[C24]` **V** — "i-PRO Introduces Active Guard Version 3.0 with Generative AI";
  "i-PRO Active Guard video analytics integrated into Luxriot EVO VMS", i-pro.com.
- `[C37a]` **V** — Hanwha Vision AI solutions and Wisenet 9 SoC, hanwhavision.eu;
  "How to Set up an Intelligent Video Analytic on Cameras using WiseAI",
  Hanwha Vision Support Portal.
- `[C37b]` **V** — *Wisenet AI Camera* white paper, Hanwha, PDF.
- `[C38]` **I, weak** — Bosch IVA Pro references in third-party comparison
  content. **Not primary Bosch documentation — see Q-6.**

### Indian vendors

- `[C25a]` **V** — Videonetics corporate site and VMS product page,
  videonetics.com.
- `[C25b]` **V** — Videonetics ANPR / FRS product descriptions, videonetics.com.
- `[C25c]` **I** — "Videonetics Empowers Asia's Biggest Real-time Governance
  Center in Andhra Pradesh", VARIndia.
- `[C25d]` **I** — "Videonetics AI Video Platform In Andhra Pradesh",
  SecurityInformed.
- `[C25e]` **I** — "Member Profile: Videonetics", ONVIF blog, May 2023.
- `[C26a]` **V** — Matrix SATATYA Enterprise NVR, matrixcomsec.com.
- `[C26b]` **V/I** — "Matrix and Yotta Partner to Deliver AI-Powered Cloud Video
  Surveillance", IT Voice / SMEStreet / SourceSecurity.
- `[C26c]` **I** — Matrix-Yotta partnership coverage, CXOToday.
- `[C28a]` **V** — AllGoVision About Us, allgovision.com.
- `[C28b]` **V** — AllGoVision Analytics and Features pages, allgovision.com.
- `[C28c]` **V** — AllGoVision Technology Partners page (ONVIF virtual camera),
  allgovision.com.
- `[C28d]` **I** — AllGoVision partner profile, Intel Partner Showcase.
- `[C43a]` **I** — "India to enforce stricter CCTV regulations from April 2025",
  asmag.com.
- `[C43b]` **V/I** — "STQC Certification and ER Compliance for CCTV Cameras",
  Matrix Comsec.
- `[C43c]` **I** — STQC IoT System Certification Scheme, stqc.gov.in.
- `[C43d]` **I** — "CCTV New Rule 2026 India: STQC Certification and ER
  Compliance Required from 1 April 2026", velvu.in.
- `[C43e]` **I, advocacy** — "STQC Certification Requirement Order Monopolises
  The CCTV Industry in India", securityupdate.in.
- `[C55a]` **V** — Vehant Technologies, vehant.com.
- `[C55b]` **I** — Staqu Technologies profile, CB Insights.
- `[C55c]` **I** — "JARVIS By Staqu", Electronics For You.
- `[C55d]` **I** — Wobot Intelligence profile, CB Insights.

### Other analytics and platform vendors

- `[C27a]` **V** — "Ipsotek launches VISuite Core to transform scalable AI-video
  analytics deployments", Eviden press release.
- `[C27b]` **V** — VISuite AI product page, ipsotek.com.
- `[C27c]` **V** — Ipsotek VISuite AI listing, Milestone Technology Partner
  Finder.
- `[C29a]` **V** — IRIS+ Video Analytics Platform Overview, irisity.com;
  *IRIS+ Professional* brochure PDF.
- `[C29b]` **V** — Irisity FAQ and Edge Analytics Devices pages, irisity.com;
  docs.irisity.com.
- `[C31a]` **V** — Nx Meta Architecture Overview, support.networkoptix.com.
- `[C31b]` **V/I** — Nx AI Manager, networkoptix.com blog and
  nx.docs.scailable.net; Edge AI and Vision Alliance coverage.
- `[C31c]` **P** — github.com/networkoptix/nx_open_integrations and
  github.com/networkoptix/nx_open (MPL 2.0).
- `[C31d]` **V** — "Nx Desktop is now Open Source", networkoptix.com.
- `[C31e]` **V** — "How to get a License for Developers", support.networkoptix.com.
- `[C31f]` **V** — Nx Witness FAQ and licensing pages, networkoptix.com.
- `[C32a]` **V** — Frigate NVR, frigate.video.
- `[C32b]` **I** — "Deploy Frigate On Jetson", Seeed Studio Wiki.
- `[C32c]` **I** — Frigate deployment guides, corelab.tech and homelabstarter.com.
- `[C33a]` **V** — Eagle Eye Networks Cloud VMS FAQ, een.com;
  *Architecture and Engineering Specifications* PDF;
  *EE AN044 Utilizing 4G and 5G Internet Connectivity with Bridges and CMVRs*.
- `[C33b]` **V** — *EE AN045 Eagle Eye Cloud VMS Subscriptions Explained* PDF.
- `[C34]` **V** — "Eagle Eye Networks Acquires Surveillance AI Leader Uncanny
  Vision", BusinessWire, 30 September 2021.
- `[C35a]` **I** — Ambient.ai platform and pricing analyses, surveillant.ai and
  coram.ai. **Third-party, competitor-adjacent.**
- `[C35b]` **V** — Ambient.ai platform overview and AI Info pages, ambient.ai.
- `[C36a]` **V** — Gorilla IVAR, gorilla-technology.com.
- `[C36b]` **I** — Gorilla IVAR listing, SecurityInfoWatch.
- `[C36c]` **V** — Gorilla EVMS, gorilla-technology.com.
- `[C36d]` **V** — Gorilla Edge AI solutions, gorilla-technology.com.
- `[C36e]` **V** — IVAR Edge AI from Gorilla, Milestone Marketplace.
- `[C39a]` **V** — SightLogix products and thermal perimeter intrusion pages,
  sightlogix.com.
- `[C39b]` **I** — Senterior/Senstar perimeter intrusion segment description.
- `[C40]` **V** — "Teledyne FLIR Introduces AI-Optimized Thermal Camera for
  Enhanced Intrusion Detection", flir.com.
- `[C50]` **V** — VaxALPR on-camera and VaxALPR product pages, vaxtor.com.
- `[C54]` **I, competitor-authored** — Coram AI comparison articles, coram.ai;
  Spot AI alternatives, spot.ai. **Treat as positioning evidence only.**

### Border-specific

- `[C41a]` **I** — "CBP Awards Anduril $363 Million For Extended Range
  Surveillance Towers", Defense Daily.
- `[C41b]` **I** — "U.S. Customs and Border Protection Set to Purchase 200
  Extended Range Sentry Towers From Anduril", HSToday.
- `[C41c]` **I** — "Anduril to Supply 200+ Tactical Sensing Towers to US Border
  Patrol", The Defense Post, 15 June 2026.
- `[C41d]` **I** — "CBP more than doubling autonomous sentry towers along
  Southwest border", FedScoop.

### Regulation and market structure

- `[C42]` **I** — "Where Dahua and Hikvision Are Banned", IPVM public report;
  NDAA Section 889 guidance materials.
- `[C44a]` **A** — EU Artificial Intelligence Act, Article 5: Prohibited AI
  Practices. artificialintelligenceact.eu/article/5/
- `[C44b]` **I** — "Red Lines under the EU AI Act: Restricting Real-time Remote
  Biometric Identification Systems for Law Enforcement Purposes", Future of
  Privacy Forum.
- `[C44c]` **I** — FPF analysis summary, WTL Governance.
- `[C45a]` **I** — Video Surveillance Market Size Report, MarketsandMarkets.
- `[C45b]` **I** — Video Surveillance Global Market Report,
  The Business Research Company.
- `[C45c]` **I** — Video Surveillance Market Size, Fortune Business Insights.
- `[C45d]` **I** — Video Analytics Market Size And Share Report 2025-2030,
  Grand View Research.
- `[C45e]` **I** — Video Analytics Market Size, Mordor Intelligence.
- `[C46a]` **I, paywalled** — Video Surveillance & Analytics Market Share
  Database, Omdia.
- `[C46c]` **I, paywalled** — World Market for Video Surveillance Hardware and
  Software, 5th edition, Novaira Insights.
- `[C51]` **I** — "VMS Training Options Compared", IPVM public report;
  Genetec and Milestone training pages.

### Standards, academic and technical

- `[C49]` **A** — DORI, IEC EN 62676-4:2015, as described across
  Infiniti Electro-Optics, TP-Link, CCTV Design Tool and Axis `[C16]`.
- `[C49b]` **I** — "How to Choose the Right Camera for ANPR Systems, Part 2",
  e-con Systems.
- `[C52a]` **V, against-interest** — "Video analytics in extreme weather: rain,
  fog and wind" and "Why Security False Alarms Happen", Davantis.
- `[C52b]` **V** — "How Do FH-Series Cameras Reduce False Alarms and Improve
  Detection Accuracy?", Teledyne FLIR.
- `[C52c]` **I, paywalled** — IPVM discussions and reports on video analytics
  accuracy and low-light performance.
- `[C56a]` **V/I** — Edge-based surveillance bandwidth analyses: Wavestore,
  Sighthound, surveillant.ai, Ground Control, Fora Soft.
- `[C56b]` **A** — *Scaling Video Analytics on Constrained Edge Nodes*,
  arXiv:1905.13536.
- `[C60a]` **A** — Rule-based vs anomaly-detection limitations, as documented in
  IJCA and ScienceDirect surveys of video anomaly detection.
- `[C60b]` **A** — Sultani, Chen and Shah, *Real-world Anomaly Detection in
  Surveillance Videos*, CVPR 2018.

### Internal cross-references

- `[docs/00-project/problem.md]` — official SIH problem statement (immutable).
- `[docs/01-research/domain/domain-research.md]` — border CCTV domain research.
- `[docs/01-research/domain/ssb-operational-context.md]` — SSB operational
  context.

---

## The strongest 10 market lessons

Ordered by how much each should change subsequent stages.

1. **Every capability the problem statement names is already a shipping product,
   from multiple vendors, today.** Human/vehicle detection, face detection and
   recognition, ANPR, virtual fence, behaviour rules, alerting and event logging
   are all commercially available `[C6][C10][C15][C17][C20][C23][C25][C28][C29][C27]`.
   There is no capability gap. Any advantage must come from architecture, cost,
   deployability or honesty — not from the feature list.
   ([§4](#4-capability-comparison))

2. **"Advanced analytics requires proprietary hardware" is half true, and the
   half that is false is already commercialised.** Genetec's Flexreader and
   Milestone's XProtect LPR both do ANPR on ordinary IP cameras
   `[C7a][C53]` — but both attach physical constraints (30 mph, 30-degree
   mounting) that transfer the dependency from the camera's silicon to the
   camera's *placement*. ([§6.2](#62-soft-dependencies--capability-works-on-existing-cameras-with-caveats))

3. **Pixels on target is the hard floor, and it is the same floor for
   everyone.** DORI sets Detection at 25 px/m and Identification at 250 px/m
   `[C49]`; BriefCam needs 12-32 px per object `[C10]`. A camera installed for
   human monitoring cannot be upgraded to face identification by software.
   ([§6.3](#63-the-dependency-nobody-can-remove-pixels-on-target))

4. **"We support ONVIF" is an intention, not a capability.** Verkada — a
   *certified* ONVIF Profile S client — still maintains a hardware compatibility
   list, an internal compatibility lab, and a weeks-to-months assessment queue,
   and states plainly that "any ONVIF Profile S camera may not work... out-of-
   the-box" `[C20]`. Milestone needed 1,000+ individually tested devices to
   converge on one optimised ONVIF driver `[C3]`.
   ([§6.4](#64-the-onvif-dependency-and-why-it-is-weaker-than-it-looks))

5. **"Process locally, ship metadata centrally" is settled practice, not an
   opening.** BriefCam Nexus, Ambient.ai, Genetec Cloudlink, Verkada, Eagle Eye
   and Milestone Kite all implement it `[C12b][C35a][C8a][C21][C33a][C48a]`.
   ([§5.2](#52-the-distributed-multi-site-pattern))

6. **The bandwidth spread across the market is four orders of magnitude, and it
   is bought with camera ownership.** Verkada achieves 20 kbps per camera by
   owning the camera `[C21]`; Genetec Cloud Storage demands recording throughput
   plus 30%, guaranteed, with a 99.9% SLA `[C4]`.
   ([§8.1](#81-published-bandwidth-figures-side-by-side))

7. **Nobody publishes power.** Not one vendor in this survey states the watts its
   analytics consume, even while mandating specific NVIDIA GPUs
   `[C4][C10][C29a][C35a]`. ([§8.4](#84-power))

8. **Suspicious-activity detection has no consensus solution.** Rule engines
   dominate `[C27b][C15c]` and are documented to produce high false-positive
   rates in unpredictable environments; learned anomaly detection needs a stable
   "normal" it can be taught `[C60a][C60b]`. Vision-language models are the new
   entrant and are unproven here `[C35a][C24]`.
   ([§4.2](#42-the-suspicious-activity-column-deserves-separate-treatment))

9. **The unit of price is the camera, everywhere, under every licensing model.**
   Perpetual, subscription or hardware-plus-licence — all of them meter per
   camera, and BriefCam meters per *sensor* `[C1][C10][C20][C9]`. That pricing
   shape penalises many-small-sites estates.
   ([§9](#p6--perpetual-licences-plus-mandatory-maintenance-or-per-camera-subscription))

10. **Regulation is now a market-entry gate, and it differs per market.** NDAA
    §889 excludes named Chinese vendors from US federal procurement `[C42]`;
    India's ER-01/STQC bars non-conforming camera sales from 1 April 2026
    `[C43d]`; the EU AI Act prohibits real-time remote biometric identification
    for law enforcement by default `[C44a]`. Face recognition is a
    **market-specific** capability, not a universal one.
    ([§9](#p9--regulation-is-becoming-a-market-entry-gate-market))

---

## The strongest 10 potential gaps

> **None of these is a product requirement.** Each is a hypothesis about market
> thinness, with its counter-evidence attached. Converting any of them into
> scope is a `docs/02-product/` decision.

1. **Fully disconnected operation as a designed default** — not a degraded mode.
   Only Irisity states air-gapped support `[C29b]`; only Milestone documents
   offline licensing `[C1]`. For most of the market this is simply
   undocumented. *(Counter: on-premise VMS has always run offline; this may be
   table stakes.)* [BORDER]

2. **A published power budget per camera per analytic.** Zero vendors publish
   it `[C4][C10][C29a][C35a]`. *(Counter: may be unmeasured rather than
   unsolved.)* [BORDER]

3. **Honest per-camera capability disclosure** — telling the operator, from the
   actual stream, which analytics this camera can and cannot support at this
   mounting, in the spirit of i-LIDS' primary-vs-secondary certification.
   Genetec has a *calculator* `[C4]`; nobody ships this as a runtime feature.
   *(Counter: vendors have a commercial incentive not to.)*

4. **Thermal analytics as portable software.** Verkada explicitly runs no
   people/vehicle analytics on thermal `[C20]`. *(Strong counter: Teledyne FLIR
   `[C40]` and SightLogix `[C39a]` solved this — inside their own cameras. The
   gap is portability, not capability.)* [BORDER]

5. **Sub-100-kbps steady state without owning the camera.** Verkada gets there
   by owning it `[C21]`; Calipsa gets there by narrowing scope to alarm frames
   `[C30c]`. *(Counter: BriefCam Nexus may already achieve this and simply not
   publish a number `[C12b]` — see Q-15.)* [BORDER]

6. **Deployment that survives no site survey and no certified integrator.**
   Certification is priced at 2-3 days and USD 595-2,995 `[C51]`; Ipsotek
   shipped a whole product variant to make rollout repeatable `[C27a]`.
   *(Counter: DORI physics means some estates genuinely cannot be made to work,
   and a product that hides that will fail in the field.)*

7. **Failure modes a non-specialist can recognise and report.** Verkada alerts
   on lost streams `[C20]` and Genetec ships a Camera Integrity Monitor `[C6a]`,
   but nothing found addresses *degraded analytic quality* — a camera still
   streaming but no longer usable for its configured analytic. *(Counter: this
   may exist under names not searched.)* [BORDER]

8. **Evidentiary integrity at the cheapest tier.** Milestone gates media
   encryption and digital signing to Expert/Corporate and Evidence Lock to
   Corporate `[C1]`; Genetec's first encryption certificate costs 30% of
   Archiver capacity `[C4]`. The smallest, most remote deployments are exactly
   the ones that get none of it. *(Counter: these are pricing decisions, not
   absent features.)*

9. **Outbound integration to arbitrary command-and-control systems.** Ingest has
   standardised on RTSP/ONVIF; egress has not `[C1][C28c][C32a][C11]`.
   *(Counter: AllGoVision's ONVIF virtual camera `[C28c]` and Milestone AI
   Bridge `[C47]` are real partial answers — for VMS targets specifically.)*

10. **A cost structure for many small, low-utilisation sites.** Per-camera
    pricing is universal `[C1][C10][C20]`; Verkada's smallest bridge is
    USD 2,999 for 10 channels `[C20]`. *(Counter: Frigate is free `[C32a]` and
    Nx sells perpetual licences `[C31f]` — the competitor at the bottom of this
    market is open source, not Genetec.)*

---

## 5 assumptions we must NOT make

1. **Do not assume the named capabilities are unsolved.** They are all shipping.
   The problem statement's framing — that FRS/ANPR/intrusion detection "often
   require specialized hardware and proprietary solutions" — is only partly
   supported: Genetec Flexreader and Milestone XProtect LPR already do ANPR on
   ordinary cameras `[C7a][C53]`, and the SSB research separately records that
   the named force has **already procured** a CCTV setup with FRS and ANPR
   (`ssb-operational-context.md`, 6.1 and 14.2).

2. **Do not assume "works with any ONVIF camera" is achievable by asserting it.**
   Two of the best-resourced engineering organisations in this market both built
   per-model compatibility apparatus and still warn the buyer `[C20][C3]`. A
   claim of universal camera support must be backed by a tested-device list, or
   it is a claim about intent.

3. **Do not assume software can compensate for the installed camera.** DORI is
   physics `[C49]`. Resolution, mounting angle, lens, illumination and vehicle
   speed bound what any algorithm can extract `[C7b][C53][C10]`.

4. **Do not assume face recognition is a globally shippable feature.** It is
   prohibited by default for law enforcement in publicly accessible spaces under
   EU AI Act Article 5 `[C44a]`, and the domain research separately flags open
   legal questions about applying it to a treaty-open border population
   (`ssb-operational-context.md`, 11.6). It is **[MARKET]**-specific.

5. **Do not assume the incumbents are expensive because they are inefficient.**
   Genetec's cost buys federation, failover, encryption, audit, certification and
   a support organisation `[C4][C57]`; the encryption alone costs 30% of Archiver
   capacity `[C4]`. Anything cheaper is trading something away, and the trade
   must be named, not hidden.

---

## 5 questions that should feed into product discovery

*(These are for `docs/02-product/`. They are not answered here.)*

1. **What is the smallest deployable unit?** Every architecture in this market
   assumes either a control room or a cloud tenant. What does a site with two
   cameras, one Sub-Inspector, a generator and a satellite phone actually get,
   and is that unit a product?
   ([8](#8-remote-and-low-bandwidth-deployment-considerations-border))

2. **Is the differentiator the analytic, or the deployment?** Given that all
   eight named capabilities are commodity ([4](#4-capability-comparison)), does
   IBVAP compete on detection quality — where it would be measured against
   vendors with decades of tuning — or on getting a working system onto an
   estate nobody else will touch?

3. **Which side of the primary/secondary line is IBVAP on?** i-LIDS distinguishes
   an analytic certified as the *sole* detection system from one certified only
   as *support* to a human (`domain-research.md`, 6.7). That choice determines
   the alerting, staffing and liability model, and should be made deliberately
   rather than by default.

4. **What does IBVAP emit, and to what?** Ingest is a solved standard; egress is
   not ([7.1](#71-findings)). What does "integration with existing command and
   control systems" mean concretely when the only documented candidate on the
   validation border records outcomes, not detections
   (`ssb-operational-context.md`, 14.10)?

5. **What is the honest answer when the camera cannot support the analytic?**
   Per [6.3](#63-the-dependency-nobody-can-remove-pixels-on-target), some
   fraction of any existing estate cannot deliver some fraction of the named
   capabilities. Is telling the operator that, clearly and per camera, a
   liability to be minimised or the product's most defensible feature?

---

## Document status

**Stage:** 01 — Research → Competitors. Complete for this pass.

**What this document is:** a documentary survey of the global intelligent video
analytics market, based on vendor engineering documentation where available,
vendor marketing where not, and independent or academic sources where they
exist. Four primary vendor PDFs were read in full.

**What this document is not:** a product decision, an architecture decision, a
feature list, or a benchmark. No gap recorded here has been turned into a
requirement, and none should be until `docs/02-product/`.

**Known weaknesses:** no pricing for most vendors (Q-1); no independent accuracy
measurement for any vendor (Q-2); no paywalled analyst or test-lab source read
directly (Q-18); Chinese, Korean, Japanese, Latin American and African vendors
largely absent (Q-19); nothing evaluated hands-on (Q-20).

**Next stage gate:** per [CLAUDE.md](../../../CLAUDE.md) section 2, product
scoping in `docs/02-product/` may proceed on the research completed so far, but
Q-1 through Q-5 in [11](#11-unknowns-requiring-further-research) should be
carried forward as open risks rather than treated as settled.

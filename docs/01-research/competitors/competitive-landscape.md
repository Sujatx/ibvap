# Competitive Landscape — Global Video Surveillance & Intelligent Video Analytics

**Stage:** 01 — Research → Competitors
**Date:** 2026-08-24
**Scope:** The global market for video management software (VMS), video content
analytics (VCA) and AI-driven video surveillance platforms — what exists, what
it depends on, what it costs, and where it does not reach.

This document records what the market already does, on what evidence, and
where the evidence runs out, to ground product scoping in `docs/02-product/`
(per [CLAUDE.md](../../../CLAUDE.md)).

Almost every source here is a **vendor** describing its own product. Vendor
capability claims are recorded as claims, not as verified real-world
performance, and independent sources (standards bodies, peer-reviewed work,
government notices, trade press, competitors) are identified as such inline.
Pricing is largely undocumented publicly — Genetec, Milestone, BriefCam,
Avigilon, Ipsotek, Videonetics and AllGoVision do not publish list prices;
Verkada is the notable exception. Analyst market-share data (Omdia, Novaira
Insights) sits behind paywalls, so only headline claims visible in public
summaries are recorded here, flagged as such. No independent, standardised
accuracy benchmark for any product in this survey was retrieved — IPVM
publishes tests but they are paywalled. This is the single largest evidence
weakness in the document (see [§7](#7-open-questions--research-gaps)).

Per [CLAUDE.md](../../../CLAUDE.md) §4, IBVAP is not India-specific. The SIH/SSB
problem statement defines the initial validation context, not the product's
eventual market. Findings that are specific to a market or force are flagged
inline as **[SIH/SSB]**, **[MARKET:xx]**, or **[BORDER]** (true for
border/frontier surveillance generally); unflagged findings are treated as
globally applicable to intelligent video analytics on existing CCTV.

## Contents

1. [Executive Summary](#1-executive-summary)
2. [Research Objective / Scope](#2-research-objective--scope)
3. [Key Findings](#3-key-findings)
4. [Detailed Findings](#4-detailed-findings)
5. [Implications for IBVAP](#5-implications-for-ibvap)
6. [Risks / Limitations](#6-risks--limitations)
7. [Open Questions / Research Gaps](#7-open-questions--research-gaps)
8. [Conclusions](#8-conclusions)
9. [References](#9-references)

---

## 1. Executive Summary

Every capability named in the official problem statement — human/vehicle
detection, face detection and recognition, ANPR, virtual fencing, behavioural
alerting, and event logging — is already a shipping product from multiple
vendors today (`[C6][C10][C15][C17][C20][C23][C25][C28][C29][C27]`; see
[§3.1](#31-capability-comparison)). There is no capability gap in this market.
Any advantage IBVAP can have must come from architecture, cost, deployability
or honesty about limitations — not from the feature list.

The market's hardest, most universal constraint is optical, not algorithmic:
DORI (IEC EN 62676-4:2015) sets Detection at 25 px/m and Identification at
250 px/m `[C49]`, and a camera installed for human monitoring cannot be
software-upgraded to face identification. This physics binds every vendor,
including IBVAP, identically ([§4.3](#43-the-dependency-nobody-can-remove-pixels-on-target)).

The claim that "advanced analytics requires proprietary hardware" is only half
true, and the false half is already commercialised: Genetec's AutoVu
Flexreader and Milestone's XProtect LPR both do ANPR on ordinary IP cameras
without dedicated ALPR hardware — but both then impose physical constraints
(vehicle speed, mounting angle) that move the dependency from the camera's
silicon to its placement (`[C7a][C53]`; [§4.2](#42-soft-dependencies--capability-works-on-existing-cameras-with-caveats)).
Camera manufacturers (Axis, i-PRO, Hanwha, Verkada, thermal specialists)
structurally tie their best analytics to their own silicon, which is why
VMS-agnostic analytics keeps being reinvented by outsiders and keeps being
acquired by insiders ([§3.6](#36-competitive-patterns)).

Architecturally, the market has already converged on "process locally, ship
metadata centrally" as the answer to bandwidth-constrained, multi-site
deployment — BriefCam Nexus, Ambient.ai, Genetec Cloudlink, Verkada, Eagle Eye
and Milestone Kite all implement variants of it
(`[C12b][C35a][C8a][C21][C33a][C48a]`). The bandwidth achievable this way spans
four orders of magnitude depending on how much of the camera itself the vendor
owns — from Verkada's 20 kbps/camera steady state (achieved by owning the
camera) to Genetec's cloud requirement of recording throughput plus 30%
guaranteed uplink ([§5.1](#51-published-bandwidth-figures-side-by-side)). No
vendor in this survey publishes a power budget for its analytics workload,
despite several mandating specific NVIDIA GPUs — a genuine blind spot in the
industry's published engineering, not just a research gap
([§5.4](#54-power)).

Pricing is almost universally per-camera regardless of licensing model
(perpetual, subscription, or hardware-plus-licence), a shape that penalises
exactly the many-small-sites, low-utilisation-per-camera pattern a distributed
border estate has. Regulation is becoming a market-entry gate that differs by
jurisdiction: NDAA §889 excludes named Chinese vendors from US federal
procurement, India's ER-01/STQC regime bars non-conforming camera sales from 1
April 2026, and the EU AI Act prohibits real-time remote biometric
identification for law enforcement by default — making face recognition a
market-specific capability, not a universal one
([§3.6](#36-competitive-patterns), [§7](#7-open-questions--research-gaps)).

The biggest open questions blocking any competitive positioning are cost (most
vendors publish no pricing), independent accuracy (no standardised benchmark
was retrieved for any product), and disconnected operation (only Irisity
states air-gapped support and only Milestone documents offline licensing — for
the rest it is simply undocumented, and it is decisive for a remote-site
product). These are carried forward as open risks into product scoping, not
treated as settled ([§7](#7-open-questions--research-gaps)).

---

## 2. Research Objective / Scope

The objective was to map the global market for VMS, video content analytics
and AI-driven surveillance platforms against the eight capabilities named in
the official SIH problem statement (`docs/00-project/problem.md`), to
establish: what exists, what it depends on (hardware, bandwidth, licensing,
regulation), what it costs where disclosed, and where the market's evidence
runs out. The research also covers the India-specific competitive set
**[MARKET:IN]** that IBVAP would meet in its initial validation market, and the
border-specific extreme end of the market (dedicated perimeter and
autonomous-tower vendors).

Sources were vendor engineering documentation and marketing (the majority),
independent trade press (IPVM, security-industry outlets), analyst summaries
(Omdia, Novaira — headline claims only, paywalled underneath), academic and
standards material (DORI/IEC, EU AI Act, peer-reviewed anomaly-detection
literature), and internal cross-references to the domain and SSB operational
research already completed in this project. Four vendor PDFs (Milestone
comparison chart, Genetec system requirements guide, Verkada Command Connector
FAQ, Axis ACAP white paper) were retrieved and read in full — these are the
strongest sources in the document because they are primary vendor engineering
documentation with concrete, checkable numbers. No competitor was evaluated
hands-on; everything here is documentary.

Findings are organised by (1) global competitors, (2) the India-specific
competitive set, (3) a capability comparison against the problem statement's
eight named capabilities, (4) architecture and deployment patterns, (5)
hardware/ecosystem dependencies, (6) integration surfaces, and (7) remote and
low-bandwidth deployment considerations — the axis most relevant to a border
context and where the evidence is thinnest.

---

## 3. Key Findings

### 3.1 Capability comparison

Mapped against the eight capabilities named in the official problem statement.
This is not a scorecard — it records what each vendor *claims*, at what
evidence quality, and what the claim depends on. **Y** = claimed with evidence
cited here. **Y\*** = claimed but conditional on the vendor's own hardware.
**P** = partial/adjacent. **—** = no evidence found in this pass (not
necessarily absent).

| Capability | Genetec | Milestone | BriefCam | Axis | Avigilon | Verkada | i-PRO | Videonetics | AllGoVision | Irisity | Ipsotek | Frigate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Human detection & tracking | Y `[C6a]` | P (VMD only) `[C1]` | Y `[C10]` | Y* `[C15a]` | Y `[C17]` | Y (not on thermal) `[C20]` | Y* `[C23]` | Y `[C25b]` | Y `[C28b]` | Y `[C29a]` | Y `[C27b]` | Y `[C32a]` |
| Vehicle detection & classification | Y `[C6a]` | P | Y `[C10]` | Y* `[C15a]` | Y `[C17]` | Y (not on thermal) `[C20]` | Y* `[C23]` | Y `[C25b]` | Y `[C28b]` | Y `[C29a]` | Y `[C27b]` | Y `[C32a]` |
| Face detection | Y `[C6b]` | — | Y `[C10]` | P (ARTPEC-9) `[C15b]` | Y `[C17]` | — | Y* `[C23]` | Y `[C25b]` | Y `[C28b]` | Y `[C29a]` | Y `[C27c]` | P |
| Face recognition | P `[C6b]` | via BriefCam | Y `[C10]` | via partner ACAP | Y `[C18a]` | — | Y* `[C24]` | Y `[C25b]` | Y `[C28b]` | Y `[C29a]` | Y `[C27c]` | — |
| ANPR / ALPR | Y `[C7a]` + Y* `[C4]` | Y `[C53]` | Y `[C10]` | via Vaxtor `[C50]` | Y (dome/bullet only) `[C18b]` | — | P (OCR) `[C24]` | Y `[C25b]` | Y `[C28b]` | — | Y `[C27c]` | — |
| Virtual fence / intrusion | Y `[C6a]` | via 3rd party | Y `[C10]` | Y* `[C15c]` | Y `[C17]` | Y `[C20]` | Y* `[C23]` | Y `[C25b]` | Y `[C28b]` | Y `[C29a]` | Y `[C27b]` | Y `[C32a]` |
| Suspicious / behaviour analytics | P `[C6a]` | — | Y (rules) `[C10]` | P `[C15c]` | P `[C17]` | P | P `[C23]` | Y `[C25b]` | Y `[C28b]` | Y `[C29a]` | Y (SBRE) `[C27b]` | — |
| Night-time movement | — | — | — | P | **No, on thermal** `[C20]` | — | — | — | — | — | P |
| Real-time alerts & event logging | Y `[C6a]` | Y `[C1]` | Y `[C10]` | Y* `[C15c]` | Y `[C17]` | Y `[C22]` | Y `[C24]` | Y `[C25a]` | Y `[C28b]` | Y `[C29a]` | Y `[C27b]` | Y `[C32a]` |

Every one of the eight named capabilities is claimed by multiple vendors, on
public record, today. None is an unsolved problem in the market. The
"night-time movement" column is the emptiest, and this looks like a real
signal rather than a search gap: the one explicit statement found about
thermal streams is negative — Verkada's people/vehicle analytics "are only
supported on visible (or non-thermal) video streams" `[C20]`. Vendors instead
sell night performance as image-sensor quality (Lightfinder, WDR, IR) or as a
dedicated thermal camera, not as a distinct night-time analytic; no vendor page
describing a night-specific analytic was found. Documented environmental
failure modes — rain/fog/snow altering contrast, wind-moved vegetation,
sunrise/sunset/headlight reflections — apply regardless of time of day
`[C52a][C52b]`.

The "suspicious activity" column is the one capability with no consensus
technical solution. Rule-based engines dominate — Ipsotek's SBRE `[C27b]`,
Axis's five fixed scenario types capped at 10 per camera `[C15c][C15d]`,
BriefCam RESPOND's behavioural rules `[C10]` — and peer-reviewed sources
document their high false-alarm rate: "Rule-based models with fixed thresholds
find it difficult to detect actual unusual behaviors in unpredictable
environments, resulting in high false positive rates and missed anomalies"
`[C60a][C60b]`. The alternative, learned anomaly detection, "need[s]
wide-ranging training sets of normal system activities, and any change in the
system's normal patterns must lead to necessary updates of the knowledge base"
`[C60a]`. Vision-language models (Ambient Pulsar, i-PRO Active Guard 3.0) are a
third, newer approach, unproven in this domain `[C35a][C24]`.

### 3.2 Cross-cutting industry patterns

These recur across enough independent vendors to be treated as properties of
the industry rather than of any one company, in descending order of how much
each should inform later stages.

1. **Analytics is a reason to buy hardware, not a portable product.** Axis
   `[C14]`, i-PRO `[C23]`, Hanwha `[C37a]`, Verkada `[C21]`, SightLogix `[C39a]`
   and Teledyne FLIR `[C40]` all bind their best analytics to their own
   silicon — the analytics exist to defend camera margin. This is presumably
   why "software-only analytics on any camera" keeps being reinvented by
   outsiders (BriefCam, Ipsotek, Irisity, AllGoVision, Calipsa, Ambient.ai) and
   keeps being *acquired* by insiders: Canon bought BriefCam, Motorola bought
   Calipsa, Eagle Eye bought Uncanny Vision, Network Optix bought Scailable
   `[C13][C30b][C34][C31b]`.
2. **"Process locally, ship metadata centrally" is settled practice.**
   BriefCam Nexus, Ambient.ai, Genetec Cloudlink, Verkada, Eagle Eye and
   Milestone Kite all implement it (`[C12b][C35a][C8a][C21][C33a][C48a]`; see
   [§5.2](#52-the-distributed-multi-site-pattern)) — it is not an opening.
3. **"We support ONVIF" is a statement of intent, not a capability.** Verkada
   — a *certified* ONVIF Profile S client — still maintains a hardware
   compatibility list, an internal compatibility lab, and a weeks-to-months
   assessment queue, and states plainly that "any ONVIF Profile S camera may
   not work with Command Connector out-of-the-box" `[C20]`. Milestone needed
   1,000+ individually tested devices to converge on one optimised ONVIF
   driver, on top of 16,500+ tested devices and bi-monthly device packs
   `[C2][C3]`. Two of the best-resourced engineering organisations in the
   market both concluded conformance alone is insufficient and built per-model
   compatibility apparatus.
4. **Pixels on target is the hard floor, and it is the same floor for
   everyone.** DORI sets Detection at 25 px/m and Identification at 250 px/m
   `[C49]`; BriefCam needs 12-32 px per object depending on class `[C10]`. A
   camera specified for human monitoring almost certainly was not specified
   for face identification, and software cannot manufacture the missing
   pixels ([§4.3](#43-the-dependency-nobody-can-remove-pixels-on-target)).
5. **The unit of price is the camera, everywhere, under every licensing
   model.** Perpetual (Milestone `[C1]`), one-time-per-sensor (BriefCam
   `[C10]`), perpetual-plus-annual-maintenance (Genetec, low confidence
   `[C9]`), hardware-plus-term-licence (Verkada `[C20]`), or both perpetual and
   recurring (Network Optix `[C31f]`) — all meter per camera. This shape
   penalises exactly the many-sites/few-cameras/low-utilisation pattern a
   distributed border estate has.
6. **Regulation is becoming a market-entry gate that differs by market.** NDAA
   §889 excludes named Chinese vendors (Dahua, Hikvision, Huawei, ZTE, Hytera)
   from US federal procurement, contractor use, and grant funding `[C42]`;
   India's ER-01/STQC regime bars non-conforming camera sales from 1 April
   2026, motivated by concern over foreign chipsets `[C43a][C43d]`; the EU AI
   Act prohibits real-time remote biometric identification in public spaces
   for law enforcement by default from 2 February 2025, with narrow exceptions
   requiring prior authorisation `[C44a][C44b]`. Face recognition is therefore
   a market-specific capability, not a universal one.
7. **Deployment is a site survey by a trained integrator, not a wizard.**
   Genetec and Milestone both run certification programmes (2 days /
   USD 595-895 and 3 days / USD 2,995 respectively `[C51]`); Genetec ships a
   *Camera Requirements Calculator* whose stated purpose includes verifying
   "whether your existing camera setup needs to be modified" `[C4]`; Ipsotek
   shipped an entire narrower product variant (VISuite Core) specifically to
   make rollout "repeatable, plug-and-play" `[C27a]`.
8. **The market is consolidating into camera-plus-VMS-plus-analytics
   conglomerates.** Canon owns Axis, Milestone and BriefCam `[C13a][C13b]`;
   Motorola Solutions owns Avigilon, Pelco and Calipsa `[C30a][C30b]`; Ipsotek
   is part of Atos/Eviden `[C27a]`; Eagle Eye Networks absorbed Uncanny Vision
   `[C34]`; Network Optix absorbed Scailable `[C31b]`. Five such acquisitions
   within eight years means "integrate with the VMS" is a moving target — the
   VMS vendor is frequently also the analytics competitor.
9. **Environment, not algorithm, is often the limiting factor outdoors.**
   Documented failure modes: rain/fog/snow altering contrast and sharpness;
   wind-moved vegetation creating constant pixel changes; sunrise/sunset/
   headlight reflections and shadows read as suspicious movement; wildlife and
   insects `[C52a][C52b]`. IPVM testing "shows lower accuracy in low light and
   with accessories" `[C52c]`. The entire perimeter-thermal industry
   ([§4.6](#46-perimeter-security-specialists-sightlogix-teledyne-flir-senstar))
   arguably exists as the industry's answer to this.
10. **The industry publishes what makes deployment plannable and withholds
    what makes vendors comparable.** Bandwidth, camera counts per server, GPU
    models, ONVIF profiles and codec support are extensively published
    `[C4][C1][C10][C20][C21]`. Pricing, accuracy, false-alarm rates and power
    draw are almost never published.

---

## 4. Detailed Findings

### 4.1 Market overview

Public estimates for the video surveillance market (hardware + software)
diverge widely — which is itself informative:

| Source | 2025 base | Forecast | CAGR |
|---|---|---|---|
| MarketsandMarkets `[C45a]` | USD 56.11 bn (2025) | USD 88.06 bn by 2031 | 7.8% |
| The Business Research Company `[C45b]` | USD 69.09 bn (2025) | USD 116.23 bn by 2030 | 10.9% |
| Fortune Business Insights `[C45c]` | USD 83.71 bn (2025) | USD 261.65 bn by 2034 | 13.5% |

For the narrower video analytics segment: Grand View Research puts it at
USD 12.71 bn (2024) → USD 37.84 bn by 2030 at 19.5% CAGR `[C45d]`; Mordor
Intelligence puts it at USD 12.39 bn (2025) → USD 33.74 bn by 2030 at 22.18%
CAGR `[C45e]`. The absolute figures are not directly usable for planning, but
the direction is consistent: every independent estimator has analytics growing
roughly twice as fast as surveillance overall (analytics CAGRs cluster
19-22% against surveillance's 8-13%). None of the public summaries break out
the specific segment IBVAP would sit in — software analytics retrofitted onto
an existing third-party camera estate, as distinct from analytics bundled with
new cameras or a new VMS.

On market share, Omdia publishes a *Video Surveillance & Analytics Market
Share Database* segmented by World, World-excluding-China, EMEA, Americas,
China and Rest of Asia & Oceania `[C46a]` — the segmentation itself is
evidence that China is treated as a separate market by the industry's
principal analyst. Verkada states it is ranked #1 worldwide in VSaaS by Omdia
`[C46b]` (a vendor citing a paywalled report, unverified); Videonetics states
it is "India's #1 VMS provider" and top-10 in Asia for seven consecutive years
`[C25a]` (vendor claim, ranking source unstated). Actual revenue-based market
shares for Genetec, Milestone, Hanwha, Bosch, Axis, Avigilon, Hikvision and
Dahua sit behind the paywalled Omdia and Novaira databases and were not
obtained `[C46a][C46c]`.

Structurally, the market is consolidating into a small number of
camera-plus-VMS-plus-analytics conglomerates (Canon, Motorola, Bosch, Hanwha,
Hikvision/Dahua) plus a thinner layer of independent, VMS-agnostic analytics
vendors that survive by staying camera- and VMS-agnostic (see pattern 8 in
[§3.2](#32-cross-cutting-industry-patterns)).

### 4.2 Global competitor profiles

**Genetec — Security Center.** A unified enterprise platform combining video
(Omnicast), access control (Synergis), ALPR (AutoVu) and analytics
(KiwiVision) on a role-based distributed architecture: Directory
(authentication/config), Archiver (recording), Media Router/Gateway (stream
distribution), expansion servers, and Federation for multi-site `[C5]`.
Genetec's own sizing guide gives concrete capacity figures:

| Server type | Minimum profile | Recommended profile |
|---|---|---|
| Directory & Archiver (video only) | 50 cameras / 50 Mbps | 100 cameras / 200 Mbps |
| Standalone Archiver (video only) | 75 cameras / 75 Mbps | 300 cameras / 500 Mbps |
| Standalone Redirector | 50 cameras / 50 Mbps | 475 cameras / 475 Mbps |
| Directory + Archiver + Access Manager | 50 cameras / 50 Mbps + 64 readers | 100 cameras / 200 Mbps + 200 readers |

The "Recommended" profile assumes an Intel Xeon Silver 4210-class server;
above 500 cameras Genetec directs buyers to its own Streamvault rackmount
appliances (500-1,000 cameras or 500-2,000 Mbps) `[C4]`. Stated deployment
constraints: systems above 300 cameras/1000 readers must isolate the Directory
on a dedicated server; software motion detection can cut maximum capacity by
up to 50%; a VM has 20% less capacity than equivalent physical hardware; the
first Fusion Stream encryption certificate on an Archiver cuts its capacity by
30% (300 cameras to 210), 20 certificates cut it to 96; and the platform
requires Windows (10/11 Pro or Server 2016/2019/2022) plus Microsoft SQL
Server `[C4]`.

KiwiVision is Genetec's analytics module set — area protection, perimeter
intrusion, object detection, direction control, Privacy Protector (dynamic
anonymisation with authorised un-masking), People Counter, and Camera
Integrity Monitor (tampering/obstruction/failure detection) `[C6a][C6b]`.
Genetec states VMs are "not recommended" for KiwiVision due to "typically high
performance requirements"; every KiwiVision server requires an AVX-compatible
processor; and GPU acceleration ("a 4 GB+ CUDA-capable NVIDIA card" plus a
separate GPU licence pack) is available only for the Tailgating detection and
People counting scenarios `[C4]`. Genetec supplies a *KiwiVision Camera
Requirements Calculator* to "verify whether your existing camera setup needs
to be modified" — Genetec's own tooling assumes retrofitting analytics onto an
existing estate may require changing the cameras `[C4]`.

AutoVu (ALPR) is sized in "AutoVu camera units" (50 minimum, 100 recommended,
up to 300 across three ALPR Managers, capped at 100 per Archiver) and is built
around Genetec's own Sharp/SharpX cameras `[C4][C7c]`. However, Genetec also
ships **AutoVu Flexreader** (announced April 2018), a software add-on that
turns existing supported fixed IP cameras into plate readers "without
dedicated ALPR hardware" — but stated to be optimised for vehicles moving up
to 30 mph/50 km/h `[C7a][C7b]`.

For cloud/edge, Genetec sells Cloudlink appliances (210, 310, 2210) — Linux
based, "push processing and storage to the edge," explicitly addressing
"support for existing devices that do not enable direct-to-cloud connectivity,
and the need to maintain local operation during connectivity disruptions"
`[C8a][C8b][C8c]`; Security Center SaaS is the hybrid-cloud offering `[C8d]`.
Genetec Cloud Storage requires "a guaranteed uplink that is 30% greater than
the video throughput recorded by all Archiver roles," with 99.9%+ SLA and
<150 ms latency to Azure — a 100 Mbps Archiver needs 130 Mbps guaranteed
uplink `[C4]`.

Genetec does not publish list pricing. Third-party (low-confidence, competitor-
adjacent) estimates put Omnicast video licences at roughly USD 150-400
one-time per channel plus an annual Software Maintenance Agreement of 18-22%
of licence value, and Streamvault appliances at USD 8,000-30,000+ per site
`[C9]`. Genetec claims to be "the only VMS vendor in the world to hold UL
cybersecurity certification" (2020, time-bound claim) `[C57]`. IPVM prices
Genetec classroom training at 2 days for USD 595-895 `[C51]`.

**Milestone Systems — XProtect.** The reference "open platform" VMS,
camera-agnostic by design, with object analytics supplied by third parties or
by BriefCam (now a Milestone product). The 2026 R1 comparison chart shows four
editions:

| | Express+ | Professional+ | Expert | Corporate |
|---|---|---|---|---|
| Deployment | Single server | Centrally managed multi-server | Centrally managed multi-server | Centrally managed distributed sites |
| Max IP devices per recording server | **48** | Unrestricted* | Unrestricted* | Unrestricted* |
| Recording servers per system | **1** | Unrestricted* | Unrestricted* | Unrestricted* |
| Edge Storage + Scalable Video Quality Recording | no | yes | yes | yes |
| Media DB encryption and digital signing | no | no | yes | yes |
| Evidence Lock | no | no | no | yes |
| Federated Architecture | no | no | Remote site | Central/Remote |
| Interconnect | Remote site | Remote site | Remote site | Central/Remote |
| Hardware-accelerated VMD (NVIDIA) | no | no | yes | yes |
| GDPR ready | no | no | yes | yes |

(*"Unrestricted" is qualified in the source as "depending on system
configuration.") All editions are perpetually licensed `[C1]`.

Device openness is broad: ONVIF/PSIA in every edition, a universal driver for
generic devices, 11,000+ supported IP devices `[C1]`; separately Milestone
states conformance with ONVIF profiles S, T, G and M, 16,500+ devices on the
supported list, and 1,000+ individually tested ONVIF devices consolidated into
"a single optimized driver," with device packs shipping every two months
`[C2][C3]`. Every edition, including the 48-camera entry tier, includes MIP
SDK integration, REST API configuration, WebRTC streaming, WebSocket/webhook
event integration, and **Milestone AI Bridge for Intelligent Video Analytics
integrations** — a documented bridge that forwards camera streams from
XProtect to third-party IVA applications **deployed as Docker containers** and
accepts events/metadata/video back `[C1][C47]`. This is a formal, documented,
container-based ingress for third-party analytics into the largest open VMS.
Offline license activation and offline device add/replace are supported in
every edition, including Express+ `[C1]`.

XProtect LPR is a licensed extension that Milestone states "works with all
variants of XProtect as well as all cameras supported by XProtect... you do
not need a purpose-built LPR camera" — recommending mounting at no more than
30 degrees off the vehicle, shipping 200+ generic/country modules with 5
country licences included, and warning the recognition logic "is processor
intensive, and varies significantly dependent on the environmental conditions,
camera settings and other parameters" `[C53]`. XProtect itself ships built-in
Video Motion Detection (auto-adjustable sensitivity, exclusion zones, motion
metadata) but not object classification `[C1]`; "XProtect Rapid REVIEW"
(BriefCam-derived) is marked Discontinued in all four editions in the 2026 R1
chart, coinciding with BriefCam's full absorption into Milestone `[C1][C13b]`.
Milestone reported USD 340 million net revenue in 2025 and states it formally
integrated BriefCam and Arcules VSaaS into the Milestone product line that
year `[C58]`. Milestone Kite/Arcules is the VSaaS line, marketed for "multiple
satellite and remote locations" with "flexible hybrid video storage... all
dependent on available bandwidth" `[C48a][C48b]`; XProtect 2025 R1 extended
the Arcules connection to Corporate, Expert and Professional+ `[C48c]`.
Milestone's per-device licence price and Milestone Care subscription cost are
not published. IPVM lists Milestone Advanced training at 3 days for
USD 2,995 `[C51]`.

**BriefCam (Canon/Milestone).** The best-known VMS-agnostic video content
analytics product — the closest existing analogue to "software that makes an
existing CCTV estate intelligent." Modules: REVIEW (video synopsis —
"superimpose objects on a stationary background, simultaneously displaying
events" for rapid forensic review), RESEARCH (BI dashboards), RESPOND
(real-time alerting on face recognition, vehicles, and behavioural rules)
`[C10]`. BriefCam is "VMS-agnostic but integrates with supported systems via
direct connectors," with a generic Video Integration API for unsupported
systems, and a tiered integration model across 30+ supported platforms: **L1**
forensic/post-event, **L2** real-time, **L2a** real-time alerts, **L3**
client/UI integration, **L4** workflow integration. Milestone XProtect is the
only L4 integration; Genetec Security Center is L3; Bosch BVMS, Nx Witness,
Qognify Ocularis and Avigilon Unity are L2/L2a `[C10][C11]` — "integrates with
30+ VMS" does not mean the same thing 30 times.

NVIDIA GPUs are mandatory ("Intel, AMD or any other non-NVIDIA GPUs not
supported"); GPU count scales with resolution and daily processing hours;
each GPU is dedicated to either real-time or on-demand processing, not both;
VMs are "technically possible but not recommended for production" `[C10][C10b]`.
Video constraints: minimum resolution CIF (352×240), native max 4K, 8-30 FPS
recommended (degraded tracking outside that range), minimum object size
12-32 px depending on class `[C10]`. Licensing is one-time purchase (optional
annual maintenance after year one), four variants (Investigator, Insights,
Rapid Review, Protect), and licensed **per camera sensor** — a multi-sensor
camera consumes multiple licences `[C10]`. **BriefCam Nexus** is a hub-and-site
architecture: each Site processes video locally in real time or on demand,
while a central Hub "aggregates RESPOND alerts and RESEARCH metadata generated
at each Site" `[C12]` — "a central server and then you have a hub at each site
processing the video locally, and then just sending the metadata back
centrally" `[C12b]`. This is the architectural pattern most relevant to
distributed, bandwidth-poor estates, and a major incumbent already ships it.
BriefCam's list pricing is not published anywhere retrieved.

**Axis Communications.** A camera manufacturer whose analytics strategy is
on-camera and Axis-only. ACAP (AXIS Camera Application Platform) requires Axis
ARTPEC SoCs with a DLPU/MLPU; ACAP applications cannot run on non-Axis cameras
`[C14]`. AXIS Object Analytics is preinstalled on compatible cameras (firmware
10.2+ on MLPU models), detects/classifies humans, vehicles and vehicle types,
across five scenario types (object in area, line crossing, time in area,
crossline counting, occupancy in area), capped at 10 scenarios per camera
`[C15a][C15b][C15c][C15d]`. Axis frames the benefit as bandwidth reduction and
lower central-server cost from local analysis `[C14]`. Axis also publishes the
industry's clearest statement of the pixel-density constraint: DORI (IEC EN
62676-4:2015) defines Detection 25 px/m, Observation 62 px/m, Recognition
125 px/m, Identification 250 px/m `[C16][C49]` — a physics-level constraint
that binds every vendor equally, including IBVAP. Axis is a camera competitor
rather than a platform competitor, but arguably the most important
dependency-shaper in the market: an estate of ARTPEC cameras already has
classification analytics on board, and an estate of anything else does not.

**Avigilon (Motorola Solutions).** Camera + VMS + analytics across two product
lines — Unity (on-premise, formerly ACC) and Alta (cloud-native, formerly
Ava). Unity Video is stated to be "compatible with any ONVIF compliant device"
`[C17]`. Appearance Search locates a person or vehicle "using a physical
description, uploaded image, or previous recorded footage"; LPR Analytics
automates plate reading `[C17][C18a]`. However, Alta Video LPR "requires the
use of a dome or bullet-type of camera, and cannot be configured to use
panoramic, 360, fisheye, or PTZ cameras" (third-party dome/bullet cameras are
supported via Alta Cloud Connectors) `[C18b]`. A notable ecosystem-lock
artefact: to use an Avigilon Alta cloud-native camera with a third-party VMS
via ONVIF, "you will need to load the camera with Avigilon Unity firmware
which is available from Avigilon technical support" `[C19]`. Which specific
Unity analytics function on third-party ONVIF cameras versus requiring
Avigilon's own H4/H5/H6 cameras is not stated on the public supported-devices
page, which instead directs buyers to sales engineering `[C17]`.

**Verkada.** Proprietary hybrid-cloud: cameras, storage and cloud are one
vertically integrated product, with a bridge appliance for third-party
cameras. The standout claim is bandwidth: Verkada cameras use "a bandwidth
uplink of no more than 20 kbps per camera" in steady state, sending encrypted
thumbnails and metadata to the cloud roughly every 20 seconds, with video
streaming only on request (~300 kbps for 720p, ~1 Mbps for full HD) — "over
100 cameras on the same connection (~only 2 Mbps)" `[C21]`. Cameras "store up
to 30-365 days of continuous video on the device itself" and continue
recording during internet outages `[C21][C22]`. This is the strongest
documented low-bandwidth architecture in the market, and it is achieved by
owning the camera.

For third-party cameras, Command Connector appliances are sold with published
prices:

| Model | Onboard storage | Channels (≤5MP) | Channels (4K) | Price (USD) |
|---|---|---|---|---|
| CC300-4TB | 30 days | 10 | 5 | 2,999 |
| CC300-8TB | 60 days | 10 | 5 | 3,499 |
| CC500-8TB | 30 days | 25 | 12 | 5,499 |
| CC500-16TB | 60 days | 25 | 12 | 6,499 |
| CC700-16TB | 30 days | 50 | 25 | 8,499 |
| CC700-32TB | 60 days | 50 | 25 | 10,499 |

Plus a per-channel licence (1/3/5/10-year terms) "priced the same as existing
Command video security licences" `[C20]`. Verkada's own FAQ is unusually
candid about the caveats: third-party cameras through Command Connector do
**not** "receive the same features and capabilities as native Verkada
devices"; compatibility is governed by a Hardware Compatibility List, and an
unlisted camera "may work" but "compatibility is not guaranteed" and "Verkada
will not be able to provide support"; adding a camera to the list requires a
Request for Compatibility Assessment that "can take anywhere from weeks to
months"; Command Connector "currently only supports H.264 video encoding,"
caps at 20 RTSP channels for non-ONVIF cameras, "does not currently utilize
any events emitted by non-Verkada cameras," and does not allow custom video
configurations on third-party cameras; it "does not integrate with other VMS
or NVR appliances" (running alongside a legacy VMS requires the cameras to
stream to two NVRs); and — most materially for a border/night context — while
"thermal video channels are visible in Command," **"people and vehicle
analytics features are only supported on visible (or non-thermal) video
streams"** `[C20]`. This thermal exclusion is directly material to night-time
analytics: the leading cloud platform runs no person/vehicle analytics on
thermal streams at all. Air-gapped camera networks are explicitly
accommodated at the network level (a second Ethernet port for an isolated
camera VLAN), though the platform itself still requires the cloud `[C20]`.

**i-PRO (formerly Panasonic Security).** Edge-AI camera manufacturer plus
server-side aggregation (Active Guard) plus its own VMS (Video Insight). The
edge AI solution "requires i-PRO network cameras with AI capabilities," with
no indication of non-i-PRO compatibility `[C23]`. Active Guard "operates on
metadata and imagery from Edge AI cameras" — i.e. it consumes camera-produced
metadata and best-shots, not raw third-party video; version 3.0 adds a
server-based generative-AI engine for natural-language queries over best-shot
images `[C23][C24]`. Stated analytics: face/human/vehicle/bicycle detection,
AI-based VMD (line-cross, loitering, direction), sound classification (gunshot,
scream, glass break), AI privacy guard (real-time face mosaic),
occupancy/crowd congestion, scene-change detection, smart coding for bandwidth
reduction `[C23]`. Active Guard integrates with Genetec Security Center,
Milestone XProtect, Luxriot EVO, Nx Witness and i-PRO Video Insight
`[C23][C24]`. i-PRO is the clearest example of the industry's dominant
commercial pattern: the analytics are the reason to buy the cameras, and the
server software is deliberately valueless without the vendor's own edge
hardware.

**Bosch and Hanwha Vision.** Hanwha's Wisenet 9 SoC "features dual neural
processing units, with one NPU handling image processing while the other
focuses on object detection and advanced analytics," filtering events at the
edge before they leave the device; WiseDetector is a machine-learning feature
that "expands the object types that can be detected by AI to specific objects
beyond pre-defined ones" `[C37a][C37b]`. Bosch IVA Pro is Bosch's edge video
analytics line, but this pass only retrieved trade commentary on it, not
primary Bosch documentation `[C38]` — treat as weakly sourced. Both vendors
appear to occupy the same structural position as Axis and i-PRO: analytics as
a camera differentiator, not a portable software product.

**Ipsotek (Eviden/Atos).** VMS-agnostic analytics explicitly positioned on
existing CCTV. VISuite is "an AI-powered video analytics platform, leveraging
existing CCTV cameras for real-time security and operations," claiming 600+
customers over 20+ years, built around a patented Scenario-Based Rule Engine
(SBRE) `[C27b]`. **VISuite Core** (2025) is a newer, narrower product — "a
carefully curated set of pre-built capabilities... through a repeatable,
plug-and-play deployment model suited to distributed estates and partner-led
rollouts" `[C27a]` — evidence that a 20-year incumbent found its own
general-purpose platform too hard to deploy at scale and shipped a constrained
variant to fix it. Ipsotek VISuite AI is a listed Milestone technology
partner covering analytics, face recognition, ANPR and forensics `[C27c]`.
Ipsotek's hardware requirements, licensing model and pricing are not published
in anything retrieved.

**Irisity (IRIS+).** Open-platform, camera-agnostic analytics with an
unusually explicit deployment matrix. "IRIS+ is an Open Platform for AI video
analytics and therefore works with any type of camera brand and model," via
RTSP/ONVIF, "including analog cameras via DVRs" `[C29a][C29b]`. Deployment
options stated: on-premise (including **air-gapped**), cloud-hosted, hybrid,
and edge; hardware platforms "x86 with NVidia GPU or AI cameras"; claimed
scaling "from small 5-10 camera installations to multi-site, multi-tenant...
supporting thousands of cameras" `[C29a][C29b]`. Irisity is the only vendor
found in this pass that states air-gapped operation as a first-class supported
deployment mode. Its per-camera pricing and measured accuracy are not
published.

**Calipsa (Pelco/Motorola Solutions).** Pure-cloud false-alarm filtering
layered on any existing IP camera, deliberately narrow in scope. Calipsa's
"cloud-based technology allows customers to add AI to existing IP-based
cameras without additional hardware," is "100% cloud-based... cloud agnostic,"
and works "by analyzing frames, not video" — "it takes about 300 Kb of
bandwidth per event" `[C30c][C30d]`. Claimed performance: reduces unwanted
alarms "by up to 95%" / "by 93% - with 99% accuracy at spotting alarms
containing people and vehicles" (vendor claim, no methodology or independent
verification retrieved) `[C30c][C30d]`. Calipsa is the clearest existing proof
that a commercially viable product can be built on event frames rather than
video streams.

**Eagle Eye Networks.** Open cloud VMS ("VSaaS") with an on-site bridge, for
existing analog and IP cameras. Some bridges "support both analog and IP
cameras on the same device, with analog cameras connecting directly to the
bridge without external encoders" via BNC `[C33a]`. The Bridge records
locally first (for buffering and backup against internet failure) and
synchronises to cloud "when bandwidth is available" `[C33a][C33b]`. Eagle Eye
recommends 400 kbps per IP camera as a starting bandwidth figure, though
third-party guidance elsewhere cites 1-2 Mbps per HD camera and 2-4 Mbps per
4K camera (the two figures are not reconciled and come from different
sources) `[C33a]`. Eagle Eye acquired **Uncanny Vision** (Bangalore) in 2021,
whose core product was an ANPR engine claimed to "consistently deliver very
high accuracy even in challenging conditions" `[C34]`.

**Network Optix (Nx Witness/Nx Meta/Nx AI Manager).** A platform for
*building* video products, not only a product — structurally different from
every other entry here. Nx Meta "is an IP video management platform that
allows users to discover, stream, configure and manage IP cameras, RTSP
streams, and I/O devices" `[C31a]`. The `nx_open_integrations` and `nx_open`
repositories are published on GitHub under Mozilla Public License 2.0; the Nx
Desktop client is open source; a TestCamera tool emulates a network camera so
integrations can be built without hardware or a licence `[C31c][C31d][C31e]`.
Both perpetual (Pro) and recurring (Enterprise) licences exist `[C31f]`. **Nx
AI Manager** is a plugin that runs AI/ML models on edge devices against live
video, supports GPU/VPU/CPU environments, imports models "from virtually any
training platform," and supports OTA mass deployment and fleet management — it
originated as the Dutch startup Scailable, acquired January 2024 `[C31b]`.
Network Optix is the closest thing in the market to an *ingredient* rather
than a *competitor* — and therefore also the fastest route for anyone else to
build a competing product.

**Ambient.ai.** Premium enterprise "intelligence layer" on existing cameras,
built around a vision-language model ("Ambient Pulsar") that "reasons about
video in real time to flag actual threats, not motion events." It "operates as
an intelligence layer on top of existing camera and access control
infrastructure, with AI processing running on edge appliances at each site and
a cloud console for monitoring, multi-site management and analytics"
`[C35a][C35b]`. "All we need to begin video processing is access to your IP
camera streams"; stated deployment range is ~100 to 10,000+ cameras across
multiple sites `[C35a][C35b]`. Pricing is quoted per deployment ("built around
camera count, edge-appliance hardware, and the AI modules you turn on") and
"sits at the premium end of the market" (third-party pricing guide, low
confidence) `[C35a]`. Ambient.ai is the market's clearest signal that
vision-language models are being commercialised for the "suspicious activity"
problem that rule engines handle badly.

**Gorilla Technology.** Edge AI video analytics combined with VMS in a single
appliance, sold into city and national security programmes. IVAR
("Intelligent Video Analytics Recorder") is "an all-in-one edge AI
surveillance solution which combines intelligent video analytics with VMS,"
stated to "utilize existing CCTV video data" to identify people, vehicles and
objects and detect suspicious events `[C36a][C36b]`. Gorilla also ships EVMS
(Edge Video Management System) and an Edge AI line "for harsh outdoor
environments"; IVAR is listed on the Milestone Marketplace `[C36c][C36d][C36e]`.
Gorilla cites a case reducing investigation time "from over 185 hours to just
15" (single vendor case study, unverified) `[C36a]`.

**Perimeter-security specialists (SightLogix, Teledyne FLIR, Senstar).**
Relevant because perimeter intrusion **[BORDER]** is their entire market, and
because they represent the "sensor-plus-analytics" answer the problem
statement's premise implicitly avoids. SightLogix SightSensor smart thermal
cameras "detect, analyze and communicate real-time intruder activity over
perimeters and outdoor sites... with low nuisance alerts over large
distances," with dual-sensor models combining thermal and visible AI
classification `[C39a]`. Teledyne FLIR's FC-Series AI is "a thermal security
camera with onboard AI analytics that accurately classifies humans and
vehicles for early intrusion detection," combining DNN- and motion-based
analytics `[C40]`. Senstar specialises in physical perimeter intrusion
detection, particularly fence-mounted and buried cable sensors `[C39b]`. This
segment's existence — built entirely around nuisance-alarm reduction and
range — suggests outdoor perimeter detection at long range is hard enough that
a whole industry sells dedicated thermal hardware to avoid doing it on
general-purpose CCTV.

**Anduril — the border-specific extreme [BORDER].** CBP awarded Anduril a
USD 363 million one-year contract in December 2025 for 200+ Extended Range
Sentry Towers (40+ delivered so far at 15+/month) `[C41a][C41b]`. The 80-foot
expeditionary tower has "high-performance sensors to autonomously detect,
classify, and track objects of interest at ranges exceeding 5 miles," modular
mission nodes and power sources, and "can be erected in less than three
hours" `[C41a][C41c]`. Over 350 Standard Range Sentry systems are reported
operating, having "autonomously identified hundreds of thousands of border
crossings"; by late 2024 the 300th deployment covered "30 percent of the U.S.
southern land border" `[C41a][C41d]`. This is the reference point for what a
well-funded border programme buys when it is *not* constrained to existing
infrastructure — purpose-built autonomous towers — and it is the direct
inverse of the IBVAP premise. It works, at scale, today.

**Open source (Frigate, and the general-purpose stack).** Frigate is "an open
source NVR built around real-time AI object detection, with all processing
performed locally"; it supports Google Coral TPU, Intel OpenVINO and NVIDIA
GPUs; "any IP camera with RTSP works"; it uses a dual-stream pattern
(high-resolution stream recorded, low-resolution substream fed to detection);
and offers event-based/24-7 recording with object-based retention, sub-second
WebRTC/MSE live view, and MQTT integration `[C32a]`. It has been deployed on
NVIDIA Jetson hardware with hardware acceleration `[C32b]`. Frigate arguably
defines the credible free floor of this market — RTSP ingestion, on-device
object detection, event recording and alerting, at zero licence cost, on
hardware costing tens to low hundreds of dollars — and any paid product must
be worth more than that difference. Whether Frigate or comparable open-source
stacks are usable at the multi-site, multi-user, audited, evidentiary standard
a security force needs was not addressed by anything retrieved.

**Newer camera-agnostic cloud entrants.** Coram AI is described (in its own
comparison content) as "a cloud, camera-agnostic platform built around
large-model natural-language search that works with any IP camera with no
rip-and-replace, auto-discovering ONVIF cameras and bulk-importing RTSP
streams"; Spot AI is positioned similarly `[C54]`. These descriptions come
from competitor-authored comparison content and should be treated as evidence
that the positioning exists and is contested, not as evidence of capability.
"Natural-language search over any existing camera" looks set to become the
standard pitch of every new entrant (alongside Ambient Pulsar `[C35a]` and
i-PRO Active Guard 3.0's generative-AI query engine `[C24]`), so it is unlikely
to remain a differentiator for long.

### 4.3 The India-specific competitive set [MARKET:IN]

This section describes the competitive set IBVAP would meet in its initial
validation market — not the boundary of its product.

**Videonetics** markets a Unified Video Computing Platform (UVCP) — VMS, Video
Analytics, Traffic Management System and Face Recognition System, "powered by
an indigenously developed True AI and deep learning engine" `[C25a][C25b]`.
ANPR is bundled with Red Light Violation and Speed Violation Detection
`[C25b]`. Its Face Recognition System is stated to be "trained with a large
database of faces covering diverse demography, and works well with facial
features of the Indian subcontinent" — the clearest instance in this research
of a competitor claiming market-specific model tuning as a differentiator, a
claim IBVAP would have to meet or beat in this market `[C25b]`. Videonetics
states deployment "across all 28 districts of Andhra Pradesh" as a state-wide
real-time intelligence network, and is an ONVIF member `[C25c][C25d][C25e]`.
Its hardware requirements, per-camera pricing, whether it runs unmodified on
existing third-party cameras, and whether the Andhra Pradesh deployment used
existing or newly procured cameras are all undocumented in what was retrieved.

**Matrix Comsec** (SATATYA) is an IP video surveillance portfolio — cameras,
NVRs, a 64-bit .NET enterprise NVR with inbuilt VMS `[C26a]`. Claimed
analytics: intrusion detection, human/vehicle classification, loitering, line
crossing, crowd density, object left/removed detection, fire/smoke detection,
PPE compliance, and ANPR `[C26b]`. Matrix announced a partnership with Yotta
for "Drishticam AI Powered Cloud Native Video Surveillance as a Service," with
encrypted cloud recording, configurable retention and multi-channel
notifications `[C26b][C26c]`. Matrix is primarily a hardware vendor extending
into analytics — structurally the same position as Hanwha or i-PRO, not a
software-only competitor.

**AllGoVision**, a Bangalore-founded (2009) video analytics company with
presence in the UK, USA, UAE and Korea `[C28a]`, makes an important
architectural claim: it "can be installed either in the same machine as VMS or
in a separate machine and can take video feed directly either from camera or
from VMS," is integrated with "10+ major VMS like Milestone, Genetec,
Honeywell EBI, HUS, DVM, Wavestore," and — notably — its **virtual camera** "is
created based on ONVIF standards and can be added in any VMS which supports
ONVIF" `[C28b][C28c]`. This ONVIF virtual-camera pattern is worth noting on
its own: rather than writing a plugin per VMS, the analytics engine presents
its annotated output as an ONVIF camera that any ONVIF VMS can already
consume. AllGoVision claims "50 plus basic and advanced Video Analytics
features" covering intrusion, counting, crowd management, traffic and face
recognition, working "with existing security cameras... without requiring
specialized hardware" `[C28b][C28d]`.

Four smaller Indian players surfaced without deliberate search effort: **Vehant
Technologies** (Security, Traffic Enforcement and Sovereign Vision AI, with
CCTV software enabling e-challan systems integrated with government databases)
`[C55a]`; **Staqu** (Gurugram, 2015; JARVIS, "a software platform that
processes peripheral CCTV footage into insights," across retail,
manufacturing, infrastructure, hospitality, public sector and smart cities)
`[C55b][C55c]`; **Wobot Intelligence** (2017; video analytics for retail, food
service, manufacturing and hospitality) `[C55d]`; and **Uncanny Vision**
(acquired by Eagle Eye Networks in 2021 `[C34]`, an Indian analytics company
absorbed into a US cloud VMS). The Indian analytics segment is crowded with
software-only players already claiming exactly the "AI on existing CCTV"
position the problem statement describes.

**The Indian regulatory factor [MARKET:IN].** India's MeitY introduced
Essential Requirements for the Security of CCTV Cameras (ER-01) in a March
2024 Gazette notification, requiring testing/certification by STQC covering
physical security, access control, network encryption, data integrity and
penetration testing, referencing OWASP 4.0 Level 2 and a Trusted Supply Chain
framework `[C43a][C43b][C43c]`. The relaxation permitting sale of
non-conforming cameras has been withdrawn: from 1 April 2026, no sale of
non-conforming CCTV cameras is permitted `[C43d]`. The stated background is
"security concerns regarding devices using foreign chipsets — security
agencies were concerned the chipsets may have allowed the cameras to send data
to servers located outside of India" `[C43a]`. At least one industry outlet
argues the STQC requirement "monopolises the CCTV industry in India" (trade
advocacy, recorded as evidence the requirement is contested, not as a finding
on its merits) `[C43e]`. ER-01 as documented applies to cameras, not to
analytics software, so it constrains the installed base IBVAP would run on
rather than IBVAP itself — but whether it applies to software has not been
independently verified, and the requirement means the Indian installed base
will churn.

### 4.4 Architecture and deployment

Four distinct inference-location patterns exist in the market; every vendor
examined uses one or a combination — and they are not really four choices so
much as one continuous trade of *where you pay* (camera silicon, site
hardware, bandwidth, or scope):

| Pattern | Who does it | What it needs | What it costs you |
|---|---|---|---|
| **A. On-camera (edge, in-sensor)** | Axis ACAP `[C14]`, i-PRO `[C23]`, Hanwha `[C37a]`, Teledyne FLIR `[C40]`, SightLogix `[C39a]` | The vendor's own camera silicon | Total camera lock-in; no retrofit path |
| **B. On-site server/appliance** | Genetec KiwiVision `[C4]`, BriefCam `[C10]`, Irisity `[C29a]`, Ambient.ai `[C35a]`, Gorilla IVAR `[C36a]`, Frigate `[C32a]` | x86 + NVIDIA GPU at each site | Hardware, power, cooling, maintenance per site |
| **C. On-site bridge, cloud brain** | Verkada Command Connector `[C20]`, Eagle Eye bridge `[C33a]`, Genetec Cloudlink `[C8a]`, Milestone Kite `[C48a]` | Appliance + reliable uplink | Recurring per-camera licence; uplink dependency |
| **D. Pure cloud, event-driven** | Calipsa `[C30c]` | Internet only | Only works for narrow, event-triggered scopes |

**5.2 The distributed multi-site pattern.** Three vendors independently
converged on the same structure: BriefCam Nexus (hub + sites, "a hub at each
site processing the video locally, and then just sending the metadata back
centrally" `[C12b]`), Ambient.ai ("AI processing running on edge appliances at
each site and a cloud console for monitoring, multi-site management, and
analytics" `[C35a]`), and Genetec Cloudlink (appliances that "push processing
and storage to the edge," maintaining "local operation during connectivity
disruptions" `[C8a][C8c]`). Milestone offers two distinct multi-site forms:
Federated Architecture (Expert/Corporate only) and Interconnect (all editions,
Corporate as the only permitted central site) `[C1]`. "Process locally, ship
metadata centrally" is settled industry practice, not an opening.

**Recording ownership** is a structural fork. Vendors that own recording:
Genetec Archiver `[C4]`, Milestone Recording Server `[C1]`, Verkada Command
Connector's onboard RAID `[C20]`, Eagle Eye Bridge `[C33a]`, Gorilla IVAR
`[C36a]`, Frigate `[C32a]`. Vendors that do not: BriefCam (reads from the VMS
or its own API) `[C10]`, Calipsa (events only) `[C30c]`, AllGoVision (feed
from camera or VMS) `[C28b]`, Ipsotek `[C27b]`. Owning recording is the
heavier commitment (storage sizing, retention policy, evidentiary chain, RAID,
failover) but also what makes evidence management and offline operation
tractable; not owning it is easier to sell but dependent on somebody else's
VMS being present and healthy.

**OS/platform dependencies.** Genetec Security Center runs on Windows only and
requires Microsoft SQL Server `[C4]`. Milestone XProtect runs servers "as
Windows Services" and is available on AWS Marketplace `[C1]`. Genetec's own
Cloudlink appliances run "a secure, Linux-based operating system" — Genetec's
edge line escapes the Windows dependency its core platform has `[C8a]`.
Frigate is distributed as Docker containers `[C32a][C32c]`; Milestone AI
Bridge expects third-party analytics "deployed as docker containers" `[C47]`.
Containerised Linux appears to be the emerging norm for the analytics layer
even where the VMS layer is Windows.

**Virtualisation.** Genetec: VMs have 20% less capacity than equivalent
physical hardware; do not exceed six VMs per host or four video-intensive VMs
per host; assign at least 16 GB RAM per VM and keep 16 GB unallocated; do not
exceed 300 Mbps per archiving VM or 1200 Mbps per host; and for KiwiVision
"using virtual machines is not recommended" `[C4]`. BriefCam: VMs are
"technically possible but not recommended for production," and must reserve
GPU, CPU, RAM and disk IOPS `[C10][C10b]`. The two most GPU-dependent products
in this survey both advise against virtualisation.

### 4.5 Hardware and ecosystem dependencies

This is the section the problem statement's premise turns on: which advanced
capabilities genuinely require proprietary hardware, and which do not?

**Hard dependencies — capability is unavailable without vendor hardware.**
Axis ACAP applications cannot run on non-Axis cameras, and AXIS Object
Analytics requires compatible Axis MLPU cameras on firmware 10.2+ `[C14][C15a]`.
i-PRO's edge AI "requires i-PRO network cameras with AI capabilities"; Active
Guard consumes i-PRO metadata and best-shots, not raw third-party video
`[C23]`. Hanwha's analytics are tied to the Wisenet SoC's dual NPUs `[C37a]`.
Verkada's 20 kbps steady-state architecture depends on the camera storing
30-365 days locally and emitting metadata — i.e. on owning a Verkada camera;
third-party cameras via Command Connector explicitly do not "receive the same
features and capabilities as native Verkada devices" `[C20][C21][C22]`.
Genetec sizes AutoVu ALPR in "AutoVu camera units," and Sharp/SharpX are
purpose-built ALPR cameras `[C4][C7c]`. Avigilon Alta LPR "cannot be
configured to use panoramic, 360, fisheye, or PTZ cameras" — dome or bullet
only `[C18b]`.

**Soft dependencies — capability works on existing cameras, with caveats.**
Genetec AutoVu Flexreader turns existing supported IP cameras into plate
readers "without dedicated ALPR hardware" — but only up to 30 mph/50 km/h
`[C7a][C7b]`. Milestone XProtect LPR needs no purpose-built camera, but the
camera must look down on the vehicle at no more than 30 degrees, and the
recognition logic is "processor intensive, and varies significantly dependent
on the environmental conditions, camera settings and other parameters"
`[C53]`. Vaxtor ships ALPR both embedded on partner cameras and as PC
software, stating embedding "decrease[s] network bandwidth and hardware
costs" `[C50]`. BriefCam works from any VMS-sourced video but requires NVIDIA
GPUs (no Intel/AMD), CIF-to-4K resolution, 8-30 FPS, and 12-32 px minimum
object size `[C10][C10b]`. Genetec KiwiVision requires an AVX-compatible CPU
on every analytics server, with GPU acceleration limited to two scenarios
`[C4]`. Both major platforms (Genetec, Milestone) turn out to have a software
path off the proprietary ALPR camera — but both then attach physical
constraints (speed, angle) that the existing camera may or may not satisfy.
The dependency did not disappear; it moved from the camera's silicon to the
camera's mounting.

**The dependency nobody can remove: pixels on target.** DORI (IEC EN
62676-4:2015): Detection 25 px/m, Observation 62 px/m, Recognition 125 px/m,
Identification 250 px/m `[C49]`; Axis publishes its own pixel-density white
paper on this `[C16]`. BriefCam's stated floor is 12-32 px per object
depending on class `[C10]`. ANPR needs roughly 250 px/m to resolve plate
characters, and most ANPR systems use IR illumination at 850 nm or 940 nm
optimised for retroreflective plates `[C49b]`. A camera installed for *human
monitoring* was almost certainly specified for Detection or Observation
density (25-62 px/m), not Identification (250 px/m), and software cannot
manufacture the missing pixels (basis: `[C49]`, plus the domain finding that
existing border CCTV was installed for live viewing —
`docs/01-research/domain/domain-research.md` §4.3). This is the boundary
condition on the entire problem statement's premise, and it applies to IBVAP
exactly as it applies to every competitor.

**The ONVIF dependency, and why it is weaker than it looks.** Verkada's
Command Connector is a certified ONVIF Profile S conformant client, yet
Verkada itself states: "the actual implementation of the various features and
capabilities rests with the camera manufacturer... any ONVIF Profile S camera
may not work with Command Connector out-of-the-box" `[C20]`, and it maintains
a Hardware Compatibility List with an internal compatibility lab and a
weeks-to-months assessment queue for new cameras `[C20]`. Milestone maintains
16,500+ tested devices, ships device packs every two months, and needed
1,000+ individually tested ONVIF devices to converge on "a single optimized
driver," with a universal driver as fallback `[C1][C2][C3]`. Two of the most
capable engineering organisations in this market both concluded ONVIF
conformance is insufficient and built a per-model compatibility apparatus —
"we support ONVIF" is a statement of intent, not a capability. Separately,
ONVIF announced on 9 October 2025 that it is ending support for Profile S in
favour of Profile T; after 31 March 2027 manufacturers can no longer submit
new products for Profile S conformance
(`docs/01-research/domain/domain-research.md` §6.7).

**Geopolitical supply-chain dependency [MARKET:US][MARKET:IN].** Under 2019
NDAA Section 889, the US federal government cannot "procure or obtain" video
surveillance "produced by" Dahua or Hikvision, including OEM rebrands; it
covers all federal agencies, the military and US embassies overseas; it bans
federal contractors that *use* such equipment "regardless of whether that
use" relates to a federal contract; and it bans federal grant money being
spent on it. Also named: Huawei, ZTE, Hytera. Indiana adopted an equivalent
state-level ban (SB477, 2023) `[C42]`. India's ER-01/STQC regime has a similar
practical effect through a different mechanism, motivated by concern over
foreign chipsets `[C43a]`, with non-conforming sales barred from 1 April 2026
`[C43d]`. Two of the world's largest procurement markets have independently
made camera provenance a gating condition — a software product that is
genuinely camera-agnostic is insulated from this; one that depends on
specific camera silicon inherits its supplier's political risk.

### 4.6 Integration and API comparison

| Vendor | Ingest | Outbound integration surface | Notes |
|---|---|---|---|
| Milestone XProtect | ONVIF (S/T/G/M), PSIA, universal driver, 11,000+ devices `[C1][C3]` | MIP SDK, REST API, WebSocket, WebRTC, webhooks, driver framework, **AI Bridge (Docker)** `[C1][C47]` | Deepest published surface found in this pass |
| Genetec Security Center | IP cameras via Security Center drivers; Media Gateway exposes **RTSP** to external apps `[C4]` | SDK, Federation, plugins | Media Gateway RTSP is never transcoded `[C4]` |
| BriefCam | VMS connectors (L1-L4) + generic Video Integration API for unsupported VMS `[C10][C11]` | Alerts into VMS as bookmarks/events with bounding boxes `[C11]` | Integration depth varies per VMS |
| AllGoVision | Direct from camera **or** from VMS `[C28b]` | **ONVIF virtual camera** consumable by any ONVIF VMS `[C28c]` | Neatest VMS-agnostic egress pattern found |
| Network Optix | IP cameras, raw RTSP streams, I/O devices `[C31a]` | Open-source integration repos (MPL 2.0), Nx Toolkit, TestCamera emulator `[C31c][C31e]` | Explicitly a build-on platform |
| Verkada | ONVIF Profile S; RTSP fallback, max 20 channels `[C20]` | Cloud Command APIs | **Does not consume third-party camera events** `[C20]` |
| i-PRO Active Guard | i-PRO camera metadata + best-shots `[C23]` | Plugs into Genetec, Milestone, Luxriot, Video Insight `[C24]` | Ingest side is closed |
| Irisity IRIS+ | Any camera via RTSP/ONVIF, incl. analog via DVR `[C29b]` | Not documented in this pass | Broadest stated ingest |
| Frigate | Any RTSP camera; dual-stream `[C32a]` | MQTT, WebRTC/MSE `[C32a]` | Integration by message bus, not SDK |

The **ingest** side of the market has effectively standardised on RTSP + ONVIF
Profile S, with per-model compatibility work layered on top
`[C1][C20][C29b][C31a][C32a]`. The **egress** side has not standardised — every
vendor emits events differently (MIP plugins, REST, WebSocket, webhooks, MQTT,
ONVIF virtual camera, VMS bookmarks) `[C1][C28c][C32a][C11]`. "Support
integration with existing command and control systems" — the phrase in the
problem statement — is therefore fundamentally an *egress* problem, and egress
is exactly where the market has no standard; this looks like a structural,
recurring difficulty rather than one specific to any one force. Two
integration patterns stand out as low-friction and reusable: AllGoVision's
ONVIF virtual camera (present analytics output as an ONVIF camera; any ONVIF
VMS ingests it with no plugin `[C28c]`) and Milestone's AI Bridge (a
documented Docker-container contract for third-party analytics into the
largest open VMS `[C47]`).

### 4.7 Remote and low-bandwidth deployment considerations [BORDER]

This is the axis on which the market's public evidence is thinnest, and where
what evidence exists is unusually concrete.

**Published bandwidth figures, side by side:**

| System | Steady-state uplink | Notes | Source |
|---|---|---|---|
| Verkada camera | **20 kbps/camera**; thumbnails + metadata every ~20 s | Requires Verkada camera; 30-365 days on-device | `[C21]` |
| Verkada, viewing | ~300 kbps (720p) / ~1 Mbps (HD) | On demand only | `[C21]` |
| Calipsa | **~300 kb per event** | Analyses frames, not video | `[C30c]` |
| Eagle Eye Networks | **400 kbps/camera** recommended | Bridge buffers locally, syncs when bandwidth allows | `[C33a]` |
| Genetec Cloud Storage | **Recording throughput + 30%**, guaranteed, 99.9% SLA, <150 ms | 100 Mbps recorded means 130 Mbps uplink | `[C4]` |
| Raw H.264 IP camera | ~5 Mbps/stream | H.265 halves it | domain research §6.2 |

The spread between Verkada's 20 kbps and Genetec's "recording throughput plus
30%" is four orders of magnitude, and it is explained entirely by where the
analysis happens.

Industry and vendor sources describe the same architecture repeatedly: local
analytics sending "only alert notifications (typically just a few kilobytes of
metadata), relevant video clips surrounding events (10-30 seconds of footage),
and periodic metadata describing scene activity" `[C56a]`. Specific claimed
reductions (vendor/industry commentary, directional not measured): "A
40-camera site that needed 80 Mbps of continuous upload to record cloud-only
now needs only a few megabits"; "A 100-camera deployment with edge processing
might require only 10-20 Mbps"; remote industrial sites "with as little as
512 Kbps of upload bandwidth can run detection locally and send only the
resulting signals upstream" `[C56a]`. Peer-reviewed systems research finds
per-camera uplink allocations in constrained deployments can be "a few hundred
kilobits per second or less," consistent with the domain research's finding
that satellite links "are typically high-latency, low-bandwidth and expensive"
`[C56b]`, `docs/01-research/domain/domain-research.md` §6.2.

**Disconnected and air-gapped operation.** Milestone supports "Offline license
activation" and "Add/replace devices without reactivation in offline systems"
in every edition `[C1]`. Irisity lists "on-premise (air-gapped)" as a
supported deployment mode `[C29b]`. Verkada documents an air-gapped *camera*
network topology (second NIC on the isolated camera VLAN, primary NIC to
internet) — but the platform itself still requires the cloud `[C20]`. Genetec
Cloudlink is positioned partly on "the need to maintain local operation during
connectivity disruptions" `[C8c]`. Frigate performs "all processing... locally
on your own hardware," "no cloud subscriptions required" `[C32a]`. Whether
Genetec, BriefCam, Videonetics, AllGoVision or Ipsotek support fully
disconnected operation including licence validation, model updates and time
synchronisation is not documented in anything retrieved — this is the single
most important unknown in this document for a remote-deployment product.

**Power.** No vendor in this survey publishes a power budget for its analytics
workload. Genetec, BriefCam, Irisity and Ambient.ai all specify NVIDIA GPUs
`[C4][C10][C29a][C35a]` without stating watts; Verkada publishes bandwidth but
not power `[C21]`. This plausibly reflects that the market's customers
generally have mains power — at a generator-powered, fuel-limited site, power
is a first-order constraint
(`docs/01-research/domain/ssb-operational-context.md` §10.2) that the
industry's published engineering simply does not address; this looks like a
genuine blind spot, not merely a gap in this research pass.

**Maintenance at unreachable sites.** Verkada: customers "cannot install their
own drives and must use the drives that Verkada provides" — a failed drive
means a shipped replacement and a physical swap; during a Command Connector
firmware update, "the cameras connected to Command Connector will not record
footage"; and "Verkada does not provide any security patches and firmware
updates for non-Verkada cameras" `[C20]`. Every appliance-based architecture
(patterns B and C in [§4.4](#44-architecture-and-deployment)) imports a
physical maintenance obligation at each site; where sites cannot be reached by
road, that obligation likely dominates cost
(`docs/01-research/domain/ssb-operational-context.md` §10.1).

---

## 5. Implications for IBVAP

> As with the rest of this document, nothing below is a product requirement.
> Each entry is a hypothesis about where the market is thin, paired with the
> evidence for it and the reason it might be thin *on purpose*. Converting any
> of these into scope is a `docs/02-product/` decision, per
> [CLAUDE.md](../../../CLAUDE.md) §2.

Ordered roughly by how well-evidenced the gap is:

1. **Disconnected-by-default operation [BORDER].** Only Irisity states
   air-gapped support `[C29b]`; only Milestone documents offline licensing
   `[C1]`; every cloud entrant assumes an uplink `[C21][C33a][C30c][C4]`. For
   most of the market this is simply undocumented rather than absent — and
   on-premise VMS has always run offline, so this may be table stakes rather
   than a differentiator. Genuinely under-documented; see
   [§7](#7-open-questions--research-gaps) Q-3.

2. **Power-aware analytics [BORDER].** Zero vendors publish power budgets
   ([§4.7](#47-remote-and-low-bandwidth-deployment-considerations-border)).
   This may be unmeasured rather than unsolved — edge NPU cameras are already
   low-power `[C14][C37a]` — but nobody has made it comparable.

3. **Honest per-camera capability disclosure.** Telling the operator, from the
   actual stream, which analytics a given camera can and cannot support at its
   mounting — in the spirit of i-LIDS' primary-vs-secondary certification
   framing (`docs/01-research/domain/domain-research.md` §6.7). Genetec ships
   a *calculator* for this `[C4]`, but nobody found ships it as a runtime
   feature. Vendors have a commercial incentive not to publish per-camera
   limitations, which may explain the gap.

4. **Thermal analytics as portable software [BORDER].** Verkada explicitly
   runs no people/vehicle analytics on thermal `[C20]`. This is largely
   solved already, just not portably: Teledyne FLIR FC-Series AI and
   SightLogix both classify humans/vehicles on thermal with onboard analytics
   `[C40][C39a]` — but only inside their own cameras. The gap is thermal
   analytics as portable software, not thermal analytics as a category.

5. **Sub-100-kbps operation without owning the camera.** Verkada reaches
   20 kbps by owning the camera `[C21]`; Calipsa reaches ~300 kb/event by
   restricting scope to alarm frames `[C30c]`; general-purpose platforms sit
   orders of magnitude higher `[C4][C33a]`. BriefCam Nexus already ships
   "process locally, send metadata" `[C12b]` without publishing a bandwidth
   figure, so this may be a gap in *disclosure* rather than *capability* — see
   Q-15.

6. **Deployment without a site survey.** Genetec's calculator asks whether
   cameras "need to be modified" `[C4]`; certification programmes cost 2-3
   days and USD 595-2,995 `[C51]`; Ipsotek shipped VISuite Core specifically
   for "repeatable, plug-and-play" rollout `[C27a]`. The counter-argument
   matters here: DORI physics
   ([§4.5](#45-hardware-and-ecosystem-dependencies)) means some estates
   genuinely cannot support some analytics, and a product that pretends
   otherwise will fail in the field. The more defensible framing of this gap
   may be *telling the operator honestly what a given camera can and cannot
   support*, which nobody appears to ship as a first-class feature (see item
   3 above).

7. **Egress standardisation.** Ingest has standardised on RTSP/ONVIF; egress
   has not ([§4.6](#46-integration-and-api-comparison)). AllGoVision's ONVIF
   virtual camera `[C28c]` and Milestone AI Bridge `[C47]` are real partial
   answers, but only for VMS targets — the unsolved part is outbound
   integration to arbitrary command-and-control systems, not outbound to a
   VMS.

8. **A cost structure that fits many small, low-utilisation sites.**
   Per-camera pricing is universal `[C1][C10][C20]`; Genetec appliances are
   priced per-site `[C9]`; Verkada's smallest Command Connector is USD 2,999
   for 10 channels `[C20]`. But Frigate is free `[C32a]` and Network Optix
   sells perpetual licences `[C31f]` — the floor is already low if the support
   model is acceptable, so the competitor to beat on cost may be open source,
   not Genetec.

9. **Evidentiary integrity as a default, not an edition upgrade.** Milestone
   gates media-database encryption/signing to Expert/Corporate and Evidence
   Lock to Corporate only `[C1]`; Genetec's encryption costs 30% of Archiver
   capacity for the first certificate `[C4]`. These features exist and are
   simply priced — but the cheapest deployments, which is what a remote site
   gets, are the ones without signing, locking or tamper-evidence.

10. **Alerting sized to a two-person post [BORDER].** Every platform examined
    assumes a control room, a video wall and an operator role hierarchy
    `[C4][C1]` (Genetec Smart Wall / XProtect Smart Wall are premium-edition
    features `[C1]`), though mobile clients exist everywhere `[C1][C4]`.
    Whether the target force even has a control room is itself unknown
    (`docs/01-research/domain/ssb-operational-context.md` §7).

11. **Failure modes a non-specialist can recognise and report.** Verkada
    alerts on lost streams `[C20]` and Genetec ships a Camera Integrity
    Monitor `[C6a]`, but nothing found addresses *degraded analytic quality* —
    a camera still streaming but no longer usable for its configured
    analytic. This may exist under names not searched.

A few apparent gaps turned out, on inspection, to already be solved and are
worth naming so they are not chased as if open:

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

Five questions worth carrying into product discovery, deliberately left
unanswered here:

1. What is the smallest deployable unit? Every architecture in this market
   assumes either a control room or a cloud tenant — what does a site with two
   cameras, one operator, a generator and a satellite phone actually get, and
   is that unit a product?
2. Given that all eight named capabilities are commodity
   ([§3.1](#31-capability-comparison)), does IBVAP compete on detection
   quality — where it would be measured against vendors with decades of
   tuning — or on getting a working system onto an estate nobody else will
   touch?
3. Which side of the primary/secondary line is IBVAP on? i-LIDS distinguishes
   an analytic certified as the *sole* detection system from one certified
   only as *support* to a human (`domain-research.md` §6.7) — this choice
   determines the alerting, staffing and liability model and should be made
   deliberately.
4. What does IBVAP emit, and to what? Ingest is a solved standard; egress is
   not ([§4.6](#46-integration-and-api-comparison)) — what does "integration
   with existing command and control systems" mean concretely when the only
   documented candidate on the validation border records outcomes, not
   detections (`ssb-operational-context.md` §14.10)?
5. What is the honest answer when the camera cannot support the analytic? Per
   [§4.5](#45-hardware-and-ecosystem-dependencies), some fraction of any
   existing estate cannot deliver some fraction of the named capabilities — is
   telling the operator that, clearly and per camera, a liability to be
   minimised or the product's most defensible feature?

---

## 6. Risks / Limitations

**Evidence quality.** Almost every source in this document is a vendor
describing its own product; a "FACT" recorded here is a fact *about what the
source claims*, not independently verified real-world performance, unless the
source is explicitly identified as independent (standards body, peer-reviewed
work, government notice, trade press, or a competitor of the vendor
described). No standardised, independent, published accuracy benchmark for
any product in this survey was retrieved — IPVM tests exist but are paywalled,
and this is the largest evidence weakness in the document. No paywalled
analyst or test-lab source (Omdia, Novaira, IPVM) was read directly; all three
are the industry's primary evidence sources for market share and measured
performance. Four vendor PDFs could not be read by the fetch tool and had to
be extracted locally; several other vendor documents were only reachable
through search-engine summaries, and any finding sourced from a summary rather
than the document itself is weaker than it appears. Chinese, Russian, Korean
and Japanese domestic vendors are almost entirely absent from this pass, as is
the entire Latin American and African market — the picture here is
Western-plus-India. No competitor was evaluated hands-on; everything is
documentary.

**Assumptions this document must not be read as making**, because the
counter-evidence is directly on record:

1. **The named capabilities are not unsolved.** They are all shipping. The
   problem statement's framing — that FRS/ANPR/intrusion detection "often
   require specialized hardware and proprietary solutions" — is only partly
   supported: Genetec Flexreader and Milestone XProtect LPR already do ANPR on
   ordinary cameras `[C7a][C53]`, and the SSB operational research separately
   records that the target force has **already procured** a CCTV setup with
   FRS and ANPR (`ssb-operational-context.md` §6.1, §14.2).
2. **"Works with any ONVIF camera" is not achievable by asserting it.** Two of
   the best-resourced engineering organisations in this market both built
   per-model compatibility apparatus and still warn the buyer `[C20][C3]`. A
   claim of universal camera support needs a tested-device list behind it, or
   it is a statement of intent, not fact.
3. **Software cannot compensate for the installed camera.** DORI is physics
   `[C49]`. Resolution, mounting angle, lens, illumination and vehicle speed
   bound what any algorithm can extract `[C7b][C53][C10]`.
4. **Face recognition is not a globally shippable feature.** It is prohibited
   by default for law enforcement in publicly accessible spaces under EU AI
   Act Article 5 `[C44a]`, and the domain research separately flags open legal
   questions about applying it to a treaty-open border population
   (`ssb-operational-context.md` §11.6). It is market-specific, not universal.
5. **The incumbents are not simply expensive because they are inefficient.**
   Genetec's cost buys federation, failover, encryption, audit, certification
   and a support organisation `[C4][C57]` — the encryption alone costs 30% of
   Archiver capacity `[C4]`. Anything cheaper is trading something away, and
   the trade should be named, not hidden.

---

## 7. Open Questions / Research Gaps

**Highest priority — these block any competitive positioning.**

- **Q-1. What does any of this actually cost?** Genetec, Milestone, BriefCam,
  Avigilon, Ipsotek, Irisity, Videonetics and AllGoVision publish no list
  pricing. Verkada is the only vendor with published hardware prices `[C20]`,
  and even there the per-channel licence price is not published. Without
  this, "cheaper than the incumbents" is an untestable claim.
- **Q-2. How accurate is any of this, measured independently?** No
  standardised, independent, published accuracy benchmark for any product in
  this survey was retrieved. IPVM tests exist but are paywalled `[C52c]`.
  i-LIDS certification exists as a framework (`domain-research.md` §6.7) but
  no vendor here was found publishing an i-LIDS result.
- **Q-3. Which of these products genuinely run fully disconnected?** Only
  Irisity states air-gapped `[C29b]` and Milestone states offline licensing
  `[C1]`. For Genetec, BriefCam, Videonetics, AllGoVision and Ipsotek this is
  unknown — and it is decisive for a remote-site product.
- **Q-4. What is the power draw of each architecture per camera?** Nobody
  publishes it ([§4.7](#47-remote-and-low-bandwidth-deployment-considerations-border)).
- **Q-5. What is the real installed-base composition worldwide?** How much of
  the world's deployed CCTV is ONVIF-conformant, at what resolution, what
  codec, what pixel density on target? Without this, "works with existing
  cameras" cannot be sized.

**High priority — shape the competitive picture.**

- **Q-6.** What are Bosch's IVA Pro capabilities and dependencies from
  *primary* Bosch documentation? This pass only retrieved trade commentary
  `[C38]`.
- **Q-7.** What do Hikvision and Dahua actually ship for analytics, and at
  what price? They are excluded from US federal procurement `[C42]` and
  constrained in India `[C43]`, but are a very large part of the world's
  installed base and were not researched in this pass.
- **Q-8.** What is Videonetics' architecture, hardware requirement and
  pricing — and does it run on existing third-party cameras unmodified? It is
  the most directly comparable competitor in the initial validation market and
  the least documented `[C25]`.
- **Q-9.** What are Ipsotek's and Irisity's per-camera hardware requirements
  and prices? Both claim the exact positioning IBVAP would take
  `[C27b][C29b]`.
- **Q-10.** Which vendors have actually deployed at land borders, and what did
  those deployments learn? Anduril's CBP programme is documented `[C41]`;
  nothing comparable was found for the VMS/analytics vendors.
- **Q-11.** What is the real-world false-alarm rate of any of these products
  in outdoor, unlit, vegetated, wildlife-rich terrain? Vendor claims exist
  (Calipsa 93-95% reduction `[C30c]`); independent measurement does not.

**Medium priority — validate assumptions made in this document.**

- **Q-12.** Is it actually true that no vendor sells a "night-time analytic"
  as a distinct feature ([§3.1](#31-capability-comparison))? Tested here only
  by absence of evidence.
- **Q-13.** Does India's ER-01/STQC regime apply to analytics *software*, or
  only to cameras? [§4.3](#43-the-india-specific-competitive-set-marketin)
  assumes the latter, unverified.
- **Q-14.** Do Avigilon Unity's advanced analytics (Appearance Search, unusual
  motion) function on third-party ONVIF cameras? `[C17]` does not say.
- **Q-15.** What are BriefCam's and Genetec's actual multi-site bandwidth
  figures? Both ship the "local processing, central metadata" pattern but
  neither publishes a number `[C12b][C8a]`.
- **Q-16.** How much of the market is VSaaS versus on-premise, by revenue and
  by camera count? Omdia and Novaira hold this behind paywalls
  `[C46a][C46c]`.

**Deliberately deferred to a later stage** — which vendors IBVAP should
integrate with (architecture); which capability IBVAP should build first
(product); whether to build on Network Optix, Frigate, or from scratch
(architecture); pricing and business model for IBVAP (product).

---

## 8. Conclusions

Ordered by how much each should change subsequent stages:

1. Every capability the problem statement names is already a shipping
   product, from multiple vendors, today. There is no capability gap; any
   advantage must come from architecture, cost, deployability or honesty —
   not the feature list.
2. "Advanced analytics requires proprietary hardware" is half true, and the
   false half is already commercialised (Genetec Flexreader, Milestone
   XProtect LPR) — but both solutions relocate the dependency from the
   camera's silicon to its placement (speed, mounting angle).
3. Pixels on target is the hard floor, and it is the same floor for everyone.
   DORI sets Detection at 25 px/m and Identification at 250 px/m; a camera
   installed for human monitoring cannot be upgraded to face identification
   by software alone.
4. "We support ONVIF" is an intention, not a capability. Both Verkada and
   Milestone — among the best-resourced engineering organisations in this
   market — built extensive per-model compatibility apparatus on top of ONVIF
   conformance and still warn buyers that it may not be enough.
5. "Process locally, ship metadata centrally" is settled practice, not an
   opening — six independent vendors (BriefCam, Ambient.ai, Genetec, Verkada,
   Eagle Eye, Milestone) already ship variants of it.
6. The bandwidth spread across the market is four orders of magnitude, and it
   is bought with camera ownership: Verkada's 20 kbps/camera versus Genetec's
   "recording throughput plus 30%, guaranteed."
7. Nobody publishes power. Not one vendor states the watts its analytics
   consume, even while mandating specific NVIDIA GPUs — a genuine blind spot
   in the industry's published engineering.
8. Suspicious-activity detection has no consensus solution. Rule engines
   dominate and are documented to produce high false-positive rates in
   unpredictable environments; learned anomaly detection needs a stable
   "normal" it can be taught; vision-language models are the new, unproven
   entrant.
9. The unit of price is the camera, everywhere, under every licensing model —
   a shape that penalises many-small-sites estates.
10. Regulation is now a market-entry gate, and it differs per market: NDAA
    §889 (US), ER-01/STQC (India), and the EU AI Act's default prohibition on
    real-time remote biometric identification for law enforcement all make
    face recognition a market-specific capability, not a universal one.

This document is a documentary survey of the global intelligent video
analytics market, based on vendor engineering documentation where available,
vendor marketing where not, and independent or academic sources where they
exist. Four primary vendor PDFs were read in full. It is not a product
decision, an architecture decision, a feature list, or a benchmark — no gap
recorded here has been turned into a requirement, and none should be until
`docs/02-product/`. Its known weaknesses are recorded in
[§6](#6-risks--limitations) and [§7](#7-open-questions--research-gaps): no
pricing for most vendors, no independent accuracy measurement for any vendor,
no paywalled analyst or test-lab source read directly, and Chinese, Korean,
Japanese, Latin American and African vendors largely absent. Per
[CLAUDE.md](../../../CLAUDE.md) §2, product scoping in `docs/02-product/` may
proceed on the research completed so far, but Q-1 through Q-5 above should be
carried forward as open risks rather than treated as settled.

---

## 9. References

Retrieved 2026-08-24 unless otherwise noted. **P** marks a primary vendor
engineering document whose text was read in full. **V** marks vendor
marketing. **I** marks an independent or third-party source. **A** marks
academic or standards material.

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

- `[C4]` **P** — *Security Center System Requirements Guide 5.12*, Genetec
  Inc., document EN.500.100-V5.12.0.0(4), last updated 6 February 2024. PDF,
  44 pages, text extracted in full.
- `[C5]` **V** — *Security Center Administrator Guide 5.12*, "About Security
  Center", techdocs.genetec.com.
- `[C6a]` **V** — KiwiVision Security video analytics module, techdocs.genetec.com.
- `[C6b]` **V** — KiwiVision Privacy Protector module, techdocs.genetec.com;
  KiwiVision unified video analytics product page, genetec.com.
- `[C7a]` **V** — "Genetec announces AutoVu Flexreader", Genetec press
  release, April 2018.
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
  tec-tel.com, spot.ai. Competitor-adjacent content; not treated as fact.
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
- `[C16]` **V/A** — *Pixel density and DORI: meeting operational requirements
  in network video*, Axis white paper, PDF.

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
- `[C30d]` **V/I** — Calipsa Video Analytics, DICE Corporation; Sharp Group
  case study.

### Verkada

- `[C20]` **P** — *Command Connector FAQ*, Verkada, doc revision 0526. PDF,
  13 pages, 53 questions, text extracted in full.
  https://docs.verkada.com/docs/command-connector-faq.pdf
- `[C21]` **V** — "Reducing Bandwidth Consumption of a Cloud Camera to
  20kbps", Verkada blog.
- `[C22]` **V** — Hybrid Cloud Physical Security Architecture; "Cloud vs.
  Hybrid Cloud Security Camera System", verkada.com; *Traditional vs Hybrid
  Cloud* PDF.
- `[C46b]` **V** — "Verkada Ranked #1 Worldwide in VSaaS", verkada.com, citing
  Omdia.

### i-PRO, Hanwha, Bosch

- `[C23]` **V** — i-PRO Edge AI solution,
  i-pro.com/products_and_solutions/en/surveillance/solutions/technologies/edge-ai-solutions
- `[C24]` **V** — "i-PRO Introduces Active Guard Version 3.0 with Generative
  AI"; "i-PRO Active Guard video analytics integrated into Luxriot EVO VMS",
  i-pro.com.
- `[C37a]` **V** — Hanwha Vision AI solutions and Wisenet 9 SoC,
  hanwhavision.eu; "How to Set up an Intelligent Video Analytic on Cameras
  using WiseAI", Hanwha Vision Support Portal.
- `[C37b]` **V** — *Wisenet AI Camera* white paper, Hanwha, PDF.
- `[C38]` **I, weak** — Bosch IVA Pro references in third-party comparison
  content. Not primary Bosch documentation — see Q-6.

### Indian vendors

- `[C25a]` **V** — Videonetics corporate site and VMS product page,
  videonetics.com.
- `[C25b]` **V** — Videonetics ANPR / FRS product descriptions,
  videonetics.com.
- `[C25c]` **I** — "Videonetics Empowers Asia's Biggest Real-time Governance
  Center in Andhra Pradesh", VARIndia.
- `[C25d]` **I** — "Videonetics AI Video Platform In Andhra Pradesh",
  SecurityInformed.
- `[C25e]` **I** — "Member Profile: Videonetics", ONVIF blog, May 2023.
- `[C26a]` **V** — Matrix SATATYA Enterprise NVR, matrixcomsec.com.
- `[C26b]` **V/I** — "Matrix and Yotta Partner to Deliver AI-Powered Cloud
  Video Surveillance", IT Voice / SMEStreet / SourceSecurity.
- `[C26c]` **I** — Matrix-Yotta partnership coverage, CXOToday.
- `[C28a]` **V** — AllGoVision About Us, allgovision.com.
- `[C28b]` **V** — AllGoVision Analytics and Features pages, allgovision.com.
- `[C28c]` **V** — AllGoVision Technology Partners page (ONVIF virtual
  camera), allgovision.com.
- `[C28d]` **I** — AllGoVision partner profile, Intel Partner Showcase.
- `[C43a]` **I** — "India to enforce stricter CCTV regulations from April
  2025", asmag.com.
- `[C43b]` **V/I** — "STQC Certification and ER Compliance for CCTV Cameras",
  Matrix Comsec.
- `[C43c]` **I** — STQC IoT System Certification Scheme, stqc.gov.in.
- `[C43d]` **I** — "CCTV New Rule 2026 India: STQC Certification and ER
  Compliance Required from 1 April 2026", velvu.in.
- `[C43e]` **I, advocacy** — "STQC Certification Requirement Order
  Monopolises The CCTV Industry in India", securityupdate.in.
- `[C55a]` **V** — Vehant Technologies, vehant.com.
- `[C55b]` **I** — Staqu Technologies profile, CB Insights.
- `[C55c]` **I** — "JARVIS By Staqu", Electronics For You.
- `[C55d]` **I** — Wobot Intelligence profile, CB Insights.

### Other analytics and platform vendors

- `[C27a]` **V** — "Ipsotek launches VISuite Core to transform scalable
  AI-video analytics deployments", Eviden press release.
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
- `[C31e]` **V** — "How to get a License for Developers",
  support.networkoptix.com.
- `[C31f]` **V** — Nx Witness FAQ and licensing pages, networkoptix.com.
- `[C32a]` **V** — Frigate NVR, frigate.video.
- `[C32b]` **I** — "Deploy Frigate On Jetson", Seeed Studio Wiki.
- `[C32c]` **I** — Frigate deployment guides, corelab.tech and
  homelabstarter.com.
- `[C33a]` **V** — Eagle Eye Networks Cloud VMS FAQ, een.com;
  *Architecture and Engineering Specifications* PDF;
  *EE AN044 Utilizing 4G and 5G Internet Connectivity with Bridges and CMVRs*.
- `[C33b]` **V** — *EE AN045 Eagle Eye Cloud VMS Subscriptions Explained* PDF.
- `[C34]` **V** — "Eagle Eye Networks Acquires Surveillance AI Leader Uncanny
  Vision", BusinessWire, 30 September 2021.
- `[C35a]` **I** — Ambient.ai platform and pricing analyses, surveillant.ai
  and coram.ai. Third-party, competitor-adjacent.
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
  Spot AI alternatives, spot.ai. Treat as positioning evidence only.

### Border-specific

- `[C41a]` **I** — "CBP Awards Anduril $363 Million For Extended Range
  Surveillance Towers", Defense Daily.
- `[C41b]` **I** — "U.S. Customs and Border Protection Set to Purchase 200
  Extended Range Sentry Towers From Anduril", HSToday.
- `[C41c]` **I** — "Anduril to Supply 200+ Tactical Sensing Towers to US
  Border Patrol", The Defense Post, 15 June 2026.
- `[C41d]` **I** — "CBP more than doubling autonomous sentry towers along
  Southwest border", FedScoop.

### Regulation and market structure

- `[C42]` **I** — "Where Dahua and Hikvision Are Banned", IPVM public report;
  NDAA Section 889 guidance materials.
- `[C44a]` **A** — EU Artificial Intelligence Act, Article 5: Prohibited AI
  Practices. artificialintelligenceact.eu/article/5/
- `[C44b]` **I** — "Red Lines under the EU AI Act: Restricting Real-time
  Remote Biometric Identification Systems for Law Enforcement Purposes",
  Future of Privacy Forum.
- `[C44c]` **I** — FPF analysis summary, WTL Governance.
- `[C45a]` **I** — Video Surveillance Market Size Report, MarketsandMarkets.
- `[C45b]` **I** — Video Surveillance Global Market Report, The Business
  Research Company.
- `[C45c]` **I** — Video Surveillance Market Size, Fortune Business Insights.
- `[C45d]` **I** — Video Analytics Market Size And Share Report 2025-2030,
  Grand View Research.
- `[C45e]` **I** — Video Analytics Market Size, Mordor Intelligence.
- `[C46a]` **I, paywalled** — Video Surveillance & Analytics Market Share
  Database, Omdia.
- `[C46c]` **I, paywalled** — World Market for Video Surveillance Hardware
  and Software, 5th edition, Novaira Insights.
- `[C51]` **I** — "VMS Training Options Compared", IPVM public report;
  Genetec and Milestone training pages.

### Standards, academic and technical

- `[C49]` **A** — DORI, IEC EN 62676-4:2015, as described across
  Infiniti Electro-Optics, TP-Link, CCTV Design Tool and Axis `[C16]`.
- `[C49b]` **I** — "How to Choose the Right Camera for ANPR Systems, Part 2",
  e-con Systems.
- `[C52a]` **V, against-interest** — "Video analytics in extreme weather:
  rain, fog and wind" and "Why Security False Alarms Happen", Davantis.
- `[C52b]` **V** — "How Do FH-Series Cameras Reduce False Alarms and Improve
  Detection Accuracy?", Teledyne FLIR.
- `[C52c]` **I, paywalled** — IPVM discussions and reports on video analytics
  accuracy and low-light performance.
- `[C56a]` **V/I** — Edge-based surveillance bandwidth analyses: Wavestore,
  Sighthound, surveillant.ai, Ground Control, Fora Soft.
- `[C56b]` **A** — *Scaling Video Analytics on Constrained Edge Nodes*,
  arXiv:1905.13536.
- `[C60a]` **A** — Rule-based vs anomaly-detection limitations, as documented
  in IJCA and ScienceDirect surveys of video anomaly detection.
- `[C60b]` **A** — Sultani, Chen and Shah, *Real-world Anomaly Detection in
  Surveillance Videos*, CVPR 2018.

### Internal cross-references

- `[docs/00-project/problem.md]` — official SIH problem statement (immutable).
- `[docs/01-research/domain/domain-research.md]` — border CCTV domain research.
- `[docs/01-research/domain/ssb-operational-context.md]` — SSB operational
  context.

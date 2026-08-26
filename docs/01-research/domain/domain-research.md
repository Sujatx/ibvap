# Domain Research — Border CCTV Surveillance

**Stage:** 01 — Research → Domain
**Date:** 2026-08-24
**Scope:** The real-world domain described by the official SIH problem statement
([Problem Statement ID 26187](../../00-project/problem.md)) — how border CCTV
surveillance is actually conducted today at Border Out Posts (BOPs), check
posts, and border roads.

This document records how border CCTV surveillance actually works today, what
is well-evidenced, what is inferred, and what remains unknown, to ground later
product scoping in `docs/02-product/` (per [CLAUDE.md](../../../CLAUDE.md)).
Statements are sourced inline as `[Sn]`, keyed to [§9 References](#9-references);
where a claim rests on inference or on a source that could not be
independently verified, that is said explicitly in the sentence. A number of
primary government documents (PIB releases, MHA press PDFs, a DHS Privacy
Impact Assessment, a Sandia report, GAO product pages) could not be fetched
directly and are recorded from search-engine summaries instead, marked
**[indirect]** at point of use — see [§6 Risks / Limitations](#6-risks--limitations).

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

Border CCTV in this domain sits inside a much larger, MHA-run sensor and
surveillance programme (CIBMS) that also includes radar, laser barriers,
thermal imaging, aerostats and unattended ground sensors, but the problem
statement targets the plainer layer beneath that: standard IP cameras that
today only record and require continuous human watching. Evidence from both
Indian sources and a US analogue converges on the same three structural
weaknesses in that model: sustained human attention degrades within 20–35
minutes even though operators are expected to watch several cameras at once;
sensor-based alerting historically produces very high false-alarm rates (90%
in the US SBInet programme) with no documented Indian protocol for
distinguishing a person from wildlife or wind-blown vegetation; and neither
the Indian nor the US material shows evidence that anyone systematically
measures whether the surveillance technology actually contributed to an
outcome.

The operating environment is harsh and resource-constrained: erratic or
absent power and connectivity at posts, line-of-sight equipment degraded by
fog/rain/vegetation, chronic shortages of technical skills and spare parts,
and heavy reliance on vendors with limited oversight. Any software that
processes video centrally is constrained by real bandwidth limits — per-camera
uplinks in comparable constrained deployments run to a few hundred kilobits
per second or less, and a single H.264 stream is already ~5 Mbps before
multiple viewers multiply that load — making full-rate video backhaul to a
central site for analysis look infeasible at scale on this kind of network.
Evidentiary and legal constraints are real and specific: BSF has no policing
power and must hand suspects/seizures to civil police within 24 hours, and
electronic evidence including CCTV footage must satisfy a Section 63 BSA 2023
certificate that includes a hash value.

The technology-performance evidence available (face recognition, ANPR) is
consistent in warning that lab-grade accuracy figures do not transfer to
uncontrolled, non-cooperative CCTV conditions — a caution directly relevant to
capabilities the problem statement names. A UK certification scheme (i-LIDS)
formalises a distinction — a system can be certified as the *sole* detector in
a zone, or only as *support* to a human — that is likely to shape how border
operators will actually trust and use any analytics IBVAP produces.

Several facts that would materially change product scoping are not
established by any source found in this pass and are treated as open
questions rather than assumptions: the actual installed camera base (count,
model, resolution, ONVIF conformance) at a representative BOP or check post,
what "existing command and control systems" concretely are, what "suspicious
activity" means operationally to a border operator, and the real operator
staffing/shift pattern. These gaps are listed in priority order in
[§7](#7-open-questions--research-gaps) and should be closed, where possible,
before product scope is finalised.

---

## 2. Research Objective / Scope

The objective of this research pass was to establish, from independently
verifiable sources wherever possible, how border CCTV surveillance is
conducted today at BOPs, check posts, and border roads — the operational
environment, the people involved, the current workflow from detection to
resolution, the problems with the conventional approach, the events operators
actually watch for, and the operational constraints (power, bandwidth,
weather, maintenance, legal/evidentiary) that bound what any software
solution could do on this infrastructure. It also builds a glossary of
domain terminology and enumerates unresolved questions for later research
passes (users, competitors, technology) and for product scoping.

This document deliberately stops short of deciding what IBVAP should build,
which capabilities to prioritise, what the interface should look like, or
what models/runtimes/compute placement to use — those are later-stage
questions under `docs/02-product/` and `docs/04-architecture/`, per
[CLAUDE.md](../../../CLAUDE.md) §2.

---

## 3. Key Findings

- **The baseline is recording plus continuous human watching.** Conventional
  CCTV at these sites provides only video recording and live monitoring;
  advanced functions (FRS, ANPR, intrusion detection, object tracking)
  require specialised, costly, proprietary hardware today (problem statement).
- **Human vigilance is a hard, measured limit.** Sustained-attention
  performance measurably declines 20–35 minutes into a watching task, while
  operators are typically expected to observe 3–30 camera scenes at once
  `[S9][S10]`. The often-repeated "45% missed at 12 min / 95% at 22 min"
  figure circulating in vendor material could not be traced to an identifiable
  study and should be treated as unverified `[S30]`.
- **False and nuisance alarms are the dominant historical failure mode of
  sensor-based perimeter systems.** 90% of SBInet sensor alerts were false
  alarms in the US `[S1]`; CIBMS analysis names false alarms and sensor
  malfunction as a leading technical issue and does not define a protocol for
  telling an infiltrator from wildlife or environmental noise `[S1][S2]`.
- **Nobody appears to measure whether the technology worked.** US GAO found
  Border Patrol did not use available data to determine surveillance
  technologies' contribution to outcomes, and found data-quality problems in
  self-reported "asset assist" records `[S12]`. No Indian-side source
  confirms or denies the same gap exists there.
- **Bandwidth and power are real, not theoretical, constraints.** CIBMS
  literature does not specify backbone bandwidth and flags this as a gap
  `[S2]`; comparable constrained edge deployments report per-camera uplinks of
  a few hundred kbps or less `[S28]`; a single H.264 stream is already ~5 Mbps
  and scales with viewer count `[S23]`. Power at border posts is erratic and
  many posts lack basic electricity `[S1][S2]`.
- **The evidentiary chain crosses organisational boundaries.** BSF cannot
  register an FIR or investigate; it must hand suspects and seizures to local
  police within 24 hours `[S22]`. Electronic evidence, including CCTV
  footage, requires a Section 63 BSA 2023 certificate with a disclosed hash
  value, signed by the device custodian and an expert `[S29]`.
- **Recorded event volumes are substantial and rising in places.** 1,104
  infiltration attempts were detected on the India–Bangladesh border in 2025
  (up from 977 in 2024, the highest in nearly a decade) `[S16][S17]`; ₹461.07
  crore of contraband was seized on the same border in 2024, also a 10-year
  high `[S16]`; BSF reported seizing 200 Pakistani drones carrying 287 kg of
  heroin and 174 weapons by October 2025 `[S18][S19]`.
- **Lab-grade recognition accuracy does not transfer to field CCTV.** NIST's
  face-recognition benchmarks use cooperative, well-lit, frontal, high-resolution
  subjects, which production CCTV does not provide `[S26]`. India's ~210
  million vehicles and 50+ number-plate formats sit well outside the
  standardised-plate conditions under which ANPR vendors report accuracy
  routinely exceeding 90% `[S27]`.
- **Trust, not just accuracy, determines whether analytics reduce workload.**
  The UK i-LIDS scheme certifies a video analytic either as a *primary (sole)*
  detector or only as a *secondary (support)* measure `[S25]` — which of these
  an operator believes an IBVAP feature to be will determine whether it
  actually reduces the burden on a human watcher.
- **Material unknowns block confident product scoping**: the actual installed
  camera base and its specifications, what "existing command and control
  systems" and "suspicious activity" concretely mean to the user, and real
  operator staffing and shift patterns are not established by any source
  found in this pass (see [§7](#7-open-questions--research-gaps)).

---

## 4. Detailed Findings

### 4.1 Operational environment

**Locations.** Border security forces deploy CCTV at BOPs, check posts,
border roads and other strategic locations (problem statement). A Border Out
Post is a permanent, self-contained defence outpost with a designated area of
responsibility, accommodation, logistics and combat infrastructure `[S15]`; in
October 2023 the Government of India sanctioned 509 new composite BOPs — 383
on the India–Bangladesh border and 126 on the India–Pakistan border `[S15]`.
The India–Pakistan land border guarded by BSF spans 3,323 km (2,308 km
Radcliffe Line / International Boundary, 776 km Line of Control, 110 km
Actual Ground Position Line), of which roughly 145.876 km (~6.3%) is unfenced
riverine stretch `[S2]`. An Integrated Check Post (ICP) is a land port for
cross-border people/goods movement operated by the Land Ports Authority of
India; nine were reported operating (Attari, Agartala, Petrapole, Raxaul,
Jogbani, Moreh, Sutarkandi, Srimantapur, Dera Baba Nanak/Kartarpur) with CCTV,
observation towers and Customs-operated scanners `[S6][S7]`. The problem
statement does not disambiguate whether "check post" covers only these large
ICPs or also smaller force-run road checkpoints; it is read here as covering
both, since it lists the term as part of a spectrum of locations rather than a
formal category. Which force(s) beyond BSF (ITBP, SSB, Assam Rifles, state
police) would deploy IBVAP is not stated in the problem statement and is
unresolved.

**Terrain and conditions.** Riverine char-land and channel terrain, such as
the 61 km Brahmaputra stretch in Dhubri, Assam, is described as making border
guarding especially difficult in the rainy season `[S3][S21]` **[indirect for
S3]**; equipment there must withstand flash floods and seasonal water-level
change, and concrete embankments are required before some infrastructure can
be installed `[S2]`. Most surveillance equipment is line-of-sight and is
degraded by heavy rain, storms, dense fog, vegetation and difficult topography
`[S1][S2]`. Observation posts are reported to lack basic electricity and
water; the Border Area Development Programme allocates roughly 41% of its
funding to infrastructure creation, and erratic power supply is separately
flagged as a surveillance-system problem `[S1][S2]`. Fog is plausibly a
seasonally dominant condition on the Punjab/Jammu plains in winter and
dust/haze in the western desert, but no source quantifies this by sector or
season, and no source gives measured fog-days, temperature range, dust
loading or humidity at camera housings.

**Existing surveillance technology.** The Comprehensive Integrated Border
Management System (CIBMS) is the MHA programme integrating manpower, sensors,
networks, intelligence and command-and-control `[S1][S2][S21]`, built from
three parts: surveillance technology (sensors, cameras, ground radar,
micro-aerostats, lasers), a dedicated fibre/satellite communication network,
and a Command and Control Centre where data is aggregated into a composite
picture for commanders `[S1]`. Documented CIBMS-linked technologies include
thermal imaging and hand-held thermal imagers, night-vision devices and
passive night-vision binoculars, 360° battlefield surveillance radars, laser
barriers, round-the-clock CCTV, unattended ground sensors, fibre-optic
communication, a 3-D GIS terrain layer, ISRO/NTRO satellite imagery, UAVs and
aerostats, and underground monitoring sensors `[S2]`. BOLD-QIT (Border
Electronically Dominated QRT Interception Technique), begun January 2018 and
inaugurated March 2019, covers the Dhubri riverine stretch with microwave,
OFC and DMR communication, day/night cameras and an intrusion detection
system, feeding BSF control rooms so Quick Reaction Teams can intercept
`[S3][S21]` **[indirect for S3]**. Two CIBMS "smart fencing" pilots in Samba
sector, Jammu (5.3 km and 5.5 km) were operationalised in September 2018;
Stage-I pilots (Jammu, Assam) are reported complete and Stage-II envisages
153 km across 4 patches `[S3][S4]` **[indirect]**. Separately, BSF is reported
to have deployed around 5,000 body-worn cameras, biometric recorders and
night-vision monitoring along the Bangladesh border by 2025, though this
comes from a low-confidence encyclopedic source `[S5]`.

The problem statement's "existing CCTV infrastructure" most plausibly refers
to standard IP cameras recorded to DVR/NVR appliances rather than the
specialised CIBMS sensor suite — the statement explicitly contrasts "standard
IP-based CCTV cameras" against "dedicated FRS, ANPR, or smart-camera
hardware," and the CIBMS grid described above covers only pilot-scale
distances, whereas CCTV is described as present at BOPs, check posts and
border roads generally. But the actual installed base — camera count per
site, make/model, resolution, codec, PTZ vs. fixed, ONVIF conformance,
network isolation, and what (if any) VMS sits in front of it — is not
established by any source, nor is whether "existing CCTV" means CIBMS-era
installations, older standalone ones, or a mix.

### 4.2 People and roles

The problem statement names only "border security forces" generically. BSF
Control Rooms receive sensor/camera feeds so that Quick Reaction Teams can
intercept `[S3][S21]` **[indirect for S3]**; senior commanders at the Command
and Control Centre receive the composite picture, analyse/classify the threat
and coordinate response `[S1]`. BSF has approximately 290,000 personnel across
192 battalions `[S5]`. In the US analogue, Border Patrol agents both monitor
feeds and respond in the field, and log "asset assists" where a technology
contributed to an apprehension or seizure `[S12]` **[indirect]**.

No source gives the intermediate assessment step by name; a plausible
staffing chain — camera → control-room operator (detects) → post
commander/duty officer (assesses) → QRT (responds) → record-keeper (logs) — is
assembled from `[S1]` (analyse/classify/coordinate) and `[S3][S21]`
(feeds → control room → QRT), not stated end-to-end anywhere. Control-room
duty is plausibly a rotating general-duty shift rather than a specialist
cadre, since `[S1]` separately reports "lack of technical expertise for
equipment operation and maintenance among BSF personnel" as a systemic
deficiency — a claim in tension with a dedicated professional operator corps.
Surveillance output likely has at least three distinct consumers with
different needs: an operator who must not miss things in real time, a
commander who needs an assessed picture to decide, and an
investigator/prosecutor who needs retrievable, defensible evidence afterward
`[S1][S22][S29]`.

Unresolved: how many operators per control room and how many
cameras/screens each watches, shift length and rotation, whether operators
are trained/certified for monitoring; whether officers above battalion level
consume live video or only summaries/reports; whether civilian or contracted
technicians maintain the systems and whether they can access feeds; and
whether non-force stakeholders (Customs, immigration, state police,
intelligence) consume the same ICP camera feeds.

### 4.3 Current surveillance workflow

Conventional CCTV today provides video recording and live monitoring only,
requiring continuous human observation (problem statement) — the workflow
IBVAP's domain begins from. In the CIBMS design, field detection equipment
feeds data through the communication network to command posts, where
commanders analyse it and direct QRTs `[S1]`; laser barriers specifically
trigger audible sirens on breach `[S2]`, and CIBMS analysis notes the design
does not define protocols for telling an infiltrator from wildlife or an
environmental trigger `[S2]`. The US analogue names an operational sequence of
detect → track → identify/classify → resolve `[S14]` **[indirect]**.

A plausible Indian sequence, assembled from the sources above rather than
stated end-to-end by any one of them, is: a sensor or operator detects
something → an operator or duty officer slews a camera or looks harder to
assess whether it is a real threat → if real, a QRT is dispatched and
informed by radio → the outcome (apprehension, seizure, nothing found) is
recorded → the video is retained and retrieved later if the incident becomes
a case. Detection and assessment appear to be genuinely separate functions —
a sensor alarm is not itself an incident; a human must look at imagery to
decide, which is arguably why CCTV exists alongside fences and other sensors
at all: the camera is the assessment medium for alarms raised by other means
(`[S1]`'s Command and Control Centre function is explicitly "analyse and
classify," distinct from sensing). The Sandia perimeter-security literature
that formalises this detection/assessment distinction (`[S11]`) could not be
retrieved in this pass.

Not established by any source: what an operator is required to do when an
alert fires (acknowledge/log/escalate/dispatch, and whether a written SOP
exists); what channel carries an alert to the QRT beyond BOLD-QIT's mention of
DMR radio `[S3]`; and whether any detection-to-interception response-time
target exists.

**Event logging.** "Real-time alert generation and event logging" is named as
a required capability in the problem statement — its presence as a stated
requirement suggests it is currently absent or inadequate. Today's logging is
plausibly manual, paper- or register-based, with video retrieval done ad hoc
by scrubbing DVR timelines, though this is inference from the problem
statement's own framing rather than a sourced claim. Whether any digital
incident register exists today, what fields it captures, and whether it links
to video are unknown.

**Investigation and evidence.** BSF has no policing power: it cannot register
an FIR or investigate, may only conduct preliminary questioning, and must hand
a suspect or seizure to local police within 24 hours `[S22]`. Its powers of
arrest, search and seizure extend to a belt from the border reported as up to
50 km in Assam, Punjab and West Bengal after a 2021 notification (previously
15 km) and up to 80 km in Gujarat — the notification's extension is
politically contested `[S22]`. Electronic records including CCTV footage are
governed by Section 63 of the Bharatiya Sakshya Adhiniyam (BSA) 2023, in force
from 1 July 2024 in place of Section 65B of the Indian Evidence Act 1872;
admissibility of a copy requires a certificate — signed by the person in
charge of the device and by an expert — that discloses the record's hash
value `[S29]`. Together these make the evidence chain cross-organisational:
the force detects and records, but the case is built by state police and
tried in a civil court, so any exported video must survive handover to an
organisation that did not produce it. Current export/handover practice
(format, who signs, whether hashes are actually computed, turnaround time,
and how often footage is used in prosecutions) and mandated or practised
retention periods are both unknown.

**Command and control integration.** The problem statement requires
"integration with existing command and control systems," and `[S1]` confirms
a Command and Control Centre is architecturally central to CIBMS — but `[S1]`
also flags that centralised decision-making may delay urgent field responses,
i.e. C2 integration is not a pure benefit. What the "existing command and
control systems" concretely are (names, vendors, protocols, APIs, data
models, network reachability from camera sites) and at what echelon they live
(BOP/Company/Battalion/Sector/Frontier/Force HQ) are unknown.

### 4.4 Problems with conventional CCTV monitoring

**Human attention.** Vigilance decrement — a measurable decline in
sustained-attention task performance — generally sets in 20–35 minutes into
the task `[S9]`, a peer-reviewed finding. CCTV monitoring is vigilance-intensive,
with operators typically required to watch 3–30 camera scenes concurrently
`[S9][S10]`, and system effectiveness is bounded by the operator's own
detection ability `[S9]`. The widely repeated claim that an operator misses
"up to 45% of screen activity after 12 minutes and up to 95% after 22
minutes" appears throughout vendor/trade material `[S30]`, but the underlying
study is not identifiable from any source repeating it, so the specific
percentages should be treated as unverified — the defensible, peer-reviewed
figure is the 20–35 minute decrement above. This is recorded because the
45%/95% figure will likely surface in competitor material and hackathon
pitches and the project should know it is soft. Separately, operator reliance
on a semi-automated system is itself shaped by the system's stated
confidence, its actual accuracy, and task complexity — adding automation
changes operator behaviour, not just workload `[S10]`.

**False and nuisance alarms.** In the US SBInet programme, 90% of sensor
alerts were false alarms, cited as a cautionary parallel for CIBMS `[S1]`.
CIBMS analysis separately names false alarms and sensor malfunctions as a
leading technical issue alongside line-of-sight constraints and unreliable
transmission `[S1]`, and does not define protocols for distinguishing
infiltrators from wildlife or environmental triggers `[S2]`. The dominant
nuisance sources at Indian borders are plausibly livestock (including
smuggled cattle themselves), wildlife, wind-blown vegetation, rain and
insects on the lens, headlight/IR glare at night, and ordinary agricultural
activity in the border belt — general perimeter-security knowledge plus
`[S2]`'s explicit mention of wildlife, but not measured at these specific
sites. An alerting system that is not trusted is plausibly worse than no
alerting system at all, since it consumes attention while supplying false
assurance — an inference from `[S10]`'s finding that system accuracy drives
operator reliance.

**Recording without intelligence.** Conventional CCTV provides only recording
and live monitoring; advanced functions require specialised hardware and
proprietary solutions, making large-scale deployment costly and difficult in
remote areas (problem statement). CIBMS-specific problems documented include
exorbitant equipment costs, unavailability of spare parts, high reliance on
external vendors with minimal oversight, and lack of technical expertise for
operation and maintenance among BSF personnel `[S1]`; BSF RFPs have reportedly
let vendors "arrive at their own conclusions" rather than specifying technical
requirements, suggesting limited in-house technical specification capacity
`[S1]`.

**Unmeasured effectiveness.** GAO found that Border Patrol had not used
available data to determine the contribution of surveillance technologies to
security outcomes `[S12]` **[indirect]**, and found data-quality problems in
self-reported "asset assist" records — one sector recorded roughly 500
assists from Integrated Fixed Towers between June and December 2016 despite
having no IFTs installed `[S12]` **[indirect]**. GAO separately found that
planned testing of IFTs would establish mission contribution but not
effectiveness and suitability under varying environmental conditions such as
weather, contrary to DHS guidance `[S13]` **[indirect]**. The same measurement
gap is plausible in Indian deployments given `[S1]`'s findings on weak vendor
oversight and absent in-house technical capability, but no Indian source
confirms or denies this either way. Whether any Indian force records which
detections were technology-assisted, and whether any effectiveness baseline
exists, is unknown.

### 4.5 Typical surveillance events

**Illegal crossing / infiltration.** 1,104 infiltration attempts were
detected on the India–Bangladesh border in 2025, up from 977 in 2024 —
reportedly the highest annual figure in nearly a decade `[S16][S17]`; more
than 2,550 Bangladeshi nationals were reported detained in 2025 attempting
illegal entry `[S17]`. CIBMS is stated to improve BSF capability against
illegal infiltration, contraband smuggling, human trafficking and
cross-border terrorism `[S1][S21]`.

**Smuggling — goods, livestock, narcotics.** BSF seized ₹461.07 crore of
contraband on the India–Bangladesh border in 2024, reportedly the highest in
10 years `[S16]`. The illegal India-to-Bangladesh cattle trade is estimated at
roughly $500 million annually and long predates the border fence `[S20]`. On
26 January 2025, BSF found three large underground bunkers used for narcotics
smuggling, holding ₹1.4 crore of codeine-based cough syrup at Majhdia, about 2
km from the border `[S16]`.

**Aerial incursion — drones.** BSF seized 245 drones from Pakistan in Punjab
in 2024 (one report gives 294 for the year); by October 2025 the force
reported seizing 200 Pakistani drones carrying 287 kg of heroin and 174
weapons including AK-47s, grenades and explosives `[S18][S19]`. Punjab is
described as the epicentre of drone-assisted narcotics trafficking, with
almost all such incidents nationally occurring along its border `[S19]`.
Drone incursion is geometrically an event class fixed ground CCTV is poorly
positioned to catch (small, fast, typically above the camera's field of view
and elevation) and is more plausibly handled by dedicated counter-UAS systems
than the CCTV grid — not sourced, but relevant because the problem statement
does not list drones among required capabilities.

**Tunnels and sub-surface crossing.** A 40-metre tunnel was uncovered in West
Bengal on 17 July 2024 `[S16]`. Tunnel detection is plausibly out of reach of
surface-camera video analytics except indirectly (spoil heaps, repeated
visits to a fixed location, unexplained vehicle stops) — not sourced.

**Vehicle and person movement at check posts.** At ICPs, movement of people
and cargo is the routine flow; security infrastructure includes CCTV,
observation towers, baggage/cargo scanners, full-body truck scanners (the
Attari truck scanner is reported non-operational) and handheld detection
equipment `[S6][S7]`. Check-post events are plausibly dominated by routine,
high-volume, legitimate traffic, while BOP/border-road events are dominated
by rare, anomalous activity — an inference from an ICP's function as a
trade/transit port `[S6]` versus a BOP as a defence outpost `[S15]`, not
directly sourced, but if true these are operationally different problems: one
is throughput and record-keeping, the other is needle-in-haystack detection.

**Night-time movement.** "Night-time movement detection" is a named required
capability in the problem statement, and CIBMS deployments consistently pair
day/night cameras `[S3][S21]` with NVDs, PNVBs and thermal imagers `[S2]`,
treating night as a distinct operating regime. Infiltration and smuggling
plausibly concentrate in darkness and poor-visibility conditions — exactly
when conventional CCTV performs worst — though this is widely stated in
security literature generally rather than quantified in any source found
here.

**Event classes implied by the problem statement.** The capabilities named in
[problem.md](../../00-project/problem.md) imply these event classes: human
presence/movement, vehicle presence/type, a detectable face, a readable
number plate, crossing of a defined virtual line or region, "suspicious
activity," and night-time movement. What "suspicious activity" means
operationally to this user is undefined both in the statement and in every
source reviewed.

### 4.6 Operational constraints

**Power.** Erratic power supply in border regions is a documented
infrastructure problem for electronic surveillance `[S1]`, and observation
posts are reported to lack basic electricity and water with no comprehensive
electrification plan documented `[S2]`. Actual power availability at a
representative BOP — grid hours per day, generator capacity and fuel
logistics, solar/battery provision, and the resulting budget for additional
compute — is unknown.

**Connectivity and bandwidth.** CIBMS uses a dedicated fibre-optic and
satellite communication network `[S1]`; BOLD-QIT specifically used microwave,
OFC and DMR `[S3][S21]`. Specific bandwidth requirements and backbone
specifications are not stated in the CIBMS literature reviewed, and the gap
is explicitly flagged, including the note that thermal and radar feeds need
adequate capacity to reach command centres `[S2]`. In constrained
deployments generally, per-camera uplink allocation can be "a few hundred
kilobits per second or less" `[S28]`, and satellite links — while enabling
remote deployment — are typically high-latency, low-bandwidth and expensive
`[S25b]`. A single H.264 IP camera stream is on the order of 5 Mbps, and each
additional client pulling that stream multiplies the load off the camera
(3 clients × 5 Mbps = 15 Mbps) `[S23]`; H.265 delivers similar visual quality
at roughly half the bitrate of H.264, halving storage and LAN bandwidth
`[S23]`. Taken together, these figures suggest that any architecture
requiring full-rate video to be shipped from a remote BOP to a central site
for analysis is likely bandwidth-infeasible at scale on this kind of network
— this is recorded here as a research finding bearing on later architecture
work, not as a decision.

**Environment and weather.** Line-of-sight equipment is vulnerable to heavy
rain, storms and dense fog, and adverse terrain/weather undermine system
function generally `[S1][S2]`. Thermal imaging is often marketed as
weather-immune, but fog and rain do severely limit thermal range because
water-droplet scattering diminishes the infrared signal (higher droplet
density causes more attenuation) — a claim from a manufacturer white paper
that runs against the vendor's own commercial interest and matches known
physics `[S24]`. Thermal cameras detect heat rather than motion, which makes
them better at rejecting environmental noise such as shadows and moving
foliage and unaffected by glare/backlighting `[S24]`. What proportion of
existing border CCTV is thermal versus visible-light, and whether visible
cameras have IR illuminators or true day/night sensors, is unknown.

**Maintenance, spares and skills.** Equipment maintenance is identified as
critical, with specialised technical training and spare-parts availability
both flagged as undefined challenges, alongside high reliance on external
vendors with minimal oversight `[S1][S2]`. One source proposes (as a
recommendation, not an implemented fact) raising a technical battalion at
Frontier level with company-strength detachments at Sector HQs to enable
localised repair `[S2]`. Any software deployed at a BOP plausibly needs to
survive long periods without an on-site engineer and fail in a way a
non-specialist can recognise and report — an inference from `[S1]`'s skills
finding.

**Cost and scale.** The problem statement requires the solution to be
cost-effective, scalable, and suitable across remote border locations and
strategic installations, eliminating dependence on expensive dedicated
surveillance hardware; exorbitant equipment cost is separately documented as
a barrier `[S1]`. "Scalable" in this context most plausibly means scalable
across many small, isolated sites — the scaling axis is site count, not user
count — reading from the statement's own phrase "across remote border
locations."

**Legal, procedural and organisational.** BSF cannot register an FIR or
investigate; suspects and seizures go to local police within 24 hours
`[S22]`. Electronic evidence requires a Section 63 BSA certificate with a hash
value, signed by the device custodian and an expert `[S29]`. Land acquisition
has been a chronic obstacle to border infrastructure: roughly 24,000 acres
belonging to about 6,000 families across 212 villages in six Punjab districts
remained disputed since 1988, and an audit found abnormal delays in 66% of
land acquisition cases, some extending nine years `[S2]`. Centralised
decision-making is separately flagged as a risk of delaying urgent field
responses `[S1]`. Unknown: the data classification, security accreditation
and network policy that would apply to a platform handling live border video
(e.g. whether internet or cloud touch is permissible at all, what
certification is required), and the privacy/legal constraints on face
recognition applied to civilians in the border belt, who are largely Indian
residents going about agricultural life.

**Technology performance constraints.** Face recognition accuracy degrades
substantially between controlled enrolment conditions and production CCTV;
angle, lighting and resolution are the primary degradation factors. NIST
benchmarks use cooperative subjects, controlled lighting, frontal poses and
high resolution, none of which production CCTV provides; NIST's FIVE
programme specifically targets non-cooperative subjects and degraded video
`[S26]` (the NIST programme descriptions are primary; specific accuracy-drop
percentages come from vendor/industry commentary and should be treated as
indicative only). India has roughly 210 million vehicles and over 50 number-plate
formats; countries with standardised plates (Australia, Vietnam, Italy) see
ANPR accuracy often exceeding 90% `[S27]` — an ANPR-vendor comparison that
should be read as directional rather than precise. Documented ANPR failure
modes include non-standardised formats, unusual fonts, plate condition,
complex scenes, camera quality and mounting position, distortion, motion
blur, contrast, reflections, processing/memory limits, and day/night
conditions; fast-moving vehicles create motion blur and shorten capture time,
and recognition falls sharply above the camera's processing limit `[S27]`.

The UK's i-LIDS (Imagery Library for Intelligent Detection Systems), a CAST/CPNI
benchmark, evaluates video analytics against security scenarios including
sterile-zone monitoring (detecting persons in a restricted area); systems
meeting its criteria may be certified as a primary (sole) detection system or
only as a secondary (support) measure, with datasets of roughly 24 hours of
footage per scenario across weather, time of day and scene density `[S25]`.
This primary/secondary distinction is arguably the single most important
framing in this research for how border operators will think about AI
analytics: whether an operator believes a given analytic is the *only* thing
watching, or merely a support to a human who is still watching, determines
whether the system reduces workload at all — an interpretation drawn from
`[S25]`'s certification categories, not stated as an operational implication
by the source itself. Separately, ONVIF Profile S standardises live H.264
streaming, audio, PTZ control, motion-detection events and basic metadata,
and most Profile S cameras also expose a plain RTSP URL; ONVIF announced on 9
October 2025 that it is ending Profile S support in favour of Profile T, and
after 31 March 2027 manufacturers can no longer submit new products for
Profile S conformance `[S23]`.

### 4.7 Domain terminology

Descriptive glossary of the domain — not IBVAP vocabulary.

**Places and organisation**

| Term | Meaning | Source |
|---|---|---|
| BOP — Border Out Post | Permanent operational base of the border force with a designated area of responsibility; self-contained, with accommodation, logistics and combat infrastructure | `[S15]` |
| Composite BOP | Newer BOP design; 509 sanctioned in 2023 (383 Indo-Bangladesh, 126 Indo-Pakistan) | `[S15]` |
| Check post | Manned control point for movement across or near the border | problem statement |
| ICP — Integrated Check Post | LPAI-operated land port combining immigration, customs, cargo and security functions | `[S6][S7]` |
| LPAI — Land Ports Authority of India | Statutory body operating ICPs | `[S6][S7]` |
| BSF — Border Security Force | CAPF under MHA guarding the Indo-Pakistan and Indo-Bangladesh borders; ~290,000 personnel, 192 battalions | `[S5]` |
| Frontier / Sector / Battalion / Company | Descending echelons of BSF command referenced in technical-battalion and C2 proposals | `[S2]` |
| IB — International Boundary | The 2,308 km Radcliffe Line segment | `[S2]` |
| LoC — Line of Control | 776 km | `[S2]` |
| AGPL — Actual Ground Position Line | 110 km | `[S2]` |
| Char land | River island/sandbar terrain, prominent in the Brahmaputra riverine border | `[S3][S21]` |

**Systems and programmes**

| Term | Meaning | Source |
|---|---|---|
| CIBMS | Comprehensive Integrated Border Management System — MHA programme integrating manpower, sensors, networks, intelligence and C2 | `[S1][S2]` |
| BOLD-QIT | Border Electronically Dominated QRT Interception Technique — CIBMS implementation over 61 km of riverine border at Dhubri, Assam | `[S3][S21]` |
| Smart fencing | Popular name for the CIBMS electronic surveillance grid used in place of, or alongside, physical fence | `[S3][S4]` |
| Command and Control Centre | Hub where sensor data is aggregated into a composite situational picture for commanders to analyse, classify and coordinate response | `[S1]` |
| Control Room | Border-level facility receiving camera and sensor feeds and cueing QRTs | `[S3][S21]` |

**People and response**

| Term | Meaning | Source |
|---|---|---|
| QRT — Quick Reaction Team | Field element dispatched to intercept on detection | `[S3][S21]` |
| Standing patrol | Small static element (min. 1 NCO + 3 men in the cited doctrine) posted to observe and disrupt infiltration, watching over obstacles | `[S31]` (general fieldcraft source, not India-specific — low confidence) |
| Anti-infiltration grid | Layered arrangement of patrols, ambushes and obstacles along likely infiltration routes | `[S31]` |
| Asset assist (US term) | A recorded instance in which a technology contributed to an apprehension or seizure | `[S12]` |

**Sensors and imaging**

| Term | Meaning | Source |
|---|---|---|
| HHTI | Hand-Held Thermal Imager | `[S2]` |
| NVD / PNVB | Night Vision Device / Passive Night Vision Binocular | `[S2]` |
| BFSR | Battlefield Surveillance Radar, 360° coverage | `[S2]` |
| UGS | Unattended Ground Sensor | `[S2]` |
| Laser barrier / laser wall | Beam-break intrusion detection used on unfenced riverine gaps; triggers an audible siren | `[S2]` |
| Aerostat / micro-aerostat | Tethered balloon carrying day/night sensors | `[S1][S2]` |
| OFC / DMR / microwave | Optical Fibre Cable / Digital Mobile Radio / microwave link — the BOLD-QIT communications mix | `[S3][S21]` |

**Surveillance-industry terms**

| Term | Meaning | Source |
|---|---|---|
| ONVIF Profile S / Profile T | Interoperability profiles for IP video; S covers H.264 live streaming, PTZ, motion events, basic metadata; T is its successor | `[S23]` |
| RTSP | Media-plane protocol carrying the actual video stream | `[S23]` |
| NVR / DVR / VMS | Network or Digital Video Recorder / Video Management System — the recording and viewing layer | `[S23]` |
| Sterile zone monitoring | i-LIDS scenario: detecting the presence of persons in a restricted area | `[S25]` |
| Primary vs secondary detection system | i-LIDS certification categories: sole detection system, versus support to a human/other primary system | `[S25]` |
| Vigilance decrement | Measurable decline in sustained-attention task performance over time, typically onset 20–35 min | `[S9]` |
| Nuisance / false alarm | Alarm from a real but benign cause, versus alarm with no cause; the dominant failure mode of sensor-based perimeter systems | `[S1][S2]` |
| Detect → track → identify/classify → resolve | The US border surveillance operational sequence | `[S14]` |

**Legal and evidentiary**

| Term | Meaning | Source |
|---|---|---|
| BSF Act, 1968 | Statute establishing the BSF and its powers | `[S22]` |
| Section 63, BSA 2023 | Provision governing admissibility of electronic records (replacing s.65B IEA 1872 from 1 July 2024); requires a certificate with hash value | `[S29]` |
| Chain of custody | Documented custody trail required to establish integrity of a digital record | `[S29]` |

---

## 5. Implications for IBVAP

These are research findings that plausibly bound or shape later product and
architecture decisions; they are not themselves decisions, per
[CLAUDE.md](../../../CLAUDE.md) §2.

- The distinction between conventional CCTV (recording + monitoring) and the
  named advanced capabilities (FRS, ANPR, intrusion detection, tracking,
  suspicious-activity detection, event logging, C2 integration) maps directly
  onto the gap the problem statement identifies — any product scoping should
  trace features back to this specific gap rather than the wider CIBMS sensor
  suite.
- The vigilance-decrement and false-alarm evidence together suggest that
  operator *trust* in an alert, not just its raw accuracy, will determine
  whether analytics reduce workload — the i-LIDS primary/secondary framing
  (`[S25]`) is a useful lens for scoping how confidently any feature can be
  positioned.
- Bandwidth and power evidence suggests that architectures requiring
  full-rate central video streaming are unlikely to be viable at the scale
  and remoteness implied by "across remote border locations" — this bears
  directly on later architecture decisions about where compute sits.
- The Section 63 BSA hash-certificate requirement and the 24-hour handover
  rule imply that any exported evidence artefact needs to support a
  hash-verifiable chain of custody usable by an organisation (police) that
  did not produce the recording.
- Lab-vs-field accuracy gaps in face recognition and ANPR mean that any
  claims made about these capabilities should be qualified against
  uncontrolled CCTV conditions rather than benchmark conditions.
- The "suspicious activity" capability named in the problem statement is
  currently undefined by any source and cannot be scoped meaningfully until
  it is operationalised (see Q-3 below).

---

## 6. Risks / Limitations

- Several primary government sources could not be fetched directly during
  this pass (HTTP 403 or connection refused) and are instead recorded from
  search-engine summaries: PIB press releases (`pib.gov.in`), MHA press
  release PDFs (`mha.gov.in`), a DHS Privacy Impact Assessment PDF
  (`dhs.gov`), Sandia SAND2014-17929 (`osti.gov`), and GAO product pages
  (`gao.gov`). These are marked **[indirect]** throughout §4 and should be
  retrieved and re-verified before being relied upon for firm conclusions
  (see Q-19).
- Some facts rest on single sources of uncertain reliability: the 5,000
  body-worn-camera figure and the BSF personnel count come from an
  encyclopedic secondary source `[S5]`; the drone-seizure figures come from a
  state news agency and a think-tank `[S18][S19]`; the standing-patrol/
  anti-infiltration-grid doctrine (`[S31]`) is not India-BSF-specific.
  Several thermal-imaging and ANPR claims come from vendor white papers
  (`[S24][S27]`) that, while directionally credible, carry a commercial
  interest.
- The widely circulated "45% at 12 min / 95% at 22 min" operator-attention
  statistic could not be traced to a verifiable source and is flagged as
  unverified rather than treated as fact — it should not be relied upon in
  later stages without independent verification (see Q-20).
- A number of connecting inferences in this document (the staffing chain,
  the practical Indian detect-assess-respond sequence, the check-post-vs-BOP
  event-profile distinction, the drone/CCTV geometry mismatch, the tunnel
  detection reasoning) are plausible constructions from adjacent sourced
  facts rather than statements made directly by any source. They are worded
  as inference in §4 rather than as established fact, and should be validated
  before being treated as settled in product scoping.
- No Indian-language or force-internal doctrine document on CCTV monitoring
  at BOPs was located in this pass; conclusions about Indian practice
  necessarily lean on secondary/think-tank analysis and a US analogue.

---

## 7. Open Questions / Research Gaps

Ordered by how much the answer would change subsequent stages. None of these
are answered by the sources reviewed in this pass.

**Highest priority — block product scoping**

- **Q-1** What is the actual installed camera base at a representative BOP
  and check post? Count, model, resolution, codec, PTZ vs fixed, thermal vs
  visible, ONVIF conformance, age. *(§4.1)*
- **Q-2** What recording/VMS layer exists today, and is it reachable over a
  network from a place where compute could sit? *(§4.1)*
- **Q-3** What does "suspicious activity" mean to a border operator, stated
  as observable behaviour? The problem statement names the capability but no
  source defines it. *(§4.5)*
- **Q-4** What are the "existing command and control systems" by name, with
  their interfaces? *(§4.3)*
- **Q-5** How many operators watch how many cameras, on what shift pattern,
  and what are they told to do when they see something? *(§4.2, §4.3)*

**High priority — shape the problem**

- **Q-6** What is the real nuisance-alarm profile at these sites: what
  actually triggers false alerts, and how often? *(§4.4)*
- **Q-7** What is the power budget available at a BOP for additional
  compute? *(§4.6)*
- **Q-8** What is the actual available bandwidth from BOP to the next
  echelon, and is it symmetric, metered, or shared with voice/radio? *(§4.6)*
- **Q-9** What retention period is required or practised for border CCTV?
  *(§4.3)*
- **Q-10** What is the current procedure for exporting footage for a case
  handed to local police, and does it currently satisfy Section 63 BSA?
  *(§4.3)*
- **Q-11** Is there a written SOP/Standing Order for alarm assessment and
  escalation that could be read? *(§4.3)*
- **Q-12** What response-time target, if any, exists from detection to
  interception? *(§4.3)*

**Medium priority — validate assumptions in this document**

- **Q-13** Is the control-room role a rotating general duty or a specialist
  cadre? (Tests §4.2.)
- **Q-14** Do check posts and BOPs really have different event profiles
  (throughput vs. anomaly)? (Tests §4.5.)
- **Q-15** What proportion of border CCTV is thermal? (Tests §4.6.)
- **Q-16** What are the measured environmental conditions per sector — fog
  days, temperature range, dust? (§4.1)
- **Q-17** Which forces beyond BSF are in scope? (§4.1)
- **Q-18** What security accreditation, data classification and network
  policy would apply to a video analytics platform on this network? (§4.6)

**Research-process gaps**

- **Q-19** Retrieve the primary sources that this pass could not fetch
  directly: MHA Annual Report border-management chapter, PIB releases on
  CIBMS and BOLD-QIT, the Sandia perimeter-security reference
  (SAND2014-17929) for formal Pd/NAR/FAR definitions, the DHS PIA for Border
  Surveillance Systems, and the GAO reports GAO-18-119 / GAO-14-368 in full.
  Several §4.3–§4.6 claims currently rest on search-engine summaries rather
  than document text.
- **Q-20** Find the primary study behind the "45% at 12 min / 95% at 22 min"
  operator-attention claim, or establish that it does not exist. (§4.4)
- **Q-21** Locate any published Indian-language or force-internal doctrine on
  CCTV monitoring at BOPs. None was found in this pass.

The following are deliberately **not** domain questions and belong to later
stages, per [CLAUDE.md](../../../CLAUDE.md) §2: what IBVAP should build,
which capabilities to prioritise, what the interface should look like, what
models or runtimes to use, and where compute should sit.

---

## 8. Conclusions

Border CCTV in this domain is the plain, unintelligent layer sitting beneath
a much better-resourced sensor programme (CIBMS): it records and requires a
human to watch it, in an environment where human vigilance is known to
degrade quickly, where sensor-based alerting has historically produced very
high false-alarm rates, and where nobody appears to systematically measure
whether the technology helps. The physical and organisational environment —
erratic power, constrained and unspecified bandwidth, harsh weather, thin
technical staffing, a strict 24-hour handover to civil police, and a specific
statutory evidence-certification requirement — imposes real constraints that
any software solution will need to respect rather than design around.
Documented event volumes (infiltration attempts, contraband seizures, drone
incursions) show the underlying problem is active and, in some categories,
worsening year over year. At the same time, this pass leaves open several
facts that materially affect what a workable product would look like —
particularly the real installed camera base, the identity and interfaces of
"existing command and control systems," and what "suspicious activity" means
operationally — and these should be prioritised for closure (§7) before
product scope in `docs/02-product/` is finalised.

---

## 9. References


Reliability key: **P** = primary/official, **A** = academic or peer-reviewed,
**T** = think-tank / policy analysis, **N** = news, **V** = vendor or trade
(interest-conflicted), **E** = encyclopedic/tertiary.

| ID | Source | Type | URL |
|---|---|---|---|
| S1 | MP-IDSA Issue Brief — *Comprehensive Integrated Border Management System: Issues and Challenges* | T | https://idsa.in/publisher/issuebrief/comprehensive-integrated-border-management-system-issues-and-challenges |
| S2 | ORF — *Comprehensive Integrated Border Management System: Implementation Challenges* | T | https://www.orfonline.org/research/comprehensive-integrated-border-management-system |
| S3 | PIB — *Union Home Minister launches Smart Fencing on Indo-Bangladesh border* (PRID 1567516) and *Rajnath Singh to inaugurate BOLD–QIT* (PRID 1567263) — **[indirect: direct fetch returned HTTP 403]** | P | https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=1567516 |
| S4 | MHA — Press release PDF, HM on CIBMS Assam, 07-03-2019 — **[indirect: HTTP 403]** | P | https://www.mha.gov.in/sites/default/files/PRESSRELEASEHMCIBMSASSAM_07032019.pdf |
| S5 | Wikipedia — *Border Security Force* | E | https://en.wikipedia.org/wiki/Border_Security_Force |
| S6 | ORF — *Integrated check-posts on the India-Bangladesh border: A field survey and brief analysis* | T | https://www.orfonline.org/research/integrated-check-posts-on-the-india-bangladesh-border-a-field-survey-and-brief-analysis |
| S7 | CSEP — *Linking Land Borders: India's Integrated Check Posts* | T | https://csep.org/working-paper/linking-land-borders-indias-integrated-check-posts/ |
| S8 | LPAI — *ICPs: Gateway to India* magazine | P | https://lpai.gov.in/sites/default/files/2022-02/ICPs%20-Gateway-to-India-%20Magazine%20.pdf |
| S9 | *Work exposure and vigilance decrements in closed circuit television surveillance*, Applied Ergonomics (ScienceDirect) | A | https://www.sciencedirect.com/science/article/abs/pii/S0003687014001847 |
| S10 | *Semi-automated CCTV surveillance: The effects of system confidence, system accuracy and task complexity on operator vigilance, reliance and workload*, Applied Ergonomics | A | https://sciencedirect.com/science/article/abs/pii/S0003687012000695 |
| S11 | Sandia National Laboratories, SAND2014-17929 — **NOT RETRIEVED** (connection refused); listed for follow-up per Q-19 | P | https://www.osti.gov/servlets/purl/1322275 |
| S12 | GAO-18-119 — *Southwest Border Security: Border Patrol Is Deploying Surveillance Technologies but Needs to Improve Data Quality and Assess Effectiveness* — **[indirect]** | P | https://www.gao.gov/products/gao-18-119 |
| S13 | GAO-14-368 — *Arizona Border Surveillance Technology Plan* — **[indirect]** | P | https://www.gao.gov/products/gao-14-368 |
| S14 | DHS — *Privacy Impact Assessment for the Border Surveillance Systems (BSS)*, Aug 2014 — **[indirect: HTTP 403]** | P | https://www.dhs.gov/sites/default/files/publications/privacy_pia_CBP_BSS_August2014.pdf |
| S15 | Business Standard / Organiser — *India to build 509 composite border outposts on frontiers with Pakistan, Bangladesh* | N | https://www.business-standard.com/india-news/india-to-build-509-composite-border-outposts-on-frontiers-with-pak-b-desh-123101000439_1.html |
| S16 | Deccan Herald — Indo-Bangladesh infiltration attempts 2025; ₹461 crore contraband seized 2024; tunnel and bunker recoveries | N | https://www.deccanherald.com/india/bsf-seized-rs-461-crore-of-contraband-on-india-bangladesh-border-in-2024-highest-in-10-years-govt-3441748 |
| S17 | The Business Standard (BD) — *India detects 1,104 infiltration attempts along Bangladesh border in 2025* | N | https://www.tbsnews.net/bangladesh/india-detects-1104-infiltration-attempts-along-bangladesh-border-2025-1329766 |
| S18 | News On Air (Prasar Bharati) — BSF drone seizures, Punjab | P/N | https://www.newsonair.gov.in/bsf-seizes-245-drones-smuggling-arms-and-narcotics-from-pakistan-in-punjab |
| S19 | ORF — *Countering Hostile Drone Activity on the India-Pakistan Border* | T | https://www.orfonline.org/research/countering-hostile-drone-activity-on-the-india-pakistan-border |
| S20 | ORF — *India-Bangladesh Border Management: The Challenge of Cattle Smuggling* | T | https://www.orfonline.org/research/india-bangladesh-border-management-the-challenge-of-cattle-smuggling |
| S21 | Drishti IAS — *BOLD-QIT Project* | E | https://www.drishtiias.com/daily-news-analysis/bold-qit-project |
| S22 | India Code — *The Border Security Force Act, 1968*; with Civilsdaily / Deccan Herald analysis of BSF jurisdiction and handover-to-police procedure | P + N | https://www.indiacode.nic.in/bitstream/123456789/1561/1/a1968-47.pdf |
| S23 | ONVIF Profile S Specification v1.3 and ONVIF Streaming Specification; with IPVM discussion on RTSP/ONVIF and per-stream bandwidth | P + V | https://www.onvif.org/wp-content/uploads/2019/12/ONVIF_Profile_-S_Specification_v1-3.pdf |
| S24 | Axis Communications — *Thermal cameras* white paper (Oct 2021) | V | https://www.axis.com/dam/public/1c/66/25/thermal-cameras-en-US-350481.pdf |
| S25 | i-LIDS (Imagery Library for Intelligent Detection Systems), CAST/CPNI — sterile zone monitoring benchmark; trade coverage | P + V | https://www.researchgate.net/publication/284353547_Imagery_Library_for_Intelligent_Detection_Systems_i-LIDS_A_Standard_for_Testing_Video_Based_Detection_Systems |
| S25b | flolive — *Edge AI: applications, challenges & best practices* (satellite backhaul constraints) | V | https://flolive.net/blog/glossary/edge-ai-8-real-world-applications-challenges-best-practices/ |
| S26 | NIST — *Face in Video Evaluation (FIVE)* and *Face Recognition Vendor Test (FRVT)* programme pages; with industry commentary on lab-vs-CCTV degradation | P + V | https://www.nist.gov/programs-projects/face-video-evaluation-five |
| S27 | Plate Recognizer — *ANPR for India*; with ANPR survey literature (PMC8123416) on failure modes | V + A | https://platerecognizer.com/anpr-for-india/ |
| S28 | *Scaling Video Analytics on Constrained Edge Nodes* (arXiv 1905.13536) | A | https://arxiv.org/pdf/1905.13536 |
| S29 | Legal commentary on Section 63, Bharatiya Sakshya Adhiniyam 2023 (replacing s.65B IEA) — certificate, expert signature, hash value | N/T | https://blog.ipleaders.in/electronic-evidence-under-the-bsa-2023/ |
| S30 | Trade/vendor material repeating the "45% at 12 min / 95% at 22 min" operator-attention figure — recorded as unverified, see §4.4 | V | https://www.fortixai.com/blog/ai-detects-what-humans-miss-and-it-never-sleeps |
| S31 | Kashmir Reader / Cadet Direct — anti-infiltration grid and standing patrol doctrine; not India-BSF-specific for the fieldcraft definitions | N | https://kashmirreader.com/2024/10/27/anti-infiltration-grid-very-strong-along-loc-bsf/ |

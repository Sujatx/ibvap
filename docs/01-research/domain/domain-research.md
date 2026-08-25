# Domain Research — Border CCTV Surveillance

**Stage:** 01 — Research → Domain
**Date:** 2026-08-24
**Scope:** The real-world domain described by the official SIH problem statement
([Problem Statement ID 26187](../../00-project/problem.md)) — how border CCTV
surveillance is actually conducted today at Border Out Posts (BOPs), check
posts, and border roads.

> **This document does not decide what IBVAP will build.** It records how the
> domain works, what is known, what is assumed, and what is still unknown.
> Product scoping happens later in `docs/02-product/`, per
> [CLAUDE.md](../../../CLAUDE.md).

---

## How to read this document

Per [CLAUDE.md](../../../CLAUDE.md) §3.7, every substantive statement is
labelled:

| Label | Meaning |
|---|---|
| **FACT** | Verifiable and sourced. The source is cited as `[Sn]`. |
| **ASSUMPTION** | Believed true but not verified against a source. |
| **UNKNOWN** | Identified gap. Nobody on this project knows this yet. |

A statement labelled **FACT** is a fact *about what the cited source says*.
Where a source is a vendor, a news outlet, or a think-tank interpretation
rather than a primary government document, this is noted inline.

### Source retrieval notes

Some primary government sources could not be retrieved directly during this
research pass and are recorded from search-engine summaries of their content
rather than from the document text. These are marked **[indirect]** at the
point of use and listed in [§9 Sources](#9-sources). This is a known weakness
of this research pass — see [§8](#8-unknowns--questions-to-investigate-next),
Q-19.

Blocked on direct fetch (HTTP 403 / network refused) during this pass:
PIB press releases (`pib.gov.in`), MHA press release PDFs (`mha.gov.in`),
DHS Privacy Impact Assessment PDF (`dhs.gov`), Sandia SAND2014-17929
(`osti.gov`), GAO product pages (`gao.gov`).

---

## 1. Operational environment

### 1.1 Where border surveillance happens

**FACT** — Border security forces deploy CCTV cameras at Border Out Posts
(BOPs), check posts, border roads, and other strategic locations for
surveillance and monitoring. *(Source: the official problem statement itself,
[problem.md](../../00-project/problem.md).)*

**FACT** — A Border Out Post (BOP) is the permanent operational base of the
Border Security Force (BSF) along a border. BOPs are described as
self-contained defence outposts with a designated area of responsibility,
equipped with infrastructure for accommodation, logistics and combat
operations. `[S15]` *(news/analysis reporting on an MHA sanction)*

**FACT** — In October 2023 the Government of India sanctioned construction of
**509 composite BOPs** — 383 along the India–Bangladesh border and 126 along
the India–Pakistan border. `[S15]` *(news reporting)*

**FACT** — India's land border guarded by BSF on the Pakistan side spans
**3,323 km**, comprising the 2,308 km Radcliffe Line (International Boundary),
the 776 km Line of Control, and the 110 km Actual Ground Position Line.
Approximately **145.876 km (~6.3%)** is unfenced riverine stretches. `[S2]`

**FACT** — An Integrated Check Post (ICP) is a designated land port for
cross-border movement of people and goods, operated by the Land Ports
Authority of India (LPAI). As of the cited surveys India operated **9 ICPs**:
Attari, Agartala, Petrapole, Raxaul, Jogbani, Moreh, Sutarkandi, Srimantapur,
and Dera Baba Nanak (Kartarpur Corridor). `[S6][S7]`

**FACT** — ICP security infrastructure includes CCTV cameras and observation
towers manned by BSF personnel, alongside baggage/cargo scanners operated by
Customs. `[S6][S7]`

**ASSUMPTION** — "Check post" in the problem statement covers both the large
LPAI-run ICPs and smaller force-run road/track check posts on approach roads.
The problem statement does not disambiguate. *(Basis: the statement lists
"BOPs, check posts, border roads" as a spectrum of locations, not as three
formal categories.)*

**UNKNOWN** — Whether the deploying force for IBVAP would be BSF specifically,
or also ITBP (China border), SSB (Nepal/Bhutan), Assam Rifles (Myanmar), or
state police. The problem statement says "border security forces" generically.

### 1.2 What the terrain and conditions are like

**FACT** — Border terrain in the CIBMS deployment areas includes vast *char*
lands (river islands) and innumerable river channels; the 61 km stretch in
Dhubri district, Assam, where the Brahmaputra enters Bangladesh, is described
as making border guarding "a tough task especially during rainy season."
`[S3][S21]` **[indirect for S3]**

**FACT** — Riverine areas present specific difficulties: equipment must
withstand flash floods and seasonal water-level changes, and concrete
embankments are mandated to stabilise river channels before laser
infrastructure can be installed. `[S2]`

**FACT** — Most border surveillance equipment operates on **line-of-sight**
principles, creating vulnerabilities during heavy rain, storms and dense fog.
Dense vegetation and difficult topography further degrade coverage. `[S1][S2]`

**FACT** — Border observation posts are reported to lack basic electricity and
water connections; the Border Area Development Programme allocates roughly 41%
of funding to infrastructure creation. `[S2]`

**FACT** — Erratic power supply in border regions is identified as an
infrastructure problem for electronic surveillance systems. `[S1]`

**ASSUMPTION** — Fog is a seasonally dominant condition on the Punjab and
Jammu plains in winter, and dust/haze in the western desert sectors. *(Basis:
line-of-sight/fog degradation is repeatedly cited `[S1][S2]` but the sources
do not quantify by sector or season.)*

**UNKNOWN** — Actual measured environmental profile per sector: fog-days per
year, ambient temperature range at camera housings, dust loading, humidity,
lightning incidence, and their effect on installed camera image quality.

### 1.3 What surveillance technology is already deployed

**FACT** — The Comprehensive Integrated Border Management System (CIBMS) is
the Ministry of Home Affairs programme to integrate manpower, sensors,
networks, intelligence and command-and-control to improve situational
awareness. `[S1][S2][S21]`

**FACT** — CIBMS is described as having three main components: (1)
surveillance technology — sensors, detectors, cameras, ground-based radar,
micro-aerostats, lasers; (2) a dedicated communication network — fibre optic
cable and satellite communication; (3) a **Command and Control Centre**, where
data is aggregated so senior commanders receive a composite situational
picture, analyse and classify the threat, and coordinate field response.
`[S1]`

**FACT** — Technologies documented in CIBMS-related deployments include:
thermal imaging and Hand-Held Thermal Imagers (HHTIs), Night Vision Devices
(NVDs) and Passive Night Vision Binoculars (PNVBs), Battlefield Surveillance
Radars (BFSRs) with 360° coverage, laser barriers, CCTV cameras operating
round-the-clock, Unattended Ground Sensors, fibre-optic communication, a 3-D
GIS terrain layer, satellite imagery from ISRO and NTRO, UAVs and aerostat
balloons with day/night vision, and underground monitoring sensors. `[S2]`

**FACT** — **BOLD-QIT** (Border Electronically Dominated QRT Interception
Technique) was undertaken by the BSF's Information and Technology Wing in
January 2018 and inaugurated in March 2019, covering the Brahmaputra span in
Dhubri with microwave communication, OFC cables, DMR communication, day and
night surveillance cameras and an intrusion detection system. **These feeds go
to BSF Control Rooms on the border and enable BSF Quick Reaction Teams (QRTs)
to intercept illegal crossings.** `[S3][S21]` **[indirect for S3]**

**FACT** — Two CIBMS "smart fencing" pilot projects in the Samba sector,
Jammu — stretches of **5.3 km and 5.5 km** — were operationalised in September
2018. Stage-I pilots (Jammu and Assam) are reported complete; Stage-II
involves rollout of **153 km in 4 patches** along the Indo-Pakistan and
Indo-Bangladesh borders. `[S3][S4]` **[indirect]**

**FACT** — In 2025 the BSF is reported to have deployed around 5,000
body-worn cameras, biometric recording devices and night-vision-enabled
monitoring systems along the Bangladesh border. `[S5]` *(encyclopedic
secondary source — treat as low-confidence)*

**ASSUMPTION** — The CCTV cameras the problem statement refers to as "existing
CCTV infrastructure" are predominantly standard IP cameras recorded to
DVR/NVR appliances and viewed on a video wall or client software, rather than
the specialised CIBMS sensor suite. *(Basis: the problem statement explicitly
contrasts "standard IP-based CCTV cameras" against "dedicated FRS, ANPR, or
smart-camera hardware". The CIBMS sensor grid described in `[S1][S2]` covers
only pilot-scale km counts, whereas CCTV is described as being at BOPs, check
posts and border roads generally.)*

**UNKNOWN** — The actual installed base: how many cameras per BOP/check post,
which makes/models, what resolution, what codec, whether PTZ or fixed, whether
they are ONVIF-conformant, whether they are on an isolated LAN, and what
DVR/NVR or VMS software (if any) sits in front of them.

**UNKNOWN** — Whether "existing CCTV infrastructure" in the problem statement
means CIBMS-era installations, older standalone installations, or both.

---

## 2. People / users involved

The problem statement names only "border security forces". The following roles
are reconstructed from the sources and are labelled accordingly.

### 2.1 Roles identified in sources

**FACT** — **BSF Control Room** operators exist at border level and receive
sensor/camera feeds; the stated operational purpose is to enable QRTs to
intercept. `[S3][S21]` **[indirect for S3]**

**FACT** — **Quick Reaction Teams (QRTs)** are the field response element
dispatched on detection; interception by QRT is the named outcome in BOLD-QIT.
`[S3][S21]` **[indirect for S3]**

**FACT** — **Senior commanders** at the Command and Control Centre receive a
composite situational picture, analyse and classify the threat, and coordinate
response. `[S1]`

**FACT** — The BSF has approximately **290,000 active personnel** across
**192 battalions**. `[S5]` *(encyclopedic secondary source)*

**FACT** — In the US analogue, Border Patrol **agents** both monitor
surveillance feeds and respond in the field, and record "asset assists" —
instances where a technology contributed to an apprehension or seizure.
`[S12]` **[indirect]**

### 2.2 Roles inferred

**ASSUMPTION** — A typical staffing chain for a camera-derived incident is:
*camera → control-room operator (detects/notices) → post commander or duty
officer (assesses/decides) → QRT (responds) → record-keeper (logs).* *(Basis:
this is the shape implied by `[S1]` (analyse/classify/coordinate) and
`[S3][S21]` (feeds → control room → QRT). The intermediate assessment role is
not named explicitly in any retrieved source.)*

**ASSUMPTION** — Control-room duty is a rotating shift assignment held by
general-duty personnel, not by a dedicated professional CCTV-operator cadre.
*(Basis: `[S1]` reports "lack of technical expertise for equipment operation
and maintenance among BSF personnel" as a systemic deficiency, which is
inconsistent with a specialist operator cadre.)*

**ASSUMPTION** — Surveillance output has at least three distinct consumers
with different needs: the **operator** (needs to not miss things, right now),
the **commander** (needs an assessed picture to decide), and the
**investigator/prosecutor** (needs retrievable, defensible evidence after the
fact). *(Basis: `[S1]` for the first two; `[S22][S29]` for the third.)*

**UNKNOWN** — How many operators are on duty per control room, how many
cameras/screens each watches, shift length, rotation policy, and whether
operators are trained or certified in monitoring specifically.

**UNKNOWN** — Whether officers above battalion level (Sector, Frontier, Force
HQ, MHA) consume live video, only summaries, or only post-incident reports.

**UNKNOWN** — Whether civilian/contracted technicians maintain the CCTV
systems, and whether they have access to feeds or recordings.

**UNKNOWN** — Whether any non-force stakeholders (Customs, immigration,
state police, intelligence agencies) consume the same camera feeds at ICPs.

---

## 3. Current surveillance workflow

### 3.1 The baseline workflow the problem statement describes

**FACT** — Conventional CCTV systems primarily provide **video recording and
live monitoring**, requiring **continuous human observation**. *(Source: the
problem statement, [problem.md](../../00-project/problem.md).)*

This is the workflow IBVAP's domain begins from: a human watches, and a
recorder records.

### 3.2 Detection → assessment → response

**FACT** — In the CIBMS design, field detection equipment feeds data through
communication networks to centralised command posts, where commanders analyse
the information and direct quick reaction teams deployed in the field. `[S1]`

**FACT** — Laser barriers trigger **audible sirens** when an object breaches
coverage. `[S2]`

**FACT** — The cited analysis notes the CIBMS design does **not** define
protocols for distinguishing infiltrators from wildlife or environmental
factors that generate alerts. `[S2]`

**FACT** — In the US analogue, the operational sequence for border
surveillance is described as **detect → track → identify/classify → resolve**.
`[S14]` **[indirect]**

**ASSUMPTION** — The practical Indian border workflow is: *sensor or operator
detects something → operator or duty officer slews a camera / looks harder to
**assess** whether it is a real threat → if real, a QRT is dispatched and
informed by radio → the outcome (apprehension, seizure, nothing found) is
recorded → recorded video is retained and retrieved later if the incident
becomes a case.* *(Basis: assembled from `[S1]`, `[S2]`, `[S3]`, `[S14]`. No
retrieved source states the full Indian sequence end-to-end.)*

**ASSUMPTION** — **Detection and assessment are separate functions.** A sensor
alarm is not an incident; a human must look at imagery to decide. This is the
core reason CCTV exists alongside fences and sensors: cameras are the
*assessment* medium for alarms raised by other means. *(Basis: `[S1]`
describes the Command and Control Centre's function as "analyse and classify
the threat", which is assessment, distinct from the sensors' detection. The
Sandia perimeter-security literature that formalises this distinction
(`[S11]`) could not be retrieved in this pass — see Q-19.)*

### 3.3 Alert handling

**UNKNOWN** — What an operator is *required* to do when an alert fires:
acknowledge, log, escalate, dispatch? Is there a written SOP or Standing Order?

**UNKNOWN** — What communications channel carries the alert to the QRT (DMR
radio is named in BOLD-QIT `[S3]`, but the alerting procedure is not).

**UNKNOWN** — Response-time expectations. Is there a target time from
detection to interception?

### 3.4 Event logging

**FACT** — "Real-time alert generation and **event logging**" is named as a
required capability in the problem statement. Its presence as a *requirement*
indicates it is currently either absent or inadequate.

**ASSUMPTION** — Event logging today is largely manual and paper- or
register-based at post level, with video retrieval done ad hoc by scrubbing
DVR timelines. *(Basis: inference from the problem statement's framing of
conventional CCTV as "recording and live monitoring" only. Not sourced.)*

**UNKNOWN** — Whether any digital incident register exists today, what fields
it captures, and whether it is linked to the video.

### 3.5 Investigation / evidence workflow

**FACT** — The BSF does **not** have policing powers. After apprehending a
suspect it cannot register an FIR or conduct an investigation; it may conduct
only "preliminary questioning", and the seized consignment or suspect must be
handed over to the local police **within 24 hours**. `[S22]` *(news/analysis
reporting on the BSF Act 1968 and CrPC-derived powers)*

**FACT** — BSF powers of arrest, search and seizure extend to a defined belt
from the international border — reported as up to 50 km in Assam, Punjab and
West Bengal following a 2021 notification (previously 15 km), and up to 80 km
in Gujarat. `[S22]` *(the 15 km figure is what the cited article states as the
previous regime; the notification change is politically contested)*

**FACT** — In India, electronic records including CCTV footage are governed by
**Section 63 of the Bharatiya Sakshya Adhiniyam (BSA), 2023**, in force from
**1 July 2024**, replacing Section 65B of the Indian Evidence Act, 1872.
Admissibility of a copy requires a certificate signed by the person in charge
of the device **and** an expert, and the certificate must disclose the
record's **hash value**. `[S29]` *(legal-commentary secondary sources; the
statute text itself was not retrieved)*

**ASSUMPTION** — This makes the border evidence chain cross-organisational:
the force detects and records, but the *case* is built by state police and
tried in a civil court, which means exported video must survive a handover to
an organisation that did not produce it. *(Basis: combining `[S22]` and
`[S29]`.)*

**UNKNOWN** — Current practice for exporting and handing over CCTV footage:
format, who signs, whether hashes are computed, how long retrieval takes,
and how often footage is actually used in prosecutions.

**UNKNOWN** — Video retention periods mandated or practised at BOPs and ICPs.

### 3.6 Command and control integration

**FACT** — The problem statement requires "integration with existing command
and control systems," and `[S1]` confirms a Command and Control Centre is
architecturally central to CIBMS.

**FACT** — `[S1]` flags that **centralised decision-making may delay urgent
field responses** — i.e. C2 integration is not purely a benefit; routing
decisions upward has an operational cost.

**UNKNOWN** — What the "existing command and control systems" concretely are:
their names, vendors, protocols, APIs, data models, and whether they are
network-reachable from where cameras sit.

**UNKNOWN** — At what echelon the C2 system lives (BOP, Company, Battalion,
Sector, Frontier, Force HQ) and whether each echelon runs a different one.

---

## 4. Problems with conventional CCTV monitoring

### 4.1 The human attention problem

**FACT** — Vigilance decrement — a measurable decrease in task performance
over time — generally occurs **20 to 35 minutes** after engaging in a
sustained-attention task. `[S9]` *(peer-reviewed ergonomics literature)*

**FACT** — CCTV surveillance is vigilance-intensive; operators are typically
required to observe **3 to 30 camera scenes concurrently** to detect potential
incidents. `[S9][S10]`

**FACT** — Operator performance directly determines system effectiveness: the
system's value is bounded by the operator's ability to detect significant
events. `[S9]`

**ASSUMPTION / CONTESTED** — The widely repeated claim that an operator misses
"up to 45% of screen activity after 12 minutes and up to 95% after 22 minutes"
appears throughout industry material `[S30]`, but the sources repeating it are
vendor and trade publications, and the underlying study is not identifiable
from them. **Treat the specific percentages as unverified.** The
peer-reviewed finding that is defensible is the 20–35 minute vigilance
decrement above `[S9]`. *(Recorded here because this figure will certainly
appear in competitor material and hackathon pitches, and the project should
know it is soft.)*

**FACT** — Operator reliance on a semi-automated system is itself affected by
the system's stated confidence, actual accuracy, and task complexity —
i.e. adding automation changes operator behaviour, not just workload. `[S10]`
*(peer-reviewed)*

### 4.2 The false / nuisance alarm problem

**FACT** — In the US SBInet programme, **90 per cent of sensor alerts were
false alarms**, cited as a cautionary parallel for CIBMS. `[S1]`

**FACT** — CIBMS-related analysis reports **false alarms and sensor
malfunctions** as a leading technical issue, alongside line-of-sight
constraints and unreliable information transmission. `[S1]`

**FACT** — The CIBMS design does not address protocols for distinguishing
infiltrators from wildlife or environmental triggers. `[S2]`

**ASSUMPTION** — The dominant nuisance-alarm sources at Indian borders are
livestock (including smuggled cattle themselves), wildlife, vegetation motion
in wind, rain and insects on the lens, headlight/IR glare at night, and
civilian agricultural activity in the border belt. *(Basis: general perimeter
security knowledge plus `[S2]`'s explicit mention of wildlife. Not measured
for these sites.)*

**ASSUMPTION** — An alerting system that is not trusted gets ignored or muted,
which is worse than no alerting system, because it consumes attention and
supplies false assurance. *(Basis: inference from `[S10]`'s finding that
system accuracy drives operator reliance.)*

### 4.3 The "recording is not intelligence" problem

**FACT** — Conventional CCTV provides recording and live monitoring only; the
advanced functions (FRS, ANPR, intrusion detection, object tracking) require
specialised hardware and proprietary solutions, making large-scale deployment
costly and difficult particularly in remote border areas. *(Source: the
problem statement.)*

**FACT** — Exorbitant equipment costs, unavailability of spare parts, and high
reliance on external vendors with minimal oversight are documented CIBMS
problems. `[S1]`

**FACT** — Lack of technical expertise for equipment operation and maintenance
among BSF personnel is a documented deficiency. `[S1]`

**FACT** — BSF requests for proposals have allowed vendors to "arrive at their
own conclusions" rather than specifying technical requirements, indicating
insufficient in-house technical specification capability. `[S1]`

### 4.4 The "was it useful?" problem

**FACT** — GAO found that Border Patrol had **not used available data to
determine the contribution of surveillance technologies** to border security
outcomes. `[S12]` **[indirect]**

**FACT** — GAO found data-quality problems in agent-reported "asset assist"
data: stations in the Rio Grande Valley sector recorded assists from Integrated
Fixed Towers in about **500 instances from June through December 2016** —
a sector that **has no IFTs**. `[S12]` **[indirect]**

**FACT** — GAO found that planned IFT testing would determine mission
contribution but **not effectiveness and suitability under varying
environmental conditions such as weather**, contrary to DHS guidance. `[S13]`
**[indirect]**

**ASSUMPTION** — The same measurement gap is likely present in Indian
deployments: whether a camera or analytic contributed to an interception is
not systematically captured, so effectiveness cannot be evaluated. *(Basis:
`[S1]`'s finding of weak vendor oversight and absent in-house technical
capability suggests weak outcome measurement, but no Indian source was found
either way.)*

**UNKNOWN** — Whether any Indian force records which detections were
technology-assisted, and whether any effectiveness baseline exists.

---

## 5. Typical surveillance events

This section catalogues what actually happens at these borders — the events an
operator is watching for. Frequency and scale figures are given where sourced.

### 5.1 Illegal crossing / infiltration

**FACT** — Indian security forces detected **1,104 infiltration attempts**
along the India–Bangladesh border in 2025, up from **977 in 2024** — reported
as the highest annual figure in nearly a decade. `[S16][S17]` *(news)*

**FACT** — More than **2,550 Bangladeshi nationals** were reported detained in
2025 attempting to enter India illegally. `[S17]` *(news)*

**FACT** — CIBMS is stated to improve BSF capability against illegal
infiltration, smuggling of contraband, human trafficking, and cross-border
terrorism. `[S1][S21]`

### 5.2 Smuggling — goods, livestock, narcotics

**FACT** — BSF seized contraband worth **₹461.07 crore** on the
India–Bangladesh border in 2024, reported as the highest in 10 years. `[S16]`
*(news)*

**FACT** — The cattle trade from India to Bangladesh is reported to be worth
approximately **$500 million annually**; it is illegal under Indian law and
long predates the border fence. `[S20]` *(think-tank/academic)*

**FACT** — On 26 January 2025, BSF found three large underground bunkers used
for narcotics smuggling on the India–Bangladesh border, holding ₹1.4 crore
worth of codeine-based cough syrup at Majhdia, ~2 km from the border. `[S16]`
*(news)*

### 5.3 Aerial incursion — drones

**FACT** — BSF seized **245 drones** from Pakistan in Punjab in 2024 (another
report gives 294 for the year). By October 2025 the force reported seizing
**200 Pakistani drones** carrying 287 kg of heroin, 174 weapons including
AK-47s, hand grenades and explosives. `[S18][S19]` *(state news agency and
think-tank)*

**FACT** — Punjab is described as the epicentre of drone-assisted narcotics
trafficking, with almost all such incidents in the country occurring along its
border. `[S19]`

**ASSUMPTION** — Drone incursion is an event class that fixed ground CCTV is
poorly positioned to catch (small, fast, above the camera's typical field of
view and elevation), and is likely handled by dedicated counter-UAS systems
rather than by the CCTV grid. *(Basis: geometry; not sourced. Relevant because
the problem statement does not list drones among required capabilities.)*

### 5.4 Tunnels and sub-surface crossing

**FACT** — On 17 July 2024 a 40-metre tunnel was uncovered in West Bengal.
`[S16]` *(news)*

**ASSUMPTION** — Tunnel detection is out of reach of video analytics on
surface cameras except indirectly (spoil heaps, repeated visits to a fixed
location, unexplained vehicle stops). *(Not sourced.)*

### 5.5 Vehicle and person movement at check posts

**FACT** — At ICPs, movement of people and cargo is the routine flow; security
infrastructure includes CCTV cameras, observation towers, baggage scanners,
full-body truck scanners (the Attari truck scanner is reported non-operational)
and handheld detection equipment. `[S6][S7]` *(think-tank field survey and
press reporting)*

**ASSUMPTION** — Check-post events are dominated by *routine, high-volume,
legitimate* traffic, whereas BOP/border-road events are dominated by *rare,
anomalous* activity. These are operationally different problems: one is
throughput and record-keeping, the other is needle-in-haystack detection.
*(Basis: inference from the function of an ICP as a trade/transit port `[S6]`
versus a BOP as a defence outpost `[S15]`. Not directly sourced.)*

### 5.6 Night-time movement

**FACT** — "Night-time movement detection" is named as a required capability
in the problem statement, and CIBMS deployments consistently pair "day and
night surveillance cameras" `[S3][S21]` with NVDs, PNVBs and thermal imagers
`[S2]`, indicating night is treated as a distinct operating regime.

**ASSUMPTION** — Infiltration and smuggling attempts concentrate in darkness
and in poor-visibility conditions (fog, rain), i.e. exactly when conventional
CCTV performs worst. *(Widely stated in the security literature but not
quantified in any source retrieved here.)*

### 5.7 Event classes named by the problem statement itself

For completeness, the capabilities named in
[problem.md](../../00-project/problem.md) imply these event classes:
human presence/movement, vehicle presence/type, a detectable face, a readable
number plate, a crossing of a defined virtual line or region, "suspicious
activity", and night-time movement. **UNKNOWN** — what "suspicious activity"
means operationally to this user; it is undefined in the statement and
undefined in every retrieved source.

---

## 6. Operational constraints

### 6.1 Power

**FACT** — Erratic power supply in border regions is a documented
infrastructure problem for electronic surveillance. `[S1]`

**FACT** — Border observation posts are reported to lack basic electricity and
water connections; no comprehensive electrification plan is documented in the
cited materials. `[S2]`

**UNKNOWN** — Actual power availability at a representative BOP: grid hours
per day, generator capacity and fuel logistics, solar/battery provision, and
the resulting power budget available to any additional computing hardware.

### 6.2 Connectivity and bandwidth

**FACT** — CIBMS uses a dedicated communication network including fibre optic
cable and satellite communication. `[S1]` BOLD-QIT specifically used microwave
communication, OFC cables and DMR communication. `[S3][S21]`

**FACT** — Specific bandwidth requirements and communication backbone
specifications are **not stated** in the reviewed CIBMS literature; the
analysis explicitly flags this gap, noting that thermal imaging and radar feeds
require adequate capacity to reach command centres. `[S2]`

**FACT** — In constrained deployments, per-camera uplink allocations can be
"a few hundred kilobits per second or less", which conflicts with streaming
all video centrally for analysis. `[S28]` *(peer-reviewed/arXiv systems
research)*

**FACT** — Satellite links, while they enable remote deployment, are typically
high-latency, low-bandwidth and expensive, making it difficult to offload data
or receive updates efficiently. `[S25b]` *(vendor/industry source)*

**FACT** — A single H.264 IP camera stream in the cited discussion is on the
order of **5 Mbps**, and each additional client pulling the stream multiplies
that load off the camera (3 clients × 5 Mbps = 15 Mbps). `[S23]` *(industry
discussion)*

**FACT** — H.265 delivers roughly the same visual quality as H.264 at about
half the bitrate, halving both storage and LAN bandwidth. `[S23]`

**ASSUMPTION** — Any architecture that requires shipping full-rate video from
a remote BOP to a central site for analysis is bandwidth-infeasible at scale
on this network. *(Basis: `[S2]`'s unspecified backbone + `[S28]`'s
constrained-uplink finding + `[S23]`'s per-stream figures. This is an
architectural implication and is recorded here as a **research finding, not a
decision** — architecture decisions belong in `docs/04-architecture/`.)*

### 6.3 Environment and weather

**FACT** — Line-of-sight equipment is vulnerable to heavy rain, storms and
dense fog. `[S1][S2]` Adverse terrain and weather undermine system function.
`[S1]`

**FACT** — Thermal imaging is often marketed as weather-immune, but fog and
rain **do** severely limit thermal range, because scattering in water droplets
diminishes the infrared signal — a higher droplet density causes more
attenuation. `[S24]` *(manufacturer white paper — note the source is a vendor,
but the claim is against the vendor's own interest and matches physics)*

**FACT** — Thermal cameras detect heat rather than motion, which makes them
better at rejecting environmental noise such as shadows and moving foliage,
and unaffected by glare and backlighting. `[S24]` *(vendor)*

**UNKNOWN** — What proportion of existing border CCTV is thermal versus
visible-light, and whether visible cameras have IR illuminators, true
day/night sensors, or neither.

### 6.4 Maintenance, spares and skills

**FACT** — Equipment maintenance is identified as critical, with specialised
technical training and spare-parts availability both undefined challenges.
`[S1][S2]`

**FACT** — There is high reliance on external vendors with minimal oversight.
`[S1]`

**FACT** — A proposal exists to raise a **technical battalion** at Frontier
level with company-strength detachments at Sector HQs to enable localised
repair and reduce servicing turnaround. `[S2]` *(a recommendation in the
source, not an implemented fact)*

**ASSUMPTION** — Any software deployed at a BOP must survive long periods
without an on-site engineer and must fail in a way a non-specialist can
recognise and report. *(Basis: inference from `[S1]`'s skills finding.)*

### 6.5 Cost and scale

**FACT** — The problem statement requires the solution to be cost-effective,
scalable, and suitable for deployment across remote border locations and
strategic installations, and to eliminate dependence on expensive dedicated
surveillance hardware.

**FACT** — Exorbitant equipment cost is a documented barrier. `[S1]`

**ASSUMPTION** — "Scalable" here means *scalable across many small, isolated
sites*, not *scalable to a large central cluster*. The scaling axis is site
count, not user count. *(Basis: the statement's own phrase "across remote
border locations".)*

### 6.6 Legal, procedural and organisational constraints

**FACT** — BSF cannot register an FIR or investigate; suspects and seizures
must be handed to local police within 24 hours. `[S22]`

**FACT** — Electronic evidence in India requires a Section 63 BSA certificate
including a hash value, signed by the person in charge of the device and an
expert. `[S29]`

**FACT** — Land acquisition has been a chronic obstacle to border
infrastructure: ~24,000 acres belonging to ~6,000 families across 212 villages
in six Punjab districts remained in dispute since 1988; an audit found abnormal
delays in **66% of land acquisition cases**, some extending nine years. `[S2]`

**FACT** — Centralised decision-making is flagged as a risk of potentially
delaying urgent field responses. `[S1]`

**UNKNOWN** — Data classification, security accreditation, and network
policy that would apply to a software platform handling live border video
(e.g. whether it may touch the internet at all, whether cloud is permissible,
what certification is required).

**UNKNOWN** — Privacy/legal constraints on face recognition applied to
civilians in the border belt, who are largely Indian residents going about
agricultural life.

### 6.7 Technology performance constraints relevant to the named capabilities

Recorded here because they bound what any software can achieve on this
hardware — these are domain constraints, not design choices.

**FACT** — Face recognition accuracy degrades substantially between controlled
enrolment conditions and production CCTV; angle, lighting and resolution are
the primary degradation factors. NIST benchmarks use cooperative subjects,
controlled lighting, frontal poses and high resolution, while production CCTV
provides none of these. NIST's FIVE programme specifically covers
non-cooperative subjects and degraded video. `[S26]` *(the NIST programme
descriptions are primary; the specific accuracy-drop percentages come from a
vendor/industry commentary and should be treated as indicative only)*

**FACT** — India has roughly **210 million vehicles** and **over 50 different
types of number plate**; countries with standardised plates (Australia,
Vietnam, Italy) see ANPR accuracy often exceeding 90%. `[S27]` *(ANPR vendor —
treat the comparison as directional)*

**FACT** — Documented ANPR failure modes include non-standardised formats,
fancy fonts, plate condition, complex scenes, camera quality and mounting
position, distortion, motion blur, contrast, reflections, processing/memory
limits, and day/night conditions. Fast-moving vehicles create motion blur and
shorten capture time; recognition falls sharply above the camera's processing
limit. `[S27]`

**FACT** — **i-LIDS** (Imagery Library for Intelligent Detection Systems) is a
UK government benchmark developed by CAST with CPNI for evaluating video
analytics against security scenarios including **sterile zone monitoring**
(detecting persons in a restricted area). Systems meeting the criteria may be
certified as a **primary (sole)** detection system or only as a **secondary
(support)** measure. Datasets contain ~24 hours of footage per scenario,
filmed across all weather conditions, times of day and scene densities.
`[S25]`

**ASSUMPTION** — The primary/secondary distinction in `[S25]` is the most
important framing in this whole document for how border operators are likely
to think about AI analytics: an analytic is either trusted to be the *only*
thing watching, or it is a *support* to a human who is still watching. Which
of these an operator believes determines whether the system reduces workload
at all. *(Interpretation; the source states the certification categories but
not this operational implication.)*

**FACT** — ONVIF Profile S standardises live H.264 streaming, audio, PTZ
control, motion-detection events and basic metadata; most Profile S cameras
also expose a plain RTSP URL. ONVIF announced on **9 October 2025** that it is
ending support for Profile S in favour of Profile T; after **31 March 2027**
manufacturers can no longer submit new products for Profile S conformance.
`[S23]`

---

## 7. Existing terminology

Terms used in the domain, with the source that establishes each. This glossary
is descriptive of the domain — it is not IBVAP vocabulary.

### 7.1 Places and organisation

| Term | Meaning | Source |
|---|---|---|
| **BOP** — Border Out Post | Permanent operational base of the border force with a designated area of responsibility; self-contained, with accommodation, logistics and combat infrastructure | `[S15]` |
| **Composite BOP** | Newer BOP design; 509 sanctioned in 2023 (383 Indo-Bangladesh, 126 Indo-Pakistan) | `[S15]` |
| **Check post** | Manned control point for movement across or near the border | problem statement |
| **ICP** — Integrated Check Post | LPAI-operated land port combining immigration, customs, cargo and security functions | `[S6][S7]` |
| **LPAI** — Land Ports Authority of India | Statutory body operating ICPs | `[S6][S7]` |
| **BSF** — Border Security Force | CAPF under MHA guarding the Indo-Pakistan and Indo-Bangladesh borders; ~290,000 personnel, 192 battalions | `[S5]` |
| **Frontier / Sector / Battalion / Company** | Descending echelons of BSF command referenced in technical-battalion and C2 proposals | `[S2]` |
| **IB** — International Boundary | The 2,308 km Radcliffe Line segment | `[S2]` |
| **LoC** — Line of Control | 776 km | `[S2]` |
| **AGPL** — Actual Ground Position Line | 110 km | `[S2]` |
| **Char land** | River island/sandbar terrain, prominent in the Brahmaputra riverine border | `[S3][S21]` |

### 7.2 Systems and programmes

| Term | Meaning | Source |
|---|---|---|
| **CIBMS** | Comprehensive Integrated Border Management System — MHA programme integrating manpower, sensors, networks, intelligence and C2 | `[S1][S2]` |
| **BOLD-QIT** | Border Electronically Dominated QRT Interception Technique — CIBMS implementation over 61 km of riverine border at Dhubri, Assam | `[S3][S21]` |
| **Smart fencing** | Popular name for the CIBMS electronic surveillance grid used in place of, or alongside, physical fence | `[S3][S4]` |
| **Command and Control Centre** | Hub where sensor data is aggregated into a composite situational picture for commanders to analyse, classify and coordinate response | `[S1]` |
| **Control Room** | Border-level facility receiving camera and sensor feeds and cueing QRTs | `[S3][S21]` |

### 7.3 People and response

| Term | Meaning | Source |
|---|---|---|
| **QRT** — Quick Reaction Team | Field element dispatched to intercept on detection | `[S3][S21]` |
| **Standing patrol** | Small static element (min. 1 NCO + 3 men in the cited doctrine) posted to observe and disrupt infiltration, watching over obstacles | `[S31]` *(general fieldcraft source, not India-specific — low confidence)* |
| **Anti-infiltration grid** | Layered arrangement of patrols, ambushes and obstacles along likely infiltration routes | `[S31]` *(news/analysis)* |
| **Asset assist** *(US term)* | A recorded instance in which a technology contributed to an apprehension or seizure | `[S12]` |

### 7.4 Sensors and imaging

| Term | Meaning | Source |
|---|---|---|
| **HHTI** | Hand-Held Thermal Imager | `[S2]` |
| **NVD / PNVB** | Night Vision Device / Passive Night Vision Binocular | `[S2]` |
| **BFSR** | Battlefield Surveillance Radar, 360° coverage | `[S2]` |
| **UGS** | Unattended Ground Sensor | `[S2]` |
| **Laser barrier / laser wall** | Beam-break intrusion detection used on unfenced riverine gaps; triggers an audible siren | `[S2]` |
| **Aerostat / micro-aerostat** | Tethered balloon carrying day/night sensors | `[S1][S2]` |
| **OFC / DMR / microwave** | Optical Fibre Cable / Digital Mobile Radio / microwave link — the BOLD-QIT communications mix | `[S3][S21]` |

### 7.5 Surveillance-industry terms

| Term | Meaning | Source |
|---|---|---|
| **ONVIF Profile S / Profile T** | Interoperability profiles for IP video; S covers H.264 live streaming, PTZ, motion events, basic metadata; T is its successor | `[S23]` |
| **RTSP** | Media-plane protocol carrying the actual video stream | `[S23]` |
| **NVR / DVR / VMS** | Network or Digital Video Recorder / Video Management System — the recording and viewing layer | `[S23]` |
| **Sterile zone monitoring** | i-LIDS scenario: detecting the presence of persons in a restricted area | `[S25]` |
| **Primary vs secondary detection system** | i-LIDS certification categories: sole detection system, versus support to a human/other primary system | `[S25]` |
| **Vigilance decrement** | Measurable decline in sustained-attention task performance over time, typically onset 20–35 min | `[S9]` |
| **Nuisance / false alarm** | Alarm from a real but benign cause, versus alarm with no cause; the dominant failure mode of sensor-based perimeter systems | `[S1][S2]` |
| **Detect → track → identify/classify → resolve** | The US border surveillance operational sequence | `[S14]` |

### 7.6 Legal and evidentiary

| Term | Meaning | Source |
|---|---|---|
| **BSF Act, 1968** | Statute establishing the BSF and its powers | `[S22]` |
| **Section 63, BSA 2023** | Provision governing admissibility of electronic records (replacing s.65B IEA 1872 from 1 July 2024); requires a certificate with hash value | `[S29]` |
| **Chain of custody** | Documented custody trail required to establish integrity of a digital record | `[S29]` |

---

## 8. Unknowns / questions to investigate next

Ordered by how much the answer would change subsequent stages. None of these
are answered by the sources reviewed in this pass.

### Highest priority — block product scoping

- **Q-1** What is the actual installed camera base at a representative BOP and
  check post? Count, model, resolution, codec, PTZ vs fixed, thermal vs
  visible, ONVIF conformance, age. *(§1.3)*
- **Q-2** What recording/VMS layer exists today, and is it reachable over a
  network from a place where compute could sit? *(§1.3)*
- **Q-3** What does "suspicious activity" mean to a border operator, stated as
  observable behaviour? The problem statement names the capability but no
  source defines it. *(§5.7)*
- **Q-4** What are the "existing command and control systems" by name, with
  their interfaces? *(§3.6)*
- **Q-5** How many operators watch how many cameras, on what shift pattern,
  and what are they told to do when they see something? *(§2.2, §3.3)*

### High priority — shape the problem

- **Q-6** What is the real nuisance-alarm profile at these sites: what actually
  triggers false alerts, and how often? *(§4.2)*
- **Q-7** What is the power budget available at a BOP for additional compute?
  *(§6.1)*
- **Q-8** What is the actual available bandwidth from BOP to the next echelon,
  and is it symmetric, metered, or shared with voice/radio? *(§6.2)*
- **Q-9** What retention period is required or practised for border CCTV?
  *(§3.5)*
- **Q-10** What is the current procedure for exporting footage for a case
  handed to local police, and does it currently satisfy Section 63 BSA?
  *(§3.5)*
- **Q-11** Is there a written SOP/Standing Order for alarm assessment and
  escalation that could be read? *(§3.3)*
- **Q-12** What response-time target, if any, exists from detection to
  interception? *(§3.3)*

### Medium priority — validate assumptions in this document

- **Q-13** Is the control-room role a rotating general duty or a specialist
  cadre? (Tests the assumption in §2.2.)
- **Q-14** Do check posts and BOPs really have different event profiles
  (throughput vs. anomaly)? (Tests §5.5.)
- **Q-15** What proportion of border CCTV is thermal? (Tests §6.3.)
- **Q-16** What are the measured environmental conditions per sector — fog
  days, temperature range, dust? (§1.2)
- **Q-17** Which forces beyond BSF are in scope? (§1.1)
- **Q-18** What security accreditation, data classification and network policy
  would apply to a video analytics platform on this network? (§6.6)

### Research-process gaps

- **Q-19** Retrieve the primary sources that this pass could not fetch
  directly: MHA Annual Report border-management chapter, PIB releases on CIBMS
  and BOLD-QIT, the Sandia perimeter-security reference (SAND2014-17929) for
  formal Pd/NAR/FAR definitions, DHS PIA for Border Surveillance Systems, and
  the GAO reports GAO-18-119 / GAO-14-368 in full. Several §3–§6 claims
  currently rest on search-engine summaries rather than document text.
- **Q-20** Find the primary study behind the "45% at 12 min / 95% at 22 min"
  operator-attention claim, or establish that it does not exist. (§4.1)
- **Q-21** Locate any published Indian-language or force-internal doctrine on
  CCTV monitoring at BOPs. None was found in this pass.

### Deliberately deferred (not this stage)

The following are **not** domain questions and belong to later stages, per
[CLAUDE.md](../../../CLAUDE.md) §2. They are listed only so they are not
mistaken for gaps in this document: what IBVAP should build, which
capabilities to prioritise, what the interface should look like, what models
or runtimes to use, and where compute should sit.

---

## 9. Sources

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
| S30 | Trade/vendor material repeating the "45% at 12 min / 95% at 22 min" operator-attention figure — **recorded as unverified**, see §4.1 | V | https://www.fortixai.com/blog/ai-detects-what-humans-miss-and-it-never-sleeps |
| S31 | Kashmir Reader / Cadet Direct — anti-infiltration grid and standing patrol doctrine; **not India-BSF-specific for the fieldcraft definitions** | N | https://kashmirreader.com/2024/10/27/anti-infiltration-grid-very-strong-along-loc-bsf/ |

---

## Document status

**Complete for Phase 1 — Domain Research.** No product, design, architecture,
or technology decisions are made or implied by this document. Assumptions
recorded here require validation before they are relied on in
`docs/02-product/`; unknowns in [§8](#8-unknowns--questions-to-investigate-next)
are the input to the next research passes (users, competitors, technology).

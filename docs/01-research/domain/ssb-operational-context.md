# SSB Operational Context — Sashastra Seema Bal

**Stage:** 01 — Research → Domain
**Date:** 2026-08-24
**Scope:** The operational context of **Sashastra Seema Bal (SSB)** — the
department named for [SIH Problem Statement 26187](../../00-project/problem.md)
— covering its border surveillance structure, BOPs and check posts, surveillance
responsibilities, CCTV/video usage, control rooms and monitoring workflow,
detection → assessment → response, surveillance technologies already in service,
command/control integration, remote-location constraints, and SSB-specific
legal/evidentiary considerations for recorded video.

> **This document does not decide what IBVAP will build.** It records how SSB
> works, what is known, what is assumed, and what is still unknown. Product
> scoping happens later in `docs/02-product/`, per [CLAUDE.md](../../../CLAUDE.md).

**Companion document:** [domain-research.md](domain-research.md) covers the
generic border-CCTV domain and is heavily BSF/CIBMS-weighted. This document is
the SSB-specific layer, and [§16](#16-what-in-domain-researchmd-is-bsf-specific-not-ssb)
explicitly marks which of its findings must **not** be carried over to SSB.

---

## How to read this document

Per [CLAUDE.md](../../../CLAUDE.md) §3.7:

| Label | Meaning |
|---|---|
| **FACT** | Verifiable and sourced. The source is cited as `[Nn]`. |
| **ASSUMPTION** | Believed true but not verified against a source. |
| **UNKNOWN** | Identified gap. Nobody on this project knows this yet. |

A statement labelled **FACT** is a fact *about what the cited source says*. Where
a source is a news outlet, a secondary compilation, or a foreign academic study
rather than an Indian primary government document, this is noted inline.

### Source retrieval notes for this pass

Unlike the earlier domain pass, **primary MHA sources were retrieved directly**
in this pass: the MHA Annual Reports 2023-24 `[N1]` and 2022-23 `[N2]`, and two
Lok Sabha Unstarred Question replies of 3 February 2026 `[N3][N4]`. Statements
sourced to these are the highest-confidence facts in this document.

Still **not** retrieved directly (marked **[indirect]** at point of use):
the text of the Sashastra Seema Bal Act, 2007 `[N5]` (both `indiacode.nic.in`
and the MHA-hosted PDF returned HTTP 403); the official SSB website
(`ssb.nic.in` does not resolve; `ssb.gov.in` served no navigable content to the
fetcher); and one Deccan Herald report on the SSB intelligence wing `[N19]`
(HTTP 403).

### Attribution caveat — read this first

**UNKNOWN / process gap** — [problem.md](../../00-project/problem.md) records the
problem statement text verbatim but does **not** record the SIH
organisation/department field. This document proceeds on the project owner's
statement that **SSB is the department named for PS 26187**. The problem
statement text itself says only "border security forces" generically. Nothing in
this document should be read as evidence that the problem statement is
SSB-specific; the *problem statement* is force-agnostic, and it is the
*department attribution* that makes SSB the operative user. Recording the
organisation field in `docs/00-project/` would close this gap without altering
the immutable statement text.

---

## 1. Who SSB is and what it is mandated to do

### 1.1 Identity and status

**FACT** — SSB is one of five **Central Armed Police Forces (CAPFs)** under the
Ministry of Home Affairs (BSF, CISF, CRPF, ITBP, SSB), of which **AR, BSF, ITBP
and SSB are the "Border Guarding Forces"**. `[N2]`

**FACT** — SSB's origin is the Special Service Bureau, raised after the 1962
conflict, with a mandate framed around the **morale and capability of the border
population against threats of subversion, infiltration and sabotage from across
the border**. It became a Border Guarding Force in **2001** under MHA and was
rechristened *Sashastra Seema Bal* **with an amended charter of duties**. `[N1][N2]`

**FACT** — SSB was declared a **Border Guarding Force and Lead Intelligence
Agency (LIA) for the Indo-Nepal border in January 2001**, and was assigned the
Indo-Bhutan border in **March 2004**. `[N6]` *(encyclopedic secondary source;
the LIA designation is repeated across secondary compilations `[N23]` but was
not found stated in the MHA Annual Reports retrieved here)*

**FACT** — Force strength: **92,541** as on 31.03.2024 `[N1]`; **90,194** as on
31.12.2022 `[N2]`. *(A tertiary source gives 94,261 `[N6]`; treat the MHA figures
as authoritative.)*

### 1.2 Charter of duties

**FACT** — SSB's statutory/rule-based charter, as summarised from the **SSB Act,
2007** and **SSB Rules, 2009**, is to: secure designated border areas; foster a
sense of security among border communities; prevent trans-border crime,
smuggling and other illegal activities; regulate unauthorised entry into or exit
from Indian territory; conduct **civic action programmes** in its area of
responsibility; and perform additional duties assigned by the Central
Government. `[N8]` **[indirect for the Act text — see N5]**

**FACT** — SSB additionally performs **Internal Security and Counter-Insurgency
duties**, and is deployed in J&K, Assam, and the LWE-affected areas of
Chhattisgarh, Jharkhand and Bihar. `[N1][N2]`

**FACT** — An SSB officer interviewed for a 2025 Tribhuvan University study
described the core function as *"border surveillance, intelligence gathering,
curbing smuggling, counter-insurgency operations, and ensuring law enforcement
along the border."* `[N8]` *(Nepali master's thesis; key-informant interview —
treat as indicative of role framing, not as doctrine)*

**ASSUMPTION** — **Intelligence collection, not interdiction alone, is a
first-class SSB output.** The LIA designation, the dedicated intelligence wing
`[N19]`, the Border Interaction Teams and the "Know Your Area" programme
`[N8]` all point the same way: SSB is expected to *know* its border population
and its routes, not only to catch people crossing it. *(Basis: convergence of
`[N6][N8][N19]`. No primary source states a doctrinal priority ordering.)*

**Why this matters for video analytics:** an intelligence-led force values
*pattern over time* (who uses this track, how often, with what vehicles) at
least as much as *alarm in the moment*. This is a materially different demand on
a video platform than pure intrusion alarming.

---

## 2. The borders SSB guards — and why they are categorically different

### 2.1 The two borders

**FACT** — SSB is deployed on the **Indo-Nepal border, 1,751 km**, and the
**Indo-Bhutan border, 699 km** — 2,450 km in total. `[N1][N2]`

**FACT** — The Indo-Nepal border passes through **Uttarakhand, Uttar Pradesh,
Bihar, West Bengal and Sikkim** `[N1]`; state-wise lengths reported as
Uttarakhand 263.7 km, Uttar Pradesh 599.3 km, Bihar 800.4 km, West Bengal
105.6 km, Sikkim 99 km `[N6]` *(tertiary)*.

**FACT** — The Indo-Bhutan border passes through **Assam, West Bengal,
Arunachal Pradesh and Sikkim** `[N1]`; reported as Sikkim 32 km, West Bengal
183 km, Assam 267 km, Arunachal Pradesh 217 km `[N6]` *(tertiary)*.

**FACT** — Deployment follows the MHA principle of **"One Border, One Border
Guarding Force" (OBOBGF)**; under it, "Nepal and Bhutan Borders — Sashastra
Seema Bal (SSB)". `[N2]`

### 2.2 The open border — the single most important SSB-specific fact

**FACT** — MHA's own statement of the problem on **both** borders is identical
and is *not* about intrusion detection: *"The main challenges along this border
are to check misuse of **open border** by terrorists and criminals for illegal
and anti-national activities."* `[N1]` (§3.26 for Nepal, §3.28 for Bhutan)

**FACT** — The **India–Nepal Treaty of Peace and Friendship, 31 July 1950**
grants citizens of each country, on a reciprocal basis, the same privileges as
to residence, property, trade and commerce, and **movement** in the other's
territory — i.e. **no passport or visa is required to cross**, and tens of
thousands cross daily. `[N7][N13]`

**FACT** — The India–Nepal border is **unfenced**, with numerous official and
unofficial crossing points in addition to designated checkposts. `[N7]`

**FACT** — Freedom of movement between India and Bhutan has existed since the
**Treaty of Friendship of 8 August 1949** (revised 2007); the border is largely
unfenced and open, with no formal immigration check at most points for citizens
holding valid identification. From **23 September 2022**, Bhutan restricted
Indian nationals' permit-free movement to the border towns of Phuentsholing,
Gelephu and Samdrup Jongkhar, with a permit obtainable on arrival beyond them.
`[N14]` *(tertiary; the 2022 restriction is a Bhutanese measure, not an Indian
border-control change)*

**FACT** — The Union Home Minister, at SSB's 61st Raising Day on **20 December
2024**, stated that *"protecting fenced borders is much easier than protecting
an open border."* `[N12]` *(state broadcaster report)*

**FACT** — Nepal's counterpart force, the **Armed Police Force (APF), Nepal**,
polices the other side under the APF Act, 2001, and the two forces conduct
**joint patrols** on the demarcation line. `[N7][N8]`

### 2.3 The operational consequence

**ASSUMPTION** — On the SSB border, **"a person crossing the line" is not
itself an offence and therefore not an incident.** What makes an event
reportable is *who* (a third-country national, a known trafficker, a minor
being moved), *what they carry* (contraband, currency, gold, narcotics, wildlife,
timber), or *when and where* (a closed crossing, an off-route track at night) —
not the crossing itself. *(Basis: the treaty right of movement `[N7][N13]`
combined with MHA's framing of the challenge as "misuse of open border" `[N1]`
and the composition of SSB's own seizure/arrest table, which is almost entirely
contraband-, currency- and person-category based rather than intrusion-count
based `[N1]` — see [§12](#12-ssb-specific-event-classes).)*

**This inverts the core assumption of virtual-fence intrusion detection.** A
line-crossing alarm that is correct 100% of the time would still be almost
entirely noise here. Recorded as a domain finding, **not** a product decision.

**FACT** — A distinct SSB event category exists precisely for this reason:
**"Third Country (Foreigner)"** — 44 cases, 58 persons arrested between
01.01.2023 and 31.03.2024. `[N1]` The open border applies to Indian and Nepali
(and Bhutanese) nationals; third-country nationals using it are an offence
class in their own right.

**UNKNOWN** — Whether SSB maintains, or is permitted to maintain, any
record of *routine* legitimate crossings by Indian/Nepali nationals — and
therefore whether a video platform generating a person-detection record for
every such crossing is even lawful, let alone useful. See
[§11](#11-ssb-specific-legal-and-evidentiary-considerations).

---

## 3. SSB organisational structure and echelons

### 3.1 Formations (primary source)

**FACT** — SSB's formations as recorded by MHA: `[N1][N2]`

| Formation | Count |
|---|---|
| Force Headquarters (FHQ) | 1 |
| Frontiers (FTR HQ) | 6 |
| Sectors (Sector HQ) | 18 |
| Battalions | 73 |
| Recruit Training Centres (RTC) | 4 |
| Central Training Centres | 2 |
| SSB Academy | 1 |
| Wireless & Telecom Training Centre | 1 |
| Dog Training & Breeding Centre | 1 |
| Composite Hospitals | 3 |
| Central Store Depot & Workshop (CSD&W) | 1 |
| Sub-CSDs | 3 |
| Medical Training Centre | 1 |
| Counter Insurgency & Jungle Warfare School | 1 |
| "G" School | 1 |

**FACT** — Of the 73 battalions, **55 are operational and 18 are reserve**.
`[N8]` *(thesis, sourced to SSB FHQ 2025 — not confirmed in `[N1]`)*

**FACT** — A **12-battalion expansion** for the Nepal and Bhutan borders and
the tri-junction area has been sanctioned. `[N15]` *(news)*

### 3.2 Command chain and rank at each echelon

**FACT** — The SSB command chain, with the commanding rank at each level: `[N8]`

| Formation | Commander |
|---|---|
| Force Headquarters (New Delhi) | Director General (DG) |
| Frontier HQ | Inspector General (IG) |
| Sector HQ | Deputy Inspector General (DIG) |
| Battalion | Commandant |
| Company | Assistant Commandant |
| **Border Out Post (BOP)** | **Sub-Inspector (SI)** |
| **Check post** | **Head Constable** |

*(Source: thesis, attributed to SSB Force HQ 2025 and corroborated for the upper
echelons by `[N6]`. Note the thesis text is internally inconsistent once,
naming "Deputy Commandant" for Company in a table and "Assistant Commandant" in
the surrounding prose; `[N6]` gives Assistant Commandant.)*

**FACT** — Nominal composition: each sector comprises **5–6 battalions**;
**2–4 sectors** form a Frontier; a battalion has **7 companies**; each company
has **3 BOPs**. `[N6]` *(tertiary; battalion strength given variously as 1,000
`[N6]` and 1,172 `[N23]`)*

**FACT** — A senior-SSB-officer interview identifies BOP- and Company-level
**decision latency** as a live problem: the layered command structure *"can
occasionally result in delays in decision-making, particularly in situations
demanding rapid responses at the BOP and COY levels,"* with more autonomy at
lower levels named as the remedy. `[N8]`

**The lowest two echelons are the ones nearest the camera, and they are led by
an SI and a Head Constable respectively.** Any interface, alert or evidentiary
procedure that assumes a technically trained officer at the point of capture is
assuming something this structure does not supply.

**UNKNOWN** — Whether Frontier or Sector HQ has any operations/monitoring
facility distinct from a battalion-level one, and which echelon would host a
video analytics deployment.

---

## 4. BOPs, check posts and other physical nodes

### 4.1 Counts (primary source)

**FACT** — **539 Border Out Posts** established along the India-Nepal border and
**195 BOPs** along the India-Bhutan border — **734 total**, unchanged between the
2022-23 and 2023-24 Annual Reports. `[N1][N2]`

**FACT** — SSB **operationalised 72 new posts** along the Indo-Nepal and
Indo-Bhutan borders, of which 18 in Sikkim and Arunachal Pradesh. `[N16]`
*(news, post-Doklam period)*

**Conflicting figures — do not treat any of these as settled:**

| Figure | Source | Confidence |
|---|---|---|
| 539 (Nepal) + 195 (Bhutan) = 734 BOPs | MHA Annual Reports `[N1][N2]` | **High — primary** |
| 734 total BOPs, 426 with road connectivity | The Tribune, 17 Aug 2025 `[N9]` | Medium — news, but matches `[N1]` total exactly |
| 474 (Nepal) + 131 (Bhutan) = 605 BOPs | secondary compilations `[N23]` | Low |
| 295 BOPs on the Nepal border within 528 total SSB "units" | thesis, from Nepali-side data `[N8]` | Low for BOP count; the thesis counts differently (units incl. HQs) and may cover only specific provinces |

**ASSUMPTION** — The 539/195 split from `[N1]` is the figure to work from, and
the lower third-party counts reflect either older data or a narrower definition
of "BOP". *(Basis: `[N1]` is primary and internally consistent with `[N2]` and
with `[N9]`'s total.)*

### 4.2 BOP spacing and density

**FACT** — Average distance between SSB BOPs on the Nepal border is reported as
**3.9 km**, against 7.7 km for Nepal's APF. `[N8]` An earlier academic account
puts SSB armed posts *"approximately three kilometres apart"* against APF posts
fifteen to twenty km apart. `[N8]` *(Baral & Pyakurel 2013, cited in the thesis)*

**FACT** — The same study describes SSB's model as a **"high-intensity security
model … continuous surveillance and rapid response"** with roughly **45,000
personnel and 528 units** on the Nepal border. `[N8]` *(Nepali thesis; the
45,000 figure is not corroborated by an Indian primary source and should be
treated as approximate)*

**ASSUMPTION** — At ~3.9 km spacing over 1,751 km, SSB's density is high enough
that **most of the border is watched by a person from a post rather than by a
sensor between posts.** This is the opposite of the CIBMS "electronic domination
of a gap" model. *(Basis: arithmetic on `[N1]`'s 539 BOPs / 1,751 km ≈ 3.25 km
per BOP, consistent with `[N8]`. Not a sourced doctrinal statement.)*

### 4.3 Check posts, ICPs and other nodes

**FACT** — SSB establishes **border outposts, observation posts, check posts and
joint check posts**, and mans **naka** checkpoints. `[N23]` *(secondary
compilations; the check-post echelon with a Head Constable in command is
corroborated by `[N8]`)*

**FACT** — Two **Integrated Check Posts (ICPs)** are operational on the
India-Nepal border: **Raxaul** (Bihar, operationalised 03.06.2016) and
**Jogbani** (Bihar, 15.11.2016). `[N2]` **Rupaidiha** (UP) and **Sunauli** (UP)
are under development; **Banbasa** (Uttarakhand) is at land-acquisition stage.
`[N2]`

**FACT** — ICP amenities as listed by MHA include an electronic weighbridge,
inspection shed and **CCTV**. `[N2]` ICPs are operated by the **Land Ports
Authority of India (LPAI)**, not by the border force. `[N21]`

**FACT** — The four major India-Nepal ICPs (Jogbani, Raxaul, Sonauli,
Rupaidiha) were first proposed in October 2003 after an NSCS assessment that
infrastructure at these locations was *"abysmal."* `[N21]`

**UNKNOWN** — **Who owns and operates the CCTV at an India-Nepal ICP** — LPAI,
Customs, Immigration, or SSB — and whether SSB has access to those feeds. The
earlier domain pass recorded that ICP observation towers are *"manned by BSF
personnel"* `[S6][S7]`; those surveys covered the India-Bangladesh border, and
that staffing cannot be assumed at Raxaul or Jogbani. See
[§16](#16-what-in-domain-researchmd-is-bsf-specific-not-ssb).

**FACT** — A **laser fence** venture was proposed by SSB at the **Sonauli check
post (UP)**, with possible extension. `[N23]` *(secondary compilation; not
found in any primary source retrieved here — low confidence, but the only
electronic-barrier proposal specific to the SSB border found in this pass)*

**UNKNOWN** — The number of SSB check posts and naka points, and how many of
them have any camera at all.

---

## 5. Typical surveillance responsibilities

### 5.1 What SSB is actually watching for

**FACT** — SSB's charter requires it to prevent trans-border crime, smuggling
and illegal activity, and to **regulate unauthorised entry into or exit from
Indian territory**. `[N8]` **[indirect for the Act]**

**FACT** — MHA frames the surveillance object on both SSB borders as **"misuse
of open border by terrorists and criminals."** `[N1]`

**FACT** — SSB is empowered under the **NDPS Act, 1985** to carry out search,
seizure and arrest for illicit narcotics trafficking at the international
border — named alongside BSF and Assam Rifles in MHA's list of drug-control
measures. `[N4]`

**FACT** — SSB and the **Narcotics Control Bureau** have agreed to strengthen
anti-drug-trafficking coordination on the Indo-Nepal border, focusing on
intelligence sharing, joint operations and capacity building. `[N20]`
*(state broadcaster)*

### 5.2 How surveillance is actually performed

**FACT** — SSB's surveillance repertoire, as described across sources, is
**patrol- and post-based**: a layered grid of BOPs, **area domination patrols**,
manned naka/check posts, joint patrols with APF Nepal, and observation posts.
`[N8][N23]`

**FACT** — Joint patrols with APF Nepal rose from **78 in FY 071/72 to 5,841 in
FY 080/81** (Nepali fiscal years; roughly 2014-15 to 2023-24). `[N8]`
*(APF Nepal HQ Border Security Department data via the thesis)*

**FACT** — SSB fields **Border Interaction Teams (BITs)** on **25 high-risk
smuggling routes**; each BIT has six members including female personnel and
operates **in civilian attire**, gathering intelligence and engaging local
communities. `[N8]`

**FACT** — SSB operates **five Anti-Human Trafficking Units (AHTUs)** in
vulnerable border regions, working with state agencies and NGOs. `[N8]`
Nationally, **788 AHTUs** are operational **including 20 established by
SSB/BSF** under the Nirbhaya Fund. `[N2]`

**FACT** — SSB fields **Small Action Teams (SATs)** of at least platoon strength
for LWE-affected regions, and **18 Rescue & Relief Teams** of 35 personnel each
for disaster response. `[N8]`

**FACT** — **Female personnel are deployed at border check posts** for frisking
and checks of female travellers, and to engage local women. `[N8]`

**FACT** — The **"Know Your Area" (KYA)** programme requires personnel to build
in-depth knowledge of local geography, culture and security risks in their
assigned stretch. `[N8]`

**ASSUMPTION** — **Human presence, not electronic sensing, is SSB's primary
surveillance instrument today.** Every mechanism named above is a person: a
patrol, a naka, an undercover team, a female frisker, an officer who knows the
area. Cameras appear in the sources as procurement line-items, never as the
described method. *(Basis: absence of any surveillance-by-camera description in
`[N1][N2][N8]`; this is an argument from silence and must be validated.)*

---

## 6. CCTV and video surveillance already in service

### 6.1 What SSB has procured (primary source)

**FACT** — In answer to Lok Sabha Unstarred Question No. 488 on **3 February
2026**, the Minister of State for Home Affairs stated that SSB *"has procured
the Unmanned Aerial Vehicles, Micro Unmanned Aerial Vehicles, Hand Held Thermal
Imager, **CCTV Surveillance Setup with Automatic Face Recognition System with
Auto Number Plate Recognition** and Satellite phones for surveillance and
modernization of the Force."* `[N3]`

**This is the single most consequential finding in this document for IBVAP, and
it cuts against the problem statement's premise.** The problem statement's
stated gap is that FRS and ANPR *"often require specialized hardware and
proprietary solutions"* and are therefore not deployed. The named department has
already procured a CCTV setup **with** FRS and ANPR. Recorded as a research
finding; the product implication belongs in `docs/02-product/`.

**FACT** — Modernisation funding: SSB was allotted **₹5,001.63 crore** for
modernisation and infrastructure development over 2015-16 to 2025-26, of which
**₹4,775.11 crore** had been spent as of the reply date. Separately, under
**Modernization Plan-II, III and IV** from 2013 to 31.03.2026, SSB was allotted
**₹241.15 crore** and spent **₹210.02 crore**. `[N3]`

**FACT** — MHA gave **no completion timeline**: *"Modernization of forces and
procurement of the latest and State of the art equipment is an ongoing process.
So specific timeline can not be given."* `[N3]`

**FACT** — CAPF-wide Modernization Plan IV procurement includes **UAVs**,
**Hand Held Thermal Imagers** and **satellite phones** — but **no video
analytics, VMS or CCTV item** appears in MHA's list of major equipment for the
plan. `[N1]`

**FACT** — SSB has sent personnel for **Drone Pilot Training** at a DGCA-approved
institute, and for **Special Communication Equipment Training at BSF**. `[N3]`

### 6.2 Other reported technology in SSB service

**FACT** — A 2025 study reports SSB using **XBIS scanners, "Netra" surveillance
drones, body-worn cameras, GPS devices, CCTV cameras and satellite phones**,
with CCTV and satellite phones specifically credited for *"real-time monitoring
and communication in remote areas."* `[N8]` *(Nepali thesis, key-informant
sourced — the specific product names are uncorroborated)*

**FACT** — Secondary compilations describe SSB as using **drones, CCTV
surveillance systems, thermal imagers, night-vision devices, GPS-based
patrolling, secure digital communication and GIS-based planning**, and state that
CCTV cameras and thermal imaging devices at strategic locations have improved
day-and-night monitoring. `[N10][N11][N23]` *(news and compilation sources
paraphrasing the same MHA replies — treat as restating `[N3]`, not as
independent evidence)*

**FACT** — SSB has an **intelligence wing with ~650 field and staff agents** for
actionable intelligence collection on both borders. `[N19]` **[indirect: HTTP 403]**

### 6.3 What is not established

**UNKNOWN** — **The installed CCTV base.** No source retrieved states how many
cameras SSB operates, where they are (BOP / check post / ICP / battalion HQ),
make and model, resolution, codec, PTZ vs fixed, thermal vs visible, ONVIF
conformance, or what recorder/VMS sits in front of them. This is the top
blocking gap.

**UNKNOWN** — **Where the procured FRS/ANPR CCTV setup is actually deployed**,
how many sites, whose software it is, whether it is a single vendor stack, and
whether it exposes any API or open stream. `[N3]` names the capability but not
the deployment.

**UNKNOWN** — Whether cameras exist at *ordinary* BOPs at all, or only at check
posts, ICPs and "key crossing points". `[N11]` says face recognition is at "key
crossing points" but is a news paraphrase.

**UNKNOWN** — Whether SSB body-worn camera footage `[N8]` is retained centrally
and would be in scope for the same analytics and evidence workflow as fixed CCTV.

---

## 7. Control rooms and monitoring workflow

**FACT** — MHA lists, among measures for detecting cross-border trafficking:
*"The installation of upgraded Surveillance grid using **AI based features**,
RADARS, Electro Optics Devices, Night Vision Devices, Motion Detectors with
**Integrated Command and Control Centre**."* `[N4]`

**Important caveat:** `[N4]` is a national narcotics-control answer covering
international borders and coastal areas generally. It is **not attributed to SSB
or to the Indo-Nepal/Indo-Bhutan borders**, and appears in the same list as
maritime and Coast Guard measures. It is the only primary-source mention of an
"Integrated Command and Control Centre" and AI-based surveillance found in this
pass, and it cannot be assigned to SSB.

**FACT** — SSB has an **SSB Wireless & Telecom Training Centre** as a standing
formation `[N1][N2]`, indicating an in-house communications cadre.

**UNKNOWN — and this is a critical gap** — **Whether SSB operates control rooms
that display live video at all.** No source retrieved in this pass describes an
SSB control room, operations room, video wall, or monitoring roster. Contrast
this with BSF, where "BSF Control Rooms on the border" receiving BOLD-QIT feeds
and cueing QRTs is documented (see [domain-research.md](domain-research.md)
§2.1). **There is no SSB equivalent in evidence.**

**UNKNOWN** — If SSB monitoring exists: at what echelon (BOP / Company /
Battalion / Sector / Frontier / FHQ), how many operators, how many cameras per
operator, shift pattern, and what they are instructed to do on seeing something.

**UNKNOWN** — Whether any live video reaches echelons above the BOP today, or
whether recording is purely local and consulted only after the fact.

**ASSUMPTION** — Monitoring, where it exists, is **local and incidental** — a
screen at a post watched by whoever is on duty — rather than a staffed control
room with a monitoring roster. *(Basis: absence of any control-room description
in `[N1][N2][N8]`, combined with the check-post/BOP command ranks in
[§3.2](#32-command-chain-and-rank-at-each-echelon) and the road/power
constraints in [§10](#10-remote-location-constraints). This is inference from
silence and is the highest-value assumption in this document to validate.)*

---

## 8. Incident detection → assessment → response

### 8.1 What is established

**FACT** — SSB's own digitised incident pathway exists for **seizures**: the
**Seizure Incident Management System (SIMS)** maintains real-time digital
records of seizures and law-enforcement actions, lets field units **log
incidents instantly**, and gives senior officials insight into smuggling
patterns via a **centralised database**. `[N8]` *(thesis, key-informant
sourced — not corroborated by an Indian primary source in this pass)*

**FACT** — Coordination with the Nepali counterpart force is **scheduled, not
event-driven**, at every echelon: `[N8]`

| Level | Frequency |
|---|---|
| DG/IG | Annually (moved to semi-annually after the 8th meeting) |
| DIG | Quarterly |
| Battalion | Monthly |
| Company / BOP | Fortnightly |

**FACT** — Cross-border coordination meetings totalled **981** over six fiscal
years, with the highest volume at **battalion level (448)** and **local level
(248)**. `[N8]` *(APF Nepal HQ data)*

**FACT** — Real-time coordination between the two forces is explicitly
inadequate: an SSB officer stated *"there are still gaps in real-time
information exchange that hinder proactive security responses."* `[N8]`

**FACT** — SSB's operational output is recorded by MHA as **cases** and
**persons arrested** per category (see [§12](#12-ssb-specific-event-classes)) —
a case/arrest ledger, not an alarm log. `[N1]`

### 8.2 What is not established

**UNKNOWN** — The actual detection → assessment → response sequence at an SSB
BOP. No source retrieved describes it. The BSF pattern recorded in
[domain-research.md](domain-research.md) §3.2 (sensor → control room → QRT
interception) is **BOLD-QIT-specific and must not be assumed for SSB** —
see [§16](#16-what-in-domain-researchmd-is-bsf-specific-not-ssb).

**UNKNOWN** — Whether SSB has a **Quick Reaction Team** construct at all, or
whether response is by the patrol/naka already in the field.

**UNKNOWN** — What carries an alert from whoever notices it to whoever responds
(radio net, mobile phone, runner), and whether any written SOP or Standing Order
governs alarm assessment and escalation.

**UNKNOWN** — Response-time expectations from detection to interception.

**UNKNOWN** — Whether SIMS is fed by hand after the fact, or is capable of
ingesting a machine-generated event; and whether it is reachable from a BOP.

**ASSUMPTION** — Because SIMS is a **seizure** system, it records *outcomes*,
not *detections*. A camera-derived event that produces no seizure has no
existing home. *(Basis: the description in `[N8]` is entirely
seizure/enforcement-action framed.)*

---

## 9. Command and control integration

**FACT** — SSB operates under MHA administrative control; MHA formulates policy,
oversees deployment, ensures coordination with other agencies, and issues
periodic guidelines for border management, intelligence gathering and disaster
response. `[N8]`

**FACT** — Named digital systems in SSB's orbit, from the sources retrieved:

| System | What it is | Source | Confidence |
|---|---|---|---|
| **SIMS** — Seizure Incident Management System | SSB's own real-time digital seizure/incident register with a centralised database | `[N8]` | Medium — single foreign academic source |
| **CCTV setup with FRS + ANPR** | Procured surveillance stack; scope and vendor unknown | `[N3]` | **High — primary**, but deployment unknown |
| "Integrated Command and Control Centre" | Named in a national narcotics answer, **not attributed to SSB** | `[N4]` | High for existence of the statement; **unattributable to SSB** |
| **EVR** — Online Electronic Vigilance Register | MHA-wide system for IPS officer vigilance profiles — **unrelated to border surveillance** | `[N2]` | High — and irrelevant; noted only to prevent misidentification |

**UNKNOWN — blocking** — **What "existing command and control systems" means for
SSB.** The problem statement requires integration with them. No source retrieved
names an SSB C2 system, its vendor, protocol, data model, or network reach.
SIMS `[N8]` is the only credible candidate found, and it is a seizure register
rather than a C2 system.

**UNKNOWN** — Which non-SSB stakeholders would consume SSB video: state police
(who take over cases), Customs, Immigration, LPAI (at ICPs), NCB (narcotics),
intelligence agencies, and APF Nepal (joint patrols). Each is a different
integration question with a different legal basis.

**ASSUMPTION** — Any C2 integration on the SSB border must survive the
**cross-organisational handover**, because SSB's cases are prosecuted by state
police, its narcotics work is coordinated with NCB, and its border counterpart
is a foreign force. Integration is therefore as much an interoperability and
authorisation problem as a technical one. *(Basis: `[N4]` for NCB, `[N8]` for
APF coordination, [§11](#11-ssb-specific-legal-and-evidentiary-considerations)
for police handover.)*

---

## 10. Remote-location constraints

### 10.1 Road access — the defining constraint

**FACT** — **308 of SSB's 734 BOPs on the Indo-Nepal and Indo-Bhutan borders
lack proper road connectivity**; only **426** have it. A consolidated proposal
for lateral and axial roads, foot-tracks and staging camps is **still under
consideration at MHA**, with "large financial implications" and an uncertain
approval timeline. `[N9]` *(The Tribune, Animesh Singh, 17 August 2025)*

**FACT** — Government has approved construction/upgradation of **1,299.80 km of
roads** along the India-Nepal border in Uttarakhand, Uttar Pradesh and Bihar.
`[N1][N2]` *(Approved — not stated as complete.)*

**42% of SSB's border out posts cannot be reached by road.** Any hardware placed
at those sites is carried in on foot, and so is every spare part and every
technician visit.

### 10.2 Power

**FACT** — **Generators have been provided at all BOPs wherever there is no
direct electricity connection**, and reverse-osmosis plants installed at all
BOPs for drinking water; the situation **varies state to state**. `[N9][N18]`

**FACT** — A parliamentary committee noted a **lack of electricity at several
BOPs, particularly those of SSB and ITBP**. `[N18]` *(PRS summary of a
Parliamentary Standing Committee report on working conditions in border guarding
forces)*

**ASSUMPTION** — At a generator-powered BOP, electrical power is **scheduled and
fuel-limited**, not continuous, and the fuel has to travel the same
unroaded path as everything else. A continuously running compute load is
therefore a logistics cost, not just an electrical one. *(Basis: combining
`[N9]`'s road finding with `[N9][N18]`'s generator finding. No measured power
budget for an SSB BOP was found.)*

### 10.3 Connectivity

**FACT** — **Satellite phones** are part of SSB's procured surveillance and
communication inventory `[N3]`, and CCTV plus satellite phones are credited with
enabling *"real-time monitoring and communication in remote areas"* `[N8]`.

**ASSUMPTION** — The presence of satellite phones in the *surveillance and
modernisation* inventory implies that **at some SSB posts, satellite is the
communications path** — which is high-latency, low-bandwidth and metered.
*(Basis: `[N3]`. The reply does not say which posts or how many.)*

**UNKNOWN** — Actual data connectivity at an SSB BOP: whether there is any IP
link at all, its bandwidth, symmetry, metering, reliability and whether it is
shared with voice.

**UNKNOWN** — Whether SSB has any dedicated communication backbone comparable to
the CIBMS OFC/microwave network. **No CIBMS-equivalent network is documented for
the Indo-Nepal or Indo-Bhutan border.** See
[§16](#16-what-in-domain-researchmd-is-bsf-specific-not-ssb).

### 10.4 Terrain and environment

**FACT** — The SSB border spans **Himalayan territories and the Indo-Gangetic
Plain** `[N7]`; the Indo-Bhutan stretch traverses **rugged Himalayan terrain and
foothills** `[N14]`; the frontiers are described as unfenced and crossing
**forests, mountains, rivers and plateaus** `[N23]`.

**FACT** — Reserved forests spanning India into Bhutan are central to conflict,
conservation and displacement processes on that border. `[N14]`

**UNKNOWN** — Measured environmental conditions per sector on the SSB borders:
fog days, monsoon intensity, temperature range at camera housings, humidity,
lightning. The earlier domain pass's environmental findings are drawn from
Punjab/Jammu/Assam CIBMS areas, not from the Himalayan foothills or the Bihar
Terai.

### 10.5 Maintenance and skills

**FACT** — SSB conducts training when new equipment is adopted, and has sent
personnel for drone-pilot and BSF special-communication training. `[N3]`

**UNKNOWN** — Whether SSB has any in-house cadre able to install, configure and
repair IP camera and analytics infrastructure at a BOP, or whether this depends
on vendors who must reach an unroaded post.

**ASSUMPTION** — Software placed at an SSB BOP must run unattended for long
periods and must fail in a way a Sub-Inspector can recognise and report over a
radio or satellite phone. *(Basis:
[§3.2](#32-command-chain-and-rank-at-each-echelon) command ranks + `[N9]` road
access + `[N18]` electricity findings.)*

---

## 11. SSB-specific legal and evidentiary considerations

### 11.1 The statutory basis is the SSB Act, not the BSF Act

**FACT** — SSB is constituted under the **Sashastra Seema Bal Act, 2007 (Act No.
53 of 2007)**, enacted **20 December 2007**, described as an Act to provide for
the constitution and regulation of an armed force of the Union for ensuring the
security of the borders of India. Its chapters cover the constitution of the
Force and conditions of service, offences, punishment, arrest and proceedings
before trial, **Force Courts** and their procedure, confirmation and revision of
proceedings, execution of sentences, and pardons and remissions. `[N5]`
**[indirect — statute text not retrieved]**

**FACT** — **SSB Rules, 2009** elaborate the structure and functions: Rule 9
mandates securing border areas, preventing trans-border crime and illegal
activity, regulating unauthorised crossings, and building trust with local
communities through civic action; Rule 10 establishes the hierarchical command
structure. `[N8]` **[indirect]**

**The BSF Act, 1968 does not govern SSB.** Every legal statement in
[domain-research.md](domain-research.md) §3.5 that rests on the BSF Act or on
BSF jurisdiction notifications must be re-derived for SSB.

### 11.2 Jurisdictional belt — 15 km, not 50 km

**FACT** — SSB's powers of arrest, search and seizure operate **within 15 km of
the international border** in **Uttarakhand, Uttar Pradesh, Bihar, West Bengal,
Sikkim, Assam and Arunachal Pradesh**, and in any other area where SSB operates.
`[N8][N17]` *(thesis citing the SSB Act 2007; corroborated by news reporting of
the enabling notification)*

**This is not the BSF belt.** The 50 km (Assam, Punjab, West Bengal) and 80 km
(Gujarat) figures recorded in [domain-research.md](domain-research.md) §3.5 come
from a **2021 BSF-specific notification** and have no application to SSB.

**UNKNOWN** — Whether the 15 km figure has been revised since; and whether it is
measured as straight-line distance or along roads (relevant if a camera site
near the limit is used to justify an action).

### 11.3 Powers under other statutes

**FACT** — SSB has been conferred powers under the **Criminal Procedure Code,
1973** (arrest without warrant, search, seizure of offensive weapons, prevention
of cognizable offences), the **NDPS Act, 1985** (entry, search, seizure and
arrest without warrant in narcotics offences), the **Arms Act, 1959** (demand
arms licences, search vessels and vehicles, seize prohibited arms in disturbed
areas), and the **Passport Act, 1967**. Extension under the **Customs Act, 1962**
is variously reported as conferred and as under consideration. `[N8][N17]`

**FACT** — MHA confirms, as a primary source, that **SSB (with BSF and Assam
Rifles) is empowered under the NDPS Act, 1985 to carry out search, seizure and
arrest for illicit narcotics trafficking at the international border.** `[N4]`

**FACT** — The **Bharatiya Nagarik Suraksha Sanhita, 2023** replaced the CrPC,
1973 with effect from **1 July 2024**. Sources describing SSB's powers cite the
CrPC 1973 and pre-date or ignore this. **UNKNOWN** — how SSB's CrPC-derived
powers map onto the BNSS, and whether any fresh notification was required.

### 11.4 Handover and prosecution

**FACT** — In practice, apprehended persons and seized items are **handed to the
local police station for further legal action**, e.g. under the NDPS Act. `[N17]`
*(news; the practice is corroborated across incident reporting)*

**FACT** — SSB's operational ledger is reported by MHA as **"Cases" and
"Arrested"** per category `[N1]` — consistent with SSB originating cases that
are then carried by another agency.

**UNKNOWN** — Whether SSB registers FIRs or files complaints/charge sheets in
its own name in any category, and whether the answer differs for NDPS (where the
force is a designated empowered agency) versus ordinary offences. The generic
CAPF position — that border guarding forces detect and hand over rather than
investigate — is documented for BSF `[S22]` but **was not confirmed for SSB in
this pass**.

### 11.5 Evidentiary requirements for recorded video

**FACT** — Electronic records in India, including CCTV footage, are governed by
**Section 63 of the Bharatiya Sakshya Adhiniyam, 2023**, in force from
**1 July 2024**, replacing s.65B of the Indian Evidence Act, 1872. Admissibility
of a copy requires a certificate signed by the person in charge of the device
**and** an expert, disclosing the record's **hash value**. `[S29]` *(carried
forward from [domain-research.md](domain-research.md) §3.5 — this is
force-agnostic Indian law and **does** apply to SSB)*

**ASSUMPTION** — Section 63 lands harder on SSB than on BSF for two structural
reasons: (1) the device custodian at the point of capture is a **Sub-Inspector
at a BOP or a Head Constable at a check post**
([§3.2](#32-command-chain-and-rank-at-each-echelon)), and (2) **42% of BOPs have
no road access** ([§10.1](#101-road-access--the-defining-constraint)), so getting
either the custodian's signature or an expert's to a site is a journey. *(Basis:
combining `[S29]` with `[N1][N8][N9]`. Not sourced as an observed problem.)*

**UNKNOWN** — Current SSB practice for exporting and handing over footage:
format, who signs the certificate, who is the "expert", whether hashes are
computed at all, how long retrieval takes, and how often footage is actually
used in a prosecution.

**UNKNOWN** — Video retention periods mandated or practised at SSB BOPs, check
posts and ICPs.

### 11.6 Face recognition on a treaty-open border

**FACT** — SSB has procured a CCTV setup **with Automatic Face Recognition and
ANPR**. `[N3]`

**FACT** — The population crossing this border includes Indian and Nepali
nationals exercising a **treaty right of movement** `[N7][N13]`, and Indian and
Bhutanese nationals with freedom of movement under the 1949/2007 treaty `[N14]`.

**ASSUMPTION** — Applying face recognition at an open border therefore processes
biometrics of **people who are committing no offence and who have a treaty right
to be there**, including foreign nationals of a friendly state. This is a
materially different legal posture from face recognition at a controlled
crossing on a closed border. *(Basis: juxtaposing `[N3]` with `[N7][N13][N14]`.
No legal analysis of this specific situation was found.)*

**UNKNOWN — high priority** — The legal basis, authorisation level, retention
rules and oversight for biometric processing by SSB on the open border:
which authority approves it, under what instrument, what happens to a template
generated from a person who is never charged, and whether the Digital Personal
Data Protection Act, 2023 or any exemption under it applies.

**UNKNOWN** — Whether there is any bilateral understanding with Nepal or Bhutan
about surveilling their nationals at the open border, given the standing
coordination architecture in [§8.1](#81-what-is-established).

---

## 12. SSB-specific event classes

This is the closest thing to a ground-truth catalogue of *what actually happens*
on the SSB border: MHA's own record of SSB operational achievements.

**FACT** — SSB operational achievements, **01.01.2023 to 31.03.2024** `[N1]`
*(primary — MHA Annual Report 2023-24)*:

| # | Category | Cases | Arrested | Seizure |
|---|---|---|---|---|
| 1 | **Narcotics** | 1,059 | 573 | 29,007.8685 kg; plus 5,875.8843 acre illicit cannabis cultivation destroyed |
| 2 | **FICN** (fake Indian currency) | 11 | 20 | ₹3,83,500 |
| 3 | **Indian Currency** | 471 | 614 | ₹10,34,03,860 |
| 4 | **Other Currency** | 197 | 316 | ₹4,00,29,910 |
| 5 | **Prohibited / contraband items** | 5,993 | 6,209 | — |
| 6 | **Forest products** | 398 | 353 | 3,71,837.6086 cft; 23,916.993 kg |
| 7 | **Wildlife products** | 78 | 101 | — |
| 8 | **Cattle** | 432 | 293 | 5,895 nos. |
| 9 | **Gold** | 38 | 63 | 20.6436 kg |
| 10 | **Silver** | 33 | 43 | 62.3841 kg |
| 11 | **Antique idols** | 1 | — | 3 nos. |
| 12 | **Psychotropic / synthetic drugs** | 157 | 171 | 4,55,250 nos. |
| 13 | **Arms, country/factory made** | 101 | 122 | 218 nos. |
| 14 | **Ammunition / cartridge / explosive** | 108 | 108 | 3,237 nos. and 266.9761 kg |
| 15 | **Maoists / Maoist linkmen** | 55 | 59 | — |
| 16 | **Third Country (Foreigner)** | 44 | 58 | — |
| 17 | **Other criminals / anti-social elements** | 25 | 41 | — |
| 18 | **Peoples Liberation Front of India (PLFI)** | 1 | 1 | — |
| 19 | **Surrendered Maoists / linkmen** | 4 | 10 | — |
| 20 | **Neutralized militants / terrorists** | 1 | 2 | — |
| 21 | **Human Trafficking** | 316 | 274 (traffickers) | **531 victims rescued (248 male, 283 female)** |

> **Extraction caveat:** these values were extracted from the Annual Report PDF's
> multi-column layout. The **category names and their case/arrest pairs are
> read directly from the table rows**; a few of the free-text seizure-quantity
> cells span rows in the source layout and their row assignment is less certain
> (notably rows 5–8). Verify against the published PDF before citing a
> quantity figure. Category *names* and *case counts* are reliable.

**FACT** — The 2022-23 report gives the same category set for 01.04.2022 to
31.12.2022, with **5,281 arrests/apprehensions of criminals/smugglers/Naxals**,
3,987 cattle, ₹1,42,50,712 Indian currency, ₹1,01,32,021 other currency,
0.5503 kg gold, 40.634 kg silver, 49 wildlife, 18,554.307 kg narcotics, 39,445
nos. psychotropic/synthetic drugs, and forest products including 41,768.1620 kg
firewood and 34,822.6511 cft wooden logs. `[N2]` *(same layout caveat applies)*

### 12.1 What this catalogue says about the domain

**FACT — by absence** — There is **no "intrusion", "infiltration attempt",
"line crossing" or "illegal entry" category** in SSB's operational achievement
table. `[N1][N2]` Contrast BSF, for which "1,104 infiltration attempts detected"
is the headline metric (see [domain-research.md](domain-research.md) §5.1).

**ASSUMPTION** — SSB's operational reality is a **contraband, currency,
trafficking and person-of-interest problem**, not an intrusion-detection problem.
The three largest categories by case count are prohibited/contraband items
(5,993), narcotics (1,059) and Indian currency (471); human trafficking (316) is
fourth. *(Basis: direct reading of `[N1]`. The inference that this reflects
operational priority rather than reporting convention is an assumption.)*

**FACT** — **Human trafficking is a first-class SSB event class with a victim
outcome**, not just an arrest outcome: 531 victims rescued in 15 months. `[N1]`
SSB runs dedicated AHTUs for it. `[N8]` The Nepal border is described as a major
trafficking corridor. `[N23]`

**ASSUMPTION** — Trafficking detection is the event class **least** served by
the analytics the problem statement names. A trafficked minor moving through a
check post with an adult produces no intrusion, no unusual vehicle and no
suspicious motion — the signal is *relational and behavioural at a legitimate
crossing*. *(Not sourced; recorded because it is the gap most likely to matter
to this specific user.)*

**ASSUMPTION** — The livestock ("cattle", 432 cases) and forest-product classes
mean that **animals and loaded human porters are targets, not nuisance alarms**,
on this border. The nuisance/false-alarm profile assumed for a fenced border in
[domain-research.md](domain-research.md) §4.2 does not transfer cleanly.
*(Basis: `[N1]`'s categories. Not measured.)*

**UNKNOWN** — Time-of-day, seasonal and location distribution of any of these
categories. MHA publishes totals only.

**UNKNOWN** — How many of these cases originated from a camera, a patrol, a naka
check, or an intelligence tip-off. No source distinguishes. This is the SSB
version of the GAO "asset assist" measurement gap
([domain-research.md](domain-research.md) §4.4).

---

## 13. SSB terminology

Descriptive of the domain; not IBVAP vocabulary.

### 13.1 Organisation

| Term | Meaning | Source |
|---|---|---|
| **SSB** — Sashastra Seema Bal | CAPF and Border Guarding Force under MHA, responsible for the Indo-Nepal and Indo-Bhutan borders; 92,541 personnel (31.03.2024) | `[N1]` |
| **Special Service Bureau** | SSB's predecessor, raised post-1962, mandated on border-population morale against subversion, infiltration and sabotage | `[N1][N2]` |
| **LIA** — Lead Intelligence Agency | SSB's designation for the Indo-Nepal border (Jan 2001) | `[N6]` |
| **OBOBGF** — One Border, One Border Guarding Force | MHA deployment principle; assigns Nepal and Bhutan borders to SSB | `[N2]` |
| **FHQ / Frontier / Sector / Battalion / Company / BOP / Check post** | SSB's seven echelons, commanded respectively by DG / IG / DIG / Commandant / Assistant Commandant / Sub-Inspector / Head Constable | `[N8]` |
| **CI&JWS** | SSB's Counter Insurgency & Jungle Warfare School | `[N1]` |
| **"G" School** | A standing SSB training formation; purpose not stated in the source | `[N1]` |
| **APF, Nepal** — Armed Police Force | SSB's counterpart on the Nepal side, under the APF Act, 2001; joint patrols with SSB | `[N7][N8]` |

### 13.2 Units and programmes

| Term | Meaning | Source |
|---|---|---|
| **BIT** — Border Interaction Team | 6-member team incl. female personnel, plain clothes, on 25 high-risk routes; intelligence and community engagement | `[N8]` |
| **AHTU** — Anti-Human Trafficking Unit | SSB has five; 20 nationally established by SSB/BSF under the Nirbhaya Fund | `[N8][N2]` |
| **SAT** — Small Action Team | Platoon-plus strike element for LWE areas | `[N8]` |
| **RRT** — Rescue & Relief Team | 18 teams × 35 personnel for disaster response | `[N8]` |
| **KYA** — Know Your Area | Programme requiring in-depth local geographic, cultural and risk knowledge | `[N8]` |
| **SIMS** — Seizure Incident Management System | SSB's real-time digital seizure/incident register with centralised database | `[N8]` |
| **Civic Action Programme (CAP)** | Statutory SSB duty; community engagement in the area of responsibility | `[N1][N8]` |
| **Naka** | Manned checkpoint on an approach route | `[N23]` |
| **Area domination patrol** | Patrolling to establish presence across a stretch rather than to react to an alarm | `[N23]` |

### 13.3 Places and legal terms

| Term | Meaning | Source |
|---|---|---|
| **Open border** | The treaty-based visa- and passport-free crossing regime with Nepal (1950 Treaty) and Bhutan (1949/2007 Treaty) | `[N7][N13][N14]` |
| **ICP** — Integrated Check Post | LPAI-operated land port; Raxaul (2016) and Jogbani (2016) operational on the Nepal border; Rupaidiha and Sunauli under development, Banbasa at land acquisition | `[N2][N21]` |
| **SSB Act, 2007** | Act No. 53 of 2007; SSB's constituting statute — **not** the BSF Act, 1968 | `[N5]` |
| **SSB Rules, 2009** | Rules elaborating structure and duties (Rule 9 duties, Rule 10 command) | `[N8]` |
| **15 km belt** | The area within which SSB's arrest/search/seizure powers operate, across seven states | `[N8][N17]` |
| **Force Court** | SSB's internal disciplinary tribunal under the SSB Act, 2007 | `[N5]` |
| **Third Country (Foreigner)** | SSB offence category for non-Indian, non-Nepali/Bhutanese nationals using the open border | `[N1]` |
| **FICN** | Fake Indian Currency Notes; a standing SSB seizure category | `[N1]` |

---

## 14. The 10 most important validated findings

Ordered by how much each should change subsequent stages. "Validated" here means
**sourced** — primary where marked; it does not mean confirmed with SSB.

1. **SSB's border is legally open, and MHA's own statement of the problem is
   "misuse of open border", not intrusion.** `[N1]` §3.26/§3.28, identical for
   both borders. Crossing is a treaty right for Indian, Nepali and Bhutanese
   nationals `[N7][N13][N14]`. **Virtual-fence intrusion detection has no clean
   mapping onto this border.**
   ([§2](#2-the-borders-ssb-guards--and-why-they-are-categorically-different))

2. **SSB has already procured a CCTV surveillance setup with Automatic Face
   Recognition and Automatic Number Plate Recognition.** Primary source: MHA
   reply to Lok Sabha USQ 488, 3 February 2026 `[N3]`. The problem statement's
   premise — that FRS and ANPR are absent because they need dedicated hardware —
   does not hold unqualified for the named department.
   ([§6.1](#61-what-ssb-has-procured-primary-source))

3. **SSB's operational achievement table contains no intrusion or infiltration
   category at all.** Its 21 categories are contraband, narcotics, currency,
   gold/silver, forest products, wildlife, cattle, arms, Maoists, third-country
   foreigners, and human trafficking. `[N1]` The largest by case count are
   prohibited/contraband (5,993), narcotics (1,059), Indian currency (471) and
   human trafficking (316). ([§12](#12-ssb-specific-event-classes))

4. **Human trafficking is a first-class SSB mission with a victim-rescue
   outcome** — 316 cases, 274 traffickers arrested, **531 victims rescued** in
   15 months `[N1]`, backed by five dedicated AHTUs `[N8]`. It is also the event
   class least addressable by any analytic the problem statement names.
   ([§12.1](#121-what-this-catalogue-says-about-the-domain))

5. **42% of SSB's BOPs cannot be reached by road.** 308 of 734 BOPs lack road
   connectivity; the remediation proposal is still under MHA consideration
   `[N9]`. Every constraint on hardware, spares, fuel and technician access
   follows from this. ([§10.1](#101-road-access--the-defining-constraint))

6. **The echelons nearest the camera are commanded by a Sub-Inspector (BOP) and
   a Head Constable (check post)** `[N8]`, and BOP/Company-level decision latency
   is already named as a problem by a senior SSB officer `[N8]`. Alerting,
   assessment and evidence-certification designs must fit that rank.
   ([§3.2](#32-command-chain-and-rank-at-each-echelon))

7. **No SSB control room, monitoring roster or video wall is documented
   anywhere in this pass.** The BSF pattern of border Control Rooms cueing QRTs
   is BOLD-QIT-specific and has no SSB counterpart in evidence. Whether SSB
   watches live video at all is genuinely unknown.
   ([§7](#7-control-rooms-and-monitoring-workflow))

8. **No CIBMS-equivalent electronic surveillance programme exists on the SSB
   borders.** MHA's 2023-24 Annual Report describes technological-solution
   segments, pilot projects (2 × 5 km in Jammu, 61 km at Dhubri) and hybrid
   surveillance pilots for the India-Pakistan, India-Bangladesh and
   India-Myanmar borders; the India-Nepal and India-Bhutan paragraphs mention
   only **roads and BOP counts** `[N1]`. ([§10.3](#103-connectivity))

9. **SSB is governed by the SSB Act, 2007 with a 15 km jurisdictional belt** —
   not the BSF Act, 1968 and not the 50/80 km BSF belt `[N8][N17][N5]`. Its
   powers derive from the CrPC (now BNSS), NDPS, Arms and Passport Acts, with
   NDPS empowerment confirmed by MHA `[N4]`. Cases are handed to state police
   `[N17]`. ([§11](#11-ssb-specific-legal-and-evidentiary-considerations))

10. **SSB already has a digital incident register — SIMS** — for seizures and
    enforcement actions, with instant field logging and a centralised database
    `[N8]`. It is the only credible candidate found for "existing command and
    control systems" on this border, and it records **outcomes, not detections**.
    ([§9](#9-command-and-control-integration))

---

## 15. Unresolved questions

Ordered by how much the answer would change subsequent stages. None are answered
by the sources reviewed in this pass.

### Highest priority — block product scoping

- **SQ-1** What is SSB's actual installed CCTV base? Count and location by node
  type (BOP / check post / ICP / battalion HQ), make, model, resolution, codec,
  PTZ vs fixed, thermal vs visible, ONVIF conformance, age. *(§6.3)*
- **SQ-2** **Where is the procured FRS/ANPR CCTV setup deployed, and what is it?**
  Vendor, site count, whether it is one stack or many, whether it exposes streams
  or APIs, and what it is used for today. `[N3]` names it but nothing more. *(§6.1)*
- **SQ-3** **Does SSB monitor live video at all, and if so at which echelon?**
  Operators per room, cameras per operator, shift pattern, instructions on
  seeing something. *(§7)*
- **SQ-4** What is the actual SSB detection → assessment → response sequence at a
  BOP and at a check post, and is there a written SOP or Standing Order? *(§8.2)*
- **SQ-5** **What is SIMS, technically?** Owner, hosting, data model, whether it
  is reachable from a BOP, and whether it can accept a machine-generated event.
  *(§9)*
- **SQ-6** What are the "existing command and control systems" for SSB by name,
  with interfaces? If SIMS is the answer, say so; if there is something else,
  identify it. *(§9)*
- **SQ-7** What does "suspicious activity" mean **on an open border** where
  crossing is lawful? The problem statement names the capability; on this border
  the question is materially harder than on a fenced one. *(§2.3)*

### High priority — shape the problem

- **SQ-8** What is the legal basis, authorisation level, retention rule and
  oversight for face recognition applied to Indian, Nepali and Bhutanese
  nationals exercising a treaty right of movement? Does DPDP 2023 apply? *(§11.6)*
- **SQ-9** Of the 308 road-inaccessible BOPs, how many have cameras today, and
  how is anything electronic maintained there? *(§10.1, §10.5)*
- **SQ-10** What is the real power budget at a generator-powered SSB BOP: hours
  per day, generator rating, fuel resupply interval, any solar/battery? *(§10.2)*
- **SQ-11** What data connectivity exists at an SSB BOP — any IP link, its
  bandwidth, symmetry, metering, reliability, and how many posts are on
  satellite? *(§10.3)*
- **SQ-12** Does SSB have a QRT construct, or is response by the patrol/naka
  already in the field? What carries the alert to them? *(§8.2)*
- **SQ-13** What retention period applies to SSB video, and what is the current
  export-and-handover procedure to state police? Does it satisfy s.63 BSA —
  who signs, who is the "expert", is a hash computed? *(§11.5)*
- **SQ-14** Who owns and operates the CCTV at ICP Raxaul and ICP Jogbani, and
  does SSB have access? *(§4.3)*
- **SQ-15** How many SSB check posts and naka points exist, and how many have a
  camera? *(§4.3)*
- **SQ-16** Do SSB's CrPC-derived powers carry over cleanly to the BNSS, 2023,
  and does SSB register FIRs in any category? *(§11.3, §11.4)*

### Medium priority — validate assumptions in this document

- **SQ-17** Is the "human presence is the primary surveillance instrument"
  assumption correct, or is there camera-led monitoring not described in any
  public source? (Tests §5.2.)
- **SQ-18** What is the real nuisance-alarm profile on this border, given that
  cattle and porters are *targets* rather than nuisances? (Tests §12.1.)
- **SQ-19** Reconcile the BOP counts: 539+195 `[N1]` vs 474+131 `[N23]` vs the
  thesis's 295 `[N8]`. Which definition of "BOP" does each use? (Tests §4.1.)
- **SQ-20** Reconcile Sector HQ count (18 in `[N1]` vs 15 in `[N23]`) and
  battalion strength (1,000 vs 1,172). (Tests §3.1.)
- **SQ-21** Is the Sonauli laser-fence proposal `[N23]` real, and what became of
  it? It is the only electronic-barrier proposal specific to this border found.
  (Tests §4.3.)
- **SQ-22** Does SSB retain body-worn camera footage centrally, and is it in the
  same evidentiary and analytics scope as fixed CCTV? (§6.3)
- **SQ-23** Which stakeholders beyond SSB would consume this video — state
  police, Customs, Immigration, LPAI, NCB, intelligence agencies — and is there
  any question about APF Nepal? (§9)
- **SQ-24** Measured environmental conditions on the SSB borders specifically:
  Terai fog and monsoon, Himalayan foothill conditions, temperature range at
  camera housings. (§10.4)
- **SQ-25** Is the Indo-Bhutan border operationally the same problem as the
  Indo-Nepal border, or a different one? Every source in this pass treats them
  together; MHA's challenge statement is verbatim identical for both `[N1]`,
  which may reflect drafting convention rather than operational sameness.

### Research-process gaps

- **SQ-26** Retrieve the **Sashastra Seema Bal Act, 2007** and **SSB Rules,
  2009** text directly. Both India Code and the MHA-hosted PDF returned HTTP 403
  in this pass; §11 currently rests on a Nepali thesis's reading of them.
- **SQ-27** Retrieve the **official SSB website**. `ssb.nic.in` does not resolve
  and `ssb.gov.in` returned no navigable content to the fetcher. The force's own
  statement of its organisation and charter of duties has not been read.
- **SQ-28** Retrieve the **MHA Annual Report 2024-25 or later** if published,
  for updated BOP counts, strength and the SSB achievements table. This pass
  used 2022-23 and 2023-24.
- **SQ-29** Find any **Parliamentary Standing Committee on Home Affairs** report
  specifically on SSB, and any **CAG audit** of SSB modernisation procurement.
  These are the likeliest sources for the installed-camera-base question (SQ-1).
- **SQ-30** Record the **SIH organisation/department field** for PS 26187 in
  `docs/00-project/`, so the SSB attribution this document rests on is itself
  documented. *(See the attribution caveat at the top.)*
- **SQ-31** Confirm the seizure-quantity cells in the §12 tables against the
  published Annual Report PDFs; the multi-column extraction leaves some row
  assignments uncertain.

---

## 16. What in `domain-research.md` is BSF-specific, not SSB

Each item below appears in [domain-research.md](domain-research.md) and **must
not be carried into SSB product, design or architecture work without
re-derivation.** Nothing here says the original entry is wrong — it says the
entry is about BSF or about a fenced/closed border, and SSB is neither.

| # | Item in `domain-research.md` | Why it is BSF-specific | What is true for SSB |
|---|---|---|---|
| 1 | **§1.1 / §7.1 — "A BOP is the permanent operational base of the Border Security Force"** and the composite-BOP definition | MHA's own text defines BOPs as *"the main workstation of **the BSF** along the borders"* `[N2]` §3.9. The 509 composite BOPs sanctioned in Oct 2023 are 383 Indo-Bangladesh + 126 Indo-Pakistan `[S15]` — **none on the SSB borders** | SSB has **539 BOPs (Nepal) + 195 (Bhutan)** `[N1]`, commanded by a **Sub-Inspector**, at ~3.9 km spacing, with **308 of 734 lacking road access** `[N8][N9]` |
| 2 | **§1.1 — 3,323 km, Radcliffe Line / LoC / AGPL, 145.876 km unfenced riverine** | Entirely the India-Pakistan border | SSB's borders are **1,751 km (Nepal) + 699 km (Bhutan)**, **unfenced throughout**, and **legally open** `[N1][N7][N14]` |
| 3 | **§1.1 / §5.5 — "ICP security infrastructure includes … observation towers manned by BSF personnel"** | Both cited surveys `[S6][S7]` are India-Bangladesh field surveys | India-Nepal ICPs are **Raxaul** and **Jogbani** `[N2]`; **who mans them and who owns the CCTV there is UNKNOWN** (SQ-14) |
| 4 | **§1.3 — CIBMS, BOLD-QIT, smart fencing, laser walls, BFSR, UGS, aerostats, the CIBMS sensor grid** | All are India-Pakistan / India-Bangladesh programmes. `[N1]` places technological-solution segments and pilots on the IPB, IBB and IMB only; its India-Nepal and India-Bhutan paragraphs mention **only roads and BOP counts** | **No CIBMS-equivalent programme is documented on the SSB borders.** The only electronic-barrier item found is an unconfirmed laser-fence proposal at Sonauli `[N23]` (SQ-21) |
| 5 | **§1.3 / §6.2 — the dedicated CIBMS communication backbone (OFC, microwave, DMR, satcom)** | BOLD-QIT and CIBMS infrastructure | SSB has **satellite phones** in its surveillance inventory `[N3]`; **no dedicated backbone is documented**. Bandwidth at an SSB BOP is UNKNOWN (SQ-11) |
| 6 | **§1.3 — "BSF deployed ~5,000 body-worn cameras … along the Bangladesh border"** | BSF, Bangladesh border | SSB is reported to use body-worn cameras `[N8]`; **no count, and retention/scope UNKNOWN** (SQ-22) |
| 7 | **§2.1 / §3.2 — "BSF Control Room" receiving feeds and cueing QRTs; the sensor → control room → QRT → interception chain** | Documented for BOLD-QIT specifically `[S3][S21]` | **No SSB control room and no SSB QRT construct is documented at all** (§7, SQ-3, SQ-12). Do not assume this chain |
| 8 | **§2.1 — "BSF has ~290,000 personnel across 192 battalions"; §7.1 Frontier/Sector/Battalion/Company as "BSF command echelons"** | BSF figures | SSB: **92,541 personnel** (31.03.2024), **6 Frontiers, 18 Sectors, 73 battalions** (55 operational + 18 reserve) `[N1][N8]`. The echelon *names* are shared; the counts and the rank at each level are not |
| 9 | **§3.5 — "BSF does not have policing powers … cannot register an FIR … handover within 24 hours" (BSF Act, 1968)** | The **BSF Act, 1968** does not govern SSB | SSB is constituted under the **SSB Act, 2007** `[N5]`, with powers under CrPC/BNSS, NDPS (MHA-confirmed `[N4]`), Arms and Passport Acts `[N8][N17]`. Whether SSB may register an FIR is **UNKNOWN** (SQ-16) |
| 10 | **§3.5 / §6.6 — the 50 km (Assam/Punjab/WB) and 80 km (Gujarat) jurisdictional belt** | A **2021 BSF-specific notification** | SSB's belt is **15 km**, across Uttarakhand, UP, Bihar, West Bengal, Sikkim, Assam and Arunachal Pradesh `[N8][N17]` |
| 11 | **§4.2 — the nuisance-alarm profile (livestock, wildlife, vegetation, civilian agricultural activity as *noise*)** | Framed for a fenced border with a sterile zone | On the SSB border **cattle (432 cases), forest products (398) and wildlife (78) are seizure categories — i.e. targets** `[N1]`, and lawful civilian crossing is constant. The signal/noise split is different in kind (SQ-18) |
| 12 | **§5.1 / §5.2 — infiltration-attempt counts, ₹461.07 crore contraband, cattle trade to Bangladesh, the Majhdia bunkers** | India-Bangladesh border statistics | Use **`[N1]`'s SSB achievements table** ([§12](#12-ssb-specific-event-classes)) as the SSB event baseline. It has **no infiltration category** |
| 13 | **§5.3 — drone incursions (245–294 drones, Punjab as epicentre)** | India-Pakistan border, Punjab | **No drone-incursion event class is documented on the SSB borders.** SSB operates UAVs itself `[N3]`; that is a capability, not a threat class |
| 14 | **§5.4 — cross-border tunnels** | India-Bangladesh / India-Pakistan | Not documented on the SSB borders |
| 15 | **§6.1 / §6.3 — power and environmental findings (BADP electrification, fog on the Punjab/Jammu plains, western desert dust, char-land riverine conditions)** | Drawn from CIBMS deployment areas | SSB-specific: **generators at all BOPs without a grid connection**, situation varying by state `[N9][N18]`; terrain is Himalayan foothills to Indo-Gangetic plain `[N7][N14]`. Sector-level environmental data is UNKNOWN (SQ-24) |
| 16 | **§4.4 — the GAO "asset assist" measurement gap** | A US finding, applied by analogy to BSF | The gap applies to SSB too — **`[N1]` records cases and arrests but never how a case was detected** — but the analogy should be re-grounded on SSB's own reporting (SQ-1, §12.1) |

**One item in `domain-research.md` transfers to SSB unchanged:** **§3.5 / §6.6 —
Section 63 of the Bharatiya Sakshya Adhiniyam, 2023** and the hash-value
certificate requirement `[S29]`. That is force-agnostic Indian evidence law and
applies to SSB video exactly as to BSF video — see
[§11.5](#115-evidentiary-requirements-for-recorded-video). The peer-reviewed
operator-vigilance findings (§4.1 `[S9][S10]`) and the technology-performance
bounds on FRS, ANPR and i-LIDS (§6.7 `[S25][S26][S27]`) are also
force-agnostic, though whether they *apply* to SSB depends on SQ-3 (whether SSB
has monitoring operators at all).

---

## 17. Sources

Reliability key: **P** = primary/official, **A** = academic or peer-reviewed,
**T** = think-tank / policy analysis, **N** = news, **V** = vendor or trade,
**E** = encyclopedic/tertiary.

| ID | Source | Type | Retrieval | URL |
|---|---|---|---|---|
| N1 | **MHA Annual Report 2023-24** — Ch. 3 (Border Management: India-Nepal §3.26–3.27, India-Bhutan §3.28) and Ch. 7 (SSB §7.51–7.53, achievements 01.01.2023–31.03.2024) | P | **Direct (full text)** | https://www.mha.gov.in/sites/default/files/AnnualReport_27122024.pdf |
| N2 | **MHA Annual Report 2022-23** — Ch. 3 (border lengths, OBOBGF, BOP definition §3.9, ICP tables §3.54–3.55) and Ch. 7 (SSB §7.53–7.55, AHTU figures) | P | **Direct (full text)** | https://www.mha.gov.in/sites/default/files/AnnualReportEngLish_11102023.pdf |
| N3 | **Lok Sabha Unstarred Question No. 488**, answered 03.02.2026 — *Modernization of Sashastra Seema Bal*; reply of MoS Home Shri Nityanand Rai | P | **Direct (full text)** | https://www.mha.gov.in/MHA1/Par2017/pdfs/par2026-pdfs/LS03022026/488.pdf |
| N4 | **Lok Sabha Unstarred Question No. 634**, answered 03.02.2026 — *Seizure of Narcotic Substances*; SSB NDPS empowerment, and the "AI based features … Integrated Command and Control Centre" measure | P | **Direct (full text)** | https://www.mha.gov.in/MHA1/Par2017/pdfs/par2026-pdfs/LS03022026/634.pdf |
| N5 | **Sashastra Seema Bal Act, 2007** (Act No. 53 of 2007, enacted 20.12.2007) — **[indirect: India Code and the MHA-hosted PDF both returned HTTP 403]** | P | Indirect | https://www.indiacode.nic.in/handle/123456789/2039 |
| N6 | Wikipedia — *Sashastra Seema Bal* (mandate, border assignment dates, echelon composition, LIA designation) | E | Direct | https://en.wikipedia.org/wiki/Sashastra_Seema_Bal |
| N7 | Wikipedia — *India–Nepal border* (length, terrain, open border, unfenced, guarding forces, joint patrols, ICP list, disputes) | E | Direct | https://en.wikipedia.org/wiki/India%E2%80%93Nepal_border |
| N8 | **Silwal, Bishal (April 2025)** — *Deployment Practices of APF, Nepal and SSB along Nepal-India Border*. Master's thesis, APF Command and Staff College, Faculty of Humanities and Social Sciences, Tribhuvan University. Supervisor: Assoc. Prof. Dr. Tikaram Gautam. Based on 7 KIIs and 2 FGDs incl. SSB officers, Jan–Feb 2025 | A | **Direct (full text)** | https://elibrary.tucl.edu.np/JQ99OgQIizUxyjI9nB0on9OyLkqsGIf4/api/core/bitstreams/7f5c9881-3446-46fd-9518-9c03f865f7c8/content |
| N9 | The Tribune — *308 SSB outposts on Nepal, Tibet borders await road connectivity*, Animesh Singh, 17 Aug 2025 (BOP road connectivity; generators and RO plants at BOPs) | N | Direct | https://www.tribuneindia.com/news/india/308-ssb-outposts-on-nepal-tibet-borders-await-road-connectivity |
| N10 | ThePrint — *SSB, guarding Nepal, Bhutan borders, equipped with state-of-the-art surveillance equipment: Govt* (reports the `[N3]` reply) | N | Direct | https://theprint.in/india/ssb-guarding-nepal-bhutan-borders-equipped-with-state-of-the-art-surveillance-equipment-govt/2844824/ |
| N11 | Indian Masterminds — *From Drones to AI Eyes: How Sashastra Seema Bal Is Reinforcing India's Nepal-Bhutan Border Security* (reports the `[N3]` reply; adds "at key crossing points" framing) | N | Direct | https://indianmasterminds.com/news/sashastra-seema-bal-nepal-bhutan-border-surveillance-systems-182910/ |
| N12 | News On Air (Prasar Bharati) — HM Amit Shah at SSB's 61st Raising Day, 20 Dec 2024 (*"protecting fenced borders is much easier than protecting an open border"*) | P/N | Direct | https://www.newsonair.gov.in/hm-amit-shah-joins-ssbs-61st-raising-day-in-west-bengal |
| N13 | India–Nepal Treaty of Peace and Friendship, 31 July 1950 — free movement, residence, property and commerce provisions | E | Direct | https://en.wikipedia.org/wiki/India%E2%80%93Nepal_Treaty_of_Peace_and_Friendship |
| N14 | Bhutan–India border and India–Bhutan Treaty of Friendship 1949 (revised 2007); freedom of movement; Bhutan's 23 Sep 2022 permit restriction; reserved forests | E | Direct | https://grokipedia.com/page/Bhutan%E2%80%93India_border |
| N15 | ThePrint — *Govt sanctions 12 new SSB battalions to fortify Nepal, Bhutan borders, tri-junction area* | N | Direct | https://theprint.in/defence/govt-sanctions-12-new-ssb-battalions-to-fortify-nepal-bhutan-borders-tri-junction-area/615268/ |
| N16 | Swarajya — *SSB Operationalises 72 Outposts Along Nepal, Bhutan Borders* (18 in Sikkim and Arunachal Pradesh) | N | Direct | https://swarajyamag.com/insta/doklam-aftermath-strengthening-its-defences-ssb-operationalises-72-outposts-along-nepal-bhutan-borders |
| N17 | DNA India — *Sashastra Seema Bal gets powers of search, arrest and seizure* (CrPC/NDPS/Arms/Passport Acts; 15 km belt across seven states; Customs Act contemplated) | N | Direct | https://www.dnaindia.com/india/report-sashastra-seema-bal-gets-powers-of-search-arrest-and-seizure-1356284 |
| N18 | PRS Legislative Research — report summary, *Working Conditions in Border Guarding Forces* (Parliamentary Standing Committee; lack of electricity at SSB and ITBP BOPs) | T/P | Direct | https://prsindia.org/policy/report-summaries/working-conditions-in-border-guarding-forces |
| N19 | Deccan Herald — SSB intelligence wing operationalised, ~650 field and staff agents — **[indirect: HTTP 403]** | N | Indirect | https://www.deccanherald.com/india/ssb-intel-wing-operationalise-monday-2025041 |
| N20 | News On Air (Prasar Bharati) — *NCB, SSB to strengthen anti-drug trafficking operations on Indo-Nepal border* | P/N | Direct | https://www.newsonair.gov.in/ncb-ssb-to-strengthen-anti-drug-trafficking-operations-on-indo-nepal-border |
| N21 | CSEP / LPAI — Riya Sinha, *Linking Land Borders: India's Integrated Check Posts* (origin of the four India-Nepal ICPs; 2003 NSCS assessment) | T | Direct | https://www.lpai.gov.in/sites/default/files/2021-10/WP_Linking-land-borders-ICP-1.pdf |
| N22 | *(reserved — AHTU / Nirbhaya Fund figures are cited from `[N2]`)* | — | — | — |
| N23 | Secondary compilations of SSB role and structure — GKToday, Model Diplomat, Grokipedia, Military Wiki, Information Array and similar. Used **only** for items no better source covered: naka / area-domination / joint-check-post vocabulary, the 474+131 BOP figures, the 15-sector figure, the 1,172 battalion strength, the Sonauli laser-fence proposal, and the trafficking-corridor framing. **Low confidence throughout; every figure from this row is flagged as conflicting or unconfirmed at point of use** | E | Direct | https://grokipedia.com/page/Sashastra_Seema_Bal |

**Carried forward from [domain-research.md](domain-research.md)** and cited here
by its IDs: `[S3]`, `[S6]`, `[S7]`, `[S9]`, `[S10]`, `[S15]`, `[S21]`, `[S22]`,
`[S25]`, `[S26]`, `[S27]`, `[S29]`. See that document's §9 for full entries.

---

## Document status

**Complete for this pass — Stage 01, Domain Research, SSB layer.**

No product, design, architecture or technology decisions are made or implied by
this document. Two findings in particular
([§14](#14-the-10-most-important-validated-findings) items 1 and 2) bear directly
on how the problem statement's named capabilities map onto this department, and
both are recorded here strictly as **research findings**; acting on them belongs
to `docs/02-product/`.

The assumptions in this document require validation before they are relied on.
The unknowns in [§15](#15-unresolved-questions) are the input to the next
research passes (users, competitors, technology) — with **SQ-1 through SQ-7**
blocking product scoping, and **SQ-26 through SQ-31** being research-process
debts this pass incurred.

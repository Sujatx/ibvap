# SSB Operational Context — Sashastra Seema Bal

**Stage:** 01 — Research → Domain
**Date:** 2026-08-24
**Scope:** The operational context of **Sashastra Seema Bal (SSB)** — the
department named for [SIH Problem Statement 26187](../../00-project/problem.md)
— covering its identity and mandate, the borders it guards, organisational
structure, physical nodes (BOPs/check posts), surveillance responsibilities,
CCTV/video usage already in service, control-room and monitoring workflow,
detection → assessment → response, command/control integration, remote-location
constraints, and SSB-specific legal/evidentiary considerations for recorded
video.

This document records how SSB works, what is well-evidenced, and what remains
unknown, to ground later product scoping in `docs/02-product/` (per
[CLAUDE.md](../../../CLAUDE.md)).

**Companion documents:** [domain-research.md](domain-research.md) covers the
generic border-CCTV domain and is heavily BSF/CIBMS-weighted; §5 of this
document marks which of its findings must **not** be carried over to SSB.
[ssb-operational-workflow.md](ssb-operational-workflow.md) covers SSB's
operational workflow in more detail.

## Contents

1. [Research Objective and Scope](#1-research-objective-and-scope)
2. [Key Findings](#2-key-findings)
3. [Detailed Findings](#3-detailed-findings)
4. [Implications for IBVAP](#4-implications-for-ibvap)
5. [Risks and Limitations](#5-risks-and-limitations)
6. [Open Questions and Research Gaps](#6-open-questions-and-research-gaps)
7. [Conclusions](#7-conclusions)
8. [References](#8-references)

---

## 1. Research Objective and Scope

The objective of this pass was to establish SSB's operational context — as
distinct from the generic, BSF-weighted border-CCTV domain research already on
file — so that later product, design and architecture work is grounded in the
correct force's structure, mandate, legal basis, borders and existing
technology.

**Attribution caveat.** [problem.md](../../00-project/problem.md) records the
SIH problem statement verbatim but does not record the SIH organisation/
department field; this document proceeds on the project owner's statement that
**SSB is the department named for PS 26187**. The problem statement text itself
describes "border security forces" generically and is force-agnostic — it is
the *department attribution*, not the problem statement, that makes SSB the
operative user. Recording the organisation field in `docs/00-project/` would
close this gap (tracked as a research-process gap in §6).

**Source base.** Primary MHA sources were retrieved directly for this pass: the
MHA Annual Reports 2023-24 and 2022-23, and two Lok Sabha Unstarred Question
replies of 3 February 2026. Statements sourced to these are the
highest-confidence facts in this document. Three sources could not be retrieved
directly and are marked "indirect" at point of use: the text of the Sashastra
Seema Bal Act, 2007 (both `indiacode.nic.in` and the MHA-hosted PDF returned
HTTP 403); the official SSB website (`ssb.nic.in` does not resolve, `ssb.gov.in`
served no navigable content); and one Deccan Herald report on the SSB
intelligence wing (HTTP 403). Full source list and reliability ratings are in
§8 (References).

Where a claim rests on inference rather than a stated source — an argument from
absence, or a conclusion drawn by combining several sources — this is noted in
the prose itself rather than tagged with a separate label, and the reasoning is
given so it can be checked.

---

## 2. Key Findings

Ordered by how much each should change subsequent stages. "High confidence"
below means well-sourced, generally against primary MHA data — it does not mean
confirmed with SSB directly.

1. **SSB's border is legally open, and MHA's own statement of the problem is
   "misuse of open border," not intrusion.** This is stated identically for both
   borders MHA administers through SSB [N1] §3.26/§3.28. Crossing is a treaty
   right for Indian, Nepali and Bhutanese nationals [N7][N13][N14]. Virtual-fence
   intrusion detection has no clean mapping onto this border (§3.2).

2. **SSB has already procured a CCTV surveillance setup with Automatic Face
   Recognition and Automatic Number Plate Recognition.** Primary source: MHA's
   reply to Lok Sabha USQ 488, 3 February 2026 [N3]. The problem statement's
   premise — that FRS and ANPR are absent because they require specialised
   hardware — does not hold unqualified for the named department (§3.6).

3. **SSB's operational-achievement table contains no intrusion or infiltration
   category at all.** Its 21 categories are contraband, narcotics, currency,
   gold/silver, forest products, wildlife, cattle, arms, Maoists, third-country
   foreigners and human trafficking [N1]. The largest by case count are
   prohibited/contraband items (5,993), narcotics (1,059), Indian currency (471)
   and human trafficking (316) (§3.12).

4. **Human trafficking is a first-class SSB mission with a victim-rescue
   outcome** — 316 cases, 274 traffickers arrested, 531 victims rescued in 15
   months [N1], backed by five dedicated Anti-Human Trafficking Units [N8]. It
   is also the event class least addressable by the analytics the problem
   statement names, since the signal is relational and behavioural rather than
   an intrusion, an unusual vehicle, or suspicious motion (§3.12).

5. **42% of SSB's Border Out Posts cannot be reached by road.** 308 of 734 BOPs
   lack road connectivity; the remediation proposal remains under MHA
   consideration [N9]. Every constraint on hardware, spares, fuel and
   technician access follows from this (§3.10).

6. **The echelons nearest the camera are commanded by a Sub-Inspector (BOP) and
   a Head Constable (check post)** [N8], and BOP/Company-level decision latency
   is already named as a problem by a senior SSB officer [N8]. Any alerting,
   assessment or evidence-certification design must fit that rank (§3.3).

7. **No SSB control room, monitoring roster or video wall is documented
   anywhere in this pass.** The BSF pattern of border Control Rooms cueing Quick
   Reaction Teams is BOLD-QIT-specific and has no demonstrated SSB counterpart.
   Whether SSB watches live video at all is a genuinely open question (§3.7).

8. **No CIBMS-equivalent electronic surveillance programme exists on the SSB
   borders.** MHA's 2023-24 Annual Report describes technological-solution
   segments and hybrid-surveillance pilots for the India-Pakistan,
   India-Bangladesh and India-Myanmar borders; its India-Nepal and India-Bhutan
   paragraphs mention only roads and BOP counts [N1] (§3.10).

9. **SSB is governed by the SSB Act, 2007, with a 15 km jurisdictional belt** —
   not the BSF Act, 1968, and not the 50/80 km BSF belt [N8][N17][N5]. Its
   powers derive from the CrPC (now BNSS), NDPS, Arms and Passport Acts, with
   NDPS empowerment confirmed directly by MHA [N4]. Apprehended persons and
   seized items are handed to local police [N17] (§3.11).

10. **SSB already has a digital incident register — the Seizure Incident
    Management System (SIMS)** — for seizures and enforcement actions, with
    instant field logging and a centralised database [N8]. It is the only
    credible candidate found for "existing command and control systems" on this
    border, and it records outcomes, not detections (§3.9).

---

## 3. Detailed Findings

### 3.1 Identity, Mandate, and Organisational Culture

SSB is one of five **Central Armed Police Forces (CAPFs)** under the Ministry
of Home Affairs (BSF, CISF, CRPF, ITBP, SSB), of which **AR, BSF, ITBP and SSB**
are the "Border Guarding Forces" [N2]. It originated as the Special Service
Bureau, raised after the 1962 conflict with a mandate centred on the morale and
capability of the border population against subversion, infiltration and
sabotage from across the border. It became a Border Guarding Force in **2001**
under MHA and was rechristened *Sashastra Seema Bal* with an amended charter of
duties [N1][N2]. It was declared a Border Guarding Force and Lead Intelligence
Agency (LIA) for the Indo-Nepal border in **January 2001**, and assigned the
Indo-Bhutan border in **March 2004** [N6] (an encyclopedic source; the LIA
designation recurs in secondary compilations [N23] but was not found stated in
the MHA Annual Reports retrieved here).

Force strength was **92,541** as of 31.03.2024 and **90,194** as of 31.12.2022,
per MHA [N1][N2] (a tertiary source gives 94,261 [N6]; the MHA figures are
treated as authoritative).

**Charter of duties.** As summarised from the SSB Act, 2007 and SSB Rules, 2009
(text not independently retrieved — see §8), SSB's charter is to: secure
designated border areas; foster a sense of security among border communities;
prevent trans-border crime, smuggling and illegal activity; regulate
unauthorised entry into or exit from Indian territory; conduct **civic action
programmes**; and perform additional duties assigned by the Central Government
[N8]. SSB additionally carries **Internal Security and Counter-Insurgency**
duties, deployed in J&K, Assam, and the LWE-affected areas of Chhattisgarh,
Jharkhand and Bihar [N1][N2]. An SSB officer interviewed for a 2025 Tribhuvan
University thesis described the core function as *"border surveillance,
intelligence gathering, curbing smuggling, counter-insurgency operations, and
ensuring law enforcement along the border"* [N8] (a Nepali master's thesis,
key-informant sourced — indicative of role framing, not doctrine).

Several indicators converge on **intelligence collection being a first-class
SSB output**, not merely incidental to interdiction: the LIA designation, a
dedicated intelligence wing [N19], the Border Interaction Teams, and the "Know
Your Area" programme (§3.5) all point the same way, though no primary source
states an explicit doctrinal priority ordering. For a video platform, this
suggests an intelligence-led force values *pattern over time* (who uses a
track, how often, with what vehicles) at least as much as *alarm in the
moment* — a materially different demand than pure intrusion alarming.

### 3.2 The Open Border

SSB is deployed on the **Indo-Nepal border (1,751 km)** and the **Indo-Bhutan
border (699 km)** — 2,450 km in total [N1][N2]. The Indo-Nepal border passes
through **Uttarakhand, Uttar Pradesh, Bihar, West Bengal and Sikkim** [N1]
(state-wise lengths reported as Uttarakhand 263.7 km, Uttar Pradesh 599.3 km,
Bihar 800.4 km, West Bengal 105.6 km, Sikkim 99 km [N6], tertiary). The
Indo-Bhutan border passes through **Assam, West Bengal, Arunachal Pradesh and
Sikkim** [N1] (reported as Sikkim 32 km, West Bengal 183 km, Assam 267 km,
Arunachal Pradesh 217 km [N6], tertiary). Deployment follows MHA's "One
Border, One Border Guarding Force" (OBOBGF) principle, under which "Nepal and
Bhutan Borders — Sashastra Seema Bal (SSB)" [N2].

**This is the single most important SSB-specific fact.** MHA's own statement
of the problem is identical on both borders and is *not* about intrusion
detection: *"The main challenges along this border are to check misuse of
**open border** by terrorists and criminals for illegal and anti-national
activities"* [N1] (§3.26 for Nepal, §3.28 for Bhutan). The **India–Nepal Treaty
of Peace and Friendship (31 July 1950)** grants citizens of each country, on a
reciprocal basis, the same privileges as to residence, property, trade,
commerce and **movement** in the other's territory — no passport or visa is
required to cross, and tens of thousands cross daily [N7][N13]. The border is
**unfenced**, with numerous official and unofficial crossing points beyond the
designated checkposts [N7]. Freedom of movement between India and Bhutan has
similarly existed since the **Treaty of Friendship of 8 August 1949** (revised
2007); the border is largely unfenced and open, with no formal immigration
check at most points for citizens holding valid identification. From **23
September 2022**, Bhutan restricted Indian nationals' permit-free movement to
the border towns of Phuentsholing, Gelephu and Samdrup Jongkhar, with a permit
obtainable on arrival beyond them [N14] (tertiary; a Bhutanese measure, not an
Indian border-control change). At SSB's 61st Raising Day (20 December 2024),
the Union Home Minister observed that *"protecting fenced borders is much
easier than protecting an open border"* [N12] (state broadcaster). Nepal's
counterpart force, the **Armed Police Force (APF), Nepal**, polices the other
side under the APF Act, 2001, and the two forces conduct **joint patrols** on
the demarcation line [N7][N8].

**Operational consequence.** On the SSB border, a person crossing the line is
not itself an offence and therefore not, on its own, a reportable incident.
What makes an event reportable is *who* (a third-country national, a known
trafficker, a minor being moved), *what they carry* (contraband, currency,
gold, narcotics, wildlife, timber), or *when and where* (a closed crossing, an
off-route track at night) — not the crossing itself. This reading follows from
the treaty right of movement [N7][N13] combined with MHA's framing of the
challenge as "misuse of open border" [N1], and is corroborated by the
composition of SSB's own seizure/arrest table, which is almost entirely
contraband-, currency- and person-category based rather than intrusion-count
based (§3.12). **This inverts the core assumption of virtual-fence intrusion
detection**: a line-crossing alarm that is correct 100% of the time would still
be almost entirely noise here. A distinct SSB event category exists precisely
for the exception: **"Third Country (Foreigner)"** — 44 cases, 58 persons
arrested between 01.01.2023 and 31.03.2024 [N1]. The open-border regime applies
to Indian, Nepali and Bhutanese nationals; third-country nationals using it are
an offence class in their own right. It remains unclear whether SSB maintains,
or is permitted to maintain, any record of *routine* legitimate crossings by
Indian/Nepali nationals — and therefore whether a video platform generating a
person-detection record for every such crossing would even be lawful (see
§3.11 and Open Question SQ-7).

### 3.3 Organisational Structure and Echelons

SSB's formations, as recorded by MHA [N1][N2]:

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

Of the 73 battalions, **55 are operational and 18 are reserve** [N8] (thesis,
sourced to SSB FHQ 2025 — not confirmed in [N1]). A **12-battalion expansion**
for the Nepal and Bhutan borders and the tri-junction area has been sanctioned
[N15] (news).

The command chain and commanding rank at each echelon [N8] (corroborated for
the upper echelons by [N6]; the thesis text is internally inconsistent once,
naming "Deputy Commandant" for Company in a table versus "Assistant
Commandant" in prose — [N6] gives Assistant Commandant):

| Formation | Commander |
|---|---|
| Force Headquarters (New Delhi) | Director General (DG) |
| Frontier HQ | Inspector General (IG) |
| Sector HQ | Deputy Inspector General (DIG) |
| Battalion | Commandant |
| Company | Assistant Commandant |
| **Border Out Post (BOP)** | **Sub-Inspector (SI)** |
| **Check post** | **Head Constable** |

Nominal composition: each sector comprises **5–6 battalions**; **2–4 sectors**
form a Frontier; a battalion has **7 companies**; each company has **3 BOPs**
[N6] (tertiary; battalion strength given variously as 1,000 [N6] and 1,172
[N23]). A senior-SSB-officer interview identifies BOP- and Company-level
**decision latency** as a live problem: the layered command structure *"can
occasionally result in delays in decision-making, particularly in situations
demanding rapid responses at the BOP and COY levels,"* with more autonomy at
lower levels named as the remedy [N8].

**The two echelons nearest the camera are led by an SI and a Head Constable
respectively.** Any interface, alert or evidentiary procedure that assumes a
technically trained officer at the point of capture is assuming something this
structure does not supply. Whether Frontier or Sector HQ hosts any
operations/monitoring facility distinct from a battalion-level one is not
established (Open Question).

### 3.4 Border Out Posts, Check Posts, and Other Nodes

MHA records **539 Border Out Posts** along the India-Nepal border and **195
BOPs** along the India-Bhutan border — **734 total**, unchanged between the
2022-23 and 2023-24 Annual Reports [N1][N2]. SSB separately reported
**operationalising 72 new posts** along the Indo-Nepal and Indo-Bhutan borders,
18 of them in Sikkim and Arunachal Pradesh [N16] (news, post-Doklam period).

BOP counts conflict across sources and should not be treated as settled:

| Figure | Source | Confidence |
|---|---|---|
| 539 (Nepal) + 195 (Bhutan) = 734 BOPs | MHA Annual Reports [N1][N2] | High — primary |
| 734 total BOPs, 426 with road connectivity | The Tribune, 17 Aug 2025 [N9] | Medium — news, but matches [N1]'s total exactly |
| 474 (Nepal) + 131 (Bhutan) = 605 BOPs | Secondary compilations [N23] | Low |
| 295 BOPs on the Nepal border, within 528 total SSB "units" | Thesis, Nepali-side data [N8] | Low — counts units incl. HQs, possibly only certain provinces |

The 539/195 split from [N1] is taken as the working figure, since it is primary
and internally consistent with [N2] and with [N9]'s total; the lower
third-party counts likely reflect older data or a narrower definition of "BOP."

**Spacing and density.** Average distance between SSB BOPs on the Nepal border
is reported as **3.9 km**, against 7.7 km for Nepal's APF [N8]; an earlier
academic account puts SSB armed posts "approximately three kilometres apart"
against APF posts fifteen to twenty km apart [N8] (Baral & Pyakurel 2013, cited
in the thesis). The same study describes SSB's model as a "high-intensity
security model … continuous surveillance and rapid response" with roughly
**45,000 personnel and 528 units** on the Nepal border [N8] (uncorroborated by
an Indian primary source; approximate). Arithmetic on [N1]'s 539 BOPs over
1,751 km gives ≈3.25 km per BOP, consistent with [N8] — at this density, most
of the border is plausibly watched by a person from a post rather than by a
sensor covering a gap between posts, the opposite of the CIBMS "electronic
domination of a gap" model. This is an inference from the spacing arithmetic,
not a sourced doctrinal statement.

**Check posts, ICPs and other nodes.** SSB establishes border outposts,
observation posts, check posts and joint check posts, and mans **naka**
checkpoints [N23] (secondary compilations; the check-post echelon commanded by
a Head Constable is corroborated by [N8]). Two **Integrated Check Posts
(ICPs)** are operational on the India-Nepal border: **Raxaul** (Bihar,
operationalised 03.06.2016) and **Jogbani** (Bihar, 15.11.2016); **Rupaidiha**
and **Sunauli** (both UP) are under development, and **Banbasa** (Uttarakhand)
is at the land-acquisition stage [N2]. ICP amenities listed by MHA include an
electronic weighbridge, inspection shed and **CCTV** [N2]; ICPs are operated by
the **Land Ports Authority of India (LPAI)**, not by the border force [N21].
The four major India-Nepal ICPs (Jogbani, Raxaul, Sonauli, Rupaidiha) were
first proposed in October 2003 after an NSCS assessment found infrastructure at
these locations "abysmal" [N21]. Who owns and operates the CCTV at an
India-Nepal ICP — LPAI, Customs, Immigration or SSB — and whether SSB has
access to those feeds, is not established; the earlier domain pass recorded
that ICP observation towers on the India-Bangladesh border are "manned by BSF
personnel" [S6][S7], but that staffing cannot be assumed to apply at Raxaul or
Jogbani (§5).

A **laser fence** venture was reportedly proposed by SSB at the **Sonauli check
post (UP)**, with possible extension [N23] (secondary compilation, not found in
any primary source — low confidence, but the only electronic-barrier proposal
specific to the SSB border found in this pass). The number of SSB check posts
and naka points, and how many have any camera at all, is not established.

### 3.5 Surveillance Responsibilities and Methods

SSB's charter requires it to prevent trans-border crime, smuggling and illegal
activity, and to regulate unauthorised entry into or exit from Indian territory
[N8] (indirect for the Act text). MHA frames the surveillance object on both
SSB borders as "misuse of open border by terrorists and criminals" [N1]. SSB is
empowered under the **NDPS Act, 1985** to carry out search, seizure and arrest
for illicit narcotics trafficking at the international border — named alongside
BSF and Assam Rifles in MHA's list of drug-control measures [N4]. SSB and the
**Narcotics Control Bureau** have agreed to strengthen anti-drug-trafficking
coordination on the Indo-Nepal border, focusing on intelligence sharing, joint
operations and capacity building [N20] (state broadcaster).

SSB's surveillance repertoire, as described across sources, is **patrol- and
post-based**: a layered grid of BOPs, area domination patrols, manned
naka/check posts, joint patrols with APF Nepal, and observation posts
[N8][N23]. Joint patrols with APF Nepal rose from **78 in FY 071/72 to 5,841 in
FY 080/81** (Nepali fiscal years; roughly 2014-15 to 2023-24) [N8] (APF Nepal HQ
data). SSB fields **Border Interaction Teams (BITs)** on **25 high-risk
smuggling routes**; each BIT has six members including female personnel and
operates in civilian attire, gathering intelligence and engaging local
communities [N8]. SSB operates **five Anti-Human Trafficking Units (AHTUs)** in
vulnerable border regions, working with state agencies and NGOs [N8];
nationally, **788 AHTUs** are operational, **including 20 established by
SSB/BSF** under the Nirbhaya Fund [N2]. SSB fields **Small Action Teams (SATs)**
of at least platoon strength for LWE-affected regions, and **18 Rescue & Relief
Teams** of 35 personnel each for disaster response [N8]. **Female personnel are
deployed at border check posts** for frisking and checks of female travellers,
and to engage local women [N8]. The **"Know Your Area" (KYA)** programme
requires personnel to build in-depth knowledge of local geography, culture and
security risks in their assigned stretch [N8].

Every surveillance mechanism named across the sources reviewed is a person: a
patrol, a naka, an undercover team, a female frisker, an officer who knows the
area — cameras appear only as procurement line-items, never as the described
method of surveillance. This suggests **human presence, not electronic
sensing, is SSB's primary surveillance instrument today**, though this is an
argument from silence in [N1][N2][N8] and should be treated as an assumption
to validate rather than a confirmed fact.

### 3.6 CCTV and Video Technology in Service

**What has been procured.** In answer to Lok Sabha Unstarred Question No. 488
on **3 February 2026**, the Minister of State for Home Affairs stated that SSB
*"has procured the Unmanned Aerial Vehicles, Micro Unmanned Aerial Vehicles,
Hand Held Thermal Imager, **CCTV Surveillance Setup with Automatic Face
Recognition System with Auto Number Plate Recognition** and Satellite phones
for surveillance and modernization of the Force"* [N3]. This is the single most
consequential finding in this document for IBVAP, and it cuts against the
problem statement's premise: the stated gap is that FRS and ANPR "often require
specialized hardware and proprietary solutions" and are therefore not deployed,
yet the named department has already procured a CCTV setup **with** FRS and
ANPR. This is recorded here strictly as a research finding; its product
implication belongs in `docs/02-product/`.

Modernisation funding: SSB was allotted **₹5,001.63 crore** for modernisation
and infrastructure development over 2015-16 to 2025-26, of which **₹4,775.11
crore** had been spent as of the reply date. Separately, under **Modernization
Plan-II, III and IV** from 2013 to 31.03.2026, SSB was allotted **₹241.15
crore** and had spent **₹210.02 crore** [N3]. MHA gave no completion timeline:
*"Modernization of forces and procurement of the latest and State of the art
equipment is an ongoing process. So specific timeline can not be given"* [N3].
Notably, CAPF-wide Modernization Plan IV procurement includes UAVs, Hand Held
Thermal Imagers and satellite phones — but **no video analytics, VMS or CCTV
item** appears in MHA's list of major equipment for the plan [N1]. SSB has also
sent personnel for **Drone Pilot Training** at a DGCA-approved institute, and
for **Special Communication Equipment Training at BSF** [N3].

**Other reported technology.** A 2025 study reports SSB using XBIS scanners,
"Netra" surveillance drones, body-worn cameras, GPS devices, CCTV cameras and
satellite phones, crediting CCTV and satellite phones specifically for
"real-time monitoring and communication in remote areas" [N8] (Nepali thesis,
key-informant sourced; specific product names uncorroborated). Secondary
compilations describe SSB using drones, CCTV surveillance systems, thermal
imagers, night-vision devices, GPS-based patrolling, secure digital
communication and GIS-based planning, and state that CCTV and thermal imaging
at strategic locations have improved day-and-night monitoring [N10][N11][N23]
(news and compilations largely paraphrasing the same MHA reply, i.e. restating
[N3] rather than adding independent evidence). SSB has an **intelligence wing
with ~650 field and staff agents** for actionable intelligence collection on
both borders [N19] (indirect: source returned HTTP 403).

**What is not established.** No source retrieved states how many cameras SSB
operates, where they are (BOP / check post / ICP / battalion HQ), make, model,
resolution, codec, PTZ vs fixed, thermal vs visible, ONVIF conformance, or what
recorder/VMS sits in front of them — this is the top blocking gap in this
document. Where the procured FRS/ANPR CCTV setup is actually deployed, how many
sites, whose software it is, whether it is a single vendor stack, and whether
it exposes any API or open stream is likewise unknown; [N3] names the
capability but not the deployment. Whether cameras exist at ordinary BOPs at
all, or only at check posts, ICPs and "key crossing points," is unclear — [N11]
mentions face recognition at "key crossing points" but is a news paraphrase.
Whether SSB body-worn camera footage [N8] is retained centrally, and would be
in scope for the same analytics and evidence workflow as fixed CCTV, is also
unknown.

### 3.7 Control Rooms and Monitoring Workflow

MHA lists, among national measures for detecting cross-border trafficking,
*"The installation of upgraded Surveillance grid using **AI based features**,
RADARS, Electro Optics Devices, Night Vision Devices, Motion Detectors with
**Integrated Command and Control Centre**"* [N4]. This is the only
primary-source mention of an "Integrated Command and Control Centre" or
AI-based surveillance found in this pass — but the answer is a national
narcotics-control response covering international borders and coastal areas
generally, listed alongside maritime and Coast Guard measures, and it is **not
attributed to SSB or to the Indo-Nepal/Indo-Bhutan borders** specifically. SSB
does maintain an **SSB Wireless & Telecom Training Centre** as a standing
formation [N1][N2], indicating an in-house communications cadre.

**This is a critical gap: no source retrieved in this pass describes an SSB
control room, operations room, video wall, or monitoring roster** — whether SSB
operates control rooms that display live video at all is unknown. This
contrasts with BSF, where "BSF Control Rooms on the border" receiving BOLD-QIT
feeds and cueing Quick Reaction Teams is documented (see
[domain-research.md](domain-research.md) §2.1) — there is no SSB equivalent in
evidence. If SSB monitoring exists, the echelon (BOP / Company / Battalion /
Sector / Frontier / FHQ), operator count, cameras per operator, shift pattern
and standing instructions on seeing something are all unknown, as is whether
any live video reaches echelons above the BOP or whether recording is purely
local and consulted after the fact.

Where monitoring exists at all, it more plausibly resembles something **local
and incidental** — a screen at a post watched by whoever is on duty — rather
than a staffed control room with a monitoring roster. This inference combines
the absence of any control-room description in [N1][N2][N8] with the
check-post/BOP command ranks (§3.3) and the road/power constraints (§3.10); it
is drawn from silence and is the single highest-value assumption in this
document to validate directly with SSB.

### 3.8 Incident Detection, Assessment, and Response

SSB's own digitised incident pathway exists for **seizures**: the **Seizure
Incident Management System (SIMS)** maintains real-time digital records of
seizures and law-enforcement actions, lets field units log incidents instantly,
and gives senior officials insight into smuggling patterns via a centralised
database [N8] (thesis, key-informant sourced — not corroborated by an Indian
primary source in this pass).

Coordination with the Nepali counterpart force is **scheduled, not
event-driven**, at every echelon [N8]:

| Level | Frequency |
|---|---|
| DG/IG | Annually (moved to semi-annually after the 8th meeting) |
| DIG | Quarterly |
| Battalion | Monthly |
| Company / BOP | Fortnightly |

Cross-border coordination meetings totalled **981** over six fiscal years, with
the highest volume at battalion level (448) and local level (248) [N8] (APF
Nepal HQ data). Real-time coordination between the two forces is explicitly
described as inadequate: an SSB officer stated *"there are still gaps in
real-time information exchange that hinder proactive security responses"*
[N8]. SSB's operational output is recorded by MHA as **cases** and **persons
arrested** per category (§3.12) — a case/arrest ledger, not an alarm log [N1].

The actual detection → assessment → response sequence at an SSB BOP is not
described in any source retrieved. The BSF pattern recorded in
[domain-research.md](domain-research.md) §3.2 (sensor → control room → QRT
interception) is BOLD-QIT-specific and must not be assumed to apply to SSB (see
§5). Whether SSB has a Quick Reaction Team construct at all, or whether
response is simply by the patrol or naka already in the field, is unknown, as
is what carries an alert from whoever notices it to whoever responds (radio
net, mobile phone, runner), whether any written SOP governs alarm assessment
and escalation, and response-time expectations from detection to interception.
It is also unclear whether SIMS is fed by hand after the fact or is capable of
ingesting a machine-generated event, and whether it is reachable from a BOP.
Because SIMS is described as a **seizure** system, it likely records
*outcomes*, not *detections* — a camera-derived event that produces no seizure
may have no existing home in it, though this inference rests solely on the
description in [N8].

### 3.9 Command and Control Integration

SSB operates under MHA administrative control; MHA formulates policy, oversees
deployment, ensures coordination with other agencies, and issues periodic
guidelines for border management, intelligence gathering and disaster response
[N8]. Named digital systems in SSB's orbit, from the sources retrieved:

| System | What it is | Source | Confidence |
|---|---|---|---|
| **SIMS** — Seizure Incident Management System | SSB's own real-time digital seizure/incident register with a centralised database | [N8] | Medium — single foreign academic source |
| **CCTV setup with FRS + ANPR** | Procured surveillance stack; scope and vendor unknown | [N3] | High for existence, unknown deployment |
| "Integrated Command and Control Centre" | Named in a national narcotics answer, **not attributed to SSB** | [N4] | High for the statement; unattributable to SSB |
| **EVR** — Online Electronic Vigilance Register | MHA-wide system for IPS officer vigilance profiles — **unrelated to border surveillance** | [N2] | High, and irrelevant — noted only to prevent misidentification |

**What "existing command and control systems" means for SSB is a blocking
unknown.** The problem statement requires integration with such systems, but no
source retrieved names an SSB C2 system, its vendor, protocol, data model or
network reach. SIMS is the only credible candidate found, and it is a seizure
register rather than a C2 system. Which non-SSB stakeholders would consume SSB
video is also unresolved: state police (who take over cases), Customs,
Immigration, LPAI (at ICPs), NCB (narcotics), intelligence agencies, and APF
Nepal (joint patrols) — each a different integration question with a different
legal basis. Any C2 integration on the SSB border must plausibly survive a
**cross-organisational handover**, since SSB's cases are prosecuted by state
police, its narcotics work is coordinated with NCB, and its border counterpart
is a foreign force; integration is therefore as much an interoperability and
authorisation problem as a technical one ([N4] for NCB, [N8] for APF
coordination, §3.11 for the police handover).

### 3.10 Remote-Location Constraints

**Road access — the defining constraint.** **308 of SSB's 734 BOPs** on the
Indo-Nepal and Indo-Bhutan borders **lack proper road connectivity**; only
**426** have it. A consolidated proposal for lateral and axial roads,
foot-tracks and staging camps remains under consideration at MHA, with "large
financial implications" and an uncertain approval timeline [N9] (The Tribune,
17 August 2025). Government has approved construction/upgradation of
**1,299.80 km of roads** along the India-Nepal border in Uttarakhand, Uttar
Pradesh and Bihar [N1][N2] (approved, not stated as complete). **42% of SSB's
border out posts cannot be reached by road** — any hardware placed at those
sites is carried in on foot, and so is every spare part and every technician
visit.

**Power.** Generators have been provided at all BOPs wherever there is no
direct electricity connection, and reverse-osmosis plants installed at all BOPs
for drinking water; the situation varies state to state [N9][N18]. A
parliamentary committee separately noted a lack of electricity at several
BOPs, particularly those of SSB and ITBP [N18] (PRS summary of a Parliamentary
Standing Committee report). At a generator-powered BOP, power is plausibly
scheduled and fuel-limited rather than continuous, and fuel must travel the
same unroaded path as everything else — making a continuously running compute
load a logistics cost, not just an electrical one. This combines the road
finding [N9] with the generator finding [N9][N18]; no measured power budget for
an SSB BOP was found.

**Connectivity.** Satellite phones are part of SSB's procured surveillance and
communication inventory [N3], and CCTV plus satellite phones are credited with
enabling "real-time monitoring and communication in remote areas" [N8]. Their
presence in the surveillance and modernisation inventory suggests that at some
SSB posts satellite is the communications path — high-latency, low-bandwidth
and metered — though the reply does not say which posts or how many. Actual
data connectivity at an SSB BOP (any IP link, bandwidth, symmetry, metering,
reliability, whether shared with voice) is unknown, as is whether SSB has any
dedicated communication backbone comparable to the CIBMS OFC/microwave network.
**No CIBMS-equivalent network is documented for the Indo-Nepal or Indo-Bhutan
border** (§5).

**Terrain and environment.** The SSB border spans **Himalayan territories and
the Indo-Gangetic Plain** [N7]; the Indo-Bhutan stretch traverses rugged
Himalayan terrain and foothills [N14]; the frontiers are described as unfenced
and crossing forests, mountains, rivers and plateaus [N23]. Reserved forests
spanning India into Bhutan are central to conflict, conservation and
displacement processes on that border [N14]. Measured environmental conditions
per sector (fog days, monsoon intensity, temperature range at camera housings,
humidity, lightning) are not available — the earlier domain pass's
environmental findings are drawn from Punjab/Jammu/Assam CIBMS areas, not from
the Himalayan foothills or the Bihar Terai.

**Maintenance and skills.** SSB conducts training when new equipment is
adopted, and has sent personnel for drone-pilot and BSF special-communication
training [N3]. Whether SSB has any in-house cadre able to install, configure
and repair IP camera and analytics infrastructure at a BOP — or whether this
depends on vendors who must reach an unroaded post — is unknown. Software
placed at an SSB BOP plausibly must run unattended for long periods and fail in
a way a Sub-Inspector can recognise and report over radio or satellite phone,
combining the command-rank finding (§3.3) with the road-access (§3.10) and
electricity ([N18]) findings.

### 3.11 Legal and Evidentiary Framework

**Statutory basis.** SSB is constituted under the **Sashastra Seema Bal Act,
2007 (Act No. 53 of 2007)**, enacted 20 December 2007, providing for the
constitution and regulation of an armed force of the Union for ensuring the
security of the borders of India. Its chapters cover the constitution of the
Force and conditions of service, offences, punishment, arrest and proceedings
before trial, **Force Courts** and their procedure, confirmation and revision
of proceedings, execution of sentences, and pardons and remissions [N5]
(indirect — statute text not retrieved). **SSB Rules, 2009** elaborate the
structure and functions: Rule 9 mandates securing border areas, preventing
trans-border crime and illegal activity, regulating unauthorised crossings, and
building trust with local communities through civic action; Rule 10
establishes the hierarchical command structure [N8] (indirect). **The BSF Act,
1968 does not govern SSB** — every legal statement in
[domain-research.md](domain-research.md) §3.5 resting on the BSF Act or BSF
jurisdiction notifications must be re-derived for SSB (§5).

**Jurisdictional belt.** SSB's powers of arrest, search and seizure operate
within **15 km of the international border** in Uttarakhand, Uttar Pradesh,
Bihar, West Bengal, Sikkim, Assam and Arunachal Pradesh, and in any other area
where SSB operates [N8][N17] (thesis citing the SSB Act 2007, corroborated by
news reporting of the enabling notification). **This is not the BSF belt**: the
50 km (Assam, Punjab, West Bengal) and 80 km (Gujarat) figures recorded in
[domain-research.md](domain-research.md) §3.5 come from a 2021 BSF-specific
notification and have no application to SSB. Whether the 15 km figure has been
revised since, and whether it is measured as straight-line distance or along
roads, is unknown.

**Powers under other statutes.** SSB has been conferred powers under the
**Criminal Procedure Code, 1973** (arrest without warrant, search, seizure of
offensive weapons, prevention of cognizable offences), the **NDPS Act, 1985**
(entry, search, seizure and arrest without warrant in narcotics offences), the
**Arms Act, 1959** (demand arms licences, search vessels and vehicles, seize
prohibited arms in disturbed areas), and the **Passport Act, 1967**; extension
under the **Customs Act, 1962** is variously reported as conferred and as under
consideration [N8][N17]. MHA confirms, as a primary source, that SSB (with BSF
and Assam Rifles) is empowered under the NDPS Act, 1985 to carry out search,
seizure and arrest for illicit narcotics trafficking at the international
border [N4]. The **Bharatiya Nagarik Suraksha Sanhita, 2023** replaced the
CrPC, 1973 effective **1 July 2024**; sources describing SSB's powers cite the
CrPC 1973 and pre-date or ignore this change. How SSB's CrPC-derived powers map
onto the BNSS, and whether any fresh notification was required, is unresolved.

**Handover and prosecution.** In practice, apprehended persons and seized items
are handed to the local police station for further legal action, e.g. under
the NDPS Act [N17] (news; corroborated across incident reporting), consistent
with MHA's ledger of SSB output as "Cases" and "Arrested" per category [N1].
Whether SSB registers FIRs or files complaints/charge sheets in its own name in
any category — and whether this differs for NDPS, where the force is a
designated empowered agency, versus ordinary offences — is unknown. The generic
CAPF position that border guarding forces detect and hand over rather than
investigate is documented for BSF [S22] but was not confirmed for SSB in this
pass.

**Evidentiary requirements for recorded video.** Electronic records in India,
including CCTV footage, are governed by **Section 63 of the Bharatiya Sakshya
Adhiniyam, 2023**, in force from 1 July 2024, replacing s.65B of the Indian
Evidence Act, 1872. Admissibility of a copy requires a certificate signed by
the person in charge of the device **and** an expert, disclosing the record's
**hash value** [S29] (force-agnostic Indian law, carried forward from
[domain-research.md](domain-research.md) §3.5 — it applies to SSB exactly as to
BSF). This requirement plausibly lands harder on SSB than on BSF for two
structural reasons: the device custodian at the point of capture is a
Sub-Inspector at a BOP or a Head Constable at a check post (§3.3), and 42% of
BOPs have no road access (§3.10) — so getting either the custodian's or an
expert's signature to a site is a journey. This combines [S29] with
[N1][N8][N9] and is not itself a sourced, observed problem. Current SSB
practice for exporting and handing over footage (format, who signs the
certificate, who is the "expert," whether hashes are computed, retrieval time,
how often footage is used in prosecution) and video retention periods at BOPs,
check posts and ICPs are both unknown.

**Face recognition on a treaty-open border.** SSB has procured a CCTV setup
with Automatic Face Recognition and ANPR [N3]. The population crossing this
border includes Indian and Nepali nationals exercising a treaty right of
movement [N7][N13], and Indian and Bhutanese nationals with freedom of movement
under the 1949/2007 treaty [N14]. Applying face recognition at an open border
therefore processes biometrics of people who are committing no offence and who
have a treaty right to be there, including foreign nationals of a friendly
state — a materially different legal posture from face recognition at a
controlled crossing on a closed border. This juxtaposes [N3] with
[N7][N13][N14]; no legal analysis of this specific situation was found. The
legal basis, authorisation level, retention rules and oversight for this
biometric processing — which authority approves it, under what instrument,
what happens to a template generated from a person never charged, and whether
the Digital Personal Data Protection Act, 2023 (or any exemption under it)
applies — is a high-priority open question (SQ-8). Whether there is any
bilateral understanding with Nepal or Bhutan about surveilling their nationals
at the open border, given the standing coordination architecture (§3.8), is
also unknown.

### 3.12 SSB Operational Event Classes

This is the closest thing to a ground-truth catalogue of what actually happens
on the SSB border: MHA's own record of SSB operational achievements,
**01.01.2023 to 31.03.2024** [N1] (primary — MHA Annual Report 2023-24):

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

The 2022-23 report gives the same category set for 01.04.2022 to 31.12.2022,
with **5,281 arrests/apprehensions of criminals/smugglers/Naxals**, 3,987
cattle, ₹1,42,50,712 Indian currency, ₹1,01,32,021 other currency, 0.5503 kg
gold, 40.634 kg silver, 49 wildlife, 18,554.307 kg narcotics, 39,445 nos.
psychotropic/synthetic drugs, and forest products including 41,768.1620 kg
firewood and 34,822.6511 cft wooden logs [N2].

*Extraction caveat: these values were extracted from the Annual Report PDF's
multi-column layout. Category names and case/arrest pairs are read directly
from the table rows and are reliable; a few free-text seizure-quantity cells
span rows in the source layout and their row assignment is less certain
(notably rows 5–8) — verify against the published PDF before citing a quantity
figure.*

**What this catalogue says about the domain.** There is **no "intrusion,"
"infiltration attempt," "line crossing" or "illegal entry" category** anywhere
in SSB's operational-achievement table [N1][N2] — contrast BSF, for which
"1,104 infiltration attempts detected" is the headline metric (see
[domain-research.md](domain-research.md) §5.1). SSB's operational reality reads
as a **contraband, currency, trafficking and person-of-interest problem**, not
an intrusion-detection problem: the three largest categories by case count are
prohibited/contraband items (5,993), narcotics (1,059) and Indian currency
(471), with human trafficking (316) fourth — though whether this reflects
actual operational priority or simply reporting convention is an inference from
[N1], not a stated fact. **Human trafficking is a first-class SSB event class
with a victim outcome**, not just an arrest outcome — 531 victims rescued in 15
months [N1], backed by dedicated AHTUs [N8], on a border described as a major
trafficking corridor [N23]. Trafficking is plausibly the event class **least**
served by the analytics the problem statement names: a trafficked minor moving
through a check post with an adult produces no intrusion, no unusual vehicle
and no suspicious motion — the signal is relational and behavioural at a
legitimate crossing (not sourced; recorded because it is the gap most likely to
matter to this user). Similarly, the livestock ("cattle," 432 cases) and
forest-product classes suggest that **animals and loaded human porters are
targets, not nuisance alarms** on this border — the nuisance/false-alarm
profile assumed for a fenced border in
[domain-research.md](domain-research.md) §4.2 does not transfer cleanly (based
on [N1]'s categories, not independently measured).

Time-of-day, seasonal and location distribution of any of these categories is
not published — MHA reports totals only. Nor does any source distinguish how
many cases originated from a camera, a patrol, a naka check, or an intelligence
tip-off — this is the SSB version of the GAO "asset assist" measurement gap
(see [domain-research.md](domain-research.md) §4.4).

### 3.13 Terminology Reference

**Organisation**

| Term | Meaning | Source |
|---|---|---|
| **SSB** — Sashastra Seema Bal | CAPF and Border Guarding Force under MHA, responsible for the Indo-Nepal and Indo-Bhutan borders; 92,541 personnel (31.03.2024) | [N1] |
| **Special Service Bureau** | SSB's predecessor, raised post-1962, mandated on border-population morale against subversion, infiltration and sabotage | [N1][N2] |
| **LIA** — Lead Intelligence Agency | SSB's designation for the Indo-Nepal border (Jan 2001) | [N6] |
| **OBOBGF** — One Border, One Border Guarding Force | MHA deployment principle; assigns Nepal and Bhutan borders to SSB | [N2] |
| **FHQ / Frontier / Sector / Battalion / Company / BOP / Check post** | SSB's seven echelons, commanded respectively by DG / IG / DIG / Commandant / Assistant Commandant / Sub-Inspector / Head Constable | [N8] |
| **CI&JWS** | SSB's Counter Insurgency & Jungle Warfare School | [N1] |
| **APF, Nepal** — Armed Police Force | SSB's counterpart on the Nepal side, under the APF Act, 2001; joint patrols with SSB | [N7][N8] |

**Units and programmes**

| Term | Meaning | Source |
|---|---|---|
| **BIT** — Border Interaction Team | 6-member team incl. female personnel, plain clothes, on 25 high-risk routes; intelligence and community engagement | [N8] |
| **AHTU** — Anti-Human Trafficking Unit | SSB has five; 20 nationally established by SSB/BSF under the Nirbhaya Fund | [N8][N2] |
| **SAT** — Small Action Team | Platoon-plus strike element for LWE areas | [N8] |
| **RRT** — Rescue & Relief Team | 18 teams × 35 personnel for disaster response | [N8] |
| **KYA** — Know Your Area | Programme requiring in-depth local geographic, cultural and risk knowledge | [N8] |
| **SIMS** — Seizure Incident Management System | SSB's real-time digital seizure/incident register with centralised database | [N8] |
| **Civic Action Programme (CAP)** | Statutory SSB duty; community engagement in the area of responsibility | [N1][N8] |
| **Naka** | Manned checkpoint on an approach route | [N23] |
| **Area domination patrol** | Patrolling to establish presence across a stretch rather than to react to an alarm | [N23] |

**Places and legal terms**

| Term | Meaning | Source |
|---|---|---|
| **Open border** | The treaty-based visa- and passport-free crossing regime with Nepal (1950 Treaty) and Bhutan (1949/2007 Treaty) | [N7][N13][N14] |
| **ICP** — Integrated Check Post | LPAI-operated land port; Raxaul (2016) and Jogbani (2016) operational on the Nepal border; Rupaidiha and Sunauli under development, Banbasa at land acquisition | [N2][N21] |
| **SSB Act, 2007** | Act No. 53 of 2007; SSB's constituting statute — not the BSF Act, 1968 | [N5] |
| **SSB Rules, 2009** | Rules elaborating structure and duties (Rule 9 duties, Rule 10 command) | [N8] |
| **15 km belt** | The area within which SSB's arrest/search/seizure powers operate, across seven states | [N8][N17] |
| **Force Court** | SSB's internal disciplinary tribunal under the SSB Act, 2007 | [N5] |
| **Third Country (Foreigner)** | SSB offence category for non-Indian, non-Nepali/Bhutanese nationals using the open border | [N1] |
| **FICN** | Fake Indian Currency Notes; a standing SSB seizure category | [N1] |

---

## 4. Implications for IBVAP

These are research-level observations about how the findings bear on the
problem space — not product decisions, which belong in `docs/02-product/`.

- **Intrusion/line-crossing detection does not map cleanly onto SSB's border.**
  MHA's own framing of the problem is "misuse of open border," and SSB's
  21-category achievement ledger has no intrusion class at all (§3.2, §3.12).
  A platform modelled on virtual-fence intrusion alarming would be answering a
  question this force's own reporting does not ask.
- **The problem statement's FRS/ANPR-hardware-gap premise does not hold
  unqualified for SSB**, which has already procured a CCTV setup with FRS and
  ANPR (§3.6). What that premise *does* still hold for — the platform's
  software-only, existing-camera approach versus a dedicated hardware
  appliance — is a distinction to sharpen in product scoping.
- **Human trafficking is a major, currently underserved event class** (531
  victims rescued in 15 months) that behaves nothing like an intrusion or an
  unusual vehicle — it is relational and behavioural at a legitimate crossing
  (§3.12). Any analytics roadmap that only targets intrusion-style detection
  would miss the event class SSB's own data says matters most after contraband.
- **Any interface, alert, or evidentiary workflow must fit a Sub-Inspector at a
  BOP or a Head Constable at a check post** — not a technically trained
  operator (§3.3) — and must survive 42% of BOPs having no road access, for
  installation, maintenance and any evidentiary custodian/expert
  certification under the Bharatiya Sakshya Adhiniyam, 2023 (§3.10, §3.11).
- **Whether SSB monitors live video at all, and through what control-room or
  equivalent workflow, is unresolved** (§3.7). This bears directly on where in
  the operational chain a video analytics platform would even plug in, and is
  the single highest-priority question to resolve directly with SSB before
  further design.
- **Face recognition at an open, treaty-governed border raises a legal
  question not present at a closed or fenced border** — biometric processing
  of people committing no offence and exercising a treaty right of movement
  (§3.11). This is a legal/compliance question, not merely a technical one, and
  precedes any product decision to include FRS.
- **Integration with "existing command and control systems" (per the problem
  statement) has no clearly identified target for SSB.** SIMS is the only
  credible candidate, and it is a seizure register, not a live C2 system
  (§3.9). Product and architecture work should not assume a C2 integration
  point exists until this is resolved.

---

## 5. Risks and Limitations

**Argument-from-silence assumptions.** Several conclusions in this document are
inferences from the *absence* of a description in the sources reviewed, not
from a positive statement — most importantly: that human presence rather than
electronic sensing is SSB's primary surveillance instrument (§3.5); that
monitoring, where it exists, is local and incidental rather than a staffed
control room (§3.7); and that SSB's border density means most of the border is
watched by a person rather than a sensor (§3.4). These are the highest-value
items in this document to validate directly with SSB, since a single
undocumented counter-example would overturn them.

**Source reliability varies.** The highest-confidence material comes from two
MHA Annual Reports and two Lok Sabha Unstarred Question replies, all retrieved
in full text. A large share of structural and echelon-level detail (command
ranks, battalion composition, BIT/AHTU/SAT details, SIMS) rests on a single
2025 Nepali master's thesis based on key-informant interviews [N8] — credible
as an indicative account but not independently corroborated by an Indian
primary source in most cases. Several numeric figures conflict across sources
(BOP counts, sector counts, battalion strength — §3.3, §3.4) and should not be
treated as settled. Three sources could not be retrieved directly (the SSB Act,
2007 text, the official SSB website, and one Deccan Herald report) and are
marked "indirect" at point of use throughout §3.

**Findings from the companion domain document that do not transfer to SSB.**
[domain-research.md](domain-research.md) is heavily BSF/CIBMS-weighted. The
following items from it must not be carried into SSB product, design or
architecture work without re-derivation — the original entries are not wrong,
they are about BSF or about a fenced/closed border, and SSB is neither:

| # | Item in `domain-research.md` | Why it is BSF-specific | What is true for SSB instead |
|---|---|---|---|
| 1 | §1.1/§7.1 — "A BOP is the permanent operational base of the Border Security Force"; the composite-BOP definition | MHA's text defines BOPs as "the main workstation of **the BSF**" [N2] §3.9; the 509 composite BOPs sanctioned in Oct 2023 are 383 Indo-Bangladesh + 126 Indo-Pakistan [S15] — none on SSB borders | SSB has 539 (Nepal) + 195 (Bhutan) BOPs [N1], commanded by a Sub-Inspector, ~3.9 km spacing, 308 of 734 lacking road access [N8][N9] |
| 2 | §1.1 — 3,323 km, Radcliffe Line/LoC/AGPL, 145.876 km unfenced riverine | Entirely the India-Pakistan border | SSB's borders are 1,751 km (Nepal) + 699 km (Bhutan), unfenced throughout, and legally open [N1][N7][N14] |
| 3 | §1.1/§5.5 — ICP observation towers "manned by BSF personnel" | Both cited surveys [S6][S7] are India-Bangladesh field surveys | Who mans India-Nepal ICPs (Raxaul, Jogbani) and who owns the CCTV is unknown (Open Question) |
| 4 | §1.3 — CIBMS, BOLD-QIT, smart fencing, laser walls, BFSR, UGS, aerostats | All India-Pakistan/India-Bangladesh programmes; [N1]'s India-Nepal/Bhutan paragraphs mention only roads and BOP counts | No CIBMS-equivalent programme is documented on the SSB borders; only an unconfirmed laser-fence proposal at Sonauli [N23] |
| 5 | §1.3/§6.2 — the dedicated CIBMS communication backbone (OFC, microwave, DMR, satcom) | BOLD-QIT/CIBMS infrastructure | SSB has satellite phones in inventory [N3]; no dedicated backbone documented; BOP bandwidth unknown |
| 6 | §1.3 — "~5,000 BSF body-worn cameras along the Bangladesh border" | BSF, Bangladesh border | SSB reportedly uses body-worn cameras [N8]; count and retention scope unknown |
| 7 | §2.1/§3.2 — "BSF Control Room" cueing QRTs; sensor → control room → QRT chain | Documented for BOLD-QIT specifically [S3][S21] | No SSB control room or QRT construct is documented; do not assume this chain (§3.7) |
| 8 | §2.1/§7.1 — "~290,000 BSF personnel across 192 battalions"; echelons framed as BSF's | BSF figures | SSB: 92,541 personnel, 6 Frontiers, 18 Sectors, 73 battalions (55 operational + 18 reserve) [N1][N8]; echelon *names* are shared, counts and rank are not |
| 9 | §3.5 — "BSF cannot register an FIR … handover within 24 hours" under the BSF Act, 1968 | The BSF Act, 1968 does not govern SSB | SSB is constituted under the SSB Act, 2007 [N5], with CrPC/BNSS, NDPS, Arms and Passport Act powers [N8][N17]; whether SSB may register an FIR is unknown |
| 10 | §3.5/§6.6 — the 50 km (Assam/Punjab/WB) and 80 km (Gujarat) jurisdictional belt | A 2021 BSF-specific notification | SSB's belt is 15 km, across seven states [N8][N17] |
| 11 | §4.2 — nuisance-alarm profile (livestock, wildlife, vegetation, civilian activity as noise) | Framed for a fenced border with a sterile zone | On SSB's border, cattle (432 cases), forest products (398) and wildlife (78) are seizure *targets*, not noise [N1]; lawful civilian crossing is constant |
| 12 | §5.1/§5.2 — infiltration-attempt counts, ₹461.07 crore contraband, cattle trade to Bangladesh, Majhdia bunkers | India-Bangladesh border statistics | Use [N1]'s SSB achievements table (§3.12) as the SSB event baseline instead — it has no infiltration category |
| 13 | §5.3 — drone incursions (245–294 drones, Punjab as epicentre) | India-Pakistan border, Punjab | No drone-incursion event class is documented on SSB borders; SSB operates UAVs itself [N3] as a capability, not a threat |
| 14 | §5.4 — cross-border tunnels | India-Bangladesh/India-Pakistan | Not documented on SSB borders |
| 15 | §6.1/§6.3 — power/environmental findings (BADP electrification, Punjab/Jammu fog, western desert dust, char-land conditions) | Drawn from CIBMS deployment areas | SSB-specific: generators at all BOPs without a grid connection, varying by state [N9][N18]; terrain is Himalayan foothills to Indo-Gangetic plain [N7][N14]; sector-level environmental data unknown |
| 16 | §4.4 — the GAO "asset assist" measurement gap | A US finding, applied by analogy to BSF | Applies to SSB too — [N1] records cases and arrests but never how a case was detected — but should be re-grounded on SSB's own reporting |

One item transfers unchanged: **Section 63 of the Bharatiya Sakshya Adhiniyam,
2023** and its hash-value certificate requirement [S29] is force-agnostic
Indian evidence law and applies to SSB video exactly as to BSF video (§3.11).
The peer-reviewed operator-vigilance findings (domain-research.md §4.1
[S9][S10]) and the technology-performance bounds on FRS, ANPR and i-LIDS
(domain-research.md §6.7 [S25][S26][S27]) are also force-agnostic, though
whether they apply to SSB depends on whether SSB has monitoring operators at
all (§3.7, Open Question SQ-3).

---

## 6. Open Questions and Research Gaps

None of the following are answered by the sources reviewed in this pass.
Ordered by how much the answer would change subsequent stages.

**Highest priority — block product scoping**

- **SQ-1.** What is SSB's actual installed CCTV base? Count and location by
  node type (BOP / check post / ICP / battalion HQ), make, model, resolution,
  codec, PTZ vs fixed, thermal vs visible, ONVIF conformance, age. (§3.6)
- **SQ-2.** Where is the procured FRS/ANPR CCTV setup deployed, and what is it
  — vendor, site count, single stack or many, whether it exposes streams or
  APIs, and what it is used for today. (§3.6)
- **SQ-3.** Does SSB monitor live video at all, and if so at which echelon?
  Operators per room, cameras per operator, shift pattern, standing
  instructions. (§3.7)
- **SQ-4.** What is the actual detection → assessment → response sequence at
  an SSB BOP and at a check post — is there a written SOP or Standing Order?
  (§3.8)
- **SQ-5.** What is SIMS, technically — owner, hosting, data model, whether it
  is reachable from a BOP, and whether it can accept a machine-generated
  event? (§3.9)
- **SQ-6.** What are the "existing command and control systems" for SSB, by
  name, with interfaces? If SIMS is the answer, confirm it; if not, identify
  the alternative. (§3.9)
- **SQ-7.** What does "suspicious activity" mean on an open border where
  crossing itself is lawful? The problem statement names this capability; on
  this border the question is materially harder than on a fenced one. (§3.2)

**High priority — shape the problem**

- **SQ-8.** What is the legal basis, authorisation level, retention rule and
  oversight for face recognition applied to Indian, Nepali and Bhutanese
  nationals exercising a treaty right of movement? Does the DPDP Act, 2023
  apply? (§3.11)
- **SQ-9.** Of the 308 road-inaccessible BOPs, how many have cameras today,
  and how is anything electronic maintained there? (§3.4, §3.10)
- **SQ-10.** What is the real power budget at a generator-powered SSB BOP:
  hours per day, generator rating, fuel resupply interval, any solar/battery?
  (§3.10)
- **SQ-11.** What data connectivity exists at an SSB BOP — any IP link, its
  bandwidth, symmetry, metering, reliability — and how many posts are on
  satellite? (§3.10)
- **SQ-12.** Does SSB have a QRT construct, or is response by the patrol/naka
  already in the field? What carries the alert to them? (§3.8)
- **SQ-13.** What retention period applies to SSB video, and what is the
  current export-and-handover procedure to state police? Does it satisfy
  s.63 BSA — who signs, who is the "expert," is a hash computed? (§3.11)
- **SQ-14.** Who owns and operates the CCTV at ICP Raxaul and ICP Jogbani, and
  does SSB have access? (§3.4)
- **SQ-15.** How many SSB check posts and naka points exist, and how many have
  a camera? (§3.4)
- **SQ-16.** Do SSB's CrPC-derived powers carry over cleanly to the BNSS,
  2023, and does SSB register FIRs in any category? (§3.11)

**Medium priority — validate assumptions in this document**

- **SQ-17.** Is "human presence is the primary surveillance instrument"
  correct, or is there camera-led monitoring not described in any public
  source? (§3.5)
- **SQ-18.** What is the real nuisance-alarm profile on this border, given
  that cattle and porters are targets rather than nuisances? (§3.12)
- **SQ-19.** Reconcile the conflicting BOP counts: 539+195 [N1] vs 474+131
  [N23] vs the thesis's 295 [N8] — which definition of "BOP" does each use?
  (§3.4)
- **SQ-20.** Reconcile the conflicting Sector HQ count (18 in [N1] vs 15 in
  [N23]) and battalion strength (1,000 vs 1,172). (§3.3)
- **SQ-21.** Is the Sonauli laser-fence proposal [N23] real, and what became
  of it? (§3.4)
- **SQ-22.** Does SSB retain body-worn camera footage centrally, and is it in
  the same evidentiary and analytics scope as fixed CCTV? (§3.6)
- **SQ-23.** Which stakeholders beyond SSB would consume this video — state
  police, Customs, Immigration, LPAI, NCB, intelligence agencies — and is
  there any question about APF Nepal? (§3.9)
- **SQ-24.** Measured environmental conditions on the SSB borders
  specifically: Terai fog and monsoon, Himalayan foothill conditions,
  temperature range at camera housings. (§3.10)
- **SQ-25.** Is the Indo-Bhutan border operationally the same problem as the
  Indo-Nepal border, or a different one? MHA's challenge statement is
  verbatim identical for both [N1], which may reflect drafting convention
  rather than operational sameness.

**Research-process gaps**

- **SQ-26.** Retrieve the Sashastra Seema Bal Act, 2007 and SSB Rules, 2009
  text directly — both India Code and the MHA-hosted PDF returned HTTP 403 in
  this pass; §3.11 currently rests on a Nepali thesis's reading of them.
- **SQ-27.** Retrieve the official SSB website — `ssb.nic.in` does not
  resolve and `ssb.gov.in` returned no navigable content; the force's own
  statement of its organisation and charter has not been read directly.
- **SQ-28.** Retrieve the MHA Annual Report 2024-25 or later, if published,
  for updated BOP counts, strength and the SSB achievements table (this pass
  used 2022-23 and 2023-24).
- **SQ-29.** Find any Parliamentary Standing Committee on Home Affairs report
  specifically on SSB, and any CAG audit of SSB modernisation procurement —
  the likeliest sources for the installed-camera-base question (SQ-1).
- **SQ-30.** Record the SIH organisation/department field for PS 26187 in
  `docs/00-project/`, so the SSB attribution this document rests on is itself
  documented (see the attribution caveat in §1).
- **SQ-31.** Confirm the seizure-quantity cells in the §3.12 tables against
  the published Annual Report PDFs — the multi-column extraction leaves some
  row assignments uncertain.

---

## 7. Conclusions

This pass establishes SSB as a force whose operational reality differs from
the BSF/CIBMS-weighted domain picture in ways that matter for a video
analytics platform: an open, treaty-governed border where crossing itself is
lawful; an operational ledger built around contraband, currency and
trafficking rather than intrusion counts; a command structure that puts an
SI or Head Constable at the point of camera capture; a road network that
cannot reach 42% of BOPs; and a legal basis (SSB Act, 2007, 15 km belt) wholly
distinct from BSF's. Two findings in particular — that SSB's border is legally
open rather than a line to be defended, and that SSB has already procured
FRS/ANPR-equipped CCTV — bear directly on how the problem statement's named
capabilities map onto this department. Both are recorded here strictly as
research findings; acting on them belongs to `docs/02-product/`.

The assumptions identified throughout this document (§5) require validation
before they are relied on, and the open questions in §6 are the input to the
next research passes (users, competitors, technology), with **SQ-1 through
SQ-7** blocking product scoping and **SQ-26 through SQ-31** being
research-process debts this pass incurred.

---

## 8. References

Reliability key: **P** = primary/official, **A** = academic or peer-reviewed,
**T** = think-tank/policy analysis, **N** = news, **V** = vendor or trade,
**E** = encyclopedic/tertiary.

| ID | Source | Type | Retrieval | URL |
|---|---|---|---|---|
| N1 | **MHA Annual Report 2023-24** — Ch. 3 (Border Management: India-Nepal §3.26–3.27, India-Bhutan §3.28) and Ch. 7 (SSB §7.51–7.53, achievements 01.01.2023–31.03.2024) | P | Direct (full text) | https://www.mha.gov.in/sites/default/files/AnnualReport_27122024.pdf |
| N2 | **MHA Annual Report 2022-23** — Ch. 3 (border lengths, OBOBGF, BOP definition §3.9, ICP tables §3.54–3.55) and Ch. 7 (SSB §7.53–7.55, AHTU figures) | P | Direct (full text) | https://www.mha.gov.in/sites/default/files/AnnualReportEngLish_11102023.pdf |
| N3 | **Lok Sabha Unstarred Question No. 488**, answered 03.02.2026 — *Modernization of Sashastra Seema Bal*; reply of MoS Home Shri Nityanand Rai | P | Direct (full text) | https://www.mha.gov.in/MHA1/Par2017/pdfs/par2026-pdfs/LS03022026/488.pdf |
| N4 | **Lok Sabha Unstarred Question No. 634**, answered 03.02.2026 — *Seizure of Narcotic Substances*; SSB NDPS empowerment, and the "AI based features … Integrated Command and Control Centre" measure | P | Direct (full text) | https://www.mha.gov.in/MHA1/Par2017/pdfs/par2026-pdfs/LS03022026/634.pdf |
| N5 | **Sashastra Seema Bal Act, 2007** (Act No. 53 of 2007, enacted 20.12.2007) — indirect: India Code and the MHA-hosted PDF both returned HTTP 403 | P | Indirect | https://www.indiacode.nic.in/handle/123456789/2039 |
| N6 | Wikipedia — *Sashastra Seema Bal* (mandate, border assignment dates, echelon composition, LIA designation) | E | Direct | https://en.wikipedia.org/wiki/Sashastra_Seema_Bal |
| N7 | Wikipedia — *India–Nepal border* (length, terrain, open border, unfenced, guarding forces, joint patrols, ICP list, disputes) | E | Direct | https://en.wikipedia.org/wiki/India%E2%80%93Nepal_border |
| N8 | **Silwal, Bishal (April 2025)** — *Deployment Practices of APF, Nepal and SSB along Nepal-India Border*. Master's thesis, APF Command and Staff College, Faculty of Humanities and Social Sciences, Tribhuvan University. Supervisor: Assoc. Prof. Dr. Tikaram Gautam. Based on 7 KIIs and 2 FGDs incl. SSB officers, Jan–Feb 2025 | A | Direct (full text) | https://elibrary.tucl.edu.np/JQ99OgQIizUxyjI9nB0on9OyLkqsGIf4/api/core/bitstreams/7f5c9881-3446-46fd-9518-9c03f865f7c8/content |
| N9 | The Tribune — *308 SSB outposts on Nepal, Tibet borders await road connectivity*, Animesh Singh, 17 Aug 2025 (BOP road connectivity; generators and RO plants at BOPs) | N | Direct | https://www.tribuneindia.com/news/india/308-ssb-outposts-on-nepal-tibet-borders-await-road-connectivity |
| N10 | ThePrint — *SSB, guarding Nepal, Bhutan borders, equipped with state-of-the-art surveillance equipment: Govt* (reports the [N3] reply) | N | Direct | https://theprint.in/india/ssb-guarding-nepal-bhutan-borders-equipped-with-state-of-the-art-surveillance-equipment-govt/2844824/ |
| N11 | Indian Masterminds — *From Drones to AI Eyes: How Sashastra Seema Bal Is Reinforcing India's Nepal-Bhutan Border Security* (reports the [N3] reply; adds "at key crossing points" framing) | N | Direct | https://indianmasterminds.com/news/sashastra-seema-bal-nepal-bhutan-border-surveillance-systems-182910/ |
| N12 | News On Air (Prasar Bharati) — HM Amit Shah at SSB's 61st Raising Day, 20 Dec 2024 ("protecting fenced borders is much easier than protecting an open border") | P/N | Direct | https://www.newsonair.gov.in/hm-amit-shah-joins-ssbs-61st-raising-day-in-west-bengal |
| N13 | India–Nepal Treaty of Peace and Friendship, 31 July 1950 — free movement, residence, property and commerce provisions | E | Direct | https://en.wikipedia.org/wiki/India%E2%80%93Nepal_Treaty_of_Peace_and_Friendship |
| N14 | Bhutan–India border and India–Bhutan Treaty of Friendship 1949 (revised 2007); freedom of movement; Bhutan's 23 Sep 2022 permit restriction; reserved forests | E | Direct | https://grokipedia.com/page/Bhutan%E2%80%93India_border |
| N15 | ThePrint — *Govt sanctions 12 new SSB battalions to fortify Nepal, Bhutan borders, tri-junction area* | N | Direct | https://theprint.in/defence/govt-sanctions-12-new-ssb-battalions-to-fortify-nepal-bhutan-borders-tri-junction-area/615268/ |
| N16 | Swarajya — *SSB Operationalises 72 Outposts Along Nepal, Bhutan Borders* (18 in Sikkim and Arunachal Pradesh) | N | Direct | https://swarajyamag.com/insta/doklam-aftermath-strengthening-its-defences-ssb-operationalises-72-outposts-along-nepal-bhutan-borders |
| N17 | DNA India — *Sashastra Seema Bal gets powers of search, arrest and seizure* (CrPC/NDPS/Arms/Passport Acts; 15 km belt across seven states; Customs Act contemplated) | N | Direct | https://www.dnaindia.com/india/report-sashastra-seema-bal-gets-powers-of-search-arrest-and-seizure-1356284 |
| N18 | PRS Legislative Research — report summary, *Working Conditions in Border Guarding Forces* (Parliamentary Standing Committee; lack of electricity at SSB and ITBP BOPs) | T/P | Direct | https://prsindia.org/policy/report-summaries/working-conditions-in-border-guarding-forces |
| N19 | Deccan Herald — SSB intelligence wing operationalised, ~650 field and staff agents — indirect: HTTP 403 | N | Indirect | https://www.deccanherald.com/india/ssb-intel-wing-operationalise-monday-2025041 |
| N20 | News On Air (Prasar Bharati) — *NCB, SSB to strengthen anti-drug trafficking operations on Indo-Nepal border* | P/N | Direct | https://www.newsonair.gov.in/ncb-ssb-to-strengthen-anti-drug-trafficking-operations-on-indo-nepal-border |
| N21 | CSEP / LPAI — Riya Sinha, *Linking Land Borders: India's Integrated Check Posts* (origin of the four India-Nepal ICPs; 2003 NSCS assessment) | T | Direct | https://www.lpai.gov.in/sites/default/files/2021-10/WP_Linking-land-borders-ICP-1.pdf |
| N22 | *(reserved — AHTU/Nirbhaya Fund figures are cited from [N2])* | — | — | — |
| N23 | Secondary compilations of SSB role and structure — GKToday, Model Diplomat, Grokipedia, Military Wiki, Information Array and similar. Used only for items no better source covered: naka/area-domination/joint-check-post vocabulary, the 474+131 BOP figures, the 15-sector figure, the 1,172 battalion strength, the Sonauli laser-fence proposal, and the trafficking-corridor framing. Low confidence throughout — every figure from this row is flagged as conflicting or unconfirmed at point of use | E | Direct | https://grokipedia.com/page/Sashastra_Seema_Bal |

**Carried forward from [domain-research.md](domain-research.md)**, cited here
by its IDs: `[S3]`, `[S6]`, `[S7]`, `[S9]`, `[S10]`, `[S15]`, `[S21]`, `[S22]`,
`[S25]`, `[S26]`, `[S27]`, `[S29]`. See that document's §9 for full entries.

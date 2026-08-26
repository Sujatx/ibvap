# SSB Operational Workflow — Research Report

**Stage:** 01 — Research → Domain
**Date:** 2026-08-24
**Scope:** Establish, from primary and authoritative sources, the real SSB
organisational hierarchy and the real surveillance / CCTV / incident workflow
— as opposed to reconstructing one from secondary sources.

This document establishes SSB's real organisational hierarchy and its real
surveillance/CCTV/incident workflow from primary and authoritative sources, to
ground later product scoping in `docs/02-product/` (per
[CLAUDE.md](../../../CLAUDE.md) §2).

**Companion documents**
- [domain-research.md](domain-research.md) — generic border-CCTV domain, BSF/CIBMS-weighted.
- [ssb-operational-context.md](ssb-operational-context.md) — the earlier SSB
  layer. This document corrects three of its findings (§1).
- [product-discovery.md](../users/product-discovery.md) — user/job discovery
  that depends on the questions this pass tried to answer.

## Contents

1. [Executive Summary](#1-executive-summary)
2. [Research Objective & Scope](#2-research-objective--scope)
3. [Key Findings](#3-key-findings)
4. [Detailed Findings](#4-detailed-findings)
5. [Implications for IBVAP](#5-implications-for-ibvap)
6. [Risks / Limitations](#6-risks--limitations)
7. [Open Questions / Research Gaps](#7-open-questions--research-gaps)
8. [Conclusions](#8-conclusions)
9. [References](#9-references)

---

## 1. Executive Summary

This pass retrieved the SSB Act, 2007, the SSB Rules, 2009, the MHA Annual
Report 2024-25, SSB's own website/API, a BPRD project report, and several
parliamentary answers, in full and in primary form. It closes the hierarchy
question that earlier research (`ssb-operational-context.md`) had answered
only from a foreign master's thesis, and it names SSB's six Frontiers,
confirms the DG→ADG→IG→DIG→Commandant command chain, and fixes the statutory
task charter (Rule 9(1)).

It does **not** close the CCTV, control-room or incident-workflow question.
After an exhaustive, documented search across statutes, annual reports,
parliamentary answers, court records, tender feeds and a government project
report, **no source describes an SSB control room, monitoring roster, video
wall, or detection→escalation→response sequence.** This absence is treated as
a finding, not a gap to paper over: §6 argues it is structural (the
documents that would answer it are internal orders that are not published),
not an artefact of insufficient searching.

Three findings from the earlier SSB pass are corrected here:

1. **SIMS is not an SSB system.** It is the MHA/NCB "Seizure Information
   Management System," a national NDPS drug-seizure e-portal launched in
   2019, to which SSB is one of several contributing agencies `[W5]`. It is
   eliminated as a candidate for "existing command and control systems."
2. SSB's achievements table **does** contain an infiltration category in AR
   2024-25 — "Illegal Infiltrators (Foreigner)," 24 cases, 30 arrested — unlike
   AR 2023-24, which had none `[W3]`.
3. Posted strength is **94,202** (as on 31.12.2024), and the official SSB
   website is reachable and serves a public JSON API `[W3][W4]`, correcting a
   stale figure and a "not navigable" finding from the earlier pass.

**Headline conclusion:** the organisational hierarchy and statutory task
charter are now well evidenced. The surveillance/CCTV/incident operational
workflow is not, and — per the structural argument in §6 — is unlikely to
become evidenced through further desk research. Later stages should treat
this as an open question requiring primary access (RTI, interview, or a
partner relationship with SSB), not as something a sharper web search will
resolve.

---

## 2. Research Objective & Scope

The goal was to determine, from primary and authoritative sources, SSB's real
organisational hierarchy (who commands whom, at what echelon) and its real
surveillance/CCTV/incident workflow (who watches video, who is alerted to an
event, and how it escalates) — replacing the reconstruction in
`ssb-operational-context.md`, which relied heavily on a Nepali master's
thesis and secondary sources.

Sources consulted directly and in full include: the SSB Act, 2007 `[W1]`; the
SSB Rules, 2009 `[W2]`; MHA Annual Report 2024-25 `[W3]`; SSB's official
website and its public JSON API `[W4]`; Lok Sabha Unstarred Question 459 of
20.07.2021 `[W5]`; a BPRD/National Police Mission project report on
integrated border management `[W7]`; and SSB's own 280-record tender feed
`[W4]`. Additional searches covered court records (Indian Kanoon), CAG
reports, Parliamentary Standing Committee reports, third-party tender
aggregators, and SSB's own Frontier e-magazines. Results — including negative
ones — are recorded in §6 and §7.

This document makes no product, design, architecture or technology
decisions, and proposes no IBVAP user hierarchy or workflow.

---

## 3. Key Findings

- **The command chain is DG → ADG → IG → DIG → Commandant**, with
  responsibility at each level above battalion defined by "the area that may
  be assigned" (SSB Rules r.9(2)); superintendence sits with the Central
  Government, command with the Director-General (SSB Act §5) `[W1][W2]`.
- **The statutory rank ladder is fixed and complete** (Rules r.8(1)): DG, ADG,
  IG, DIG, Commandant, 2-i-C, Dy Comdt, AC / Subedar Major, Inspector, SI, ASI
  / HC, Naik, L/Naik / Constable, Enrolled followers `[W2]`.
- **Frontier = IG, Sector = DIG, Battalion = Commandant**, consistent with
  Rule 9(2) and observed directly in SSB's own publications `[W2][W4][W8]`.
- **Frontier, Sector, Company, Platoon and Border Out Post are administrative
  constructs, not statutory formations.** Only "battalion" and "unit" are
  constituted by the Central Government; the rest exist under the DG's Rule
  9(4) discretion and are defined in internal orders that are not public
  `[W1][W2]`.
- **The statutory task (Rule 9(1))** is: safeguard the assigned borders and
  promote a sense of security among the border population; prevent
  trans-border crime, smuggling and illegal activity; prevent unauthorised
  entry and exit; carry out civic action. **Surveillance, cameras, sensors and
  monitoring are not named anywhere in the Act or the Rules** `[W1][W2]`.
- **No description of an SSB control room, video wall, monitoring roster or
  operator establishment was found anywhere** — not in the statutes, three
  consecutive MHA Annual Reports, parliamentary answers, the BPRD report,
  SSB's own site, court records, or six tender aggregators. CIBMS — MHA's
  integrated sensor/C2 programme — is explicitly confined to the
  India-Pakistan and India-Bangladesh borders and does not extend to SSB's
  Nepal/Bhutan borders `[W3]`.
- **SSB has procured "CCTV Surveillance Setup with Automatic Face Recognition
  System with Auto Number Plate Recognition"** `[N3]`, but nothing states
  where, how many sites, whose product, or who operates it — and the purchase
  appears in no tender feed searched in this pass (SQ-W2).
- **SSB's own tender feed (280 records, Oct 2025–Aug 2026) contains zero
  tenders for CCTV, cameras, VMS, video analytics, FRS, ANPR, a control room
  or a command centre.** It is dominated by BOP civil works (fencing, sentry
  posts, barracks) and off-grid solar power `[W4]`.
- **The detection → assessment → escalation → response sequence for a border
  event is undocumented.** Every verified SSB reporting instrument is
  outcome-shaped (a case, an arrest, a seizure) or discipline-shaped (a
  death, a loss, a change of command) — none records a detection `[W1][W2][W3][W7]`.
- **Handover to local police is SSB's terminal step**, and the receiving
  agency is documented by a government report as under-resourced for these
  cases `[W7]`.
- **SIMS is eliminated as a candidate SSB command-and-control system**; no
  replacement candidate was found. What "existing command and control
  systems" means for SSB, which the SIH problem statement requires
  integrating with, remains unanswered.

---

## 4. Detailed Findings

### 4.1 Organisational hierarchy

**Statutory basis.** The SSB Act, 2007 (Act No. 53 of 2007, assented
20.12.2007) constitutes "an armed force of the Union for ensuring the
security of the borders of India" (§4(1)) `[W1]`. Superintendence, direction
and control vest in the Central Government; command and supervision vest in
a Director-General, assisted by "such number of Additional
Directors-General, Inspectors-General, Deputy Inspectors-General, Additional
Deputy Inspectors-General, Commandants and other officers" (§5) `[W1]`. The
SSB Rules, 2009 were made under §155 of the Act `[W2]`.

**Rank structure** (Rules r.8(1)) `[W2]`:

| Category | Ranks, in order |
|---|---|
| (a) Officers | Director-General · Additional Director-General · Inspector-General · Deputy Inspector-General · Commandant · Second-in-Command · Deputy Commandant · Assistant Commandant |
| (b) Subordinate Officers | Subedar Major · Inspector · Sub-Inspector · Assistant Sub-Inspector |
| (c) Under Officers | Head Constable · Naik · Lance Naik |
| (d) Enrolled persons other than Under Officers | Constable · Enrolled followers |

"Additional Deputy Inspector-General" is defined in the Act (§2(g)) and named
in §5(2) but does not appear in this Rule 8(1) list `[W1][W2]`. Rule 8(3)–(4)
lets the DG grant a "local rank" carrying command powers of that rank but no
extra pay or seniority `[W2]`.

**Command responsibility** (Rules r.9(2)) `[W2]`:

| Rank | Responsibility extends to |
|---|---|
| Additional Director-General | all battalions, units, headquarters, establishments and personnel placed under him, within the area assigned |
| Inspector-General | same, within the area assigned |
| Deputy Inspector-General | battalions, units and personnel placed under him, within the area assigned |
| Commandant | the battalion or unit placed under him, within the area assigned |

Command not placed under a DIG or IG "shall be carried out by such officers
and in such manner as may be laid down by the Director-General from time to
time" (r.9(4)) `[W2]`. An officer appointed to command has power over all
officers and men "irrespective of seniority" (r.10(1)); if he cannot exercise
it, command devolves to the Second-in-Command, then an officiating officer,
then the senior-most officer present, whose assumption of command "shall be
immediately reported to the next higher authority" (r.10(2)) `[W2]`.

**Sub-battalion echelons — what the statute actually says.** This is the
most important hierarchy correction in this pass, since the earlier pass
rested it on a Nepali master's thesis. SSB Act §56(3)–(4) gives command power
over an outpost to "a Deputy Commandant or an Assistant Commandant,
commanding a company or a detachment or an outpost," or to "a subordinate
officer not below the rank of Sub-Inspector who is commanding a detachment or
an outpost" `[W1]`. This sets a statutory floor (not below SI) and ceiling (Dy
Comdt/AC), not a fixed norm — so the thesis-sourced claim that a BOP is
commanded by a Sub-Inspector `[N8]` is consistent with the statute but not
required by it. The normal (as opposed to permitted) rank of a BOP in-charge,
check-post in-charge, or platoon commander, and whether it varies by
frontier, terrain or BOP category, remains unknown.

**What is not statutory.** The words "Frontier," "Sector," "Company,"
"Platoon" and "Border Out Post" do not appear as constituted formations
anywhere in the Act or Rules — the only formations the statute constitutes
are the "battalion" (§2(b)) and the "unit" (§2(y)) `[W1][W2]`. The statute's
own operational vocabulary is picket, patrol, guard, sentry, post, party,
detachment, outpost, company, camp, quarters, Force lines (e.g. §2(a)(ii),
§22(g), §30(a)) `[W1]`. Frontier, Sector, Company, Platoon and BOP are
therefore read as administrative/deployment constructs created under the
DG's Rule 9(4) authority — reorganisable without amending the Act, and
defined in internal SSB orders that are not public.

**Administrative structure.** Per MHA Annual Report 2024-25 §7.51, SSB is
deployed on the Indo-Nepal border (1,751 km) and the Indo-Bhutan border (699
km), with posted strength 94,202 (as on 31.12.2024) `[W3]`:

| Formation | Count |
|---|---|
| Force Headquarters | 1 |
| Frontiers | 6 |
| Sectors | 18 |
| Battalions | 73 |
| Recruit Training Centres | 4 |
| Central Training Centres | 2 |
| SSB Academy | 1 |
| Wireless & Telecom Training Centre | 1 |
| Dog Training & Breeding Centre | 1 |
| Composite Hospitals | 3 |
| Central Store Depot & Workshop | 1 |
| Sub-CSDs | 3 |
| Medical Training Centre | 1 |
| Counter Insurgency & Jungle Warfare School | 1 |
| "G" School | 1 |

All counts are unchanged from AR 2023-24 `[N1]`. The six Frontiers, named
from SSB's own website API `[W4]` — superseding earlier tertiary sources that
still assert only three (Lucknow, Patna, Guwahati) — are: **Ranikhet,
Lucknow, Patna, Siliguri, Guwahati, Tezpur.**

Force Headquarters sits at East Block-V, R.K. Puram, New Delhi – 110066,
with a Directorate-General and an IG (Admn) `[W6]`. An IG (Operations) post
exists at FHQ, evidenced by a BPRD/MHA report referencing "IG (Ops), SSB"
furnishing trans-border-crime case data, and "Addl. DsG, In-charge of
operations of BSF and SSB" `[W7]`. Frontier commanders hold IG rank (e.g. "IG,
SSB, Frontier Patna," per SSB's own circulars) `[W4]`; Sector commanders hold
DIG rank (e.g. "Deputy Inspector General, SSB, Gorakhpur," per PTI, which
also corroborates Rule 9(2)(c)'s DIG-over-battalions responsibility) `[W8]`.
The Frontier → Sector HQ → Battalion → BOP addressing scheme is visible
directly in SSB's own tender feed, e.g. "BOP Bongling of 38 Bn SSB Tawang
under FTR Hqrs SSB [Tezpur]" and "BOP Jiti, SHQ Jalpaiguri" `[W4]`. Battalions
and stations observed in the Oct 2025–Aug 2026 feed include 3 & 70
(Lakhimpur Kheri), 6 (Ranighuli/Bongaigaon/Guwahati), 18, 23, 25 (Ghitorni,
Delhi), 27, 30, 31, 37, 38 (Tawang), 45 (Birpur), 52 (Araria), 56 (Bathnaha),
57 (Sitarganj), 67 (Lungla), plus 9–14, 17, 20, 34, 36, 39, 42, 43, 46, 53,
55, 59, 62, 68, 69 and 73 `[W4][W9]`. Platoons exist as a deployment unit with
a named "Commander" — evidenced incidentally by a Delhi court record for an
internal-security guard deployment (R&AW training institute, Gurgaon), not a
border task `[W10]`.

The authoritative Frontier→Sector→Battalion order of battle, which Frontier
holds which Sectors, and which battalions sit on the Nepal border versus the
Bhutan border versus internal-security deployments (J&K, Assam, LWE areas of
Chhattisgarh/Jharkhand/Bihar `[W3]`) remains unknown. So does whether the
widely quoted "7 companies per battalion, 3 BOPs per company" `[N6]` is a
sanctioned establishment or a tertiary-source generalisation — nothing in
`[W1][W2][W3][W4]` states it.

**Cadres.** SSB's recruitment-rules index lists: GD, Communication,
Veterinary, Tech (Armament), Ministerial, MT, Engineering, Tradesman, Judge
Attorney (JAG), Hindi Translator, Medical, Mountaineering, Ordnance, CIOA
`[W4]`. The Communication cadre is combatised (Group 'A' down to Constable)
and supported by a standing Wireless & Telecom Training Centre `[W3][W4]`. No
IT, computer, cyber, data, video, surveillance or electronics cadre appears
in the list — the nearest are Communication (wireless/telecom) and Tech
(Armament) `[W4]`. If any SSB cadre is structurally responsible for
installing, operating and maintaining IP video infrastructure at a post, it
is most likely the Communication cadre, whose training establishment is a
wireless-and-telecom school rather than an IT school — noting that BSF, by
contrast, has a visible EDP (Electronic Data Processing) Directorate address
(`edpdte@bsf.nic.in`) with no SSB equivalent found `[W11]`. Separately, SSB
has sent personnel for Drone Pilot Training at a DGCA-approved institute and
for Special Communication Equipment Training at BSF `[N3]`.

### 4.2 Surveillance responsibilities

**Statutory charter** (Rules r.9(1)), verbatim: the Force shall, in its area
of responsibility, (i) safeguard the security of assigned borders and
promote a sense of security among the border population; (ii) prevent
trans-border crimes, smuggling and illegal activity; (iii) prevent
unauthorised entry into or exit from India; (iv) carry out civic action
programmes; (v) perform any other duty assigned by the Central Government
`[W2]`. Rule 9(5) makes any superior officer's order connected to this task a
"lawful command" `[W2]`.

Two features of this charter bear directly on any surveillance product, and
are recorded here purely as findings: the border population is, by statute,
a constituency to reassure (r.9(1)(i), and civic action as a statutory task
under r.9(1)(iv)) — not only a population to watch; and Rule 9(1) contains no
mention of observation, surveillance, monitoring, sensors, cameras or
recording — its verbs are safeguard, promote, prevent, carry out, perform
`[W2]`.

**Who performs which function:**

| Function | Evidence |
|---|---|
| Border surveillance | Not statutorily assigned to a named role. Practice is described (secondary sources) as post- and patrol-based: BOPs, observation posts, check posts, joint check posts, naka `[N8][N23]` |
| Patrolling | Statutorily recognised — "active duty" includes a unit "operating at a picket or engaged on patrol or other guard duty along the borders of India" (§2(a)(ii)) `[W1]`. Area-domination and joint patrols with APF Nepal: 5,841 in FY 080/81 `[N8]` |
| Checking / frisking | Manned naka and check posts; female personnel deployed at border check posts for checks of female travellers `[N8]`; metal detectors at Sonauli and Thuthibari outposts `[W8]` |
| Intelligence gathering | SSB is Lead Intelligence Agency for the Indo-Nepal and Indo-Bhutan borders; intelligence wing of ~650 field/staff agents; 25 Border Interaction Teams in civilian attire on high-risk routes; "Know Your Area" programme `[N8][N19]` |
| Incident reporting | No SSB reporting instrument for a border incident was located. What is statutory is internal: r.10(2)(d) requires command changes to be "immediately reported to the next higher authority"; r.176 requires a Court of Inquiry for unnatural deaths, disabling injuries, financial losses, loss of secret documents, and injury/damage to private persons, with an unnatural death reported "through the messenger" to the police `[W2]` |
| Incident assessment | No source describes who assesses a border event, against what criteria, or in what time |
| Escalation | Statutory command runs outpost/detachment → company → Commandant (battalion) → DIG → IG → ADG → DG → Central Government (r.9(2), §5) `[W1][W2]`. Whether an operational alert follows this same chain is not stated |
| Response coordination | Cases are "handed over to the local police for investigation and further disposal, as per existing laws and procedures" after apprehension/seizure `[W7]` |
| Cross-border coordination | Scheduled, not event-driven: DG/IG annual→semi-annual, DIG quarterly, Battalion monthly, Company/BOP fortnightly `[N8]`; reaffirmed at national level by the 14th India-Nepal Joint Working Group on Border Management, Dehradun, 20–21 August 2026 `[W12]` |
| Narcotics interdiction | SSB is empowered under the NDPS Act, 1985, alongside BSF, Indian Coast Guard, RPF and NIA `[W5]` |

**A documented capability gap.** A BPRD project report records that "only
BSF has developed a system of monitoring, supervising and following up with
the local Police" on registered criminal cases; "IG (Ops), SSB has furnished
the details of cases booked" and arrest/seizure figures, "however, SSB could
not provide data with respect to the present status of the cases," and "is
now in the process of developing systems and procedures for monitoring
progress of investigation and trial" `[W7]` (report approved 09.02.2021; the
underlying data request dates to 2018). As of that period, SSB could report
cases, arrests and seizure quantities but not case outcomes after handover —
consistent with characterising SSB's reporting as an outcome ledger rather
than an event log. Whether the case-monitoring system BPRD describes as
in-development was ever built, and what it is called, is unknown (SQ-W1).

### 4.3 CCTV / control-room evidence

This section is short because almost nothing is verified — that absence is
itself the finding.

**What is established.** MHA confirmed in a Lok Sabha reply (03.02.2026)
that SSB "has procured the Unmanned Aerial Vehicles, Micro Unmanned Aerial
Vehicles, Hand Held Thermal Imager, CCTV Surveillance Setup with Automatic
Face Recognition System with Auto Number Plate Recognition and Satellite
phones for surveillance and modernization of the Force" `[N3]` — procurement
only; no site, count, or operator is stated. A ministerial statement lists
"drones, CCTV systems, thermal imagers, night-vision equipment, GPS-based
patrolling, secure digital communication systems and GIS-based planning" as
technologies in use `[W13]` — a capability list, not a workflow. At the 14th
India-Nepal Joint Working Group on Border Management (Dehradun, 20–21 August
2026), India and Nepal "agreed to enhance security surveillance at sensitive
locations in the border areas through the use of modern and latest
technologies, including CCTV cameras and other advanced equipment," and to
"strengthen coordination and real-time information sharing" `[W12]`.

CIBMS — defined by MHA as "the integration of manpower, sensors, networks,
intelligence and command control solutions to improve situational awareness
at different levels of hierarchy" — is placed explicitly on the
India-Pakistan and India-Bangladesh borders only, with pilots of 2×5 km in
Jammu and 61 km at Dhubri, and hybrid-surveillance pilots on the
India-Myanmar border `[W3]`. The India-Nepal and India-Bhutan border
paragraphs in the same Annual Report contain only border length, the
"misuse of the open border" framing, road construction, and BOP counts (539
Nepal, 195 Bhutan) — no technology, sensors, surveillance programme, or
command-and-control item appears for either border `[W3]`. ICPs, which do
list CCTV among their infrastructural facilities, are operated by the Land
Ports Authority of India, not the border guarding force; Raxaul (03.06.2016)
and Jogbani (15.11.2016) are the operationalised India-Nepal ICPs `[W3]`.

**What is not established** — the central gap: whether SSB monitors live
video anywhere, at any echelon. No control room, operations room, video
wall, monitoring roster, shift pattern, operator establishment, or
cameras-per-operator figure for SSB was found in this pass or the previous
one. Also unknown: where the procured FRS/ANPR setup is installed, how many
sites, and whether it exposes streams or APIs; whether ordinary BOPs have
cameras at all versus only check posts/ICPs/"key crossing points"; who owns
and monitors CCTV at ICP Raxaul and Jogbani, and whether SSB has access to
those feeds; retention period, storage location and export procedure for any
SSB video; and where drone/UAV video goes, and whether it is recorded.

**The proposal that implies the absence.** A BPRD/National Police Mission
project report (*Integrated Border Management and National Security*,
Project 05/MM:06, approved 09.02.2021) proposes Integrated Law Enforcement
Centres (ILECs) "stationed at existing and proposed Integrated Check Posts,"
co-locating Customs, NCB, NIA, DRI, ED, local police, IB, R&AW's Special
Bureau and the Wildlife/Biodiversity Wing alongside "personnel from border
guarding forces of the area" `[W7]`. The proposal includes a "Situation
Room": "near real-time situation of the borders will be built-up" from
collated multi-source information, with trend analysis used "for planning
routine operations by Border Guarding Forces" `[W7]`. In the same report's
proposed ILEC equipment schedule, CCTV appears once — "CCTV with monitor —
For Camp security — 6 — Pooled" — alongside a "Digital Camera with still &
video — For operations and investigation" `[W7]`. That a 2021 government
report designed specifically for integrated border management describes a
"Situation Room" in the future tense, and budgets CCTV as camp security
rather than a border-surveillance instrument, is circumstantial but
consistent evidence that no equivalent facility existed on the borders and
ICPs the report addressed, to be described in the present tense.

### 4.4 Incident / alert workflow

**What is verified is all internal or judicial, not operational.** Handover
is the terminal step: forces "after carrying out apprehension of trans
border criminals and/or seizure of contrabands... hand them over to the
local police for investigation and further disposal," and the same source
notes these cases "find sub-optimum level of priority and seriousness in
investigation and disposal" because state police have "neither the resources
nor adequate professional expertise" `[W7]`. A statutory reporting duty
exists for unnatural deaths, with a person as its default transport: r.176
requires "an immediate report... sent through the messenger to the
officer-in-charge of the police station," or, if that is not possible within
a reasonable time, a written report in Appendix XIII form `[W2]`. A Court of
Inquiry is mandatory for unnatural deaths within Force lines, disabling
injuries, financial irregularities/losses/theft, loss of secret documents,
and injury/damage to private persons likely to found a claim against
Government; r.176(1) also allows one for "any other matter of importance"
`[W2]`. "Alarm" is a statutory concept and a human act — §22(f)/§23(e) make it
an offence to "intentionally or through neglect occasion a false alarm...
or spread... reports calculated to create unnecessary alarm or despondency"
`[W1]`. Command-change events must be reported "immediately... to the next
higher authority" (r.10(2)(d)) `[W2]`. Section 63 of the Bharatiya Sakshya
Adhiniyam, 2023 governs electronic records force-agnostically, requiring a
certificate with a hash value signed by the device custodian and an expert
`[S29]`; SSB's own site publishes the BNS/BNSS/BSA texts under
`assets/document/Laws/`, indicating force-wide dissemination `[W4]`.

**What is not verified** is the detection → assessment → escalation →
response sequence for a border event at a BOP or check post — nothing
retrieved describes it. The BSF/BOLD-QIT chain (sensor → Control Room → QRT
→ interception), documented in `domain-research.md` §2.1–§3.2, is explicitly
non-transferable per `ssb-operational-context.md` §16 item 7, and this pass
found nothing to replace it with. Also unknown: whether SSB has a Quick
Reaction Team construct at all, or whether response is by the patrol/naka
already in the field; what carries an operational alert (radio, phone,
landline, runner) — the only transport the statute names for any report is
"through the messenger," and that is for the police, for a death `[W2]`;
whether any written SOP or Standing Order governs border-event assessment
and escalation (SSB's public site uses "SOP" only for recruitment and
dependent I-cards `[W3][W4]`); response-time expectations from detection to
interception; and whether any event producing no seizure and no arrest is
recorded anywhere. Taken together, SSB's evidenced reporting instruments are
outcome-shaped and discipline-shaped, not detection-shaped: every verified
instrument records a result (case, arrest, seizure, handover) or an internal
irregularity (death, loss, change of command) — none records a detection.

### 4.5 Existing systems relevant to IBVAP

| System | What it actually is | Owner | Confidence |
|---|---|---|---|
| **SIMS** — Seizure Information Management System | MHA e-portal launched 2019 for pan-India NDPS drug-seizure data digitisation across all NDPS-empowered agencies. Not an SSB system, not a C2 system, not an incident register. SSB is one contributing agency among several `[W5]` | MHA / NCB | High — and removes SIMS from the C2 candidate list |
| CCTV/FRS/ANPR setup | Procured by SSB `[N3]`; no vendor, site count, deployment or interface stated | SSB | High for procurement; deployment unknown |
| Case-monitoring system (post-handover) | "In the process of developing" as of the 2018–2021 window `[W7]` | SSB | Medium — statement of intent, outcome unknown |
| Rotational E-Transfer System | Personnel transfer/posting automation (PHP/Apache/Linux/MySQL). Administrative, not operational `[W14]` | SSB | Medium for existence; irrelevant to surveillance |
| CLMS (`clms.ssb.gov.in`) / recruitment portals | Separate SSB web systems; naming suggests learning-management and recruitment `[W4]` | SSB | Medium for existence; purpose unknown, appears administrative |
| NIDMS — National IED Data Management System | NSG/Rashtriya Raksha University system to "synergize & integrate IED related incidents" with real-time data ingestion from state police/CAPFs and planned AI/ML; total cost ₹10.11 crore `[W3]` | NSG / MHA | High for existence; scope is IED incidents only, SSB is only one feeding CAPF |
| "Integrated Command and Control Centre" (AI surveillance grid, RADARS, EO, night vision, motion detectors) | Named in an MHA national narcotics answer covering international borders/coastal areas generally `[N4]` | MHA (unattributed) | High for the statement; not attributable to SSB or its borders |
| CIBMS | Integration of manpower/sensors/networks/intelligence/C2, India-Pakistan and India-Bangladesh borders only `[W3]` | MHA / BSF | High — and explicitly not on SSB's borders |
| ILEC "Situation Room" | 2021 BPRD proposal, not a system in service `[W7]` | Proposed: MHA | High that it was proposed; no evidence it exists |
| PMU — Project Monitoring Unit, Dept of Border Management, MHA | Real MHA unit (East Block-I) for border infrastructure — fencing, roads, buildings — not surveillance systems `[W15]` | MHA | High for existence; not a surveillance system |
| Modernisation Plan-IV | CCS-approved scheme, ₹1,523 crore total to 31.03.2026, SSB's share ₹122.21 crore; equipment list is weapons/vehicles (Grenade Launchers, Assault Rifle, Bomb Detection/Disposal, Mine Protected Vehicle) — no video analytics, VMS, CCTV or C2 item `[W3]` | MHA | High |
| CAPF modernisation (Rajya Sabha reply, reported 04.08.2026) | Reported to cover thermal imagers, NVGs, UAVs, secure comms, "Hyper-Converged Infrastructure servers, networking equipment and digital command-and-control platforms" `[W16]` | MHA | Medium — primary PDF not located; closest statement found to an MHA C2-platform reference, needs verification |

The blocking unknown carried from the previous pass: **what "existing
command and control systems" means for SSB**, which the problem statement
requires integrating with. SIMS has been eliminated as a candidate and
nothing has replaced it — no source names an SSB C2 system, vendor,
protocol, data model or network reach.

### 4.6 Procurement evidence

SSB publishes a tender feed on its own website; this pass retrieved the
complete feed as served — **280 tenders, dated 07.10.2025 to 11.08.2026**,
across FHQ and all six Frontiers (Guwahati 61, Tezpur 53, FHQ 44, Patna 44,
Siliguri 40, Lucknow 24, Ranikhet 14) `[W4]`.

**Not one of those 280 tenders is for CCTV, cameras, NVR/DVR, video
management software, video analytics, face recognition, number-plate
recognition, a control room, or a command centre.** Searching for *cctv,
camera, surveillance, video, analytic, control room, command, ANPR, number
plate, face, VMS, NVR, DVR, monitor, network, server* across the full feed
returns only: `[W4]`

| Date | Formation | Tender |
|---|---|---|
| 08.12.2025 | FHQ | Repair and renovation of Communication Server Room at FHQ |
| 31.10.2025 | FHQ | Victim Location Unit (With Breaching System), 18 Nos. |
| 05.01.2026 | FHQ | Lift repair and AMC, SSB Campus Mahipalpur |
| 03.02.2026 | FHQ | Officers' mess toilet renovation, 25th Bn Ghitorni |
| 19.02.2026 | Ranikhet | Bitumen road repair, Transit Camp Kathgodam |

The feed is overwhelmingly civil works at BOPs: permanent buildings,
barracks, women's barracks, toilet blocks, waterproofing, border pillar
construction, and — recurring dozens of times across the Tezpur Frontier
alone — a standard package of "chain link fencing i/c security gate, sentry
post (01 No.) and morcha (04 Nos.)" per BOP `[W4]`. Read against MHA's
statement that both SSB borders are open and unfenced `[W3]`, this package
reads as hardening of the BOP compound itself, not fencing of the
international border. SSB's other recurring technical procurement is
off-grid solar power at BOPs, tendered per-battalion in lots of roughly 6–8
BOPs by Frontier/Sector Executive Engineers — e.g. ₹67,87,593 for the 6th Bn
Ranighuli site, 7 BOPs at 70th Bn Lakhimpur Kheri II, 8 BOPs at 31st Bn
Gossaigaon, 6 BOPs at 57th Bn Sitarganj `[W9]`. The only IT-adjacent SSB
tenders found via third-party aggregators in the 2025 window are cyber
security/compliance audits at ₹50,000–₹60,000 in Jharkhand and Uttar Pradesh
`[W17]`. SSB's site publishes a document titled "Three years Procurements
Plan," but the PDF served under that title is actually a concatenation of
education-welfare MoUs; the actual procurement plan was not retrievable
`[W4][W6]`.

Whether an SSB CCTV/FRS/ANPR/VMS/analytics/control-room tender exists in the
CPPP (eprocure.gov.in) or GeM archives is unknown — the SSB site's own feed
covers only about ten months, CPPP's public search was not queryable without
a session in this pass, and the FRS/ANPR setup MHA confirmed in Feb 2026
`[N3]` was procured through some route that left no trace in any feed
searched here. Two readings of this evidence remain open: (1) SSB's video
procurement happens centrally at FHQ/MHA level — via the CAPF Modernisation
Plan, GeM, or a nomination route — and so never appears in the
Frontier-level engineering feed, which is dominated by CPWD-style civil
works; or (2) SSB's video estate is genuinely small, so few tenders exist to
find. Locating the FRS/ANPR procurement document would settle both the route
and the scale (SQ-W2).

---

## 5. Implications for IBVAP

These are the statements this pass considers strong enough for later stages
to build on without further validation. None of them is a product decision,
a user model, or a workflow proposal — they are inputs to be weighed when
`docs/02-product/` scopes the product.

1. Command runs DG → ADG → IG → DIG → Commandant, with responsibility
   defined by assigned area above battalion level (§5, r.9(2)) `[W1][W2]`.
2. The statutory rank ladder (r.8) is fixed and complete, from DG down to
   Enrolled followers `[W2]`.
3. Frontier = IG, Sector = DIG, Battalion = Commandant, consistently
   observed and consistent with r.9(2) `[W2][W4][W8]`.
4. An outpost is commanded by a Deputy Commandant/Assistant Commandant, or
   by a subordinate officer not below Sub-Inspector — a statutory floor, not
   a norm `[W1]` §56(3)–(4).
5. Frontier, Sector, Company, Platoon and BOP are administrative constructs,
   not statutory formations; only "battalion" and "unit" are constituted by
   the Central Government `[W1][W2]`.
6. The statutory task (r.9(1)) is border safeguarding plus promoting a
   sense of security among the border population, preventing trans-border
   crime and unauthorised entry/exit, and civic action — surveillance is not
   named as a task `[W2]`.
7. Both SSB borders are open and unfenced; MHA's framing — "misuse of the
   open border by terrorists and criminals" — is verbatim identical for
   India-Nepal and India-Bhutan across three consecutive Annual Reports
   `[N1][N2][W3]`.
8. No CIBMS-equivalent programme exists on SSB's borders; CIBMS is located
   only on the India-Pakistan and India-Bangladesh borders `[N1][W3]`.
9. BOP counts are stable at 539 (Nepal) + 195 (Bhutan) = 734, unchanged
   across three Annual Reports `[N1][N2][W3]`.
10. SSB has procured a CCTV/FRS/ANPR setup as a matter of record; deployment
    is unknown `[N3]`.
11. SSB apprehends and seizes; local police investigate and prosecute.
    Handover is the terminal step of an SSB case, and the receiving agency is
    documented as under-resourced for these cases `[W7]`.
12. SSB is NDPS-empowered, alongside BSF, Indian Coast Guard, RPF and NIA
    `[W5]`.
13. SIMS is MHA's national NDPS seizure-data portal, not an SSB system, and
    therefore not a candidate for "existing command and control systems"
    `[W5]`.
14. Section 63 BSA, 2023 applies to SSB video exactly as to any other
    electronic record — a certificate with a hash, signed by the device
    custodian and an expert. SSB itself distributes the BNS/BNSS/BSA texts
    force-wide `[S29][W4]`.
15. SSB's technical cadre is Communication, supported by a Wireless &
    Telecom Training Centre; there is no IT, cyber, video or electronics
    cadre `[W3][W4]`.
16. BOP electrical supply is being addressed by off-grid solar, tendered
    per-battalion in lots of 6–8 BOPs `[W9]`.
17. SSB's current BOP construction programme hardens the post, not the
    border: chain-link fencing, a gate, one sentry post and four morchas per
    BOP, plus permanent buildings `[W4]`.
18. 42% of SSB BOPs lack road connectivity (308 of 734), unchanged and
    uncontradicted by AR 2024-25 `[N9]`.
19. SSB is deployed on internal-security/counter-insurgency duties beyond
    the border (J&K, Assam, LWE areas of Chhattisgarh/Jharkhand/Bihar), so
    not every battalion is a border battalion `[W3]`.
20. As of 21 August 2026, India and Nepal have agreed at government level to
    enhance border surveillance using CCTV and other technologies, and to
    strengthen real-time information sharing `[W12]`.

---

## 6. Risks / Limitations

**The central limitation is structural, not a search failure.** The SSB
Act's eleven chapters (Preliminary; Constitution of the Force and Conditions
of Service; Offences; Punishments; Deductions from Pay and Allowances;
Arrest and Proceedings Before Trial; Force Courts; Procedure of Force
Courts; Confirmation and Revision of Proceedings; Execution of Sentences,
Pardons, Remissions; Miscellaneous) `[W1]` are a constitution-and-discipline
instrument, not an operational doctrine. Chapter VI ("Arrest and Proceedings
Before Trial") concerns arrest of Force members for offences under the Act,
not powers over civilians `[W1]`. Neither the Act nor the Rules contains the
words *camera, video, photograph, surveillance, monitor, CCTV, sensor* or
*electronic record* in any operational sense `[W1][W2]`. SSB's border-policing
powers instead come from notifications under other statutes (CrPC/BNSS,
NDPS `[W5]`, Arms, Passport), and its operational method lives in internal
orders issued under the DG's Rule 9(4) authority, which are not public. This
is why the CCTV/control-room/incident workflow could not be found, and it
means the workflow is **unlikely to be findable by desk research at all** —
the documents that would answer it are the class of document that does not
get published. Only an RTI reply, a published SSB Standing Order, or a
training-institution syllabus would falsify this.

**Source-quality caveats.** Several load-bearing findings rest on secondary
sources rather than primary government documents: patrol/checking practice
details and volumes (`[N8]`), the "7 companies per battalion, 3 BOPs per
company" figure (`[N6]`, unverified against any primary source), the CAPF
Rajya Sabha reply on "digital command-and-control platforms" (`[W16]`, news
reporting a parliamentary answer whose primary PDF was not located), and
several tender/procurement facts sourced through trade-press reproductions
of CPPP notices (`[W9][W17]`) rather than CPPP directly. Court records
(Indian Kanoon) were searched but returned an overwhelmingly service- and
seniority-litigation corpus, not operational-procedure judgments — the one
substantive fact obtained (platoons under a named "Commander") was
incidental to an unrelated case `[W10]`.

**Corpora that could not be exploited.** SSB's own Frontier e-magazines
(*Rhino*, *Barahsinga*, *Guldar*, *Dhanesh*, *Devbhoomi*, *Tiger Trail*, and
others — 110 issues indexed) were downloaded but are predominantly Hindi
with non-extractable font encoding, and remain the most promising
unexploited primary corpus (SQ-W7) `[W4]`. The CPPP (eprocure.gov.in) archive
was not queryable without a session in this pass. CAG search returned only
state-police modernisation audits, not CAPF or border-force audits. A
Parliamentary Standing Committee search returned nothing SSB-specific beyond
a previously known PRS summary (*Working Conditions in Border Guarding
Forces*, `[N18]`).

---

## 7. Open Questions / Research Gaps

**Critical unknowns — must not be silently resolved by assumption in later
stages:**

- Whether SSB monitors live video at all, and if so at what echelon. Two
  research passes across primary statutes, three Annual Reports,
  parliamentary answers, a BPRD report, SSB's own site, court records and
  six tender aggregators produced no description of an SSB control room,
  operations room, video wall or operator establishment. The BSF/BOLD-QIT
  pattern is explicitly non-transferable.
- The detection → assessment → escalation → response sequence at a BOP or
  check post. The command chain is a disciplinary/administrative chain
  (r.9(2)); whether an operational alert travels the same path is unstated.
- What carries an alert, and to whom. The only report transport named in
  the statute is "through the messenger," for a death, to a police station.
- Whether a QRT construct exists in SSB, or whether response is the patrol
  or naka already deployed.
- The installed camera base — count, siting, make, resolution, codec,
  PTZ/fixed, thermal/visible, ONVIF conformance, recorder/VMS. `[N3]`
  confirms procurement and nothing else.
- What "existing command and control systems" means for SSB. SIMS has been
  eliminated and nothing replaces it; treating any named system as SSB's C2
  without evidence would be inventing a requirement.
- Whether a written SOP or Standing Order governs border-event handling. If
  so it sits with the DG under Rule 9(4) and is not published — structurally
  unlikely to be resolved by desk research.
- Whether any event producing no seizure and no arrest is recorded anywhere.
  Every verified SSB reporting instrument is outcome- or discipline-shaped.
- The normal rank and establishment of a BOP in-charge and check-post
  in-charge — the statute gives a floor and a ceiling, not a norm.
- Who owns and monitors CCTV at ICP Raxaul and ICP Jogbani — LPAI operates
  ICPs, but SSB's relationship to those feeds is unstated.
- The legal basis, authorisation level, retention rule and oversight for
  face recognition applied to Indian, Nepali and Bhutanese nationals
  exercising a treaty right of movement — nothing in the Act or Rules
  addresses this.
- Bandwidth, power budget and connectivity at an SSB BOP. Off-grid solar
  tenders establish that power is being addressed, not what budget results;
  no data-link evidence was found.
- What "suspicious activity" means on a border where crossing is lawful.
  MHA's own framing — "misuse of the open border" — presupposes a
  lawful-use baseline nobody has defined.
- Whether the Indo-Bhutan border is operationally the same problem as the
  Indo-Nepal border. Every source treats them together with verbatim
  identical challenge language, which may reflect drafting convention
  rather than operational sameness; the Frontier structure hints otherwise
  (Tezpur/Siliguri on the Bhutan side, Ranikhet/Lucknow/Patna on the Nepal
  side).

**Specific follow-up questions raised by this pass:**

- **SQ-W1** — Was SSB's post-handover case-monitoring system (in development
  per BPRD, 2021) ever built? What is it called, and does it hold anything
  beyond case outcomes?
- **SQ-W2** — Through what procurement route was the FRS/ANPR CCTV setup
  bought, given it appears in no tender feed searched here?
- **SQ-W3** — What are CLMS and the SSB recruitment portal, and does SSB run
  any other internal web system?
- **SQ-W4** — Does SSB have an EDP/IT directorate equivalent to BSF's, or
  does the Communication cadre own all technical systems?
- **SQ-W5** — What is the CIOA cadre? It appears in SSB's own index with no
  expansion given anywhere found.
- **SQ-W6** — What became of the ILEC/Situation Room proposal after
  09.02.2021? Was any ILEC established at an India-Nepal ICP?
- **SQ-W7** — Mine the SSB Frontier e-magazines (*Rhino, Barahsinga, Guldar,
  Dhanesh, Devbhoomi, Tiger Trail, Dolphin, Koshi* — 110 issues indexed).
  They are the most likely public place for SSB to describe its own posts,
  equipment and daily working, but require OCR of Hindi Devanagari.
- **SQ-W8** — Retrieve the primary PDF of the Rajya Sabha reply of
  04.08.2026 referencing "digital command-and-control platforms" for CAPFs.
- **SQ-W9** — Was anything agreed at the 14th India-Nepal JWG beyond the
  CCTV sentence — specifically who installs, who monitors, and whether any
  feed or data crosses the border?
- **SQ-W10** — Retrieve SSB's actual "Three years Procurements Plan"; the
  file published under that title is a different document.
- **SQ-W11** — Is there a sanctioned establishment table for a BOP — personnel
  count, equipment, ranks? Nothing found states it.

**Status of prior open questions** (`ssb-operational-context.md` §15): SQ-26,
SQ-27 and SQ-28 are closed by this pass (Act/Rules retrieved, SSB website
retrieved, AR 2024-25 retrieved). SQ-5 is superseded — SIMS is now known to
be an MHA/NCB national NDPS database, not an SSB system, so the original
question no longer applies (replaced by SQ-W1). SQ-19/SQ-20 (BOP and
formation counts) are partly answered — AR 2024-25 re-confirms 539+195 BOPs
and 6/18/73 formations, stable across three Annual Reports, though
lower third-party counts remain unreconciled. SQ-1 through SQ-4, SQ-6
through SQ-15, SQ-17, SQ-18, SQ-21 through SQ-25, and SQ-29 through SQ-31
remain open.

---

## 8. Conclusions

This pass upgrades the organisational-hierarchy question from
thesis-sourced reconstruction to statute-grounded fact: the command chain,
rank ladder, sub-battalion command floor, and statutory task charter are now
evidenced directly from the SSB Act, 2007 and SSB Rules, 2009, cross-checked
against SSB's own site and MHA's Annual Report. It also closes three
specific errors in the earlier SSB research pass, most importantly removing
SIMS as a candidate "existing command and control system."

It does not, however, resolve the question that matters most for IBVAP: who,
if anyone, in SSB watches video, and what happens between a detection and a
response. This is not for lack of searching — the search was documented and
exhaustive across primary statutes, three Annual Reports, parliamentary
answers, a government project report, SSB's own publication and tender
corpus, court records and multiple tender aggregators. The argument in §6 is
that this gap is structural: SSB's operational method is set by internal DG
orders that are, by design, not published, so the class of document that
would answer this question is unlikely to surface through further desk
research.

The correct status of "the primary user" for any later product-discovery
work is therefore: **the surveillance/CCTV operational workflow has not been
sufficiently validated from available sources — not that it does not
exist.** Any user hierarchy or workflow written into `docs/02-product/`
before the critical unknowns in §7 are answered will be invented, not
discovered, and must be labelled as such at the point it is written. Closing
this gap will most plausibly require primary access — an RTI request, an
interview with serving or retired SSB personnel, or a partner relationship
with the Force — rather than further open-source research.

---

## 9. References

Reliability key: **P** = primary/official Indian government · **G** =
government research body · **A** = academic · **N** = news · **V** =
vendor/trade · **C** = court record · **E** = encyclopedic/tertiary.

| ID | Source | Type | Retrieval | URL |
|---|---|---|---|---|
| W1 | **The Sashastra Seema Bal Act, 2007** (Act No. 53 of 2007), Gazette of India Extraordinary, 20.12.2007 — §2 definitions, §4 constitution, §5 control, §22/§23/§30 offences, §56 powers of commanding officers and of officers commanding a company/detachment/outpost | P | Direct (full text) | https://www.mha.gov.in/sites/default/files/2023-01/SSB-Act2007_0[1]_1[1]_0.pdf |
| W2 | **The Sashastra Seema Bal Rules, 2009** (made under s.155) — r.7 constitution, r.8 ranks, r.9 task/command/control, r.10 command, r.176 Courts of Inquiry | P | Direct (full text, 110 pp.) | https://www.mha.gov.in/sites/default/files/SSB-Rule2009_3.pdf |
| W3 | **MHA Annual Report 2024-25** — §3.20–3.24 CIBMS/IMB, §3.26–3.28 India-Nepal/India-Bhutan borders, §3.39 ICP list, §7.50–7.52 SSB profile/formations/strength/achievements, §7.60–7.61 Modernisation Plan-IV, NIDMS | P | Direct (full text, 22.7 MB) | https://www.mha.gov.in/sites/default/files/AREnglish_24032026.pdf |
| W4 | **Official SSB website and its public JSON API** (`ssb.gov.in`, API base `https://ssb.gov.in/api/api`) — Frontier list; full tender feed (280 records, 07.10.2025–11.08.2026); circulars (81); recruitment-rules cadre index; forms; publications index (110 issues); document paths incl. `assets/document/Laws/{BNS,BNSS,BSA}` | P | Direct (API queried; documents downloaded) | https://ssb.gov.in/ |
| W5 | **MHA, Lok Sabha Unstarred Question No. 459**, answered 20.07.2021 — *Drug Trafficking*; defines SIMS and records SSB's NDPS empowerment | P | Direct (full text) | https://www.mha.gov.in/MHA1/Par2017/pdfs/par2021-pdfs/LS-20072021/459.pdf |
| W6 | **SSB-signed Memoranda of Understanding** (Rungta Education Foundation; DAV University Jalandhar; CSR Educational Trust), published on the SSB site under the "Three years Procurements Plan" title — FHQ address, IG (Admn) as SSB Joint Manager | P | Direct (scanned pages read) | https://ssb.gov.in/assets/document/circulars/1.pdf |
| W7 | **Bureau of Police Research and Development, MHA / National Police Mission, Micro Mission 06** — *Integrated Border Management and National Security*, Project No. 05/MM:06, project leader Shri Santosh Mehra, IPS, ADG BPR&D, approved 09.02.2021 — handover practice; IG (Ops) SSB case-data gap; ILEC and Situation Room proposal; ILEC equipment schedule | G | Direct (full text) | https://bprd.nic.in/uploads/pdf/Integrated%20Border%20Management%20and%20National%20Security.pdf |
| W8 | Deccan Herald / PTI — *Indo-Nepal border under tight vigil ahead of PM Modi's Ayodhya visit*, 27.12.2023 — quotes Deputy Inspector General, SSB, Gorakhpur, Akhileshvar Singh; dog squads, one platoon of the women's wing, metal detectors at Sonauli and Thuthibari outposts | N | Direct (headline and attribution block; article body behind SPA) | https://www.deccanherald.com/india/uttar-pradesh/indo-nepal-border-under-tight-vigil-ahead-of-pm-modis-ayodhya-visit-2826402 |
| W9 | **EQ Mag Pro** — trade-press reproductions of SSB CPPP tender notices for off-grid solar power plants at BOPs (6th Bn Ranighuli/SHQ Bongaigaon/FTR Guwahati; 70th Bn Lakhimpur Kheri II; 31st Bn Gossaigaon; 57th Bn Sitarganj/EE SHQ Pilibhit) | V | Indirect (search-result extracts; site returned HTTP 403 to direct fetch) | https://www.eqmagpro.com/tag/ssb-guwahati/ |
| W10 | **Indian Kanoon** — four targeted searches of the SSB corpus. *Nisha Priya Bhatia vs S.K Goel*, Delhi District Court, 06.03.2012 (incidental: "Commander, Sh. S. Murup of the SSB Platoon which guards the R&AW training institute campus, Gurgaon"); *Saurabh Dubey & Ors. vs Union of India*, Delhi High Court, 25.05.2015 (CAPF cadre seniority) | C | Direct | https://indiankanoon.org/ |
| W11 | **CPWD Border Fencing Zone circulation list** — BSF EDP Directorate contact (`edpdte@bsf.nic.in`), and DG addresses for ITBP, BRO and SSB | P | Direct (within `[W15]`) | — |
| W12 | **14th India-Nepal Joint Working Group on Border Management**, Dehradun, 20–21 August 2026 — CCTV surveillance agreement; delegations led by Ms. Pausumi Basu, JS (BM-I), MHA and Mr. Ananda Kafle, JS, MoHA Nepal; 15th meeting to be held in Nepal | N | Direct (multiple outlets, consistent wording) | https://therahnuma.com/nepal-and-india-agree-to-enhance-security-surveillance-at-sensitive-locations-along-border |
| W13 | Deccan Chronicle — *SSB Safeguards 2,450-km Open borders with Nepal, Bhutan: Bandi Sanjay* — MoS Home statement on SSB technology; 2025-26 outputs (661 trafficking victims rescued, 6,324 apprehended); 18 relief and rescue teams | N | Direct | https://www.deccanchronicle.com/nation/ssb-safeguards-2450-km-open-borders-with-nepal-bhutan-bandi-sanjay-1979854 |
| W14 | Raygain Technologies — case study, SSB Rotational E-Transfer System (PHP/Apache/Linux/MySQL) | V | Direct | https://raygain.com/case_studies/sashastra-seema-bal-ssb/ |
| W15 | **CPWD, Office of the Chief Engineer, Border Fencing Zone** — *Engagement of Retired Govt. Officer/Qualified Professionals as Chief Consultant on Contract Basis*, No. W-12011/268/CE/EE-I/2025-26/1452, dated 24.10.2025 — Project Monitoring Unit, Department of Border Management, MHA; circulated to JS (BM-I) MHA, DGs of BSF/ITBP/SSB/AR, Director (ICB) (BM-IV) | P | Direct (scanned page read) | https://ssb.gov.in/assets/document/Circulars/Circular_181125_144338.pdf |
| W16 | ETV Bharat — *New Weapons, Smarter Surveillance: CAPFs Gain Edge In Border, Internal Security Missions*, 04.08.2026 — reports a Rajya Sabha reply by MoS Home Nityanand Rai to MP Bhola Singh; SSB Modernisation Plan-IV outlay; "Hyper-Converged Infrastructure servers, networking equipment and digital command-and-control platforms" | N | Direct | https://www.etvbharat.com/en/bharat/new-weapons-smarter-surveillance-capfs-gain-stronger-edge-in-border-and-internal-security-missions-enn26080406342 |
| W17 | Tata nexarc / Tendersontime / TendersPlus / TenderDetail / BidAssist — third-party SSB tender aggregators, used to test for CCTV/VMS/analytics tenders; returned cyber-security audits, civil works and solar | V | Direct/partial (some HTTP 403) | https://www.tatanexarc.com/t/authority/sashastra-seema-bal-ssb-tenders/ |

**Carried forward** from `ssb-operational-context.md` §17, cited here by
their original IDs: `[N1]`, `[N2]`, `[N3]`, `[N4]`, `[N6]`, `[N8]`, `[N9]`,
`[N18]`, `[N19]`, `[N23]`. **Carried forward** from `domain-research.md` §9:
`[S29]`.

**Sources sought and not obtained**, recorded so a later pass does not
repeat the attempt blindly: India Code (`indiacode.nic.in`) returned HTTP
404 on the SSB Act handle/bitstream (not needed — the MHA-hosted texts
`[W1][W2]` were obtained instead); SSB's actual "Three years Procurements
Plan" (the published file under that title is a set of education MoUs
`[W6]`); the primary PDF of the Rajya Sabha reply of 04.08.2026 `[W16]`; a
CAG audit of CAPF or border-force modernisation procurement; a Parliamentary
Standing Committee report specific to SSB (beyond the PRS summary `[N18]`);
the eprocure.gov.in (CPPP) archive (not queryable without a session in this
pass); and the SSB Frontier e-magazines (downloaded but not machine-readable
— Hindi, non-extractable font encoding; see SQ-W7).

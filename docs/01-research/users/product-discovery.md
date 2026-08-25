# Product Discovery — IBVAP

**Stage:** 01 — Research → Users / Synthesis
**Date:** 2026-08-24
**Inputs:** [problem.md](../../00-project/problem.md), [vision.md](../../00-project/vision.md),
[goals.md](../../00-project/goals.md),
[domain-research.md](../domain/domain-research.md),
[ssb-operational-context.md](../domain/ssb-operational-context.md),
[ssb-operational-workflow.md](../domain/ssb-operational-workflow.md),
[competitive-landscape.md](../competitors/competitive-landscape.md),
[technical-feasibility.md](../technology/technical-feasibility.md).

**Revised 2026-08-24** against
[ssb-operational-workflow.md](../domain/ssb-operational-workflow.md). That pass
withdraws the framing *"the primary user may not exist"* (ibid. §0.3). Every
place in this document that treated the absence of public documentation as
evidence of operational absence has been corrected. See
[§1.1](#11-the-most-important-structural-finding-about-users).

> **This document does not define the product.** It is a synthesis pass that
> states who the users are, what they are trying to do, what hurts, what is
> worth solving, and what is still unknown. No PRD, no UI, no architecture, no
> code. Per [CLAUDE.md](../../../CLAUDE.md) §2, scoping decisions belong to
> `docs/02-product/` and are **not made here**.

---

## How to read this document

| Label | Meaning |
|---|---|
| **FACT** | Verifiable and sourced, with the source document and section cited. A FACT is a fact *about what the cited research records*. |
| **ASSUMPTION** | Believed true but not verified. Every assumption states what would falsify it. |
| **HYPOTHESIS** | A proposed explanation or approach to be tested. Not a belief; a candidate for validation. |
| **OPPORTUNITY** | A place where a product could plausibly create value, with its counter-evidence attached. |
| **UNKNOWN** | Identified gap — not established by available evidence. Carried from the research documents by its original ID (`Q-n` domain, `SQ-n` SSB, `A-n`/`B-n`/`C-n`/`E-n` technology, `Q-n` competitors) wherever one exists. **An UNKNOWN is never a claim of absence.** |
| **PRODUCT MODEL** | A workflow or user structure IBVAP *may choose to design for*. **Not a claim about how any force actually works.** No PRODUCT MODEL is defined in this document. |

### FACT, UNKNOWN and PRODUCT MODEL — the distinction this document enforces

These three are kept strictly apart, because collapsing them is how an absence of
sources becomes an invented finding.

| Label | Means | Does **not** mean |
|---|---|---|
| **FACT** | Verified from an authoritative source and cited — for [SIH/SSB] findings that means MHA, SSB or other Indian government primary material; for [BORDER] and [GLOBAL] findings, the peer-reviewed, standards or vendor sources named at the point of use | That the matter is settled beyond what the cited source actually says |
| **UNKNOWN** | Not established by available evidence. Either the search was made and returned nothing, or no retrieved source addresses it | **That the thing does not exist.** Absence of public documentation is not evidence of operational absence, and is never recorded as a FACT of absence |
| **PRODUCT MODEL** | A workflow, user structure or role model IBVAP *may choose to design for*: a design construct, owned by `docs/02-product/` | A description of how SSB — or any force — actually operates. A PRODUCT MODEL is never evidence, and never becomes a FACT by being built on |

**No PRODUCT MODEL is defined in this document, and no user hierarchy is proposed
here.** The label is introduced now so that when one is written — in
`docs/02-product/`, per [CLAUDE.md](../../../CLAUDE.md) §2 — it is recognisable
as a design choice rather than as a research finding, and is labelled as such at
the point it is written
([ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §9, final
constraint).

### Scope labels

Per [CLAUDE.md](../../../CLAUDE.md) §4, every finding is scoped:

| Label | Meaning |
|---|---|
| **[SIH/SSB]** | True only for this problem statement or for Sashastra Seema Bal. |
| **[BORDER]** | True for border/frontier surveillance generally, in any country. |
| **[GLOBAL]** | True for intelligent video analytics on existing CCTV anywhere. |
| **[MARKET]** | Legal, procurement, connectivity or pricing factor that varies by country. |

### Two rules this document holds itself to

1. **A research gap is not a requirement.** An UNKNOWN means "we do not know",
   not "build the thing that would answer it". Gaps appear here as questions
   ([§13](#13-questions-that-must-be-resolved-before-prd)), not as capabilities.
2. **A capability named in the problem statement is a *requirement of the
   statement*, which is a different thing from a *problem worth solving*.**
   [§5](#5-required-sih-capabilities) records the former;
   [§6](#6-validated-problems) records the latter. They are deliberately kept
   apart, and they do not fully overlap.

### The attribution this document rests on

**FACT** — [problem.md](../../00-project/problem.md) records the statement text
verbatim but does **not** record the SIH organisation/department field. The SSB
research proceeds on the project owner's statement that **SSB is the department
named for PS 26187**, and flags this as an open process gap
([ssb-operational-context.md](../domain/ssb-operational-context.md), attribution
caveat; SQ-30).

**This matters more here than anywhere else in the research corpus**, because
users are department-specific in a way that camera protocols are not. If the
department attribution is wrong, [§1](#1-users) through [§4](#4-pain-points) of
this document are about the wrong force. The problem statement text itself says
only "border security forces", and is force-agnostic.

---

## 1. Users

The problem statement names only **"border security forces"**
([problem.md](../../00-project/problem.md)). Every role below is reconstructed
from the research, and each carries the evidence quality of its source.

### 1.1 The most important structural finding about users

**FACT [SIH/SSB]** — Two deliberate research passes — across the **SSB Act 2007
and SSB Rules 2009**, three MHA Annual Reports, parliamentary answers, a BPRD
project report, SSB's own website, publication corpus and full tender feed, court
records and six tender aggregators — **retrieved no description of an SSB control
room, operations room, video wall, monitoring roster, shift pattern or operator
establishment** ([ssb-operational-workflow.md](../domain/ssb-operational-workflow.md)
§3.2, §7.1, H-1; [ssb-operational-context.md](../domain/ssb-operational-context.md)
§7, §14.7). This is a FACT **about what the searches returned**, and about nothing
else.

**UNKNOWN [SIH/SSB]** — **The exact SSB CCTV/control-room workflow is not
publicly validated. Our research does not establish the absence of control rooms,
monitoring personnel, or surveillance workflows. It only establishes that the
exact workflow is not sufficiently documented in publicly accessible sources.**
(SQ-3; carried as **H-1** and **H-2** in
[ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §9.)

**The earlier framing in this document — that the primary user may not exist — is
withdrawn as too strong** (ibid. §0.3). The open question is *what the workflow
is*, **not** *whether there is one*. The research is also structurally unlikely
to answer it: Rule 9(4) places standing orders in the DG's hands and such orders
are not published (ibid. §7.2), so silence here is the expected condition rather
than a signal.

**FACT [BORDER]** — The equivalent role **is** documented for BSF: border-level
Control Rooms receive BOLD-QIT feeds and cue Quick Reaction Teams
([domain-research.md](../domain/domain-research.md) §2.1). That is
BOLD-QIT-specific, and the SSB research explicitly forbids carrying it across
([ssb-operational-context.md](../domain/ssb-operational-context.md) §16, item 7).

**FACT [GLOBAL]** — **Every commercial platform surveyed assumes a control room
exists** ([competitive-landscape.md](../competitors/competitive-landscape.md)
§10, G7).

Because the workflow is **unvalidated rather than known to be absent**, no user
model may be asserted here in either direction. Neither "an operator at a
console" nor "a Sub-Inspector at a post" is established for this force, and
neither may be written into this document as a finding. Whatever structure IBVAP
eventually designs for is a **PRODUCT MODEL**, belongs in `docs/02-product/`, and
must be labelled as one at the point it is written — it is **not** proposed here.

This single unknown (SQ-3) governs who the product is for, and therefore governs
almost everything downstream. **It must be answered before the PRD** — see
[§13](#131-blocking--the-prd-cannot-be-honest-without-these), B2.

### 1.2 User inventory

| # | User | Evidence | Scope | Status |
|---|---|---|---|---|
| **U1** | **BOP in-charge — Sub-Inspector.** Commands the lowest echelon that could have a camera on it | `[N8]` via [ssb-operational-context.md](../domain/ssb-operational-context.md) §3.2 | [SIH/SSB] | **FACT** (rank); **ASSUMPTION** that they are the video user |
| **U2** | **Check post in-charge — Head Constable.** Commands the node where lawful, high-volume crossing is processed | ibid. §3.2, §4.3 | [SIH/SSB] | **FACT** (rank) |
| **U3** | **Company / Battalion commander — Assistant Commandant / Commandant.** The assessing and deciding echelon | ibid. §3.2 | [SIH/SSB] | **FACT** |
| **U4** | **Monitoring operator.** Watches live video; subject to vigilance decrement at 20–35 min while observing 3–30 scenes | [domain-research.md](../domain/domain-research.md) §4.1 `[S9][S10]` | [BORDER] / [GLOBAL] | **FACT** that the role exists in the domain; **UNKNOWN** whether it exists in SSB (SQ-3) |
| **U5** | **Intelligence staff.** SSB is Lead Intelligence Agency for the Indo-Nepal border; ~650 field and staff agents; 25 Border Interaction Teams in plain clothes on high-risk routes; "Know Your Area" programme | [ssb-operational-context.md](../domain/ssb-operational-context.md) §1.1, §5.2, §6.2 | [SIH/SSB] | **FACT** (existence); **ASSUMPTION** that they would consume video-derived pattern data |
| **U6** | **Anti-Human Trafficking Unit staff.** Five SSB AHTUs; 316 trafficking cases and **531 victims rescued** in 15 months | ibid. §5.2, §12 `[N1][N8]` | [SIH/SSB] | **FACT** |
| **U7** | **Evidence custodian / handover officer.** Must produce a s.63 BSA certificate with a hash, signed by the device custodian **and** an expert, for footage handed to state police | ibid. §11.5; [domain-research.md](../domain/domain-research.md) §3.5 `[S29]` | [MARKET:IN] | **FACT** (the legal requirement); **UNKNOWN** whether the role is staffed (SQ-13) |
| **U8** | **Downstream case owner — state police / prosecutor.** Receives the case; did not produce the video | [ssb-operational-context.md](../domain/ssb-operational-context.md) §11.4 `[N17]` | [MARKET:IN] / [BORDER] | **FACT** (the handover); **ASSUMPTION** that video reaches them at all |
| **U9** | **Technical maintainer.** SSB has a Wireless & Telecom Training Centre as a standing formation; whether any cadre can install or repair IP camera and analytics infrastructure at a BOP is unknown | ibid. §7, §10.5; SQ-9 | [SIH/SSB] | **FACT** (formation); **UNKNOWN** (capability) |
| **U10** | **Procurement / modernisation staff (FHQ, MHA).** ₹5,001.63 crore allotted 2015-16 to 2025-26, ₹4,775.11 crore spent; MHA states no completion timeline is possible | ibid. §6.1 `[N3]` | [SIH/SSB] | **FACT** |
| **U11** | **Adjacent-agency consumers** — LPAI/Customs/Immigration at ICP Raxaul and Jogbani, NCB (narcotics), state police, intelligence agencies, and APF Nepal on joint patrols | ibid. §4.3, §9; SQ-14, SQ-23 | [SIH/SSB] / [BORDER] | **FACT** (they exist); **UNKNOWN** (whether they consume this video) |

### 1.3 Distinctions that must not be collapsed

**The buyer is not the user.** U10 procures; U1–U3 live with the result. The
research records a documented consequence of that gap: BSF requests for proposals
"allowed vendors to arrive at their own conclusions" rather than specifying
technical requirements ([domain-research.md](../domain/domain-research.md) §4.3),
and there is high reliance on external vendors with minimal oversight (ibid.).

**ASSUMPTION [BORDER]** — A product optimised for the procurement document and
not for the Sub-Inspector will be bought and not used. *Falsified by: evidence
that field units drive requirements in this force.*

**Detection and assessment are different jobs, done by different people.**
A sensor alarm is not an incident; a human must look at imagery to decide
([domain-research.md](../domain/domain-research.md) §3.2). Cameras exist as the
*assessment* medium for alarms raised by other means. A product that treats
"alert" and "incident" as the same object is designing for a role that does not
exist.

### 1.4 Non-users, recorded so they are not mistaken for users

- **The border population.** Tens of thousands cross the India–Nepal border
  daily under a treaty right
  ([ssb-operational-context.md](../domain/ssb-operational-context.md) §2.2
  `[N7][N13]`). They are the **subject** of the system, not its user, and their
  legal position is what makes several named capabilities contested
  ([§5](#5-required-sih-capabilities), [§11](#11-capabilities-to-exclude-for-now)).
- **SIH evaluators.** A real audience with real influence over what gets built,
  and **not an operational user**. Recorded explicitly because the strongest
  pressure to treat the eight-capability list as the product comes from this
  audience, not from any user. See [§5.4](#54-the-tension-this-creates).

---

## 2. User jobs

What each user is trying to accomplish, stated as the job — not as a feature.
Each job cites the evidence that it exists.

| Job | Who | Evidence | Label |
|---|---|---|---|
| **J1 — Know what is happening in my stretch, without watching it continuously** | U1, U2, U4 | Conventional CCTV requires continuous human observation ([problem.md](../../00-project/problem.md)); vigilance decays at 20–35 min ([domain-research.md](../domain/domain-research.md) §4.1) | **FACT** that the burden exists; **ASSUMPTION** that U1/U2 currently carry it |
| **J2 — Decide whether a thing I have been told about is real, fast enough to act** | U1, U3, U4 | The C2 function is "analyse and classify the threat" ([domain-research.md](../domain/domain-research.md) §1.3); assessment is distinct from detection (ibid. §3.2) | **FACT** |
| **J3 — Get the right people to the right place before the moment passes** | U1, U3 | BOP/Company-level **decision latency** named as a live problem by a senior SSB officer ([ssb-operational-context.md](../domain/ssb-operational-context.md) §3.2) | **FACT** |
| **J4 — Find the contraband, the currency, the trafficker — not the crossing** | U1, U2, U5, U6 | SSB's own achievement ledger: prohibited items 5,993 cases, narcotics 1,059, Indian currency 471, cattle 432, forest products 398, human trafficking 316. An **"Illegal Infiltrators (Foreigner)" category does exist — 24 cases — but is small against these major categories** ([ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2 C-2) | **FACT** |
| **J5 — Know my area: who uses this track, how often, with what** | U5 | LIA designation, ~650-agent intelligence wing, 25 BITs, KYA programme (ibid. §1.1, §5.2, §6.2) | **FACT** that the mission exists; **ASSUMPTION** that video would serve it |
| **J6 — Rescue victims, not just arrest traffickers** | U6 | 531 victims rescued vs 274 traffickers arrested in 15 months (ibid. §12) — the victim outcome is larger than the arrest outcome | **FACT** |
| **J7 — Hand a case to the police in a form that survives** | U1, U7, U8 | s.63 BSA requires a hash and two signatures ([domain-research.md](../domain/domain-research.md) §3.5); cases are handed to state police ([ssb-operational-context.md](../domain/ssb-operational-context.md) §11.4) | **FACT** (the requirement); **UNKNOWN** (current practice, SQ-13) |
| **J8 — Log what happened, somewhere that is not a paper register** | U1, U3 | "Real-time alert generation and **event logging**" is a named requirement ([problem.md](../../00-project/problem.md)); SIMS is MHA's national NDPS seizure database, not an SSB logging system ([ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2 C-1, §5) | **FACT** (the requirement); **ASSUMPTION** that current logging is manual ([domain-research.md](../domain/domain-research.md) §3.4) |
| **J9 — Keep the kit working when I cannot reach it and cannot fix it** | U1, U9 | 308 of 734 BOPs lack road connectivity; generators where there is no grid; lack of technical expertise documented ([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.1, §10.2; [domain-research.md](../domain/domain-research.md) §4.3) | **FACT** |
| **J10 — Show that the money bought something** | U10 | GAO found Border Patrol had not used available data to determine surveillance technology's contribution, and found ~500 recorded "asset assists" from towers in a sector that has none ([domain-research.md](../domain/domain-research.md) §4.4) | **FACT** (US analogue); **ASSUMPTION** for SSB (ibid.; [ssb-operational-context.md](../domain/ssb-operational-context.md) §12.1) |

**ASSUMPTION [SIH/SSB]** — **J4 and J5, not J1, are the jobs this force is
actually measured on.** MHA records SSB's output as *cases and persons arrested
per contraband category* — a case/arrest ledger, not an alarm log
([ssb-operational-context.md](../domain/ssb-operational-context.md) §8.1, §12).
*Falsified by: any SSB reporting instrument that counts detections, alarms or
crossings.*

---

## 3. Current workflow

### 3.1 The workflow the problem statement begins from [GLOBAL]

**FACT** — Conventional CCTV provides **video recording and live monitoring**,
requiring **continuous human observation**
([problem.md](../../00-project/problem.md)). A human watches; a recorder records.

### 3.2 The SSB workflow, as far as the research establishes it [SIH/SSB]

**FACT** — SSB's surveillance repertoire is **patrol- and post-based**: a layered
grid of BOPs at ~3.9 km spacing, area domination patrols, manned naka and check
posts, joint patrols with APF Nepal (5,841 in FY 080/81, up from 78 in FY
071/72), observation posts, plain-clothes Border Interaction Teams, and AHTUs
([ssb-operational-context.md](../domain/ssb-operational-context.md) §4.2, §5.2).

**FACT** — Cross-border coordination with APF Nepal is **scheduled, not
event-driven** — annual/semi-annual at DG level down to fortnightly at
Company/BOP level — and an SSB officer states there are "still gaps in real-time
information exchange that hinder proactive security responses" (ibid. §8.1).

**FACT** — **SIMS is the Seizure Information Management System, an MHA e-portal
launched in 2019 for pan-India digitisation of NDPS drug-seizure data**, used by
all drug-law-enforcement agencies empowered under the NDPS Act, 1985 — SSB among
them, alongside BSF, Indian Coast Guard, RPF and NIA
([ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2 C-1,
§5). **It is not an SSB system and not a command-and-control or surveillance
system**; it records national drug-seizure outcomes, not detections. No
candidate for "existing command and control systems" on this border has been
identified (ibid. §5).

**FACT** — Cases end with **handover to the local police station** (ibid. §11.4).
SSB's jurisdictional belt is **15 km** under the SSB Act, 2007 — not the BSF's
50/80 km (ibid. §11.2).

**ASSUMPTION** — **Human presence, not electronic sensing, is SSB's primary
surveillance instrument today.** Every mechanism named in the sources is a
person; cameras appear as procurement line-items, never as the described method
(ibid. §5.2). *The research states this is an argument from silence.* **It is a
statement about what the sources describe, not a finding that camera-led
monitoring is absent.** *Falsified by: SQ-17 — any evidence of camera-led
monitoring.*

**UNKNOWN** — **Whether monitoring is staffed and rostered, local and incidental,
or something else entirely, is not established.** The earlier assumption on this
point — that monitoring is "local and incidental, a screen at a post watched by
whoever is on duty, rather than a staffed control room with a roster" — rested
wholly on silence in the sources, and silence does not support it (ibid. §7;
[ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §3.2, H-1).
It is therefore **withdrawn as an assumption and recorded as an UNKNOWN**.
*Resolved only by SQ-3 / B2, put to the force.*

### 3.3 The BSF workflow, recorded as contrast only [BORDER]

**FACT** — Documented for BOLD-QIT: feeds reach BSF Control Rooms, which cue QRTs
to intercept ([domain-research.md](../domain/domain-research.md) §1.3, §2.1). The
US analogue sequence is **detect → track → identify/classify → resolve** (ibid.
§3.2).

**This chain must not be assumed for SSB.** No SSB control room and no SSB QRT
construct is **documented in any source retrieved**
([ssb-operational-context.md](../domain/ssb-operational-context.md) §16, item 7;
[ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §3.2, §4.2,
H-1, H-4; SQ-12). **UNKNOWN, not absent.** The BSF chain is unavailable as
evidence *for* an SSB equivalent, and its undocumented status is equally
unavailable as evidence *against* one.

### 3.4 What is genuinely unknown about the current workflow

SQ-3 (whether live monitoring is performed and at which echelon — **unvalidated
in either direction**, not disproved), SQ-4 (the actual
detection → assessment → response sequence, and whether an SOP exists), SQ-12
(who responds, and what carries the alert to them), Q-11/Q-12 (SOP and
response-time targets). SQ-5 (what SIMS is, technically) is now resolved — SIMS
is MHA's national NDPS seizure database, not an SSB system
([ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2 C-1)
— but the broader question of what SSB's "existing command and control systems"
are remains open (ibid. §5).

**Five of the seven blocking SSB questions are about the workflow, not the
technology.** That is the shape of this discovery.

---

## 4. Pain points

Each pain point states **whose** pain it is and **how well evidenced** it is.
Ordered by evidence strength, not by how appealing they are to solve.

### 4.1 Well-evidenced

| # | Pain | Whose | Evidence | Scope |
|---|---|---|---|---|
| **PP1** | **Continuous observation does not work.** Vigilance decrement onsets at 20–35 min; operators watch 3–30 scenes; system effectiveness is bounded by operator detection ability | U4 (**if the role exists**) | [domain-research.md](../domain/domain-research.md) §4.1 `[S9][S10]` — peer-reviewed | [GLOBAL] |
| **PP2** | **Alerting systems are not trusted.** SBInet: 90% of sensor alerts were false alarms. CIBMS analysis names false alarms and sensor malfunction as a leading technical issue, and notes the design defines no protocol for distinguishing infiltrators from wildlife | U1, U3, U4 | ibid. §4.2 `[S1][S2]` | [BORDER] |
| **PP3** | **The point of capture is not technical.** BOP = Sub-Inspector, check post = Head Constable; lack of technical expertise for equipment operation and maintenance is a documented deficiency | U1, U2, U9 | [ssb-operational-context.md](../domain/ssb-operational-context.md) §3.2; [domain-research.md](../domain/domain-research.md) §4.3 | [SIH/SSB] / [BORDER] |
| **PP4** | **The site cannot be reached.** 308 of 734 BOPs lack road connectivity; generators where there is no grid, with fuel travelling the same unroaded path; a parliamentary committee noted lack of electricity at SSB and ITBP BOPs specifically | U1, U9, U10 | [ssb-operational-context.md](../domain/ssb-operational-context.md) §10.1, §10.2 `[N9][N18]` | [SIH/SSB] |
| **PP5** | **Decisions are slow at the echelon nearest the event.** BOP/Company-level decision latency named directly by a senior SSB officer, with more autonomy at lower levels named as the remedy. Separately, CIBMS analysis flags that centralised decision-making may delay urgent field responses | U1, U3 | ibid. §3.2; [domain-research.md](../domain/domain-research.md) §3.6 | [SIH/SSB] / [BORDER] |
| **PP6** | **Nobody can say whether the technology helped.** GAO found Border Patrol had not used available data to determine surveillance technology's contribution, and found ~500 recorded "asset assists" from towers in a sector that has none | U10, U3 | [domain-research.md](../domain/domain-research.md) §4.4 `[S12]` | [BORDER] |
| **PP7** | **Evidence has to survive a cross-organisational handover.** s.63 BSA (in force 1 July 2024) requires a certificate disclosing the record's **hash value**, signed by the device custodian **and** an expert. The custodian at the point of capture is an SI or HC, and 42% of posts have no road | U1, U7, U8 | [ssb-operational-context.md](../domain/ssb-operational-context.md) §11.5; [domain-research.md](../domain/domain-research.md) §3.5 `[S29]` | [MARKET:IN] |
| **PP8** | **What the force actually catches is overwhelmingly not intrusion.** MHA AR 2024-25 records an "Illegal Infiltrators (Foreigner)" category — 24 cases — but it is small against 3,649 prohibited/contraband cases and 1,026 narcotics cases. The three largest categories are prohibited items, narcotics and currency | U1, U5, U6 | [ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2 C-2 | [SIH/SSB] |
| **PP9** | **Real-time information exchange with the counterpart force is inadequate**, and coordination is calendar-driven | U3, U5 | ibid. §8.1 | [SIH/SSB] |
| **PP10** | **Night is the operational peak and the technical trough.** Visible-light detection scores mAP 0.430 vs 0.651 for infrared on the same night scenes — a 33.9% relative drop — while infiltration and smuggling are believed to concentrate in darkness | U1, U4 | [technical-feasibility.md](../technology/technical-feasibility.md) §3.10 `[T26]`; [domain-research.md](../domain/domain-research.md) §5.6 | [BORDER] |

### 4.2 Assumed, not evidenced — flagged as such

| # | Pain | Basis | Falsified by |
|---|---|---|---|
| **PP11** | **Event logging is manual; video retrieval is DVR-scrubbing** | Inference from the problem statement's framing ([domain-research.md](../domain/domain-research.md) §3.4). Not sourced | SQ-5, Q-9 — any digital incident register linked to video |
| **PP12** | **A camera-derived detection that produces no seizure has nowhere to go**, because SIMS is MHA's national NDPS seizure database, not an SSB system, and records outcomes only | [ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2 C-1, §5 | SQ-5 — SIMS accepting a machine-generated, non-seizure event |
| **PP13** | **Trafficking is the least-served event class by any named analytic.** A trafficked minor moving through a check post with an adult produces no intrusion, no unusual vehicle and no suspicious motion; the signal is relational and behavioural at a *lawful* crossing | ibid. §12.1 — explicitly recorded there as unsourced | Direct enquiry with U6 (AHTU staff) |
| **PP14** | **Cattle, porters and forest produce are targets, not nuisance alarms**, inverting the signal/noise assumption of a fenced border | ibid. §12.1 | SQ-18 — a measured nuisance profile on this border |

**The pain points with the strongest evidence (PP2, PP3, PP4, PP7) are all about
the *conditions of deployment*, not about detection quality.** That asymmetry is
the single most useful thing this synthesis produces.

---

## 5. Required SIH capabilities

These are **required by the immutable problem statement**
([problem.md](../../00-project/problem.md), [goals.md](../../00-project/goals.md)).
They are recorded here with their feasibility and their operational fit, because
requirement, feasibility and usefulness are three different questions.

### 5.1 The eight named capabilities

| # | Capability (as named in the statement) | Market status | Feasibility on **existing, non-purpose-mounted** CCTV | Operational fit on the validation border |
|---|---|---|---|---|
| 1 | Human detection and tracking | Shipping from every vendor surveyed | Detection **Moderate–High**; single-camera tracking **Moderate** (≥3 fps floor, occlusion); cross-camera **Low** | Fits — a person is the primitive every other job composes from |
| 2 | Vehicle detection and classification | Shipping from every vendor | Detection **Moderate–High**; coarse class **Moderate**; make/model/colour **Low** | Partial — the operationally relevant classes (porter's cart, load-carrying tractor-trailer, driven livestock) are **not** COCO or TrafficCamNet classes |
| 3 | Face detection | Shipping | **Low–Moderate** — overview cameras look down on the tops of heads; mounting geometry, and no model fixes it | Unclear — depends entirely on whether any camera sees faces at face-scale |
| 4 | ANPR | Shipping; **already solved software-only twice** (Genetec Flexreader ≤50 km/h; Milestone XProtect LPR ≤30° mounting) | **Low** on a general camera; **Moderate–High** on a lane-aimed camera. Needs ~250 px/m; India has ~210 m vehicles and 50+ plate types | Fits **at ICPs / check posts / barriers only**. Does not fit a wide-area border-road camera |
| 5 | Virtual fence intrusion detection | Shipping, including free open source | Mechanism **High**; **at an acceptable nuisance rate: Unproven** | **Poor fit.** Crossing is a **treaty right**; MHA's own statement of the problem is "misuse of open border", not intrusion. A line-crossing alarm that was 100% correct would still be almost entirely noise here |
| 6 | Suspicious activity detection | **No consensus solution in the market** | **Low** as a learned model; **Moderate** as explicit composite rules over reliable primitives | **Undefined.** The term is undefined in the statement and in every retrieved source (Q-3), and materially harder on an open border (SQ-7) |
| 7 | Night-time movement detection | **Not a distinct product feature anywhere in the market** — it is an operating condition | **Low–Moderate** on visible cameras; **High** on thermal, which most estates do not have | Highest operational weight, worst technical outlook — the "night inversion" |
| 8 | Real-time alert generation and event logging | Shipping | **High**, bounded by what the link can carry | Fits — and is the one capability whose presence *as a requirement* suggests it is currently absent or inadequate |

*(Sources for this table:
[competitive-landscape.md](../competitors/competitive-landscape.md) §4, §6.2,
§6.3; [technical-feasibility.md](../technology/technical-feasibility.md) §3, §11;
[ssb-operational-context.md](../domain/ssb-operational-context.md) §2.3, §12.1;
[domain-research.md](../domain/domain-research.md) §5.7, §6.7.)*

### 5.2 The seven required outcomes

From [goals.md](../../00-project/goals.md). Each is recorded with the research
finding that bears on it.

| Outcome | Bearing finding |
|---|---|
| Eliminate dependence on expensive dedicated surveillance hardware | **Half true, and already commercialised.** The dependency moved from the camera's silicon to the camera's *mounting* — Flexreader's 50 km/h, XProtect LPR's 30° ([competitive-landscape.md](../competitors/competitive-landscape.md) §6.2) |
| Enable intelligent monitoring through AI-powered video analytics | Achievable for presence-and-motion primitives; not for identity primitives on overview cameras ([technical-feasibility.md](../technology/technical-feasibility.md) §11) |
| Provide real-time alerts for security incidents and border intrusions | Achievable; the binding question is **nuisance rate**, not mechanism (ibid. §3.8) |
| Support facial recognition, vehicle identification and behavioural analytics **through software** | The capability most in tension with the deployment model. **NIST's own conclusion**: video FR can approach still-photo accuracy "**but only if image collection can be improved**" — camera positioning, mounting, lighting and optics, all of which are hardware (ibid. §3.5 `[T23b]`) |
| Improve situational awareness and response time | Fits PP5 directly. Note the counter-finding: centralising decisions may *delay* urgent field responses ([domain-research.md](../domain/domain-research.md) §3.6) |
| Support integration with existing command and control systems | **Ingest has standardised; egress has not** ([competitive-landscape.md](../competitors/competitive-landscape.md) §7.1). **SIMS has been eliminated as a candidate** — it is MHA's national NDPS seizure database, not an SSB system — and **no SSB command-and-control system has been identified** ([ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §5; SQ-5, SQ-6) |
| Cost-effective, scalable, suitable for remote deployment | **ASSUMPTION**: "scalable" here means *across many small isolated sites*, not to one large central cluster — the scaling axis is **site count** ([domain-research.md](../domain/domain-research.md) §6.5). Per-camera pricing, universal in the market, penalises exactly this shape ([competitive-landscape.md](../competitors/competitive-landscape.md) §9, P6) |

### 5.3 The three constraints

**FACT** — Must ingest live streams from standard IP-based CCTV; must **not**
require dedicated FRS/ANPR/smart-camera hardware; must use AI/ML/CV/video
analytics ([goals.md](../../00-project/goals.md)).

**FACT [SIH/SSB]** — The named department **has already procured** a "CCTV
Surveillance Setup with Automatic Face Recognition System with Auto Number Plate
Recognition" (MHA reply to Lok Sabha USQ 488, 3 February 2026)
([ssb-operational-context.md](../domain/ssb-operational-context.md) §6.1, §14.2).
Where it is deployed, whose software it is, and whether it exposes any stream or
API are all unknown (SQ-2).

**The problem statement's stated gap — that FRS and ANPR are absent because they
need dedicated hardware — does not hold unqualified for the named department.**
This is a research finding. What to do about it is a `docs/02-product/` decision.

### 5.4 The tension this creates

**Two audiences want different things, and this must be decided deliberately
rather than by drift:**

- The **SIH evaluation** rewards visible coverage of all eight named
  capabilities.
- The **operational user** (U1–U6) is measured overwhelmingly on contraband,
  currency, trafficking and third-country foreigners — the ledger's "Illegal
  Infiltrators (Foreigner)" category is only 24 cases against 3,649
  prohibited/contraband cases and 1,026 narcotics cases
  ([ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2
  C-2).

Capability 5 (virtual fence) is the sharpest case: technically easy,
operationally misdirected on this border. Capability 7 (night) is the inverse:
technically hardest, operationally heaviest.

**This document does not resolve the tension.** It records that the resolution is
a product decision, that it belongs in `docs/02-product/`, and that "build all
eight because they are listed" is one option among several — not the default.

---

## 6. Validated problems

A problem qualifies here only if the research supports **both** that it exists
**and** that it hurts someone identified in [§1](#1-users). Everything else is in
[§7](#7-assumptions).

| # | Validated problem | Evidence | Whose | Scope |
|---|---|---|---|---|
| **V1** | **Sustained human observation is not a reliable detection method.** Vigilance decays at 20–35 min across 3–30 scenes; system effectiveness is bounded by operator detection ability | Peer-reviewed `[S9][S10]` | U4 (**conditional on SQ-3**) | [GLOBAL] |
| **V2** | **A high-nuisance alerting system destroys its own value.** 90% false alarms is the documented precedent; operator reliance tracks system accuracy; CIBMS defines no protocol for separating infiltrators from wildlife | `[S1][S2][S10]` | U1, U3, U4 | [BORDER] |
| **V3** | **Identity-grade analytics are unreachable on cameras specified for overview.** DORI: Detection 25 px/m, Identification 250 px/m (per one source, 500 px/m in the 2025 revision). Software cannot manufacture missing pixels | `[C49][T8][T9]` | U1, U3 | [GLOBAL] |
| **V4** | **The deployment site defeats conventional architectures.** 42% of BOPs unroaded; generator power, fuel-limited, logistics-bound; satellite in the surveillance inventory; every appliance architecture imports a physical maintenance obligation at each site | `[N3][N9][N18]`; [competitive-landscape.md](../competitors/competitive-landscape.md) §8.5 | U1, U9, U10 | [SIH/SSB] / [BORDER] |
| **V5** | **The person at the point of capture is not a technician.** SI at a BOP, HC at a check post; documented lack of technical expertise for equipment operation and maintenance | `[N8]`; [domain-research.md](../domain/domain-research.md) §4.3 | U1, U2, U9 | [SIH/SSB] / [BORDER] |
| **V6** | **Video evidence must survive a handover to an organisation that did not produce it, under a statute demanding a hash and two signatures.** s.63 BSA, in force 1 July 2024 | `[S29]`; [ssb-operational-context.md](../domain/ssb-operational-context.md) §11.5 | U1, U7, U8 | [MARKET:IN] |
| **V7** | **Nobody can demonstrate what surveillance technology contributed.** GAO's finding, plus the data-quality failure that proves it (assists recorded from a sector with no such assets) | `[S12]` | U10, U3 | [BORDER] |
| **V8** | **The named force's actual event classes are overwhelmingly contraband, currency, trafficking and third-country foreigners, not intrusion.** MHA AR 2024-25's "Illegal Infiltrators (Foreigner)" category is real but small — 24 cases against 3,649 prohibited/contraband and 1,026 narcotics cases | [ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2 C-2 | U1, U5, U6 | [SIH/SSB] |
| **V9** | **Night is when it matters and when the technology is worst.** 33.9% relative detection drop, visible vs infrared, same scenes; and no vendor sells a night analytic | `[T26]`; [competitive-landscape.md](../competitors/competitive-landscape.md) §4.1 | U1, U4 | [BORDER] |
| **V10** | **"Suspicious activity" cannot currently be delivered as understood.** 94.55% AUC collapsing to 16.35% on same-scene reversed labels; FAR rising 42% on hard-normal sets, some >70%; human annotators agree only at Fleiss' κ 0.51–0.68; AUC insensitive to *when* detection occurs | `[T27]` | U1, U3, and the evaluators | [GLOBAL] |

**V1 is conditional, and must stay marked as such.** It is the strongest
peer-reviewed pain in the corpus and it may not apply to the named user at all,
because SQ-3 is unanswered. **Building for V1 before answering SQ-3 is the single
most likely way to build the wrong product.**

---

## 7. Assumptions

Beliefs the product would rest on if it proceeded today. Each states what would
falsify it. **None of these is a fact, and none should be quoted as one.**

| # | Assumption | Basis | Falsified by |
|---|---|---|---|
| **A1** | SSB is the department for PS 26187 | Project owner's statement; the SIH organisation field is not recorded | Recording the actual SIH department field (SQ-30) |
| **A2** | **Withdrawn — replaced by an UNKNOWN.** The earlier assumption ("SSB has no staffed video control room; monitoring is local and incidental") rested on an argument from silence and is not carried forward. What stands in its place is not an assumption of absence but a gap: the SSB CCTV/control-room workflow is not sufficiently documented in publicly accessible sources ([§1.1](#11-the-most-important-structural-finding-about-users)) | Argument from silence across `[N1][N2][N8]` — **insufficient**; superseded by [ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.3, H-1 | Not applicable: nothing is now assumed here. SQ-3 / B2 resolves the gap in **either** direction |
| **A3** | Existing border cameras were specified for Detection/Observation density (25–62 px/m), not Identification | DORI, plus the finding that existing CCTV was installed for live viewing | SQ-1 / A-1 — a measured site survey |
| **A4** | Uplinks at these sites are of the order of hundreds of kbps, or intermittent, or satellite | Satellite phones in the surveillance inventory; peer-reviewed constrained-edge findings | SQ-11 / A-3 |
| **A5** | Continuous compute at a generator-powered, unroaded site is a fuel-logistics cost, not just an electrical one | Road and generator findings combined | SQ-10 / A-4 |
| **A6** | Event logging today is manual/register-based; retrieval is DVR-scrubbing | Inference from the statement's framing | SQ-5, Q-9 |
| **A7** | A camera-derived detection that yields no seizure has no home in existing systems | SIMS is MHA's national NDPS seizure database, not an SSB system, and is seizure-framed | SQ-5 |
| **A8** | On this border, cattle, porters and forest produce are *targets*, not nuisance alarms — the signal/noise split differs in kind from a fenced border | SSB's own seizure categories | SQ-18 |
| **A9** | Trafficking detection is the event class least served by the named analytics | Explicitly unsourced in the research | Enquiry with U6 |
| **A10** | The buyer/user gap will cause a procurement-optimised product to go unused | Documented RFP and vendor-oversight weaknesses | Evidence that field units drive requirements |
| **A11** | "Scalable" means many small sites, not one big cluster | The statement's own phrase "across remote border locations" | Direct clarification |
| **A12** | Per-camera pricing, universal in the market, is a poor fit for a many-small-sites estate | Market pricing survey plus the estate shape | Actual pricing data (competitors Q-1) |
| **A13** | An untrusted alerting system is worse than none, because it consumes attention and supplies false assurance | Inference from the operator-reliance finding | An operator study on this estate |
| **A14** | IR-illuminated night video is effectively monochrome, so every colour-dependent mechanism degrades at night | Physics of IR illumination; not stated in a retrieved source | Directly testable on the rig (E-6) |

---

## 8. Opportunities

**Nothing here is a requirement.** Each entry pairs the opening with the reason
it may be thin *on purpose*, per the competitive research's own discipline
([competitive-landscape.md](../competitors/competitive-landscape.md) §10).

| # | **OPPORTUNITY** | Evidence for | Evidence against | Scope |
|---|---|---|---|---|
| **O1** | **Honest per-camera capability disclosure** — tell the operator, measured from the actual stream, which analytics this camera can and cannot support at this mounting, in the spirit of i-LIDS' primary-vs-secondary certification | No vendor examined ships this as a runtime feature; Genetec ships a *calculator* only. It is unusually well-aligned with the pixels-on-target reality | Vendors have a commercial incentive not to publish per-camera limitations. It also means telling a buyer their estate cannot do what they hoped | [GLOBAL] |
| **O2** | **Disconnected-by-default operation as a designed property**, decomposed into its four independent parts: analytics keep running; events queue and reconcile idempotently; licensing does not expire; time stays trustworthy | Only Irisity states air-gapped support; only Milestone documents offline licensing; for Genetec, BriefCam, Videonetics, AllGoVision and Ipsotek this is **undocumented** — the competitive survey's own "single most important unknown" | On-premise VMS has always run offline; this may be table stakes rather than a differentiator | [BORDER] |
| **O3** | **A published, measured nuisance-alarm rate with a cause histogram** — the number the entire market declines to publish | P10, the disclosure asymmetry: bandwidth and GPU models are published; accuracy, false-alarm rates and power are not. The experiment is cheap (7 days on the existing rig) | Publishing a real FAR invites unfavourable comparison with vendors who publish nothing | [GLOBAL] |
| **O4** | **A published power budget per camera per analytic** | **Zero** vendors in the survey publish watts, even while mandating specific NVIDIA GPUs. At a fuel-limited site this is a first-order constraint | May be unmeasured rather than unsolved; edge NPU cameras are already low-power | [BORDER] |
| **O5** | **Alerting sized to a two-person post** — event record plus a small crop in real time, full clip fetched on demand | Every platform surveyed assumes a control room, a video wall and an operator hierarchy; Smart Wall is a premium-edition feature. Arithmetic: a 15 s 1080p clip = 7.8 min on 128 kbps; a 320×320 crop = 1.6 s — **a factor of ~300** | Mobile clients exist everywhere. And whether the target force even *has* a control room is itself unknown (SQ-3) | [BORDER] |
| **O6** | **Evidentiary integrity at the cheapest tier** — hash-chained events, signed exports and tamper-evidence as a default rather than an edition upgrade | Milestone gates media encryption and signing to Expert/Corporate and Evidence Lock to Corporate; Genetec's first encryption certificate costs 30% of Archiver capacity. **The smallest, most remote deployments are exactly the ones that get none of it** — and those are the deployments here | These are pricing decisions, not absent features. And a wrong clock at a disconnected site silently invalidates the whole chain | [MARKET:IN] / [BORDER] |
| **O7** | **Standards-based egress that already exists and nobody uses.** ONVIF **Profile M** defines metadata for vehicle, licence plate, face, body and geolocation with MQTT delivery; **MISB ST 0903 (VMTI)** inside STANAG 4609 defines per-frame detections with bounding boxes, geolocation, track IDs and confidence, and NATO-compatible C2 systems already ingest it. **No vendor in the competitive survey was found emitting either** | Egress is the unstandardised half of the market, and it is exactly what "integration with existing C2" means | The target C2 is unnamed (SQ-6). Building an adapter for a system that may not exist is the risk here | [GLOBAL] / [BORDER] |
| **O8** | **Pattern-over-time for an intelligence-led force** — who uses this track, how often, with what — rather than alarm-in-the-moment | SSB is the **Lead Intelligence Agency** for the Indo-Nepal border, with a ~650-agent intelligence wing, 25 BITs and the KYA programme. An intelligence-led force values pattern at least as much as alarm | **Directly adjacent to solved products** (BriefCam VIDEO SYNOPSIS, Avigilon Appearance Search, Ambient Pulsar). And on an open border, retaining records of lawful crossings may not be permissible at all (SQ-8) | [SIH/SSB] / [BORDER] |
| **O9** | **Deployment without a certified integrator and without a site survey**, on an estate nobody else will touch | Certification is priced at 2–3 days and USD 595–2,995; Ipsotek shipped a whole product variant for "repeatable, plug-and-play" rollout | **DORI physics means some estates genuinely cannot be made to work**, and a product that hides that fails in the field. This opportunity only works *paired with* O1 | [BORDER] |
| **O10** | **Failure modes a non-specialist can recognise and report** — specifically *degraded analytic quality*: a camera still streaming but no longer usable for its configured analytic (dirt, web, condensation, IR hotspot, drift, refocus) | Stream-loss alerts and camera-integrity monitors exist; nothing found addresses silent analytic degradation. Pairs directly with PP3 and PP5 | May exist under product names not searched | [BORDER] |
| **O11** | **A cost structure for many small, low-utilisation sites** | Per-camera pricing is universal; the smallest Verkada bridge is USD 2,999 for 10 channels | **The competitor at the bottom of this market is open source, not Genetec.** Frigate is free and does person/vehicle detection, virtual fence, alerting and event logging today | [BORDER] |

### 8.1 Opportunities that are not opportunities — do not chase these

**FACT** — Already solved, per
[competitive-landscape.md](../competitors/competitive-landscape.md) §10.1: ANPR
without dedicated ANPR cameras; analytics on existing third-party cameras;
natural-language video search; rapid forensic review of long recordings; AI
false-alarm reduction; privacy-preserving redaction; multi-site metadata
aggregation; cloud video on low bandwidth; open APIs into a VMS; camera tamper
detection.

**And the discipline the competitive research demands, restated:** *do not assume
the incumbents are expensive because they are inefficient.* Genetec's cost buys
federation, failover, encryption, audit, certification and a support
organisation; the encryption alone costs 30% of Archiver capacity. **Anything
cheaper is trading something away, and the trade must be named, not hidden.**

---

## 9. Potential differentiation

### 9.1 What IBVAP cannot differentiate on

**FACT** — All eight named capabilities are shipping products from multiple
vendors today. **There is no capability gap**
([competitive-landscape.md](../competitors/competitive-landscape.md) §4.1,
lesson 1).

Therefore, ruled out as differentiators:

- **Detection accuracy.** Competing here means being measured against vendors
  with decades of tuning, on benchmarks nobody publishes anyway (competitors
  Q-2).
- **The feature list.** Every row of it is commodity.
- **Price alone.** The floor competitor is **free** (Frigate). "Cheaper than
  Genetec" is not a position; it is a description of open source.
- **"Works with any ONVIF camera."** Two of the best-resourced engineering
  organisations in this market both built per-model compatibility labs and still
  warn buyers. Asserting universal support is a claim about intent, not
  capability.
- **"Indian-tuned models."** Videonetics already claims exactly this — models
  that "work well with facial features of the Indian subcontinent" — as its
  stated differentiator in this market.

### 9.2 Where differentiation is plausible

Each of these is a **HYPOTHESIS**, not a decision.

| # | **HYPOTHESIS** | Why it might hold | What would kill it |
|---|---|---|---|
| **D1** | **Honesty is the feature.** A platform that measures and states, per camera, what it can and cannot do — and refuses to claim identity-grade analytics on Detection-grade cameras (O1 + O3 + O10) | Nobody ships it; the physics guarantees it will often be needed; and it converts the product's biggest weakness (inherited cameras) into its most credible claim | If buyers reward the claim over the truth — which the RFP finding suggests they might |
| **D2** | **The smallest deployable unit is the product.** Not a control room, not a cloud tenant: a post with two cameras, a Sub-Inspector, a generator and an intermittent link | Every architecture surveyed assumes a control room or a cloud tenant. The estate here is 734 BOPs, 42% unroaded | If the force actually operates centrally, and this unit is not how they want to buy or run it (SQ-3, SQ-6) |
| **D3** | **Fit the ledger, not the fence.** Design around the event classes the force is actually measured on — contraband, currency, trafficking, third-country foreigners — rather than around intrusion | Primary-source evidence: the ledger's infiltration category (24 cases) is small against the major contraband/narcotics categories ([ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2 C-2) | The gap between "what a camera can see" and "what the ledger counts" may be unbridgeable by video alone. **A camera cannot see contraband inside a sack** |
| **D4** | **Disconnection as a designed property, published as four separable guarantees** (O2) | It is the competitive survey's own most important unknown about every incumbent | It may be table stakes that vendors simply do not document |
| **D5** | **Standards-based egress** (ONVIF Profile M / MISB ST 0903) instead of a bespoke adapter per C2 (O7) | Existing, vendor-neutral, already ingestible by NATO-compatible C2; nobody in the survey emits it | If the actual target C2 (SQ-6) speaks neither, this is elegant and useless |
| **D6** | **Measured, published operating envelope** — nuisance rate, watts per analysed frame, latency decomposition, behaviour across a multi-day disconnection (O3 + O4) | These are exactly the four things the industry does not publish (P10) | Measurement on one rig is not measurement on the estate. The numbers must be honest about their sample |

**ASSUMPTION** — **The differentiator is the deployment, not the analytic.**
*(Basis: [§9.1](#91-what-ibvap-cannot-differentiate-on), plus the fact that the
best-evidenced pain points — PP2, PP3, PP4, PP7 — are all deployment conditions.
This is the competitive research's own question 2 to product discovery, and it is
the answer the evidence points to. It remains an assumption. Falsified by:
evidence that the estate can support identity-grade analytics and that detection
quality, not deployability, is what the user lacks.)*

---

## 10. Candidate capabilities

Classified as instructed: **MUST INVESTIGATE**, **STRONG MVP CANDIDATE**,
**LATER**, **DO NOT PURSUE**.

> **These are not MVP decisions.** A "STRONG MVP CANDIDATE" is a candidate the
> evidence supports carrying into scoping — not a committed feature. MVP
> selection happens in `docs/02-product/`.

### 10.1 Foundation

| Capability | Class | Rationale |
|---|---|---|
| RTSP/ONVIF ingest from existing IP cameras, read-only and non-degrading to the live estate | **STRONG MVP CANDIDATE** | Mandated by the statement's constraints. Note the market lesson: ONVIF conformance is insufficient — a tested-device record is part of the capability, not a nicety. Note also that a **safety test must pass first**: concurrent RTSP clients must not degrade the existing recorder (E-12) |
| Per-camera capability audit — measured px/m at operational range, achievable fps, codec, anamorphic detection, and a plain statement of which analytics this camera can support | **STRONG MVP CANDIDATE** | The unfilled market gap (O1); the precondition for every honest claim the product makes; answers A-1/E-1 as a by-product |
| Person detection (support-grade) | **STRONG MVP CANDIDATE** | The primitive every other job composes from; throughput is not the constraint (256 fps on an Orin Nano); feasibility Moderate–High |
| Vehicle detection and coarse classification | **STRONG MVP CANDIDATE** | Same; 419 fps on an Orin Nano. Coarse class only — attributes are Low |
| Single-camera multi-object tracking at ≥3 fps | **STRONG MVP CANDIDATE** | Required for any dwell, direction or count rule; the ≥3 fps floor is measured (AssA 43.6% → 27.8% between 3 and 1 fps) |
| Object-class-gated zone / line / direction / dwell rule engine (the **mechanism**) | **STRONG MVP CANDIDATE** | Strictly better than pixel-motion VMD, and it is the substrate an operator authors on top of. **The mechanism is trivial; the product is the nuisance rejection** |
| Local event log with tamper-evident record (hash-chained) and explicit time integrity | **STRONG MVP CANDIDATE** | Named in the statement (capability 8); required by s.63 BSA; O6. **A silent wrong clock is the worst version of the evidential risk** — time integrity is not optional |
| Local-first operation with store-and-forward, idempotent monotonically-identified events, bounded queue and a defined discard policy | **STRONG MVP CANDIDATE** | V4 + A4 + O2. At a site offline for days, **the queue will fill** — the discard policy is a first-class design object, not an edge case |
| Alert payload discipline: event record plus small crop in real time, full clip on demand | **STRONG MVP CANDIDATE** | Arithmetic, not opinion: a factor of ~300 on a 128 kbps link |
| Retrospective query over locally held event metadata (time, zone, class, camera) | **STRONG MVP CANDIDATE** | The cheap backbone of J5 and J8; costs almost nothing once events exist. Note the adjacency to solved forensic-search products — the claim must stay modest |
| Degraded-analytic-quality detection and reporting (dirt, web, condensation, IR hotspot, refocus, drift) in language a Sub-Inspector can act on | **STRONG MVP CANDIDATE** | O10 + PP3 + V5; nothing found in the market addresses it |

### 10.2 Must investigate before any commitment

| Capability | Class | What must be answered first |
|---|---|---|
| Virtual fence **as an operational concept** on this border | **MUST INVESTIGATE** | SQ-7 / Q-3. Crossing is lawful; a perfect line-crossing alarm is still noise here. The *mechanism* is above; the *framing* is not decided |
| "Suspicious activity" as **operator-authored composite rules** over reliable primitives (e.g. "person in zone A, 2200–0500, >90 s"; "vehicle stopped on the border road outside a lay-by >5 min") | **MUST INVESTIGATE** | A-8 / Q-3 — what suspicious means, stated as observable behaviour. **No experiment substitutes for this answer.** The research records this shape as a HYPOTHESIS, explicitly not a recommendation |
| Night-time analytics on the estate's actual night imagery (IR-illuminated visible, or thermal) | **MUST INVESTIGATE** | Q-15 / SQ-1 — what fraction is thermal, and whether visible cameras have IR illuminators, true day/night sensors, or neither. Then E-6 on real footage |
| Measured nuisance-alarm rate as a **product feature** (rate plus cause histogram, per camera, shown to the operator) | **MUST INVESTIGATE** | Cheap to run (7-day unattended run on the existing rig, E-5); the research calls it "the single most valuable experiment on the list". Whether it belongs in the product surface or only in the engineering record is a product question |
| ANPR **at lane-aimed nodes only** — ICP Raxaul/Jogbani, check posts, barriers | **MUST INVESTIGATE** | SQ-14 (who owns ICP CCTV and does the force have access), SQ-2 (the already-procured ANPR stack), and whether a lane-aimed camera exists at all. Already solved twice in the market — entering here means matching Flexreader/XProtect LPR, not beating them |
| Non-standard object classes the ledger actually contains — loaded porter, cart, driven livestock, timber load | **MUST INVESTIGATE** | D3's viability turns on this. These are not COCO or TrafficCamNet classes; training data is the open question |
| Evidence export package satisfying s.63 BSA (hash preserved through export, no re-transcode, custodian and expert signature workflow) | **MUST INVESTIGATE** | SQ-13 — current practice, who signs, who is "expert". **Transcoding changes the hash**, so this constrains the whole media path |
| Egress format: ONVIF Profile M over MQTT, MISB ST 0903 VMTI, plain webhook | **MUST INVESTIGATE** | SQ-5, SQ-6, A-5 — the target C2 is unnamed. A spike (experiment 10) is warranted; an adapter is not |
| Pattern-over-time / route-usage analytics for intelligence use (O8) | **MUST INVESTIGATE** | SQ-8 — whether records of lawful crossings by treaty-protected nationals may be retained at all. **This is a legality question before it is a product question** |
| Whether the product's alerting posture is **primary (sole)** or **secondary (support)** in i-LIDS terms | **MUST INVESTIGATE** | Determines alerting, staffing and liability. The competitive research names this as a choice that "should be made deliberately rather than by default" |

### 10.3 Later

| Capability | Class | Why not now |
|---|---|---|
| Cross-camera tracking / person re-identification | **LATER** | Feasibility **Low**; re-ID degrades badly out of domain; fixed cameras with no overlap give no geometric constraint to exploit |
| Face recognition against a **bounded watchlist** (tens of known traffickers), if and only if a legal basis and a gallery exist | **LATER** | Technically a different and easier problem than open-set identification, and NIST's own advice is to limit gallery size. But SQ-8 (legal basis on a treaty-open border) and A-9 (does a gallery exist) are both unanswered |
| Multi-site aggregation / federation to a higher echelon | **LATER** | "Process locally, ship metadata" is settled practice, not an opening. Also gated on SQ-3 and SQ-6 — we do not know which echelon would host it |
| Mobile / handheld alert client | **LATER** | Plausible fit for a post with no console (D2), but mobile clients exist everywhere in the market, and the connectivity profile (SQ-11) decides whether it is even usable |
| Body-worn camera ingest | **LATER** | SSB reportedly uses them, but retention and central handling are unknown (SQ-22) |
| Video synopsis / rapid forensic review | **LATER** | Solved since before 2018 by BriefCam. Not a place to start |
| Automatic bidirectional C2 integration | **LATER** | The target does not have a name yet (SQ-6) |
| PTZ control / slew-to-cue | **LATER** | Stable-background analytics are invalid while a PTZ moves; this is an interaction to design after the primitives are trusted |
| UAV / drone video ingest | **LATER** | SSB operates UAVs, so the feed exists — but nothing in the research establishes a job for analysing it, and the problem statement does not name it |

### 10.4 Do not pursue

| Capability | Class | Why |
|---|---|---|
| Learned anomaly detection as the delivery of "suspicious activity" | **DO NOT PURSUE** | 94.55% AUC → 16.35% on same-scene reversed labels; FAR +42% on hard-normal sets, some >70%; contested ground truth (κ 0.51–0.68); AUC insensitive to detection timing. Three independent failures, all measured |
| Open-set face identification of the border population | **DO NOT PURSUE** | Legally unresolved on a treaty-open border (SQ-8); prohibited by default for law enforcement in publicly accessible spaces under EU AI Act Art. 5 (a **[MARKET]** capability, not a universal one); and NIST's precondition — improve image collection — is exactly what this deployment model forbids |
| ANPR on wide-area border-road cameras | **DO NOT PURSUE** | A plate at that range and angle is far below the required pixel density. Physics, not effort |
| Full video egress to a central site | **DO NOT PURSUE** | Arithmetic: not possible at these link speeds. The whole market has already converged away from it |
| Replacing the existing recorder / VMS layer | **DO NOT PURSUE** | Outside the statement's scope, multiplies the deployment burden at exactly the sites that cannot absorb it, and puts the product in direct competition with the incumbents' strongest ground |
| Cloud-dependent SaaS as the primary deployment mode | **DO NOT PURSUE** | Contradicts V4 and A4 outright, and data-classification / network policy for border video is entirely unestablished (Q-18 / A-10) |
| Competing on published detection-accuracy benchmarks | **DO NOT PURSUE** | See [§9.1](#91-what-ibvap-cannot-differentiate-on). Benchmarks in this market are unpublished, paywalled, or scene-overfitted |
| Drone / counter-UAS detection | **DO NOT PURSUE** | Not named in the problem statement; not a documented event class on the SSB borders; and fixed ground CCTV is geometrically poorly positioned for it |
| Tunnel detection | **DO NOT PURSUE** | Out of reach of surface video analytics; not a documented SSB event class |

---

## 11. Capabilities to exclude for now

Distinct from [§10.4](#104-do-not-pursue): these are things it would be
*reasonable* to want, which should nevertheless stay out of an MVP conversation
until something specific changes.

| Excluded | Until |
|---|---|
| **Anything whose value depends on a control room existing** — video wall, operator hierarchy, multi-operator workflow, shift handover | SQ-3 is answered |
| **Anything whose value depends on a named C2 system** — adapters, bidirectional sync, alarm-acknowledgement round-trips | SQ-5 / SQ-6 name the target |
| **Any biometric processing of the border population** | SQ-8 establishes a legal basis, authorisation level, retention rule and oversight |
| **Any claim of identity-grade capability (face recognition, ANPR) on the general estate** | A-1 / E-1 measures actual px/m and shows which cameras, if any, support it |
| **Retention of records of lawful crossings** | SQ-8 and the DPDP-applicability question are resolved |
| **Any published accuracy or false-alarm claim** | E-5 and E-6 have been run on real footage and the number is ours, measured |
| **Cross-border data sharing with APF Nepal** | SQ-23 establishes whether any legal basis exists |
| **Fine-grained vehicle attributes (make / model / colour)** | Someone establishes an operational job for them; colour is gone at night anyway |
| **A pricing model** | Competitors Q-1 yields a real price anchor. "Cheaper" is currently an untestable claim |

---

## 12. Product principles

Candidate principles, each traced to the finding that produced it. **These are
proposed, not adopted** — adoption is a `docs/02-product/` decision recorded in
`docs/00-project/decisions.md`.

| # | Principle | Traces to |
|---|---|---|
| **PR1** | **Measure, then claim.** Never assert a capability for a camera that has not been measured. Per-camera truth is stated to the operator, not hidden from them | V3, O1, D1 |
| **PR2** | **An alert must be worth the attention it costs.** Attention is the scarcest resource in this domain, and a nuisance alarm spends it while supplying false assurance | V1, V2, A13 |
| **PR3** | **Assume no link, no engineer, no certainty of power.** Every behaviour must have a defined answer for the disconnected, unattended, fuel-limited case — including what gets discarded when the queue fills | V4, V5, O2 |
| **PR4** | **Fail legibly to a Sub-Inspector.** Failure states must be recognisable and reportable over a radio or satellite phone by someone with no technical training | V5, PP3, O10 |
| **PR5** | **Evidence integrity is a default, never a tier.** Hashes, tamper-evidence and time integrity ship at the smallest deployment, because the smallest deployment is the one at the border | V6, O6 |
| **PR6** | **Do not detect what is not an offence.** On an open border the crossing is lawful; what is reportable is who, what they carry, and when and where | V8, SQ-8, §5.1 capability 5 |
| **PR7** | **Detection is not assessment.** The system's job is to bring a human to the right frame at the right time, not to decide. Which side of the i-LIDS primary/secondary line the product stands on is declared explicitly | [domain-research.md](../domain/domain-research.md) §3.2, §6.7 |
| **PR8** | **Never degrade the operational estate.** The existing recorder and live-view path keep working, unchanged, whatever the platform is doing — verified before anything touches a live site | E-12, PP4 |
| **PR9** | **Metadata crosses the link; video stays home.** Video moves only when a person asks for it | Arithmetic, [technical-feasibility.md](../technology/technical-feasibility.md) §5.3; market pattern P2 |
| **PR10** | **Say what it cannot do.** Per-camera limits, per-analytic limits, and the conditions under which each degrades, are product surface — not a support ticket | O1, D1, V3 |
| **PR11** | **Legality gates biometrics, not capability.** Face recognition is a market-specific capability with an unresolved legal basis here; it is switched on by a legal answer, never by a feature flag | SQ-8, EU AI Act Art. 5 |
| **PR12** | **Scale by site count, not by user count.** The unit of deployment is a small, isolated, hard-to-reach post — and the cost model must survive that shape | A11, A12, O11 |
| **PR13** | **Name the trade.** Anything cheaper than an incumbent is trading something away; the trade is stated, not hidden | [competitive-landscape.md](../competitors/competitive-landscape.md), "5 assumptions we must NOT make", item 5 |

---

## 13. Questions that must be resolved before PRD

Carried by their original IDs so the research trail stays intact.

### 13.1 Blocking — the PRD cannot be honest without these

| # | Question | Origin |
|---|---|---|
| **B1** | **Is the SIH department attribution actually SSB?** Record the organisation field for PS 26187 | SQ-30 |
| **B2** | **Does the force monitor live video at all, and at which echelon?** Operators, cameras per operator, shift pattern, instructions on seeing something | SQ-3 / Q-5 |
| **B3** | **What is the installed camera base?** Count and location by node type, make, model, resolution, codec, PTZ vs fixed, thermal vs visible, ONVIF conformance, age — and native IP vs analog behind a DVR/XVR with a shared encoder budget | SQ-1 / Q-1 / A-1 / A-2 |
| **B4** | **What does "suspicious activity" mean, stated as observable behaviour, on an open border?** No experiment substitutes for this | Q-3 / SQ-7 / A-8 |
| **B5** | **What are the "existing command and control systems", by name, with interfaces?** SIMS has been eliminated as a candidate — it is MHA's national NDPS seizure database (owner, hosting and data model now known via [ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2 C-1, §5) — so no SSB C2 system has yet been identified by name | SQ-6 / Q-4 / A-5 |
| **B6** | **Where is the already-procured FRS/ANPR CCTV setup deployed, what is it, and does it expose streams or APIs?** This determines whether IBVAP complements, replaces, or duplicates it | SQ-2 |
| **B7** | **What is the legal basis, authorisation level, retention rule and oversight for biometric processing of people exercising a treaty right of movement?** Does DPDP 2023 apply? | SQ-8 |

### 13.2 High priority — these shape scope

| # | Question | Origin |
|---|---|---|
| **H1** | What is the actual detection → assessment → response sequence, and is there a written SOP or Standing Order? | SQ-4 / Q-11 |
| **H2** | Is there a QRT construct, or is response by the patrol/naka already in the field? What carries the alert to them? | SQ-12 |
| **H3** | What connectivity exists at a post — any IP link, bandwidth, symmetry, metering, reliability, how many on satellite? | SQ-11 / Q-8 / A-3 |
| **H4** | What power is available for compute — generator hours, rating, fuel resupply interval, solar/battery — and what does an extra 15–60 W cost in logistics? | SQ-10 / Q-7 / A-4 |
| **H5** | What retention applies to video, clips and metadata separately, and is there a **time source** at a disconnected site? | SQ-13 / Q-9 / A-6 / A-7 |
| **H6** | What is the current export-and-handover procedure to state police, and does it satisfy s.63 BSA today — who signs, who is the "expert", is a hash computed? | SQ-13 / Q-10 |
| **H7** | Who owns and operates the CCTV at ICP Raxaul and Jogbani, and does the force have access? | SQ-14 |
| **H8** | What security accreditation, data classification and network policy applies to a platform handling live border video? Is cloud or internet permissible at all? | Q-18 / A-10 |
| **H9** | What is the real nuisance profile here, given that cattle, porters and forest produce are **targets** rather than nuisances? | SQ-18 / Q-6 |
| **H10** | Is the Indo-Bhutan border operationally the same problem as the Indo-Nepal border, or a different one? | SQ-25 |

### 13.3 Answerable without the force — by experiment or desk research

| # | Question | Origin |
|---|---|---|
| **X1** | What is the measured nuisance-alarm rate and cause histogram of an object-gated virtual fence over 7 unattended days on real footage? | E-5 / experiment 3 |
| **X2** | How do detection and tracking behave on IR-illuminated night footage from an ordinary camera? | E-6 / experiment 4 |
| **X3** | What is the analysis-rate floor on these scenes (25 / 10 / 5 / 3 / 1 fps)? | E-7 / experiment 6 |
| **X4** | Does adding concurrent RTSP clients degrade an existing recorder's own recording? **This must pass before anything touches a live estate** | E-12 |
| **X5** | Does the pipeline survive a 72-hour disconnection with events reconciling without duplication or loss, licences intact and clocks in tolerance? | E-11 / experiment 7 |
| **X6** | What does an analysed frame cost in joules, per accelerator? | E-10 / experiment 9 |
| **X7** | Does the market's pricing even permit a "cost-effective" claim to be tested? | Competitors Q-1 |
| **X8** | Verify the IEC/EN 62676-4:2025 pixel-density figures against the standard itself — a 2× change in the identification threshold is too consequential to carry on a secondary source | C-1 |

---

## The 5 strongest product opportunities

1. **Honest per-camera capability disclosure (O1 + O10 + D1).** Measure the
   actual stream and tell the operator which analytics this camera can support,
   which it cannot, and when it has silently degraded. Nobody ships it; the
   physics guarantees it is needed; and it converts the product's inherited
   weakness into its most defensible claim. **It is also the cheapest of these
   five to prove.**

2. **Disconnected-by-default operation, decomposed and guaranteed (O2).**
   Analytics keep running; events queue and reconcile idempotently; licensing
   does not expire; time stays trustworthy. This is the competitive survey's own
   *most important unknown about every incumbent*, and it is the deployment
   reality at 42% of the target sites.

3. **The smallest deployable unit as the product (D2 + O5).** A post with two
   cameras, one Sub-Inspector, a generator and an intermittent link — with
   alerting sized to that, not to a video wall. Every architecture surveyed
   assumes a control room; the estate here is 734 posts.

4. **Measured operating envelope, published (O3 + O4 + D6).** Nuisance rate with
   a cause histogram, watts per analysed frame, latency decomposition, and
   multi-day-disconnection behaviour. These are precisely the four things the
   entire industry declines to publish — and three of them can be measured on
   hardware this project already has.

5. **Evidentiary integrity at the cheapest tier (O6).** Hash-chained events,
   signed exports, explicit time integrity, no silent transcode — shipped by
   default rather than sold as an edition upgrade, in a jurisdiction where s.63
   BSA demands a hash and two signatures and the custodian is a Sub-Inspector at
   an unroaded post.

---

## The 5 biggest product risks

1. **We do not know how the user works.** The SSB CCTV/control-room workflow is
   not publicly validated (SQ-3) — which is **not** the same as knowing it is
   absent. Any product built around a specific monitoring posture, in either
   direction, rests on an unvalidated workflow; and any structure adopted before
   SQ-3 is answered is a **PRODUCT MODEL**, not a discovered fact. **This risk
   sits upstream of every other decision in this document**, and it is
   answerable by one question to the force.

2. **The estate may not physically support the named capabilities, and nobody has
   measured it.** If existing cameras deliver 25–62 px/m, face recognition and
   ANPR are unreachable at any software quality. The problem statement requires
   them anyway.

3. **Nuisance alarms make the system untrusted, which is worse than no system.**
   90% false alarms is the documented precedent; the environmental triggers
   (wind-moved vegetation, rain, fog, headlight glare, wildlife, IR-attracted
   insects) are all present; and on this border the usual "noise" categories are
   *targets*, so the standard mitigations may not transfer.

4. **The capability list and the operational reality point in different
   directions, and the pressure is to satisfy the list.** The force's ledger's
   infiltration category is real but small — 24 cases against 3,649
   prohibited/contraband and 1,026 narcotics cases; the statement's centrepiece
   is a virtual fence. Building all eight because they are listed is a
   decision — and if taken by default rather than deliberately, the result
   satisfies the evaluator and not the user.

5. **Night is the operational peak and the technical trough, and "night-time
   movement detection" is not a feature anyone sells.** A 33.9% relative
   detection drop on visible-light night imagery, against an operational belief
   that crossings concentrate in darkness. **The research names this inversion as
   the central risk of the whole programme until measured.**

---

## The 5 unresolved questions

1. **Is the department SSB, and does it monitor live video at all — where, by
   whom, on what roster?** (B1, B2 / SQ-30, SQ-3)
2. **What cameras are actually installed, at what resolution, mounting and px/m —
   and is there a recorder in front of them with a shared encoder budget?**
   (B3 / SQ-1, A-1, A-2)
3. **What does "suspicious activity" mean, as observable behaviour, on a border
   where crossing is lawful?** (B4 / Q-3, SQ-7)
4. **What is the "existing command and control system", by name — and can it
   accept a machine-generated detection rather than only a seizure outcome?**
   (B5 / SQ-5, SQ-6)
5. **What is the legal basis for processing biometrics of people exercising a
   treaty right of movement — and what happens to a template generated from
   someone who is never charged?** (B7 / SQ-8)

---

## Recommended next step

**Run a user-research pass to answer B1–B7, and run experiments X4 and X1 in
parallel, because they need nobody's permission.**

Concretely, in this order:

1. **Close B1 first** — record the SIH organisation/department field in
   `docs/00-project/`. It costs minutes, it does not touch the immutable problem
   statement, and it determines whether [§1](#1-users)–[§4](#4-pain-points) of
   this document are about the right force.
2. **Open a user-research document under `docs/01-research/users/` targeting
   B2–B7.** These are questions for people, not for a test rig, and five of the
   seven are about workflow rather than technology. Sources worth trying, named
   by the research itself: Parliamentary Standing Committee on Home Affairs
   reports, any CAG audit of SSB modernisation procurement, the MHA Annual Report
   2024-25 or later, the SSB Act 2007 and Rules 2009 text, and the official SSB
   website (SQ-26 through SQ-29).
3. **In parallel, run X4 (recorder safety), then X1 (7-day unattended
   nuisance-alarm run with a cause histogram)** on the existing rig. X4 is a
   safety precondition. X1 produces the single number the entire market declines
   to publish, needs nothing this project does not already have, and directly
   tests risk 3 above.
4. **Do not start the PRD until B2, B3 and B4 have answers — or explicit,
   recorded assumptions in their place.** If they cannot be answered, the PRD
   should state the assumption it substitutes and what would falsify it, per
   [CLAUDE.md](../../../CLAUDE.md) §3.7, rather than proceeding silently.

**Stop.**

---

## Document status

**Stage:** 01 — Research → Users / Product Discovery. Complete for this pass.

**What this document is:** a synthesis of the four research documents into users,
jobs, workflow, pain, opportunity and open questions.

**What this document is not:** a PRD, a feature list, an MVP decision, a design,
or an architecture. No capability in [§10](#10-candidate-capabilities) is
committed; no principle in [§12](#12-product-principles) is adopted; no
opportunity in [§8](#8-opportunities) is scoped.

**Known weaknesses:** the user model rests on A1 (the SSB attribution, itself
unrecorded); **whether the U4 monitoring role exists in this force is
unvalidated in either direction** (SQ-3), and this document asserts neither its
presence nor its absence; **no user of any kind has been spoken to in any
research pass to date**; and every pain point in [§4](#4-pain-points) is
documentary rather than observed.

**Revision, 2026-08-24 —** reinterpreted against
[ssb-operational-workflow.md](../domain/ssb-operational-workflow.md). The
conclusion *"the primary user may not exist"* is **withdrawn**; assumption **A2**
is withdrawn with it; and the **FACT / UNKNOWN / PRODUCT MODEL** distinction is
recorded above. Sections revised: the Inputs block, the label tables,
[§1.1](#11-the-most-important-structural-finding-about-users),
[§3.2](#32-the-ssb-workflow-as-far-as-the-research-establishes-it-sihssb),
[§3.3](#33-the-bsf-workflow-recorded-as-contrast-only-border),
[§3.4](#34-what-is-genuinely-unknown-about-the-current-workflow),
[§7](#7-assumptions) (A2), and product risk 1. **No PRD, no user hierarchy and no
PRODUCT MODEL was created in this revision.**

**Next stage gate:** per [CLAUDE.md](../../../CLAUDE.md) §2, `docs/02-product/`
may begin once B1–B7 are answered, or explicitly assumed with falsification
criteria recorded.

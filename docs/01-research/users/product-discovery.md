# Product Discovery — IBVAP

**Stage:** 01 — Research → Users / Synthesis
**Date:** 2026-08-24 (revised 2026-08-24 against
[ssb-operational-workflow.md](../domain/ssb-operational-workflow.md))
**Status:** Complete for this pass — a research synthesis, not a decision.
**Inputs:** [problem.md](../../00-project/problem.md),
[vision.md](../../00-project/vision.md), [goals.md](../../00-project/goals.md),
[domain-research.md](../domain/domain-research.md),
[ssb-operational-context.md](../domain/ssb-operational-context.md),
[ssb-operational-workflow.md](../domain/ssb-operational-workflow.md),
[competitive-landscape.md](../competitors/competitive-landscape.md),
[technical-feasibility.md](../technology/technical-feasibility.md).

This document synthesizes prior research into who IBVAP's users are, what
they are trying to do, what hurts, and what looks worth solving, to ground
scoping decisions in `docs/02-product/` (per [CLAUDE.md](../../../CLAUDE.md) §2).
An earlier pass argued the primary user "may not exist"; that framing is
withdrawn as too strong — the finding it rested on is an absence of public
documentation, not evidence of an absent workflow. Every place below that
could be misread as a claim of absence has been corrected; see
[§4.1](#41-users-and-organisational-roles).

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

This document reconstructs, from documentary research rather than direct
contact with any user, who is likely to use IBVAP at a Sashastra Seema Bal
(SSB) Border Out Post (BOP), what they are trying to do, and where the
strongest evidence of pain and opportunity lies.

**The single most consequential finding is a gap, not a discovery.** Two
research passes — across the SSB Act 2007 and SSB Rules 2009, three MHA Annual
Reports, parliamentary answers, a BPRD project report, SSB's own website,
publications and tender feed, court records, and six tender aggregators —
retrieved no description of an SSB control room, video wall, monitoring
roster, shift pattern or camera-operator establishment. This is a fact about
what the searches returned, not a fact about SSB's operations: standing orders
under Rule 9(4) sit with the Director-General and are not published, so this
silence is close to the expected condition rather than a signal of absence.
Whether SSB monitors live video at all, and at which echelon, is unresolved in
either direction (carried as **SQ-3**) and governs almost everything else in
this document — it must be answered, or explicitly assumed with a stated
falsification test, before a PRD can be written honestly.

**The force's own reporting shows its actual output is dominated by
contraband, narcotics, currency and trafficking — not border-crossing
interdiction.** MHA's 2024-25 Annual Report lists 5,993 cases of prohibited
items, 1,059 narcotics cases, 471 currency cases, 432 cattle cases, 398 forest
produce cases and 316 trafficking cases, against an "Illegal Infiltrators
(Foreigner)" category of just 24 cases. This creates a direct tension with the
problem statement's most prominent named capability — virtual-fence intrusion
detection — since crossing the India–Nepal border is itself a treaty right for
the tens of thousands of people who do so daily, and a perfectly accurate
crossing alarm would still be almost entirely noise on this border.

**The best-evidenced pain points concern the conditions of deployment, not the
quality of detection.** Continuous human video-monitoring is a documented,
peer-reviewed weak link (vigilance decays after 20–35 minutes across 3–30
scenes); comparable sensor systems have produced very high false-alarm rates
(90% in one documented US case) that erode operator trust; the person at the
point of capture is a Sub-Inspector or Head Constable, not a technician; 308 of
734 BOPs (42%) have no road access and run on generators; and a 2024 evidence
statute (BSA s.63) requires a hash-verified, dual-signed certificate before
footage can be handed to police — a requirement that lands squarely on an
under-resourced post. Night-time detection is the sharpest technical weak
point identified: visible-light detection scores 33.9% worse (relative) than
infrared on the same night scenes, precisely when infiltration and smuggling
are believed to concentrate.

**All eight capabilities named in the problem statement already ship from
multiple vendors; there is no capability gap in the market.** ANPR without
dedicated hardware and analytics layered on third-party cameras are both
already solved, shipping products. Where a genuine opening may exist is in
deployment characteristics the market does not currently sell or publish:
honest per-camera capability disclosure, verified disconnected operation,
evidentiary integrity as a default rather than a paid tier, and pricing suited
to many small, low-utilisation sites rather than one large estate.

**Risk is concentrated upstream of the technology.** The two largest risks are
that IBVAP is built around a monitoring workflow that does not match how SSB
actually operates (SQ-3), and that the deployment estate cannot physically
support the identity-grade analytics (face recognition, ANPR) the problem
statement names, because typical overview cameras fall well short of the pixel
density those tasks require. Both are answerable — one by asking the force,
the other by measuring the estate — and neither has been answered yet.

Seven blocking questions (**B1–B7**, [§7](#7-open-questions--research-gaps))
must be resolved, or explicitly assumed with a stated falsification test,
before product scoping proceeds.

---

## 2. Research Objective and Scope

**Objective.** To synthesize the domain, SSB operational-context/workflow,
competitive-landscape and technical-feasibility research into a first picture
of IBVAP's users, their jobs, their current workflow, their pain points, and
the questions that remain open — as an input to product scoping, not a
substitute for it.

**Out of scope for this document.** Feature decisions, UI, architecture, and
MVP selection. Where this document names candidate capabilities or principles
([§5](#5-implications-for-ibvap)), they are explicitly non-binding inputs to
`docs/02-product/`, not commitments.

**The attribution this document rests on.** [problem.md](../../00-project/problem.md)
records the SIH problem statement verbatim but does not record the SIH
organisation/department field. This research proceeds on the project owner's
statement that SSB is the department named for PS 26187, and flags this as an
open process gap (**SQ-30**). This matters more here than anywhere else in the
research corpus, because users are department-specific in a way that camera
protocols are not: if the attribution is wrong, [§4](#4-detailed-findings) of
this document is about the wrong force. The problem statement's own text says
only "border security forces" and is force-agnostic.

**Notation used throughout.**

- **Scope tags** — `[SIH/SSB]` true only for this problem statement or this
  force; `[BORDER]` true for border/frontier surveillance generally, in any
  country; `[GLOBAL]` true for intelligent video analytics on existing CCTV
  anywhere; `[MARKET]` a legal, procurement, connectivity or pricing factor
  that varies by country.
- **Citation keys** — bracketed codes such as `[N8]`, `[S9][S10]`, `[T26]`,
  `[C49]` are citation keys into the bibliographies of the underlying research
  documents (`N-` = ssb-operational-context.md, `S-` = domain-research.md,
  `T-` = technical-feasibility.md, `C-` = competitive-landscape.md). `SQ-`,
  `Q-`, `A-`, `B-`, `E-`, `H-` codes are open-question, assumption or
  experiment IDs carried from those same documents so the research trail
  stays traceable.
- **Confidence** — findings are stated in plain language as documented,
  believed-but-unverified, or unresolved, rather than tagged with repeated
  inline labels. Where a finding's evidentiary strength materially affects
  whether it should be acted on, that is said explicitly in the text.

**Two interpretive rules held throughout.** A research gap is not a
requirement — an open question means "we do not know," not "build the thing
that would answer it" (gaps appear in [§7](#7-open-questions--research-gaps)
as questions, not capabilities). And a capability named in the problem
statement is a *requirement of the statement*, which is a different thing from
a *validated operational problem* — [§5.1](#51-the-eight-named-capabilities)
and [§4.4](#44-pain-points) are kept distinct because they do not fully
overlap.

---

## 3. Key Findings

1. **SSB's CCTV/control-room workflow is not documented in any source
   examined** — an evidence gap, not an established absence (**SQ-3**;
   [ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §3.2,
   §7.1, H-1; [ssb-operational-context.md](../domain/ssb-operational-context.md)
   §7, §14.7).
2. **The equivalent role is documented for BSF and assumed by every commercial
   platform surveyed, but cannot be carried across to SSB.** BSF's BOLD-QIT
   feeds route to Control Rooms that cue Quick Reaction Teams
   ([domain-research.md](../domain/domain-research.md) §2.1); every vendor
   surveyed assumes a control room exists
   ([competitive-landscape.md](../competitors/competitive-landscape.md) §10,
   G7); the SSB research explicitly forbids importing the BSF construct
   ([ssb-operational-context.md](../domain/ssb-operational-context.md) §16,
   item 7).
3. **SSB's documented surveillance repertoire is patrol- and post-based, not
   sensor-based.** A layered grid of BOPs at ~3.9 km spacing, area-domination
   patrols, manned naka/check posts, joint patrols with APF Nepal (5,841 in FY
   080/81, up from 78 in FY 071/72), observation posts, plain-clothes Border
   Interaction Teams and Anti-Human Trafficking Units. Every mechanism named
   in the sources is a person; cameras appear only as procurement line items
   (ibid. §4.2, §5.2).
4. **SIMS is not a candidate command-and-control system.** It is the MHA's
   Seizure Information Management System, a 2019 e-portal for pan-India NDPS
   drug-seizure digitisation, shared by SSB, BSF, Coast Guard, RPF and NIA —
   not SSB-specific, and not a surveillance or C2 system
   ([ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2
   C-1, §5). No SSB command-and-control system has been identified by name.
5. **The force's actual case mix is contraband/narcotics/currency/trafficking,
   not border-crossing interdiction.** "Illegal Infiltrators (Foreigner)" is
   24 cases against 5,993 prohibited-items, 1,059 narcotics, 471 currency, 432
   cattle, 398 forest-produce and 316 trafficking cases (ibid. §0.2 C-2).
6. **The deployment estate is physically hard to reach.** 308 of 734 BOPs
   (42%) lack road connectivity; sites run on generators where there is no
   grid, with fuel travelling the same unroaded path
   ([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.1,
   §10.2).
7. **Continuous human video-monitoring is a documented, peer-reviewed weak
   link.** Vigilance decays after 20–35 minutes while observing 3–30 scenes,
   and system effectiveness is bounded by the human operator's own detection
   ability ([domain-research.md](../domain/domain-research.md) §4.1 `[S9][S10]`).
8. **Comparable sensor systems have produced very high false-alarm rates.**
   SBInet: 90% of sensor alerts were false alarms; CIBMS analysis names false
   alarms and sensor malfunction as a leading issue and defines no protocol
   for distinguishing infiltrators from wildlife (ibid. §4.2 `[S1][S2]`).
9. **Night-time detection is a sharp, measured weak point.** Visible-light
   detection scores 0.430 mAP vs 0.651 for infrared on the same night scenes —
   a 33.9% relative drop — while infiltration and smuggling are believed to
   concentrate in darkness
   ([technical-feasibility.md](../technology/technical-feasibility.md) §3.10
   `[T26]`).
10. **A 2024 statute makes video chain-of-custody a first-class requirement.**
    Bharatiya Sakshya Adhiniyam s.63 (in force 1 July 2024) requires a
    certificate disclosing the record's hash value, signed by both the device
    custodian and an expert, before footage can be used as evidence — and the
    custodian at the point of capture is typically an SI or HC, possibly at an
    unroaded post ([ssb-operational-context.md](../domain/ssb-operational-context.md)
    §11.5; [domain-research.md](../domain/domain-research.md) §3.5 `[S29]`).
11. **There is no capability gap in the market.** All eight capabilities named
    in the problem statement already ship from multiple vendors; ANPR without
    dedicated hardware and analytics on third-party cameras are already
    solved, shipping products
    ([competitive-landscape.md](../competitors/competitive-landscape.md) §4,
    §10.1).
12. **The named department has already procured a bundled FRS/ANPR CCTV
    system** (MHA reply to Lok Sabha USQ 488, 3 February 2026); where it is
    deployed and whether it exposes any usable interface is unknown (**SQ-2**;
    [ssb-operational-context.md](../domain/ssb-operational-context.md) §6.1,
    §14.2).
13. **Identity-grade analytics need far more pixel density than typical
    overview cameras deliver.** IEC/EN 62676-4 puts Detection at 25 px/m and
    Identification at 250 px/m (500 px/m in a 2025 revision) — a mounting and
    optics limit no software can correct
    ([competitive-landscape.md](../competitors/competitive-landscape.md);
    [technical-feasibility.md](../technology/technical-feasibility.md) §11).
14. **The buyer is not the user.** Procurement (FHQ/MHA) selects the system;
    field command lives with the result. Documented BSF RFPs "allowed vendors
    to arrive at their own conclusions" rather than specifying requirements,
    with high reliance on external vendors and minimal oversight
    ([domain-research.md](../domain/domain-research.md) §4.3).

---

## 4. Detailed Findings

### 4.1 Users and organisational roles

The problem statement names only "border security forces"
([problem.md](../../00-project/problem.md)); every role below is reconstructed
from research rather than confirmed with any user, and each carries the
evidence quality of its source.

**Field command** — the echelons that would carry a camera or a console, if
one exists.

| # | Role | Evidence | Scope | Notes |
|---|---|---|---|---|
| **U1** | BOP in-charge — Sub-Inspector. Commands the lowest echelon that could have a camera on it | `[N8]`; [ssb-operational-context.md](../domain/ssb-operational-context.md) §3.2 | [SIH/SSB] | Rank is documented; that this person is the video user is inferred, not confirmed |
| **U2** | Check post in-charge — Head Constable. Commands the node where lawful, high-volume crossing is processed | ibid. §3.2, §4.3 | [SIH/SSB] | Rank documented |
| **U3** | Company/Battalion commander — Assistant Commandant/Commandant. The assessing and deciding echelon | ibid. §3.2 | [SIH/SSB] | Documented |

**Operational and analytical roles** — roles that would consume video-derived
information if a workflow for it exists.

| # | Role | Evidence | Scope | Notes |
|---|---|---|---|---|
| **U4** | Monitoring operator. Watches live video; subject to vigilance decrement at 20–35 min while observing 3–30 scenes | [domain-research.md](../domain/domain-research.md) §4.1 `[S9][S10]` | [BORDER]/[GLOBAL] | The role is well documented in the domain generally; whether it exists in SSB is unresolved (**SQ-3**) |
| **U5** | Intelligence staff. SSB is Lead Intelligence Agency for the Indo-Nepal border; ~650 field and staff agents; 25 Border Interaction Teams in plain clothes on high-risk routes; "Know Your Area" programme | [ssb-operational-context.md](../domain/ssb-operational-context.md) §1.1, §5.2, §6.2 | [SIH/SSB] | The mission is documented; that this staff would consume video-derived pattern data is inferred |
| **U6** | Anti-Human Trafficking Unit staff. Five SSB AHTUs; 316 trafficking cases and 531 victims rescued in 15 months | ibid. §5.2, §12 `[N1][N8]` | [SIH/SSB] | Documented |

**Evidence and downstream roles.**

| # | Role | Evidence | Scope | Notes |
|---|---|---|---|---|
| **U7** | Evidence custodian/handover officer. Must produce a s.63 BSA certificate with a hash, signed by the device custodian and an expert, for footage handed to state police | ibid. §11.5; [domain-research.md](../domain/domain-research.md) §3.5 `[S29]` | [MARKET:IN] | The legal requirement is documented; whether the role is actually staffed is unresolved (**SQ-13**) |
| **U8** | Downstream case owner — state police/prosecutor. Receives the case; did not produce the video | [ssb-operational-context.md](../domain/ssb-operational-context.md) §11.4 `[N17]` | [MARKET:IN]/[BORDER] | The handover is documented; whether video reaches them at all is assumed, not confirmed |

**Support and adjacent roles.**

| # | Role | Evidence | Scope | Notes |
|---|---|---|---|---|
| **U9** | Technical maintainer. SSB has a Wireless & Telecom Training Centre as a standing formation; whether any cadre can install or repair IP camera/analytics infrastructure at a BOP is unresolved | ibid. §7, §10.5; **SQ-9** | [SIH/SSB] | Formation documented; capability unresolved |
| **U10** | Procurement/modernisation staff (FHQ, MHA). ₹5,001.63 crore allotted 2015-16 to 2025-26, ₹4,775.11 crore spent; MHA states no completion timeline is possible | ibid. §6.1 `[N3]` | [SIH/SSB] | Documented |
| **U11** | Adjacent-agency consumers — LPAI/Customs/Immigration at ICP Raxaul and Jogbani, NCB (narcotics), state police, intelligence agencies, and APF Nepal on joint patrols | ibid. §4.3, §9; **SQ-14, SQ-23** | [SIH/SSB]/[BORDER] | Their existence is documented; whether they consume this video is unresolved |

**Distinctions that must not be collapsed.**

- **The buyer is not the user.** U10 procures; U1–U3 live with the result. BSF
  RFPs "allowed vendors to arrive at their own conclusions" rather than
  specifying technical requirements, with high reliance on external vendors
  and minimal oversight ([domain-research.md](../domain/domain-research.md)
  §4.3). A product optimised for the procurement document and not for the
  Sub-Inspector risks being bought and not used — this would be falsified by
  evidence that field units drive requirements in this force.
- **Detection and assessment are different jobs, done by different people.**
  A sensor alarm is not an incident; a human must look at imagery to decide
  (ibid. §3.2). Cameras exist as the assessment medium for alarms raised by
  other means. A product that treats "alert" and "incident" as the same
  object is designing for a role that does not exist.

**Non-users, recorded so they are not mistaken for users.**

- **The border population.** Tens of thousands cross the India–Nepal border
  daily under a treaty right
  ([ssb-operational-context.md](../domain/ssb-operational-context.md) §2.2
  `[N7][N13]`). They are the subject of the system, not its user, and their
  legal position is what makes several named capabilities contested
  ([§5.1](#51-the-eight-named-capabilities), [§5.5](#55-capabilities-to-exclude-for-now)).
- **SIH evaluators.** A real audience with real influence over what gets
  built, and not an operational user. Noted explicitly because the strongest
  pressure to treat the eight-capability list as the product comes from this
  audience, not from any user (see [§5.1](#51-the-eight-named-capabilities)).

### 4.2 User jobs

What each user is trying to accomplish, stated as the job rather than a
feature.

| Job | Who | Evidence |
|---|---|---|
| **J1 — Know what is happening in my stretch, without watching it continuously** | U1, U2, U4 | Conventional CCTV requires continuous human observation ([problem.md](../../00-project/problem.md)); vigilance decays at 20–35 min ([domain-research.md](../domain/domain-research.md) §4.1). That U1/U2 currently carry this burden is inferred, not confirmed |
| **J2 — Decide whether a thing I have been told about is real, fast enough to act** | U1, U3, U4 | The C2 function is "analyse and classify the threat" (ibid. §1.3); assessment is distinct from detection (ibid. §3.2) |
| **J3 — Get the right people to the right place before the moment passes** | U1, U3 | BOP/Company-level decision latency named as a live problem by a senior SSB officer ([ssb-operational-context.md](../domain/ssb-operational-context.md) §3.2) |
| **J4 — Find the contraband, the currency, the trafficker — not the crossing** | U1, U2, U5, U6 | SSB's own achievement ledger: prohibited items 5,993, narcotics 1,059, currency 471, cattle 432, forest products 398, trafficking 316; infiltration is a real but small category at 24 cases ([ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2 C-2) |
| **J5 — Know my area: who uses this track, how often, with what** | U5 | LIA designation, ~650-agent intelligence wing, 25 BITs, KYA programme (ibid. §1.1, §5.2, §6.2). That video would serve this mission is inferred |
| **J6 — Rescue victims, not just arrest traffickers** | U6 | 531 victims rescued vs 274 traffickers arrested in 15 months (ibid. §12) — the victim outcome exceeds the arrest outcome |
| **J7 — Hand a case to the police in a form that survives** | U1, U7, U8 | s.63 BSA requires a hash and two signatures ([domain-research.md](../domain/domain-research.md) §3.5); cases are handed to state police ([ssb-operational-context.md](../domain/ssb-operational-context.md) §11.4). Current practice is unresolved (**SQ-13**) |
| **J8 — Log what happened, somewhere that is not a paper register** | U1, U3 | "Real-time alert generation and event logging" is a named requirement ([problem.md](../../00-project/problem.md)); SIMS is a national NDPS database, not an SSB logging system ([ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2 C-1, §5). That current logging is manual is inferred from the statement's own framing |
| **J9 — Keep the kit working when I cannot reach it and cannot fix it** | U1, U9 | 308 of 734 BOPs lack road connectivity; generators where there is no grid; lack of technical expertise documented ([ssb-operational-context.md](../domain/ssb-operational-context.md) §10.1, §10.2; [domain-research.md](../domain/domain-research.md) §4.3) |
| **J10 — Show that the money bought something** | U10 | GAO found US Border Patrol had not used available data to determine surveillance technology's contribution, and found ~500 recorded "asset assists" from towers in a sector that has none — a US analogue, not a confirmed SSB finding ([domain-research.md](../domain/domain-research.md) §4.4) |

MHA records SSB's output as a case/arrest ledger by contraband category, not
an alarm log ([ssb-operational-context.md](../domain/ssb-operational-context.md)
§8.1, §12) — which suggests J4 and J5, not J1, are the jobs this force is
actually measured on. This would be falsified by any SSB reporting instrument
that counts detections, alarms or crossings rather than cases and seizures.

### 4.3 Current operational workflow

**The baseline the problem statement starts from [GLOBAL].** Conventional
CCTV provides video recording and live monitoring, requiring continuous human
observation ([problem.md](../../00-project/problem.md)). A human watches; a
recorder records.

**The SSB workflow, as far as the research establishes it [SIH/SSB].**
SSB's surveillance repertoire is patrol- and post-based: a layered grid of
BOPs at ~3.9 km spacing, area domination patrols, manned naka and check posts,
joint patrols with APF Nepal (5,841 in FY 080/81, up from 78 in FY 071/72),
observation posts, plain-clothes Border Interaction Teams, and AHTUs
([ssb-operational-context.md](../domain/ssb-operational-context.md) §4.2,
§5.2). Cross-border coordination with APF Nepal is scheduled rather than
event-driven — annual/semi-annual at DG level down to fortnightly at
Company/BOP level — and an SSB officer states there are "still gaps in
real-time information exchange that hinder proactive security responses"
(ibid. §8.1). Cases end with handover to the local police station; SSB's
jurisdictional belt is 15 km under the SSB Act 2007, versus BSF's 50/80 km
(ibid. §11.2, §11.4).

Human presence, not electronic sensing, appears to be SSB's primary
surveillance instrument today — every mechanism named in the sources is a
person, and cameras appear only as procurement line items (ibid. §5.2). This
is explicitly an argument from silence: it is a statement about what the
sources describe, not a finding that camera-led monitoring is absent, and
would be falsified by any evidence of camera-led monitoring (**SQ-17**).
Whether monitoring is staffed and rostered, local and incidental, or
something else entirely, is not established — an earlier assumption that it
is "local and incidental, a screen watched by whoever is on duty" rested
wholly on this silence and has been withdrawn in favour of recording it as an
open question, resolved only by putting **SQ-3** to the force directly
([ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §3.2,
H-1).

**The BSF workflow, recorded as contrast only [BORDER].** BOLD-QIT feeds reach
BSF Control Rooms, which cue Quick Reaction Teams to intercept
([domain-research.md](../domain/domain-research.md) §1.3, §2.1); the broader
US analogue sequence is detect → track → identify/classify → resolve (ibid.
§3.2). This chain must not be assumed for SSB: no SSB control room and no SSB
QRT construct is documented in any source retrieved
([ssb-operational-context.md](../domain/ssb-operational-context.md) §16, item
7; [ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §3.2,
§4.2, H-1, H-4; **SQ-12**). The BSF chain is unavailable as evidence *for* an
SSB equivalent, and its undocumented status is equally unavailable as evidence
*against* one.

**What is genuinely unknown about the workflow.** Whether live monitoring is
performed and at which echelon (**SQ-3**); the actual
detection → assessment → response sequence and whether an SOP exists
(**SQ-4**); who responds and what carries the alert to them (**SQ-12**);
response-time targets and SOP content (**Q-11/Q-12**). SIMS is now resolved as
MHA's national NDPS seizure database rather than an SSB system
([ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2
C-1), but the broader question of what SSB's "existing command and control
systems" are remains open (ibid. §5). Five of the seven blocking questions
carried into [§7](#7-open-questions--research-gaps) are about the workflow,
not the technology — that is the shape of this discovery.

### 4.4 Pain points

Each pain point states whose pain it is and how well evidenced it is, ordered
by evidence strength rather than by how appealing it is to solve.

**Well evidenced.**

| # | Pain | Whose | Evidence | Scope |
|---|---|---|---|---|
| **P1** | Sustained human observation is not a reliable detection method. Vigilance decrement onsets at 20–35 min; operators watch 3–30 scenes; system effectiveness is bounded by operator detection ability | U4 (conditional on **SQ-3**) | [domain-research.md](../domain/domain-research.md) §4.1 `[S9][S10]` — peer-reviewed | [GLOBAL] |
| **P2** | Alerting systems become untrusted once nuisance rates are high. SBInet: 90% of sensor alerts were false alarms; CIBMS analysis names false alarms/sensor malfunction as a leading issue and defines no protocol for distinguishing infiltrators from wildlife | U1, U3, U4 | ibid. §4.2 `[S1][S2]` | [BORDER] |
| **P3** | The point of capture is not technical. BOP = Sub-Inspector, check post = Head Constable; lack of technical expertise for equipment operation and maintenance is a documented deficiency | U1, U2, U9 | [ssb-operational-context.md](../domain/ssb-operational-context.md) §3.2; [domain-research.md](../domain/domain-research.md) §4.3 | [SIH/SSB]/[BORDER] |
| **P4** | The site cannot be reached. 308 of 734 BOPs lack road connectivity; generators where there is no grid, with fuel travelling the same unroaded path; a parliamentary committee noted lack of electricity at SSB and ITBP BOPs specifically | U1, U9, U10 | [ssb-operational-context.md](../domain/ssb-operational-context.md) §10.1, §10.2 `[N9][N18]` | [SIH/SSB] |
| **P5** | Decisions are slow at the echelon nearest the event. BOP/Company-level decision latency named directly by a senior SSB officer; CIBMS analysis separately flags that centralised decision-making may delay urgent field responses | U1, U3 | ibid. §3.2; [domain-research.md](../domain/domain-research.md) §3.6 | [SIH/SSB]/[BORDER] |
| **P6** | Nobody can say whether the technology helped. GAO found Border Patrol had not used available data to determine surveillance technology's contribution, and found ~500 recorded "asset assists" from towers in a sector that has none | U10, U3 | [domain-research.md](../domain/domain-research.md) §4.4 `[S12]` | [BORDER] |
| **P7** | Evidence has to survive a cross-organisational handover. s.63 BSA (in force 1 July 2024) requires a certificate disclosing the record's hash value, signed by the device custodian and an expert; the custodian at capture is an SI or HC, and 42% of posts have no road | U1, U7, U8 | [ssb-operational-context.md](../domain/ssb-operational-context.md) §11.5; [domain-research.md](../domain/domain-research.md) §3.5 `[S29]` | [MARKET:IN] |
| **P8** | What the force actually catches is overwhelmingly not intrusion. "Illegal Infiltrators (Foreigner)" is 24 cases against 3,649 prohibited/contraband cases and 1,026 narcotics cases; the three largest categories are prohibited items, narcotics and currency | U1, U5, U6 | [ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2 C-2 | [SIH/SSB] |
| **P9** | Real-time information exchange with the counterpart force is inadequate, and coordination is calendar-driven | U3, U5 | ibid. §8.1 | [SIH/SSB] |
| **P10** | Night is the operational peak and the technical trough. Visible-light detection scores 0.430 mAP vs 0.651 for infrared on the same night scenes — a 33.9% relative drop — while infiltration and smuggling are believed to concentrate in darkness | U1, U4 | [technical-feasibility.md](../technology/technical-feasibility.md) §3.10 `[T26]`; [domain-research.md](../domain/domain-research.md) §5.6 | [BORDER] |
| **P11** | Identity-grade analytics are unreachable on cameras specified for overview. DORI puts Detection at 25 px/m and Identification at 250 px/m (500 px/m in a 2025 revision) — software cannot manufacture missing pixels | U1, U3 | `[C49][T8][T9]` | [GLOBAL] |
| **P12** | "Suspicious activity" cannot currently be delivered as commonly understood. A learned anomaly-detection benchmark's 94.55% AUC collapses to 16.35% on same-scene reversed labels; false-alarm rate rises 42% on hard-normal sets, over 70% in some; human annotators agree only at Fleiss' κ 0.51–0.68; AUC is insensitive to *when* detection occurs | U1, U3, and evaluators | `[T27]` | [GLOBAL] |

**Believed but not directly evidenced — flagged as such, with what would
confirm or rule each out.**

| # | Pain | Basis | Would be confirmed/ruled out by |
|---|---|---|---|
| **P13** | Event logging is manual; video retrieval is DVR-scrubbing | Inference from the problem statement's own framing ([domain-research.md](../domain/domain-research.md) §3.4); not independently sourced | **SQ-5, Q-9** — any digital incident register linked to video |
| **P14** | A camera-derived detection that produces no seizure has nowhere to go, because SIMS records seizure outcomes only and is not an SSB system | [ssb-operational-workflow.md](../domain/ssb-operational-workflow.md) §0.2 C-1, §5 | **SQ-5** — SIMS accepting a machine-generated, non-seizure event |
| **P15** | Trafficking is the event class least served by any named analytic — a trafficked minor moving through a check post with an adult produces no intrusion, no unusual vehicle and no suspicious motion; the signal is relational and behavioural at a lawful crossing | ibid. §12.1 — explicitly recorded there as unsourced | Direct enquiry with U6 (AHTU staff) |
| **P16** | Cattle, porters and forest produce are targets, not nuisance alarms, inverting the signal/noise assumption of a fenced border | ibid. §12.1 | **SQ-18** — a measured nuisance profile on this border |

**The strongest-evidenced pain points (P2, P3, P4, P7) are all about the
conditions of deployment, not about detection quality.** That asymmetry is
the single most useful thing this synthesis produces. P1 is the strongest
peer-reviewed pain in the corpus, but it is conditional on **SQ-3** and may
not apply to the named force at all — building for P1 before SQ-3 is answered
is the single most likely way to build the wrong product.

---

## 5. Implications for IBVAP

Everything in this section is a candidate input to product scoping, not a
decision. Adoption of any capability, principle or opportunity below happens
in `docs/02-product/`, per [CLAUDE.md](../../../CLAUDE.md) §2.

### 5.1 The eight named capabilities

Required by the immutable problem statement
([problem.md](../../00-project/problem.md), [goals.md](../../00-project/goals.md)).
Recorded here with feasibility and operational fit, because requirement,
feasibility and usefulness are three different questions.

| # | Capability (as named) | Market status | Feasibility on existing, non-purpose-mounted CCTV | Operational fit on the validation border |
|---|---|---|---|---|
| 1 | Human detection and tracking | Shipping from every vendor surveyed | Detection moderate–high; single-camera tracking moderate (≥3 fps floor, occlusion); cross-camera low | Fits — a person is the primitive every other job composes from |
| 2 | Vehicle detection and classification | Shipping from every vendor | Detection moderate–high; coarse class moderate; make/model/colour low | Partial — the operationally relevant classes (porter's cart, load-carrying tractor-trailer, driven livestock) are not COCO or TrafficCamNet classes |
| 3 | Face detection | Shipping | Low–moderate — overview cameras look down on the tops of heads; mounting geometry, and no model, fixes this | Unclear — depends entirely on whether any camera sees faces at face-scale |
| 4 | ANPR | Shipping; already solved software-only twice (Genetec Flexreader ≤50 km/h; Milestone XProtect LPR ≤30° mounting) | Low on a general camera; moderate–high on a lane-aimed camera. Needs ~250 px/m; India has ~210 million vehicles and 50+ plate types | Fits at ICPs/check posts/barriers only. Does not fit a wide-area border-road camera |
| 5 | Virtual fence intrusion detection | Shipping, including free open source | Mechanism high; nuisance rate at an acceptable level unproven | Poor fit. Crossing is a treaty right; MHA's own framing is "misuse of open border," not intrusion. A line-crossing alarm that was 100% correct would still be almost entirely noise here |
| 6 | Suspicious activity detection | No consensus solution in the market | Low as a learned model; moderate as explicit composite rules over reliable primitives | Undefined. The term is undefined in the statement and in every retrieved source (**Q-3**), and materially harder on an open border (**SQ-7**) |
| 7 | Night-time movement detection | Not a distinct product feature anywhere in the market — it is an operating condition | Low–moderate on visible cameras; high on thermal, which most estates do not have | Highest operational weight, worst technical outlook — the "night inversion" |
| 8 | Real-time alert generation and event logging | Shipping | High, bounded by what the link can carry | Fits — and is the one capability whose presence as a requirement suggests it is currently absent or inadequate |

*(Sources: [competitive-landscape.md](../competitors/competitive-landscape.md)
§4, §6.2, §6.3; [technical-feasibility.md](../technology/technical-feasibility.md)
§3, §11; [ssb-operational-context.md](../domain/ssb-operational-context.md)
§2.3, §12.1; [domain-research.md](../domain/domain-research.md) §5.7, §6.7.)*

**The seven required outcomes** (from [goals.md](../../00-project/goals.md)),
with the research finding bearing on each:

| Outcome | Bearing finding |
|---|---|
| Eliminate dependence on expensive dedicated surveillance hardware | Half true, and already commercialised. The dependency moved from the camera's silicon to the camera's mounting — Flexreader's 50 km/h, XProtect LPR's 30° |
| Enable intelligent monitoring through AI-powered video analytics | Achievable for presence-and-motion primitives; not for identity primitives on overview cameras |
| Provide real-time alerts for security incidents and border intrusions | Achievable; the binding question is nuisance rate, not mechanism |
| Support facial recognition, vehicle identification and behavioural analytics through software | The capability most in tension with the deployment model. NIST's own conclusion: video face recognition can approach still-photo accuracy "but only if image collection can be improved" — camera positioning, mounting, lighting and optics, all hardware `[T23b]` |
| Improve situational awareness and response time | Fits P5 directly, but note the counter-finding: centralising decisions may delay urgent field responses |
| Support integration with existing command and control systems | Ingest has standardised; egress has not. SIMS has been eliminated as a candidate, and no SSB command-and-control system has been identified |
| Cost-effective, scalable, suitable for remote deployment | Believed to mean scaling across many small isolated sites, not to one large central cluster. Per-camera pricing, universal in the market, penalises exactly this shape |

**The three constraints.** Must ingest live streams from standard IP-based
CCTV; must not require dedicated FRS/ANPR/smart-camera hardware; must use
AI/ML/CV/video analytics ([goals.md](../../00-project/goals.md)). The named
department has already procured a "CCTV Surveillance Setup with Automatic
Face Recognition System with Auto Number Plate Recognition" (MHA reply to Lok
Sabha USQ 488, 3 February 2026)
([ssb-operational-context.md](../domain/ssb-operational-context.md) §6.1,
§14.2) — where it is deployed, whose software it is, and whether it exposes
any stream or API are all unresolved (**SQ-2**). The problem statement's
stated gap, that FRS and ANPR are absent because they need dedicated
hardware, does not hold unqualified for the named department; what to do
about that is a `docs/02-product/` decision.

**The tension this creates.** Two audiences want different things. SIH
evaluation rewards visible coverage of all eight named capabilities; the
operational user (U1–U6) is measured overwhelmingly on contraband, currency,
trafficking and third-country foreigners, where the ledger's "Illegal
Infiltrators (Foreigner)" category is only 24 cases against 3,649
prohibited/contraband cases and 1,026 narcotics cases. Capability 5 (virtual
fence) is the sharpest case — technically easy, operationally misdirected on
this border; capability 7 (night) is the inverse — technically hardest,
operationally heaviest. This document does not resolve the tension; it
records that the resolution is a product decision, and that "build all eight
because they are listed" is one option among several, not the default.

### 5.2 Opportunities

Nothing here is a requirement. Each entry pairs the opening with the reason
it may be thin on purpose, per the competitive research's own discipline
([competitive-landscape.md](../competitors/competitive-landscape.md) §10).

| # | Opportunity | Evidence for | Evidence against | Scope |
|---|---|---|---|---|
| **O1** | Honest per-camera capability disclosure — tell the operator, measured from the actual stream, which analytics this camera can and cannot support at this mounting, in the spirit of i-LIDS' primary-vs-secondary certification | No vendor examined ships this as a runtime feature; Genetec ships a calculator only. Unusually well aligned with the pixels-on-target reality | Vendors have a commercial incentive not to publish per-camera limitations; it also means telling a buyer their estate cannot do what they hoped | [GLOBAL] |
| **O2** | Disconnected-by-default operation as a designed property, decomposed into four independent parts: analytics keep running; events queue and reconcile idempotently; licensing does not expire; time stays trustworthy | Only Irisity states air-gapped support; only Milestone documents offline licensing; for Genetec, BriefCam, Videonetics, AllGoVision and Ipsotek this is undocumented — the competitive survey's own "single most important unknown" | On-premise VMS has always run offline; this may be table stakes rather than a differentiator | [BORDER] |
| **O3** | A published, measured nuisance-alarm rate with a cause histogram — the number the entire market declines to publish | Bandwidth and GPU models are published; accuracy, false-alarm rates and power are not. The experiment is cheap (7 days on the existing rig) | Publishing a real false-alarm rate invites unfavourable comparison with vendors who publish nothing | [GLOBAL] |
| **O4** | A published power budget per camera per analytic | Zero vendors in the survey publish watts, even while mandating specific NVIDIA GPUs. At a fuel-limited site this is a first-order constraint | May be unmeasured rather than unsolved; edge-NPU cameras are already low-power | [BORDER] |
| **O5** | Alerting sized to a two-person post — event record plus a small crop in real time, full clip fetched on demand | Every platform surveyed assumes a control room, a video wall and an operator hierarchy. A 15 s 1080p clip = 7.8 min on 128 kbps; a 320×320 crop = 1.6 s — a factor of ~300 | Mobile clients exist everywhere, and whether the target force even has a control room is itself unknown (**SQ-3**) | [BORDER] |
| **O6** | Evidentiary integrity at the cheapest tier — hash-chained events, signed exports and tamper-evidence as a default rather than an edition upgrade | Milestone gates media encryption/signing to Expert/Corporate and Evidence Lock to Corporate; Genetec's first encryption certificate costs 30% of Archiver capacity. The smallest, most remote deployments get none of it — and those are the deployments here | These are pricing decisions, not absent features; a wrong clock at a disconnected site silently invalidates the whole chain | [MARKET:IN]/[BORDER] |
| **O7** | Standards-based egress that already exists and nobody uses. ONVIF Profile M defines metadata for vehicle, plate, face, body and geolocation with MQTT delivery; MISB ST 0903 (VMTI) inside STANAG 4609 defines per-frame detections with bounding boxes, geolocation, track IDs and confidence, and NATO-compatible C2 systems already ingest it. No vendor in the survey was found emitting either | Egress is the unstandardised half of the market, and it is exactly what "integration with existing C2" means | The target C2 is unnamed (**SQ-6**); building an adapter for a system that may not exist is the risk | [GLOBAL]/[BORDER] |
| **O8** | Pattern-over-time for an intelligence-led force — who uses this track, how often, with what — rather than alarm-in-the-moment | SSB is the Lead Intelligence Agency for the Indo-Nepal border, with a ~650-agent wing, 25 BITs and the KYA programme | Directly adjacent to solved products (BriefCam Video Synopsis, Avigilon Appearance Search, Ambient Pulsar); on an open border, retaining records of lawful crossings may not be permissible at all (**SQ-8**) | [SIH/SSB]/[BORDER] |
| **O9** | Deployment without a certified integrator and without a site survey, on an estate nobody else will touch | Certification is priced at 2–3 days and USD 595–2,995; Ipsotek shipped a product variant for "repeatable, plug-and-play" rollout | DORI physics means some estates genuinely cannot be made to work, and a product that hides that fails in the field. Only works paired with O1 | [BORDER] |
| **O10** | Failure modes a non-specialist can recognise and report — specifically degraded analytic quality: a camera still streaming but no longer usable for its configured analytic (dirt, web, condensation, IR hotspot, drift, refocus) | Stream-loss alerts and camera-integrity monitors exist; nothing found addresses silent analytic degradation. Pairs directly with P3 and P5 | May exist under product names not searched | [BORDER] |
| **O11** | A cost structure for many small, low-utilisation sites | Per-camera pricing is universal; the smallest Verkada bridge is USD 2,999 for 10 channels | The competitor at the bottom of this market is open source, not Genetec — Frigate is free and does person/vehicle detection, virtual fence, alerting and event logging today | [BORDER] |

**Opportunities that are not opportunities.** Already solved, per
[competitive-landscape.md](../competitors/competitive-landscape.md) §10.1:
ANPR without dedicated ANPR cameras; analytics on existing third-party
cameras; natural-language video search; rapid forensic review of long
recordings; AI false-alarm reduction; privacy-preserving redaction;
multi-site metadata aggregation; cloud video on low bandwidth; open APIs into
a VMS; camera tamper detection. The competitive research's own discipline
applies: do not assume the incumbents are expensive because they are
inefficient. Genetec's cost buys federation, failover, encryption, audit,
certification and a support organisation — the encryption alone costs 30% of
Archiver capacity. Anything cheaper is trading something away, and the trade
must be named, not hidden.

### 5.3 Potential differentiation

**What IBVAP cannot differentiate on.** All eight named capabilities are
shipping products from multiple vendors today; there is no capability gap
([competitive-landscape.md](../competitors/competitive-landscape.md) §4.1,
lesson 1). Ruled out: detection accuracy (competing here means being measured
against vendors with decades of tuning, on benchmarks nobody publishes
anyway); the feature list (every row of it is commodity); price alone (the
floor competitor is free — Frigate); "works with any ONVIF camera" (two of
the best-resourced engineering organisations in this market both built
per-model compatibility labs and still warn buyers); "Indian-tuned models"
(Videonetics already claims models that "work well with facial features of
the Indian subcontinent" as its stated differentiator).

**Where differentiation is plausible.** Each of these is a hypothesis to be
tested, not a decision.

| # | Hypothesis | Why it might hold | What would kill it |
|---|---|---|---|
| **D1** | Honesty is the feature — a platform that measures and states, per camera, what it can and cannot do, and refuses to claim identity-grade analytics on detection-grade cameras (O1 + O3 + O10) | Nobody ships it; the physics guarantees it will often be needed; converts the product's biggest weakness (inherited cameras) into its most credible claim | If buyers reward the claim over the truth, which the RFP finding suggests they might |
| **D2** | The smallest deployable unit is the product — not a control room, not a cloud tenant, but a post with two cameras, a Sub-Inspector, a generator and an intermittent link | Every architecture surveyed assumes a control room or cloud tenant; the estate is 734 BOPs, 42% unroaded | If the force actually operates centrally, and this unit is not how they want to buy or run it (**SQ-3, SQ-6**) |
| **D3** | Fit the ledger, not the fence — design around the event classes the force is actually measured on (contraband, currency, trafficking, third-country foreigners) rather than intrusion | The ledger's infiltration category (24 cases) is small against the major contraband/narcotics categories | The gap between what a camera can see and what the ledger counts may be unbridgeable by video alone — a camera cannot see contraband inside a sack |
| **D4** | Disconnection as a designed property, published as four separable guarantees (O2) | It is the competitive survey's own most important unknown about every incumbent | It may be table stakes that vendors simply do not document |
| **D5** | Standards-based egress (ONVIF Profile M / MISB ST 0903) instead of a bespoke adapter per C2 (O7) | Existing, vendor-neutral, already ingestible by NATO-compatible C2; nobody in the survey emits it | If the actual target C2 (**SQ-6**) speaks neither, this is elegant and useless |
| **D6** | Measured, published operating envelope — nuisance rate, watts per analysed frame, latency decomposition, behaviour across a multi-day disconnection (O3 + O4) | These are exactly the four things the industry does not publish | Measurement on one rig is not measurement on the estate; the numbers must be honest about their sample |

The evidence points toward **the deployment being the differentiator, not the
analytic** — the best-evidenced pain points (P2, P3, P4, P7) are all
deployment conditions, and this echoes the competitive research's own
question back to product discovery. This remains a working assumption,
falsified by evidence that the estate can support identity-grade analytics
and that detection quality, not deployability, is what the user actually
lacks.

### 5.4 Candidate capability classification

These are not MVP decisions. A capability marked as a strong candidate is one
the evidence supports carrying into scoping, not a committed feature. MVP
selection happens in `docs/02-product/`.

**Foundation.**

| Capability | Rationale |
|---|---|
| RTSP/ONVIF ingest from existing IP cameras, read-only and non-degrading to the live estate | Mandated by the statement's constraints. ONVIF conformance alone is insufficient — a tested-device record is part of the capability. A safety test must pass first: concurrent RTSP clients must not degrade the existing recorder (**E-12**) |
| Per-camera capability audit — measured px/m at operational range, achievable fps, codec, anamorphic detection, and a plain statement of which analytics this camera can support | The unfilled market gap (O1); the precondition for every honest claim the product makes; answers **A-1/E-1** as a by-product |
| Person detection (support-grade) | The primitive every other job composes from; throughput is not the constraint (256 fps on an Orin Nano); feasibility moderate–high |
| Vehicle detection and coarse classification | Same; 419 fps on an Orin Nano. Coarse class only — attributes are low feasibility |
| Single-camera multi-object tracking at ≥3 fps | Required for any dwell, direction or count rule; the ≥3 fps floor is measured (AssA 43.6% → 27.8% between 3 and 1 fps) |
| Object-class-gated zone/line/direction/dwell rule engine | Strictly better than pixel-motion VMD, and it is the substrate an operator authors on top of. The mechanism is trivial; the product is the nuisance rejection |
| Local event log with tamper-evident record (hash-chained) and explicit time integrity | Named in the statement (capability 8); required by s.63 BSA; O6. A silent wrong clock is the worst version of the evidential risk |
| Local-first operation with store-and-forward, idempotent monotonically-identified events, bounded queue and a defined discard policy | P4 + A4 + O2. At a site offline for days the queue will fill — the discard policy is a first-class design object, not an edge case |
| Alert payload discipline: event record plus small crop in real time, full clip on demand | Arithmetic, not opinion — a factor of ~300 on a 128 kbps link |
| Retrospective query over locally held event metadata (time, zone, class, camera) | The cheap backbone of J5 and J8; note the adjacency to solved forensic-search products — the claim must stay modest |
| Degraded-analytic-quality detection and reporting (dirt, web, condensation, IR hotspot, refocus, drift) in language a Sub-Inspector can act on | O10 + P3 + P11; nothing found in the market addresses it |

**Must investigate before any commitment.**

| Capability | What must be answered first |
|---|---|
| Virtual fence as an operational concept on this border | **SQ-7/Q-3.** Crossing is lawful; a perfect line-crossing alarm is still noise here. The mechanism is feasible; the framing is not decided |
| "Suspicious activity" as operator-authored composite rules over reliable primitives (e.g. "person in zone A, 2200–0500, >90 s") | **A-8/Q-3** — what suspicious means, stated as observable behaviour. No experiment substitutes for this answer; this remains a hypothesis, not a recommendation |
| Night-time analytics on the estate's actual night imagery (IR-illuminated visible, or thermal) | **Q-15/SQ-1** — what fraction is thermal, and whether visible cameras have IR illuminators, true day/night sensors, or neither. Then **E-6** on real footage |
| Measured nuisance-alarm rate as a product feature (rate plus cause histogram, per camera, shown to the operator) | Cheap to run (7-day unattended run on the existing rig, **E-5**), and possibly the single most valuable experiment on the list. Whether it belongs in the product surface or only in the engineering record is a product question |
| ANPR at lane-aimed nodes only — ICP Raxaul/Jogbani, check posts, barriers | **SQ-14** (who owns ICP CCTV, and does the force have access), **SQ-2** (the already-procured ANPR stack), and whether a lane-aimed camera exists at all. Already solved twice in the market — entering here means matching Flexreader/XProtect LPR, not beating them |
| Non-standard object classes the ledger actually contains — loaded porter, cart, driven livestock, timber load | D3's viability turns on this; these are not COCO or TrafficCamNet classes, so training data is the open question |
| Evidence export package satisfying s.63 BSA (hash preserved through export, no re-transcode, custodian and expert signature workflow) | **SQ-13** — current practice, who signs, who is "expert." Transcoding changes the hash, so this constrains the whole media path |
| Egress format: ONVIF Profile M over MQTT, MISB ST 0903 VMTI, plain webhook | **SQ-5, SQ-6, A-5** — the target C2 is unnamed. A spike is warranted; an adapter is not |
| Pattern-over-time/route-usage analytics for intelligence use (O8) | **SQ-8** — whether records of lawful crossings by treaty-protected nationals may be retained at all. This is a legality question before it is a product question |
| Whether the product's alerting posture is primary (sole) or secondary (support), in i-LIDS terms | Determines alerting, staffing and liability; the competitive research names this as a choice that "should be made deliberately rather than by default" |

**Later.**

| Capability | Why not now |
|---|---|
| Cross-camera tracking/person re-identification | Feasibility low; re-ID degrades badly out of domain; fixed non-overlapping cameras give no geometric constraint to exploit |
| Face recognition against a bounded watchlist (tens of known traffickers), if a legal basis and gallery exist | Technically easier than open-set identification, and NIST's advice is to limit gallery size — but **SQ-8** (legal basis on a treaty-open border) and **A-9** (does a gallery exist) are both unanswered |
| Multi-site aggregation/federation to a higher echelon | "Process locally, ship metadata" is settled practice, not an opening; also gated on **SQ-3** and **SQ-6** — the hosting echelon is unknown |
| Mobile/handheld alert client | Plausible fit for a post with no console (D2), but the connectivity profile (**SQ-11**) decides whether it is even usable |
| Body-worn camera ingest | SSB reportedly uses them, but retention and central handling are unknown (**SQ-22**) |
| Video synopsis/rapid forensic review | Solved since before 2018 by BriefCam — not a place to start |
| Automatic bidirectional C2 integration | The target does not have a name yet (**SQ-6**) |
| PTZ control/slew-to-cue | Stable-background analytics are invalid while a PTZ moves; an interaction to design after the primitives are trusted |
| UAV/drone video ingest | SSB operates UAVs, so the feed exists — but nothing establishes a job for analysing it, and the problem statement does not name it |

**Do not pursue.**

| Capability | Why |
|---|---|
| Learned anomaly detection as the delivery of "suspicious activity" | 94.55% AUC → 16.35% on same-scene reversed labels; false-alarm rate +42% on hard-normal sets, some >70%; contested ground truth (κ 0.51–0.68); AUC insensitive to detection timing — three independent, measured failures |
| Open-set face identification of the border population | Legally unresolved on a treaty-open border (**SQ-8**); prohibited by default for law enforcement in publicly accessible spaces under EU AI Act Art. 5 (a market-specific rule, not universal); NIST's precondition — improve image collection — is exactly what this deployment model forbids |
| ANPR on wide-area border-road cameras | A plate at that range and angle is far below the required pixel density — physics, not effort |
| Full video egress to a central site | Not possible at these link speeds; the whole market has already converged away from it |
| Replacing the existing recorder/VMS layer | Outside the statement's scope, multiplies the deployment burden at exactly the sites that cannot absorb it, and competes directly on incumbents' strongest ground |
| Cloud-dependent SaaS as the primary deployment mode | Contradicts P4/site-connectivity findings outright; data-classification/network policy for border video is entirely unestablished (**Q-18/A-10**) |
| Competing on published detection-accuracy benchmarks | See "what IBVAP cannot differentiate on" above; benchmarks in this market are unpublished, paywalled, or scene-overfitted |
| Drone/counter-UAS detection | Not named in the problem statement; not a documented event class; fixed ground CCTV is geometrically poorly positioned for it |
| Tunnel detection | Out of reach of surface video analytics; not a documented SSB event class |

### 5.5 Capabilities to exclude for now

Distinct from "do not pursue" above: these are things it would be reasonable
to want, which should stay out of an MVP conversation until something
specific changes.

| Excluded | Until |
|---|---|
| Anything whose value depends on a control room existing — video wall, operator hierarchy, multi-operator workflow, shift handover | **SQ-3** is answered |
| Anything whose value depends on a named C2 system — adapters, bidirectional sync, alarm-acknowledgement round-trips | **SQ-5/SQ-6** name the target |
| Any biometric processing of the border population | **SQ-8** establishes a legal basis, authorisation level, retention rule and oversight |
| Any claim of identity-grade capability (face recognition, ANPR) on the general estate | **A-1/E-1** measures actual px/m and shows which cameras, if any, support it |
| Retention of records of lawful crossings | **SQ-8** and the DPDP-applicability question are resolved |
| Any published accuracy or false-alarm claim | **E-5** and **E-6** have been run on real footage and the number is measured, not assumed |
| Cross-border data sharing with APF Nepal | **SQ-23** establishes whether any legal basis exists |
| Fine-grained vehicle attributes (make/model/colour) | Someone establishes an operational job for them; colour is gone at night anyway |
| A pricing model | Competitors **Q-1** yields a real price anchor — "cheaper" is currently an untestable claim |

### 5.6 Candidate product principles

Each traced to the finding that produced it. These are proposed, not
adopted — adoption is a `docs/02-product/` decision recorded in
`docs/00-project/decisions.md`.

| # | Principle | Traces to |
|---|---|---|
| **PR1** | Measure, then claim — never assert a capability for a camera that has not been measured; per-camera truth is stated to the operator, not hidden | P11, O1, D1 |
| **PR2** | An alert must be worth the attention it costs — attention is the scarcest resource here, and a nuisance alarm spends it while supplying false assurance | P1, P2, A13 |
| **PR3** | Assume no link, no engineer, no certainty of power — every behaviour must have a defined answer for the disconnected, unattended, fuel-limited case, including what gets discarded when the queue fills | P4, P3, O2 |
| **PR4** | Fail legibly to a Sub-Inspector — failure states must be recognisable and reportable over a radio or satellite phone by someone with no technical training | P3, O10 |
| **PR5** | Evidence integrity is a default, never a tier — hashes, tamper-evidence and time integrity ship at the smallest deployment, because the smallest deployment is the one at the border | P7, O6 |
| **PR6** | Do not detect what is not an offence — on an open border the crossing is lawful; what is reportable is who, what they carry, and when and where | P8, SQ-8, capability 5 |
| **PR7** | Detection is not assessment — the system's job is to bring a human to the right frame at the right time, not to decide; which side of the i-LIDS primary/secondary line the product stands on is declared explicitly | [domain-research.md](../domain/domain-research.md) §3.2, §6.7 |
| **PR8** | Never degrade the operational estate — the existing recorder and live-view path keep working, unchanged, whatever the platform is doing, verified before anything touches a live site | E-12, P4 |
| **PR9** | Metadata crosses the link; video stays home — video moves only when a person asks for it | Arithmetic; [technical-feasibility.md](../technology/technical-feasibility.md) §5.3; market pattern P2 |
| **PR10** | Say what it cannot do — per-camera limits, per-analytic limits, and the conditions under which each degrades, are product surface, not a support ticket | O1, D1, P11 |
| **PR11** | Legality gates biometrics, not capability — face recognition has an unresolved legal basis here; it is switched on by a legal answer, never by a feature flag | SQ-8, EU AI Act Art. 5 |
| **PR12** | Scale by site count, not by user count — the unit of deployment is a small, isolated, hard-to-reach post, and the cost model must survive that shape | A11, A12, O11 |
| **PR13** | Name the trade — anything cheaper than an incumbent is trading something away; the trade is stated, not hidden | [competitive-landscape.md](../competitors/competitive-landscape.md), "5 assumptions we must NOT make," item 5 |

---

## 6. Risks and Limitations

**The five biggest risks this research identifies:**

1. **We do not know how the user works.** The SSB CCTV/control-room workflow
   is not publicly validated (**SQ-3**) — which is not the same as knowing it
   is absent. Any product built around a specific monitoring posture, in
   either direction, rests on an unvalidated workflow, and any structure
   adopted before SQ-3 is answered is a design choice, not a discovered fact.
   This risk sits upstream of every other decision in this document, and it
   is answerable by one question to the force.
2. **The estate may not physically support the named capabilities, and
   nobody has measured it.** If existing cameras deliver 25–62 px/m, face
   recognition and ANPR are unreachable at any software quality — and the
   problem statement requires them anyway.
3. **Nuisance alarms make the system untrusted, which is worse than no
   system.** 90% false alarms is the documented precedent; the environmental
   triggers (wind-moved vegetation, rain, fog, headlight glare, wildlife,
   IR-attracted insects) are all present; and on this border the usual
   "noise" categories are targets, so standard mitigations may not transfer.
4. **The capability list and the operational reality point in different
   directions, and the pressure is to satisfy the list.** The ledger's
   infiltration category is real but small — 24 cases against 3,649
   prohibited/contraband and 1,026 narcotics cases — while the statement's
   centrepiece is a virtual fence. Building all eight because they are
   listed is a decision, and if taken by default rather than deliberately,
   the result satisfies the evaluator and not the user.
5. **Night is the operational peak and the technical trough, and
   "night-time movement detection" is not a feature anyone sells.** A 33.9%
   relative detection drop on visible-light night imagery, against an
   operational belief that crossings concentrate in darkness. This inversion
   is the central technical risk of the whole programme until measured.

**Assumptions this analysis rests on.** None of these is established fact;
each states what would falsify it.

| # | Assumption | Basis | Falsified by |
|---|---|---|---|
| **A1** | SSB is the department for PS 26187 | Project owner's statement; the SIH organisation field is not recorded | Recording the actual SIH department field (**SQ-30**) |
| **A3** | Existing border cameras were specified for Detection/Observation density (25–62 px/m), not Identification | DORI, plus the finding that existing CCTV was installed for live viewing | **SQ-1/A-1** — a measured site survey |
| **A4** | Uplinks at these sites are of the order of hundreds of kbps, or intermittent, or satellite | Satellite phones in the surveillance inventory; peer-reviewed constrained-edge findings | **SQ-11/A-3** |
| **A5** | Continuous compute at a generator-powered, unroaded site is a fuel-logistics cost, not just an electrical one | Road and generator findings combined | **SQ-10/A-4** |
| **A6** | Event logging today is manual/register-based; retrieval is DVR-scrubbing | Inference from the statement's framing | **SQ-5, Q-9** |
| **A7** | A camera-derived detection that yields no seizure has no home in existing systems | SIMS is a national NDPS seizure database, not an SSB system, and is seizure-framed | **SQ-5** |
| **A8** | On this border, cattle, porters and forest products are targets, not nuisance alarms — the signal/noise split differs in kind from a fenced border | SSB's own seizure categories | **SQ-18** |
| **A9** | Trafficking detection is the event class least served by the named analytics | Explicitly unsourced in the research | Enquiry with U6 |
| **A10** | The buyer/user gap will cause a procurement-optimised product to go unused | Documented RFP and vendor-oversight weaknesses | Evidence that field units drive requirements |
| **A11** | "Scalable" means many small sites, not one big cluster | The statement's own phrase "across remote border locations" | Direct clarification |
| **A12** | Per-camera pricing, universal in the market, is a poor fit for a many-small-sites estate | Market pricing survey plus the estate shape | Actual pricing data (**Competitors Q-1**) |
| **A13** | An untrusted alerting system is worse than none, because it consumes attention and supplies false assurance | Inference from the operator-reliance finding | An operator study on this estate |
| **A14** | IR-illuminated night video is effectively monochrome, so every colour-dependent mechanism degrades at night | Physics of IR illumination; not stated in a retrieved source | Directly testable on the rig (**E-6**) |

*(An earlier assumption, A2 — "SSB has no staffed video control room; monitoring
is local and incidental" — rested on an argument from silence and has been
withdrawn; it is replaced by the open question **SQ-3**, not by an assumption
in either direction.)*

**Other known limitations of this research.**

- The user model rests on **A1** (the SSB attribution itself is unrecorded at
  the SIH-process level).
- Whether the monitoring-operator role (U4) exists in this force is
  unvalidated in either direction (**SQ-3**); this document asserts neither
  its presence nor its absence.
- No user of any kind has been spoken to in any research pass to date — every
  finding here is documentary, not observed.
- Every pain point in [§4.4](#44-pain-points) is inferred from documentary
  evidence rather than directly observed in the field.

---

## 7. Open Questions / Research Gaps

Carried by their original IDs so the research trail stays intact.

**Blocking — a PRD cannot be honest without these.**

| # | Question | Origin |
|---|---|---|
| **B1** | Is the SIH department attribution actually SSB? Record the organisation field for PS 26187 | SQ-30 |
| **B2** | Does the force monitor live video at all, and at which echelon? Operators, cameras per operator, shift pattern, instructions on seeing something | SQ-3/Q-5 |
| **B3** | What is the installed camera base? Count and location by node type, make, model, resolution, codec, PTZ vs fixed, thermal vs visible, ONVIF conformance, age — and native IP vs analog behind a DVR/XVR with a shared encoder budget | SQ-1/Q-1/A-1/A-2 |
| **B4** | What does "suspicious activity" mean, stated as observable behaviour, on an open border? No experiment substitutes for this | Q-3/SQ-7/A-8 |
| **B5** | What are the "existing command and control systems," by name, with interfaces? SIMS has been eliminated as a candidate (owner, hosting and data model now known), so no SSB C2 system has yet been identified by name | SQ-6/Q-4/A-5 |
| **B6** | Where is the already-procured FRS/ANPR CCTV setup deployed, what is it, and does it expose streams or APIs? Determines whether IBVAP complements, replaces, or duplicates it | SQ-2 |
| **B7** | What is the legal basis, authorisation level, retention rule and oversight for biometric processing of people exercising a treaty right of movement? Does DPDP 2023 apply? | SQ-8 |

**High priority — these shape scope.**

| # | Question | Origin |
|---|---|---|
| **H1** | What is the actual detection → assessment → response sequence, and is there a written SOP or Standing Order? | SQ-4/Q-11 |
| **H2** | Is there a QRT construct, or is response by the patrol/naka already in the field? What carries the alert to them? | SQ-12 |
| **H3** | What connectivity exists at a post — any IP link, bandwidth, symmetry, metering, reliability, how many on satellite? | SQ-11/Q-8/A-3 |
| **H4** | What power is available for compute — generator hours, rating, fuel resupply interval, solar/battery — and what does an extra 15–60 W cost in logistics? | SQ-10/Q-7/A-4 |
| **H5** | What retention applies to video, clips and metadata separately, and is there a time source at a disconnected site? | SQ-13/Q-9/A-6/A-7 |
| **H6** | What is the current export-and-handover procedure to state police, and does it satisfy s.63 BSA today — who signs, who is the "expert," is a hash computed? | SQ-13/Q-10 |
| **H7** | Who owns and operates the CCTV at ICP Raxaul and Jogbani, and does the force have access? | SQ-14 |
| **H8** | What security accreditation, data classification and network policy applies to a platform handling live border video? Is cloud or internet permissible at all? | Q-18/A-10 |
| **H9** | What is the real nuisance profile here, given that cattle, porters and forest produce are targets rather than nuisances? | SQ-18/Q-6 |
| **H10** | Is the Indo-Bhutan border operationally the same problem as the Indo-Nepal border, or a different one? | SQ-25 |

**Answerable without the force — by experiment or desk research.**

| # | Question | Origin |
|---|---|---|
| **X1** | What is the measured nuisance-alarm rate and cause histogram of an object-gated virtual fence over 7 unattended days on real footage? | E-5/experiment 3 |
| **X2** | How do detection and tracking behave on IR-illuminated night footage from an ordinary camera? | E-6/experiment 4 |
| **X3** | What is the analysis-rate floor on these scenes (25/10/5/3/1 fps)? | E-7/experiment 6 |
| **X4** | Does adding concurrent RTSP clients degrade an existing recorder's own recording? This must pass before anything touches a live estate | E-12 |
| **X5** | Does the pipeline survive a 72-hour disconnection with events reconciling without duplication or loss, licences intact and clocks in tolerance? | E-11/experiment 7 |
| **X6** | What does an analysed frame cost in joules, per accelerator? | E-10/experiment 9 |
| **X7** | Does the market's pricing even permit a "cost-effective" claim to be tested? | Competitors Q-1 |
| **X8** | Verify the IEC/EN 62676-4:2025 pixel-density figures against the standard itself — a 2× change in the identification threshold is too consequential to carry on a secondary source | C-1 |

---

## 8. Conclusions

**This research does not support starting a PRD yet.** The most consequential
open question (whether and how SSB monitors live video, **SQ-3**) is
unresolved, and two of the three constraints named in the problem statement
(identity-grade analytics on general cameras; integration with an unnamed C2
system) cannot be scoped honestly until the estate and the target system are
known.

**Recommended next step, in order:**

1. **Close B1 first** — record the SIH organisation/department field in
   `docs/00-project/`. It costs minutes, does not touch the immutable problem
   statement, and determines whether [§4](#4-detailed-findings) of this
   document is about the right force.
2. **Open a user-research pass under `docs/01-research/users/` targeting
   B2–B7.** These are questions for people, not for a test rig, and five of
   the seven are about workflow rather than technology. Sources worth trying,
   named by the research itself: Parliamentary Standing Committee on Home
   Affairs reports, any CAG audit of SSB modernisation procurement, the MHA
   Annual Report 2024-25 or later, the SSB Act 2007 and Rules 2009 text, and
   the official SSB website (**SQ-26 through SQ-29**).
3. **In parallel, run X4 (recorder safety), then X1 (7-day unattended
   nuisance-alarm run with a cause histogram)** on the existing rig. X4 is a
   safety precondition; X1 produces the single number the entire market
   declines to publish, needs nothing this project does not already have,
   and directly tests risk 3 in [§6](#6-risks-and-limitations).
4. **Do not start the PRD until B2, B3 and B4 have answers — or explicit,
   recorded assumptions in their place.** If they cannot be answered, the PRD
   should state the assumption it substitutes and what would falsify it,
   rather than proceeding silently.

Per [CLAUDE.md](../../../CLAUDE.md) §2, `docs/02-product/` may begin once
B1–B7 are answered, or explicitly assumed with falsification criteria
recorded.

---

## 9. References

**Primary inputs synthesized by this document:**

- [docs/00-project/problem.md](../../00-project/problem.md) — the immutable
  SIH problem statement
- [docs/00-project/vision.md](../../00-project/vision.md)
- [docs/00-project/goals.md](../../00-project/goals.md)
- [docs/01-research/domain/domain-research.md](../domain/domain-research.md)
  — cited inline as `[S-]`
- [docs/01-research/domain/ssb-operational-context.md](../domain/ssb-operational-context.md)
  — cited inline as `[N-]`
- [docs/01-research/domain/ssb-operational-workflow.md](../domain/ssb-operational-workflow.md)
- [docs/01-research/competitors/competitive-landscape.md](../competitors/competitive-landscape.md)
  — cited inline as `[C-]`
- [docs/01-research/technology/technical-feasibility.md](../technology/technical-feasibility.md)
  — cited inline as `[T-]`

Inline citation keys (e.g. `[N8]`, `[S9][S10]`, `[T26]`, `[C49]`) refer to
sources catalogued in the bibliographies of the documents above. `SQ-`, `Q-`,
`A-`, `B-`, `E-`, `H-` codes are open-question, assumption and experiment IDs
carried from those same documents so the research trail stays traceable
across the corpus.

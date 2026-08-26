# IBVAP — Product Requirements Document

**Stage:** 02 — Product Definition
**Date:** 2026-08-25
**Status:** Approved. All product decisions D-1 … D-14, listed in
[§19](#19-product-decisions-requiring-human-approval), are **accepted** and
recorded in [decisions.md](../00-project/decisions.md) (2026-08-25).

**Primary requirement:** the official SIH/MHA problem statement, PS 26187, recorded
verbatim and immutably in [problem.md](../00-project/problem.md). Nothing in this
document reinterprets, narrows, removes or contradicts it. Every capability it
names is preserved in [§9](#9-sih-required-capabilities) and carried through to
[§7](#7-functional-requirements).

**Research inputs (complete):**
[domain-research.md](../01-research/domain/domain-research.md) ·
[ssb-operational-context.md](../01-research/domain/ssb-operational-context.md) ·
[ssb-operational-workflow.md](../01-research/domain/ssb-operational-workflow.md) ·
[competitive-landscape.md](../01-research/competitors/competitive-landscape.md) ·
[technical-feasibility.md](../01-research/technology/technical-feasibility.md) ·
[product-discovery.md](../01-research/users/product-discovery.md)

## Contents

0. [How to read this document](#0-how-to-read-this-document)
1. [Product vision](#1-product-vision)
2. [Problem statement](#2-problem-statement)
3. [Target users](#3-target-users)
4. [User needs / jobs](#4-user-needs--jobs)
5. [Core user workflows](#5-core-user-workflows)
6. [Product goals](#6-product-goals)
7. [Functional requirements](#7-functional-requirements)
8. [Non-functional requirements](#8-non-functional-requirements)
9. [SIH-required capabilities](#9-sih-required-capabilities)
10. [MVP scope](#10-mvp-scope)
11. [Post-MVP scope](#11-post-mvp-scope)
12. [Explicit non-goals](#12-explicit-non-goals)
13. [Success metrics](#13-success-metrics)
14. [Constraints](#14-constraints)
15. [Assumptions](#15-assumptions)
16. [Risks](#16-risks)
17. [Open questions](#17-open-questions)
18. [Acceptance criteria](#18-acceptance-criteria)
19. [Product decisions requiring human approval](#19-product-decisions-requiring-human-approval)
20. [Traceability — problem statement → this document](#20-traceability--problem-statement--this-document)

---

## 0. How to read this document

### 0.1 Labels — and the one distinction that matters most

Per [CLAUDE.md](../../CLAUDE.md) §3.7, every substantive statement carries a label.
This document adds one label the research stage introduced but deliberately never
used, because it belongs here and only here.

| Label | Meaning | Never means |
|---|---|---|
| **FACT** | Verified in the research corpus, cited to the document and section that establishes it. A FACT is a fact *about what the cited research records* | That the matter is settled beyond what the source says |
| **ASSUMPTION** | Believed true, unverified. Every assumption states what would falsify it | A fact |
| **HYPOTHESIS** | A proposed approach to be tested | A commitment |
| **UNKNOWN** | Not established by available evidence | **That the thing does not exist.** Absence of documentation is never recorded as absence in fact |
| **DECISION** | A product choice made here, with rationale. Every DECISION is listed in [§19](#19-product-decisions-requiring-human-approval) and is provisional until approved | A research finding |
| **PRODUCT MODEL** | A workflow or role structure **IBVAP chooses to design for**, where the evidence does not establish the real-world workflow | A description of how SSB — or any force — actually operates. A PRODUCT MODEL is a design construct and never becomes a FACT by being built on |

> **The rule this document enforces, carried from
> [ssb-operational-workflow.md](../01-research/domain/ssb-operational-workflow.md)
> §9 (final constraint):** *"Any user hierarchy or workflow written into
> `docs/02-product/` before H-1 and H-2 are answered will be **invented, not
> discovered**, and must be labelled as such at the point it is written."*
> [§5](#5-core-user-workflows) is therefore labelled **PRODUCT MODEL** throughout,
> in full, with no exceptions.

### 0.2 Scope labels

Per [CLAUDE.md](../../CLAUDE.md) §4 — IBVAP is **not** India-specific:

| Label | Meaning |
|---|---|
| **[SIH/SSB]** | True only for this problem statement or for Sashastra Seema Bal, the department attributed to PS 26187 |
| **[BORDER]** | True for border/frontier surveillance generally, in any country |
| **[GLOBAL]** | True for intelligent video analytics on existing CCTV anywhere |
| **[MARKET:xx]** | Legal, procurement, connectivity or pricing factor specific to a market |

### 0.3 What this document is and is not

**It is:** the definition of what IBVAP is, who it serves, what it must do, what it
must not claim, what ships first, and how we will know it worked.

**It is not:** a UX design ([03-design](../03-design/)), a system architecture
([04-architecture](../04-architecture/)), a technology-stack selection, an
implementation plan, or a task list. **No stack is chosen here. No architecture is
designed here. No code is written here.** Where research produced an arithmetic
consequence that constrains the product (for example, that full video cannot cross
a 128 kbps link), it is recorded as a **product constraint** in
[§14](#14-constraints) — *what must be true* — and never as *how to build it*.

### 0.4 Reading order for a reviewer with ten minutes

[§9](#9-sih-required-capabilities) (the SIH obligation and how each capability is
honoured) → [§10](#10-mvp-scope) (what ships) → [§12](#12-explicit-non-goals) (what
does not) → [§19](#19-product-decisions-requiring-human-approval) (what needs your
signature).

---

## 1. Product vision

### 1.1 Vision statement

**IBVAP turns cameras that were installed to be watched into cameras that watch —
in software, on the estate that already exists, at posts nobody else will deploy
to, and it tells the truth about what each camera can and cannot see.**

The problem statement's own vision — transform existing IP-based CCTV at BOPs,
check posts, border roads and strategic locations into an intelligent surveillance
network, without dedicated FRS/ANPR/smart-camera hardware
([vision.md](../00-project/vision.md)) — is adopted unchanged as IBVAP's purpose.
The sentence above is how IBVAP proposes to be *distinguishable* while doing it.

### 1.2 Why the second half of that sentence is in the vision

**FACT [GLOBAL]** — Every capability the problem statement names is already a
shipping product from multiple vendors. There is no capability gap
([competitive-landscape.md](../01-research/competitors/competitive-landscape.md),
lesson 1).

**FACT [GLOBAL]** — The binding constraint moved rather than disappeared: out of
the camera's silicon and into the pixels the installed camera delivers, the encoder
budget of the recorder in front of it, the decode cost of the stream, and the watts
and bits available at the site
([technical-feasibility.md](../01-research/technology/technical-feasibility.md)
§0).

**FACT [GLOBAL]** — No vendor surveyed ships per-camera capability disclosure as a
runtime feature; no vendor publishes power; no vendor publishes a measured
false-alarm rate
([competitive-landscape.md](../01-research/competitors/competitive-landscape.md)
§9 P10, §10 G2/G6).

**DECISION D-1 (accepted)** — **IBVAP differentiates through deployment,
transparency, reliability and camera-aware operation; it pursues sufficient
accuracy for each defined use case rather than competing primarily on benchmark
leadership.** It will not claim universal camera support, and it will not chase
headline accuracy figures disconnected from a measured use case — but accuracy
remains a first-class, per-capability requirement, gated and reported by the
Camera Spec Sheet rather than asserted in the abstract. It competes on running where
nothing else runs and on stating, per camera, what it can and cannot do, at what
measured accuracy.
*Rationale:* all eight capabilities are commodity, so accuracy claimed in the
abstract is not a defensible sole differentiator against vendors with decades of
tuning; the four best-evidenced pain points (PP2, PP3, PP4, PP7) are all
conditions of deployment. Sufficient, measured accuracy per use case remains
required — it is the entry condition the Camera Spec Sheet enforces (D-6) — it is
just not, by itself, the basis for competitive positioning
([product-discovery.md](../01-research/users/product-discovery.md) §4.1, §9).

### 1.3 Positioning within scope (per [CLAUDE.md](../../CLAUDE.md) §4)

| Layer | What IBVAP is |
|---|---|
| **[GLOBAL]** | A software video-analytics platform for existing IP CCTV estates that are old, mixed, poorly sited, badly connected and unattended — the estates the market's architectures assume away |
| **[BORDER]** | A surveillance platform for dispersed, low-staffed, low-bandwidth, hard-to-reach frontier posts, where the unit of scale is the *site*, not the user |
| **[SIH/SSB]** | The SIH 2026 validation context: PS 26187, with SSB's Indo-Nepal and Indo-Bhutan estate as the concrete deployment to be reasoned about and demonstrated against |

**DECISION D-2 (accepted)** — **SSB is the validation context, not the
product boundary.** All requirements are written force-agnostically and market
factors are labelled. SSB-specific and India-specific requirements are marked
`[SIH/SSB]` / `[MARKET:IN]` and are *satisfiable* rather than *assumed*.
*Rationale:* [CLAUDE.md](../../CLAUDE.md) §4 requires it; the problem statement
text itself says only "border security forces".

---

## 2. Problem statement

### 2.1 The official problem (primary, immutable)

Recorded verbatim in [problem.md](../00-project/problem.md). Restated here only by
reference, never by paraphrase:

- **Background:** conventional CCTV provides recording and live monitoring only,
  requiring continuous human observation. Advanced functions (FRS, ANPR, intrusion
  detection, object tracking) often require specialised hardware and proprietary
  solutions, making large-scale deployment costly and difficult in remote border
  areas.
- **Description:** an AI-driven software platform ingesting live streams from
  standard IP-based CCTV, performing real-time analytics, providing the eight named
  capabilities.
- **Expected solution:** eliminate dependence on expensive dedicated hardware;
  enable intelligent monitoring; real-time alerts; face recognition, vehicle
  identification and behavioural analytics **through software**; improve situational
  awareness and response time; integrate with existing command and control systems;
  be cost-effective, scalable and deployable at remote border locations.

**This is the requirement. Sections 2.2–2.4 do not replace it; they record what the
research established about the conditions under which it must be met.**

### 2.2 What the research adds to the problem — the four hard truths

**T1 — The software premise holds; the pixel premise does not.**
**FACT [GLOBAL]** — Every named capability ships as software on third-party cameras
today; but capabilities needing *identity* — face recognition, ANPR, cross-camera
tracking, fine vehicle attributes — need pixel densities (250 px/m in the 2015
standard, reported as 500 px/m in the 2025 revision) that cameras installed for
human overview (25–62 px/m) were never specified to deliver
([technical-feasibility.md](../01-research/technology/technical-feasibility.md)
§9 L1, §11, finding 1).
**FACT [GLOBAL]** — NIST's own conclusion on video face recognition: it may approach
still-photo accuracy *"but only if image collection can be improved"* — camera
positioning, mounting, lighting, optics. All four are hardware (ibid. §3.5).

**T2 — Nuisance alarms, not missed detections, are the documented failure mode.**
**FACT [BORDER]** — 90% of SBInet sensor alerts were false alarms; CIBMS analysis
names false alarms and sensor malfunction as a leading technical issue and records
that the design defines no protocol for distinguishing infiltrators from wildlife
([domain-research.md](../01-research/domain/domain-research.md) §4.2).
**FACT [GLOBAL]** — Operator reliance on a semi-automated system tracks that
system's accuracy (ibid. §4.1). An untrusted alerting system consumes attention and
supplies false assurance.

**T3 — The site defeats the market's architectures.**
**FACT [SIH/SSB]** — 308 of 734 SSB BOPs (42%) lack road connectivity; generators
where there is no grid; off-grid solar being tendered in lots of 6–8 BOPs; satellite
phones in the surveillance inventory
([ssb-operational-context.md](../01-research/domain/ssb-operational-context.md)
§10; [ssb-operational-workflow.md](../01-research/domain/ssb-operational-workflow.md)
G-16, G-18).
**FACT [GLOBAL]** — Every commercial platform surveyed assumes a control room or a
cloud tenant
([competitive-landscape.md](../01-research/competitors/competitive-landscape.md)
§10 G7).

**T4 — On the validation border, the crossing is not the offence.**
**FACT [SIH/SSB]** — MHA's own statement of the challenge on both SSB borders,
verbatim identical across three consecutive Annual Reports, is *"to check misuse of
the open border by terrorists and criminals"* — not intrusion. Crossing is a treaty
right for Indian, Nepali and Bhutanese nationals
([ssb-operational-workflow.md](../01-research/domain/ssb-operational-workflow.md)
G-7).
**FACT [SIH/SSB]** — MHA AR 2024-25's SSB achievements table does contain *"Illegal
Infiltrators (Foreigner)" — 24 cases*, alongside 3,649 prohibited/contraband cases
and 1,026 narcotics cases (ibid. §0.2 C-2).

### 2.3 The product problem IBVAP solves

> **A border force owns cameras it cannot watch, at posts it cannot reach, on links
> it cannot fill, and it has no way to know which of those cameras is capable of
> telling it anything useful. When something does happen, the record of it is
> shaped for an outcome ledger, not for a detection — and the footage has to
> survive a handover to an organisation that did not produce it.**

Each clause traces to evidence:

| Clause | Evidence |
|---|---|
| *cameras it cannot watch* | Vigilance decrement at 20–35 min across 3–30 scenes; system effectiveness bounded by operator detection ability `[S9][S10]` ([domain-research.md](../01-research/domain/domain-research.md) §4.1) |
| *posts it cannot reach* | 42% of BOPs unroaded; generator power; no in-house IT/video cadre ([ssb-operational-workflow.md](../01-research/domain/ssb-operational-workflow.md) G-15, G-18) |
| *links it cannot fill* | Per-camera uplinks of "a few hundred kilobits per second or less" in constrained deployments; a 15 s 1080p clip = 7.8 min on 128 kbps ([technical-feasibility.md](../01-research/technology/technical-feasibility.md) §5.3) |
| *no way to know which camera is capable* | DORI physics; no vendor ships per-camera capability disclosure ([competitive-landscape.md](../01-research/competitors/competitive-landscape.md) §10 G6) |
| *record shaped for an outcome ledger* | Every verified SSB reporting instrument is outcome-shaped or discipline-shaped; no verified instrument records a detection ([ssb-operational-workflow.md](../01-research/domain/ssb-operational-workflow.md) §4.2) |
| *survive a handover* | s.63 BSA 2023: certificate with hash value, signed by device custodian **and** an expert; cases handed to local police ([ssb-operational-context.md](../01-research/domain/ssb-operational-context.md) §11.4–11.5) |

### 2.4 What IBVAP does not claim to solve

Recorded here so the claim boundary is explicit before any requirement is read:
IBVAP does not improve any camera's optics, mounting, illumination or field of
view; does not raise a recorder's shared encoder budget; does not add photons at
night; does not see contraband inside a sack; and does not make an unlawful act out
of a lawful crossing. See [§12](#12-explicit-non-goals) and
[§14](#14-constraints).

---

## 3. Target users

**FACT [SIH/SSB]** — The problem statement names only *"border security forces"*.
The roles below are carried from
[product-discovery.md](../01-research/users/product-discovery.md) §1.2 with their
original evidence quality intact. **No role is upgraded in confidence by appearing
in a PRD.**

### 3.1 Primary users — the product is designed for these

| # | User | Evidence status | Scope | Why primary |
|---|---|---|---|---|
| **U1** | **Post in-charge** — the person commanding the lowest echelon that could have a camera on it. Statutorily an outpost is commanded by a Deputy/Assistant Commandant **or** a subordinate officer not below Sub-Inspector; the *normal* rank is **UNKNOWN** (statute sets a floor, not a norm) | **FACT** (statutory floor, `[W1]` §56(3)–(4)); **UNKNOWN** (norm, H-9); **ASSUMPTION** that they are the video user | [SIH/SSB] → [BORDER] | The estate is 734 posts; the person nearest the camera is the person who can act inside the moment |
| **U2** | **Check-post in-charge** — commands the node where lawful, high-volume crossing is processed | **FACT** (the node exists); rank **UNKNOWN** | [SIH/SSB] → [BORDER] | The only node where lane-aimed identity analytics (ANPR, face) are physically plausible |
| **U3** | **Company / Battalion commander** — the assessing and deciding echelon (Assistant Commandant / Commandant; Rule 9(2) makes the Commandant responsible for the battalion) | **FACT** (statutory) | [SIH/SSB] → [BORDER] | Decision latency at BOP/Company level is a named live problem |
| **U4** | **Monitoring operator** — watches live video; subject to vigilance decrement at 20–35 min over 3–30 scenes | **FACT** that the role exists in the domain; **UNKNOWN** whether it exists in this force (SQ-3 / B2, H-1) | [BORDER] / [GLOBAL] | The role the whole market designs for. IBVAP must work **whether or not** it exists — see [§5](#5-core-user-workflows) |

**This is the single most important user constraint in the document, and it is a
gap, not a finding:**

**UNKNOWN [SIH/SSB] — carried as H-1** — *Whether SSB monitors live video at all,
and at which echelon.* Two deliberate research passes across the SSB Act 2007 and
Rules 2009, three MHA Annual Reports, parliamentary answers, a BPRD project report,
SSB's own website and 280-tender feed, court records and six tender aggregators
retrieved **no description** of an SSB control room, operations room, video wall,
monitoring roster or operator establishment
([ssb-operational-workflow.md](../01-research/domain/ssb-operational-workflow.md)
§3.2, §7.1, H-1). **This establishes what the searches returned and nothing else.**
The research further argues the answer is *structurally unlikely* to be found by
desk research, because Rule 9(4) places standing orders in the DG's hands and such
orders are not published (ibid. §7.2).

**DECISION D-3 (accepted)** — **IBVAP is designed to function correctly
whether or not a remote monitoring/control-room layer is available, or is
temporarily unavailable.** Core, site-local operation — analysis, rule-firing,
logging, local alerting — does not depend on a control room, an operator on shift,
or a console being present or reachable. Where a remote monitoring or
control-room capability does exist, IBVAP integrates with it as an additive layer.
Nothing in the MVP requires an operator to be watching, and nothing in the MVP
assumes one is not.
*Rationale:* the exact SSB CCTV/control-room workflow is unresolved (H-1);
designing around either its presence or its absence as the assumed baseline
invents a workflow the research does not establish, so the product is built to be
correct under both answers rather than to bet on one. *Falsified by:* an answer to
B2 showing a staffed monitoring posture that this additive layer fails to serve.

### 3.2 Secondary users — served, not designed around

| # | User | Evidence status | Scope | What IBVAP owes them |
|---|---|---|---|---|
| **U5** | **Intelligence staff** — SSB is Lead Intelligence Agency for the Indo-Nepal border; ~650-agent intelligence wing; 25 Border Interaction Teams; "Know Your Area" | **FACT** (existence); **ASSUMPTION** they would consume video-derived pattern data | [SIH/SSB] / [BORDER] | Retrospective query over event metadata (MVP); pattern-over-time (post-MVP, legally gated) |
| **U6** | **Anti-Human-Trafficking Unit staff** — 5 SSB AHTUs; 316 cases, 274 traffickers arrested, **531 victims rescued** in 15 months | **FACT** | [SIH/SSB] / [BORDER] | Honesty first: [§12](#12-explicit-non-goals) NG-12 states plainly that no analytic named in the statement detects trafficking |
| **U7** | **Evidence custodian / handover officer** — must produce a s.63 BSA certificate with a hash, signed by the device custodian *and* an expert | **FACT** (the legal requirement); **UNKNOWN** whether staffed (SQ-13) | [MARKET:IN] | Evidence export pack, hash at capture, custody log (MVP) |
| **U8** | **Downstream case owner — state police / prosecutor.** Receives the case; did not produce the video; documented as under-resourced for these cases | **FACT** (the handover) | [MARKET:IN] / [BORDER] | An export that opens and verifies without IBVAP installed |
| **U9** | **Technical maintainer.** SSB's technical cadre is the **Communication cadre** (wireless/telecom), supported by a Wireless & Telecom Training Centre. **No IT, cyber, video or electronics cadre exists** | **FACT** (`[W3][W4]`, G-15) | [SIH/SSB] | Failure states legible without IT training; no on-site engineer assumed |
| **U10** | **Procurement / modernisation staff (FHQ, MHA)** | **FACT** | [SIH/SSB] | Attribution data answering "did it help?" ([§13](#13-success-metrics) SM-8) |
| **U11** | **Adjacent-agency consumers** — LPAI/Customs/Immigration at ICP Raxaul and Jogbani, NCB, state police, intelligence agencies, APF Nepal | **FACT** (they exist); **UNKNOWN** whether they consume this video (SQ-14, SQ-23) | [SIH/SSB] / [BORDER] | Nothing in MVP. Cross-border sharing is a non-goal ([§12](#12-explicit-non-goals) NG-16) |

### 3.3 Non-users — recorded so they are not mistaken for users

- **The border population.** Tens of thousands cross the India–Nepal border daily
  under a treaty right. They are the **subject** of the system, never its user, and
  their legal position is what gates several named capabilities
  ([§9](#9-sih-required-capabilities) CAP-3b, CAP-5).
- **SIH evaluators.** A real audience with real influence, and **not an operational
  user**. Recorded explicitly because the strongest pressure to treat the
  eight-capability list as the product comes from this audience
  ([product-discovery.md](../01-research/users/product-discovery.md) §1.4).

### 3.4 The buyer is not the user

**FACT [BORDER]** — BSF requests for proposals have allowed vendors to *"arrive at
their own conclusions"* rather than specifying technical requirements, and there is
high reliance on external vendors with minimal oversight
([domain-research.md](../01-research/domain/domain-research.md) §4.3).

**ASSUMPTION [BORDER]** — A product optimised for the procurement document and not
for the person at the post will be bought and not used. *Falsified by:* evidence
that field units drive requirements in this force.

**Consequence for this PRD:** where a requirement serves the buyer (U10) and a
requirement serves the post (U1), and they conflict, this document resolves in
favour of U1 and says so at the point of conflict.

---

## 4. User needs / jobs

Carried from [product-discovery.md](../01-research/users/product-discovery.md) §2,
each stated as the job rather than the feature, each with its evidence class and
its MVP treatment.

| Job | Who | Evidence | MVP treatment |
|---|---|---|---|
| **J1 — Know what is happening in my stretch without watching it continuously** | U1, U2, U4 | **FACT** the burden exists (problem statement; vigilance decrement); **ASSUMPTION** U1/U2 carry it today | **Core.** The primitives + rules + alerting spine |
| **J2 — Decide whether a thing I have been told about is real, fast enough to act** | U1, U3, U4 | **FACT** — assessment is a distinct function from detection | **Core.** Alert carries the evidence needed to assess (crop first, clip on demand) |
| **J3 — Get the right people to the right place before the moment passes** | U1, U3 | **FACT** — BOP/Company decision latency named by a senior SSB officer | **Partial.** IBVAP shortens *notice*; it does not dispatch. Dispatch is out of scope (NG-9) |
| **J4 — Find the contraband, the currency, the trafficker — not the crossing** | U1, U2, U5, U6 | **FACT** — the ledger's composition | **Honest partial.** See [§12](#12-explicit-non-goals) NG-12 and D-9 |
| **J5 — Know my area: who uses this track, how often, with what** | U5 | **FACT** the mission exists; **ASSUMPTION** video would serve it | **Minimal in MVP** (local retrospective query only); full pattern analytics post-MVP and legally gated |
| **J6 — Rescue victims, not just arrest traffickers** | U6 | **FACT** — 531 victims rescued vs 274 traffickers arrested | **Not served.** Stated as a non-goal rather than implied |
| **J7 — Hand a case to the police in a form that survives** | U1, U7, U8 | **FACT** (the requirement); **UNKNOWN** (current practice) | **Core.** Evidence integrity is MVP, not a tier |
| **J8 — Log what happened, somewhere that is not a paper register** | U1, U3 | **FACT** — named in the statement; no SSB detection-shaped instrument identified | **Core.** Event log is a named SIH capability and the product's spine |
| **J9 — Keep the kit working when I cannot reach it and cannot fix it** | U1, U9 | **FACT** | **Core.** Health and degraded-analytic reporting in plain language |
| **J10 — Show that the money bought something** | U10 | **FACT** (US analogue: GAO); **ASSUMPTION** for SSB | **Core, cheaply.** Outcome attribution on every event ([§13](#13-success-metrics) SM-8) |

**ASSUMPTION [SIH/SSB]** — **J4 and J5, not J1, are the jobs this force is actually
measured on.** MHA records SSB's output as cases and persons arrested per contraband
category — a case/arrest ledger, not an alarm log. *Falsified by:* any force
reporting instrument that counts detections, alarms or crossings.

**This assumption is the reason [§12](#12-explicit-non-goals) NG-12 exists.** A
product that quietly implies it addresses J4 when it addresses J1 is mis-selling,
and the research is unambiguous that a camera cannot see contraband inside a sack
([product-discovery.md](../01-research/users/product-discovery.md) §9.2, D3
counter-evidence).

---

## 5. Core user workflows

> ### ⚠ EVERYTHING IN THIS SECTION IS A **PRODUCT MODEL**
>
> **These workflows are design constructs chosen by this document. They are not
> descriptions of how SSB, or any force, actually works.** The real
> detection → assessment → escalation → response sequence is **UNKNOWN** (H-2), what
> carries an alert is **UNKNOWN** (H-3), whether a QRT construct exists is
> **UNKNOWN** (H-4), and whether live video is monitored at all is **UNKNOWN**
> (H-1). No PRODUCT MODEL below becomes a FACT by being built on, and each must be
> validated against the force before [03-design](../03-design/) commits to it.

### 5.1 The design invariant that makes a PRODUCT MODEL safe here

**DECISION D-4 (accepted)** — **Core workflows are modelled around artefacts
and their states, with role assignment and permissions configurable.** The product
produces four core artefacts — an **Event**, an **Alert**, a **Case**, and a
**Camera Spec Sheet** — and every workflow is a path through those artefacts' states.
Which human occupies which step, and what permissions that role carries, is
configurable and carries no product assumption about the real SSB workflow.
*Rationale:* this is the only way to satisfy the constraint in
[§0.1](#01-labels--and-the-one-distinction-that-matters-most) while still shipping a
coherent workflow. If H-1 resolves to "there is a staffed control room", the same
artefacts and states route to an operator under the corresponding role and
permissions; if it resolves to "a Sub-Inspector and a phone", the same artefacts
route to him. **No re-architecture is required by either answer**, and that
property is itself the requirement (FR-31).

### 5.2 The four artefacts

| Artefact | Definition | Why it is a separate object |
|---|---|---|
| **Event** | A machine-generated observation: *this camera, this time, this object class, this rule, this confidence, this evidence pointer.* Produced whether or not anyone is watching, whether or not the link is up, whether or not it is interesting | **FACT [SIH/SSB]** — every verified force reporting instrument is outcome-shaped; **a camera-derived detection that produces no seizure has no existing home** ([ssb-operational-workflow.md](../01-research/domain/ssb-operational-workflow.md) §4.2, PP12). The Event *is* the gap the statement's "event logging" requirement names |
| **Alert** | An Event (or correlated group) that a rule has judged **worth spending a human's attention on**, delivered to somebody | **FACT [GLOBAL]** — detection and assessment are different functions; a sensor alarm is not an incident ([domain-research.md](../01-research/domain/domain-research.md) §3.2). A product that treats Event and Alert as one object is designing for a role that does not exist |
| **Case** | A human-opened container binding Events, evidence, an assessment and an outcome, exportable for handover | **FACT [MARKET:IN]** — cases are handed to state police under s.63 BSA with hash + two signatures |
| **Camera Spec Sheet** | A measured, per-camera statement of what this camera can and cannot support, at this mounting, right now | **FACT [GLOBAL]** — pixels on target is the hard floor and nobody discloses it per camera ([competitive-landscape.md](../01-research/competitors/competitive-landscape.md) §10 G6) |

### 5.3 W1 — Commission a camera *(PRODUCT MODEL)*

**Actor:** U1/U9 at the post, or U10/U9 remotely. **Frequency:** once per camera,
plus on change.

1. Point IBVAP at an existing stream (native IP camera, or a channel behind an
   existing DVR/NVR) using credentials the force already holds. **Read-only.**
2. IBVAP measures the stream as delivered: effective resolution (including
   anamorphic detection — **FACT [rig-measured]**: "1080" can mean 960 horizontal
   pixels), achievable analysed frame rate, codec, GOP, bitrate, day/night
   behaviour, and stability over an observation window.
3. The operator marks a reference distance in the scene (one measurement, no survey
   kit) — or accepts a range estimate with its uncertainty stated.
4. IBVAP issues a **Camera Spec Sheet**: for each analytic, `Eligible` /
   `Eligible, degraded` / `Not eligible`, **with the measured reason in plain
   language** ("a person at 40 m is 19 px tall here; person detection needs ~25
   px/m — this camera can tell you *someone* is there, not *who*").
5. Analytics that are `Not eligible` **cannot be enabled** on that camera. The
   product refuses rather than under-performs.

**Why step 5 is a hard behaviour and not a warning:** **FACT [GLOBAL]** — a claim of
capability that the optics cannot support is the failure mode the entire market
tolerates, and the one IBVAP proposes to convert into its most defensible claim
([product-discovery.md](../01-research/users/product-discovery.md), opportunity O1 /
hypothesis D1).

### 5.4 W2 — Watch, unattended *(PRODUCT MODEL)*

**Actor:** nobody. **Frequency:** continuous. **This is the workflow that must work
when H-1 resolves to "there is no operator".**

1. IBVAP analyses eligible cameras against enabled rules, locally, at the site.
2. Every observation that fires a rule becomes an **Event**, written to a local
   hash-chained log with a time-integrity status.
3. Events matching an alerting rule become **Alerts**, delivered by whatever
   channels are configured; where no channel is reachable, they queue.
4. If the link is down, analysis continues, the log continues, the queue grows
   under a bounded, **declared discard policy**.
5. Health and degradation are self-reported continuously — including **silent
   analytic degradation** (dirt, spider web, condensation, IR hotspot, refocus,
   drift) which is distinct from stream loss and which nothing in the surveyed
   market addresses.

### 5.5 W3 — Assess an alert *(PRODUCT MODEL)*

**Actor:** U1, or U4 if U4 exists. **Design target: seconds, not minutes.**

1. The Alert arrives carrying, in order of arrival: *what fired, where, when, which
   camera, which rule* — then a **small object crop** — then the full clip **only on
   demand**.
   **CALCULATION [GLOBAL]** — this ordering is arithmetic, not preference: a 15 s
   1080p clip is ~7.5 MB ≈ **7.8 minutes** on 128 kbps; a 320×320 crop is ~25 KB ≈
   **1.6 seconds**. A factor of ~300
   ([technical-feasibility.md](../01-research/technology/technical-feasibility.md)
   §5.3).
2. The human decides: **real / not real / unsure**, in one action.
3. The decision is written back onto the Event. This is the product's own ground
   truth and the input to [§13](#13-success-metrics) SM-1 and SM-2.
4. `Not real` optionally feeds a per-camera, per-rule suppression the operator can
   see and reverse. **Suppression is always visible and always reversible** — a
   silently self-muting system is the failure mode T2 describes.

### 5.6 W4 — Open and hand over a case *(PRODUCT MODEL)*

**Actor:** U1 → U7 → U8.

1. From one or more Events, a human opens a **Case** and states an outcome
   (apprehension / seizure / nothing found / handed over / no action).
2. IBVAP assembles an **evidence pack**: the original stored bitstream segments
   **without re-encoding**, the hash computed **at capture**, the event records,
   the chain-of-custody log, and a pre-filled certificate template naming the fields
   s.63 BSA requires (custodian, expert, hash).
   **FACT [MARKET:IN]** — transcoding changes the hash; therefore no export path may
   silently re-encode
   ([technical-feasibility.md](../01-research/technology/technical-feasibility.md)
   §6.5).
3. The pack opens and verifies **without IBVAP installed**, because U8 does not have
   it.
4. IBVAP **does not sign on anyone's behalf and does not assert admissibility.** It
   produces what the statute asks for and records who signed.

### 5.7 W5 — Look back *(PRODUCT MODEL)*

**Actor:** U1, U3, U5.

Query the local event store by time, camera, zone, object class, rule and outcome.
Retrieve the evidence attached to any Event. **In MVP this is site-local and
metadata-only.** Cross-site aggregation and pattern-over-time analytics are
post-MVP and, on this border, **legally gated** (OQ-7).

### 5.8 W6 — Emit to a command and control system *(PRODUCT MODEL)*

**Actor:** integrator, once per deployment.

**UNKNOWN — blocking, carried as H-6** — *What "existing command and control
systems" means for this force.* The only prior candidate, SIMS, has been eliminated:
it is **MHA's national NDPS seizure e-portal**, not an SSB system and not a C2
system. **Nothing has replaced it**
([ssb-operational-workflow.md](../01-research/domain/ssb-operational-workflow.md)
§0.2 C-1, §5).

**DECISION D-5 (accepted)** — **IBVAP satisfies "integration with existing
command and control systems" by being an emitter with a documented, stable, open
event contract, demonstrated against at least one real external integration path —
not by shipping an adapter for a named system.** MVP ships the published, versioned
event schema plus a generic outbound mechanism (e.g. webhook, REST, or MQTT), and
demonstrates that mechanism actually delivering events to a real external consumer
end-to-end. Standards-based egress (ONVIF Profile M over MQTT; MISB ST 0903 VMTI
within STANAG 4609) and adapters for a **specific named C2 system** remain
post-MVP, unless and until a real target system is identified — **and no vendor
surveyed emits either standard today**.
*Rationale:* building an adapter for a system that has no name is the documented
integration risk; a published, demonstrated generic contract is the strongest form
of the requirement that can be satisfied before H-6 is answered — it proves the
mechanism works end-to-end without inventing a target that does not exist.
*Falsified by:* H-6 naming a system, at which point a reference adapter to that
named system becomes MVP-worthy.

---

## 6. Product goals

Each goal maps to a required outcome of the problem statement
([goals.md](../00-project/goals.md)) and to the measure that will test it
([§13](#13-success-metrics)).

| # | Product goal | Maps to statement outcome | Measured by |
|---|---|---|---|
| **G1** | **A camera the force already owns produces machine-generated events without new camera hardware** | 1, 2 | SM-6 |
| **G2** | **The events are trustworthy enough to be acted on** — a measured, published nuisance rate with a cause histogram, per camera | 3 | SM-1, SM-2 |
| **G3** | **A human learns about something worth their attention, and can assess it, faster than by watching** | 3, 5 | SM-3, SM-4 |
| **G4** | **The system states, per camera, what it can and cannot do — and refuses what it cannot** | 4 (honestly), 2 | SM-5 |
| **G5** | **It runs where the market's architectures will not: no console, no engineer, no reliable link, no reliable power** | 7 | SM-7, SM-9, SM-10 |
| **G6** | **Everything it observes is logged in a form that survives a handover to another organisation** | 3 (event logging), 6 | SM-11 |
| **G7** | **What it emits can be consumed by a command and control system that has not been named yet** | 6 | SM-12 |
| **G8** | **The force can answer "did this help?"** | 5, 7 | SM-8 |
| **G9** | **All eight named capabilities are present, each at a declared and measured grade** | statement §Description | SM-13, [§18](#18-acceptance-criteria) |

**G9 is a first-class goal, not a compliance footnote.** The problem statement is
the primary requirement; "we decided capability *n* was operationally
misdirected" is not an available answer. What *is* available is delivering it with
its constraints and grade stated — which is what
[§9](#9-sih-required-capabilities) does.

---

## 7. Functional requirements

Requirements are grouped. Each carries **MVP** / **POST-MVP** and a trace to the
evidence or statement clause that produces it. Capability-specific requirements live
in [§9](#9-sih-required-capabilities) and are cross-referenced, not duplicated.

### 7.1 Ingest and camera handling

| # | Requirement | Priority | Trace |
|---|---|---|---|
| **FR-1** | Ingest live video from standard IP-based CCTV via RTSP, and via ONVIF where the device supports it, using credentials the force already holds | **MVP** | Statement (§Description) |
| **FR-2** | Ingest from **analog cameras behind an existing DVR/XVR/NVR**, treating each channel as a source | **MVP** | **FACT [rig-measured]** — the recorder in this repository is exactly this shape; the market's broadest-ingest vendor explicitly lists analog-via-DVR |
| **FR-3** | Operate **read-only** against the existing estate: never reconfigure a camera or recorder as a side effect, never take ownership of recording, never alter the existing live-view path | **MVP** | PR8; NG-1 |
| **FR-4** | Where the product *is* asked to write a device setting, **verify by read-back** and report the actual landed value | **MVP** | **FACT [rig-measured]** — firmware returns OK for values it silently discards |
| **FR-5** | Detect and correct anamorphic/"1080N"-style encoding, and report the **effective** resolution, never the advertised one | **MVP** | **FACT [rig-measured]** — 1080N squeezes 1920×1080 into 960×1080 |
| **FR-6** | Maintain and expose a **tested-device record**: which makes/models/firmware have been verified, with what result | **MVP** | **FACT [GLOBAL]** — "we support ONVIF" is an intention, not a capability; a certified ONVIF client still runs a compatibility lab |
| **FR-7** | Degrade gracefully and *visibly* when a source is unavailable, unstable, or returns fewer frames than requested | **MVP** | PR4 |

### 7.2 Camera Spec Sheet — capability measurement and disclosure

| # | Requirement | Priority | Trace |
|---|---|---|---|
| **FR-8** | Measure, per camera: effective resolution, achievable analysed fps, codec/GOP, bitrate, day/night transition behaviour, and stability | **MVP** | E-1, E-8 |
| **FR-9** | Derive **pixels-per-metre at operator-marked reference distances**, and express it against published detection/observation/recognition/identification thresholds | **MVP** | DORI/OODPCVS `[T8][T9]` |
| **FR-10** | Publish a per-camera, per-analytic eligibility verdict — `Eligible` / `Eligible, degraded` / `Not eligible` — **with the measured reason in plain language** | **MVP** | O1, G6 |
| **FR-11** | **Refuse to enable an analytic on a camera whose Spec Sheet marks it `Not eligible`**, with an explicit, logged, named-authority override that stamps every resulting Event as `capability-overridden` | **MVP** | D-6; PR1, PR10 |
| **FR-12** | Re-issue the Spec Sheet on demand and on schedule, and raise a change when a camera's measured capability drops (moved, refocused, dirty, IR failed) | **MVP** | O10 |
| **FR-13** | Report **silent analytic degradation** distinctly from stream loss, in language a non-technical post commander can relay over a radio | **MVP** | O10, PP3, U9 |

**DECISION D-6 (accepted)** — **A capability that the camera cannot support is
refused, not degraded.** Overriding is possible, requires a named authority, and
permanently marks the resulting events.
*Rationale:* this is the product's central claim (D-1) and the market's unfilled gap;
a soft warning would be indistinguishable from every vendor's disclaimer.
*Known cost:* it means telling a buyer their estate cannot do what they hoped — the
counter-evidence recorded against opportunity O1.

### 7.3 Analytics primitives

| # | Requirement | Priority | Trace |
|---|---|---|---|
| **FR-14** | Detect **persons** on eligible cameras | **MVP** | CAP-1 |
| **FR-15** | Detect **vehicles** and assign a **coarse type** class on eligible cameras | **MVP** | CAP-2 |
| **FR-16** | **Track** detected objects within a single camera view, maintaining identity across the analysis window | **MVP** | CAP-1 |
| **FR-17** | Detect **faces** (presence and location, not identity) on eligible cameras | **MVP** | CAP-3a |
| **FR-18** | Read **number plates** on cameras whose Spec Sheet marks ANPR eligible | **MVP** | CAP-4 |
| **FR-19** | Operate every primitive at a configurable analysed frame rate, with a **product floor** below which tracking-dependent rules are automatically disabled and the operator told why | **MVP** | **FACT** — identity association collapses below ~2–3 analysed fps (AssA 43.6% → 27.8% between 3 and 1 fps) |
| **FR-20** | Recognise faces against a **bounded, explicitly configured, authorized watchlist gallery**. Ships in MVP and is usable in a **controlled development/test environment**. Against a **real deployment**, matching is **technically blocked** unless four separately recorded conditions are all configured and current: **(1)** a legal basis for that deployment, **(2)** the required authority record, **(3)** the authorized gallery, **(4)** retention/oversight requirements. **The authority record (2) is never treated as evidence that the legal basis (1) exists.** The environment classification (dev/test vs. operational) is itself an explicit, authority-controlled, audited setting | **MVP, gated** (dev/test); **blocked** for real deployment pending (1)–(4) | CAP-3b; D-7 |
| **FR-21** | Track objects **across cameras** | **POST-MVP** | Feasibility Low; re-ID degrades badly out of domain |
| **FR-22** | Detect operationally-relevant non-standard classes (loaded porter, cart, driven livestock, timber load) | **POST-MVP, research-gated** | **FACT [SIH/SSB]** — these dominate the force's ledger and are **not** standard model classes |

### 7.4 Rules, zones and alerting

| # | Requirement | Priority | Trace |
|---|---|---|---|
| **FR-23** | Author **zones, lines, directions and dwell timers** per camera, gated on **object class and confidence and minimum track length** | **MVP** | CAP-5; object-gated rules are strictly better than pixel-motion rules |
| **FR-24** | Compose rules into **operator-authored composite conditions** across class, zone, direction, dwell, time-of-day and camera | **MVP** | CAP-6 |
| **FR-25** | Ship a **starter rule library**, every entry of which is explicitly marked *unvalidated against this force's definition of suspicious* | **MVP** | **UNKNOWN** — "suspicious activity" is undefined in the statement and in every retrieved source (Q-3 / SQ-7 / OQ-4) |
| **FR-26** | Apply **time-of-day scoping** to any rule, with per-camera night eligibility applied automatically | **MVP** | CAP-7 |
| **FR-27** | Distinguish **Event** from **Alert**: every observation is logged; only rule-selected observations interrupt a human | **MVP** | D-4, §5.2 |
| **FR-28** | Deliver alerts **payload-progressively**: event record → object crop → full clip on demand | **MVP** | CALCULATION §5.5 |
| **FR-29** | Record a human **assessment** (real / not real / unsure) against any Alert, in one action | **MVP** | W3; SM-2 |
| **FR-30** | Offer **visible, reversible, per-camera-per-rule suppression** driven by assessments. Never suppress silently, never suppress globally, never suppress without showing the count of what was suppressed | **MVP** | T2; PR2 |
| **FR-31** | Route alerts to a configurable set of destinations without assuming any of them exists: local annunciation at the post, an on-site display, a queued message to a higher echelon, an outbound integration | **MVP** | D-3, D-4 |

### 7.5 Event log, evidence and time

| # | Requirement | Priority | Trace |
|---|---|---|---|
| **FR-32** | Write every Event to a **local, append-only, hash-chained log** that continues to function with no link and no operator | **MVP** | Statement capability 8; §5.2 |
| **FR-33** | Compute the evidence **hash at capture**, over the stored bitstream, not over an exported copy | **MVP** | **FACT [MARKET:IN]** — s.63 BSA requires the hash; **transcoding changes it** |
| **FR-34** | **Never silently re-encode** media on any export or retrieval path; if a transformation is unavoidable, produce it as an additional artefact and preserve the original with its hash | **MVP** | ibid. |
| **FR-35** | Maintain and **display a time-integrity status** for every camera and every Event: synchronised / drifting / unverified / known-bad — and mark Events created under a suspect clock | **MVP** | **UNKNOWN — blocks any evidential design**: whether target sites have NTP, GNSS or any time source. *A silent wrong clock is the worst version of the evidential risk* |
| **FR-36** | Produce an **evidence export pack** containing the original segments, hashes, event records, custody log and a certificate template naming the s.63 BSA fields — openable and verifiable **without IBVAP installed** | **MVP** | J7, U8 |
| **FR-37** | Record chain of custody for every export: who, when, what, from which device | **MVP** | s.63 BSA |
| **FR-38** | Apply **per-class retention** (continuous video, event clips, crops, metadata) with configurable periods and an explicit, logged deletion record | **MVP** | **UNKNOWN** — mandated retention is unestablished (OQ-9); therefore configurable, never hard-coded |
| **FR-39** | Query the local event store by time, camera, zone, class, rule, assessment and outcome | **MVP** | J5, J8, W5 |

### 7.6 Site operation, resilience and health

| # | Requirement | Priority | Trace |
|---|---|---|---|
| **FR-40** | Perform all analysis **at the site**; never require full video to leave it | **MVP** | Arithmetic (§5.3 of the tech research); market pattern P2 |
| **FR-41** | Continue analysing, logging and locally alerting **with the uplink down**, for a declared minimum duration | **MVP** | O2(a) |
| **FR-42** | Queue outbound events and reconcile on reconnect **idempotently** — no duplication, no loss, monotonic identifiers | **MVP** | O2(b) |
| **FR-43** | Bound the local queue and apply a **declared, visible discard policy** when it fills — because at a site offline for days, it *will* fill | **MVP** | O2(b); **HYPOTHESIS** carried from the tech research |
| **FR-44** | **Never expire, disable or degrade because it could not reach a licence or update server** | **MVP** | O2(c) |
| **FR-45** | Report health in **plain language for a non-technical reader**, including: source down, source degraded, analytic degraded, clock suspect, queue filling, storage filling, power event | **MVP** | PR4, U9 |
| **FR-46** | Survive unclean power loss without corrupting the event log or the hash chain | **MVP** | Generator/solar power at target sites |
| **FR-47** | Install and be commissioned **without a certified integrator and without a formal site survey** | **MVP** | O9 — *paired with* FR-10, which is what makes it honest |
| **FR-48** | Update in a way that assumes no engineer visits the site and tolerates interruption | **MVP** | 42% unroaded; no on-site technical cadre |

### 7.7 Measurement and attribution

| # | Requirement | Priority | Trace |
|---|---|---|---|
| **FR-49** | Continuously compute and expose, per camera and per rule, the **alert rate and the assessed-nuisance rate**, with a **cause histogram** | **MVP** | O3, G2 — *the number the entire market declines to publish* |
| **FR-50** | Record an **outcome attribution** on every Case: did this event contribute to an apprehension, a seizure, a dismissal, or nothing | **MVP** | J10; **FACT** — GAO found the contribution of surveillance technology was not determinable, and found ~500 recorded assists in a sector with no such assets |
| **FR-51** | Make the attribution data exportable as a **plain dataset**, so the force can audit it independently of IBVAP's own reporting | **MVP** | GAO's data-quality failure is the counter-example |
| **FR-52** | Report **energy consumed** by the analytics workload where the platform can observe it | **POST-MVP** | O4 — zero vendors publish watts |

### 7.8 Egress and integration

| # | Requirement | Priority | Trace |
|---|---|---|---|
| **FR-53** | Publish a **stable, versioned, documented event schema** covering time, camera, site, object class, rule, confidence, geometry, evidence pointer, assessment and outcome | **MVP** | D-5, G7 |
| **FR-54** | Emit events outbound over a generic, configurable mechanism, with retry, backoff and idempotency | **MVP** | D-5 |
| **FR-55** | Expose a local read API for events, evidence pointers and health | **MVP** | W5, W6 |
| **FR-56** | Emit **ONVIF Profile M metadata over MQTT** | **POST-MVP** | O7 — exists, vendor-neutral, unused by the market |
| **FR-57** | Emit **MISB ST 0903 VMTI** within STANAG 4609 | **POST-MVP** | O7 — NATO-compatible C2 systems already ingest it |
| **FR-58** | Aggregate events from multiple sites at a higher echelon | **POST-MVP** | Gated on H-1/H-6 — we do not know which echelon would host it |

### 7.9 Administration, authority and audit

| # | Requirement | Priority | Trace |
|---|---|---|---|
| **FR-59** | Authenticate users and record an **audit trail** for every configuration change, override, suppression, export and deletion | **MVP** | s.63 BSA custody; NFR-14 |
| **FR-60** | Gate legally-sensitive capabilities behind an explicit **authority record** — who authorised it, under what instrument, with what expiry — not behind a feature flag. **The authority record is necessary but not sufficient: the product must never treat it as evidence that an underlying legal basis exists** — the legal-basis record is a separate, independently required and independently recorded condition (see FR-20) | **MVP** | PR11; D-7 — gates CAP-3b face recognition (itself gated MVP, blocked for real deployment pending FR-20's four conditions); also applies to any capability still deferred behind it (e.g. PM-5) |
| **FR-61** | Operate with **no outbound internet dependency**, and permit deployment on an isolated network | **MVP** | **UNKNOWN** — data classification and network policy for border video is unestablished (OQ-10); therefore assume the most restrictive |

---

## 8. Non-functional requirements

Every NFR below is either (a) derived from measured evidence, or (b) explicitly
marked as a **target to be validated**, because **FACT [GLOBAL]** — the industry
publishes neither accuracy, nor false-alarm rate, nor power, nor
disconnection behaviour (the disclosure asymmetry, P10), so there are no market
figures to inherit.

| # | Non-functional requirement | Basis |
|---|---|---|
| **NFR-1** | **Alert latency (site-local):** from the analysed frame that satisfies a rule to a locally-annunciated alert, **target ≤ 5 s** at the product's analysis-rate floor. **To be validated**, not asserted | No latency budget exists anywhere in the research; E-9 |
| **NFR-2** | **Alert latency (remote):** from the same frame to a remote human seeing *event + crop*, **target ≤ 30 s on a 128 kbps link** — of which the crop is ~1.6 s of transfer | CALCULATION §5.3 of the tech research |
| **NFR-3** | **Evidence latency:** full clip retrievable on demand; the product must **state the expected wait** before the user asks (7.8 min on 128 kbps is a legitimate answer; a silent 7.8-minute wait is not) | ibid. |
| **NFR-4** | **Nuisance rate:** IBVAP publishes its measured rate per camera per rule. **No numeric target is set in this PRD, and setting one before X1 is run would be fiction.** The requirement is that the number is measured, exposed and improvable | O3; the 90% SBInet precedent is the thing to beat, not a target to adopt |
| **NFR-5** | **Analysis-rate floor:** tracking-dependent rules require ≥3 analysed fps; below it they are disabled, not silently degraded | AssA 43.6% → 27.8% between 3 and 1 fps |
| **NFR-6** | **Disconnection tolerance:** full local function for **≥ 72 hours** with no uplink, with events reconciling on reconnect without duplication or loss | E-11 / experiment 7 |
| **NFR-7** | **Bandwidth:** steady-state outbound at a quiet site must fit within a **128 kbps** shared link alongside voice; the product must expose its own consumption | §5.3; A4 |
| **NFR-8** | **Power:** the analytics workload must have a **stated, measured** wattage per site configuration, because at a fuel-limited, unroaded site an extra 15–60 W is a logistics cost, not an electrical one | §4.6; O4 |
| **NFR-9** | **Estate safety:** adding IBVAP must not degrade the existing recorder's own recording or live-view path — **verified before any live estate is touched** | E-12; **this is a safety precondition, not a performance goal** |
| **NFR-10** | **Commissioning effort:** a two-camera site commissioned by a non-specialist in **≤ 1 hour**, without a site survey or certified integrator | O9; certification in this market is priced at 2–3 days and USD 595–2,995 |
| **NFR-11** | **Legibility:** every user-facing failure state expressible in one sentence a non-technical post commander can relay over a radio | PR4, U9 |
| **NFR-12** | **Scale axis:** the product's cost, configuration and operational model must scale by **site count**, not by user count or central capacity | A11, PR12; per-camera pricing is universal in the market and penalises this shape |
| **NFR-13** | **Data residency / isolation:** deployable with no internet access and no cloud dependency | OQ-10; NG-6 |
| **NFR-14** | **Auditability:** every override, suppression, export, deletion and authority grant is attributable to a person and a time | s.63 BSA; FR-59 |
| **NFR-15** | **Integrity:** the event log is append-only and tamper-evident **in every deployment**, not in an upper edition | G10; **FACT** — the market gates signing and tamper-evidence to upper editions, so *the smallest, most remote deployments get none of it* |
| **NFR-16** | **Honesty invariant:** no user-facing surface may state or imply a capability the Camera Spec Sheet marks `Not eligible` | D-1, D-6 |

---

## 9. SIH-required capabilities

**This section is the compliance spine of the document.** Every capability named in
[problem.md](../00-project/problem.md) appears here, **none is dropped, narrowed
away, or reinterpreted**. For each: user outcome, functional requirement, operating
constraints (stated, not hidden), acceptance criteria, and MVP priority.

**DECISION D-8 (accepted)** — **All eight SIH capabilities are explicitly
addressed in the product, with implementation maturity, operating conditions and
limitations declared for each.** Each is delivered at a *declared grade*, gated by
the Camera Spec Sheet, with its limitations stated in the product surface. No
capability is delivered as an unqualified claim, and **no SIH capability is
silently omitted**.
*Rationale:* the problem statement is the primary requirement (rule 1) and inventing
requirements is forbidden (rule 2); but the research establishes hard physical bounds
on several of these capabilities on inherited cameras, and PR1/PR10 forbid claiming
what cannot be measured. Declaring maturity, operating conditions and limitations
per capability is the only construction that satisfies both — an unqualified claim
of full delivery would violate PR1/PR10, and dropping any capability would violate
rule 2.

### Grade vocabulary used below

| Grade | Meaning |
|---|---|
| **Primary-candidate** | May be trusted as the sole detection mechanism for its rule, subject to measurement |
| **Support** | Brings a human to the right frame; the human decides. *(i-LIDS' "secondary" category)* |
| **Conditional** | Available only on cameras whose Spec Sheet marks it eligible; typically a lane-aimed or purpose-sited camera |
| **Gated** | Available only when a legal basis and named authority are recorded |

**DECISION D-9 (accepted)** — **IBVAP is an intelligent video-analytics layer
that can operate alongside existing surveillance/VMS infrastructure and integrate
with external command/control systems** — not a system that replaces the existing
surveillance system or that removes the human from assessment. Per capability, an
alert routes to a human for assessment rather than acting as the sole basis for a
decision; in i-LIDS terms, IBVAP operates in a *support* posture for every
capability in the MVP, not as the *primary* (sole) detection system.
*Rationale:* i-LIDS distinguishes these and the choice determines alerting, staffing
and liability; the competitive research explicitly names this as a decision to be
made deliberately rather than by default. IBVAP has no measured detection
probability on this estate and will not have one before X1/X2. Operating as an
additive support layer alongside existing infrastructure is the honest posture and
is reversible upward per-rule once measured; declaring itself the sole detection
system is not reversible after a miss.

---

### CAP-1 — Human detection and tracking

**Grade: Support. MVP priority: P0 — the foundation primitive.**

| Aspect | Definition |
|---|---|
| **User outcome** | *"I am told when a person is where a person should not be, or is doing something I asked to be told about — without me watching the screen."* (J1, J2) |
| **Functional requirement** | FR-14 (detect persons), FR-16 (track within a camera), FR-19 (analysis-rate floor), FR-23 (class-gated rules), FR-27 (event vs alert) |
| **Operating constraints** | **(a)** Detection is the least demanding pixel level (~25 px/m) but a person at long range on a wide-angle camera may still fall below the model's minimum object size (documented 12–32 px). **(b)** Tracking requires **≥3 analysed fps**; below it, identity association collapses. **(c)** Occlusion is the documented dominant tracking failure mode. **(d)** Night detection on visible cameras degrades measurably — see CAP-7. **(e)** **Cross-camera** tracking is *not* in MVP: feasibility Low, re-ID degrades badly out of domain, and fixed non-overlapping cameras give no geometric constraint |
| **Acceptance criteria** | **AC-1.1** On a camera the Spec Sheet marks eligible, a person walking a pre-marked route in daylight is detected in ≥95% of the frames in which they are unoccluded and above the stated pixel threshold. **AC-1.2** Track identity persists across the route without a switch, at the product's stated analysis rate. **AC-1.3** At an analysis rate below the floor, tracking-dependent rules are automatically disabled and the operator is told why, in one sentence. **AC-1.4** A person below the camera's stated pixel threshold is **not** claimed as a detection failure — the Spec Sheet already told the operator that range is out of scope |
| **MVP priority** | **P0.** Every other capability composes from it |

---

### CAP-2 — Vehicle detection and classification

**Grade: Support (detection + coarse class). MVP priority: P0.**

| Aspect | Definition |
|---|---|
| **User outcome** | *"I am told when a vehicle appears, stops, or moves in a direction I care about on my stretch — and roughly what kind it is."* |
| **Functional requirement** | FR-15, FR-16, FR-23 |
| **Operating constraints** | **(a)** "Classification" means **coarse type** (car / truck / bus / motorcycle / bicycle). **Make, model and colour are explicitly out of MVP** — they need Recognition-grade pixel density and are far more viewpoint- and illumination-sensitive. **(b)** **Colour is gone at night** on IR-illuminated cameras — IR-illuminated video is effectively monochrome, so every colour-dependent attribute degrades or fails after dark. **(c) [SIH/SSB]** The vehicle classes that matter most on this border — a loaded porter's cart, a tractor-trailer carrying forest produce, driven livestock — are **not standard model classes**. FR-22 addresses this and is **post-MVP and research-gated** |
| **Acceptance criteria** | **AC-2.1** On an eligible camera, a vehicle traversing a marked zone in daylight is detected in ≥95% of unoccluded frames above threshold. **AC-2.2** Coarse class is assigned, and the product **states its class vocabulary explicitly** rather than implying an open taxonomy. **AC-2.3** No user-facing surface offers make/model/colour in MVP. **AC-2.4** Where the ledger's real classes (porter, cart, livestock) are not supported, the product says so on the surface where a user would look for them |
| **MVP priority** | **P0** for detection + coarse class; **P3 / post-MVP** for non-standard classes; **excluded** for attributes |

---

### CAP-3a — Face detection

**Grade: Support, Conditional. MVP priority: P1.**

| Aspect | Definition |
|---|---|
| **User outcome** | *"Where a camera is sited so it can see faces, I know a face was present and can retrieve that frame."* Presence and location — **not identity** |
| **Functional requirement** | FR-17, with FR-10 eligibility gating |
| **Operating constraints** | **(a)** Face detection is high-achievability *where a face is large enough — and that is the whole question*. **(b)** An overhead-mounted, wide-angle camera installed for area overview **looks down on the tops of heads**; this is mounting geometry and no model fixes it. **(c)** Accuracy is dominated by face angle and lighting. **(d)** Consequence: on most of an inherited overview estate, this capability will be marked `Not eligible` — and **the product will say so rather than return nothing and imply nothing was there** |
| **Acceptance criteria** | **AC-3a.1** Camera Spec Sheet reports face-detection eligibility per camera with the measured reason. **AC-3a.2** On an eligible (typically lane- or gate-aimed) camera, a face presented at the stated range is detected. **AC-3a.3** On a `Not eligible` camera the analytic **cannot be switched on** without a logged override. **AC-3a.4** The product never presents "no faces detected" from a `Not eligible` camera as evidence that no face was present |
| **MVP priority** | **P1.** Named explicitly in the statement's capability list; cheap on top of CAP-1; the eligibility disclosure is the real deliverable |

---

### CAP-3b — Face recognition *(the statement's "support facial recognition … through software")*

**Grade: Gated, Conditional, watchlist-only. MVP priority: P1, gated** — the
capability ships in MVP and can be exercised and demonstrated in a **controlled
development/test environment** against an explicitly configured, bounded gallery;
**enabling it against a real deployment is technically blocked** unless the four
conditions in D-7 (legal basis, authority record, gallery, retention/oversight)
are all configured and current for that deployment. See D-7.

| Aspect | Definition |
|---|---|
| **User outcome** | *"If a person on a small, lawfully authorised watchlist appears at a lane-aimed camera, I am told."* **Not** identification of the population |
| **Functional requirement** | FR-20 (bounded watchlist), FR-60 (authority record), FR-10 (eligibility) |
| **Operating constraints — stated in full, because this is the capability most at risk of being oversold** | **(a) NIST's own conclusion:** video face recognition may approach still-photo accuracy *"but only if image collection can be improved"* — camera positioning, mounting, lighting, optics. **All four are hardware, and improving them is precisely what this deployment model forbids.** **(b)** NIST FIVE reports identification anywhere from **~60% to >99%**, purely on video/image quality; the named degradations are small faces, uneven lighting, non-forward-facing angles. **(c)** Sub-0.1% error rates quoted in the market come from **mugshot- and visa-quality stills** and are not transferable to CCTV. **(d)** NIST's own advice is to **limit gallery size** — a watchlist of tens of known traffickers is a fundamentally different and easier problem than open-set identification, and only the former is contemplated here. **(e) [SIH/SSB] Legal:** applying face recognition on a treaty-open border processes biometrics of people committing no offence who have a **treaty right** to be there, including nationals of friendly states. The legal basis, authorisation level, retention rule and oversight are **UNKNOWN** (OQ-7). **(f) [MARKET:EU]** Real-time remote biometric identification in publicly accessible spaces for law enforcement is prohibited by default under EU AI Act Art. 5 from 2 Feb 2025. **(g) [SIH/SSB]** The named department has **already procured** a CCTV setup with FRS and ANPR; where it is deployed and what it is are **UNKNOWN** (OQ-6) |
| **Acceptance criteria** | **AC-3b.1** In a **controlled development/test environment**, the capability can be enabled and demonstrated against an explicitly configured, bounded test gallery, without satisfying AC-3b.2 — because a dev/test environment does not process the biometrics of the actual protected population. **AC-3b.2** Against a **real deployment**, biometric matching is **technically blocked** unless all four conditions are configured and current: **(a)** a recorded legal basis for that specific deployment, **(b)** the required authority record (who authorised, under what instrument, scope, expiry), **(c)** the authorized bounded gallery, and **(d)** applicable retention/oversight requirements. **(b) is never treated by the product as evidence that (a) exists — they are recorded as separate, independently required fields.** **AC-3b.3** The environment classification itself (development/test vs. operational) is an explicit, authority-controlled, audited setting; an operator cannot self-declare an operational site as "test" to bypass AC-3b.2. **AC-3b.4** Gallery is bounded and its size is stated in the product surface. **AC-3b.5** Only cameras whose Spec Sheet marks recognition-grade eligibility may run it. **AC-3b.6** A no-match generates **no biometric record**, and the retention rule for templates and probes is explicit, configurable and audited. **AC-3b.7** Every match is `support`-graded — it is a reason to look, never an identification assertion. **AC-3b.8** Every biometric operation — enable, match, no-match, gallery change, authority-record change, legal-basis-record change, environment-classification change, expiry — is logged and auditable |
| **MVP priority** | **P1, gated.** **DECISION D-7 (accepted):** Face **detection** (CAP-3a) ships unconditionally in MVP. **The controlled face-recognition capability also ships in MVP** and can be **exercised and demonstrated in a controlled development/test environment**, against an explicitly configured, bounded gallery. **For a real deployment, biometric matching is technically blocked** unless all four conditions are configured and current for that deployment: **(1)** a recorded, valid legal basis for that deployment; **(2)** the required authority record; **(3)** the authorized, bounded gallery; **(4)** applicable retention and oversight requirements. **The authority record is never treated by the product as evidence that the legal basis exists — the two are separate, independently required and independently recorded conditions.** Any biometric operation outside those configured, satisfied conditions is **blocked by the product**, not merely discouraged, and every biometric operation — enable, match, no-match, gallery change, authority-record change, legal-basis-record change, expiry — is **logged and auditable**. **No unrestricted, open-set or population-scale face recognition ships at any point.** *Rationale:* the statement requires facial recognition to be *supported through software*, and this decision ships that support in MVP — demonstrable now, technically gated for real use — without asserting a legal basis this project has not established. **This document does not claim, and this decision does not create, a legal basis for activating biometric matching against the SSB deployment; OQ-7 (the legal basis, authorisation level, retention rule and oversight for biometrics on a treaty-open border) remains explicitly unresolved.** *This decision is the one most likely to be contested at SIH evaluation and needs an explicit human call.* |

---

### CAP-4 — Automatic Number Plate Recognition (ANPR)

**Grade: Conditional (lane-aimed cameras only). MVP priority: P1 at eligible nodes.**

| Aspect | Definition |
|---|---|
| **User outcome** | *"At a check post, ICP lane or barrier, the plate of a passing vehicle is read and logged automatically, so I am not writing it in a register."* |
| **Functional requirement** | FR-18, FR-10 (eligibility), FR-32 (logged) |
| **Operating constraints** | **(a)** **Already solved twice in software** by the two largest VMS vendors — and both attach *physical* constraints: ≤50 km/h in one case, ≤30° mounting angle in the other. **The dependency moved from the camera's silicon to the camera's mounting; it did not disappear.** **(b)** Plate reading needs Identification-grade pixel density (~250 px/m under the 2015 standard) — far above a wide-area border-road camera at range. **(c)** Documented failure modes: plate condition, non-standard formats, motion blur, contrast, reflections, tilt/skew, fog, day/night. **(d)** Dedicated ANPR cameras achieve 95–99% using **fast/global shutters** and **plate-tuned IR illuminators** — physical mechanisms software cannot substitute. **(e)** End-to-end accuracy drops ~15 points between two *curated* research datasets (93.53% → 78.33%) — the best available estimate of how fast ANPR degrades as conditions get real. **(f) [MARKET:IN]** India has ~210 million vehicles and **50+ plate types**, against ANPR accuracy often exceeding 90% in standardised-plate countries. **(g)** ANPR on wide-area border-road cameras is a **non-goal** (NG-4) — physics, not effort |
| **Acceptance criteria** | **AC-4.1** The Spec Sheet marks ANPR eligibility per camera, deriving it from measured plate-scale pixel density and mounting angle, and states the **speed and angle envelope** it is valid within. **AC-4.2** On an eligible lane-aimed camera within that envelope, plates are read and logged with per-read confidence. **AC-4.3** Reads outside the stated envelope are marked as such, not silently included. **AC-4.4** ANPR **cannot be enabled** on a `Not eligible` camera without a logged override. **AC-4.5** The product publishes its **measured** read rate on the deployment's own footage; no vendor-style headline accuracy figure is claimed |
| **MVP priority** | **P1** at eligible nodes (check post / ICP lane / barrier), **excluded** elsewhere. **Note [SIH/SSB]:** whether such a camera exists, and who owns the CCTV at ICP Raxaul and Jogbani, are **UNKNOWN** (OQ-11) — so this capability may have **no eligible camera in the validation estate**, which the Spec Sheet will state plainly rather than hide |

---

### CAP-5 — Virtual fence intrusion detection

**Grade: Support (mechanism Primary-candidate, nuisance rate unproven). MVP priority: P0.**

| Aspect | Definition |
|---|---|
| **User outcome** | *"I draw a line or an area on the picture, say what kind of object and what time of day I care about, and I am told when it happens — without being told a hundred times a night about a cow, a moth and a branch."* |
| **Functional requirement** | FR-23 (object-class-gated zones, lines, directions, dwell), FR-26 (time scoping), FR-30 (visible reversible suppression), FR-49 (measured nuisance rate) |
| **Operating constraints** | **(a) The mechanism is trivial; the product is the nuisance rejection.** A polygon, a line, a direction and a dwell timer are commodity — including in free open source. The entire industry's effort goes into false-alarm rejection. **(b)** Documented outdoor false-trigger sources: rain, fog and snow altering contrast; wind-moved vegetation; sunrise/sunset and headlights creating reflections and shadows *"that basic algorithms read as suspicious movement"*; and at night, IR hotspot glare and insects attracted to the emitter. **(c)** The precedent is **90% false alarms** (SBInet), and CIBMS analysis records that its design **defines no protocol for distinguishing infiltrators from wildlife**. **(d) [SIH/SSB] — the framing constraint:** on the validation border, **crossing is a treaty right** and MHA's own statement of the problem is *"misuse of the open border"*. **A line-crossing alarm that fired with perfect accuracy would still be almost entirely noise there.** **(e) [SIH/SSB]** The usual "noise" categories invert: cattle (432 cases), forest products (398) and wildlife (78) are **seizure categories — i.e. targets** — so mitigations tuned for a fenced border may not transfer |
| **Acceptance criteria** | **AC-5.1** Zones, lines, directions and dwell rules are authorable per camera by a non-technical user and are **gated on object class, confidence and minimum track length** — never on raw pixel motion. **AC-5.2** A person crossing a configured line in daylight on an eligible camera generates exactly one Event. **AC-5.3** The measured alert rate and **cause histogram** are visible per camera per rule, continuously (FR-49). **AC-5.4** Suppression driven by `not real` assessments is visible, reversible and shows what it suppressed. **AC-5.5 [SIH/SSB]** The product supports framing a zone as an **attention zone** (report *who/what/when*, not *that a line was crossed*) so the capability is usable on an open border; **the intrusion framing remains available and unchanged for closed-border deployments** |
| **MVP priority** | **P0.** Explicitly named by the statement, and the substrate CAP-6 composes on |

**DECISION D-10 (accepted)** — **The virtual-fence capability ships in full,
and additionally supports an open-border framing.** IBVAP does not remove or rename
intrusion detection; it adds the ability to make the *reportable condition* be
class, time, direction, dwell or accompaniment rather than the crossing itself.
*Rationale:* the statement requires the capability (rule 1) and it is technically
straightforward; the research establishes it is operationally misdirected **on this
particular border** but not on fenced borders generally — which is exactly the
[BORDER] vs [SIH/SSB] distinction [CLAUDE.md](../../CLAUDE.md) §4 demands.

---

### CAP-6 — Suspicious activity detection

**Grade: Support, rule-based only. MVP priority: P1, with its definition explicitly unresolved.**

| Aspect | Definition |
|---|---|
| **User outcome** | *"I can express the things that actually worry me on my stretch — 'a person in the orchard between 2200 and 0500 for more than 90 seconds', 'a vehicle stopped on the border road outside a lay-by for more than 5 minutes' — and be told when they happen."* |
| **Functional requirement** | FR-24 (composite rules), FR-25 (starter library, marked unvalidated), FR-26 (time scoping), FR-23 (primitives) |
| **Operating constraints — this is the weakest capability in the statement and its weakness is measured** | **(a)** **The term is undefined.** It is undefined in the problem statement and in **every retrieved source**, and it is materially harder to define on an open border where crossing is lawful (OQ-4). **(b)** **Learned anomaly detection does not transfer:** models scoring **94.55% AUC** collapse to **16.35%** on same-scene evaluation with reversed labels — much of the reported performance is scene memorisation, not anomaly understanding. **(c)** Methods with ≤10% false-alarm rates on standard test sets show a **42% average increase** on hard-normal benchmarks, **some exceeding 70% FAR**. **(d)** **The ground truth is contested:** human annotators agree only at Fleiss' κ **0.51–0.68**. **(e)** The headline metrics (AUC, AP) are **insensitive to *when* a detection occurs** — which is the entire operational point. **(f)** The market has no consensus solution either: rule engines with documented high false-positive rates, or learned anomaly detection needing a stable "normal", plus unproven vision-language approaches |
| **Acceptance criteria** | **AC-6.1** A non-technical user can author a composite rule over class, zone, direction, dwell, time-of-day and camera **without writing code**. **AC-6.2** Every rule states, in the UI, what it will and will not catch. **AC-6.3** The starter library ships with each entry **marked as an unvalidated proposal**, not as a definition of suspicious. **AC-6.4** Rule firings carry the same measured nuisance reporting as CAP-5 (FR-49). **AC-6.5** The product **does not present a learned anomaly score as "suspicious activity"** anywhere in MVP |
| **MVP priority** | **P1** as operator-authored composite rules. **P-never (MVP)** as a learned anomaly model — see NG-2 |

**DECISION D-11 (accepted)** — **"Suspicious activity detection" is delivered
as an operator-authored composite rule engine over reliable primitives, plus a
starter library explicitly marked unvalidated. No learned anomaly model ships in
MVP.**
*Rationale:* three independent, measured failures of learned VAD (scene overfitting,
false-alarm explosion, contested ground truth) against a capability whose definition
nobody has supplied. The rule engine is the only construction that can be *honest*
about what it detects. **This decision must be revisited the moment OQ-4 is answered
by the force — no experiment substitutes for that answer.**

---

### CAP-7 — Night-time movement detection

**Grade: Support, with per-camera night eligibility. MVP priority: P0 — an explicit
product capability**, implemented as a first-class, separately-measured operating
mode across the existing detection primitives rather than as a separate detector;
see D-12.

| Aspect | Definition |
|---|---|
| **User outcome** | *"The system still works after dark, and where it doesn't, it tells me — instead of quietly detecting nothing all night."* |
| **Functional requirement** | FR-8/FR-10 (night eligibility measured separately from day), FR-26 (night-scoped rules), FR-13 (night-specific degradation reporting), FR-49 (night nuisance rate reported separately) |
| **Operating constraints** | **(a) The night inversion — the central risk of the whole programme until measured.** Visible-light detection scores mAP@0.5:0.95 of **0.430** against **0.651** for infrared on the *same* night scenes — a **33.9% relative drop** — while infiltration and smuggling are believed to concentrate in darkness. **(b)** "Night-time movement detection" is **not a distinct product feature anywhere in the market**; it is an operating condition every other feature either survives or does not. Vendors sell it as sensor quality or as a thermal camera, never as an analytic. **(c)** Thermal analytics *is* solved — but only by buying thermal cameras with the analytics inside; and **what proportion of any border estate is thermal is UNKNOWN**. **(d)** Thermal is **not weather-immune**: fog and rain attenuate infrared by droplet scattering. **(e)** IR-illuminated video is effectively **monochrome** — colour-dependent mechanisms fail. **(f)** IR illuminators create their own nuisance sources: hotspot glare, lit insects and dust, retroreflection from vegetation and signage |
| **Acceptance criteria** | **AC-7.1** The Camera Spec Sheet carries a **separate night verdict** per analytic, measured after dark, not inferred from the day verdict. **AC-7.2** Rules can be scoped to night, and are automatically disabled on cameras whose night verdict is `Not eligible`, with the reason shown. **AC-7.3** Nuisance rate and cause histogram are reported **separately for night**. **AC-7.4** Night degradation is stated numerically for the deployment's own footage — the product publishes **its measured** day-vs-night gap, not a literature figure. **AC-7.5** The product never reports "quiet night" from a camera that was not night-eligible |
| **MVP priority** | **P0.** Named by the statement; carries the highest operational weight and the worst technical outlook; and the disclosure requirement (AC-7.5) is cheap and is the honest minimum |

**DECISION D-12 (accepted)** — **Night-time Movement Detection is an explicit
product capability**, implemented as a first-class, separately-measured operating
mode across the existing detection primitives, rather than as a separate "night AI
model." Concretely, it is delivered through: **(a)** night-specific camera
eligibility on the Camera Spec Sheet, measured after dark and reported independently
of the day verdict; **(b)** the same person and vehicle movement-detection
primitives (CAP-1, CAP-2) run against night-eligible cameras; **(c)** night-scoped
rules — time-of-day gating on zones, lines, direction and dwell; and **(d)**
measured, disclosed limitations — the night-vs-day performance gap and cause
histogram, published per camera. **IBVAP does not ship a separate model or product
surface named "night analytic"** — night is a condition the existing primitives are
measured and gated against, not a distinct detector requiring its own architecture.
*Rationale:* the market's framing (night is a condition, not a feature) is correct
and evidenced; the gap is that nobody *measures and discloses* the condition, and
the statement names the capability explicitly, so it must be represented in the
product as a real, named capability rather than only as an internal engineering
property. Thermal support is post-MVP and gated on OQ-12 (what fraction of the
estate is thermal).

---

### CAP-8 — Real-time alert generation and event logging

**Grade: Primary-candidate (the mechanism is fully in IBVAP's control). MVP priority: P0.**

| Aspect | Definition |
|---|---|
| **User outcome** | *"Something worth my attention reaches me quickly with enough to judge it; and everything the system saw is written down somewhere I can search and hand over."* |
| **Functional requirement** | FR-27 through FR-39 in full |
| **Operating constraints** | **(a)** **What an alert carries is a bandwidth decision worth a factor of ~300** — the ordering event → crop → clip-on-demand is arithmetic. **(b)** A per-frame metadata firehose is *not* cheap: 13–30 kbps per camera is comparable to an entire published per-camera cloud budget, and eight cameras of it saturates a 128 kbps link. **(c)** Event logging's presence *as a requirement* in the statement indicates it is currently absent or inadequate; and **[SIH/SSB]** every verified force reporting instrument is outcome-shaped — **a detection that produces no seizure has no existing home**. **(d) [MARKET:IN]** The log is also the evidence: s.63 BSA requires a hash and two signatures, and **transcoding changes the hash**. **(e)** **Time integrity is unestablished at target sites** and a silent wrong clock is the worst version of the evidential risk |
| **Acceptance criteria** | **AC-8.1** Every rule firing produces exactly one Event in an append-only hash-chained local log, with no link and no operator present. **AC-8.2** The log survives unclean power loss with the chain intact. **AC-8.3** Alerts are delivered payload-progressively and the product states the expected wait for a clip before it is requested. **AC-8.4** Events queue during disconnection ≥72 h and reconcile idempotently, with a declared discard policy if the queue fills. **AC-8.5** Every Event carries a time-integrity status; Events created under a suspect clock are marked. **AC-8.6** An evidence pack opens and verifies **on a machine with no IBVAP installed**. **AC-8.7** The event store is queryable locally by time, camera, zone, class, rule, assessment and outcome |
| **MVP priority** | **P0.** This is the product's spine — every other capability writes into it |

---

### 9.1 Capability × MVP summary

| # | Capability (statement wording) | Grade | MVP | Where the limitation is stated |
|---|---|---|---|---|
| 1 | Human detection and tracking | Support | **P0** (single-camera) | CAP-1 (c),(e) |
| 2 | Vehicle detection and classification | Support | **P0** (coarse class) | CAP-2 (a),(c) |
| 3 | Face detection | Support, Conditional | **P1** | CAP-3a (b),(d) |
| — | *Face recognition (Expected Solution)* | Gated, watchlist-only | **P1, gated** | CAP-3b (a)–(g), D-7 |
| 4 | ANPR | Conditional (lane-aimed) | **P1** where eligible | CAP-4 (a)–(g), NG-4 |
| 5 | Virtual fence intrusion detection | Support | **P0** | CAP-5 (a)–(e), D-10 |
| 6 | Suspicious activity detection | Support, rules only | **P1** | CAP-6 (a)–(f), D-11 |
| 7 | Night-time movement detection | Support, mode | **P0** | CAP-7 (a)–(f), D-12 |
| 8 | Real-time alerts and event logging | Primary-candidate | **P0** | CAP-8 (a)–(e) |

**Every row of the statement's capability list is present. Not one is dropped.**

---

## 10. MVP scope

### 10.1 The MVP thesis

**DECISION D-13 (accepted)** — **The MVP is one site, complete.** The smallest
coherent product is a **single deployment site with its existing cameras, running
the full loop** — ingest → spec sheet → primitives → rules → event → alert →
assessment → case → export → egress — end to end. The MVP boundary is: **(a)** one
deployment site; **(b)** complete end-to-end operation across that loop; **(c)**
local, site-level operation must work independently of any remote layer; **(d)**
remote monitoring and/or command-and-control integration may be supported where
present, but core operation does not require it; **(e)** the MVP does not assume a
specific, undocumented SSB CCTV or control-room workflow; **(f)** core operation
does not require a remote control room.
*Rationale:* this is the smallest unit that demonstrates the *complete operational
value* of IBVAP end-to-end while satisfying the SIH direction, and it is the unit
the estate actually consists of (734 posts, 42% unroaded). The exact SSB monitoring
workflow is unresolved (H-1); drawing the MVP boundary this way means it neither
assumes a control room exists nor asserts that one does not.

### 10.2 What is in the MVP

**The complete loop, at one site:**

| Block | Contents | Requirements |
|---|---|---|
| **1. Ingest** | RTSP/ONVIF from IP cameras and from channels behind an existing DVR/NVR; read-only; tested-device record; estate-safety verified first | FR-1 … FR-7, NFR-9 |
| **2. Camera Spec Sheet** | Measured stream properties, px/m at marked reference distances, per-analytic eligibility with plain-language reasons, refusal + logged override, re-issue on change, silent-degradation reporting | FR-8 … FR-13 |
| **3. Primitives** | Person detection; vehicle detection + coarse class; single-camera tracking; face **detection**; ANPR on eligible lane-aimed cameras; analysis-rate floor enforcement | FR-14 … FR-19 |
| **4. Rules** | Object-class-gated zones / lines / directions / dwell; composite operator-authored rules; starter library marked unvalidated; time-of-day and night scoping; open-border attention-zone framing | FR-23 … FR-26, AC-5.5 |
| **5. Events and alerts** | Event/Alert separation; payload-progressive delivery; one-action assessment; visible reversible suppression; configurable destinations that assume none exists | FR-27 … FR-31 |
| **6. Log and evidence** | Append-only hash-chained local log; hash at capture; no silent transcode; time-integrity status; evidence export pack openable without IBVAP; custody log; per-class retention; local query | FR-32 … FR-39 |
| **7. Site resilience** | Site-local analysis; ≥72 h disconnected operation; idempotent store-and-forward with a declared discard policy; no licence-server dependency; plain-language health; unclean-power survival; commissioning without integrator or survey | FR-40 … FR-48 |
| **8. Measurement** | Per-camera per-rule alert and nuisance rate with cause histogram; outcome attribution on every Case; exportable plain dataset | FR-49 … FR-51 |
| **9. Egress** | Published versioned event schema; generic outbound with retry/backoff/idempotency; local read API | FR-53 … FR-55 |
| **10. Authority and audit** | Authentication; full audit trail; authority-record mechanism for legally-gated capabilities; no internet dependency; isolated-network deployable | FR-59 … FR-61 |

### 10.3 Why each block is *in* the MVP — the coherence argument

The MVP is not a feature list; it is one argument. Remove any block and the argument
fails:

- Without **Spec Sheet**, every claim the product makes is the market's claim, and D-1
  is gone.
- Without **primitives**, there is nothing to gate rules on and rules regress to
  pixel motion — which is what the estate already has.
- Without **rules**, there is no capability 5, 6 or 7.
- Without **event/alert separation**, the product designs for a role (detection =
  incident) that the domain research says does not exist.
- Without **measurement**, G2 is unfalsifiable and the product is indistinguishable
  from a vendor claim.
- Without **evidence integrity**, the whole loop stops at "we detected something" and
  the case dies at the handover.
- Without **site resilience**, none of the above survives the actual site.
- Without **egress**, the statement's C2 requirement is unmet.

### 10.4 MVP validation estate

**DECISION D-14 (accepted)** — **The MVP is developed and validated against
the existing development CCTV rig in this repository** — five live channels behind a
real analog XVR with a **fixed 1080N anamorphic encode, a shared 12,288 kbps /
120 fps budget across 8 channels, TCP-only RTSP, and firmware that returns OK for
settings it discards.** This rig is **the existing development and validation
environment used to test IBVAP against real-world legacy CCTV/DVR constraints** —
it is not claimed to represent the SSB camera estate, which remains unmeasured
(OQ-2).
*Rationale:* a single measured recorder already falsified three convenient
assumptions (UDP viability, the "1080" resolution claim, and read-back-vs-trust
firmware behaviour), which is why development is validated against real hardware
constraints rather than specified ones. Per [CLAUDE.md](../../CLAUDE.md) rule 6, the
existing setup (`dvr.py`, `dvr.env`, `backups/`, `requirements.txt`) is **preserved,
not modified** — IBVAP consumes it, it does not replace it.

### 10.5 MVP exit gates — what must be true before MVP is called done

| Gate | Condition |
|---|---|
| **Gate 1 — Safety** | NFR-9 passes: concurrent IBVAP ingest does **not** degrade the existing recorder's own recording or live-view path. **This gate precedes every other activity on a live estate** |
| **Gate 2 — Honesty** | Every camera in the demonstration estate has a Spec Sheet, and at least one analytic is **refused** on at least one camera with a plain-language reason — because the estate genuinely cannot support it |
| **Gate 3 — Measured nuisance** | A ≥7-day unattended run has produced a per-camera nuisance rate and cause histogram, **and the number is published in the product surface** whatever it is |
| **Gate 4 — Night** | The same measurement exists separately for night, with the product's own measured day-vs-night gap |
| **Gate 5 — Disconnection** | A ≥72 h link-down soak: analysis continued, events reconciled without duplication or loss, no licence expiry, clock status honest |
| **Gate 6 — Evidence** | An export pack from the rig opens and verifies on a clean machine with no IBVAP present, and its hash matches the capture-time hash |
| **Gate 7 — Compliance** | Every row of [§9.1](#91-capability--mvp-summary) is demonstrable at its declared grade, and every limitation listed is visible in the product surface |

---

## 11. Post-MVP scope

Ordered by the condition that unblocks each, not by appeal.

### 11.1 Unblocked by an answer from the force

| # | Item | Unblocked by |
|---|---|---|
| **PM-1** | **Enabling face recognition for a live SSB deployment specifically.** The recognition capability itself ships in MVP and is demonstrable in a controlled development/test environment (FR-20, CAP-3b, D-7); what remains technically blocked for a real deployment is satisfying all four gating conditions — a recorded legal basis, the authority record, the authorized bounded gallery, and retention/oversight requirements — **none of which is evidence that the others are satisfied** | OQ-7 (legal basis, authority, retention, oversight for SSB specifically) **and** configuring the authorized gallery for that deployment |
| **PM-2** | **Reference C2 adapter** for a named system | OQ-5 (what the C2 actually is) |
| **PM-3** | **Multi-site aggregation to a higher echelon** (FR-58) | OQ-1 (does live monitoring exist, at which echelon) + OQ-5 |
| **PM-4** | **Control-room surface** — multi-camera wall, operator hierarchy, shift handover | OQ-1 resolving to "yes, staffed" |
| **PM-5** | **Pattern-over-time / route-usage analytics** for intelligence use (J5, U5) | OQ-7 — on a treaty-open border, **retaining records of lawful crossings may not be permissible at all. This is a legality question before it is a product question** |
| **PM-6** | **Validated "suspicious activity" rule set** replacing the unvalidated starter library | OQ-4 — the force's own definition, stated as observable behaviour |
| **PM-7** | **ICP / check-post deployment profile** (lane-aimed ANPR + face detection at scale) | OQ-11 (who owns and operates ICP CCTV, and whether the force has access) |

### 11.2 Unblocked by measurement or engineering

| # | Item | Unblocked by |
|---|---|---|
| **PM-8** | **Thermal stream analytics** | OQ-12 (what fraction of the estate is thermal) — and note thermal is not weather-immune |
| **PM-9** | **Standards-based egress**: ONVIF Profile M over MQTT (FR-56); MISB ST 0903 VMTI in STANAG 4609 (FR-57) | An interoperability spike; both already exist and no surveyed vendor emits either |
| **PM-10** | **Energy reporting** per site configuration (FR-52) | Instrumented measurement; zero vendors publish watts |
| **PM-11** | **Non-standard operational classes** — loaded porter, cart, driven livestock, timber load (FR-22) | Training data. **This is the single item that most determines whether IBVAP can address J4 at all** |
| **PM-12** | **Cross-camera tracking / re-identification** (FR-21) | Feasibility currently Low; needs geometry or overlap the estate does not provide |
| **PM-13** | **Mobile / handheld alert client** | OQ-8 (connectivity) determining whether it is usable at all |
| **PM-14** | **Body-worn camera ingest** | OQ-13 (retention and central handling of BWC footage) |
| **PM-15** | **UAV/drone video ingest** | Nothing in the research establishes a *job* for analysing it; the statement does not name it |
| **PM-16** | **PTZ control / slew-to-cue** | Stable-background analytics are invalid while a PTZ moves; this is an interaction to design after the primitives are trusted |
| **PM-17** | **Compressed-domain pre-filtering** as a power/bandwidth lever | An experiment on real border-type footage |

---

## 12. Explicit non-goals

**A non-goal is a commitment, not an omission.** Each is stated with the evidence
that makes it a decision rather than a deferral.

| # | Non-goal | Why |
|---|---|---|
| **NG-1** | **IBVAP will not replace or become the VMS/recorder.** It does not own recording, does not take over live view, does not require the estate's recording layer to change | Outside the statement's scope; multiplies the deployment burden at exactly the sites that cannot absorb it; and puts the product in direct competition with the incumbents' strongest ground |
| **NG-2** | **No learned anomaly model presented as "suspicious activity"** in MVP | 94.55% → 16.35% AUC on reversed same-scene labels; FAR +42% on hard-normal sets, some >70%; annotator agreement only κ 0.51–0.68; AUC insensitive to detection timing. Three independent, measured failures |
| **NG-3** | **No open-set face identification of the border population** | Legally unresolved on a treaty-open border; prohibited by default for law enforcement in publicly accessible spaces under EU AI Act Art. 5 [MARKET:EU]; and NIST's own precondition — improve image collection — is exactly what this deployment model forbids |
| **NG-4** | **No ANPR on wide-area border-road cameras** | A plate at that range and angle is far below the required pixel density. Physics, not effort |
| **NG-5** | **No full video egress to a central site** | Arithmetic at these link speeds; the whole market has already converged away from it |
| **NG-6** | **No cloud-dependent SaaS as the primary deployment mode** | Contradicts the connectivity and power evidence outright; and data classification / network policy for border video is entirely unestablished (OQ-10) |
| **NG-7** | **No competing on published detection-accuracy benchmarks** | Benchmarks in this market are unpublished, paywalled or scene-overfitted; IBVAP publishes **its own measured** numbers on **its own** footage instead |
| **NG-8** | **No claim of universal camera support.** "Works with any ONVIF camera" is not asserted | Two of the best-resourced engineering organisations in this market both built per-model compatibility labs and still warn buyers. A claim of universal support is a claim about intent |
| **NG-9** | **No dispatch, tasking, resource management or response coordination.** IBVAP produces notice and evidence; it does not command | Whether a QRT construct exists is **UNKNOWN** (H-4); what carries an alert to a responder is **UNKNOWN** (H-3). Building a dispatch model on those unknowns would be inventing a workflow |
| **NG-10** | **No drone / counter-UAS detection** | Not named in the problem statement; not a documented event class on the validation borders; fixed ground CCTV is geometrically poorly positioned for it |
| **NG-11** | **No tunnel detection** | Out of reach of surface video analytics; not a documented event class on the validation borders |
| **NG-12** | **IBVAP does not detect trafficking, contraband, currency or narcotics.** It detects **people, vehicles, faces, plates, movement and time** — and it will say so plainly | **A camera cannot see contraband inside a sack.** Trafficking's signal is *relational and behavioural at a lawful crossing*: a trafficked minor moving through a check post with an adult produces no intrusion, no unusual vehicle and no suspicious motion. **This is the honest limit of the whole product against the force's actual ledger (J4, J6), and stating it is a requirement** |
| **NG-13** | **No biometric processing of any kind without a recorded legal authority** | PR11: legality gates biometrics, not capability |
| **NG-14** | **No retention of records of lawful crossings** until OQ-7 resolves | Treaty-protected movement; DPDP applicability unresolved |
| **NG-15** | **No silent suppression, no silent degradation, no silent transcode, no silent clock** | Each is a documented failure mode; together they are the honesty invariant (NFR-16) |
| **NG-16** | **No cross-border data sharing** (e.g. with a counterpart force) | OQ-14 — no legal basis established. Note a government-level agreement to *"strengthen real-time information sharing"* exists, which makes this a **question**, not a capability |
| **NG-17** | **No pricing model in this PRD** | The floor competitor in this market is **free** open source. "Cheaper" is currently an untestable claim (OQ-15) |
| **NG-18** | **IBVAP does not assert admissibility of evidence** | It produces what s.63 BSA asks for and records who signed. Admissibility is a court's finding, not a product's claim |

---

## 13. Success metrics

Metrics are grouped by what they test. **Where the research provides no baseline,
the metric is stated as "measure and publish", not as a number — inventing a target
before X1/X2 have run would be fiction (NFR-4).**

### 13.1 Product-value metrics

| # | Metric | Definition | Target | Tests |
|---|---|---|---|---|
| **SM-1** | **Alert precision, assessed** | Alerts assessed `real` ÷ all assessed alerts, per camera per rule | **Measure and publish.** Improvement over successive runs is the goal; the 90% false-alarm precedent is the thing to beat, not a target to adopt | G2, T2 |
| **SM-2** | **Nuisance rate and cause histogram** | Alerts per camera per 24 h assessed `not real`, broken down by cause | **Measure and publish**, day and night separately | G2, O3 |
| **SM-3** | **Time to first assessable evidence** | Rule-satisfying frame → human sees event + crop | ≤30 s on a 128 kbps link (NFR-2) | G3, J2 |
| **SM-4** | **Assessment completion rate** | Alerts receiving a human assessment ÷ alerts delivered | **Measure.** A falling rate is the early warning that the system is being ignored — the worse-than-nothing failure | G3, T2 |
| **SM-5** | **Spec Sheet coverage and refusal rate** | % cameras with a current Spec Sheet; % analytic-camera pairs refused | 100% coverage. **Refusals are a success signal, not a defect count** | G4, D-1 |
| **SM-6** | **Events from unmodified estate** | Events produced from cameras with **zero** hardware change | 100% of MVP events | G1, statement outcome 1 |

### 13.2 Deployability metrics

| # | Metric | Definition | Target | Tests |
|---|---|---|---|---|
| **SM-7** | **Commissioning time** | Non-specialist, two cameras, no site survey, no integrator | ≤1 h (NFR-10) | G5, O9 |
| **SM-8** | **Outcome attribution coverage** | % Cases carrying a recorded outcome; % of the force's own recorded outcomes traceable to an Event | **Measure.** The GAO failure (assists recorded from a sector with no such assets) is the anti-pattern: **the dataset must be independently auditable** (FR-51) | G8, J10, V7 |
| **SM-9** | **Disconnection survival** | Hours of link-down with full local function and clean reconciliation | ≥72 h, zero duplicates, zero losses (NFR-6) | G5, O2 |
| **SM-10** | **Site energy draw** | Measured watts of the analytics workload per site configuration | **Measure and publish** — zero vendors do | G5, O4 |
| **SM-11** | **Evidence pack validity** | % export packs that open and verify on a clean machine with the capture-time hash intact | 100% (NFR-15) | G6, J7 |
| **SM-12** | **Egress consumability** | An independent consumer ingests the published schema without bespoke help | ≥1 independent consumer | G7, D-5 |

### 13.3 Compliance metric

| # | Metric | Definition | Target |
|---|---|---|---|
| **SM-13** | **Statement capability coverage** | Every capability in [§9.1](#91-capability--mvp-summary) demonstrable at its declared grade, with its limitations visible in the product surface | **8 of 8**, plus face recognition demonstrable as a gated mechanism |

### 13.4 Anti-metrics — things we will not optimise

- **Number of alerts.** More alerts is not more value; T2 says the opposite.
- **Number of supported analytics per camera.** Spec Sheet refusals are correct.
- **Headline accuracy percentages.** NG-7.
- **Cameras supported on paper.** NG-8; only the tested-device record counts.

---

## 14. Constraints

Constraints are things IBVAP must live within. They are not risks (which may or may
not occur) and not decisions (which we chose).

### 14.1 Constraints imposed by the problem statement (immutable)

| # | Constraint |
|---|---|
| **C-1** | Must ingest live video streams from **standard IP-based CCTV cameras** (existing infrastructure) |
| **C-2** | Must **not** require dedicated FRS, ANPR, or smart-camera hardware |
| **C-3** | Must use AI, ML, CV and video analytics techniques |
| **C-4** | Must support integration with existing command and control systems |
| **C-5** | Must be cost-effective, scalable, and suitable for deployment across remote border locations and strategic installations |

### 14.2 Physical constraints — software cannot remove these [GLOBAL]

Carried verbatim in substance from
[technical-feasibility.md](../01-research/technology/technical-feasibility.md) §9.
**Each becomes a product constraint because it bounds what may be claimed.**

| # | Constraint | Product consequence |
|---|---|---|
| **C-6** | **Pixels on target.** Detection ~25 px/m; identification 250 px/m (2015) / reported 500 px/m (2025). Interpolation manufactures no information | Spec Sheet eligibility (FR-9, FR-10); NG-3, NG-4 |
| **C-7** | **Field of view and mounting.** A face that enters frame only as the top of a head cannot be recognised. NIST: improvement requires positioning, mounting, lighting, optics — all hardware | CAP-3a (b), CAP-3b (a) |
| **C-8** | **Photons at night.** 33.9% relative detection drop, visible vs infrared, same scenes. Enhancement trades noise for blur; it adds no photons | CAP-7; separate night verdict |
| **C-9** | **Atmospheric attenuation.** Rain, fog, storms degrade line-of-sight — **and thermal is not exempt** | Weather-conditional eligibility; honest degradation reporting |
| **C-10** | **Motion blur.** Set by exposure and target velocity; it is why software ANPR is speed-limited | CAP-4 speed envelope |
| **C-11** | **Viewing angle.** Software LPR requires ≤30° look-down; some camera geometries (panoramic, fisheye, 360, PTZ) are excluded outright | CAP-4 angle envelope |
| **C-12** | **Temporal sampling.** Identity association collapses below ~2–3 analysed fps | NFR-5; FR-19 floor |
| **C-13** | **Codec information loss.** An upscaled 1080N frame contains the information of 960×1080; artefacts are indistinguishable from content downstream | FR-5 effective resolution |
| **C-14** | **The recorder's shared budget.** Where a DVR/XVR fronts cameras, total bitrate and frame rate are fixed and shared. No downstream software raises it | FR-2, FR-4; site sizing |
| **C-15** | **Occlusion.** The dominant tracking failure mode | CAP-1 (c) |
| **C-16** | **The link.** 128 kbps carries 128 kilobits per second | FR-28, FR-40, NFR-7 |
| **C-17** | **Energy.** Inference costs joules, and at a fuel-limited site that is a logistics fact | NFR-8 |

### 14.3 Estate constraints — properties of the cameras we inherit [BORDER]

**C-18** Cameras specified for Detection/Observation density, not Identification.
**C-19** Anamorphic "1080N"-style encoding advertising a resolution it does not deliver.
**C-20** Wide-angle overview mounting that maximises coverage and minimises px/m.
**C-21** No true day/night sensor or IR illuminator on some cameras.
**C-22** IR illumination is monochrome — colour ceases to be a feature at night.
**C-23** Fixed cameras with no overlap — no geometric constraint for cross-camera work.
**C-24** PTZ on preset tour — stable-background analytics invalid while moving.
**C-25** Unknown/undocumented ONVIF conformance and firmware; compatibility is per-model.
**C-26** Lens condition — dirt, webs, condensation, IR hotspot — degrades silently.
**C-27** Clock drift on camera or recorder breaks correlation and evidential timestamps.

### 14.4 Deployment constraints [SIH/SSB] → [BORDER]

**C-28** **42% of BOPs (308 of 734) lack road connectivity.** Hardware, spares, fuel
and technicians all arrive on foot.
**C-29** **Power is generator- or solar-based at many sites**, scheduled and
fuel-limited; a parliamentary committee noted lack of electricity at SSB and ITBP
BOPs specifically.
**C-30** **Connectivity is unestablished and may be satellite** — high-latency,
low-bandwidth, metered. **No CIBMS-equivalent backbone exists on these borders.**
**C-31** **No IT, cyber, video or electronics cadre exists in the force.** The
nearest is the Communication (wireless/telecom) cadre.
**C-32** **The echelon nearest the camera is commanded at Sub-Inspector level or
equivalent**, and BOP/Company decision latency is already a named problem.
**C-33** **Software at such a site must run unattended for long periods and fail in a
way a non-specialist can recognise and report over a radio or satellite phone.**

### 14.5 Legal and regulatory constraints

**C-34 [MARKET:IN]** **s.63 BSA 2023** (in force 1 July 2024): admissibility of an
electronic record copy requires a certificate signed by the device custodian **and**
an expert, disclosing the **hash value**.
**C-35 [MARKET:IN]** Cases are **handed to the local police** for investigation and
prosecution; the receiving agency is documented as under-resourced for these cases.
**C-36 [SIH/SSB]** The force's jurisdictional belt is **15 km** under its own Act —
not another force's 50/80 km.
**C-37 [SIH/SSB]** The border population includes nationals exercising a **treaty
right of movement**; biometric processing of them has no established legal basis.
**C-38 [MARKET:EU]** Real-time remote biometric identification in publicly accessible
spaces for law enforcement is **prohibited by default** under EU AI Act Art. 5.
**C-39 [MARKET:IN]** ER-01/STQC bars sale of non-conforming cameras from 1 April
2026 — **the installed base will churn**, so the tested-device record is a moving
target.
**C-40 [MARKET:US]** NDAA §889 excludes named vendors from US federal procurement —
relevant to any hardware recommendation, which this PRD does not make.
**C-41** **Data classification, security accreditation and network policy for a
platform handling live border video are unestablished** (OQ-10) — therefore assume
the most restrictive: no internet, isolated network deployable (FR-61).

### 14.6 Project constraints

**C-42** Development order is fixed: Research → Product → Design → Architecture →
Engineering → Testing → Demo. No stage may be skipped
([CLAUDE.md](../../CLAUDE.md) §2).
**C-43** No product feature may exist that does not trace to the problem statement
(rule 2). Every requirement in [§7](#7-functional-requirements) traces.
**C-44** The existing CCTV access/testing setup (`dvr.py`, `dvr.env`, `backups/`,
`requirements.txt`) is **preserved unmodified** (rule 6).
**C-45** SIH 2026 is a fixed-date evaluation with a demonstration expectation —
[§10.5](#105-mvp-exit-gates--what-must-be-true-before-mvp-is-called-done) gates are
also the demo's substance.

---

## 15. Assumptions

Every assumption states what would falsify it. **None is a fact and none may be
quoted as one.** Assumptions carried from
[product-discovery.md](../01-research/users/product-discovery.md) §7 keep their
original IDs where one exists.

| # | Assumption | Basis | Falsified by |
|---|---|---|---|
| **A1** | SSB is the department for PS 26187 | Project owner's statement; the SIH organisation field is **not recorded** in `docs/00-project/` | Recording the actual SIH department field (OQ-16) |
| **A2** | The force has *some* camera estate at *some* nodes on these borders | Procurement of a CCTV setup with FRS/ANPR is a stated fact of record; MHA lists CCTV among ICP facilities | A site survey finding no cameras at candidate nodes |
| **A3** | Existing cameras were specified for Detection/Observation density (25–62 px/m), not Identification | DORI + the fact that existing CCTV was installed for live viewing | A measured site survey (OQ-2) |
| **A4** | Uplinks are of the order of hundreds of kbps, intermittent, or satellite | Satellite phones in the surveillance inventory; peer-reviewed constrained-edge findings | OQ-8 |
| **A5** | Continuous compute at a generator-powered, unroaded site is a **fuel-logistics** cost, not just an electrical one | Road + generator findings combined | OQ-9 |
| **A6** | Event logging today is manual or register-based; retrieval is timeline-scrubbing | Inference from the statement's framing; no detection-shaped force instrument identified | Any digital incident register linked to video |
| **A7** | A camera-derived detection that yields no seizure has no home in existing systems | Every verified force reporting instrument is outcome-shaped | Any force instrument that counts detections, alarms or sightings |
| **A8** | On this border, cattle, porters and forest produce are **targets**, not nuisance alarms — the signal/noise split differs in kind from a fenced border | The force's own seizure categories | A measured nuisance profile on this border (OQ-17) |
| **A9** | Trafficking detection is the event class least served by the named analytics | Explicitly unsourced in the research | Direct enquiry with AHTU staff (U6) |
| **A10** | A product optimised for the procurement document and not for the post will be bought and not used | Documented RFP and vendor-oversight weaknesses | Evidence that field units drive requirements |
| **A11** | "Scalable" means many small isolated sites, not one large central cluster | The statement's own phrase, "across remote border locations" | Direct clarification |
| **A12** | Per-camera pricing, universal in the market, is a poor fit for a many-small-sites estate | Market pricing survey + estate shape | Real pricing data (OQ-15) |
| **A13** | An untrusted alerting system is worse than none — it consumes attention and supplies false assurance | Inference from the operator-reliance finding | An operator study on this estate |
| **A14** | IR-illuminated night video is effectively monochrome, so every colour-dependent mechanism degrades at night | Physics of IR illumination; not stated in a retrieved source | Directly testable on the rig |
| **A15** | The MVP's four artefacts (Event / Alert / Case / Spec Sheet) are expressive enough for whatever workflow H-1 turns out to be | D-4's reasoning; untested against a real workflow | The force describing a workflow the artefacts cannot represent |
| **A16** | A published, versioned event schema is a *sufficient* answer to "integration with existing command and control systems" for evaluation purposes | D-5; ingest has standardised, egress has not | An evaluator or the force requiring a working adapter to a named system |
| **A17** | Refusing an analytic on an ineligible camera will be read as integrity, not as a defect | Opportunity O1's own counter-evidence says the opposite is possible | Buyer or evaluator feedback treating refusals as missing capability |

---

## 16. Risks

Ordered by expected impact × likelihood. Each names its mitigation **direction** —
not its implementation, which belongs to later stages.

| # | Risk | Evidence | Mitigation direction |
|---|---|---|---|
| **R1** | **We do not know how the user works.** The CCTV/control-room workflow is not publicly validated (H-1, H-2) — which is **not** the same as knowing it is absent. Any product built around a specific monitoring posture rests on an unvalidated workflow | Two exhaustive research passes; the research argues it is structurally unlikely to be resolved by desk research | **D-3 + D-4**: be correct under both answers; artefacts not roles; additive console layer. **Ask the force (OQ-1)** |
| **R2** | **The estate cannot physically support the named capabilities, and nobody has measured it.** If cameras deliver 25–62 px/m, face recognition and ANPR are unreachable at any software quality — and the statement requires them | DORI; estate unknown (OQ-2) | **The Camera Spec Sheet turns this risk into the product.** Measure before promising |
| **R3** | **Nuisance alarms make the system untrusted, which is worse than no system** | 90% SBInet precedent; all documented environmental triggers present; and here the usual "noise" categories are *targets* | Object-class gating; measured-and-published nuisance rate (FR-49); visible reversible suppression; **7-day unattended run before any claim** |
| **R4** | **The capability list and the operational reality point in different directions, and the pressure is to satisfy the list** | The ledger's infiltration category is 24 cases against 3,649 contraband and 1,026 narcotics cases; the statement's centrepiece is a virtual fence | **D-8 + D-10**: deliver all eight at declared grades **and** support the open-border framing. Decide deliberately, in writing, rather than by drift |
| **R5** | **Night is the operational peak and the technical trough**, and no vendor in the surveyed market sells "night-time movement detection" as a distinct feature | 33.9% relative drop; night not a market feature | **D-12**: Night-time Movement Detection ships as an explicit MVP capability, implemented as a separately-measured mode across the existing primitives with mandatory disclosure. **Measure on the rig after dark before claiming anything** |
| **R6** | **The uplink cannot carry what the design assumes** | Constrained-edge findings; satellite in the inventory; OQ-8 unanswered | Payload-progressive alerts; site-local analysis; declared queue discard policy; publish own bandwidth consumption |
| **R7** | **Power and physical maintenance at unroaded sites exceed the software's value** | 42% unroaded; fuel-limited generators; no on-site cadre | Measure and publish watts (SM-10); commissioning without integrator (NFR-10); **no appliance obligation the site cannot absorb** |
| **R8** | **Evidence produced is inadmissible or unusable** — clocks, hashes, transcode | s.63 BSA; transcoding changes the hash; **time integrity at a disconnected site is entirely unestablished**. *A silent wrong clock is the worst version of this risk* | Hash at capture; no silent transcode; **explicit time-integrity status on every Event**; export verifiable without IBVAP |
| **R9** | **Integration has no defined target** — building an adapter for a system that may not exist, or missing one that does | H-6; SIMS eliminated and nothing replaced it | **D-5**: published contract now, standards-based egress next, adapter only when named |
| **R10** | **Legal exposure from biometrics on a treaty-open border** | No established legal basis; DPDP applicability unresolved; EU prohibition by default | **D-7 + NG-13**: recognition ships in MVP and is demonstrable in a controlled development/test environment; against a real deployment it is technically blocked unless a recorded legal basis, the authority record, the authorized gallery and retention/oversight are all configured and current — **the authority record alone is never treated as evidence the legal basis exists**. Population-scale/open-set use remains excluded regardless of OQ-7 (NG-3), and this document does not claim a legal basis has been established for the SSB estate (PM-1) |
| **R11** | **Per-model compatibility work is unbounded and consumes the team** | Two of the best-resourced vendors both built compatibility labs and still warn buyers; one rig produced three surprises | Tested-device record as a **product artefact** (FR-6); scope compatibility as an operating cost, not a phase |
| **R12** | **The force's real event classes are not video-detectable at all** — a camera cannot see contraband inside a sack | J4 vs the ledger; PM-11 is the only lever and it is data-gated | **NG-12**: say it plainly. Do not let the demo imply otherwise |
| **R13** | **The department attribution is wrong** (A1) | The SIH organisation field is not recorded | **OQ-16 costs minutes.** Close it first |
| **R14** | **The already-procured FRS/ANPR stack makes IBVAP a duplicate at some nodes** | The procurement is a stated fact of record; its deployment is unknown | **OQ-6**: determine whether IBVAP complements, replaces or duplicates. Complementing (metadata + evidence + resilience around an existing stack) is a live option |
| **R15** | **Refusal-as-a-feature backfires commercially** (A17) | O1's own counter-evidence: vendors have a commercial incentive not to disclose | Frame refusals as *scoped* capability with a stated remedy ("this camera can do X; for Y it would need to be re-aimed") rather than as absence |

---

## 17. Open questions

**Rule enforced here, carried from
[ssb-operational-workflow.md](../01-research/domain/ssb-operational-workflow.md)
§9:** every item the research marked "must remain UNKNOWN" appears below as an
explicit open question. **None is silently resolved by assumption anywhere in this
document.**

### 17.1 Blocking — the PRD's honesty depends on these

| # | Question | Research ID | What it changes |
|---|---|---|---|
| **OQ-1** | **Does the force monitor live video at all, and at which echelon?** Operators, cameras per operator, shift pattern, instructions on seeing something | H-1 / SQ-3 / B2 | Whether PM-3/PM-4 are the next thing built, or never built. **D-3 exists solely to survive this being unanswered** |
| **OQ-2** | **What is the installed camera base?** Count and location by node type, make, model, resolution, codec, PTZ vs fixed, thermal vs visible, ONVIF conformance, age — and native IP vs analog behind a DVR with a shared encoder budget | H-5 / SQ-1 / B3 | Which rows of [§9.1](#91-capability--mvp-summary) have any eligible camera at all |
| **OQ-3** | **What is the actual detection → assessment → escalation → response sequence, and is there a written SOP or Standing Order?** | H-2, H-7 / SQ-4 | Whether [§5](#5-core-user-workflows)'s PRODUCT MODEL survives contact |
| **OQ-4** | **What does "suspicious activity" mean, stated as observable behaviour, on a border where crossing is lawful?** | H-13 / Q-3 / SQ-7 / B4 | CAP-6 entirely. **No experiment substitutes for this answer** |
| **OQ-5** | **What are the "existing command and control systems", by name, with interfaces?** SIMS is eliminated; nothing has replaced it | H-6 / SQ-6 / B5 | Whether D-5 is sufficient or PM-2 becomes MVP |
| **OQ-6** | **Where is the already-procured FRS/ANPR CCTV setup deployed, what is it, and does it expose streams or APIs?** | SQ-2 / B6 | Whether IBVAP complements, replaces or duplicates it (R14) |
| **OQ-7** | **What is the legal basis, authorisation level, retention rule and oversight for biometric processing of people exercising a treaty right of movement? Does DPDP 2023 apply?** | H-11 / SQ-8 / B7 | CAP-3b, PM-1, PM-5, NG-14 |

### 17.2 High priority — these shape scope

| # | Question | Research ID |
|---|---|---|
| **OQ-8** | What connectivity exists at a post — any IP link, bandwidth, symmetry, metering, reliability, how many on satellite? | H-12 / SQ-11 / H3 |
| **OQ-9** | What power is available for compute — generator hours, rating, fuel resupply interval, solar/battery — and what does an extra 15–60 W cost in logistics? What retention is required for video, clips and metadata separately? | H-12 / SQ-10 / SQ-13 |
| **OQ-10** | What security accreditation, data classification and network policy applies to a platform handling live border video? Is cloud or internet permissible at all? | Q-18 / H8 |
| **OQ-11** | Who owns and operates the CCTV at ICP Raxaul and Jogbani, and does the force have access? | H-10 / SQ-14 |
| **OQ-12** | What proportion of the estate is thermal, and do visible cameras have IR illuminators, true day/night sensors, or neither? | Q-15 / SQ-1 |
| **OQ-13** | Is there a **time source** at a disconnected site — NTP, GNSS, or nothing? | A-7 (new in the tech pass) — **blocks any evidential design** |
| **OQ-14** | Which stakeholders beyond the force would consume this video, and is there any legal basis for cross-border sharing given the government-level agreement to strengthen real-time information sharing? | SQ-23, SQ-W9 |
| **OQ-15** | Does the market's pricing even permit a "cost-effective" claim to be tested? | Competitors Q-1 |
| **OQ-16** | **Is the SIH department attribution actually SSB?** Record the organisation field for PS 26187 in `docs/00-project/` | SQ-30 / B1 — **costs minutes; close it first** |
| **OQ-17** | What is the real nuisance profile here, given that cattle, porters and forest produce are **targets** rather than nuisances? | SQ-18 / Q-6 |
| **OQ-18** | Is the Indo-Bhutan border operationally the same problem as the Indo-Nepal border, or a different one? | H-14 / SQ-25 |
| **OQ-19** | Is there a QRT construct, or is response by the patrol/naka already in the field? What carries the alert to them? | H-3, H-4 / SQ-12 |
| **OQ-20** | Is any event that produces **no seizure and no arrest** recorded anywhere today? | H-8 |

### 17.3 Answerable without the force — by experiment on the existing rig

| # | Question | Research ID | Gate |
|---|---|---|---|
| **OQ-21** | Does adding concurrent RTSP clients degrade the existing recorder's own recording? | E-12 / X4 | **Gate 1 — must pass before anything touches a live estate** |
| **OQ-22** | Measured nuisance-alarm rate and cause histogram of an object-gated virtual fence over 7 unattended days | E-5 / X1 | Gate 3 |
| **OQ-23** | Detection and tracking behaviour on IR-illuminated night footage from an ordinary camera | E-6 / X2 | Gate 4 |
| **OQ-24** | The analysis-rate floor on these scenes (25/10/5/3/1 fps) | E-7 / X3 | NFR-5 validation |
| **OQ-25** | Does the pipeline survive 72 h disconnection with idempotent reconciliation, licences intact, clocks in tolerance? | E-11 / X5 | Gate 5 |
| **OQ-26** | Energy per analysed frame, per configuration | E-10 / X6 | SM-10 |
| **OQ-27** | Can a 1080N anamorphic stream support **any** identity-grade analytic at any range? | E-8 | CAP-4 eligibility on the rig |
| **OQ-28** | Verify the 2025 pixel-density revision (250 → 500 px/m) against the standard itself, not a secondary source | C-1 | C-6 |

---

## 18. Acceptance criteria

Capability-level acceptance criteria are in [§9](#9-sih-required-capabilities)
(AC-1.1 … AC-8.7). This section defines **product-level** acceptance — the criteria
that decide whether IBVAP, as a whole, is what this PRD said it would be.

### 18.1 Product-level acceptance criteria

| # | Criterion | Verified by |
|---|---|---|
| **AC-P1** | **Estate safety.** Running IBVAP against a live estate does not degrade the existing recorder's recording or live-view path | OQ-21 measurement, before any live deployment |
| **AC-P2** | **Zero hardware change.** Every MVP capability is demonstrated on cameras with **no** hardware modification, replacement, re-aiming or added illumination | Deployment record; SM-6 |
| **AC-P3** | **Honesty invariant.** No user-facing surface states or implies a capability the Spec Sheet marks `Not eligible`; every refusal carries a plain-language measured reason; every override is logged and stamps its events | Adversarial UI review against NFR-16, plus an audit of every override path |
| **AC-P4** | **Complete loop at one site.** A single post demonstrates ingest → spec sheet → primitive → rule → event → alert → assessment → case → export → egress, end to end, unattended | End-to-end demonstration on the rig |
| **AC-P5** | **Works with nobody watching.** With no operator, no console open and no link, the system continues to analyse, log, alert locally and queue — and reconciles cleanly on reconnect | 72 h soak (OQ-25) |
| **AC-P6** | **Works with somebody watching.** The same artefacts route to a human at a console without changing the site's configuration or requiring a different deployment | Configuration demonstration; validates D-3/D-4 |
| **AC-P7** | **Measured, not claimed.** Every number IBVAP publishes about itself — nuisance rate, day/night gap, latency, bandwidth, watts, read rate — is measured on the deployment's own footage and dated | Metrics audit against [§13](#13-success-metrics) |
| **AC-P8** | **Evidence survives departure.** An export pack opens and verifies on a clean machine with no IBVAP present, hash matching the capture-time hash, custody log intact | Clean-machine verification |
| **AC-P9** | **Legibility.** Every failure state IBVAP can enter is expressible in one sentence a non-technical post commander can relay over a radio | Enumerate every failure state; review each sentence |
| **AC-P10** | **Non-technical commissioning.** A two-camera site is commissioned in ≤1 h by someone with no video-analytics training, without a site survey or certified integrator | Timed commissioning with a naive operator |
| **AC-P11** | **Full statement coverage.** All eight named capabilities are demonstrable at their declared grades; facial recognition is demonstrable as a **gated mechanism** with its authority record; every documented limitation is visible in the product | [§9.1](#91-capability--mvp-summary) walkthrough |
| **AC-P12** | **Traceability.** Every implemented feature traces to a requirement in [§7](#7-functional-requirements) or [§9](#9-sih-required-capabilities), and every such requirement traces to the problem statement or to a cited research finding | Requirements trace audit; enforces [CLAUDE.md](../../CLAUDE.md) rule 2 |
| **AC-P13** | **No silent anything.** No silent suppression, no silent degradation, no silent transcode, no silent clock, no silent discard. Each has a visible state and a record | Negative-path review against NG-15 |
| **AC-P14** | **Isolation.** The system deploys and runs fully with no internet access and no cloud service reachable | Isolated-network deployment |
| **AC-P15** | **Unknowns preserved.** Every open question in [§17](#17-open-questions) is either answered-and-recorded or still open — **none has been quietly closed by an implementation assumption** | Review of [§17](#17-open-questions) against what was built, at MVP exit |

### 18.2 What acceptance explicitly does **not** require

- A stated detection-accuracy percentage (NG-7, SM anti-metrics).
- A stated false-alarm target (NFR-4 — the requirement is measurement, not a number).
- Support for any specific camera make (NG-8 — only the tested-device record counts).
- A working adapter to a named C2 system (D-5, until OQ-5 answers).
- Face recognition operating against any general or open population — only bounded,
  explicitly authorized gallery matching is supported, and against a real
  deployment only where a recorded legal basis, the authority record, the
  authorized gallery and retention/oversight requirements are all configured and
  current. **The authority record alone does not satisfy this** (D-7, NG-3).
- Any claim that a detected event is an offence, an intrusion, or contraband
  (NG-12, NG-18).

---

## 19. Product decisions requiring human approval

**All fourteen below are accepted**, recorded with date and rationale in
[decisions.md](../00-project/decisions.md), per [CLAUDE.md](../../CLAUDE.md) §3.7.
The table records the rationale and risk considered at approval.

| # | Decision | Why it needs a human | Cost if wrong |
|---|---|---|---|
| **D-1** | Differentiate through **deployment, transparency, reliability and camera-aware operation**; pursue **sufficient accuracy per defined use case** rather than competing primarily on benchmark leadership | Sets the entire competitive posture and what the SIH pitch claims | We compete where incumbents are strongest and lose |
| **D-2** | **SSB is the validation context, not the product boundary**; requirements written force-agnostically | Interpretation of [CLAUDE.md](../../CLAUDE.md) §4 against SIH pressure to look India-specific | Generalisation costs focus; over-fitting costs the market |
| **D-3** | Function correctly **whether or not a remote monitoring/control-room layer is available**, or is temporarily unavailable; core operation never depends on one | Accepts building an additive console layer that may be unnecessary — or a post-first product that may be unwanted | Wasted scope in one direction; a mis-shaped product in the other |
| **D-4** | **Core workflows modelled around artefacts and their states** (Event / Alert / Case / Camera Spec Sheet), with role assignment and permissions configurable | This is the mechanism that makes a PRODUCT MODEL safe under an unresolved H-1 | If the artefacts cannot express the real workflow (A15), the model must be rebuilt |
| **D-5** | Satisfy C2 integration by a **published contract + generic egress, demonstrated against at least one real external integration path** (webhook / REST / MQTT); named C2 adapters remain post-MVP until a real target system is identified | An evaluator or the force may demand a working adapter (A16) | "Integration" is judged unmet at evaluation |
| **D-6** | **Refuse, don't degrade** — analytics blocked on ineligible cameras, override logged and stamped | Directly trades demo breadth for integrity; may read as missing capability (R15) | Perceived as a weaker product than one that claims everything |
| **D-7** | **Face detection ships unconditionally in MVP; controlled face recognition also ships in MVP and is demonstrable in a controlled development/test environment; against a real deployment it is technically blocked unless a recorded legal basis, the authority record, the authorized bounded gallery and retention/oversight are all configured and current — the authority record is never treated as proof the legal basis exists; all biometric operations are logged and auditable** | **The most contestable decision in this document.** The statement's Expected Solution names facial recognition support; we ship it as a demonstrable, gated capability rather than withholding it or claiming a legal basis this document has not established | The four-condition gate is only as strong as its enforcement — if it can be bypassed, misconfigured, or the legal-basis field populated without a genuinely sound basis, the underlying exposure is unchanged. *Counter:* the gate is technically enforced, the environment classification (dev/test vs. operational) is itself authority-controlled and audited, and every operation is logged |
| **D-8** | **All eight SIH capabilities explicitly addressed, with implementation maturity, operating conditions and limitations declared for each; none silently omitted** | The chosen construction for honouring the statement without over-claiming | If graded delivery reads as hedging, the compliance story weakens |
| **D-9** | IBVAP is **an intelligent video-analytics layer that can operate alongside existing surveillance/VMS infrastructure and integrate with external command/control systems** — a support layer, not a sole (primary) detection system, and not a replacement for the existing surveillance system | Determines alerting, staffing and liability posture; the research says decide deliberately | "Support layer" may be read as low ambition; declaring itself sole (primary) detection is not reversible after a miss |
| **D-10** | Virtual fence ships **in full**, plus an **open-border attention-zone framing** | Reconciles a statement requirement with a border where crossing is lawful | Doing only the fence satisfies the statement and not the user; doing only zones inverts that |
| **D-11** | "Suspicious activity" = **operator-authored composite rules**; **no learned anomaly model in MVP** | An evaluator may expect a learned model; the measured evidence says it does not transfer | Perceived as less "AI"; *counter:* three measured failure modes |
| **D-12** | **Night-time Movement Detection ships as an explicit product capability**, implemented via night-specific eligibility + existing movement primitives + night-scoped rules + measured limitations — not a separate night model | Makes capability 7 a visible, named product capability rather than only an internal property | If the underlying primitives underperform at night, the capability is named and visible, so its measured limitations must be prominent — otherwise the disclosure itself becomes the risk |
| **D-13** | **MVP is one site, complete** — one deployment site, complete end-to-end operation; local operation works independently of any remote layer; remote monitoring/integration may be supported but is not required for core operation; no assumption of a specific undocumented SSB CCTV workflow | Concentrates all effort on depth at one site instead of breadth across sites | If the force buys centrally, the MVP demos the wrong unit |
| **D-14** | **Develop and validate against the existing development/validation CCTV rig** in this repository, used to test IBVAP against real-world legacy CCTV/DVR constraints — not claimed to represent the SSB estate | Ties the MVP to one device's quirks | Over-fitting to one recorder; *counter:* it is a real hardware environment and has already falsified three assumptions |

### 19.1 The two decisions made first

These were accepted first, ahead of the rest, because most other decisions in this
document are downstream of them:

1. **D-7 (face recognition posture)** — it is the one an SIH evaluator is most likely
   to challenge: it ships a demonstrable, gated recognition capability in MVP —
   usable in a controlled development/test environment now, technically blocked for
   a real deployment until a recorded legal basis, the authority record, the
   authorized gallery and retention/oversight are all configured — without the
   project asserting that a legal basis for the SSB deployment exists (OQ-7 remains
   open); rejecting it would have meant withholding the capability from MVP entirely.
2. **D-13 (one site, complete)** — everything in [§10](#10-mvp-scope) is downstream
   of it.

---

## 20. Traceability — problem statement → this document

| Statement clause | Where honoured |
|---|---|
| Ingest live streams from standard IP-based CCTV | FR-1, FR-2, C-1 |
| Without dedicated FRS/ANPR/smart-camera hardware | FR-3, AC-P2, C-2 |
| Real-time analytics using AI/ML/CV | FR-14 – FR-19, C-3 |
| Human detection and tracking | CAP-1 |
| Vehicle detection and classification | CAP-2 |
| Face detection | CAP-3a |
| ANPR | CAP-4 |
| Virtual fence intrusion detection | CAP-5 |
| Suspicious activity detection | CAP-6 |
| Night-time movement detection | CAP-7 |
| Real-time alert generation and event logging | CAP-8 |
| Eliminate dependence on expensive dedicated hardware | G1, AC-P2, SM-6 |
| Enable intelligent monitoring through AI-powered analytics | G1, G3, CAP-1 – CAP-8 |
| Real-time alerts for security incidents and border intrusions | G3, CAP-5, CAP-8, NFR-1 – NFR-3 |
| Support facial recognition, vehicle identification and behavioural analytics through software | CAP-3b (gated), CAP-2, CAP-6; D-7, D-11 |
| Improve situational awareness and response time | G3, W3, SM-3 |
| Support integration with existing command and control systems | G7, D-5, FR-53 – FR-58 |
| Cost-effective, scalable, suitable for remote deployment | G5, NFR-7 – NFR-12, D-13 |

---

## Document status

**Stage:** 02 — Product Definition. **Draft, pending approval of
[§19](#19-product-decisions-requiring-human-approval).**

**What this document is:** the product definition for IBVAP — vision, users, jobs,
workflows, goals, functional and non-functional requirements, SIH capability
treatment, MVP and post-MVP scope, non-goals, metrics, constraints, assumptions,
risks, open questions and acceptance criteria.

**What this document is not:** a design, an architecture, a technology-stack
selection, or an implementation plan. **No stack is chosen. No architecture is
designed. No implementation tasks are created.**

**Known weaknesses, stated plainly:**

1. **No user of any kind has been spoken to in any research pass to date.** Every
   pain point behind this PRD is documentary, not observed.
2. **[§5](#5-core-user-workflows) is a PRODUCT MODEL in full.** The real workflow is
   unvalidated (OQ-1, OQ-3). D-3 and D-4 exist to make that survivable; they do not
   make it known.
3. **A1 is unrecorded.** The SIH organisation field for PS 26187 is not in
   `docs/00-project/`. **OQ-16 closes it in minutes and should be closed first.**
4. **Every number IBVAP will publish about itself is currently unmeasured.** NFR-4
   sets no false-alarm target for exactly this reason, and Gates 3–5 exist to fix it
   before any claim is made.

**Next stage gate:** per [CLAUDE.md](../../CLAUDE.md) §2,
[03-design](../03-design/) may begin for a feature once (a) the decisions in
[§19](#19-product-decisions-requiring-human-approval) that bear on it are approved
and recorded in [decisions.md](../00-project/decisions.md), and (b) the open
questions in [§17.1](#171-blocking--the-prds-honesty-depends-on-these) that bear on
it are answered or explicitly assumed with falsification criteria recorded.

# IBVAP — Product Requirements Document

| | |
|---|---|
| **Status** | Approved |
| **Date** | 2026-08-26 |
| **Owner** | IBVAP project |
| **Current build scope** | [§6](#6-current-build-mvp-scope) — five screens, per [ADR 0016](../adr/0016-mvp-ui-cut-to-five-screens.md) |
| **Primary requirement** | [problem.md](../00-project/problem.md) — the official SIH problem statement, PS 26187, immutable |
| **Source research** | [domain-research.md](../01-research/domain/domain-research.md) · [ssb-operational-context.md](../01-research/domain/ssb-operational-context.md) · [ssb-operational-workflow.md](../01-research/domain/ssb-operational-workflow.md) · [competitive-landscape.md](../01-research/competitors/competitive-landscape.md) · [technical-feasibility.md](../01-research/technology/technical-feasibility.md) · [product-discovery.md](../01-research/users/product-discovery.md) |

IBVAP is not India-specific. The SIH problem statement and the SSB research
define the validation context for this build, not the product's market
boundary — requirements below are written to hold generally, with anything
specific to this force or this market said plainly where it applies.

## Contents

1. [Executive summary](#1-executive-summary)
2. [Background](#2-background)
3. [Goals, non-goals and success criteria](#3-goals-non-goals-and-success-criteria)
4. [Users](#4-users)
5. [Requirements](#5-requirements)
6. [Current build (MVP scope)](#6-current-build-mvp-scope)
7. [Roadmap beyond this MVP](#7-roadmap-beyond-this-mvp)
8. [Risks and mitigations](#8-risks-and-mitigations)
9. [Open questions](#9-open-questions)
10. [References](#10-references)

---

## 1. Executive summary

A border force owns hundreds of CCTV cameras and no reliable way to know
which of them can actually tell it anything useful. Conventional CCTV only
records and displays; using it well requires someone watching continuously,
which does not scale across remote, low-staffed posts. Advanced capability —
facial recognition, ANPR, intrusion detection — is normally sold as
specialised, proprietary hardware, which is expensive and hard to deploy at
the scale a real border demands.

IBVAP turns the cameras a force already has into an intelligent surveillance
network in software: it ingests existing IP and analog CCTV, measures what
each camera can actually support, runs the eight capabilities the problem
statement names at a declared and honestly stated grade, and turns firings
into real-time alerts a human can assess in seconds. It does not replace the
existing recorder, does not require new hardware, and does not claim
capability a camera's optics cannot deliver.

The current build ([§6](#6-current-build-mvp-scope)) is five screens — Sign
in, Live View, Rules, Alerts & Events, Integration — covering exactly what
the problem statement names, nothing more.

---

## 2. Background

### The problem, as stated

Border forces deploy CCTV at posts, check posts and border roads for
surveillance, but conventional systems provide only recording and live
viewing — which requires continuous human observation to be useful.
Facial recognition, ANPR, intrusion detection and object tracking are
normally sold as specialised, proprietary hardware, making large-scale
deployment costly and difficult in remote areas. Full wording is recorded
verbatim in [problem.md](../00-project/problem.md).

### What the research adds

Every one of the eight named capabilities already exists as a shipping
software product from multiple vendors — there is no capability gap in the
market. What no vendor discloses is what a *specific inherited camera* can
actually support: capabilities needing identity — face recognition, ANPR,
fine vehicle attributes — need far higher pixel density on target than
cameras installed for general overview were ever specified to deliver.
NIST's own conclusion on video face recognition is that it can approach
still-photo accuracy only if image collection improves — camera positioning,
mounting, lighting, optics — all of which are hardware, not something
software fixes after the fact.

The documented failure mode across comparable deployments is nuisance
alarms, not missed detections: 90% of SBInet's sensor alerts were false
alarms, and a comparable Indian border programme's own analysis names false
alarms and sensor malfunction as a leading technical issue, with no protocol
defined for distinguishing an infiltrator from wildlife. An alerting system
operators don't trust gets ignored, which is worse than no system.

The deployment context itself defeats most vendors' assumed architecture:
a meaningful share of SSB border posts lack road connectivity, run on
generators or solar, and carry satellite phones as their communication
fallback — every commercial platform surveyed assumes a control room or a
cloud tenant that this estate frequently does not have.

And on the Indo-Nepal/Indo-Bhutan validation border specifically, crossing
itself is not the offence — it's a treaty right for Indian, Nepali and
Bhutanese nationals. MHA's own framing of the challenge across three
consecutive Annual Reports is "to check misuse of the open border," not to
stop crossing. A line-crossing alarm that fired with perfect accuracy would
still be almost entirely noise on this specific border, even though the
same mechanism is exactly right on a closed or fenced one.

### The product problem IBVAP solves

A border force owns cameras it cannot watch, at posts it cannot reach, on
links it cannot fill, with no way to know which camera is capable of telling
it anything useful. When something does happen, the record of it is shaped
for an outcome ledger, not for a detection — and evidence has to survive a
handover to an organisation that did not produce it.

---

## 3. Goals, non-goals and success criteria

### Goals

| Goal | What it means |
|---|---|
| **Zero new hardware** | A camera the force already owns produces machine-generated events without new camera hardware |
| **Trustworthy alerts** | Events are trustworthy enough to act on — a measured, published nuisance rate per camera, not a vendor claim |
| **Fast human decision** | A human learns about something worth attention, and can assess it, faster than by watching |
| **Honest capability** | The system states, per camera, what it can and cannot do — and refuses what it cannot |
| **Runs where the market doesn't** | No console, no engineer, no reliable link, no reliable power required |
| **Full statement coverage** | All eight named capabilities are present, each at a declared and measured grade |
| **Integrable** | What it emits can be consumed by a command-and-control system, even one not yet named |

### Non-goals

| Not doing | Why |
|---|---|
| Replacing the existing VMS or recorder | Outside the statement's scope; competes on the incumbents' strongest ground for no benefit |
| A learned anomaly model for "suspicious activity" | Measured research shows these badly overfit to scene and collapse on realistic evaluation; an operator-authored rule engine is the honest construction until the force defines the term |
| Open-set face identification of the general population | Legally unresolved on a treaty-open border, and prohibited by default for law enforcement under the EU AI Act — bounded watchlist matching only, and even that is cut from the current build (§6) |
| ANPR on wide-area border-road cameras | Physics, not effort — the pixel density needed is far beyond what that range and angle delivers |
| Full video egress to a central site | The arithmetic doesn't work at real link speeds, and the market has already converged away from it |
| Competing on published accuracy benchmarks | Benchmarks in this market are unpublished, paywalled, or scene-overfitted; IBVAP publishes its own measured numbers on its own footage instead |
| Claiming universal camera support | Even the best-resourced vendors in this market maintain per-model compatibility labs and still warn buyers |
| Dispatch, tasking or response coordination | IBVAP produces notice and evidence; it does not command a response |
| Detecting trafficking, contraband, currency or narcotics | A camera cannot see contraband inside a sack — IBVAP detects people, vehicles, faces, plates, movement and time, and says so plainly |
| A pricing model in this document | The floor competitor in this market is free and open source; "cheaper" is not yet a testable claim |

### Success criteria

| Metric | What's measured | Target |
|---|---|---|
| Alert precision | Alerts assessed real ÷ all assessed, per camera per rule | Measured and published; the 90% false-alarm precedent is the bar to beat, not a target to adopt |
| Nuisance rate and cause | False alarms per camera per day, broken down by cause | Measured and published, day and night separately |
| Time to assessable evidence | Rule-satisfying frame → human sees the record and a crop | ≤30 s on a 128 kbps link |
| Capability coverage and refusal rate | Share of cameras measured; share of analytic-camera pairs correctly refused | 100% coverage; refusals are a success signal, not a defect count |
| Events from unmodified estate | Events produced with zero hardware change | 100% |
| Commissioning time | Two cameras, no site survey, no integrator | ≤1 hour |
| Disconnection survival | Hours of link-down with full local function and clean reconciliation | ≥72 hours, zero duplicates, zero losses |
| Egress consumability | An independent external consumer ingests the published schema without bespoke help | At least one |

No target is set for detection accuracy, a false-alarm rate, or supported
camera makes — those are measured and published on this deployment's own
footage, not asserted in advance.

---

## 4. Users

| User | What they need |
|---|---|
| **Post in-charge** | Told when something worth attention happens on their stretch, with enough to judge it in seconds, without watching a screen — and told plainly when a camera can't do something before they rely on it |
| **Check-post in-charge** | A plate read and logged automatically, and a face detected where the camera is sited to see one, instead of written into a register |
| **Company/Battalion commander** | Learns about something worth deciding on sooner than by phone, and can see how noisy the system that told them is |
| **Monitoring operator** *(if the role exists at this force — unconfirmed)* | The same events reach a console without the site needing to be configured any differently |
| **Technical maintainer** | When something breaks, it says so in a sentence they can read out over a radio — this force has no dedicated IT or video cadre |
| **Procurement / modernisation staff** | An independently auditable dataset showing whether this contributed to anything |

Whether this force staffs continuous video monitoring at all is genuinely
unconfirmed (see [§8](#8-open-questions)) — IBVAP is built to work correctly
whether or not that role exists, rather than assuming either answer.

---

## 5. Requirements

### 5.1 The eight named capabilities

| Capability | What ships | Key constraint |
|---|---|---|
| **Human detection and tracking** | Detection and single-camera tracking, gated on a minimum analysed frame rate | Tracking needs roughly 3+ analysed frames per second; below that, identity association collapses and the rule is disabled with a stated reason |
| **Vehicle detection and classification** | Coarse type only — car, truck, bus, motorcycle, bicycle | Make, model and colour are out of scope; colour is unavailable at night on IR-illuminated footage regardless |
| **Face detection** | Detection — presence and location, not identity | Overhead, wide-angle cameras installed for area overview mostly see the tops of heads; where a camera can't support it, the product says so rather than silently returning nothing |
| **Facial recognition** *(Expected Solution)* | Not in the current build ([ADR 0016](../adr/0016-mvp-ui-cut-to-five-screens.md)) | Matching a detected face against a watchlist needs a legal-authority workflow — recorded legal basis, authority record, bounded gallery, retention rules — that a five-screen demo build doesn't carry. See §6 |
| **ANPR** | Plate reads, logged with per-read confidence, on lane- or gate-aimed cameras only | Needs far higher pixel density than a wide-area border-road camera delivers; excluded there on physics, not effort |
| **Virtual fence intrusion detection** | Operator-drawn lines and zones, gated on object class, confidence and minimum track length | On the validation border specifically, crossing is a treaty right, so the same mechanism is reframed as an attention zone (report who/what/when) alongside the standard intrusion framing, which stays available unchanged for closed borders |
| **Suspicious activity detection** | Operator-authored composite rules over the reliable primitives above | "Suspicious" has no agreed definition anywhere in the problem statement or the research; a human defines it as a rule, since learned anomaly models measurably fail to transfer between scenes |
| **Night-time movement detection** | The same detection primitives, run continuously after dark, with a separately measured night eligibility and nuisance rate per camera | Visible-light detection measurably degrades relative to infrared at night; the product states its own measured day/night gap rather than a literature figure |
| **Real-time alert generation and event logging** | Every rule firing writes an Event; an alerting rule also raises an Alert, delivered payload-progressively (record, then a small crop, then a full clip only on request) | The record→crop→clip ordering is arithmetic: a full clip is roughly 300× the size of a crop, which matters directly on a 128 kbps link |
| **Integration with command-and-control** *(Expected Solution)* | A published, versioned, documented outbound event feed | No adapter to a named system ships — what "existing command and control systems" means for this force isn't established, so a generic, demonstrated contract is the strongest claim that can be made honestly |

### 5.2 Cross-cutting requirements

| Requirement | Detail |
|---|---|
| Read-only against the existing estate | Never reconfigures a camera or recorder, never takes over recording, never alters the existing live-view path |
| Honest capability disclosure | A capability a specific camera cannot reliably support is not offered — stated inline, in plain language, where a user would look for it |
| No invented vocabulary | Never "intruder," "suspect," "threat level," "identified" — only the detected class and the rule that fired |
| Local, unattended operation | Detection, rule-firing and event logging continue with no screen open and no remote link, for at least 72 hours disconnected, queuing and reconciling without duplication or loss on reconnect |
| Plain-language health reporting | Every failure state is expressible in one sentence a non-technical post commander can relay over a radio |
| Non-technical commissioning | A two-camera site commissioned in under an hour by a non-specialist, without a site survey or certified integrator |
| No licence-driven degradation | Nothing expires, disables or degrades because a licence or update server is unreachable |
| Isolated-network deployable | No outbound internet dependency required |
| Attributable actions | Every consequential action is tied to a person and a time |
| Rig-measured constraints | A camera labelled "1080p" may deliver as few as 960 real horizontal pixels (anamorphic encoding); firmware may report a setting as accepted while silently discarding it; recorder bandwidth is shared and finite — measured on the development CCTV rig, not assumed ([ADR 0015](../adr/0015-mvp-validated-against-development-cctv-rig.md)) |

---

## 6. Current build (MVP scope)

Five screens — Sign in, Live View, Rules, Alerts & Events, Integration —
covering exactly what the problem statement names, nothing more. Per
[ADR 0016](../adr/0016-mvp-ui-cut-to-five-screens.md), this narrows a broader 27-screen design;
the full reasoning for the cut lives there. **Status: frozen.**

### 6.1 Capability → screen mapping

| SIH capability | Implementation | Screen |
|---|---|---|
| Human detection and tracking | Box + label overlay | Live View |
| Vehicle detection and classification | Box + label overlay | Live View |
| Face detection | Box overlay. Detection only — no gallery matching (§6.3) | Live View |
| Automatic Number Plate Recognition | Plate text overlay, logged | Live View, Alerts & Events |
| Virtual fence intrusion detection | Line/zone rule | Rules |
| Suspicious activity detection | Zone + class/dwell rule, operator-authored | Rules |
| Night-time movement detection | Continuous detection after dark; day/night state indicator | Live View |
| Real-time alert generation and event logging | Rule firing → Event (always). Alerting rule → Event + Alert | Alerts & Events |
| Integration with command-and-control systems *(Expected Solution)* | Documented outbound event feed | Integration |

### 6.2 End-to-end workflow

| Step | Action | Screen |
|---|---|---|
| 1 | Camera added via its existing stream address. No reconfiguration of camera or recorder. | Live View |
| 2 | Detection runs on the live stream: boxes, labels, plate text. | Live View |
| 3 | A rule is defined against the camera: line/zone, class, condition, alert-or-log-only. | Rules |
| 4 | Rule fires → one Event is written. Alerting rule → an Alert is also raised. | — |
| 5 | Alert reviewed; assessed real / not real / unsure in one action. | Alerts & Events |
| 6 | Not-real assessment may mute that camera+rule combination for a set duration (1h / 1d / 1w / indefinite) or be reversed early. | Alerts & Events |
| 7 | Event feed delivered to an external destination. | Integration |

### 6.3 Cut from this build

Excluded per **D-15**. Not simplified into another screen — removed. Not
named in `problem.md`.

| Excluded | Reason |
|---|---|
| Case management, evidence-pack export, chain-of-custody records | Not named in `problem.md`. The event log remains the record of what happened; export/custody tooling is downstream work |
| Face-recognition matching against a watchlist | Requires a legal-authority workflow not built in this MVP. Detection (§6.1) is unaffected |
| Camera-capability certification screen, override workflow, re-issue cycle | Requirement retained (§5.2) as an inline state on Live View, not as a separate screen |
| Audit log, authority records, people & roles management | Governance tooling for a permanent deployment, not a demo requirement |
| Measurement dashboard, system-health dashboard | Same |

If IBVAP is developed past this MVP, these are the first items to revisit —
deferred, not disproven.

### 6.4 Acceptance criteria

| # | Criterion |
|---|---|
| **AC-1** | Two cameras ingest unmodified, including at least one analog channel behind the existing DVR. |
| **AC-2** | Each of the eight named capabilities fires at least once, correctly, on a camera that supports it. |
| **AC-3** | At least one capability is refused, inline, with a plain-language reason, on a camera that cannot support it. |
| **AC-4** | A rule (line or zone) is authored, fires, and produces exactly one Event, plus one Alert if the rule is alerting. |
| **AC-5** | An alert is assessed in one action; a not-real assessment offers a mute, and the mute suppresses the next repeat. |
| **AC-6** | The event feed reaches a real external destination via Integration. |
| **AC-7** | Detection, logging and alerting continue with no screen open. |

### 6.5 Known limitations

| Limitation | Detail |
|---|---|
| Detection accuracy | Depends on camera resolution, mounting angle and distance. Measured and stated, not corrected. |
| Night-time detection | IR-illuminated, effectively monochrome. No colour-dependent claim is made after dark. |
| "Suspicious activity" | No agreed definition exists in `problem.md` or the research corpus. Defined per-deployment by a human as a rule, not inferred by the product. |
| Command-and-control integration | No adapter to a named system ships. Integration publishes a documented event feed; the receiving system is out of scope. |

---

## 7. Roadmap beyond this MVP

| Item | Unblocked by |
|---|---|
| Face-recognition matching against a watchlist, for a real deployment | A recorded legal basis, an authority-record mechanism, and a bounded, authorized gallery all being configured — the original gate design is preserved in [ADR 0008](../adr/0008-face-detection-unconditional-gated-recognition.md) |
| Case management and evidence-pack export | Product decision to reintroduce it — deferred, not disproven |
| A reference adapter to a named C2 system | Knowing what that system actually is — currently unestablished |
| Multi-site aggregation to a higher echelon | Confirming whether live monitoring exists above post level at all |
| Pattern-over-time / route-usage analytics | A resolved legal basis — on a treaty-open border, retaining records of lawful crossings may not be permissible at all |
| A validated "suspicious activity" rule set | The force's own definition, stated as observable behaviour |
| Thermal stream analytics | Knowing what share of the real estate is thermal |
| Cross-camera tracking / re-identification | Camera geometry the current estate doesn't provide; feasibility is currently low |
| Standards-based egress (ONVIF Profile M, MISB ST 0903) | An interoperability spike — both exist, no surveyed vendor emits either today |

---

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| The real monitoring workflow at this force is unconfirmed — a product built around one specific posture could be wrong | Built to work correctly whether or not a console operator exists; nothing in the core loop requires one |
| The estate's cameras may not physically support the capabilities the statement names, and this hasn't been measured at scale | Per-camera capability is measured and stated inline before anything is claimed; refusal is a normal, honest outcome, not a defect |
| Nuisance alarms erode trust faster than missed detections do | Object-class gating, a measured and published nuisance rate, and a reversible per-camera-per-rule mute |
| Night is the operational peak and the technical trough | Detection continues after dark; the product measures and states its own day/night gap rather than assuming parity |
| The uplink may not carry what a naive design assumes | Payload-progressive alerts, site-local analysis, and a declared discard policy when a queue fills |
| Evidence or logged data could be unusable later — bad hash, bad timestamp | Every event carries a time-integrity status; events under a suspect clock are marked. (Evidence export itself is cut from this build — see §6) |
| Integration has no confirmed target system | A published, versioned, generic contract now; a named adapter only once a real target is identified |
| Legal exposure from biometric processing on a treaty-open border | Face-recognition matching is cut entirely from this build; detection only ships, which raises no matching/biometric-record question |
| Per-camera-model compatibility work is unbounded | A maintained record of which makes/models/firmware have actually been tested, rather than an unqualified "supports ONVIF" claim |
| The department's real, ledger-recorded priorities (contraband, narcotics, trafficking) are not what video can see | Stated plainly on the product's own surface — a camera cannot see contraband inside a sack, and IBVAP does not claim otherwise |

---

## 9. Open questions

Genuinely unresolved items that would change scope if answered. None of
these is silently assumed elsewhere in this document.

| Question | Why it matters |
|---|---|
| Does this force monitor live video at all today, and at what level? | Determines whether a console/operator layer is ever built, and at what priority |
| What cameras actually exist across the estate — count, model, resolution, IP vs. analog behind a DVR? | Determines which capabilities have any eligible camera at all |
| Is there a written standard operating procedure for detection → assessment → response? | Determines whether the assumed workflow survives contact with reality |
| What does "suspicious activity" mean here, stated as observable behaviour? | Directly defines the suspicious-activity capability; no experiment substitutes for this answer |
| What are this force's "existing command and control systems," specifically? | Determines whether a generic event feed is sufficient or a named adapter becomes necessary |
| What connectivity and power actually exist at a typical post? | Sets the real bandwidth and uptime budget the product has to live inside |
| What is the legal basis, authority level and retention rule for biometric processing of people exercising a treaty right of movement? | Blocks any future reintroduction of face-recognition matching |
| Is there a reliable time source (NTP, GNSS, or none) at a disconnected post? | A wrong clock with no visible warning is the worst version of the evidential-risk problem, should evidence handling return |
| What security accreditation and data-classification policy applies to a platform handling live border video? | Determines whether any network connectivity beyond fully isolated is ever permissible |

---

## 10. References

- [problem.md](../00-project/problem.md) — the official SIH problem statement (immutable)
- [docs/adr/](../adr/README.md) — decision records, one file per decision (ADR 0001 … 0029)
- [UX.md](../03-design/UX.md) — screens and states for the current build
- [domain-research.md](../01-research/domain/domain-research.md)
- [ssb-operational-context.md](../01-research/domain/ssb-operational-context.md)
- [ssb-operational-workflow.md](../01-research/domain/ssb-operational-workflow.md)
- [competitive-landscape.md](../01-research/competitors/competitive-landscape.md)
- [technical-feasibility.md](../01-research/technology/technical-feasibility.md)
- [product-discovery.md](../01-research/users/product-discovery.md)

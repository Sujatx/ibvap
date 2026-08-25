# Decisions Log

Record of project-level DECISIONs, each with rationale and date. Stage-specific
decisions (product, design, architecture) may keep their own log within that
stage's folder; this file is for project-level decisions.

Use this format per entry:

```
## YYYY-MM-DD — Short title

**DECISION:** ...
**Rationale:** ...
**Status:** proposed | accepted | superseded by <link>
```

---

## 2026-08-24 — Project setup and documentation structure established

**DECISION:** Adopt the workflow Research → Product → Design → Architecture →
Engineering → Testing → Demo, with corresponding `docs/` folders, and treat the
official SIH problem statement (Problem Statement ID 26187) recorded in
[problem.md](problem.md) as immutable. No tech stack, architecture, or product
features are chosen at this stage.

**Rationale:** Per explicit project setup instructions — keep research,
product, design, architecture, and implementation separate, and avoid
premature technical or product decisions.

**Status:** accepted

---

## 2026-08-25 — D-1: Differentiate on deployment, transparency and reliability, not on benchmark accuracy leadership

**DECISION:** IBVAP differentiates through deployment, transparency, reliability
and camera-aware operation; it pursues sufficient accuracy for each defined use
case rather than competing primarily on benchmark leadership. It will not claim
universal camera support, and it will not chase headline accuracy figures
disconnected from a measured use case — but accuracy remains a first-class,
per-capability requirement, gated and reported by the Camera Passport rather than
asserted in the abstract. It competes on running where nothing else runs and on
stating, per camera, what it can and cannot do, at what measured accuracy.

**Rationale:** All eight capabilities are commodity, so accuracy claimed in the
abstract is not a defensible sole differentiator against vendors with decades of
tuning; the four best-evidenced pain points (PP2, PP3, PP4, PP7) are all
conditions of deployment. Sufficient, measured accuracy per use case remains
required — it is the entry condition the Camera Passport enforces (D-6) — it is
just not, by itself, the basis for competitive positioning
([product-discovery.md](../01-research/users/product-discovery.md) §4.1, §9).

**Reference:** [docs/02-product/PRD.md](../02-product/PRD.md), §1.2 "Why the
second half of that sentence is in the vision", Decision D-1.

**Status:** accepted

---

## 2026-08-25 — D-2: SSB is the validation context, not the product boundary

**DECISION:** SSB is the validation context, not the product boundary. All
requirements are written force-agnostically and market factors are labelled.
SSB-specific and India-specific requirements are marked `[SIH/SSB]` /
`[MARKET:IN]` and are *satisfiable* rather than *assumed*.

**Rationale:** [CLAUDE.md](../../CLAUDE.md) §4 requires it; the problem statement
text itself says only "border security forces".

**Reference:** [docs/02-product/PRD.md](../02-product/PRD.md), §1.3 "Positioning
within scope (per CLAUDE.md §4)", Decision D-2.

**Status:** accepted

---

## 2026-08-25 — D-3: Function correctly whether or not a remote monitoring/control-room layer is available

**DECISION:** IBVAP is designed to function correctly whether or not a remote
monitoring/control-room layer is available, or is temporarily unavailable. Core,
site-local operation — analysis, rule-firing, logging, local alerting — does not
depend on a control room, an operator on shift, or a console being present or
reachable. Where a remote monitoring or control-room capability does exist, IBVAP
integrates with it as an additive layer. Nothing in the MVP requires an operator
to be watching, and nothing in the MVP assumes one is not.

**Rationale:** The exact SSB CCTV/control-room workflow is unresolved (H-1);
designing around either its presence or its absence as the assumed baseline
invents a workflow the research does not establish, so the product is built to be
correct under both answers rather than to bet on one. Falsified by: an answer to
B2 showing a staffed monitoring posture that this additive layer fails to serve.

**Reference:** [docs/02-product/PRD.md](../02-product/PRD.md), §3.1 "Primary
users — the product is designed for these", Decision D-3.

**Status:** accepted

---

## 2026-08-25 — D-4: Core workflows modelled around artefacts and their states

**DECISION:** Core workflows are modelled around artefacts and their states, with
role assignment and permissions configurable. The product produces four core
artefacts — an Event, an Alert, a Case, and a Camera Passport — and every
workflow is a path through those artefacts' states. Which human occupies which
step, and what permissions that role carries, is configurable and carries no
product assumption about the real SSB workflow.

**Rationale:** This is the only way to satisfy the constraint in
[§0.1 of the PRD](../02-product/PRD.md#01-labels--and-the-one-distinction-that-matters-most)
while still shipping a coherent workflow. If H-1 resolves to "there is a staffed
control room", the same artefacts and states route to an operator under the
corresponding role and permissions; if it resolves to "a Sub-Inspector and a
phone", the same artefacts route to him. No re-architecture is required by either
answer, and that property is itself the requirement (FR-31).

**Reference:** [docs/02-product/PRD.md](../02-product/PRD.md), §5.1 "The design
invariant that makes a PRODUCT MODEL safe here", Decision D-4.

**Status:** accepted

---

## 2026-08-25 — D-5: Satisfy C2 integration via a demonstrated generic event contract, not a named adapter

**DECISION:** IBVAP satisfies "integration with existing command and control
systems" by being an emitter with a documented, stable, open event contract,
demonstrated against at least one real external integration path — not by
shipping an adapter for a named system. MVP ships the published, versioned event
schema plus a generic outbound mechanism (e.g. webhook, REST, or MQTT), and
demonstrates that mechanism actually delivering events to a real external
consumer end-to-end. Standards-based egress (ONVIF Profile M over MQTT; MISB
ST 0903 VMTI within STANAG 4609) and adapters for a specific named C2 system
remain post-MVP, unless and until a real target system is identified — and no
vendor surveyed emits either standard today.

**Rationale:** Building an adapter for a system that has no name is the
documented integration risk; a published, demonstrated generic contract is the
strongest form of the requirement that can be satisfied before H-6 is answered —
it proves the mechanism works end-to-end without inventing a target that does not
exist. Falsified by: H-6 naming a system, at which point a reference adapter to
that named system becomes MVP-worthy.

**Reference:** [docs/02-product/PRD.md](../02-product/PRD.md), §5.8 "W6 — Emit to
a command and control system", Decision D-5.

**Status:** accepted

---

## 2026-08-25 — D-6: Refuse capabilities the camera cannot support, rather than degrade them

**DECISION:** A capability that the camera cannot support is refused, not
degraded. Overriding is possible, requires a named authority, and permanently
marks the resulting events.

**Rationale:** This is the product's central claim (D-1) and the market's
unfilled gap; a soft warning would be indistinguishable from every vendor's
disclaimer. Known cost: it means telling a buyer their estate cannot do what they
hoped — the counter-evidence recorded against opportunity O1.

**Reference:** [docs/02-product/PRD.md](../02-product/PRD.md), §7.2 "Camera
Passport — capability measurement and disclosure", Decision D-6.

**Status:** accepted

---

## 2026-08-25 — D-7: Face detection unconditional in MVP; controlled, gated face recognition also ships in MVP

**DECISION:** MVP priority: P1, gated. Face detection (CAP-3a) ships
unconditionally in MVP. The controlled face-recognition capability also ships in
MVP and can be exercised and demonstrated in a controlled development/test
environment, against an explicitly configured, bounded gallery. For a real
deployment, biometric matching is technically blocked unless all four conditions
are configured and current for that deployment: (1) a recorded, valid legal basis
for that deployment; (2) the required authority record; (3) the authorized,
bounded gallery; (4) applicable retention and oversight requirements. The
authority record is never treated by the product as evidence that the legal
basis exists — the two are separate, independently required and independently
recorded conditions. Any biometric operation outside those configured, satisfied
conditions is blocked by the product, not merely discouraged, and every
biometric operation — enable, match, no-match, gallery change, authority-record
change, legal-basis-record change, expiry — is logged and auditable. No
unrestricted, open-set or population-scale face recognition ships at any point.

**Rationale:** The statement requires facial recognition to be supported through
software, and this decision ships that support in MVP — demonstrable now,
technically gated for real use — without asserting a legal basis this project
has not established. This document does not claim, and this decision does not
create, a legal basis for activating biometric matching against the SSB
deployment; OQ-7 (the legal basis, authorisation level, retention rule and
oversight for biometrics on a treaty-open border) remains explicitly unresolved.
This decision is the one most likely to be contested at SIH evaluation and needs
an explicit human call.

**Reference:** [docs/02-product/PRD.md](../02-product/PRD.md), §9, CAP-3b — Face
recognition (the statement's "support facial recognition … through software"),
Decision D-7.

**Status:** accepted

---

## 2026-08-25 — D-8: All eight SIH capabilities addressed, with declared maturity, conditions and limitations

**DECISION:** All eight SIH capabilities are explicitly addressed in the product,
with implementation maturity, operating conditions and limitations declared for
each. Each is delivered at a declared grade, gated by the Camera Passport, with
its limitations stated in the product surface. No capability is delivered as an
unqualified claim, and no SIH capability is silently omitted.

**Rationale:** The problem statement is the primary requirement (rule 1) and
inventing requirements is forbidden (rule 2); but the research establishes hard
physical bounds on several of these capabilities on inherited cameras, and
PR1/PR10 forbid claiming what cannot be measured. Declaring maturity, operating
conditions and limitations per capability is the only construction that
satisfies both — an unqualified claim of full delivery would violate PR1/PR10,
and dropping any capability would violate rule 2.

**Reference:** [docs/02-product/PRD.md](../02-product/PRD.md), §9 "SIH-required
capabilities" (introduction), Decision D-8.

**Status:** accepted

---

## 2026-08-25 — D-9: IBVAP as a support-posture analytics layer alongside existing infrastructure

**DECISION:** IBVAP is an intelligent video-analytics layer that can operate
alongside existing surveillance/VMS infrastructure and integrate with external
command/control systems — not a system that replaces the existing surveillance
system or that removes the human from assessment. Per capability, an alert
routes to a human for assessment rather than acting as the sole basis for a
decision; in i-LIDS terms, IBVAP operates in a support posture for every
capability in the MVP, not as the primary (sole) detection system.

**Rationale:** i-LIDS distinguishes these and the choice determines alerting,
staffing and liability; the competitive research explicitly names this as a
decision to be made deliberately rather than by default. IBVAP has no measured
detection probability on this estate and will not have one before X1/X2.
Operating as an additive support layer alongside existing infrastructure is the
honest posture and is reversible upward per-rule once measured; declaring itself
the sole detection system is not reversible after a miss.

**Reference:** [docs/02-product/PRD.md](../02-product/PRD.md), §9 "Grade
vocabulary used below", Decision D-9.

**Status:** accepted

---

## 2026-08-25 — D-10: Virtual fence ships in full, plus an open-border framing

**DECISION:** The virtual-fence capability ships in full, and additionally
supports an open-border framing. IBVAP does not remove or rename intrusion
detection; it adds the ability to make the reportable condition be class, time,
direction, dwell or accompaniment rather than the crossing itself.

**Rationale:** The statement requires the capability (rule 1) and it is
technically straightforward; the research establishes it is operationally
misdirected on this particular border but not on fenced borders generally —
which is exactly the [BORDER] vs [SIH/SSB] distinction CLAUDE.md §4 demands.

**Reference:** [docs/02-product/PRD.md](../02-product/PRD.md), §9, CAP-5 —
Virtual fence intrusion detection, Decision D-10.

**Status:** accepted

---

## 2026-08-25 — D-11: Suspicious activity detection as an operator-authored rule engine, not a learned model

**DECISION:** "Suspicious activity detection" is delivered as an
operator-authored composite rule engine over reliable primitives, plus a starter
library explicitly marked unvalidated. No learned anomaly model ships in MVP.

**Rationale:** Three independent, measured failures of learned VAD (scene
overfitting, false-alarm explosion, contested ground truth) against a capability
whose definition nobody has supplied. The rule engine is the only construction
that can be honest about what it detects. This decision must be revisited the
moment OQ-4 is answered by the force — no experiment substitutes for that
answer.

**Reference:** [docs/02-product/PRD.md](../02-product/PRD.md), §9, CAP-6 —
Suspicious activity detection, Decision D-11.

**Status:** accepted

---

## 2026-08-25 — D-12: Night-time Movement Detection as an explicit, measured MVP capability

**DECISION:** Night-time Movement Detection is an explicit product capability,
implemented as a first-class, separately-measured operating mode across the
existing detection primitives, rather than as a separate "night AI model."
Concretely, it is delivered through: (a) night-specific camera eligibility on
the Camera Passport, measured after dark and reported independently of the day
verdict; (b) the same person and vehicle movement-detection primitives (CAP-1,
CAP-2) run against night-eligible cameras; (c) night-scoped rules — time-of-day
gating on zones, lines, direction and dwell; and (d) measured, disclosed
limitations — the night-vs-day performance gap and cause histogram, published
per camera. IBVAP does not ship a separate model or product surface named
"night analytic" — night is a condition the existing primitives are measured and
gated against, not a distinct detector requiring its own architecture.

**Rationale:** The market's framing (night is a condition, not a feature) is
correct and evidenced; the gap is that nobody measures and discloses the
condition, and the statement names the capability explicitly, so it must be
represented in the product as a real, named capability rather than only as an
internal engineering property. Thermal support is post-MVP and gated on OQ-12
(what fraction of the estate is thermal).

**Reference:** [docs/02-product/PRD.md](../02-product/PRD.md), §9, CAP-7 —
Night-time movement detection, Decision D-12.

**Status:** accepted

---

## 2026-08-25 — D-13: MVP scoped to one deployment site, complete end-to-end

**DECISION:** The MVP is one site, complete. The smallest coherent product is a
single deployment site with its existing cameras, running the full loop —
ingest → passport → primitives → rules → event → alert → assessment → case →
export → egress — end to end. The MVP boundary is: (a) one deployment site; (b)
complete end-to-end operation across that loop; (c) local, site-level operation
must work independently of any remote layer; (d) remote monitoring and/or
command-and-control integration may be supported where present, but core
operation does not require it; (e) the MVP does not assume a specific,
undocumented SSB CCTV or control-room workflow; (f) core operation does not
require a remote control room.

**Rationale:** This is the smallest unit that demonstrates the complete
operational value of IBVAP end-to-end while satisfying the SIH direction, and it
is the unit the estate actually consists of (734 posts, 42% unroaded). The exact
SSB monitoring workflow is unresolved (H-1); drawing the MVP boundary this way
means it neither assumes a control room exists nor asserts that one does not.

**Reference:** [docs/02-product/PRD.md](../02-product/PRD.md), §10.1 "The MVP
thesis", Decision D-13.

**Status:** accepted

---

## 2026-08-25 — D-14: MVP developed and validated against the existing development CCTV rig

**DECISION:** The MVP is developed and validated against the existing
development CCTV rig in this repository — five live channels behind a real
analog XVR with a fixed 1080N anamorphic encode, a shared 12,288 kbps / 120 fps
budget across 8 channels, TCP-only RTSP, and firmware that returns OK for
settings it discards. This rig is the existing development and validation
environment used to test IBVAP against real-world legacy CCTV/DVR constraints —
it is not claimed to represent the SSB camera estate, which remains unmeasured
(OQ-2).

**Rationale:** A single measured recorder already falsified three convenient
assumptions (UDP viability, the "1080" resolution claim, and
read-back-vs-trust firmware behaviour), which is why development is validated
against real hardware constraints rather than specified ones. Per CLAUDE.md
rule 6, the existing setup (`dvr.py`, `dvr.env`, `backups/`, `requirements.txt`)
is preserved, not modified — IBVAP consumes it, it does not replace it.

**Reference:** [docs/02-product/PRD.md](../02-product/PRD.md), §10.4 "MVP
validation estate", Decision D-14.

**Status:** accepted

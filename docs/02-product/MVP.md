# IBVAP — MVP Scope

**Stage:** 02 — Product Definition
**Date:** 2026-08-26 (rewritten per [D-15](../00-project/decisions.md) — five-screen scope)
**Status:** Frozen.

**Summary:** Existing CCTV in, AI detection on the feed, real-time alerts on
operator-defined rules, event logging, and an outbound integration feed. Five
screens. Every capability traces to [problem.md](../00-project/problem.md)
(immutable); the document adds nothing beyond it.

## Contents

1. [Capability mapping](#1-capability-mapping)
2. [Workflow](#2-workflow)
3. [Retained requirements](#3-retained-requirements)
4. [Out of scope](#4-out-of-scope)
5. [Acceptance criteria](#5-acceptance-criteria)
6. [Known limitations](#6-known-limitations)
7. [Document status](#7-document-status)

---

## 1. Capability mapping

| SIH capability | Implementation | Screen |
|---|---|---|
| Human detection and tracking | Box + label overlay | Live View |
| Vehicle detection and classification | Box + label overlay | Live View |
| Face detection | Box overlay. Detection only — no gallery matching (§4) | Live View |
| Automatic Number Plate Recognition | Plate text overlay, logged | Live View, Alerts & Events |
| Virtual fence intrusion detection | Line/zone rule | Rules |
| Suspicious activity detection | Zone + class/dwell rule, operator-authored. No agreed definition of "suspicious" exists in the problem statement or research corpus, so the condition is human-defined, not a learned model | Rules |
| Night-time movement detection | Continuous detection after dark; day/night state indicator | Live View |
| Real-time alert generation and event logging | Rule firing → Event (always). Alerting rule → Event + Alert | Alerts & Events |
| Integration with command-and-control systems *(Expected Solution)* | Documented outbound event feed | Integration |

Five screens: Sign in, Live View, Rules, Alerts & Events, Integration.

---

## 2. Workflow

| Step | Action | Screen |
|---|---|---|
| 1 | Camera added via its existing stream address. No reconfiguration of camera or recorder. | Live View |
| 2 | Detection runs on the live stream: boxes, labels, plate text. | Live View |
| 3 | A rule is defined against the camera: line/zone, class, condition, alert-or-log-only. | Rules |
| 4 | Rule fires → one Event is written. Alerting rule → an Alert is also raised. | — |
| 5 | Alert reviewed; assessed real / not real / unsure in one action. | Alerts & Events |
| 6 | Not-real assessment may mute that camera+rule combination for a set duration (1h / 1d / 1w / indefinite) or be reversed early. | Alerts & Events |
| 7 | Event feed delivered to an external destination. | Integration |

---

## 3. Retained requirements

Carried from **D-1 … D-14**. Unaffected by the screen-count reduction.

| Requirement | Specification | Source |
|---|---|---|
| No overclaiming camera capability | A class not reliably supported on a given camera is not drawn; a one-line reason is shown inline on Live View | D-1, D-6 |
| Controlled vocabulary | No "intruder," "suspect," "threat level." Only the detected class and the rule that fired | — |
| No dedicated hardware required | Runs against existing IP cameras and analog channels behind an existing DVR/XVR | — |
| Local, unattended operation | Detection, rule evaluation and event logging continue with no screen open and no remote link | — |
| Rig-measured constraints | A camera labelled "1080p" may deliver as few as 960 real horizontal pixels (anamorphic encoding); firmware may report a setting accepted while discarding it; recorder bandwidth is shared and finite | D-14 |

---

## 4. Out of scope

Excluded from this MVP per **D-15**. Not simplified into another screen —
removed. Not named in `problem.md`.

| Excluded | Reason |
|---|---|
| Case management, evidence-pack export, chain-of-custody records | Not named in `problem.md`. The event log remains the record of what happened; export/custody tooling is downstream work |
| Face-recognition matching against a watchlist | Requires a legal-authority workflow not built in this MVP. Detection (§1) is unaffected |
| Camera-capability certification screen, override workflow, re-issue cycle | Requirement retained (§3) as an inline state on Live View, not as a separate screen |
| Audit log, authority records, people & roles management | Governance tooling for a permanent deployment, not a demo requirement |
| Measurement dashboard, system-health dashboard | Same |

If IBVAP is developed past this MVP, these are the first items to revisit —
deferred, not disproven.

---

## 5. Acceptance criteria

| # | Criterion |
|---|---|
| **AC-1** | Two cameras ingest unmodified, including at least one analog channel behind the existing DVR. |
| **AC-2** | Each of the eight named capabilities fires at least once, correctly, on a camera that supports it. |
| **AC-3** | At least one capability is refused, inline, with a plain-language reason, on a camera that cannot support it. |
| **AC-4** | A rule (line or zone) is authored, fires, and produces exactly one Event, plus one Alert if the rule is alerting. |
| **AC-5** | An alert is assessed in one action; a not-real assessment offers a mute, and the mute suppresses the next repeat. |
| **AC-6** | The event feed reaches a real external destination via Integration. |
| **AC-7** | Detection, logging and alerting continue with no screen open. |

---

## 6. Known limitations

| Limitation | Detail |
|---|---|
| Detection accuracy | Depends on camera resolution, mounting angle and distance. Measured and stated, not corrected. |
| Night-time detection | IR-illuminated, effectively monochrome. No colour-dependent claim is made after dark. |
| "Suspicious activity" | No agreed definition exists in `problem.md` or the research corpus. Defined per-deployment by a human as a rule, not inferred by the product. |
| Command-and-control integration | No adapter to a named system ships. Integration publishes a documented event feed; the receiving system is out of scope. |

---

## 7. Document status

**Stage:** 02 — Product Definition. **Status:** frozen, five-screen scope.

**Supersedes** the prior 27-screen version of this document (Camera Spec
Sheet as a dedicated screen, Case/evidence artefacts, recognition matching,
audit/authority/roles, measurement/health dashboards), per **D-15**
(2026-08-26, [decisions.md](../00-project/decisions.md)). The prior version
and the D-1…D-14 reasoning that preceded the cut remain in git history and in
the decisions log.

**Derived from:** [problem.md](../00-project/problem.md) (immutable),
[PRD.md](PRD.md), [decisions.md](../00-project/decisions.md) D-1…D-15.

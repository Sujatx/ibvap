<div align="center">

# IBVAP

### Intelligent Border Video Analytics Platform

Smart India Hackathon 2026 · Problem Statement ID **26187**

</div>

---

## 1. Description

IBVAP is an AI-driven software platform that turns **existing IP-based CCTV
infrastructure** at Border Out Posts (BOPs), check posts, and border roads into
an intelligent surveillance network — **without requiring dedicated FRS, ANPR,
or smart-camera hardware** — by running real-time video analytics on top of
the cameras a border force already owns.

This repository currently holds completed **research** and **product
definition** work, plus the development CCTV rig used to validate it against
real hardware. Engineering has not started.

## 2. Problem

Conventional CCTV at border posts provides only recording and live viewing,
which requires continuous human observation to be useful. Advanced
functionality — facial recognition, ANPR, intrusion detection, object tracking
— is normally sold as specialized, proprietary hardware. That makes it
expensive and hard to deploy at scale, especially at remote, low-connectivity,
low-staffed border locations.

The result: a force can own hundreds of cameras and still have no reliable way
to know what any one of them is watching, or whether it is even capable of
telling them anything useful.

## 3. Solution

IBVAP ingests live video from cameras a force already has — native IP cameras
over RTSP/ONVIF, and analog channels behind an existing DVR/XVR/NVR — and runs
AI/computer-vision analytics on that video in software, read-only against the
existing estate.

Before running any analytic, IBVAP measures what each camera can actually
support (resolution, frame rate, day/night behaviour) and issues a per-camera,
per-capability verdict: eligible, eligible-but-degraded, or not eligible. A
capability the camera cannot support is **refused, not silently degraded** —
IBVAP does not claim what it cannot measure.

Firings are turned into logged **Events**, a subset of which become **Alerts**
routed to a human for a one-tap real / not real / unsure assessment. Events
can also be emitted outward over a documented, generic event contract for
integration with an external command-and-control system.

IBVAP does not replace an existing VMS or recorder, does not act as the sole
basis for a decision, and does not claim to detect contraband, currency, or
trafficking — only the people, vehicles, faces, plates, movement, and timing
that its analytics primitives actually produce.

## 4. Core capabilities

All eight capabilities named by the problem statement are addressed. Each
ships at a declared maturity, gated per camera against what that camera can
actually measure — none is delivered as an unqualified, universal claim.

| Capability | MVP grade | Key condition |
|---|---|---|
| Human detection and tracking | Support | Single-camera tracking only; needs ≥3 analysed fps |
| Vehicle detection and classification | Support | Coarse type only (car/truck/bus/motorcycle/bicycle) — no make/model/colour |
| Face detection | Support, conditional | Ships unconditionally; many overview-mounted cameras will be marked not eligible |
| Facial recognition (matching against a watchlist) | Not in MVP | Detection ships; matching a detected face against a gallery is cut (D-15) — it needs a legal-authority workflow this build doesn't carry |
| Automatic Number Plate Recognition (ANPR) | Conditional | Lane-/gate-aimed cameras only, within a stated speed and mounting-angle envelope |
| Virtual fence intrusion detection | Support | Rule engine over zones/lines/direction/dwell |
| Suspicious activity detection | Support, rule-based only | Operator-authored composite rules over reliable primitives; no learned anomaly model in MVP |
| Night-time movement detection | Support | Detection continues after dark; a day/night state on the live view, not a separate mode |
| Real-time alerts and event logging | Primary-candidate | The product's spine: a rule firing always writes an Event; an alerting rule also raises an Alert |

No capability here is presented as working on every camera. If a specific
camera can't reliably support a class, that's stated inline, right where the
detection would have appeared — not hidden.

## 5. MVP

Per **[ADR 0016](docs/adr/0016-mvp-ui-cut-to-five-screens.md)**, the MVP is deliberately five
screens — exactly what the problem statement names, built as a finished
product, nothing built around it:

| Screen | Answers |
|---|---|
| **Sign in** | Who's using this right now? |
| **Live View** *(home)* | What is the camera seeing, right now? — human/vehicle/face/plate detection, night-time movement |
| **Rules** | What should this camera watch for? — virtual fence, suspicious activity |
| **Alerts & Events** | What happened, and what needs me? — real-time alerting, event logging |
| **Integration** | How does this reach our other systems? |

Case management, evidence chain-of-custody export, watchlist face-matching,
and the audit/authority/roles/measurement/health governance layer are cut
entirely for this MVP — not simplified, not hidden inside another screen.
They're real needs for a permanently deployed force, not what a five-screen
demo needs to show; see [ADR 0016](docs/adr/0016-mvp-ui-cut-to-five-screens.md) for the full
reasoning and [PRD.md §6](docs/02-product/PRD.md) for what's kept.

The MVP is developed and validated against the development CCTV rig in this
repository (see [§9](#9-development-cctv-environment)) — that rig is not
claimed to represent any real border camera estate.

## 6. How it works

```mermaid
flowchart LR
    A[Existing CCTV / DVR] --> B[Live View — AI detection]
    B --> C[Rules]
    C --> D[Event]
    D --> E[Alert]
    E --> F[Assessment]
    F --> G[Integration]
```

## 7. Project status

| Stage | Status |
|---|---|
| Research | ✓ Complete |
| Product Discovery | ✓ Complete |
| PRD | ✓ Complete |
| Decisions (ADR 0001 – 0029) | ✓ Accepted |
| MVP scope | ✓ Frozen — five screens (ADR 0016) |
| UX / Product Design | → Proposed, pending approval |
| Architecture | ○ Not started |
| Engineering | ○ Not started |

## 8. Documentation

| | Document |
|---|---|
| Project instructions | [CLAUDE.md](CLAUDE.md) |

**Project**

| Document | Description |
|---|---|
| [Problem Statement](docs/00-project/problem.md) | Official, immutable SIH problem statement |
| [Vision and Scope](docs/00-project/vision-and-scope.md) | Vision statement plus required capabilities, outcomes and constraints, per the problem statement |
| [Decisions](docs/adr/README.md) | Architecture Decision Records, one file per decision (ADR 0001 – 0029) |

**Research**

| Document | Description |
|---|---|
| [Domain Research](docs/01-research/domain/domain-research.md) | Border-surveillance domain research |
| [SSB Operational Context](docs/01-research/domain/ssb-operational-context.md) | SSB-specific operational context |
| [SSB Operational Workflow](docs/01-research/domain/ssb-operational-workflow.md) | SSB-specific workflow research |
| [Product Discovery](docs/01-research/users/product-discovery.md) | User and needs research |
| [Competitive Landscape](docs/01-research/competitors/competitive-landscape.md) | Competitor and market research |
| [Technical Feasibility](docs/01-research/technology/technical-feasibility.md) | Technical feasibility research |

**Product**

| Document | Description |
|---|---|
| [PRD](docs/02-product/PRD.md) | Product Requirements Document, including MVP scope (§6) — five screens, frozen per D-15 |

**Design**

| Document | Description |
|---|---|
| [UX Definition](docs/03-design/UX.md) | Five screens, their states, and what they must never say — for the frozen five-screen MVP |

## 9. Development CCTV environment

This repository includes an existing home CCTV/DVR setup (`dvr.py`, `dvr.env`,
`backups/`, `requirements.txt`) that serves as the development and validation
environment for IBVAP — a real analog XVR with real firmware and bandwidth
constraints, used to test IBVAP against real-world legacy CCTV/DVR behaviour
rather than assumed behaviour.

This setup is preserved as-is and is not part of the IBVAP product. Connection
details, credentials, and network configuration for this rig are kept out of
version control and are not documented here.

## 10. Repository structure

```
ibvap-surveillance/
├── CLAUDE.md                 project & workflow rules
├── README.md
├── dvr.py                    development CCTV/DVR access (preserved, not IBVAP)
├── dvr.env                   development CCTV credentials (gitignored)
├── requirements.txt          dvr.py dependencies
├── backups/                  original DVR encoder config
└── docs/
    ├── 00-project/           problem statement, vision, goals
    ├── 01-research/          domain, users, competitors, technology research
    ├── 02-product/           PRD, incl. frozen MVP scope
    ├── 03-design/            UX definition
    └── adr/                  decision records, one file per decision
```

## 11. Development methodology

```
Research → Product → Design → Architecture → Engineering → Testing → Demo
```

Each stage lives in its own `docs/` folder and is not mixed with another. A
stage does not begin before the stage(s) before it are complete for the
relevant feature or decision.

## 12. Scope

The SIH problem statement and Sashastra Seema Bal (SSB) research define the
**initial validation context** for SIH 2026 — they do not define the product's
market boundary. **IBVAP is not India-specific.** Requirements throughout the
documentation are distinguished as SIH/SSB-specific, border-security-specific,
globally applicable, or market-specific.

## 13. Disclaimer

IBVAP is a Smart India Hackathon 2026 development project. It is not a
production deployment, and it is not an official SSB or Government of India
system.

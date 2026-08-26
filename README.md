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
routed to a human for assessment. Assessed events can be gathered into a
**Case** with an exportable evidence pack, and events can also be emitted
outward over a documented, generic event contract for integration with an
external command-and-control system.

IBVAP does not replace an existing VMS or recorder, does not act as the sole
basis for a decision, and does not claim to detect contraband, currency, or
trafficking — only the people, vehicles, faces, plates, movement, and timing
that its analytics primitives actually produce.

## 4. Core capabilities

All eight capabilities named by the problem statement are addressed. Each
ships at a declared maturity, gated by the per-camera Camera Spec Sheet verdict
— none is delivered as an unqualified, universal claim.

| Capability | MVP grade | Key condition |
|---|---|---|
| Human detection and tracking | Support | Single-camera tracking only; needs ≥3 analysed fps |
| Vehicle detection and classification | Support | Coarse type only (car/truck/bus/motorcycle/bicycle) — no make/model/colour |
| Face detection | Support, conditional | Ships unconditionally; many overview-mounted cameras will be marked not eligible |
| Facial recognition | Gated, conditional, watchlist-only | Demonstrable in a controlled dev/test environment; technically blocked on a real deployment unless a legal basis, authority record, bounded gallery, and retention rules are all configured |
| Automatic Number Plate Recognition (ANPR) | Conditional | Lane-/gate-aimed cameras only, within a stated speed and mounting-angle envelope |
| Virtual fence intrusion detection | Support | Rule engine over zones/lines/direction/dwell; measured nuisance rate published per camera |
| Suspicious activity detection | Support, rule-based only | Operator-authored composite rules over reliable primitives; no learned anomaly model in MVP |
| Night-time movement detection | Support | Separate night eligibility verdict per camera; day-vs-night gap measured and disclosed, not assumed |
| Real-time alerts and event logging | Primary-candidate | The product's spine: append-only hash-chained event log, payload-progressive alerts |

No capability here is presented as working on every camera. Eligibility is
measured per camera by the Camera Spec Sheet, and a capability is refused on a
camera that cannot support it.

## 5. MVP

The MVP is one deployment site, complete end-to-end: a single site's existing
cameras, unmodified, running the full loop from ingest to an outbound event —
locally and unattended, with no remote control room required.

- **Camera Spec Sheet** — measures each camera and issues an eligibility verdict
  per analytic, with the reason in plain language.
- **Analytics primitives** — person, vehicle, face, and plate detection on
  eligible cameras only.
- **Rules → Event → Alert → Assessment → Case** — every firing is logged; a
  subset alert a human; a human assesses and can open a case with an
  exportable evidence pack.
- **Site resilience** — local operation continues for ≥72 hours with no
  uplink; no licence or capability expires because a server is unreachable.
- **Egress** — a published, versioned event schema plus a generic outbound
  mechanism, demonstrated against at least one real external consumer.

The MVP is developed and validated against the development CCTV rig in this
repository (see [§9](#9-development-cctv-environment)) — that rig is not
claimed to represent any real border camera estate.

## 6. How it works

```mermaid
flowchart LR
    A[Existing CCTV / DVR] --> B[Video Ingestion]
    B --> C[Camera Spec Sheet]
    C --> D[AI Analytics]
    D --> E[Rules]
    E --> F[Event]
    F --> G[Alert]
    G --> H[Assessment]
    H --> I[Case / Evidence]
    I --> J[External Integration]
```

## 7. Project status

| Stage | Status |
|---|---|
| Research | ✓ Complete |
| Product Discovery | ✓ Complete |
| PRD | ✓ Complete |
| Product decisions D-1 – D-14 | ✓ Approved |
| MVP scope | ✓ Frozen |
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
| [Vision](docs/00-project/vision.md) | Vision statement derived from the problem statement |
| [Goals](docs/00-project/goals.md) | Required capabilities and outcomes per the problem statement |
| [Decisions](docs/00-project/decisions.md) | Project-level decisions log (D-1 – D-14) |

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
| [PRD](docs/02-product/PRD.md) | Product Requirements Document |
| [MVP](docs/02-product/MVP.md) | Frozen MVP scope |

**Design**

| Document | Description |
|---|---|
| [UX Definition](docs/03-design/UX.md) | Information architecture, screens, navigation, journeys and states for the frozen MVP |

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
    ├── 00-project/           problem statement, vision, goals, decisions
    ├── 01-research/          domain, users, competitors, technology research
    ├── 02-product/           PRD, MVP scope freeze
    └── 03-design/            UX definition
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

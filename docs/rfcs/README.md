# RFCs (Design Docs)

This is the index of IBVAP's design docs — the layer between a defined
product requirement and code, where a non-trivial implementation is worked
out and reviewed before it's built. Per
[CLAUDE.md](../../CLAUDE.md), any non-trivial implementation gets one here,
reviewed, before code — the same way an ADR records a decision already made,
an RFC proposes one that isn't made yet.

## Contents

- [Index](#index)
- [Template](#template)
- [Status values](#status-values)

## Index

| # | Title | Status |
|---|---|---|
| [0001](0001-video-ingest-capability-measurement-and-playback.md) | Video ingest, capability measurement, and playback retrieval | Accepted |
| [0002](0002-rule-evaluation-engine.md) | Rule evaluation engine | Accepted |
| [0003](0003-event-store-and-alert-state.md) | Event store and alert state pipeline | Accepted |
| [0004](0004-web-application-and-api-contracts.md) | Web application and API contracts | Accepted |
| [0005](0005-c2-event-egress-publisher.md) | Generic C2 event egress publisher | Accepted |
| [0006](0006-detection-and-analytics-primitives.md) | Detection and analytics primitives | Accepted |

Six, not the five the [roadmap](../../ROADMAP.md) originally named: the model
primitives were split out of 0001, which otherwise carried ingest, capability
measurement, inference placement, playback retrieval *and* every detection
model.

Decode throughput and the recorded-playback route are established per
deployment, at commissioning, rather than as one-time measurements this
document blocks on — see RFC 0001's Decode throughput and Recorded-video
retrieval sections.

## Template

Copy this structure for a new RFC. File name:
`NNNN-short-kebab-case-title.md`.

```markdown
# NNNN. Title

**Status:** Draft
**Author:**
**Date:**

## Context and scope

## Goals and non-goals

## Design

## System-context diagram

## APIs

## Data storage

## Alternatives considered

## Cross-cutting concerns
```

## Status values

| Status | Meaning |
|---|---|
| Draft | Under review, not yet a commitment |
| Accepted | Reviewed and approved — implementation may proceed |
| Superseded by NNNN | Replaced by a later RFC |
| Withdrawn | Dropped without being implemented |

A decision made *during* an RFC's review that's worth recording independently
(e.g. "we chose X over Y") gets its own file in [docs/adr/](../adr/README.md),
same as any other decision — the RFC is the design, the ADR is the choice.

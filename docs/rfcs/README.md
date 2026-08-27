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
| [0001](0001-video-ingest-and-analytics-pipeline.md) | Video ingest and analytics pipeline | Draft |

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

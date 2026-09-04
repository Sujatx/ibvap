# IBVAP System Design Document

This is a System Design Document (SDS) for IBVAP, synthesised from the six
accepted RFCs in [docs/rfcs/](../../rfcs/README.md) and the supporting ADRs in
[docs/adr/](../../adr/README.md). It organises what those documents already
decided into the sections a reviewer expects from a design document —
overview, architecture, data model, interfaces, security, integration,
deployment, quality attributes and open risks — following the structure common
to IEEE 1016-style software design descriptions and the arc42 template
[docs/architecture/README.md](../README.md) already uses at the whole-system
level.

**This set is a derivative, not a second source of truth.** Every RFC and ADR
cited remains authoritative for exact wire formats, SQL DDL and JSON examples;
where this document summarises a table or an endpoint list, the summary is
scoped to stay accurate to the cited section, not to replace it. If an RFC
changes, the file here that cites it needs re-checking against the new text —
this is a regenerated view, not a hand-maintained parallel spec.

No application code is written or implied here. Interface signatures shown are
design contracts (the same ones the RFCs already fixed), not implementations.

## Contents

| File | Covers | Primary sources |
|---|---|---|
| [01-system-overview.md](01-system-overview.md) | Purpose, scope, actors, system context, document map | `docs/problem-statement.md`, all six RFCs |
| [02-architecture-overview.md](02-architecture-overview.md) | Building blocks, module boundaries, technology stack | RFC 0001, 0006, ADR 0032–0035, 0050, 0054 |
| [03-data-model.md](03-data-model.md) | Entities, relationships, retention | RFC 0003 |
| [04-api-contracts.md](04-api-contracts.md) | REST endpoints, `/ws/live` protocol, conventions | RFC 0004 |
| [05-core-components-and-pipeline.md](05-core-components-and-pipeline.md) | Ingest lifecycle, detection cascade, rule evaluation, the event pipeline end to end | RFC 0001, 0002, 0006 |
| [06-security-and-auth.md](06-security-and-auth.md) | Authentication, authorisation, credentials, transport security, privacy and biometric governance | RFC 0004, 0006, ADR 0007, 0008, 0059 |
| [07-integration-and-egress.md](07-integration-and-egress.md) | The C2 event contract, transports, delivery guarantees | RFC 0005, ADR 0006, 0020 |
| [08-deployment-and-infrastructure.md](08-deployment-and-infrastructure.md) | Deployment topology, process model, offline behaviour, supervision | RFC 0001, 0003, ADR 0033, 0050, 0054 |
| [09-non-functional-requirements.md](09-non-functional-requirements.md) | Performance budget, availability, scalability boundary, observability | RFC 0001, 0003, 0005, 0006 |
| [10-risks-and-open-items.md](10-risks-and-open-items.md) | What is decided as a per-deployment fact, what is deferred, what is genuinely open | All six RFCs, `docs/architecture/README.md` §11 |

## How this maps to a standard SDD

| Standard SDD section | Here |
|---|---|
| Introduction / Scope | 01 |
| Architectural Design | 02 |
| Data Design | 03 |
| Interface Design | 04 |
| Component / Detailed Design | 05 |
| Security Design | 06 |
| External Interface / Integration Design | 07 |
| Deployment Design | 08 |
| Quality Attributes (NFRs) | 09 |
| Risks, Assumptions, Open Issues | 10 |

## Relationship to the rest of the architecture documentation

[docs/architecture/README.md](../README.md) is the arc42 description of the
whole system and stays the place decisions are indexed against product
constraints. This directory exists alongside it as a fuller, presentation- and
review-ready expansion of the same accepted design — for someone who needs the
data model or the API surface in one place rather than assembled from six RFCs.
Where the two overlap, the RFC is authoritative; both link to it rather than to
each other.

## What is not here

Diagrams beyond the Mermaid figures embedded in these files are tracked as
owed work in [10-risks-and-open-items.md](10-risks-and-open-items.md) — they
are not
fabricated here to make this set look more finished than the underlying RFCs
are. Product requirements and success criteria stay in the
[Notion PRD](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204)
per [CLAUDE.md](../../../CLAUDE.md) §2 and are referenced, not restated.

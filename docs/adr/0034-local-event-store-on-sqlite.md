# 34. The local event store is SQLite, and the egress queue lives in it

**Date:** 2026-09-01
**Status:** Accepted

## Context

Events are the product's spine — a rule firing always writes one, and an
alerting rule also raises an Alert. Everything the operator ever sees on
Alerts & Events, every assessment recorded against one, every suppression
under [ADR 0027](0027-suppression-works-like-notification-snooze.md), and
every payload leaving for a command-and-control system under
[ADR 0006](0006-c2-integration-via-generic-event-contract.md) passes through
whatever stores them. [docs/architecture/README.md](../architecture/README.md)
§8 lists the storage engine as open.

Two constraints shape it more than the query patterns do. The site must run
disconnected for at least 72 hours with no data loss on reconnect, and it must
do so unattended, with no engineer and possibly no reliable power. That makes
the store's most important property durability under sudden loss, not
throughput.

The [technical feasibility research](https://app.notion.com/p/3c986dda46e281a7a1c3d87623970822?pvs=204)
(Notion) sizes what is actually being stored, and the numbers span six orders
of magnitude: a fifteen-second 1080p clip is about 7.5 MB, a full-frame
snapshot about 250 KB, a 320×320 object crop about 25 KB, and a discrete event
record about 1 KB — twenty of which a camera might produce in a day. Per-frame
object metadata, if kept, is a different animal again at roughly 138 MB per
camera per day. Treating those as one class of thing with one retention clock
would be a design error rather than a simplification.

## Decision

**SQLite in WAL mode, through SQLAlchemy 2.0, with Alembic migrations from
the first schema.** Four people changing a schema in parallel need migrations
before they need anything else; retrofitting them after divergence is a bad
week.

**DuckDB is rejected.** It is an excellent analytical engine with a
single-writer model, and this workload is not analytical: small frequent
writes from the rule engine, point reads and short range scans from the API,
concurrent with ingest. That is SQLite's shape. WAL mode is what makes the
concurrent-reader-during-write case work, and it is also what makes an
unexpected power loss survivable, which matters more here than any query
benchmark.

**Binary artefacts live on the filesystem; the database holds their paths,
sizes and hashes.** A 7.5 MB clip does not belong in a column.

**The egress queue is a table in the same database as the events it
publishes.** Writing an event and enqueuing it for a command-and-control
system is then one transaction, and the 72-hour disconnection reconciles on
reconnect without loss or duplication. Every event carries a monotonically
increasing identifier and an idempotency key, so a consumer that sees the
same event twice can say so.

**The queue is bounded and its discard policy is stated rather than left to
whoever writes the code.** At a site offline for days the queue will fill.
When it does, the oldest non-alerting Events are dropped first and the fact of
the drop is itself recorded — a gap the operator can see beats a silent one.

**Retention is per artefact class, with a separate clock for each** —
continuous video, event clips, crops, per-frame metadata and the event records
themselves. The actual periods are a product question, not this decision.

**Every event stores the capture time and a flag recording whether the clock
was trustworthy when it was taken.** A site that reboots with a wrong clock
produces evidence with a wrong time and fails silently, which is the worst
version of that problem. The flag is the mechanism behind the time-integrity
marking the PRD already requires.

## Consequences

Choosing SQLite means the store scales with the site, not with the estate. A
single Border Out Post with a handful of cameras is comfortably inside it. An
aggregation tier across many sites would not be, and would need a different
engine — that is a real boundary, and worth stating now so nobody discovers it
by trying.

SQLAlchemy costs an abstraction layer over a database this project has no
intention of changing. It buys migrations, typed models that line up with the
Pydantic contract from
[ADR 0033](0033-backend-framework-packaging-and-auth.md), and a test suite
that can run against a temporary database without ceremony. That trade is
worth making once, at the start.

Putting the egress queue in the same database ties the publisher's
availability to the store's. That is the intended direction of the coupling:
an event that was written but not queued is a lost event, and there is no
configuration in which that is acceptable.

Storing artefacts on the filesystem means the database and the disk can
disagree — an orphaned file, or a row pointing at a file a retention sweep
already removed. Reconciliation is now a real background job that has to
exist, not an implementation detail.

Hashing at capture rather than at export is what makes the hash meaningful,
and it only works because
[ADR 0032](0032-inference-runtime-decode-path-and-detector-licence.md) cuts
clips at I-frame boundaries without re-encoding. Re-encode anywhere in that
path and the hash stops describing the stored bytes.

[docs/architecture/README.md](../architecture/README.md) §8 no longer lists
the storage engine as open.

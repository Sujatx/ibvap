# 0003. Event store and alert state pipeline

**Status:** Accepted
**Author:** Sujat
**Date:** 2026-09-03

## Context and scope

[ADR 0034](../adr/0034-local-event-store-on-sqlite.md) chose SQLite in WAL mode
through SQLAlchemy 2.0 with Alembic migrations, put the egress queue in the same
database as the events it publishes, and named four obligations without
discharging them: a bounded queue with a stated discard policy, retention per
artefact class with a separate clock for each, a clock-trust flag on every event,
and a reconciliation job for the disagreement between the database and the disk.

This RFC discharges them, and adds the schema the whole platform writes to and
reads from. It also settles a debt
[ADR 0046](../adr/0046-timeline-markers-carry-class-colour.md) explicitly left
here: every timeline marker now carries a detection class, so the store has to
say what an event with more than one class — or none — gets.

Everything upstream of the write is
[RFC 0002](0002-rule-evaluation-engine.md)'s. Everything downstream of the queue
is [RFC 0005](0005-c2-event-egress-publisher.md)'s. The HTTP surface over this
data is [RFC 0004](0004-web-application-and-api-contracts.md)'s.

## Goals and non-goals

**Goals**

1. A complete schema — tables, types, indexes, constraints — and the first
   Alembic migration.
2. The alert state machine, including assessment, impact grade, mute and the
   dismissal cause, matching what the hi-fi S-04 frames actually do.
3. A bounded egress queue whose discard policy is written down and whose
   discards are visible.
4. Retention with a separate clock per artefact class, and the sweep that
   enforces it.
5. A rule for `primary_class` that always resolves to exactly one of the four
   colour tokens.
6. Database-to-disk reconciliation.

**Non-goals**

- Case management, evidence export, watchlists, audit-log and people-and-roles
  screens, and the measurement dashboard. All cut by
  [ADR 0016](../adr/0016-mvp-ui-cut-to-five-screens.md). Tables are not created
  speculatively for them.
- Multi-site aggregation. ADR 0034 states the boundary: this store scales with
  the site, not with the estate, and an aggregation tier would need a different
  engine.
- Continuous video recording. IBVAP is read-only against the estate; the
  recorder keeps continuous video under its own retention, which IBVAP neither
  controls nor extends.

## Design

### Engine configuration

```sql
PRAGMA journal_mode = WAL;        -- concurrent readers during a write
PRAGMA synchronous = NORMAL;      -- WAL makes this durable enough for a power cut
PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = 5000;
PRAGMA wal_autocheckpoint = 1000;
```

`synchronous = NORMAL` under WAL survives an application crash always and a power
loss with at most the last transaction lost. `FULL` would close that gap at the
cost of an fsync per commit, on a workload that commits on every rule fire. The
trade is stated because a site with no reliable power is exactly where it gets
tested.

### Time and identity conventions

- Every timestamp is UTC, stored as an ISO-8601 string with a `Z` suffix so it
  sorts lexically and survives a `sqlite3` shell inspection.
- Every event carries `captured_at` (when the frame was captured, per RFC 0001)
  and `recorded_at` (when the row was written). They differ, and a large gap is
  itself diagnostic.
- `clock_trusted` accompanies `captured_at` everywhere it appears. It is set by
  ingest and never re-derived downstream.

### Schema

```sql
-- ---------- identity ----------

CREATE TABLE users (
    id              INTEGER PRIMARY KEY,
    username        TEXT    NOT NULL UNIQUE,
    password_hash   TEXT    NOT NULL,          -- Argon2id, ADR 0033
    can_reset       INTEGER NOT NULL DEFAULT 0,-- holds the local reset right
    state           TEXT    NOT NULL           -- 'active' | 'disabled' | 'expired'
                    CHECK (state IN ('active','disabled','expired')),
    failed_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until    TEXT,                      -- progressive self-clearing delay
    created_at      TEXT    NOT NULL,
    last_seen_at    TEXT
);

CREATE TABLE sessions (
    id              TEXT    PRIMARY KEY,       -- opaque, in the HTTP-only cookie
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at      TEXT    NOT NULL,
    expires_at      TEXT    NOT NULL,
    last_used_at    TEXT    NOT NULL
);
CREATE INDEX ix_sessions_user ON sessions(user_id);

-- ---------- estate ----------

CREATE TABLE recorders (
    id              INTEGER PRIMARY KEY,
    name            TEXT    NOT NULL,
    host            TEXT    NOT NULL,
    port            INTEGER NOT NULL DEFAULT 554,
    onvif_port      INTEGER,
    username        TEXT    NOT NULL,
    secret_ref      TEXT    NOT NULL,          -- indirection; no password column
    url_template    TEXT,                      -- vendor fallback, RFC 0001
    created_at      TEXT    NOT NULL
);

CREATE TABLE cameras (
    id                    INTEGER PRIMARY KEY,
    recorder_id           INTEGER NOT NULL REFERENCES recorders(id),
    channel               INTEGER NOT NULL,
    name                  TEXT    NOT NULL,
    stream_uri            TEXT,
    encoded_width         INTEGER,
    encoded_height        INTEGER,
    display_width         INTEGER,
    display_height        INTEGER,
    reference_distance_m  REAL,                -- commissioning input, RFC 0001
    scene_width_m         REAL,                -- commissioning input, RFC 0001
    connection_state      TEXT NOT NULL DEFAULT 'stopped',
    delivered_fps         REAL,
    analysed_fps          REAL,
    site_sketch_x         REAL,                -- normalised pin, ADR 0044
    site_sketch_y         REAL,
    site_sketch_facing    REAL,                -- degrees; the hand-drawn wedge
    created_at            TEXT    NOT NULL,
    UNIQUE (recorder_id, channel)
);

CREATE TABLE capability_verdicts (
    id                    INTEGER PRIMARY KEY,
    camera_id             INTEGER NOT NULL REFERENCES cameras(id) ON DELETE CASCADE,
    capability            TEXT    NOT NULL
                          CHECK (capability IN ('human_detect','vehicle_detect',
                                 'face_detect','face_recognize','anpr',
                                 'night_movement','recorded_playback')),
    illumination          TEXT    NOT NULL CHECK (illumination IN ('colour','infrared')),
    supported             INTEGER NOT NULL,
    reason                TEXT,                -- a full sentence when not supported
    px_per_m_at_reference REAL,
    delivered_fps         REAL,
    analysed_fps          REAL,
    measured_at           TEXT    NOT NULL,
    superseded_at         TEXT,                -- history, not overwrite
    overridden_by         TEXT,                -- named authority, ADR 0007
    overridden_at         TEXT,
    override_reason       TEXT
);
CREATE INDEX ix_verdict_current
    ON capability_verdicts(camera_id, capability, illumination)
    WHERE superseded_at IS NULL;

-- ---------- rules ----------

CREATE TABLE rules (
    id                 INTEGER PRIMARY KEY,
    camera_id          INTEGER NOT NULL REFERENCES cameras(id) ON DELETE CASCADE,
    name               TEXT    NOT NULL,
    enabled            INTEGER NOT NULL DEFAULT 1,
    current_version_id INTEGER,
    created_by         INTEGER NOT NULL REFERENCES users(id),
    created_at         TEXT    NOT NULL
);

CREATE TABLE rule_versions (
    id                    INTEGER PRIMARY KEY,
    rule_id               INTEGER NOT NULL REFERENCES rules(id) ON DELETE CASCADE,
    version               INTEGER NOT NULL,
    geometry              TEXT    NOT NULL,    -- JSON, normalised coordinates
    drawn_encoded_width   INTEGER NOT NULL,
    drawn_encoded_height  INTEGER NOT NULL,
    condition             TEXT    NOT NULL,    -- JSON condition tree, RFC 0002
    schedule              TEXT    NOT NULL,    -- JSON
    alerting              INTEGER NOT NULL,
    cooldown_seconds      REAL    NOT NULL DEFAULT 30,
    refused_reason        TEXT,
    created_by            INTEGER NOT NULL REFERENCES users(id),
    created_at            TEXT    NOT NULL,
    UNIQUE (rule_id, version)
);

-- ---------- events and alerts ----------

CREATE TABLE events (
    id              INTEGER PRIMARY KEY,        -- rowid: monotonic within the site
    camera_id       INTEGER NOT NULL REFERENCES cameras(id),
    rule_version_id INTEGER NOT NULL REFERENCES rule_versions(id),
    captured_at     TEXT    NOT NULL,
    recorded_at     TEXT    NOT NULL,
    clock_trusted   INTEGER NOT NULL,
    primary_class   TEXT    NOT NULL
                    CHECK (primary_class IN ('person','vehicle','face','plate')),
    class_mixed     INTEGER NOT NULL DEFAULT 0,
    alerting        INTEGER NOT NULL,
    illumination    TEXT    NOT NULL CHECK (illumination IN ('colour','infrared')),
    track_ids       TEXT    NOT NULL,           -- JSON array
    boxes           TEXT    NOT NULL,           -- JSON array of xyxy, encoded geometry
    plate_text      TEXT,
    plate_confidence REAL,
    plate_grammar_matched INTEGER,
    under_override  INTEGER NOT NULL DEFAULT 0, -- produced under an ADR 0007 override
    idempotency_key TEXT    NOT NULL UNIQUE
);
CREATE INDEX ix_events_time   ON events(captured_at DESC);
CREATE INDEX ix_events_camera ON events(camera_id, captured_at DESC);

CREATE TABLE alerts (
    id              INTEGER PRIMARY KEY,
    event_id        INTEGER NOT NULL UNIQUE REFERENCES events(id) ON DELETE CASCADE,
    raised_at       TEXT    NOT NULL,
    state           TEXT    NOT NULL DEFAULT 'new'
                    CHECK (state IN ('new','assessed')),
    impact_grade    TEXT                         -- operator-assigned only, ADR 0018
                    CHECK (impact_grade IS NULL OR
                           impact_grade IN ('low','medium','high'))
);
CREATE INDEX ix_alerts_state ON alerts(state, raised_at DESC);

CREATE TABLE assessments (
    id              INTEGER PRIMARY KEY,
    alert_id        INTEGER NOT NULL REFERENCES alerts(id) ON DELETE CASCADE,
    verdict         TEXT    NOT NULL
                    CHECK (verdict IN ('real','not_real','unsure')),
    assessed_by     INTEGER NOT NULL REFERENCES users(id),
    assessed_at     TEXT    NOT NULL
);
CREATE INDEX ix_assessments_alert ON assessments(alert_id, assessed_at DESC);

CREATE TABLE mutes (
    id              INTEGER PRIMARY KEY,
    camera_id       INTEGER NOT NULL REFERENCES cameras(id) ON DELETE CASCADE,
    rule_id         INTEGER NOT NULL REFERENCES rules(id) ON DELETE CASCADE,
    started_at      TEXT    NOT NULL,
    ends_at         TEXT,                        -- NULL = until turned off
    ended_at        TEXT,                        -- set when reversed early
    dismissal_cause TEXT                         -- captured here, ADR 0023
                    CHECK (dismissal_cause IS NULL OR dismissal_cause IN
                           ('wind','animal','shadow','glare','rain','other','unknown')),
    suppressed_count INTEGER NOT NULL DEFAULT 0,
    created_by      INTEGER NOT NULL REFERENCES users(id),
    UNIQUE (camera_id, rule_id, started_at)
);
CREATE INDEX ix_mutes_active ON mutes(camera_id, rule_id) WHERE ended_at IS NULL;

-- ---------- artefacts ----------

CREATE TABLE artefacts (
    id              INTEGER PRIMARY KEY,
    event_id        INTEGER REFERENCES events(id) ON DELETE SET NULL,
    kind            TEXT    NOT NULL
                    CHECK (kind IN ('clip','crop','snapshot','frame_metadata')),
    path            TEXT    NOT NULL UNIQUE,
    bytes           INTEGER NOT NULL,
    sha256          TEXT    NOT NULL,            -- taken at capture, ADR 0034
    created_at      TEXT    NOT NULL,
    expires_at      TEXT    NOT NULL,            -- per-class clock, set on write
    missing_since   TEXT                         -- set by reconciliation
);
CREATE INDEX ix_artefacts_expiry ON artefacts(expires_at) WHERE missing_since IS NULL;
CREATE INDEX ix_artefacts_event  ON artefacts(event_id);

-- ---------- egress ----------

CREATE TABLE egress_endpoints (
    id              INTEGER PRIMARY KEY,
    kind            TEXT    NOT NULL CHECK (kind IN ('webhook','mqtt')),
    url             TEXT    NOT NULL,
    topic           TEXT,                        -- MQTT only
    secret_ref      TEXT,                        -- HMAC key indirection
    enabled         INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT    NOT NULL
);

CREATE TABLE egress_queue (
    sequence        INTEGER PRIMARY KEY AUTOINCREMENT,  -- monotonic, never reused
    event_id        INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    endpoint_id     INTEGER NOT NULL REFERENCES egress_endpoints(id) ON DELETE CASCADE,
    idempotency_key TEXT    NOT NULL,
    state           TEXT    NOT NULL DEFAULT 'pending'
                    CHECK (state IN ('pending','in_flight','delivered','dead')),
    attempts        INTEGER NOT NULL DEFAULT 0,
    next_attempt_at TEXT    NOT NULL,
    last_error      TEXT,
    enqueued_at     TEXT    NOT NULL,
    UNIQUE (event_id, endpoint_id)
);
CREATE INDEX ix_queue_due ON egress_queue(state, next_attempt_at);

CREATE TABLE egress_deliveries (
    id              INTEGER PRIMARY KEY,
    sequence        INTEGER NOT NULL REFERENCES egress_queue(sequence) ON DELETE CASCADE,
    attempted_at    TEXT    NOT NULL,
    outcome         TEXT    NOT NULL
                    CHECK (outcome IN ('accepted','rejected','unreachable','timeout')),
    status_code     INTEGER,
    detail          TEXT
);
CREATE INDEX ix_deliveries_seq ON egress_deliveries(sequence, attempted_at DESC);

CREATE TABLE egress_drops (
    id              INTEGER PRIMARY KEY,
    dropped_at      TEXT    NOT NULL,
    from_sequence   INTEGER NOT NULL,
    to_sequence     INTEGER NOT NULL,
    count           INTEGER NOT NULL,
    reason          TEXT    NOT NULL             -- 'queue_bound'
);

-- ---------- watchlist (ADR 0059; inert until watchlist_config.enabled) ----------

CREATE TABLE watchlist_config (
    id                INTEGER PRIMARY KEY CHECK (id = 1),  -- singleton row
    enabled           INTEGER NOT NULL DEFAULT 0,
    legal_basis_ref   TEXT,                        -- ADR 0008 condition 1
    authority_ref     TEXT,                        -- ADR 0008 condition 2 --
                                                     -- never treated as proof condition 1 holds
    retention_days    INTEGER,                     -- ADR 0008 condition 4
    configured_by     INTEGER REFERENCES users(id),
    configured_at     TEXT
);

CREATE TABLE watchlist_subjects (
    id              INTEGER PRIMARY KEY,
    label           TEXT    NOT NULL,              -- operator-assigned identifier
    notes           TEXT,
    created_by      INTEGER NOT NULL REFERENCES users(id),
    created_at      TEXT    NOT NULL,
    disabled_at     TEXT                            -- soft removal from the active gallery
);

CREATE TABLE watchlist_faces (
    id              INTEGER PRIMARY KEY,
    subject_id      INTEGER NOT NULL REFERENCES watchlist_subjects(id) ON DELETE CASCADE,
    artefact_id     INTEGER NOT NULL REFERENCES artefacts(id),  -- the enrolled reference photo
    embedding       BLOB    NOT NULL,               -- 128-d SFace feature vector
    created_at      TEXT    NOT NULL
);
CREATE INDEX ix_watchlist_faces_subject ON watchlist_faces(subject_id);

CREATE TABLE watchlist_matches (
    id              INTEGER PRIMARY KEY,
    event_id        INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    subject_id      INTEGER NOT NULL REFERENCES watchlist_subjects(id),
    similarity      REAL    NOT NULL,               -- cosine similarity at match time
    threshold_used  REAL    NOT NULL,               -- recorded, since the threshold can change
    matched_at      TEXT    NOT NULL
);
CREATE INDEX ix_watchlist_matches_event   ON watchlist_matches(event_id);
CREATE INDEX ix_watchlist_matches_subject ON watchlist_matches(subject_id, matched_at DESC);

-- ---------- settings ----------

CREATE TABLE settings (
    key             TEXT PRIMARY KEY,
    value           TEXT NOT NULL,
    updated_by      INTEGER REFERENCES users(id),
    updated_at      TEXT NOT NULL
);
```

The four `watchlist_config` columns are exactly ADR 0008's four conditions,
minus the gallery itself, which is `watchlist_subjects`/`watchlist_faces`
being non-empty and bounded. `enabled` is a fifth, separate field an
administrator sets deliberately — populating the other four is not itself
enough, because ADR 0008 is explicit that an authority record's existence is
never treated as evidence that the legal basis it names is valid. Until
`enabled` is true, [RFC 0006](0006-detection-and-analytics-primitives.md)
never loads the recognition model and no row is ever written to
`watchlist_matches`.

A match does not get its own class. `watchlist_matches.event_id` points at an
ordinary `events` row whose `primary_class` is `face`, the same as any other
face detection — the match is an attribute of that event, joined in, not a
different kind of event.

No password column exists anywhere except `users.password_hash`. Recorder and
HMAC secrets are held behind a `secret_ref` indirection so a database file copied
off the machine for debugging does not carry the estate's credentials with it.

### `primary_class` — settling the ADR 0046 debt

ADR 0046 made timeline markers carry the detection class, using the same four
`DetectionBox` tokens, and noted that the store must decide what a mixed or
classless event gets. It gets this:

> An Event stores exactly one `primary_class`: the class of the highest-confidence
> track that satisfied the rule. Where other classes were also present, the
> boolean `class_mixed` records that fact, and is not drawn.

Three consequences, all intended. A marker always resolves to one of the four
existing tokens, so no fifth colour is invented and the palette stays as ADR 0030
defined it. `class_mixed` is available to a detail panel that wants to say "and a
vehicle was also present" in words, which is where a nuance like that belongs.
And a `movement`-only rule — MOG2 fired, the detector classified nothing — cannot
occur, because a movement primitive is evaluated against a class filter and the
rule's declared class is what the event records.

The determinism matters: "highest-confidence track that satisfied the rule" is a
rule, not a heuristic, so the same event replayed produces the same colour.

### Alert state machine

```
                    ┌──────────────────────────────────┐
   rule fires  →  Event (always written)               │
                    │                                  │
              alerting rule?                           │
                    │ yes                              │ no
              mute active? ── yes ──▶ Event only,      │
                    │ no              suppressed_count │
                    ▼                 incremented      │
                  Alert: new ◀────────────────────────-┘
                    │
              operator assesses
                    │
        ┌───────────┼────────────┐
      real       unsure      not real
        │           │             │
        │           │      mute offered ── declined ──┐
        │           │             │ accepted          │
        │           │      dismissal cause            │
        │           │      + snooze duration          │
        └───────────┴─────────────┴──────────────────-┘
                    ▼
              Alert: assessed
              impact grade optional, at any point
```

Notes that the diagram cannot carry:

- **An Alert is never deleted and never expires.** `assessed` is terminal for
  this build; there is no case, no close, no archive — ADR 0016 cut all three.
- **Assessment is append-only.** A changed mind writes a second `assessments`
  row; the latest wins for display, and the history stays. An assessment that
  can be silently edited is not a record of a judgement.
- **The impact grade lives on the alert, not the assessment**, is nullable, has
  no default, and is written only by a person. Nothing in the platform computes,
  suggests or infers it (ADR 0018).
- **The dismissal cause is on the mute, not the assessment** (ADR 0023). Deciding
  an alert was not real and deciding this camera-and-rule pair is noisy are two
  different judgements.
- **A mute never expires on its own** unless the operator chose a duration.
  `ends_at NULL` means until turned off, and both forms are reversible early by
  setting `ended_at` (ADR 0027).

### Retention

A separate clock per artefact class, with the period held in `settings` so a site
can change it without a migration. `expires_at` is computed once, at write time,
from the class's current period — so changing a period affects future artefacts
and leaves existing ones alone, which is what makes the change safe to make.

| Class | What it is | Default | Rationale |
|---|---|---|---|
| `clip` | ~15 s of original bitstream around the event, ≈ 7.5 MB | 30 days | The expensive one |
| `crop` | The detection region, ≈ 25 KB | 90 days | Cheap, and what the console shows first |
| `snapshot` | Full frame at the event, ≈ 250 KB | 90 days | |
| `frame_metadata` | Per-frame objects, ≈ 138 MB per camera per day | **off** | Largest, least read; opt-in only |
| Event rows | ≈ 1 KB each, ~20 per camera per day | 365 days | The audit record outlives its media |
| `watchlist_faces.embedding` | A 128-d biometric template per enrolled subject | `watchlist_config.retention_days` | Governed by ADR 0008's configured retention condition, not the class table above — there is no platform default, because there is no platform-wide legal basis to default it against |

Event rows outliving their artefacts is deliberate: an event whose clip has
expired still says that something happened, when, on which camera, under which
rule. Losing the row as well would turn a retention policy into a hole in the
log.

The sweep runs hourly: delete expired artefact files, then their rows, in that
order — a file deleted with its row still present is recoverable by
reconciliation, whereas a row deleted with the file still present is an orphan
nobody will ever find.

Continuous video is not in the table because IBVAP does not record it. The
recorder does, under its own retention, and the timeline's extent is therefore
whatever the recorder happens to still hold — which is why ADR 0038 has the
timeline draw its own edges rather than assert a window.

### Reconciliation

ADR 0034 names the disagreement between database and disk as a real background
job. It runs daily:

1. For each artefact row not already marked missing, check the file exists and
   its size matches. A row whose file has gone gets `missing_since` set — it is
   not deleted, because "this evidence existed and is now gone" is itself worth
   recording.
2. Walk the artefact directory for files with no row. A file older than the
   longest retention period with no row is an orphan and is deleted; a younger
   one is left alone, because it may belong to a transaction still in flight.

Hashes are not re-verified on every sweep — reading every clip daily is a lot of
disk for a check that only catches silent corruption. A hash is verified when an
artefact is served.

### The bounded egress queue

The queue is bounded at a configured row count, default 100,000 — at ~20 events
per camera per day across five cameras, roughly a thousand days of headroom, so
the bound exists for the pathological case rather than the normal one.

When a write would exceed the bound:

1. Delete the oldest `pending` rows whose event is **not** alerting, oldest
   first, until there is room.
2. If that is not enough, delete the oldest `pending` rows regardless, oldest
   first.
3. Record every deletion as a row in `egress_drops`, carrying the sequence range
   and the count.

Step 3 is the part that matters. A gap in the sequence numbers a consumer
receives is then explainable rather than mysterious, and the console can say "412
events were not delivered between these two times" instead of the operator
discovering it by counting. A gap the operator can see beats a silent one.

Deleting a queue row never deletes the Event. The record stays; only the
undelivered copy is dropped.

### Migrations

Alembic from the first schema, not retrofitted.
[ADR 0034](../adr/0034-local-event-store-on-sqlite.md) is explicit about why: four
people changing a schema in parallel need migrations before they need anything
else. Two rules follow from SQLite's limited `ALTER TABLE`:

- Every migration has a working `downgrade`, or says in a comment why it cannot.
- Column changes use the create-copy-swap batch pattern, which Alembic's
  `batch_alter_table` handles; the naming convention is set in `env.py` so
  constraints have deterministic names to reference.

## System-context diagram

Where this sits in the whole system: the
[container view](../architecture/diagrams/c4-l2-container.md).

The detailed diagrams for this RFC — the entity-relationship diagram, the alert and mute state machines, and the retention sweep — are still owed, and are tracked
as remaining Phase 3 work rather than assumed to exist.

## APIs

Internal. One function owns the write, because the transaction boundary is the
whole point of putting the queue in the same database:

```python
def record_match(match: RuleMatch, artefacts: list[PendingArtefact]) -> RecordResult:
    """Write an Event, its artefacts, any Alert, and one egress queue row per
    enabled endpoint -- in a single transaction.

    An event that was written but not queued is a lost event, and there is no
    configuration in which that is acceptable (ADR 0034).
    """
```

`RecordResult` carries the event id, whether an alert was raised or suppressed by
a mute, and the queue sequences allocated. The suppressed case increments
`mutes.suppressed_count`, which is what the console's always-visible mute banner
counts.

The REST and WebSocket shapes over these tables are RFC 0004's.

## Alternatives considered

**DuckDB.** Rejected by ADR 0034 before this RFC: a single-writer analytical
engine against a workload of small frequent writes concurrent with reads.

**A separate queue technology — Redis, a file-backed queue, SQLite in a second
file.** Rejected because all three break the one-transaction property. An event
written and then enqueued in a second store has a window in which a power loss
loses the delivery, and ADR 0034 is explicit that the coupling is intended.

**Blobs in the database.** Rejected: a 7.5 MB clip in a column bloats the file,
defeats WAL checkpointing, and makes a backup an all-or-nothing proposition.

**Overwriting capability verdicts instead of superseding them.** Rejected. A
refusal that changed after someone moved a camera is worth being able to see, and
the history costs a nullable column.

**Mutable assessments.** Rejected: append-only is what makes the record a record.

**A fifth, neutral marker colour for mixed-class events.** Rejected in favour of
`primary_class`, above — it would add a token ADR 0030's palette does not have,
to express a nuance that reads better as a sentence in the detail panel.

**Deleting the Event when its queue row is dropped.** Rejected outright. The
queue is a delivery mechanism; the Event is the record.

## Cross-cutting concerns

**Time integrity.** `clock_trusted` propagates from ingest to Event to the
timeline's unverified-clock band to the outbound payload. It is never recomputed,
because the only moment it can honestly be assessed is at capture.

**Attribution.** Every consequential row — rule version, assessment, mute,
override, settings change — carries the user who caused it and when. There is no
separate audit log to fall out of sync with the data.

**Durability under power loss.** WAL plus `synchronous = NORMAL` risks the last
transaction. The consequence is bounded and stated: at most one Event, which is
still visible as a gap in the recorder's own footage the operator can review.

**Backup.** A consistent copy is `VACUUM INTO` a second file, which works while
the application runs. The artefact directory copies alongside it. Nothing here
requires stopping the platform, which matters at a site with no engineer.

**Growth.** Event rows are ~1 KB and clips dominate. At five cameras the store is
comfortably inside SQLite for years. The boundary ADR 0034 names — an aggregation
tier across many sites — is unchanged by anything in this RFC.

**Concurrency.** One writer at a time is SQLite's model, and this workload has
one writer: the event writer. The API reads, the egress publisher reads and marks
rows, and WAL keeps both from blocking on the writer. `busy_timeout` covers the
brief overlap when the publisher updates a queue row while an event is being
written.

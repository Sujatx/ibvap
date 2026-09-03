# 0005. Generic C2 event egress publisher

**Status:** Accepted
**Author:** Sujat
**Date:** 2026-09-03

## Context and scope

[ADR 0006](../adr/0006-c2-integration-via-generic-event-contract.md) settles how
IBVAP integrates with a command-and-control system: not by writing an adapter for
a named product, but by publishing a generic, versioned event contract and
demonstrating it end to end against a real external consumer. No target C2 system
has been named, and designing for one that has not been named is how integration
work gets thrown away.

That decision leaves the contract itself unwritten. This RFC writes it — the
payload, its versioning rules, the two transports that carry it, the retry and
dead-letter behaviour, and what an operator sees on S-05 when it fails.

The queue this publisher drains is [RFC 0003](0003-event-store-and-alert-state.md)'s,
in the same SQLite database as the events, for the reason
[ADR 0034](../adr/0034-local-event-store-on-sqlite.md) gives: an event that was
written but not queued is a lost event.

## Goals and non-goals

**Goals**

1. A published, versioned payload with an exact JSON example and a Pydantic
   model that generates it.
2. Two transports — HTTP webhook and MQTT — covering push and pull consumers.
3. Delivery that survives 72 hours offline and reconciles on reconnect without
   loss or duplication.
4. A dead-letter state that says why, rather than a message that disappears.
5. The S-05 test-event flow, so integration is demonstrated rather than asserted.

**Non-goals**

- ONVIF Profile M over MQTT, and MISB ST 0903 VMTI in STANAG 4609. Both are named
  post-MVP by ADR 0006 and neither is prototyped here.
- A classification, ownership or release-filter field.
  [ADR 0020](../adr/0020-egress-classification-field-deferred.md) considered and
  deferred it until the deployment's data-classification policy is known. Its
  absence below is a decision, not an oversight.
- Inbound control. The C2 system receives events; it does not command IBVAP.
  Nothing here opens a path from outside the site into the platform.
- Guaranteed ordering across endpoints. Per endpoint, delivery is attempted in
  sequence order; a consumer that needs global ordering uses the sequence number.

## Design

### The payload: `ibvap.event.v1`

```json
{
  "schema": "ibvap.event.v1",
  "sequence": 48213,
  "idempotency_key": "01JQ7Z2K9M4N6P8R0T2V4X6Y8A",
  "event_id": 9142,
  "site": {
    "id": "bop-north-01",
    "name": "BOP North"
  },
  "camera": {
    "id": 3,
    "name": "Gate North",
    "encoded_width": 960,
    "encoded_height": 1080,
    "display_width": 1920,
    "display_height": 1080
  },
  "rule": {
    "id": 12,
    "version": 4,
    "name": "Approach zone after dark",
    "alerting": true
  },
  "captured_at": "2026-09-03T18:42:07.412Z",
  "recorded_at": "2026-09-03T18:42:07.508Z",
  "clock_trusted": true,
  "illumination": "infrared",
  "detection": {
    "primary_class": "person",
    "class_mixed": false,
    "boxes": [[412, 318, 468, 470]],
    "geometry": "encoded",
    "track_ids": [1187]
  },
  "plate": null,
  "under_override": false,
  "links": {
    "crop": "https://10.4.1.20:8443/api/artefacts/55210?t=…",
    "snapshot": "https://10.4.1.20:8443/api/artefacts/55211?t=…",
    "clip": "https://10.4.1.20:8443/api/artefacts/55212?t=…"
  }
}
```

Where a plate was read:

```json
  "plate": {
    "text": "DL01AB1234",
    "confidence": 0.81,
    "grammar_matched": true
  }
```

Every field above is generated from the Pydantic v2 models
[ADR 0033](../adr/0033-backend-framework-packaging-and-auth.md) makes the single
source of truth. The same models produce the OpenAPI specification RFC 0004
publishes, so the payload the C2 system receives and the payload the API
documents cannot diverge — which is the failure ADR 0006 exists to prevent.

Four fields carry decisions rather than data:

- **`clock_trusted`** — false means the capture time is not reliable. A consumer
  that timestamps its own records from this field needs to know that.
- **`geometry: "encoded"`** — boxes are in the stream's native encoded geometry,
  not display geometry. On an anamorphic stream those differ by a factor of two,
  and a consumer that draws them without the stretch will be wrong in a way that
  looks plausible.
- **`under_override`** — the event was produced on a camera whose capability
  verdict was overridden by a named authority (ADR 0007). It travels with the
  event permanently.
- **`class_mixed`** — other classes were present; `primary_class` is the one the
  rule fired on.

There is no severity, priority, threat level or score. Nothing computes one
(ADR 0018), so nothing publishes one.

### Payload-progressive delivery

The event goes out immediately with the record and three links. The crop is
small and usually already written; the clip may still be being cut. A consumer
fetches what it wants, when it wants it, over the same API the console uses,
authenticated by a per-artefact token embedded in the link.

That ordering is what makes egress work on a link that is intermittent or slow:
the thing that must arrive is ~2 KB of JSON, and 7.5 MB of video is fetched only
if somebody actually looks. A design that pushed the clip would make every event
as slow and as fragile as its largest artefact.

Artefact links expire with the artefact. A link to something the retention sweep
has removed returns a refusal that says so, rather than a 404 that reads like a
bug.

### Versioning

The `schema` field is the contract. Rules:

- **Additive changes keep the version.** A new optional field is not a breaking
  change, and a consumer must ignore fields it does not recognise. This is stated
  in the published schema so it is a requirement rather than a hope.
- **Removing or retyping a field is a new major version**, published as
  `ibvap.event.v2`, delivered to a separately configured endpoint or MQTT topic.
  Both versions can be published concurrently during a migration.
- **The JSON Schema is an artefact**, generated from the Pydantic models and
  served at `GET /api/integration/schema/{version}` so a consumer can fetch
  exactly what this build emits rather than what a document claims it emits.

### Transports

**HTTP webhook.** `POST` of the JSON body over `httpx`, async.

| Header | Value |
|---|---|
| `Content-Type` | `application/json` |
| `X-IBVAP-Schema` | `ibvap.event.v1` |
| `X-IBVAP-Sequence` | the monotonic sequence number |
| `X-IBVAP-Idempotency-Key` | the key, also in the body |
| `X-IBVAP-Signature` | `sha256=<hex>`, HMAC-SHA256 of the raw request body |

The signature is over the raw bytes, before any parsing, so a consumer verifies
exactly what arrived. The key is per endpoint and held behind the `secret_ref`
indirection RFC 0003 uses. Any 2xx is acceptance; 4xx other than 408 and 429 is
rejection and is not retried, because a consumer saying "this is malformed" will
say it again; 408, 429, 5xx, connection failures and timeouts are retried.

**MQTT.** `aiomqtt`, QoS 1, not retained.

```
ibvap/<site_id>/events/<camera_id>/<primary_class>
```

The topic carries site, camera and class so a subscriber can filter without
parsing every payload. QoS 1 is at-least-once, which is why the idempotency key
is in the payload and not only in a header. Not retained, because a C2 system
reconnecting should get what happens next, not a stale event replayed as if it
were current — the backlog is the queue's job, and it comes through in order.

Both transports can be configured at once. Each endpoint gets its own queue row
per event, so a failing webhook does not hold up a working MQTT broker.

### Delivery loop

One async task per enabled endpoint:

1. Claim due rows: `state = 'pending' AND next_attempt_at <= now`, ordered by
   `sequence`, in small batches. Mark `in_flight`.
2. Send. Record the attempt in `egress_deliveries` regardless of outcome.
3. On acceptance, mark `delivered`.
4. On rejection, mark `dead` with the reason.
5. On a retryable failure, increment `attempts`, set `next_attempt_at` by the
   backoff schedule, return to `pending`.
6. After the attempt ceiling, mark `dead`.

Backoff is exponential with full jitter: `min(2^attempts, 300) × random(0, 1)`
seconds, capped at five minutes, with a ceiling of 12 attempts — roughly an hour
of trying before a message is declared dead. Jitter matters because a site coming
back online after three days has thousands of queued rows, and an unjittered
backoff would deliver them in synchronised bursts that look like an attack to
anything in front of the consumer.

Rows left `in_flight` by a crash are returned to `pending` at startup. That can
re-send a message the consumer already accepted, which is precisely what the
idempotency key exists to make harmless.

A `dead` row is never deleted by the publisher. It is visible on S-05 with its
last error, and an operator can requeue it.

### Reconnect after 72 hours offline

Nothing special happens, which is the design goal.

The queue accumulated rows the whole time, in the same transaction that wrote
each event. The delivery loop kept failing and backing off to its five-minute
cap. On reconnect the first attempt succeeds and the backlog drains in sequence
order, jittered.

Two things the operator can see afterwards, on S-05: how many events were
delivered late, and — from `egress_drops` — whether the queue bound was reached
and a range of events was discarded. The second is the honest part. At the
configured bound the site would have to be offline for years before it triggers,
but if it does, the gap is a row in a table and a line on a screen rather than a
silence.

### The test event

S-05 sends a synthetic event through the whole path — same payload shape, same
signing, same transport — with `"site": {"id": "…"}` unchanged and an
`"event_id": null` plus `"test": true` field marking it. It is not written to
`events` and not queued; it is sent inline so the operator gets the result while
still looking at the screen.

The result is rendered as a `DeliveryRow` with the outcome the hi-fi frames draw:
accepted, rejected with the status code, or unreachable. That is what ADR 0006
means by *demonstrated* — an integration that has been shown to work against the
actual consumer, from the actual screen, rather than asserted in a document.

A consumer that cannot distinguish a test event from a real one is a consumer
with a bug, so `test: true` is a required field of the schema rather than an
optional extra.

## System-context diagram

Where this sits in the whole system: the
[container view](../architecture/diagrams/c4-l2-container.md).

The detailed diagrams for this RFC — the queue-item state machine, the retry flow, and the offline-reconnect sequence — are still owed, and are tracked
as remaining Phase 3 work rather than assumed to exist.

## APIs

Outbound is the payload above. Inbound — the S-05 configuration surface — belongs
to RFC 0004 and is listed here so the pairing is visible:

| Endpoint | Purpose |
|---|---|
| `GET /api/integration/endpoints` | List configured endpoints and their state |
| `POST /api/integration/endpoints` | Add a webhook or MQTT endpoint |
| `PATCH /api/integration/endpoints/{id}` | Enable, disable, or rotate the secret |
| `POST /api/integration/endpoints/{id}/test` | Send a test event, return the outcome inline |
| `GET /api/integration/deliveries` | Recent delivery attempts, for the `DeliveryRow` list |
| `POST /api/integration/deliveries/{sequence}/requeue` | Return a dead row to pending |
| `GET /api/integration/schema/{version}` | The published JSON Schema |

The publisher's own Pydantic models:

```python
class EgressSite(BaseModel):
    id: str
    name: str

class EgressCamera(BaseModel):
    id: int
    name: str
    encoded_width: int
    encoded_height: int
    display_width: int
    display_height: int

class EgressRule(BaseModel):
    id: int
    version: int
    name: str
    alerting: bool

class EgressDetection(BaseModel):
    primary_class: Literal["person", "vehicle", "face", "plate"]
    class_mixed: bool
    boxes: list[tuple[int, int, int, int]]
    geometry: Literal["encoded"] = "encoded"
    track_ids: list[int]

class EgressPlate(BaseModel):
    text: str
    confidence: float
    grammar_matched: bool

class EgressLinks(BaseModel):
    crop: HttpUrl | None = None
    snapshot: HttpUrl | None = None
    clip: HttpUrl | None = None

class EgressEventV1(BaseModel):
    schema_: Literal["ibvap.event.v1"] = Field("ibvap.event.v1", alias="schema")
    sequence: int
    idempotency_key: str
    event_id: int | None
    test: bool = False
    site: EgressSite
    camera: EgressCamera
    rule: EgressRule
    captured_at: datetime
    recorded_at: datetime
    clock_trusted: bool
    illumination: Literal["colour", "infrared"]
    detection: EgressDetection
    plate: EgressPlate | None = None
    under_override: bool = False
    links: EgressLinks
```

TypeScript interfaces for the S-05 screen are in RFC 0004 alongside the rest of
the console's types.

## Data storage

All of it is RFC 0003's: `egress_endpoints`, `egress_queue`,
`egress_deliveries`, `egress_drops`. This RFC adds no tables and owns no schema.

The one storage-shaped decision here is that `egress_deliveries` records **every
attempt**, not only the last one. A consumer that intermittently rejects is a
different problem from one that is unreachable, and only the attempt history
distinguishes them.

## Alternatives considered

**A named adapter for a specific C2 product.** Rejected by ADR 0006 before this
RFC. No target system has been named, and an adapter for a guessed one is work
thrown away plus a false claim of compatibility.

**ONVIF Profile M over MQTT as the primary contract.** The standards-aligned
choice, and the right long-term direction. Deferred by ADR 0006 to post-MVP
because it constrains the payload to what the profile models, and this build
needs to demonstrate an integration rather than conform to a profile no named
consumer has asked for.

**Kafka, AMQP, or any broker as a hard dependency.** Rejected: it is another
service to deploy, supervise and explain at a site with no engineer, for a
delivery rate of tens of events per day.

**Push the clip with the event.** Rejected above — it makes every event as slow
and as fragile as its largest artefact, on the link least able to carry it.

**At-most-once delivery to avoid duplicates.** Rejected. On an unreliable link,
at-most-once loses events, and a lost security event is worse than a duplicate
one a consumer can dedupe with the key it was given.

**Deleting dead rows after a period.** Rejected. A dead row is the record of a
delivery that did not happen; expiring it quietly recreates the silence the
`egress_drops` table exists to avoid.

**Signing with TLS client certificates instead of an HMAC.** Reasonable, and
rejected on commissioning cost: certificate distribution at a site with no IT
support and no internet is exactly the kind of setup that gets skipped, leaving
the integration unsigned in practice.

## Cross-cutting concerns

**Security.** The HMAC authenticates the sender and detects tampering, and works
whether or not TLS is available — an isolated network with no certificate
authority is a plausible deployment, and the contract should not require one.
Where TLS is available it is used, and certificate verification is on by default
with an explicit per-endpoint opt-out for a self-signed C2 endpoint, recorded
with who turned it off.

**Outbound only.** The publisher opens connections; nothing listens. There is no
inbound path from the C2 system into the platform, which keeps the site's attack
surface to the console's own port.

**No internet dependency.** Both transports address a consumer on a network the
site can reach. Nothing resolves an external name, checks a licence, or phones
home — the constraint from
[ADR 0004](../adr/0004-function-without-remote-monitoring-layer.md) applied to
the one component whose whole job is talking to something else.

**Backpressure on the publisher.** A slow consumer causes the queue to grow, not
the analytics loop to stall. The publisher never blocks the event writer; the
only coupling is the shared transaction at write time, which is a single row
insert.

**Observability.** Per endpoint: pending depth, oldest pending age, delivered in
the last hour, dead count, and last error. Oldest-pending-age is the one that
matters — it is what tells an operator the link has been down since Tuesday
rather than that a handful of messages are queued.

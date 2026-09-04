# 07. Integration and Egress Design

How IBVAP hands events to a command-and-control system. Summarises
[RFC 0005](../../rfcs/0005-c2-event-egress-publisher.md), which holds the
exact payload example and Pydantic models.

## Contents

- [Why generic, not a named adapter](#why-generic-not-a-named-adapter)
- [Payload contract](#payload-contract)
- [Versioning](#versioning)
- [Transports](#transports)
- [Delivery loop](#delivery-loop)
- [Reconnect after an extended outage](#reconnect-after-an-extended-outage)
- [The test-event flow](#the-test-event-flow)

## Why generic, not a named adapter

No target C2 system is named by the problem statement or the PRD. Designing
an adapter for a guessed product would be work thrown away and a false claim
of compatibility, so IBVAP publishes a **generic, versioned event contract**
and demonstrates it end to end against a real external consumer instead
([ADR 0006](../../adr/0006-c2-integration-via-generic-event-contract.md)).

## Payload contract

`ibvap.event.v1`, generated from the same Pydantic v2 models RFC 0004's
OpenAPI document uses, so the payload a consumer receives and the payload the
API documents cannot diverge.

| Field group | Carries |
|---|---|
| Identity | `schema`, `sequence`, `idempotency_key`, `event_id` |
| Site / camera / rule | Site id and name; camera id, name and both geometries; rule id, version, name, `alerting` |
| Timing | `captured_at`, `recorded_at`, `clock_trusted` |
| Detection | `primary_class`, `class_mixed`, boxes in encoded geometry, track ids |
| Plate (optional) | Text, confidence, `grammar_matched` |
| Governance | `under_override` — produced under a named-authority capability override |
| Links | Time-limited URLs to the crop, snapshot and clip artefacts |

There is no severity, priority, threat level or classification field — nothing
computes one, so nothing publishes one
([ADR 0018](../../adr/0018-operator-assigned-impact-grade.md),
[ADR 0020](../../adr/0020-egress-classification-field-deferred.md)). Its
absence is a decision, not an oversight.

**Payload-progressive delivery.** The ~2 KB record and its links go out
immediately; the 7.5 MB clip is fetched only if a consumer looks, over the
same authenticated API the console uses. A design that pushed the clip would
make every event as slow and as fragile as its largest artefact.

## Versioning

- An additive field keeps the version; a consumer must ignore fields it does
  not recognise.
- Removing or retyping a field is a new major version (`ibvap.event.v2`),
  deliverable concurrently with `v1` during a migration.
- The JSON Schema is generated, not hand-written, and served at
  `GET /api/integration/schema/{version}`.

## Transports

| Transport | Mechanism | Delivery semantics |
|---|---|---|
| HTTP webhook | `POST` over `httpx`, HMAC-SHA256 signature over the raw body | 2xx accepted; 4xx (except 408/429) rejected and not retried; 408/429/5xx/timeout retried |
| MQTT | `aiomqtt`, topic `ibvap/<site>/events/<camera>/<class>` | QoS 1, not retained — a reconnecting consumer gets what happens next, not a stale replay |

Both can run at once; each endpoint gets its own queue row per event, so one
failing transport never holds up the other.

## Delivery loop

One async task per enabled endpoint: claim due `pending` rows in sequence
order → send → record the attempt regardless of outcome → mark `delivered` or
`dead` (rejection) or return to `pending` with exponential backoff (retryable
failure). Backoff is `min(2^attempts, 300) × random(0,1)` seconds, jittered
specifically so a site reconnecting after days offline does not deliver its
backlog in synchronised bursts that look like an attack to anything in front
of the consumer, capped at 12 attempts (~1 hour) before a row is declared
dead. A `dead` row is visible on the integration screen with its last error
and can be requeued by an operator; it is never silently deleted.

## Reconnect after an extended outage

Nothing special happens, by design. The queue accumulates rows the whole time,
each written in the same transaction as its Event; the delivery loop keeps
backing off to its five-minute cap; on reconnect the backlog drains in
sequence order, jittered. Two facts stay visible afterward: how many events
delivered late, and — from `egress_drops` — whether the queue's bound was ever
reached and a range of events discarded. At the configured bound (default
100,000 rows) a site would need to be offline for roughly a thousand days
before that triggers.

## The test-event flow

The integration screen sends a synthetic event through the real path — same
schema, same signing, same transport — carrying `test: true` and no
`event_id`, not written to the store. The result renders inline as accepted,
rejected (with status code), or unreachable. This is what "demonstrated"
means under ADR 0006: shown working against the actual consumer, not asserted
in a document.

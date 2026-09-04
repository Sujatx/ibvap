# 04. API Contracts

The HTTP and WebSocket surface between the console and the application. This
summarises [RFC 0004](../../rfcs/0004-web-application-and-api-contracts.md),
which holds the exact JSON examples, Pydantic models and TypeScript
interfaces for every endpoint listed here.

## Contents

- [Conventions](#conventions)
- [Endpoint catalogue](#endpoint-catalogue)
- [The `/ws/live` protocol](#the-wslive-protocol)
- [Overlay synchronisation](#overlay-synchronisation)
- [Authentication and offline recovery](#authentication-and-offline-recovery)

## Conventions

- **Base path** `/api`, unversioned — an internal contract shipped with its
  only client. The contract that must stay stable is RFC 0005's outbound
  payload, not this one.
- **Times** are UTC ISO-8601 with `Z`, in both directions.
- **Coordinates** are in the stream's *encoded* geometry; the display stretch
  is applied once, in the browser.
- **Refusal is content, not an error.** A capability a camera cannot support,
  or a rule that cannot run, returns `200` with `supported: false` and a full
  reason sentence — the same sentence rendered verbatim wherever it appears.
  A `409` is reserved for an action that *conflicts* with a refusal.
- **Errors** are `application/problem+json` (RFC 9457), carrying the same
  reason text as the resource it describes.
- **Pagination** is cursor-based (`?limit=&cursor=`), because an offset drifts
  under a feed that grows while it is being read.

## Endpoint catalogue

| Group | Representative endpoints | Purpose |
|---|---|---|
| Session | `POST/GET/DELETE /api/auth/session`, `POST /api/auth/password-reset/*`, `POST /api/users/{id}/password` | Sign in/out, session restore, network and local-administrator password recovery |
| Cameras and capabilities | `GET /api/cameras`, `GET /api/cameras/{id}/capabilities`, `POST .../remeasure`, `POST .../{capability}/override`, `GET .../stream` | The grid, focused view, capability chips, and how to play a camera (WHEP primary, MJPEG fallback) |
| Rules | `GET/POST/PUT/PATCH/DELETE /api/rules`, `GET /api/rules/{id}/versions` | CRUD over rules; edits create a new version, never mutate one |
| Watchlist | `GET/PUT /api/watchlist/config`, `GET/POST/DELETE /api/watchlist/subjects`, `GET /api/watchlist/matches` | Enroll and manage the face-recognition gallery; every route `409`s until `watchlist_config.enabled` is true |
| Events, alerts, mutes | `GET /api/events`, `GET /api/events/{id}`, `POST /api/events/{id}/clip`, `GET /api/alerts`, `POST /api/alerts/{id}/assessment`, `PATCH /api/alerts/{id}`, `GET/POST/DELETE /api/mutes` | The event feed, alert triage (real/not real/unsure), impact grade, mute/snooze |
| Timeline and playback | `GET /api/cameras/{id}/timeline`, `POST /api/cameras/{id}/playback` | Recorded-video bands, gaps and markers, or the refusal when the recorder serves none |
| Integration | `GET/POST/PATCH /api/integration/endpoints`, `POST .../test`, `GET /api/integration/deliveries`, `GET /api/integration/schema/{version}` | C2 endpoint configuration, the test-event flow, delivery history |

Filters on `/api/events`: `camera_id`, `klass`, `kind` (`alert`\|`logged`),
`from`, `to`, `assessed`, `limit`, `cursor` — exactly what the alerts screen's
filter drawer offers.

## The `/ws/live` protocol

One socket per console session, authenticated by the session cookie. The
client subscribes to the cameras it is currently showing.

| Direction | Message | Carries |
|---|---|---|
| Client → server | `subscribe` / `unsubscribe` | A list of camera ids |
| Server → client | `hello` | Server time, protocol version |
| Server → client | `detections` | Per-camera boxes at the analysed frame rate, in encoded geometry |
| Server → client | `event` / `alert` | The same shape the REST feed returns — one shape, two transports |
| Server → client | `camera_status` | Connection state, delivered/analysed fps |
| Server → client | `capability_changed` | A camera's verdicts changed |
| Server → client | `mute_changed` | A mute was created, ended, or expired |
| Server → client | `artefact_ready` | A requested clip/crop/snapshot finished writing |
| Server → client | `delivery_status` | Egress queue depth and last outcome, per endpoint |

## Overlay synchronisation

Video reaches the page over WebRTC; detection boxes reach it over the
WebSocket, at different latencies. The client buffers ~2 seconds of
`detections` messages and, per animation frame, draws the newest one whose
capture time is at or before the video's current playback time within a 120 ms
lead tolerance — or draws nothing, rather than a wrong box, once staleness
passes 500 ms. The anamorphic stretch is applied once, to the video element
and the canvas overlay together, from the same scale factor — correcting one
layer and not the other is how an overlay ends up wrong by exactly a factor of
two (RFC 0004, Overlay synchronisation).

## Authentication and offline recovery

Session state is an opaque id in an HTTP-only, `SameSite=Strict`, `Secure`
cookie, held server-side, with Argon2id password hashing
([ADR 0033](../../adr/0033-backend-framework-packaging-and-auth.md)). Lockout
is a progressive, self-clearing delay rather than an admin-cleared block, with
three distinct sentences for disabled, expired and locked accounts
([ADR 0037](../../adr/0037-sign-in-follows-the-reference-username-password.md)).

Two recovery paths exist side by side: an emailed network reset for a site
with a link, and a **local administrator reset** — a second account holding
`can_reset` can set another user's password from the console with no network
at all, restoring the offline recovery capability a prior revision of the
sign-in design dropped
([ADR 0055](../../adr/0055-offline-password-recovery-by-local-admin-reset.md)).
Every reset writes who performed it, for whom, and when.

Full detail, including per-endpoint schemas, lives in RFC 0004; security
properties are consolidated in
[06-security-and-auth.md](06-security-and-auth.md).

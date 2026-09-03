# 0004. Web application and API contracts

**Status:** Accepted
**Author:** Sujat
**Date:** 2026-09-03

## Context and scope

Phase 2 finished twelve hi-fi frames in Figma `03 Hi-fi`. Those frames are the
specification for the console, and this RFC's job is to make sure an API exists
that fills every element on them — proved element by element, not assumed.

That leads to a precedence rule which this document states once and applies
throughout:

> **Where an ADR and the hi-fi frames disagree, the frames are the
> specification and the ADR is history.**

Several ADRs are older than the frames they describe, and two of them record
Figma prototyping workarounds that have no business surviving into code. They are
enumerated below so nobody has to rediscover which is which.

This RFC also settles a debt
[ADR 0037](../adr/0037-sign-in-follows-the-reference-username-password.md) left
here explicitly: dropping the pre-issued recovery codes made password recovery
depend on the network, which is a real regression at a border post with no link.

Everything the API serves comes from
[RFC 0003](0003-event-store-and-alert-state.md)'s tables, populated by
[RFC 0001](0001-video-ingest-capability-measurement-and-playback.md),
[RFC 0006](0006-detection-and-analytics-primitives.md) and
[RFC 0002](0002-rule-evaluation-engine.md). Egress configuration endpoints are
listed in [RFC 0005](0005-c2-event-egress-publisher.md) and not repeated.

## Goals and non-goals

**Goals**

1. Every REST endpoint with a JSON example, a Pydantic v2 model and a TypeScript
   interface — the roadmap's Phase 3 Definition of Done.
2. The `/ws/live` protocol, same treatment.
3. A trace from each of the twelve hi-fi frames to the endpoints that fill it.
4. The overlay synchronisation algorithm, because two transports with different
   latencies is the hard part of
   [ADR 0035](../adr/0035-operator-console-stack-and-video-transport.md).
5. A decision on offline password recovery.
6. The console's own architecture: routing, state, the token export, the Canvas
   layer.

**Non-goals**

- Re-designing any screen. The frames exist; this RFC serves them.
- The flow-state frames — `too many attempts`, `drawing a zone`, `mute applied`,
  `the test event was refused`. Deferred out of Phase 2 by
  [ADR 0048](../adr/0048-phase-2-closes-flow-frames-deferred.md); the endpoints
  that would back them exist here, the visual design does not yet.
- A sixth screen. [ADR 0016](../adr/0016-mvp-ui-cut-to-five-screens.md) froze
  five, and nothing here needs another.
- Public API stability. This is an internal contract between one backend and one
  front end shipped together. The *outbound* contract that must stay stable is
  RFC 0005's.

## Design

### Where the frames overrule an ADR

| The ADR says | The frames show | What gets built |
|---|---|---|
| [0047](../adr/0047-rail-collapse-becomes-baked-frame-pairs.md) — collapse is baked frame pairs reached by `NAVIGATE` | Collapsed and expanded chrome at the same 1440 width | Runtime state on `AppShell`. The baked pairs are a workaround for Figma's interactive-component memory and have no meaning in code |
| [0041](../adr/0041-hi-fi-assembled-from-an-appshell-component.md) — five 1440 masters, five 1280 counterparts | Twelve 1440 frames plus a 1920 fluid proof | Build the frames; 0047 already narrowed this |
| [0017](../adr/0017-cameras-site-sketch-not-a-map.md) — site sketch on a Cameras list | Site sketch panel on the focused Live View | Build [0044](../adr/0044-site-sketch-returns-on-live-view.md) |
| [0038](../adr/0038-historical-timeline-on-the-focused-camera-view.md) / [0045](../adr/0045-timeline-second-pass-controls-and-density.md) — markers carry no hue | Markers coloured by detection class | Build [0046](../adr/0046-timeline-markers-carry-class-colour.md) |
| [0036](../adr/0036-wireframe-breakpoints-and-required-state-set.md) — three widths, a frame per state | Two drawn widths, a state matrix as evidence | Build [0039](../adr/0039-state-coverage-evidenced-three-ways.md) |
| Wireframes — S-04 as a five-column table with a header | `EventRow` cards, no `TableHeader` | Build the cards |

One consequence reaches the API rather than the components. ADR 0043 added an
**Active Alerts rail to Live View**, restating data that S-04 owns. It is served
by the same endpoint and the same WebSocket messages S-04 uses — never a
parallel query — so the two cannot disagree. Where they would, S-04 is right.

### Authentication, and offline recovery

Session as ADR 0033 decided: an opaque id in an HTTP-only, `SameSite=Strict`,
`Secure` cookie over server-side session state, with Argon2id password hashing.
No token leaves the machine and no external identity provider is contacted.

ADR 0037 keeps configurable timeouts, a progressive self-clearing delay rather
than an admin-cleared lockout, three distinct sentences for disabled, expired and
locked, and a minimum-length-only password rule. It drops the post ID, the
passphrase and the pre-issued recovery codes — and, in dropping the last of
those, makes recovery depend on a network the site may not have for three days.

**Decision: a local administrator reset returns, alongside the network reset.**

A second account holds `can_reset`. That account can set another user's password
from the console, on the machine, with no link — the recovery path that works at
a disconnected post. The emailed reset stays for sites that do have a link,
because it does not require a second person to be present. Neither is a security
downgrade from pre-issued codes: a printed code in a drawer at an unstaffed post
is not obviously safer than a named colleague who has to log in and be recorded
doing it.

Every reset writes who did it, for whom, and when. Recorded as an ADR alongside
this RFC.

### Conventions

- **Base path** `/api`. Version in the path is deliberately absent — this is an
  internal contract shipped with its only client. RFC 0005's outbound contract
  carries the version that matters.
- **Times** are UTC ISO-8601 with `Z`, everywhere, in both directions.
- **Coordinates** are in the stream's *encoded* geometry, and every payload
  containing one says so. The display stretch is applied once, in the browser.
- **Errors** are `application/problem+json` (RFC 9457):

```json
{
  "type": "https://ibvap.local/problems/capability-refused",
  "title": "Capability refused on this camera",
  "status": 409,
  "detail": "ANPR is refused on Gate North. At 40 m this camera resolves about 12 pixels of plate height; reading a plate needs at least 20.",
  "instance": "/api/rules/44"
}
```

  `detail` carries the same sentence the store holds, so a refusal reads
  identically wherever it appears.
- **Refusal is not an error.** A capability a camera cannot support is a `200`
  with `supported: false` and a reason, on the resource that describes it. The
  `409` above is only for an action that *conflicts* with a refusal — trying to
  arm a rule that cannot run.
- **Pagination** is cursor-based: `?limit=50&cursor=…`, response carries
  `next_cursor` or `null`. Offsets drift under a feed that grows while you read
  it.

### Endpoint catalogue

#### Session

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/auth/session` | Sign in |
| `GET` | `/api/auth/session` | Who am I; used on load to restore a session |
| `DELETE` | `/api/auth/session` | Sign out |
| `POST` | `/api/auth/password-reset/request` | Start the network reset |
| `POST` | `/api/auth/password-reset/complete` | Finish it with a token |
| `POST` | `/api/users/{id}/password` | Local administrator reset; requires `can_reset` |

```json
// POST /api/auth/session
{ "username": "post.operator", "password": "…", "remember_username": true }

// 201
{ "user": { "id": 2, "username": "post.operator", "can_reset": false },
  "expires_at": "2026-09-04T02:11:00Z" }

// 401, when the account is locked -- three distinct sentences, ADR 0037
{ "type": "https://ibvap.local/problems/account-locked",
  "title": "Too many attempts",
  "status": 401,
  "detail": "Sign-in is paused for 4 minutes after five failed attempts. It will clear on its own.",
  "instance": "/api/auth/session" }
```

#### Cameras and capabilities

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/cameras` | The grid, the sidebar, the `CameraThumb` strip |
| `GET` | `/api/cameras/{id}` | The focused view's `SpecRow` list |
| `GET` | `/api/cameras/{id}/capabilities` | Chip row and `CapabilityNotice` |
| `POST` | `/api/cameras/{id}/capabilities/remeasure` | Re-run the pass |
| `POST` | `/api/cameras/{id}/capabilities/{capability}/override` | Named-authority override |
| `GET` | `/api/cameras/{id}/snapshot` | Still frame, for the rules editor |
| `GET` | `/api/cameras/{id}/stream` | How to play this camera |
| `GET` / `PUT` | `/api/site-sketch` | The operator-supplied image and pins |

```json
// GET /api/cameras/3
{
  "id": 3,
  "name": "Gate North",
  "recorder": { "id": 1, "name": "BOP North XVR" },
  "channel": 3,
  "connection_state": "streaming",
  "encoded_width": 960, "encoded_height": 1080,
  "display_width": 1920, "display_height": 1080,
  "delivered_fps": 24.8,
  "analysed_fps": 5.0,
  "illumination": "infrared",
  "reference_distance_m": 40.0,
  "scene_width_m": 22.0,
  "site_sketch": { "x": 0.62, "y": 0.31, "facing_degrees": 210 }
}

// GET /api/cameras/3/capabilities
{
  "measured_at": "2026-09-03T05:02:11Z",
  "illumination": "infrared",
  "capabilities": [
    { "capability": "human_detect", "supported": true,  "reason": null },
    { "capability": "vehicle_detect", "supported": true, "reason": null },
    { "capability": "face_detect", "supported": false,
      "reason": "Face detection is refused on Gate North. At 40 m a face is about 9 pixels wide here; detecting one needs at least 24." },
    { "capability": "anpr", "supported": false,
      "reason": "ANPR is refused on Gate North. At 40 m this camera resolves about 12 pixels of plate height; reading a plate needs at least 20." },
    { "capability": "night_movement", "supported": true, "reason": null },
    { "capability": "recorded_playback", "supported": false,
      "reason": "This recorder does not serve recorded video to IBVAP, so the timeline is unavailable on every camera." }
  ]
}
```

`GET /api/cameras/{id}/stream` returns how to play, not the pixels:

```json
{
  "primary": { "kind": "webrtc", "whep_url": "https://10.4.1.20:1984/api/whep?src=cam3" },
  "fallback": { "kind": "mjpeg", "url": "https://10.4.1.20:1984/api/stream.mjpeg?src=cam3" }
}
```

The fallback is always present. ADR 0035 keeps MJPEG as the documented retreat —
a degraded picture, not a missing screen — and the client falls back on its own
when the WebRTC negotiation fails.

#### Rules

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/rules?camera_id=` | The `RuleCard` list |
| `POST` | `/api/rules` | Create |
| `GET` | `/api/rules/{id}` | One rule, current version |
| `PUT` | `/api/rules/{id}` | Edit — creates a new version |
| `PATCH` | `/api/rules/{id}` | Enable or disable |
| `DELETE` | `/api/rules/{id}` | Remove |
| `GET` | `/api/rules/{id}/versions` | History |

```json
// POST /api/rules
{
  "camera_id": 3,
  "name": "Approach zone after dark",
  "geometry": {
    "kind": "zone",
    "points": [[0.31,0.44],[0.68,0.44],[0.71,0.92],[0.27,0.92]],
    "drawn_encoded_width": 960,
    "drawn_encoded_height": 1080
  },
  "condition": {
    "op": "primitive",
    "primitive": { "condition": "dwell", "klass": "person", "seconds": 120 }
  },
  "schedule": { "kind": "night", "windows": [], "days": [] },
  "alerting": true,
  "cooldown_seconds": 60
}

// 201 -- note the refusal travels on the resource, not as an error
{ "id": 44, "version": 1, "enabled": true, "refused_reason": null, "…": "…" }
```

#### Watchlist

Gated end to end by [ADR 0059](../adr/0059-face-recognition-ships-against-a-configured-watchlist.md):
every endpoint below returns `409` with a refusal sentence, the same voice
`CapabilityNotice` uses, when `watchlist_config.enabled` is false.

**No hi-fi frame exists for this.** The twelve frames Phase 2 built have no
enrollment or match-review screen, and the Notion PRD does not name one — this
is the gap [ADR 0059](../adr/0059-face-recognition-ships-against-a-configured-watchlist.md)
records against [CLAUDE.md](../../CLAUDE.md) §2's four-homes rule. The
contract below is written so a screen can be built against it once Figma and
the PRD carry one; it is not itself a claim that the screen exists.

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/watchlist/config` | The four conditions and whether recognition is enabled |
| `PUT` | `/api/watchlist/config` | Set the four conditions; `enabled` is a separate, explicit field |
| `GET` | `/api/watchlist/subjects` | The gallery |
| `POST` | `/api/watchlist/subjects` | Enroll a subject from a reference photo |
| `DELETE` | `/api/watchlist/subjects/{id}` | Soft-remove from the active gallery |
| `GET` | `/api/watchlist/matches?since=` | Matches, newest first, for review |

```json
// PUT /api/watchlist/config
{
  "enabled": true,
  "legal_basis_ref": "SIH 2026 controlled demonstration, consented test subjects",
  "authority_ref": "…",
  "retention_days": 30
}

// POST /api/watchlist/subjects  (multipart: label, notes, photo)
// 201 -- note the reference photo becomes an artefact and an embedding, not a stored photo alone
{ "id": 7, "label": "Subject 7", "enrolled_at": "2026-09-03T10:00:00Z" }

// GET /api/watchlist/matches?since=2026-09-03T00:00:00Z
{
  "matches": [
    { "event_id": 5501, "subject_id": 7, "similarity": 0.41,
      "threshold_used": 0.363, "matched_at": "2026-09-03T10:14:02Z" }
  ]
}
```

A match also arrives on `/ws/live` as an `event` message like any other, with
`primary_class: "face"` — a client watching for watchlist activity reads
`GET /api/watchlist/matches` for the join to `subject_id`, rather than the
protocol growing a second event shape for the same fact.

#### Events, alerts, assessment and mutes

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/events` | The S-04 feed, filtered |
| `GET` | `/api/events/{id}` | The detail panel |
| `POST` | `/api/events/{id}/clip` | Request the full clip — payload-progressive |
| `GET` | `/api/alerts?active=true&limit=` | The Live View alerts rail |
| `POST` | `/api/alerts/{id}/assessment` | Real / not real / unsure |
| `PATCH` | `/api/alerts/{id}` | Impact grade |
| `GET` | `/api/mutes` | The always-visible mute banner |
| `POST` | `/api/mutes` | Snooze this camera and rule |
| `DELETE` | `/api/mutes/{id}` | Turn it off early |
| `GET` | `/api/artefacts/{id}` | Crop, snapshot or clip bytes |

Filters on `/api/events`: `camera_id`, `klass`, `kind` (`alert` | `logged`),
`from`, `to`, `assessed` (`true` | `false`), `limit`, `cursor` — exactly the set
the hi-fi filter drawer offers, and no more.

```json
// GET /api/events?kind=alert&limit=2
{
  "events": [
    {
      "id": 9142,
      "captured_at": "2026-09-03T18:42:07.412Z",
      "clock_trusted": true,
      "camera": { "id": 3, "name": "Gate North" },
      "rule": { "id": 12, "version": 4, "name": "Approach zone after dark" },
      "primary_class": "person",
      "class_mixed": false,
      "illumination": "infrared",
      "alerting": true,
      "alert": { "id": 771, "state": "new", "impact_grade": null,
                 "assessment": null },
      "artefacts": { "crop": 55210, "snapshot": 55211, "clip": null },
      "plate": null,
      "under_override": false
    }
  ],
  "next_cursor": "eyJpZCI6OTE0Mn0"
}

// POST /api/alerts/771/assessment
{ "verdict": "not_real" }

// 201 -- the mute is offered, never applied automatically
{ "assessment": { "verdict": "not_real", "assessed_at": "2026-09-03T18:44:02Z" },
  "mute_offer": { "camera_id": 3, "rule_id": 12,
                  "durations": ["1h", "1d", "1w", "until_off"] } }

// POST /api/mutes -- the dismissal cause is captured here, ADR 0023
{ "camera_id": 3, "rule_id": 12, "duration": "1d", "dismissal_cause": "animal" }
```

`clip: null` above is the payload-progressive shape: the crop exists at once, the
clip is cut on request and `POST /api/events/{id}/clip` returns `202` with the
artefact id to poll or await over the WebSocket.

#### Timeline and playback

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/cameras/{id}/timeline?from=&to=` | The band, its markers and its gaps |
| `POST` | `/api/cameras/{id}/playback` | Open a playback session at a time |

```json
// GET /api/cameras/3/timeline?from=2026-09-03T12:00:00Z&to=2026-09-04T00:00:00Z
{
  "supported": true,
  "reason": null,
  "extent": { "from": "2026-09-01T09:14:00Z", "to": "2026-09-04T00:00:00Z" },
  "bands": [
    { "kind": "recorded",       "from": "2026-09-03T12:00:00Z", "to": "2026-09-03T17:31:00Z" },
    { "kind": "gap",            "from": "2026-09-03T17:31:00Z", "to": "2026-09-03T17:48:00Z" },
    { "kind": "recorded",       "from": "2026-09-03T17:48:00Z", "to": "2026-09-04T00:00:00Z" },
    { "kind": "unverified_clock","from": "2026-09-03T17:48:00Z", "to": "2026-09-03T18:05:00Z" }
  ],
  "markers": [
    { "event_id": 9142, "at": "2026-09-03T18:42:07.412Z",
      "kind": "alert", "klass": "person" },
    { "event_id": 9139, "at": "2026-09-03T18:11:44.900Z",
      "kind": "logged", "klass": "vehicle" }
  ]
}
```

Four band kinds — `recorded`, `gap`, `pre_retention`, `unverified_clock` — are
exactly what ADR 0046 draws inside the axis bar. Markers carry `kind` for weight
and `klass` for colour, which is the whole of ADR 0046's rule, and carry no
severity because none exists.

When the recorder serves nothing, the same endpoint returns the refusal rather
than an error:

```json
{ "supported": false,
  "reason": "This recorder does not serve recorded video to IBVAP, so the timeline is unavailable on every camera.",
  "extent": null, "bands": [], "markers": [] }
```

### The `/ws/live` protocol

One socket per console session, authenticated by the same session cookie.
Messages are JSON objects with a `type`. The client subscribes to the cameras it
is currently showing, so the grid gets nine streams of detections and the focused
view gets one.

**Client → server**

```json
{ "type": "subscribe",   "cameras": [1, 2, 3, 4, 5] }
{ "type": "unsubscribe", "cameras": [4, 5] }
```

**Server → client**

```json
// on connect
{ "type": "hello", "server_time": "2026-09-03T18:42:00.000Z", "protocol": 1 }

// the overlay's input -- at the analysed frame rate, per subscribed camera
{ "type": "detections",
  "camera_id": 3,
  "frame_captured_at": "2026-09-03T18:42:07.412Z",
  "clock_trusted": true,
  "geometry": "encoded",
  "encoded_width": 960, "encoded_height": 1080,
  "boxes": [
    { "klass": "person", "confidence": 0.88, "track_id": 1187,
      "box": [412, 318, 468, 470] }
  ] }

{ "type": "event",  "event": { "…": "the GET /api/events item shape" } }
{ "type": "alert",  "alert": { "…": "with its event inline" } }
{ "type": "camera_status", "camera_id": 3, "state": "reconnecting",
  "delivered_fps": 0, "analysed_fps": 0 }
{ "type": "capability_changed", "camera_id": 3,
  "capabilities": [ "…" ] }
{ "type": "mute_changed", "mute": { "…": "" } }
{ "type": "artefact_ready", "event_id": 9142, "kind": "clip", "artefact_id": 55212 }
{ "type": "delivery_status", "endpoint_id": 1, "pending": 0,
  "oldest_pending_age_s": null, "last_outcome": "accepted" }
```

`event` and `alert` carry the same shape the REST feed returns. One shape, two
transports — the S-04 list and the Live View rail render from identical objects
whether they arrived by fetch or by push, which is what stops the two drifting.

### Overlay synchronisation

The hard part of ADR 0035. Video reaches the page over WebRTC; boxes reach it
over the WebSocket. They have different latencies, and a box drawn against the
wrong frame is worse than no box.

```
on detections(msg):
    buffer[msg.camera_id].push(msg)          # keep ~2 seconds, ordered

each animation frame, per tile:
    t_video = videoEl.currentTime mapped to capture time via the WHEP
              RTCRtpReceiver timestamp and the `hello` server_time offset
    pick    = newest msg in buffer with frame_captured_at <= t_video + tolerance
    if pick is None or (t_video - pick.frame_captured_at) > max_stale:
        draw nothing                          # hold, then drop
    else:
        draw pick, stretched with the video
```

Three constants, and the reason each exists:

- **tolerance = 120 ms** — a box may lead the frame slightly rather than lag it,
  because detection runs on a frame the decoder produced before the gateway
  packetised it.
- **max_stale = 500 ms** — beyond this the boxes are describing a moment that has
  visibly passed, and drawing nothing is more honest than drawing history.
- **buffer = 2 s** — enough to ride out a WebSocket hiccup without unbounded
  memory.

When the overlay is dropping, the tile says so — a small inline notice, not a
silent absence, because "no boxes" and "boxes we could not trust" are different
facts.

**The anamorphic stretch is applied once, to both layers together.** The Canvas
is sized to the video element's rendered box, and every box is scaled by
`renderedWidth / encoded_width` and `renderedHeight / encoded_height`. Correcting
in one layer and not the other is how overlays end up wrong by exactly a factor
of two.

### Console architecture

**Routing.** React Router, five routes plus the focused view:

```
/signin                    S-01
/live                      S-02 grid
/live/:cameraId            S-02 focused
/rules                     S-03
/alerts                    S-04
/integration               S-05
```

`AppShell` wraps everything but `/signin`, holds the rail's expanded/collapsed
state in a `useState` persisted to `localStorage`, and derives the active
destination from the route. That is the whole of ADR 0047's "baked frame pairs"
in code: one boolean.

**Data.** TanStack Query for REST — it gives caching, refetch-on-focus and
mutation invalidation, which is most of what five screens need. The WebSocket is
a thin hook that pushes into the same query cache, so a component does not know
or care which transport its data arrived on. No global store; there is no state
that outlives a route and is not server state.

**Tokens.** The Figma variable collections export to CSS custom properties, and
Tailwind v4 consumes those properties directly. A build step owns the export, and
a component referencing a token that no longer exists is a build failure rather
than a wrong colour — the direction ADR 0035 intends. A raw colour, spacing or
type value inside a component is a defect
([ADR 0031](../adr/0031-component-grammar-chip-states-fact-segmented-control-chooses.md)).

**Overlay.** Canvas 2D on a transparent layer sized to the video element. Boxes
are drawn from the four `DetectionBox` class tokens; rule zones from the
`RuleZone` token. Nothing is drawn in a severity colour because there is no
severity.

**Testing.** Vitest and Testing Library for components and the sync algorithm —
which is pure and deserves real tests. Playwright is deferred; it needs a running
backend and a fake camera, and that is Phase 5 work.

### Screen-by-screen trace

Every frame, every element, and what fills it. The Watchlist endpoints above
are deliberately absent from this trace — no hi-fi frame consumes them yet,
per the gap named in that section.

**S-01 Sign in.** `POST /api/auth/session`. The brand panel's photograph and
capability row are static assets. "Remember me" stores the username in
`localStorage` only — never a token.

**S-02 Live View, grid** (expanded and collapsed). `GET /api/cameras` for the
tiles and the sidebar; `GET /api/cameras/{id}/stream` per tile for the WHEP URL;
`subscribe` on the socket for `detections` and `camera_status`;
`GET /api/alerts?active=true` plus pushed `alert` messages for the Active Alerts
rail. Every `AlertCard` navigates to `/alerts`, which still owns the event.

**S-02 Focused camera** (expanded and collapsed). Everything above for one
camera, plus `GET /api/cameras/{id}` for the `SpecRow` list,
`GET /api/cameras/{id}/capabilities` for the chip row and `CapabilityNotice`,
`GET /api/site-sketch` for the sketch panel, and
`GET /api/cameras/{id}/timeline` for the axis, its bands and its markers.
`POST /api/cameras/{id}/playback` when the operator scrubs. The `CameraThumb`
strip is the same `GET /api/cameras` response.

**S-03 Rules** (expanded and collapsed). `GET /api/rules?camera_id=` for the
`RuleCard` list; `GET /api/cameras/{id}/snapshot` for the still the zone is drawn
on; `POST`/`PUT /api/rules` to save. A rule whose `refused_reason` is non-null
renders the refusal inline, in the same voice as a capability refusal.

**S-04 Alerts & Events** (expanded and collapsed). `GET /api/events` with the
drawer's filters for the `EventRow` stack; `GET /api/events/{id}` for the detail
panel; `POST /api/alerts/{id}/assessment` for `AssessControl`;
`POST /api/mutes` carrying the `DismissalCausePicker`'s choice and the snooze
duration; `GET /api/mutes` for the `MuteBanner`; `POST /api/events/{id}/clip` for
`ClipRequest`, resolved by the `artefact_ready` message.

**S-05 Integration** (expanded and collapsed). RFC 0005's endpoint list:
`GET`/`POST`/`PATCH /api/integration/endpoints` for configuration,
`POST …/test` for the test event, `GET /api/integration/deliveries` for the
`DeliveryRow` list, and the `delivery_status` message for `ConnectionState`.

**Shell — 1920 fluid proof.** No endpoints of its own; it proves the layout holds
when the content column grows.

## System-context diagram

Where this sits in the whole system: the
[container view](../architecture/diagrams/c4-l2-container.md).

The detailed diagrams for this RFC — the live-view, sign-in, triage and playback sequences — are still owed, and are tracked
as remaining Phase 3 work rather than assumed to exist.

## APIs

The Pydantic models are the source; the TypeScript is generated from the OpenAPI
document they produce, so the pair below is illustrative of the mapping rather
than two hand-maintained copies.

```python
# Python -- the source of truth

class CapabilityRead(BaseModel):
    capability: Literal["human_detect", "vehicle_detect", "face_detect",
                        "anpr", "night_movement", "recorded_playback"]
    supported: bool
    reason: str | None

class CameraRead(BaseModel):
    id: int
    name: str
    recorder: RecorderRef
    channel: int
    connection_state: Literal["resolving", "connecting", "measuring",
                              "streaming", "reconnecting", "stopped"]
    encoded_width: int | None
    encoded_height: int | None
    display_width: int | None
    display_height: int | None
    delivered_fps: float | None
    analysed_fps: float | None
    illumination: Literal["colour", "infrared"] | None
    reference_distance_m: float | None
    scene_width_m: float | None
    site_sketch: SiteSketchPin | None

class EventRead(BaseModel):
    id: int
    captured_at: datetime
    clock_trusted: bool
    camera: CameraRef
    rule: RuleRef
    primary_class: Literal["person", "vehicle", "face", "plate"]
    class_mixed: bool
    illumination: Literal["colour", "infrared"]
    alerting: bool
    alert: AlertRead | None
    artefacts: ArtefactRefs
    plate: PlateRead | None
    under_override: bool

class AlertRead(BaseModel):
    id: int
    state: Literal["new", "assessed"]
    impact_grade: Literal["low", "medium", "high"] | None
    assessment: AssessmentRead | None

class TimelineBand(BaseModel):
    kind: Literal["recorded", "gap", "pre_retention", "unverified_clock"]
    from_: datetime = Field(alias="from")
    to: datetime

class TimelineMarker(BaseModel):
    event_id: int
    at: datetime
    kind: Literal["alert", "logged"]
    klass: Literal["person", "vehicle", "face", "plate"]

class TimelineRead(BaseModel):
    supported: bool
    reason: str | None
    extent: TimeRange | None
    bands: list[TimelineBand]
    markers: list[TimelineMarker]
```

```ts
// TypeScript -- generated from the OpenAPI document

export type Klass = "person" | "vehicle" | "face" | "plate";
export type Illumination = "colour" | "infrared";
export type ConnectionState =
  | "resolving" | "connecting" | "measuring"
  | "streaming" | "reconnecting" | "stopped";

export interface Capability {
  capability: "human_detect" | "vehicle_detect" | "face_detect"
            | "anpr" | "night_movement" | "recorded_playback";
  supported: boolean;
  reason: string | null;
}

export interface Camera {
  id: number;
  name: string;
  recorder: RecorderRef;
  channel: number;
  connectionState: ConnectionState;
  encodedWidth: number | null;
  encodedHeight: number | null;
  displayWidth: number | null;
  displayHeight: number | null;
  deliveredFps: number | null;
  analysedFps: number | null;
  illumination: Illumination | null;
  referenceDistanceM: number | null;
  sceneWidthM: number | null;
  siteSketch: SiteSketchPin | null;
}

export interface Event {
  id: number;
  capturedAt: string;
  clockTrusted: boolean;
  camera: CameraRef;
  rule: RuleRef;
  primaryClass: Klass;
  classMixed: boolean;
  illumination: Illumination;
  alerting: boolean;
  alert: Alert | null;
  artefacts: { crop: number | null; snapshot: number | null; clip: number | null };
  plate: PlateRead | null;
  underOverride: boolean;
}

export interface TimelineBand {
  kind: "recorded" | "gap" | "pre_retention" | "unverified_clock";
  from: string;
  to: string;
}

export interface TimelineMarker {
  eventId: number;
  at: string;
  kind: "alert" | "logged";
  klass: Klass;
}

export type LiveMessage =
  | { type: "hello"; serverTime: string; protocol: number }
  | { type: "detections"; cameraId: number; frameCapturedAt: string;
      clockTrusted: boolean; geometry: "encoded";
      encodedWidth: number; encodedHeight: number; boxes: DetectionBox[] }
  | { type: "event"; event: Event }
  | { type: "alert"; alert: Alert & { event: Event } }
  | { type: "camera_status"; cameraId: number; state: ConnectionState;
      deliveredFps: number; analysedFps: number }
  | { type: "capability_changed"; cameraId: number; capabilities: Capability[] }
  | { type: "mute_changed"; mute: Mute }
  | { type: "artefact_ready"; eventId: number; kind: "clip" | "crop" | "snapshot";
      artefactId: number }
  | { type: "delivery_status"; endpointId: number; pending: number;
      oldestPendingAgeS: number | null; lastOutcome: DeliveryOutcome };
```

## Data storage

None of its own. Every table this RFC reads and writes is
[RFC 0003](0003-event-store-and-alert-state.md)'s. The one piece of state the
console keeps locally is the remembered username and the rail's collapsed
boolean, both in `localStorage`, neither security-relevant.

## Alternatives considered

**Burning boxes into frames server-side and shipping MJPEG.** Rejected by ADR
0035 as the default: it forces a re-encode of every frame of every camera to draw
a rectangle, which is exactly the cost ADR 0032 arranges to avoid. It survives as
the documented fallback, and the `stream` endpoint always returns it.

**A single transport — detections multiplexed into the video stream.** Removes
the synchronisation problem entirely, at the cost of the separation that makes a
box inspectable data rather than pixels somebody painted, and that lets a refusal
appear where a detection would have.

**GraphQL.** Rejected: five screens with a well-known shape, one client, and a
requirement that the schema be generated from Pydantic models that already exist
for the outbound contract. REST plus a generated OpenAPI document is less
machinery for the same result.

**Server-sent events instead of a WebSocket.** Adequate for one-way push, and
rejected because the client needs to subscribe and unsubscribe as the operator
moves between the grid and a focused camera, and doing that over a second channel
is worse than having one bidirectional one.

**Redux or Zustand.** Rejected: almost all state here is server state, and a
query cache models that better than a store somebody has to keep in sync.

**Keeping the pre-issued recovery codes from ADR 0024.** Rejected in favour of
the local administrator reset, above — a printed code at an unstaffed post is not
clearly safer than a named colleague whose reset is recorded.

**Path versioning on `/api`.** Rejected as ceremony for an internal contract with
one client shipped alongside it. The version that matters is RFC 0005's, on the
payload that leaves the building.

## Cross-cutting concerns

**Authorisation.** One role distinction exists — `can_reset` — because ADR 0016
cut the people-and-roles screen. Every other authenticated user can do everything
else. That is a deliberate simplification for a one-operator post, and it is
recorded here so a later multi-user site knows exactly which assumption to
revisit.

**Attribution.** Every mutating endpoint records the session's user on the row it
writes. There is no action a person can take that the record cannot attribute.

**Refusals are content, not errors.** A camera that cannot do ANPR, a recorder
that will not serve playback, a rule that cannot run — each returns `200` with a
sentence. The console never composes its own wording for any of them, so a
refusal reads identically in the chip row, the rule card and the timeline.

**No invented vocabulary.** No endpoint returns "intruder", "threat", "risk" or a
score, because nothing computes one.

**Offline.** The console is served from the same machine as the API. Fonts,
icons and the photograph are bundled; nothing is fetched from a CDN. A site with
no link for three days loses nothing but the emailed password reset, which is why
the local one exists.

**Transport security.** HTTPS with a self-signed certificate generated at
install, because a site with no internet has no path to a public CA. The cookie
is `Secure`, which requires it. The certificate's fingerprint is shown at
commissioning so the operator can recognise their own machine.

**Failure visibility.** A dropped WebSocket reconnects with backoff, and the
console says it is reconnecting rather than showing stale boxes. A camera that
stops delivering shows its state and how long it has been that way. Neither is
drawn in an error colour — ADR 0030 reserves attention for things that want
attention, and a camera being offline is a fact.

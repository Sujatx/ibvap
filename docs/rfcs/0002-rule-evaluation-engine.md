# 0002. Rule evaluation engine

**Status:** Accepted
**Author:** Sujat
**Date:** 2026-09-03

## Context and scope

[ADR 0012](../adr/0012-suspicious-activity-as-operator-authored-rules.md) makes
a commitment the rest of the platform has to honour: "suspicious activity" is
not a model output, it is something an operator composes out of primitives that
are individually reliable. That decision only means anything if the composition
layer actually exists and is expressive enough that an operator does not need a
model to describe what they care about.

This RFC specifies that layer. It sits between
[RFC 0006](0006-detection-and-analytics-primitives.md), which produces a
`FrameAnalysis` per analysed frame, and
[RFC 0003](0003-event-store-and-alert-state.md), which persists what the rules
decide is worth recording.

Two other ADRs land here.
[ADR 0011](../adr/0011-virtual-fence-plus-open-border-framing.md) ships the
virtual fence in full and adds an open-border framing: the reportable condition
can be class, time, direction, dwell or accompaniment rather than the crossing
itself — which is a statement about this engine's condition vocabulary.
[ADR 0013](../adr/0013-night-time-movement-detection-as-explicit-capability.md)
makes night an explicit operating mode, which means rules must be scopeable to
it.

Out of scope: the models (RFC 0006), the schema and retention
(RFC 0003), the rule editor's interaction design — the hi-fi S-03 frames own
that, and this RFC serves them rather than the reverse — and egress
([RFC 0005](0005-c2-event-egress-publisher.md)).

## Goals and non-goals

**Goals**

1. A rule model expressive enough for the virtual fence, loitering, night
   movement, ANPR and the composite conditions ADR 0012 promises.
2. Geometry that survives a camera resolution change without silently moving a
   fence.
3. Timers that survive a tracker identity switch without resetting or
   double-firing.
4. One crossing producing one Event.
5. Rules refused on cameras that cannot support them, in the same voice
   RFC 0001's capability verdicts use.
6. A stated interaction with mute and snooze, so a muted rule still logs.

**Non-goals**

- Learned or statistical anomaly detection of any kind. Excluded by ADR 0012 and
  not smuggled back in as a "baseline deviation" condition.
- Plate watchlists. This build reads a plate and records it on the Event.
  Matching a read against a list of plates of interest is a product capability
  nobody has specified, and inventing it here would violate
  [CLAUDE.md](../../CLAUDE.md) rule 2.
- Cross-camera correlation. One rule, one camera, for this build.
- The starter rule library. ADR 0012 marks it unvalidated and
  [ADR 0016](../adr/0016-mvp-ui-cut-to-five-screens.md) cuts it from the MVP.

## Design

### Anatomy of a rule

A rule is five independent choices, and every screen, endpoint and stored row
follows the same five:

```
  WHERE     geometry      zone polygon | tripline | whole frame
  WHAT      class filter  person | vehicle | face | plate | movement
  WHEN      schedule      always | time window | night-scoped
  CONDITION what counts   crossing, presence, dwell, count, accompaniment, absence
  ACTION    consequence   log an Event | log an Event and raise an Alert
```

Separating them is what makes the vocabulary open-ended without a combinatorial
UI: "a vehicle dwelling for more than 5 minutes inside the approach zone after
dark, and alert me" is one path through five orthogonal choices, not a preset.

`ACTION` is deliberately binary. There is no severity, no priority, no score —
[ADR 0030](../adr/0030-dark-console-palette-no-severity-colour.md) makes
alert-versus-logged a binary and never a scale, and the engine is where that
binary is decided.

### Geometry

**Stored normalised, evaluated in pixels.** A zone is stored as coordinates in
`[0, 1]` against the *encoded* geometry of the stream it was drawn on, together
with the encoded width and height at drawing time. At evaluation the normalised
coordinates are multiplied back up by the current encoded geometry.

This matters more than it looks. The rig delivers 960×1080 and displays
1920×1080; a fence stored in display pixels and evaluated against encoded pixels
is wrong by exactly a factor of two, in the direction that quietly halves the
protected area. Storing normalised, with the geometry it was drawn against
recorded alongside, means a recorder reconfiguration is detectable — the stored
geometry no longer matches the live one — rather than silently corrupting.

**The ground point is the bottom-centre of the box**, not its centre. A person
standing at the edge of a zone has a box whose centre is a metre above the
ground and possibly outside the zone; the point where they are actually standing
is the bottom-centre. Every membership and crossing test uses that point.

**Zones are Shapely polygons.** Point-in-polygon by ray casting is what Shapely
does, correctly, including the self-intersecting polygons an operator will draw
by accident. A `prepared` geometry is built once per rule version and reused, so
the per-frame cost is a bounding-box reject for almost every test.

**A tripline is a directed segment.** Crossing is detected between the track's
previous and current ground point:

```
crossed  = segments_intersect(prev → curr, line.a → line.b)
direction = sign of cross(line.b − line.a, curr − prev)
```

The sign gives which way, so a rule can require *in* only, *out* only, or either
— the direction condition ADR 0011 names.

Geometry is 2D image space, not ground plane. A homography onto the ground would
give real distances, and needs a calibration step nobody can perform in the
under-an-hour commissioning the constraints allow. That limitation is declared,
in RFC 0006's maturity table, rather than hidden.

### Conditions

| Condition | Needs a track | Meaning |
|---|---|---|
| `crosses` | yes | Ground point crossed the tripline, optionally in a stated direction |
| `enters` / `exits` | yes | Ground point moved into or out of the zone |
| `present` | no | A detection of the class is inside the zone on this frame |
| `dwell` | yes | A track has been continuously inside the zone for ≥ N seconds |
| `count` | no | ≥ N detections of the class inside the zone on this frame |
| `accompanied` | yes | A track of class A inside the zone while ≥ N of class B are too |
| `absent_for` | no | No detection of the class inside the zone for ≥ N seconds |
| `movement` | no | MOG2 movement covering ≥ X% of the zone |
| `plate_read` | yes | A plate was read from a vehicle track inside the zone |
| `watchlist_match` | yes | A face on a track inside the zone matched an enrolled watchlist subject |

`movement` is the one that carries ADR 0013: it does not depend on the detector
recognising anything, which is exactly what makes it useful on an IR frame where
the detector sees nothing. `absent_for` is the open-border inverse ADR 0011
asks for — a patrol road with nothing on it for six hours can be as reportable
as one with something on it. `watchlist_match` is
[ADR 0059](../adr/0059-face-recognition-ships-against-a-configured-watchlist.md)'s
condition — it is refused, like every other condition, on a camera whose
`face_recognize` capability is refused, whether that refusal is for pixels or
because recognition is not configured for the deployment at all.

### Composition

A rule's condition is a single expression over the table above:

```
condition := primitive
           | condition AND condition
           | condition OR condition
           | NOT primitive
```

No nesting beyond that, no arithmetic, no user-supplied code. It is deliberately
a small language: an operator has to be able to read a rule back and know what it
does, and a reviewer has to be able to tell an over-broad rule from a precise one
at a glance.

Both sides of an `AND` are evaluated against the same frame and the same zone.
"A person and a vehicle in the zone at the same time" is expressible; "a person
in zone A while a vehicle is in zone B on another camera" is not, and is named
as out of scope above.

### Schedules, and what "night" means

Three schedule kinds:

- **Always.**
- **Time window** — one or more local-time ranges, with the days they apply on.
- **Night-scoped** — active whenever the camera reports `infrared` illumination.

Night is scoped on the **measured illumination mode, not the clock**. A clock
says it is 19:40; it does not say whether this particular camera has switched to
IR, which depends on the season, the lens, the site lighting and whether the
camera is under a floodlight. Since the platform already measures illumination
per frame (RFC 0006), using it is both more accurate and more honest — and it
degrades sensibly at a site whose clock is wrong, which
[ADR 0034](../adr/0034-local-event-store-on-sqlite.md) says will happen.

A time window is evaluated against the camera's local time, and an Event that
fires under a suspect clock carries the suspect flag through unchanged.

### Timers, and surviving an identity switch

`dwell` and `absent_for` need state that outlives a frame. Dwell timers are keyed
on `(rule_version_id, camera_id, track_id)` and hold the time the track entered
the zone.

ByteTrack will lose and re-acquire identity — through occlusion, through a frame
drop, through two people crossing. Naively keyed, that resets a dwell timer and a
loiterer never trips a five-minute rule. The engine therefore applies a **grace
window**: when a track disappears, its timer is retained for a few seconds, and a
new track appearing within that window whose first ground point is close to the
lost track's last one inherits the timer.

The inheritance rule is deliberately conservative — same zone, short window,
small distance — because the failure it prevents (a rule that never fires) is
recoverable by the operator noticing, whereas the failure it could introduce (a
timer transplanted onto the wrong person) is evidence that says something untrue.
Where it cannot be sure, it starts a new timer, and the rule fires late rather
than wrongly.

### Debounce

One crossing produces one Event.

Each rule holds a per-track cooldown: once a rule fires for a track, it will not
fire again for that track until the cooldown elapses *and* the condition has gone
false in between. The second half is what stops a track sitting exactly on a
tripline from generating a stream of events as the ground point jitters across
it.

The cooldown is a property of the rule, not a global constant, because the right
value for a tripline (seconds) and for a dwell rule (minutes) are different, and
an operator who cannot change it will get either duplicates or silence.

### Capability gating

A rule is refused, not silently ignored, when the camera cannot support it:

- The class it filters on is refused on that camera — an ANPR rule on a camera
  whose plate verdict is `refused`, or a `watchlist_match` rule on a camera
  whose `face_recognize` verdict is `refused` — including the case where
  recognition is not configured anywhere in the deployment, which refuses the
  condition on every camera at once rather than camera by camera.
- It needs a track and the camera cannot sustain the 3 analysed fps that
  multi-object tracking needs (RFC 0001).
- Its geometry no longer matches the camera's encoded geometry, because the
  recorder was reconfigured under it.

In each case the rule is stored, shown, and marked refused with a sentence
naming the reason — the same treatment
[ADR 0007](../adr/0007-refuse-unsupported-capabilities-not-degrade.md) gives a
capability. A refused rule never fires and never silently half-works.

### Mute is not suppression of the record

When a rule fires, an Event is written **always**. If the rule is an alerting
rule, an Alert is raised **unless** a mute is active for that camera-and-rule
pair.

That ordering is the whole point of
[ADR 0027](../adr/0027-suppression-works-like-notification-snooze.md): a snooze
silences the notification, not the log. An operator who mutes a noisy camera for
a week still has a complete record of what happened during that week, which is
what makes muting safe to offer at all.

The mute state itself, its duration and its reversal live in RFC 0003. The engine
only consults it, at the one point marked above.

### Rule versions

Editing a rule creates a new version rather than mutating the old one, and every
Event records the `rule_version_id` that fired it.

Without this, an Event says "fired by the North Gate fence rule" and the North
Gate fence rule has since been redrawn, so the record no longer describes what
actually happened. With it, an event from three weeks ago can still be shown
against the geometry that produced it. Versions are cheap — a rule is a few
hundred bytes — and the alternative is evidence that quietly rewrites itself.

### Evaluation loop

Per analysed frame, per camera:

1. Fetch the active rule versions for this camera (cached; invalidated on edit).
2. Drop rules whose schedule is not active, and rules currently refused.
3. For each remaining rule, evaluate its condition tree against the frame's
   tracks, detections and movement regions.
4. For each satisfied rule, check the debounce; if it passes, emit a `RuleMatch`.
5. Hand every `RuleMatch` to the event writer, which owns the transaction.

Cost is bounded by rules-per-camera rather than by frame size: the expensive
operation is point-in-polygon against a prepared geometry, at a handful of
tracks × a handful of rules. This is not where the machine's time goes; decode
is.

## System-context diagram

Where this sits in the whole system: the
[container view](../architecture/diagrams/c4-l2-container.md).

The detailed diagrams for this RFC — the evaluation loop and the track-timer state machine — are still owed, and are tracked
as remaining Phase 3 work rather than assumed to exist.

## APIs

Internal. The wire form the S-03 editor uses is RFC 0004's, derived from these.

```python
Klass = Literal["person", "vehicle", "face", "plate", "movement"]

class Geometry(BaseModel):
    kind: Literal["zone", "tripline", "frame"]
    points: list[tuple[float, float]]     # normalised 0..1, encoded geometry
    drawn_encoded_width: int
    drawn_encoded_height: int


class Primitive(BaseModel):
    condition: Literal["crosses", "enters", "exits", "present", "dwell",
                       "count", "accompanied", "absent_for", "movement",
                       "plate_read"]
    klass: Klass
    direction: Literal["in", "out", "either"] | None = None
    seconds: float | None = None          # dwell, absent_for
    threshold: int | None = None          # count, accompanied
    fraction: float | None = None         # movement
    companion_klass: Klass | None = None  # accompanied


class Condition(BaseModel):
    op: Literal["primitive", "and", "or", "not"]
    primitive: Primitive | None = None
    operands: list["Condition"] = []


class Schedule(BaseModel):
    kind: Literal["always", "window", "night"]
    windows: list[tuple[time, time]] = []
    days: list[int] = []                  # 0 = Monday


class RuleVersion(BaseModel):
    rule_id: int
    version: int
    camera_id: int
    name: str
    geometry: Geometry
    condition: Condition
    schedule: Schedule
    alerting: bool
    cooldown_seconds: float
    enabled: bool
    refused_reason: str | None = None     # a full sentence when refused


@dataclass(frozen=True, slots=True)
class RuleMatch:
    rule_version_id: int
    camera_id: int
    captured_at: datetime
    clock_trusted: bool
    alerting: bool
    primary_class: Klass                  # see RFC 0003 -- exactly one
    class_mixed: bool
    track_ids: list[int]
    boxes: list[tuple[int, int, int, int]]
    plate_read: PlateRead | None
    illumination: Literal["colour", "infrared"]
```

## Data storage

Owned by RFC 0003; what this RFC fixes is what must be stored:

- `rules` — identity, camera, name, enabled, current version pointer.
- `rule_versions` — one row per edit: geometry, condition tree (JSON), schedule,
  alerting flag, cooldown, and the encoded geometry it was drawn against.
- `mutes` — read by the engine at alert time, written by the triage flow.

Timer and debounce state is **in memory only**. It is rebuilt from scratch on
restart, which loses in-flight dwell timers — a five-minute loiterer restarts
their five minutes across a process restart. That is the correct trade: the
alternative is a database write per track per frame, and a restart at a site is
rare while that write is constant.

## Alternatives considered

**Hand-rolled ray casting instead of Shapely.** Tempting for a dependency-free
engine, rejected because the edge cases — a point exactly on an edge, a
self-intersecting polygon an operator drew by dragging back over themselves, a
zone with a hole — are exactly the ones a hand-rolled implementation gets wrong,
and they are the ones that produce a fence with a silent gap in it.

**Ground-plane homography for real-world distances.** Would let a rule say "5
metres" instead of "inside this shape", and would make dwell-plus-speed
conditions possible. Rejected for this build because calibration needs a site
survey and known reference distances, and the constraints require commissioning
by a non-specialist in under an hour with no survey.

**A general complex-event-processing engine.** Rejected on the same grounds the
condition language is kept small: an operator has to read a rule back and know
what it means, and a CEP query language optimises for expressiveness at the cost
of exactly that.

**Storing zones in display coordinates.** Rejected above — it is the mistake that
halves a fence on an anamorphic stream, and it fails silently.

**Firing on every frame the condition holds, and de-duplicating downstream.**
Rejected: it moves the debounce into the store, where the decision has less
context — the store cannot tell a jittering ground point from a second person.

**Mute suppressing the Event as well as the Alert.** Rejected by ADR 0027, and
worth restating: an operator mutes to stop being interrupted, not to stop
recording, and conflating the two turns a convenience into a gap in the record.

## Cross-cutting concerns

**Attribution.** Every rule version records who wrote it and when. An Event
therefore traces to a rule, to a version of that rule, to a person, and to a
time — the attributable-actions requirement, satisfied by construction rather
than by a separate audit log.

**No invented vocabulary.** The engine has no notion of "intruder", "threat" or
"suspicious". It has classes, zones, times and conditions, and the rule's name is
whatever the operator called it.

**Determinism.** Given the same `FrameAnalysis` sequence and the same rule
versions, the engine emits the same matches. The only state that is not a pure
function of the input is the timer table, and its behaviour on restart is stated
above rather than left to be discovered.

**Failure mode.** A rule whose condition tree cannot be evaluated — a corrupt
geometry, a class the camera no longer reports — is marked refused with a reason
and skipped. It never throws into the analytics loop, and it never silently
evaluates to false, because a fence that stopped working and said nothing is the
worst outcome available.

**Observability.** Per rule: fires per hour, fires suppressed by debounce, fires
suppressed by mute, and current refusal state. The ratio of the first to the
third is what tells an operator a rule is badly drawn, and it is the input to the
noisiest-camera-and-rule view ADR 0022 describes for a later build.

# 10. Risks and Open Items

What is genuinely undecided, what is deliberately deferred, and what looks
like a gap but is actually a stated per-deployment fact rather than a fixed
number this design withholds. Consolidated from all six RFCs and
`docs/architecture/README.md` §11, so a reviewer finds every open thread in
one place rather than six.

## Contents

- [Genuinely open](#genuinely-open)
- [Established as a per-deployment fact, not a fixed number](#established-as-a-per-deployment-fact-not-a-fixed-number)
- [Deliberately deferred](#deliberately-deferred)
- [Accepted trade-offs](#accepted-trade-offs)
- [Diagrams still owed](#diagrams-still-owed)

## Genuinely open

| Item | Why it's open | Where it will be settled |
|---|---|---|
| Process supervision on the site machine | A decoder crash takes the API down with it ([ADR 0050](../../adr/0050-single-process-inference-placement.md)); nothing yet restarts either process | Deployment work [ADR 0033](../../adr/0033-backend-framework-packaging-and-auth.md) explicitly defers |
| The starter rule library | Marked unvalidated by [ADR 0012](../../adr/0012-suspicious-activity-as-operator-authored-rules.md) and cut from the MVP by [ADR 0016](../../adr/0016-mvp-ui-cut-to-five-screens.md) | Needs real operating data before it is worth writing |

## Established as a per-deployment fact, not a fixed number

These look like unmeasured gaps but are deliberate design choices: the right
answer depends on hardware and recorder firmware this repository cannot
generalise from one developer's rig, so the design commits to *how it is
measured continuously in production* rather than to a number.

| Item | How it is established |
|---|---|
| Decode throughput for concurrent streams | Per-camera fps and drift telemetry, continuously, per site (RFC 0001, Decode throughput) |
| Recorded-video retrieval route | Tried — ONVIF Profile G, vendor RTSP playback, or recorder files — against whatever recorder a site actually has, at commissioning; refused on every camera if none succeed (RFC 0001, Recorded-video retrieval) |
| Whether a two-RTSP-session load (analytics + go2rtc) is sustainable on a given recorder's shared bandwidth | Observed per site; the stated retreat is go2rtc taking the sub-stream |

## Deliberately deferred

| Item | Deferred by | Condition that reopens it |
|---|---|---|
| Containerisation | [ADR 0033](../../adr/0033-backend-framework-packaging-and-auth.md) | A second deployment site, or a machine where Python/CUDA versions cannot be pinned by hand |
| ONVIF Profile M / MISB ST 0903 egress | [ADR 0006](../../adr/0006-c2-integration-via-generic-event-contract.md) | A named consumer that requires a standards-conformant profile |
| An egress classification/release-filter field | [ADR 0020](../../adr/0020-egress-classification-field-deferred.md) | The deployment's data-classification policy becomes known |
| Case management, evidence export, audit-log and people-and-roles screens | [ADR 0016](../../adr/0016-mvp-ui-cut-to-five-screens.md) | A later phase, if the product scope grows |
| Ground-plane homography for real-world rule distances | RFC 0002, Alternatives considered | A calibration step becomes compatible with under-an-hour commissioning |

## Accepted trade-offs

Not risks to resolve — decisions made with the cost stated up front:

- **Dwell/absence timer state does not survive a process restart.** Rebuilt
  from nothing; a loiterer's clock restarts. Accepted over a database write
  per track per frame (RFC 0002, Data storage).
- **ANPR and face detection are refused on wide-area cameras below their
  pixel floor.** A fact about camera placement, not a defect in either
  capability — demonstrable on footage that clears the floor via the
  file-backed source
  ([ADR 0060](../../adr/0060-file-backed-frame-source-for-testing.md)), but
  genuinely unavailable on this development rig's own five channels (RFC
  0006, Per-capability detail).
- **The face-recognition pixel floor (72 px) is carried over from a prior
  estimate**, pending validation once a real watchlist gallery exists to
  measure against (RFC 0006, Face recognition) — flagged rather than
  presented as settled.
- **The model manifest's `face_recognizer` input shape (112×112) has not been
  independently verified** against the shipped ONNX file's own metadata; the
  hash check exists precisely so a mistyped or assumed shape cannot silently
  diverge from the artefact that actually ships (RFC 0006, Model manifest).

## Diagrams still owed

Every RFC names its detailed diagrams as not yet drawn, tracked as remaining
Phase 3 work rather than assumed to exist. The Mermaid figures embedded in
this system-design set (context, container, cascade, pipeline, ER, deployment)
cover the whole-system shape; still missing are the fine-grained sequence and
state diagrams: camera connection state machine, capability-measurement
flowchart, rule evaluation/track-timer state machine, alert and mute state
machines, retention sweep, egress retry/dead-letter flow, and the per-screen
UI sequences (live view, sign-in, alert triage, timeline playback). None of
these gaps are hidden inside their owning RFCs — this is the one place they
are all listed together.

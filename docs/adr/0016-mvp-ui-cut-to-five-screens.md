# 16. MVP UI cut to five screens — exactly the problem statement, nothing built around it

**Date:** 2026-08-26
**Status:** Accepted

## Context

Built and reviewed against the prior 27-screen `UX.md`/`MVP.md` scope (22
of 27 screens tagged "Core" — a label that had stopped discriminating),
the call made was: build exactly what the problem statement names, as a
finished product, and nothing else. Case management, evidence
chain-of-custody, and the legal/authority governance apparatus are real
needs for an actually-deployed force, but they are not named in
`problem.md` and are not what a demo build should carry. If IBVAP moves
past MVP, they are the first candidates to come back — deferred, not
disproven.

## Decision

The MVP interface is five screens: **Sign in, Live View, Rules, Alerts &
Events, Integration.** Every named SIH capability (human/vehicle/face
detection, ANPR, virtual fence, suspicious activity, night-time movement,
real-time alerting and event logging, C2 integration) is satisfied inside
these five — detection classes are overlays and filters on Live View and
Alerts & Events, not screens of their own.

Cut entirely from the build — not merged, not simplified, removed: Case
management and evidence-pack export; watchlist/gallery face-recognition
matching and its legal-gate workflow; a dedicated camera-capability
certification screen (the underlying honesty behaviour survives as an
inline state on Live View — a class that can't be trusted on a camera
simply doesn't draw, with a reason, no separate gate screen or override
ceremony); audit log, authority records, people & roles as management
screens; measurement and system-health dashboards; starter rule library;
annunciator display mode; a "what IBVAP does not detect" screen.

This narrows what
[0005](0005-core-workflows-modelled-around-artefacts-and-states.md)
(artefact-modelled workflows — Case is no longer a built artefact),
[0007](0007-refuse-unsupported-capabilities-not-degrade.md) (refuse via a
dedicated gate screen — the refusal now lives inline), 
[0008](0008-face-detection-unconditional-gated-recognition.md) (recognition
*matching* no longer ships; detection still does), and
[0010](0010-support-posture-analytics-layer.md) (support-posture layer,
which assumed the fuller governance surface) had each committed to. It
does not reverse the underlying honesty or non-goal principles those
decisions established — those survive as cross-cutting rules inside the
five screens, not as screens of their own.

## Consequences

[UX.md](https://www.figma.com/design/ZDrrYveQkuzTFD9VufbQZO/IBVAP-%E2%80%94-Product-Design?m=auto&t=crzSM6HZroTo7LFV-6) rewritten to five screens.
[PRD.md](https://app.notion.com/p/3c986dda46e28195ba55dd42265e7072?pvs=204) §6 rewritten to match, and later merged with
the standalone `MVP.md` this decision originally produced (see
[0028](0028-mvp-md-merged-into-prd-md.md)).

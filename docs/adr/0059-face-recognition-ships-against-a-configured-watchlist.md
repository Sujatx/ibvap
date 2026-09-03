# 59. Face recognition ships against a configured watchlist, using SFace, exactly as 0008 gated it

**Date:** 2026-09-03
**Status:** Accepted, narrows 0016; extends 0051

## Context

[0008](0008-face-detection-unconditional-gated-recognition.md) specified, at the
outset, exactly how recognition could ship: unconditional detection, plus
recognition technically blocked in a real deployment unless four conditions are
configured and current — a recorded legal basis, an authority record (never
treated as evidence that the legal basis exists), a bounded gallery, and
retention/oversight requirements — while remaining exercisable in a controlled
development/test environment against an explicitly configured, bounded gallery.
[0016](0016-mvp-ui-cut-to-five-screens.md) then cut "watchlist/gallery
face-recognition matching and its legal-gate workflow" from the five-screen MVP
build entirely, for scope reasons: the case-management and governance apparatus
a real deployment needs is not named in the problem statement, so it was
deferred rather than built.

[docs/problem-statement.md](../problem-statement.md)'s Expected Solution
paragraph states the platform should "Support facial recognition, vehicle
identification, and behavioral analytics through software" — language distinct
from, and broader than, the capability list's "Face detection." Building to
that sentence, not only to the capability list, is a product scope call, made
here: reopening the specific item 0016 deferred, before RFC 0004's frontend
contract is written against it.

[0051](0051-face-detection-model-and-refusal-threshold.md) chose YuNet for
detection and discarded its five landmarks, because their only use is aligning
a face for recognition and recognition wasn't built. It also said explicitly
that reinstating recognition "requires the four conditions 0008 sets and a new
decision — not a configuration change." This is that decision.

## Decision

**Recognition ships as matching against a locally-held, bounded watchlist
gallery, using SFace (a MobileFaceNet-architecture embedding model, OpenCV Zoo,
Apache-2.0) on top of YuNet's detection box and landmarks. It is technically
blocked — the model is never loaded and no verdict is computed — until an
administrator has explicitly configured and attested all four conditions 0008
named: a legal-basis reference, an authority-record reference, the bounded
gallery itself, and a retention period. Configuring the four fields does not
itself enable matching; an administrator additionally toggles it on, because
0008 is explicit that a record's existence is never treated as evidence that
the legal basis it names is valid.**

SFace is chosen over the InsightFace-family embeddings (ArcFace, SCRFD-adjacent
models) for the same reason 0051 picked YuNet over SCRFD: those weights carry a
non-commercial research restriction, and this repository already carries one
AGPL encumbrance from the detector — a second, incompatible restriction on the
one capability with the highest consequence for being wrong is not a trade
worth making for accuracy. SFace's own accuracy figure — 99.60% on the LFW
benchmark, at a documented cosine-similarity threshold of 0.363 (equivalently,
an L2-norm threshold of 1.128) — is a number under LFW's conditions, not a claim
about a 960-px-wide 1080N crop at a border checkpost, and RFC 0006 records it
that way, per [0002](0002-differentiate-on-deployment-not-benchmark-accuracy.md).

YuNet's five landmarks, which 0051 discarded, are retained when recognition is
configured and enabled: SFace's alignment step consumes them before computing
an embedding. This does not reopen 0051's detector choice — YuNet remains the
correct choice for *detection* regardless of whether recognition runs on top of
it.

A face-recognition capability verdict (`face_recognize`) is measured and gated
the same way every other capability is: refused outright when recognition is
not configured for the deployment, and refused per camera when a face box does
not clear a pixel floor higher than detection needs, because an embedding is
far more sensitive to resolution than a bounding box.

A match produces an Event and, if the matching rule is alerting, an Alert —
through the same rule engine, event store and assessment workflow every other
capability uses. There is no separate automated action. An operator assesses a
watchlist match exactly as they assess any other alert: real, not real, or
unsure.

## Consequences

This narrows 0016's cut to exactly the matching *capability and its technical
gate* — not the case-management, evidence chain-of-custody, audit-log-as-a-
screen, or authority-record-as-a-management-screen items 0016 also cut, none of
which this ADR reinstates. The four conditions are held as configuration (a
`watchlist_config` row, [RFC 0003](../rfcs/0003-event-store-and-alert-state.md)),
not as the fuller governance workflow — for a controlled demonstration or test
environment this is exactly what 0008 already permits, and for a real
deployment the legal-basis and authority-record fields are references to
records that exist outside this product, not documents this product manages.

RFC 0004's screen-by-screen trace cannot cite a hi-fi frame for watchlist
enrollment or match review, because none exists in the twelve frames Phase 2
built. That is a genuine gap against [CLAUDE.md](../../CLAUDE.md) §2's
four-homes rule: the product requirement belongs in the Notion PRD and the
screens belong in Figma, and neither has been updated to carry this yet. RFC
0004 records the API contract this ADR requires and names the gap rather than
inventing screens to fill it.

An embedding is a biometric template. It is held under the same retention
clock as any other artefact, is never exported, and every match is logged with
the subject, the similarity score, and the threshold used at match time — so a
threshold changed later does not retroactively make old matches unreadable
evidence of what was actually decided at the time.

This is the second time this decision log has had to say, out loud, that a
capability exists because the problem statement's own words support it, and
that the platform's answer to "can it be wrong at a border" is to gate it, log
it, and never automate past a human — the same posture 0008 established, for
exactly this reason.

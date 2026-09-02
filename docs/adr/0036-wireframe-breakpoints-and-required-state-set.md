# 36. Three console widths, and the state set a screen is not finished without

**Date:** 2026-09-01
**Status:** Superseded by [0039](0039-state-coverage-evidenced-three-ways.md)

## Context

`01 Wireframes` carried five frames: one screen, one state, one width each.
They were faithful to the decisions recorded here — the capability-refusal
wording, the mute sentences, the queue behaviour all came out right — but
they drew only the case where everything works. No loading, no empty, no
failure, no in-progress, no hover explanation, and no indication of what
happens when the window is not exactly 1440 × 900. A frontend track cannot
be scoped from that, and the gap was not going to be noticed screen by
screen; it needed a rule.

A reference mock supplied for the rebuild was denser and covered far more of
the interaction surface, which is why it was used. It also contradicted a
dozen accepted decisions — severity colour on every alert row, a coloured
real/not-real/unsure triad, eight navigation items, a geospatial map, PTZ
controls and a recorded-video scrubber. Those were refused one by one
against [0007](0007-refuse-unsupported-capabilities-not-degrade.md),
[0008](0008-face-detection-unconditional-gated-recognition.md),
[0016](0016-mvp-ui-cut-to-five-screens.md),
[0017](0017-cameras-site-sketch-not-a-map.md),
[0018](0018-operator-assigned-impact-grade.md),
[0023](0023-dismissal-cause-captured-on-suppression.md),
[0024](0024-session-lockout-and-recovery-for-one-person-site.md),
[0030](0030-dark-console-palette-no-severity-colour.md) and
[0031](0031-component-grammar-chip-states-fact-segmented-control-chooses.md),
plus [CLAUDE.md](../../CLAUDE.md) rule 2 for the features the problem
statement does not name.

Two of the reference's departures were not refused. Its sign-in — username
and password, "remember me", a password reset — was adopted on an explicit
instruction after the conflict with
[0024](0024-session-lockout-and-recovery-for-one-person-site.md) was raised
twice; [0037](0037-sign-in-follows-the-reference-username-password.md)
records that decision and supersedes 0024. Its "Government of India" footer
was adopted on the same instruction. The reference's SSO button and theme
switcher were drawn and then removed.

Refusing the rest once, in a rebuild, is cheap.
Refusing them again on every future screen is not, which is the second
reason this needs to be written down rather than remembered.

## Decision

**Three widths: 1920, 1440 and 1280.** These are console-class widths, which
is what a BOP post terminal is. There is no tablet tier and no mobile tier:
the problem statement names no mobile surface, a video wall does not fold to
a phone, and inventing a sixth screen's worth of mobile triage would be
inventing a requirement. Across those three widths the navigation rail
collapses to an icon rail at 1280, the fourth column becomes a right-anchored
overlay drawer at 1280, and the live grid drops from 3×3 to 2×2. No page
scrolls horizontally at any width; wide content scrolls inside its own
container.

**A screen is not finished until it draws seven states:** loading, empty,
filtered-empty, error, in-progress, tooltip or inline explanation, and
collapsed chrome. Where a state cannot exist the screen says so rather than
skipping it silently — Sign in has no collection, so it has no empty state,
and that is a fact about the screen and not a gap in it.

Layout frames are drawn at all three widths. State frames are drawn at 1440,
and additionally at 1280 only where the responsive behaviour itself differs.

## Consequences

`01 Wireframes` now holds 75 frames across five screens and a shell section,
in greyscale, one section per screen, with the five superseded frames
moved to `99 Archive` under `Superseded — 2026-08`. The reference images stay on `99 Archive`, renamed to
say plainly that they are not the design and which decisions they contradict.

Drawing every state surfaced what the UI kit does not yet cover — thirteen
components missing outright, six needing new variants, two needing changes
before they survive the responsive rule. That list is recorded as a
`Kit gaps` section on `02 UI Kit` and is the input to the hi-fi pass; nothing
on it was built here.

Two things this deliberately does not do. It does not settle colour: these
frames are greyscale primitives, they bind to no token, and the raw-fill
sweep [0031](0031-component-grammar-chip-states-fact-segmented-control-chooses.md)
requires does not apply to them — it applies when the hi-fi screens are
assembled from the kit. And it does not touch `PayloadPreview`,
`MuteDurationMenu` or the alert detail's hand-built record list, which
[0031](0031-component-grammar-chip-states-fact-segmented-control-chooses.md)
knowingly left duplicating later generics.

The frames sit in sections rather than groups for a concrete reason: a
prototype NAVIGATE destination must be a top-level frame, and a frame nested
in a group is not one. Grouping the rows silently broke prototyping. A basic
flow is wired — sign in, the navigation rail across all five screens, opening
a camera and returning, and the assess → mute → cause sequence on Alerts —
with `Sign in` as the flow starting point.

[ROADMAP.md](../../ROADMAP.md) Phase 2 Task 1 is complete. Task 2 — the five
hi-fi screens on `03 Hi-fi` — is unblocked, and starts by building the kit
gaps rather than by drawing a screen.

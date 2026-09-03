# 47. The rail's collapsed state is baked frame pairs, not a runtime variant swap

**Date:** 2026-09-03
**Status:** Accepted — narrows [0041](0041-hi-fi-assembled-from-an-appshell-component.md); applies to the Figma prototype only, narrowed by [0057](0057-hi-fi-frames-are-the-ui-specification.md)

## Context

Testing the prototype in Figma's Present mode surfaced a bug 0041 could not
have caught by inspection alone: with the rail expanded, clicking between
screens updated the active nav highlight correctly; collapse the rail first,
and the highlight went stale — the page changed, the rail did not reflect it.
A read-only audit of every `AppShell` instance and every nav item's `NAVIGATE`
reaction showed the authored data was correct in both states. The defect was
Present mode's own behaviour: `AppShell`'s `Collapse control` used `CHANGE_TO`,
and Figma's Interactive Component memory carries a component's whole resolved
variant state forward across a `NAVIGATE`, unless the reaction that navigates
away resets it — and that reset is all-or-nothing per instance, not
per-property. Setting `resetInteractiveComponents: true` on the cross-page
reactions fixed the highlight and broke the collapse itself: every navigation
now forced the rail back open.

A second, older bug came out of the same investigation. Every screen's visible
content — the rule builder, the camera grid, the alert list — turned out to be
a sibling frame next to the `AppShell` instance, not nested inside its content
slot, absolutely positioned at `x: 240` to match the Expanded rail's width.
Resizing or swapping the instance alone never moved it. 0041's `Rail=Collapsed`
variant, drawn at a smaller 1280×800 canvas, hid this: the whole frame shrank,
so the dead 176px gap between rail and content was never visually exposed.
Once collapse stayed at the Expanded frame's own 1440×900 (the fix in the
superseded plan section below this one), the gap became visible on every
screen — a pre-existing defect, not one this change introduces.

## Decision

**Every real screen gets a second, fully-baked Collapsed frame, and collapse
becomes `NAVIGATE`, not `CHANGE_TO`.** For each of the five screens — S-02
grid, S-02 focused camera, S-03 Rules, S-04 Alerts, S-05 Integration — the
Expanded frame is cloned, the clone's `AppShell` instance is set to
`Rail=Collapsed` as a real persisted change, and its content sibling is
repositioned (`x: 240 → 64`) and widened (`1200 → 1376`, absorbed by each
screen's auto-layout `FILL` column; S-02 focused camera's two `FIXED`-width
columns needed an explicit resize instead). `Collapse control` on each frame
now navigates to the other frame of its pair with a `SMART_ANIMATE`
transition; every other nav reaction on a Collapsed frame — rail items and,
where present, in-content links such as a camera tile or an alert action —
targets the Collapsed clone of its destination, not the Expanded one. No
Figma Variable or Conditional action is used; this stays inside the
`NAVIGATE`/`NODE` reaction model already used everywhere else in the file.

This means `Rail=Collapsed` no longer implies the 1280 canvas 0041 described.
Collapse is now a same-width (1440), narrower-rail state; canvas width is a
breakpoint concern only, unrelated to whether the rail is expanded. 0041's
"five 1440 masters, the five 1280 counterparts" description of frame layout
no longer holds — see Consequences for the frame count as it stands now.

Widening the content frame exposed a second defect: an image fill in `CROP`
mode holds a fixed crop rectangle sampled from the source photo, so widening
the frame that holds it shows a different, shifted crop rather than adapting.
Found on S-03 Rules' camera image; swept for elsewhere and found once more on
S-02 grid. Fixed by switching those fills from `CROP` to `FILL` scale mode,
which recomputes to cover the new frame automatically. Unmodified frames keep
their existing `CROP` transforms — those remain correct for a size that never
changed.

## Consequences

`03 Hi-fi` now holds twelve top-level frames, not eleven: sign in, the four
S-02 frames (grid and focused camera, each Expanded and Collapsed), and two
each for Rules, Alerts and Integration, plus the 1920 fluid proof. The
Collapsed frames are real siblings in each screen's section, not runtime
states of the Expanded ones — a rail change now costs two edits per screen
instead of one, which is the direct trade for sidestepping Figma's
whole-instance Interactive Component memory rather than fighting it.

A full audit after wiring — every reactive node on all twelve frames,
classified by whether its destination is Expanded, Collapsed, or neither —
found zero stray cross-state links; the one reaction that should stay
unchanged in both states (sign out, which has no Collapsed counterpart) does.
That audit, plus a side-by-side screenshot of one pair, is what this decision
rests on — a fresh Present-mode walkthrough is still owed as the final check.

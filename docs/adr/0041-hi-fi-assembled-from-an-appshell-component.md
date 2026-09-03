# 41. The hi-fi screens are assembled, and what assembling them settled

**Date:** 2026-09-02
**Status:** Accepted — collapsed-rail canvas narrowed by [0047](0047-rail-collapse-becomes-baked-frame-pairs.md), flow-frame scope narrowed by [0048](0048-phase-2-closes-flow-frames-deferred.md), collapse-as-frames narrowed by [0057](0057-hi-fi-frames-are-the-ui-specification.md)

## Context

[0040](0040-kit-gaps-built-out-for-hi-fi.md) closed the kit gaps and left one
thing outstanding: `03 Hi-fi` was empty, and the five screens still had to be
built from `02 UI Kit`. This records what building them decided.

Two facts shaped the work. `01 Wireframes` holds 2629 frames and not a single
component instance — it is hand-drawn greyscale throughout, so hi-fi is a fresh
build that reads the wireframes as a layout spec rather than a re-skin. And
[0039](0039-state-coverage-evidenced-three-ways.md)'s own complaint about the
old wireframes, that the console shell was hand-drawn about fifty times, was
about to repeat itself in a more expensive medium.

## Decision

**The console chrome is a component, `AppShell`, and every screen but sign in is
an instance of it.** Eight variants: `Rail=Expanded` at 1440 and
`Rail=Collapsed` at 1280, crossed with `Active` naming the highlighted
destination. The alternative — drawing the app bar and rail onto each frame —
is the failure 0039 named, and a rail change would have been eleven edits. The
component lives in `02 UI Kit`, so "assembled solely from `02 UI Kit`" is met by
putting the shell in the kit rather than by redrawing it outside.

**Eleven frames, not a mirror of all thirty-one.** The five 1440 masters, the
five 1280 counterparts, and the focused-camera view. The focused view is the
only screen where `Timeline`, `DetectionBox`, `RuleZone` and `CapabilityNotice`
render at all; without it four of the kit's most load-bearing components would
appear nowhere in hi-fi, and the [0038](0038-historical-timeline-on-the-focused-camera-view.md)
timeline would go unshown. The flow frames — `too many attempts`, `drawing a
zone`, `mute applied`, `the test event was refused` and the rest — are a second
pass. Day is rendered as a check, not designed.

**The prototype is wired to what exists, and says so.** Sign in to Live View,
rail navigation between the four shell screens within each width set, sign out
back to sign in, and grid to focused camera and back. 1440 does not link to 1280;
that is a breakpoint, not a navigation. 0039 fixed the destination set as
exactly the Flow frames, so this prototype is partial by construction until the
second pass lands, and should not be read as complete.

**The rail gets glyphs, because the kit had none.** `NavItem / Variant=Collapsed`
carried an empty 18×18 placeholder and the Expanded variant had no icon slot at
all, so a collapsed 1280 rail would have been four blank squares. `NavGlyph`
adds five glyphs — the four destinations plus the collapse control — each in a
Rest and an Active tone matching `NavItem`'s own label colours. It is not a
general icon set; the rail is the only chrome in IBVAP that carries icons.

**Shell dimensions become tokens rather than typed numbers.** `chrome/appbar`
= 52, `chrome/rail-expanded` = 240, `chrome/rail-collapsed` = 64 and `icon/md`
= 18, on the same reasoning [0040](0040-kit-gaps-built-out-for-hi-fi.md) used
when it added `control/xl` instead of typing 56.

**`Panel` and `Drawer` are detached in hi-fi; everything inside them is not.**
Neither exposes a content slot, and a Figma instance cannot take new children,
so a panel holding real screen content has to be detached. Detaching preserves
every variable binding and text style, and the atoms inside — `Input`, `Button`,
`Select`, `SegmentedControl`, `RuleCard`, `EventRow`, `DeliveryRow`,
`ConnectionState`, `VideoTile`, `Timeline`, `AssessControl`, `ClipRequest`,
`CapabilityNotice` — all remain instances. The cost is that a later change to
`Panel` will not reach these screens. Giving `Panel` an instance-swap content
property was considered and rejected for now: it would require a component per
panel body, which is a worse trade at eleven frames than at fifty.

**The near-white active nav row stands.** Stretched full-bleed across a 240px
rail, `NavItem / State=Active` reads considerably louder than it does at the
kit's own 166px, which sits awkwardly against
[0030](0030-dark-console-palette-no-severity-colour.md)'s premise that a bright
screen at a dark post is a liability. It was put to the decision and kept: the
component was reviewed under [0031](0031-component-grammar-chip-states-fact-segmented-control-chooses.md),
the token wins, and reopening a settled component to soften one screen is the
wrong trade. Recorded here because the tension is real and someone will see it
again.

## Consequences

`03 Hi-fi` holds eleven screen frames in five sections plus a 1920 fluid proof,
all in Night. The raw-value sweep [0031](0031-component-grammar-chip-states-fact-segmented-control-chooses.md)
requires returns zero across every hand-built node: 85 spacing and radius values
bound to tokens, and seventeen off-scale numbers snapped onto the scale rather
than left as judgement calls — the brand panel's 72px margin became
`space/40`, the capability row's 10px gap became `space/8`, the zoom control's
6/10 padding became `space/4` and `space/8`.

Assembly found two components that did not survive being resized, which no
amount of inspecting them at their built size would have shown. `RuleLine`'s
geometry had no stretch constraint, so a rule drawn on a camera frame ran off
the edge of it; `VideoTile`'s timestamp and header were pinned top-left, so an
enlarged tile put its clock in the middle of the picture. Both were fixed in the
kit rather than worked around on the screen, which is the same choice 0040 made
with `AppBar`. This is now the third time a check has paid for itself, and the
pattern is consistent: components are correct at the size they were drawn and
wrong at every other size until something forces the question.

Rendering Day caught nothing that vanishes, but it did expose a tension worth
stating. `surface/video` inverts to a light surface, while `video-chrome/fg`
holds one fixed value in both modes by 0040's deliberate decision — so on an
empty placeholder tile the Day timestamp is nearly unreadable. That is an
artefact of there being no footage rather than a defect: the fixed pair exists
precisely because real pixels under the chrome are footage and not a themed
surface. No change was made, and the reasoning is recorded so the next person
does not "fix" it.

One divergence from the wireframes is deliberate. S-04 draws its event list as a
stack of `EventRow` cards with no `TableHeader`, because the kit's `EventRow` is
a card carrying a thumbnail, chip, description and source line — not a row of
cells that a header could label. A header strip over it would assert an
alignment that does not exist. The wireframe's five-column table and the kit's
row disagree, and the kit is what ships.

The remaining work of Phase 2 Task 2 is the second pass: the flow frames, and
the prototype destinations that come with them.

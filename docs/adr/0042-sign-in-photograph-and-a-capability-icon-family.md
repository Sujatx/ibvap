# 42. The sign-in panel carries the photograph, and the icons become one family at two grids

**Date:** 2026-09-02
**Status:** Accepted

## Context

[0041](0041-hi-fi-assembled-from-an-appshell-component.md) built the sign-in
brand panel as a token-bound surface with no image, because none existed — the
photograph was one of two open inputs the hi-fi pass ran without. One has since
been supplied: 768×1024, a border watchtower and a fenceline against mountains,
shot high-key and almost fully desaturated.

The four capability marks on that panel were standing in with `NavGlyph`, the
18px rail set. That was expedient rather than right. The rail set names
destinations — Live View, Rules, Alerts, Integration, Collapse — and the
capability row names capabilities, so the substitution put a grid-of-tiles glyph
under `LIVE MONITORING` and a chain link under `ACTIONABLE INSIGHTS`. Neither
glyph said what the word beside it said.

The rail set had a second problem that the sign-in row exposed. Its five glyphs
were drawn to no shared rule — a four-square grid, a tilted quad, a bell, a link
and a pair of chevrons, each at whatever weight it needed to read. Beside a row
drawn to one grid and one stroke, the rail looked assembled rather than designed.

## Decision

**The capability marks are a component set of their own, not four more `NavGlyph`
variants.** `CapabilityGlyph` holds Monitoring, Detection, Alerts and Insights —
a camera, a crosshair, a bell and a rising bar chart — drawn as one family on a
24 grid at 1.5 stroke with round caps and joins. Two sets rather than one
because the rows answer different questions, and folding them together would
mean a rail icon could change because the sign-in panel wanted a camera.

**The rail is redrawn into that same family, at its own grid.** All five
`NavGlyph` glyphs are replaced in place with drawings that follow the family
rule — 18 grid, 1.5 stroke, round caps and joins — and Live View and Alerts now
carry the family's camera and bell instead of a grid of tiles and a bell of their
own. Rules, Integration and Collapse keep what they meant and change only how
they are drawn. One family at two grids, then: 18 names destinations, 24 names
capabilities. The two sets stay separate so the sizes stay independent, and the
drawings they share are shared deliberately rather than by coincidence.

**`icon/lg` = 24 is added; `icon/md` is not redefined.** The rail runs at 18 and
must keep running at 18. This is the move
[0040](0040-kit-gaps-built-out-for-hi-fi.md) made for `control/xl`, for the same
reason: moving a token that other components already sit on changes them
silently.

**The photograph sits under a scrim bound to `surface/canvas`, and is darkened in
the paint rather than buried under an opaque one.** The image is nearly white
across its top two-thirds, so a scrim heavy enough to bring it into the Night
palette on its own would have hidden the tower and the fence — the only two
things in the frame that say what the product is for. Exposure, contrast and
shadows are pulled down and most of the saturation removed in the paint itself,
which lets the scrim stay at 0.72 and the structure read. The scrim is a layer of
its own at the bottom of the panel and carries that opacity on the node, not on
the paint: paint-level opacity on a variable-bound fill does not survive the
variable being re-resolved, and reverted silently to opaque once. Binding the scrim to
`surface/canvas` rather than to a fixed dark is deliberate: the pixels under it
are a brand surface that should invert with the theme, not footage, so the
fixed-in-both-modes `video-chrome/scrim` from 0040 is the wrong token here.

## Consequences

`02 UI Kit` gains one component set of four variants and one dimension token, and
`NavGlyph`'s ten variants are redrawn in place. Redrawing in place rather than
replacing the set means every `NavItem`, every `AppShell` variant and all eleven
hi-fi frames inherit the new glyphs with nothing to relink, and the four
destinations keep the names and tones they had. The raw-value sweep [0031](0031-component-grammar-chip-states-fact-segmented-control-chooses.md)
requires returns zero across the new set and across both brand panels, excepting
the crest instance `Icon / Property 1=Dark`, whose two fills are the mark itself
and were already exempt.

Both `S-01` frames are updated and nothing else moved; the capability item grows
from 40 to 46 high and the auto-layout absorbs it at 1440 and 1280 alike.

In Day mode the photograph washes out to nearly flat, because it is darkened in
the paint and then covered by a light scrim. Night is what this pass designs, so
this is recorded rather than fixed — the same treatment 0041 gave the
`surface/video` tension. It is worth knowing that the crest is close to invisible
in Day too, which predates this change and is a separate problem.

0041's statement that the brand panel carries no photograph no longer holds.
Nothing else in it changes. The supplied `sign-in bg` rectangle stays on the
`03 Hi-fi` page as the asset drop; the panels reference the image directly and no
longer depend on it.

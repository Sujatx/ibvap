# 44. The site sketch returns, on Live View, and stops short of being a map

**Date:** 2026-09-03
**Status:** Accepted

## Context

[0017](0017-cameras-site-sketch-not-a-map.md) allowed the console one
operator-supplied, non-interactive site image with hand-placed camera markers,
for orientation only — no coordinates, no GPS, no geospatial layer, no viewshed
modelling. It then noted that the screen which would have carried it, a dedicated
Cameras list, does not exist in the five-screen build
([0016](0016-mvp-ui-cut-to-five-screens.md)), and closed by saying the decision
would apply if that screen came back. It never did, so nothing was ever drawn.

The reference archived on `99 Archive` (frame 23:7) puts a spatial panel on the
focused camera view instead of on a screen of its own: a topographic map with
zoom controls, a Map/Satellite toggle, a camera marker and a shaded cone showing
what that camera sees. Asked which of the reference's refused elements he wanted,
Sujat named this one.

Every documented platform above one site gives its cameras some spatial
reference, which is what
[0017](0017-cameras-site-sketch-not-a-map.md) was built on. What has changed is
not the argument but the place: the panel no longer needs a screen to live on.

## Decision

**The site sketch appears as a panel on the focused Live View.** It answers one
question — where is the camera I am watching, relative to the others — at the
moment that question is asked, which is not a question worth a screen.

**It is a picture with pins on it, and everything on it is placed by hand.** The
image is supplied by the operator. The markers are positioned by the operator.
The facing wedge on a marker is the operator's note about roughly where that
camera points; it is not surveyed, not projected, and not computed from a lens,
a mounting height or a terrain model. Calling it a viewshed would be claiming an
accuracy nothing here has, which is the failure
[0017](0017-cameras-site-sketch-not-a-map.md) exists to prevent, so the panel
says `not to scale` on its face.

**What it is not:** no coordinates, no GPS, no geospatial layer, no zoom, no pan,
no Map/Satellite toggle, no basemap fetched from anywhere. Those would make it a
map, the single-site boundary
([0014](0014-mvp-scoped-to-one-deployment-site.md)) does not earn one, and a
console that cannot reach the internet from a border post cannot serve one
honestly.

**A site with no image says so.** `State=No image` is the resting state, in plain
language, because a site that has not supplied a picture is a normal site and not
a fault ([0030](0030-dark-console-palette-no-severity-colour.md) rule 2).

At 1280 the panel does not fit beside everything else and moves behind a
`Site view` control in the camera header, the same move
[0039](0039-state-coverage-evidenced-three-ways.md) makes for the third column on
S-03 and S-04.

## Consequences

This narrows [0017](0017-cameras-site-sketch-not-a-map.md) rather than
superseding it: the permission it granted is unchanged, the screen it was waiting
for is not coming, and the panel now has a home. Its exclusions are restated here
because they are what keeps the panel from growing into the map the reference
drew.

`02 UI Kit` gains `SiteSketch` and `CameraMarker`. The marker's `Offline` state
reuses the transport tokens `StatusDot` uses, because it is the same fact about
the same stream and should not acquire a second vocabulary.

The panel needs an image that does not exist yet. Until one is supplied it draws
the markers on a flat ground, which is honest but is not what the panel is for —
this is the second open input on this screen, alongside the camera stills.

If a deployment ever spans more than one site, this panel is the first thing that
breaks, and the right answer then is a decision about multi-site, not a bigger
picture.

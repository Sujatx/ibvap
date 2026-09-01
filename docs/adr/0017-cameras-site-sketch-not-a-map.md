# 17. A static site sketch on the Cameras list, not a map

**Date:** 2026-08-26
**Status:** Accepted — screen cut from current build by [0016](0016-mvp-ui-cut-to-five-screens.md)

## Context

[international-border-surveillance-platforms.md](https://app.notion.com/p/3c986dda46e281bbbd54c6b5c8061a3f?pvs=204)
found every documented platform above one site provides some spatial
reference for its cameras. The MVP's single-site boundary
([0014](0014-mvp-scoped-to-one-deployment-site.md)(a)) rules out a full
common operating picture, which stays excluded — a plain static image is a
different, far cheaper object, previously omitted only by oversight.

## Decision

The Cameras screen may carry one operator-supplied, non-interactive site
image with hand-placed camera markers, for at-a-glance orientation only —
no coordinates, no GPS, no geospatial layer, no viewshed modelling.

## Consequences

A dedicated Cameras screen doesn't exist in the current five-screen build
([0016](0016-mvp-ui-cut-to-five-screens.md)); this decision would apply if
that screen returns.

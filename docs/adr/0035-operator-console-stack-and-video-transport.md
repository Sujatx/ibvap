# 35. Operator console stack, and video reaches the browser separately from detections

**Date:** 2026-09-01
**Status:** Accepted — gateway choice settled by [0054](0054-go2rtc-is-the-webrtc-gateway.md)

## Context

Five screens are frozen ([ADR 0016](0016-mvp-ui-cut-to-five-screens.md)) and
the Figma UI kit that builds them is complete — two-layer variable
collections with Night and Day modes, nine text styles, close to forty
components. [ADR 0030](0030-dark-console-palette-no-severity-colour.md) makes
a raw colour value inside a component a defect rather than a shortcut, and
[ADR 0031](0031-component-grammar-chip-states-fact-segmented-control-chooses.md)
fixes the control grammar. None of that survives contact with code unless the
front-end stack carries the token layer intact.

Live View is the screen that actually decides this. It has to show what a
camera is seeing now, with detection boxes over it, and a camera can be
refused a capability inline
([ADR 0007](0007-refuse-unsupported-capabilities-not-degrade.md)). How the
pixels arrive is the single unanswered question — and the
[technical feasibility research](https://app.notion.com/p/3c986dda46e281a7a1c3d87623970822?pvs=204)
(Notion) is emphatic that video and metadata are different products with
bandwidth profiles orders of magnitude apart, and that the industry has
converged on processing locally and shipping metadata rather than video.

The rig encodes 1080N — 960×1080 squeezed from a 1920×1080 image, which every
frame has to be stretched back out to before a person can read it.

## Decision

**React with TypeScript, built by Vite.**

**The Figma variable collections are exported to CSS custom properties, and
that is the only route by which colour, spacing or type enters a component.**
Tailwind v4 consumes those properties directly, which is why it is used here
rather than a utility framework carrying its own palette. Night and Day are a
swap of the semantic layer, exactly as they are in Figma; a component never
learns which mode it is in.

**Video and detections travel to the browser as two separate channels and are
composited there.** H.264 pixels reach the page over WebRTC, served by an
embedded gateway — go2rtc or MediaMTX — that republishes the camera's existing
stream without transcoding it. Detections arrive as JSON on the application's
own WebSocket and are drawn on a transparent Canvas 2D layer aligned to the
video element.

The alternative — burning boxes into frames server-side and shipping the
result as MJPEG — is rejected as the default, because it forces the platform
to re-encode every frame of every camera purely to draw a rectangle, and
re-encoding is precisely the cost
[ADR 0032](0032-inference-runtime-decode-path-and-detector-licence.md) is
arranged to avoid. **MJPEG over HTTP stays as the documented fallback** for
any browser, network or camera the WebRTC path cannot reach.

**Anamorphic correction happens in the browser.** Detection coordinates are
produced and transmitted in the stream's native encoded geometry, and the
display layer applies the stretch to both the video and the overlay together.
Correcting in one place and not the other is how overlays end up misaligned
by exactly a factor of two.

## Consequences

Separating the channels is what keeps the overlay honest. A box on screen is
data the operator can see the provenance of — a detection with a class, a
confidence and a timestamp — rather than pixels somebody already decided to
paint. It is also what makes a refusal displayable in the same place a
detection would have been, which
[ADR 0007](0007-refuse-unsupported-capabilities-not-degrade.md) requires.

It also creates a synchronisation problem that burning boxes into frames does
not have: the video and the detections arrive over different transports with
different latencies, and an overlay drawn against the wrong frame is worse
than no overlay. Detections carry the frame timestamp they belong to, and the
overlay is responsible for holding or dropping accordingly. This is real work,
and it is the price of the separation.

The WebRTC gateway is the one component in this decision that is a third-party
binary rather than a library, and it is the highest-risk choice in the
front-end stack. It is chosen because it is proven at exactly this job in the
one comparable open-source product, and because writing a streaming server is
not what this team should spend a hackathon on. If it does not hold, MJPEG is
the retreat and it is already documented — a degraded picture, not a missing
screen.

Generating tokens from Figma means the export is a build step someone has to
own, and a component referencing a token that no longer exists is a build
failure rather than a wrong colour. That is the intended direction.

Nothing here decides how the Rules screen's polygon editor is drawn, or how
clips are played back on Alerts & Events. Both sit on top of this stack and
neither changes it.

[docs/architecture/README.md](../architecture/README.md) §8 no longer lists
payload-progressive delivery as depending on an undecided transport.

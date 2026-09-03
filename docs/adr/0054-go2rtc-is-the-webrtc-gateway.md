# 54. go2rtc is the WebRTC gateway

**Date:** 2026-09-03
**Status:** Accepted — settles the open choice in [0035](0035-operator-console-stack-and-video-transport.md)

## Context

[0035](0035-operator-console-stack-and-video-transport.md) decided that video and
detections travel to the browser as two separate channels: H.264 pixels over
WebRTC from an embedded gateway that republishes the camera's stream without
transcoding, and detections as JSON on the application's own WebSocket. It named
the gateway as "go2rtc or MediaMTX" and did not choose, while also naming it the
highest-risk choice in the front-end stack — the one component that is a
third-party binary rather than a library.

Both candidates do the core job: pull RTSP, republish to WebRTC, no transcode,
single Go binary, MIT licence, runs on Windows. MediaMTX has broader adoption and
better protocol coverage. go2rtc is smaller and purpose-built for republishing
existing camera streams to a browser.

The deciding consideration is what happens when WebRTC does not work. 0035 keeps
MJPEG over HTTP as the documented fallback — "a degraded picture, not a missing
screen" — and someone has to build that fallback.

## Decision

**go2rtc is the WebRTC gateway.**

It negotiates WebRTC, and falls back through MSE, HLS and MJPEG within a single
player when WebRTC cannot be established. That hands 0035 its documented retreat
as a property of the component rather than as a feature the console has to
implement, test and maintain against browsers nobody has enumerated.

The gateway runs as a separate process from the IBVAP application, configured
from a generated YAML file listing one stream per camera. It pulls its own RTSP
session from each camera, independent of the analytics pipeline's session.
`GET /api/cameras/{id}/stream` returns both the WHEP URL and the MJPEG URL, and
the console chooses.

## Consequences

The console's video component gets simpler: one player, one source, automatic
degradation. Building and maintaining a hand-rolled MJPEG fallback path was real
work that this removes, and it was work that would only ever have been exercised
on the browsers and networks nobody tested.

Each camera now carries two RTSP sessions — one for go2rtc, one for analytics —
against a recorder with a shared 12,288 kbps / 120 fps budget across eight
channels
([0015](0015-mvp-validated-against-development-cctv-rig.md)). That doubling is
the real cost of this whole two-channel architecture, not of go2rtc specifically,
but it lands here and it needs measuring alongside the decode bench. If the
recorder cannot serve two sessions per channel, the fallback is for go2rtc to
consume the sub-stream while analytics takes the main stream.

The risk 0035 named does not go away. This is still a third-party binary in the
front-end path, still the highest-risk component in the console stack, and still
something to be supervised at a site with no engineer. Choosing the smaller and
more specialised of the two candidates reduces the surface but does not remove
the dependency.

Nothing about this decision is hard to reverse. Both candidates speak WHEP and
both are configured by a file; swapping to MediaMTX changes the binary, the
config generator, and the URL the `stream` endpoint returns. It does not touch
the console's player or the analytics pipeline, because neither knows which
gateway is running.

[docs/architecture/README.md](../architecture/README.md) records the gateway as
decided rather than as a choice between two.

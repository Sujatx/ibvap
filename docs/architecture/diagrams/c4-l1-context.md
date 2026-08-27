# C4 — Level 1: System Context

The IBVAP system and its direct actors — nothing inside the system boundary.
Referenced from [../README.md §3](../README.md#3-context-and-scope).

```mermaid
C4Context
  title IBVAP — System Context

  Person(operator, "Post operator", "Views live detections, authors rules, assesses alerts")

  System(ibvap, "IBVAP", "Turns existing CCTV into an intelligent surveillance network")

  System_Ext(cctv, "Existing CCTV / recorder", "IP cameras, or analog channels behind an existing DVR/XVR/NVR")
  System_Ext(c2, "Command & control system", "Generic — no named target system confirmed (ADR 0006)")

  Rel(operator, ibvap, "Signs in, configures, assesses", "HTTPS")
  Rel(ibvap, cctv, "Reads video streams, read-only", "RTSP / ONVIF")
  Rel(ibvap, c2, "Publishes events", "Webhook / REST / MQTT — ADR 0006")
```

## Notes

- IBVAP never writes to the camera or recorder — no reconfiguration, no
  takeover of recording ([ADR 0004](../../adr/0004-function-without-remote-monitoring-layer.md)).
- The existing VMS/live-view path, if any, is unaffected — IBVAP is an
  additional, independent RTSP consumer, not a replacement.
- The C2 system is drawn as external and generic because no real target
  system has been named ([ADR 0006](../../adr/0006-c2-integration-via-generic-event-contract.md)).

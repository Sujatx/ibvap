# C4 — Level 2: Container

**Status: proposed, not decided.** This is the container split proposed in
[RFC 0001](../../rfcs/0001-video-ingest-and-analytics-pipeline.md) (Draft),
shown here to make the proposal concrete — it becomes authoritative only if
that RFC is accepted, and this diagram must be updated to match if the
proposal changes during review.

```mermaid
C4Container
  title IBVAP — Container view (proposed, RFC 0001)

  Person(operator, "Post operator")
  System_Ext(cctv, "Existing CCTV / recorder")
  System_Ext(c2, "Command & control system")

  Container_Boundary(ibvap, "IBVAP") {
    Container(ingest, "Ingest service", "Per-camera RTSP/ONVIF connection, capability measurement, per-vendor path handling")
    Container(inference, "Inference service", "Runs detection/classification models against decoded frames")
    Container(rules, "Rule engine", "Evaluates operator-authored rules against inference output; writes Events/Alerts")
    Container(store, "Event store", "Events, Alerts, assessments, rule definitions, capability verdicts")
    Container(egress, "Egress publisher", "Delivers the versioned event contract outward; queues when disconnected")
    Container(webapp, "Web application", "Sign in, Live View, Rules, Alerts & Events, Integration")
    Container(api, "API", "Backs the web application; authorization and attribution")
  }

  Rel(operator, webapp, "Uses", "HTTPS")
  Rel(webapp, api, "Calls")
  Rel(api, store, "Reads/writes")
  Rel(ingest, cctv, "Reads streams", "RTSP/ONVIF")
  Rel(ingest, inference, "Decoded frames")
  Rel(inference, rules, "Detections")
  Rel(rules, store, "Events, Alerts")
  Rel(store, egress, "Reads")
  Rel(egress, c2, "Publishes", "Webhook/REST/MQTT")
```

## Open questions this view does not answer

- Edge vs. central placement of the inference container — see RFC 0001.
- Whether ingest and inference are one process or two, given decode is the
  binding compute cost, not inference itself (technical-feasibility research
  §3.3).
- Storage engine for the event store.
- Whether the egress publisher is push (webhook) or pull (MQTT subscriber),
  or both.

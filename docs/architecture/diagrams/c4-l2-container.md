# C4 — Level 2: Container

**Status: proposed, not decided.** This is the container split the project
currently expects, shown here to make it concrete. It becomes authoritative
only once the [RFCs](../../rfcs/README.md) covering ingest, rules, the event
store, the API and egress are accepted, and must be updated to match if any
of them lands differently.

```mermaid
C4Container
  title IBVAP — Container view (proposed)

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

- Edge vs. central placement of the inference container.
- Whether ingest and inference are one process or two, given decode is the
  binding compute cost, not inference itself (technical-feasibility research
  §3.3).
- Whether the egress publisher is push (webhook) or pull (MQTT subscriber),
  or both.

The storage engine is no longer open — see
[ADR 0034](../../adr/0034-local-event-store-on-sqlite.md).

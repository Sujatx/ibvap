# 09. Non-Functional Requirements

The quality attributes the design above is sized against: performance,
availability, scalability boundary, observability and maintainability.
Success-criteria numbers owned by product stay in the Notion PRD; what
follows is what the RFCs themselves commit to and measure.

## Contents

- [Performance budget](#performance-budget)
- [Availability and reliability](#availability-and-reliability)
- [Scalability boundary](#scalability-boundary)
- [Observability](#observability)
- [Maintainability](#maintainability)

## Performance budget

Per camera, per second, at the target analysed rate of 5 fps
([RFC 0006](../../rfcs/0006-detection-and-analytics-primitives.md), Frame
budget):

| Stage | Invocations | Unit cost | Subtotal |
|---|---|---|---|
| Detector | 5 | ~8 ms | ~40 ms |
| ByteTrack | 5 | < 1 ms | ~5 ms |
| MOG2 + illumination | 5 | ~4 ms, CPU | ~20 ms CPU |
| YuNet | ≤ 2 crops | ~2 ms | ~4 ms |
| SFace (where enabled) | ≤ 1 track | ~3 ms | ~3 ms |
| Plate detect + OCR | ≤ 1 track | ~7 ms | ~7 ms |

Five cameras multiply the GPU line to roughly 250–300 ms of GPU work per wall
second — consistent with a stated ~5× estimated margin
([ADR 0032](../../adr/0032-inference-runtime-decode-path-and-detector-licence.md)).
**This headroom is not the binding constraint — decode is**, and decode
capacity is treated as a per-site operational fact rather than a number fixed
once in this document (see
[10-risks-and-open-items.md](10-risks-and-open-items.md)).

VRAM budget against the 4 GB target machine:

| Consumer | Estimate |
|---|---|
| ONNX Runtime CUDA context | ~300 MB |
| Detector weights + activations | ~400 MB |
| YuNet, SFace, plate detector, plate OCR | ~180 MB combined |
| NVDEC sessions, 5 channels | ~500 MB |
| Headroom | Remainder of 4 GB |

The stated order of retreat if the measured total does not fit: reduce
detector input resolution → reduce analysed rate to the 3 fps floor → move ROI
models to CPU → reduce channel count — the last of which is recorded as a
hardware finding, not a quiet reduction in what the platform claims.

## Availability and reliability

- **72 hours offline, no data loss on reconnect.** Ingest and analytics have
  no remote dependency; the egress queue accumulates and drains in order
  ([08-deployment-and-infrastructure.md](08-deployment-and-infrastructure.md)).
- **Power-loss durability.** WAL with `synchronous = NORMAL` risks at most the
  last transaction — bounded and stated, not hidden (RFC 0003).
- **Backpressure drops frames, never cameras.** A slow analytics pass loses
  the newest-overwrites-oldest frame on one camera; it never takes a camera
  offline (RFC 0001).
- **Bounded egress queue with a stated, visible discard policy.** Oldest
  non-alerting rows are dropped first, and every discard is itself a row in
  `egress_drops` — a gap a consumer can see, not one it discovers by counting
  (RFC 0003, RFC 0005).
- **Every refusal is visible and worded consistently.** A camera, a rule, or
  a whole timeline that cannot do something says so in one voice across the
  chip row, the rule card, and the API response
  ([ADR 0007](../../adr/0007-refuse-unsupported-capabilities-not-degrade.md)).

## Scalability boundary

**One site, one machine, by design** — not a current limitation awaiting more
engineering, but a stated boundary
([ADR 0014](../../adr/0014-mvp-scoped-to-one-deployment-site.md)). No table,
queue, or module here is built for multi-site aggregation; that would need a
different storage engine and is explicitly out of scope (RFC 0003,
Non-goals). Within a site, growth is bounded by SQLite's comfortable range at
five cameras for years, dominated by clip storage rather than row count (RFC
0003, Cross-cutting concerns).

## Observability

| Layer | Tracked, continuously, per unit |
|---|---|
| Ingest | Connection state, delivered fps, analysed fps, dropped-frame count, reconnect count, decode path, newest-frame age — per camera (RFC 0001) |
| Analytics | Analysed fps achieved, per-stage latency, crops attempted vs. skipped by gate, plate reads split by grammar-matched vs. unverified — per camera (RFC 0006) |
| Rules | Fires per hour, fires suppressed by debounce, fires suppressed by mute, current refusal state — per rule (RFC 0002) |
| Egress | Pending depth, oldest-pending age, delivered in the last hour, dead count, last error — per endpoint (RFC 0005) |

Oldest-pending-age and analysed-vs-delivered fps are the two numbers called
out specifically as what make a degraded site diagnosable by someone who is
not standing next to it.

## Maintainability

- **Models are versioned artefacts, not code.** `models/manifest.json` names
  file, hash, input shape and licence per model; the application refuses to
  run with an artefact it cannot identify
  ([ADR 0058](../../adr/0058-model-artefacts-are-versioned-files-with-a-manifest.md)).
  Swapping a detector is a file and a manifest change, not a code change.
- **Rule and capability-verdict history is immutable.** Every edit is a new
  version; nothing overwrites a record of what was true at the time.
- **Migrations from the first schema.** Alembic, with the create-copy-swap
  batch pattern SQLite's limited `ALTER TABLE` requires, and a working
  `downgrade` on every migration or a stated reason it cannot have one (RFC
  0003, Migrations).
- **The AGPL boundary is confined and auditable.** Only the detector artefact
  carries copyleft (exported via Ultralytics); no component imports
  Ultralytics, PyTorch or InsightFace at runtime, which is what keeps the
  detector swappable to an Apache-2.0 alternative (RTMDet, YOLOX, RT-DETR) a
  file change rather than a rewrite (RFC 0006, Cross-cutting concerns).

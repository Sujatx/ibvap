# 58. Model artefacts are versioned files with a manifest, not code

**Date:** 2026-09-03
**Status:** Accepted

## Context

[0032](0032-inference-runtime-decode-path-and-detector-licence.md) makes an
argument that the whole licence position rests on: ONNX Runtime consumes an ONNX
file and knows nothing about what produced it, so a force needing a non-copyleft
deployment can swap in a permissively licensed detector without touching the
pipeline. It states plainly that this escape route "only exists because the model
is an artefact rather than a library call, and it stops being true the moment a
component imports Ultralytics at runtime."

[RFC 0006](../rfcs/0006-detection-and-analytics-primitives.md) now brings four
model families into the same process — a general detector, a face detector, a
plate detector and a plate OCR model — carrying at least three different licences
between them. The property 0032 relies on has to be maintained deliberately
across all of them, and it has to be checkable by someone who was not there.

There is a second problem the first one hides. A model file is large, opaque, and
easy to replace. A silently swapped detector produces silently different
evidence, on a platform whose output may be used to justify stopping a person or
a vehicle.

## Decision

**Model files live in `models/`, are not committed to git, and are described by
`models/manifest.json`, which is. The application verifies every artefact's hash
at startup and refuses to run with one it cannot identify.**

The manifest carries, per artefact: an id, the filename, a SHA-256, the input
name, shape and layout, the output layout, the class map, the licence, and where
it came from.

```json
{
  "id": "detector",
  "file": "yolo-detector.onnx",
  "sha256": "…",
  "input": {"name": "images", "shape": [1, 3, 384, 640], "layout": "NCHW"},
  "output": {"name": "output0", "layout": "xywh+conf+cls"},
  "classes": ["person", "bicycle", "car", "motorcycle", "bus", "truck"],
  "licence": "AGPL-3.0-or-later",
  "source": "…"
}
```

Two rules go with it. **No component imports a training framework at runtime** —
not Ultralytics, not PyTorch, not InsightFace. Doing so is a defect, in the sense
0032 already established. And **a model swap is a manifest change**, not a code
change: replacing the detector with RTMDet, or the plate OCR with PaddleOCR,
means a new file and a new manifest entry.

## Consequences

The licence position becomes auditable rather than folkloric. Anyone can read
`models/manifest.json` and see which artefacts carry which terms, and the AGPL
encumbrance is visible as one row rather than as tribal knowledge about how the
detector was exported. A force needing a permissive deployment has an exact list
of what to replace.

Startup verification means a corrupted or substituted model is a refusal to
start, not a subtly different set of detections. That is the right failure: a
platform that will not run is a problem someone fixes, and a platform producing
quietly wrong evidence is a problem nobody notices.

Keeping the files out of git costs a distribution step. A fresh checkout does not
run until the artefacts are fetched, and the manifest is what makes fetching them
verifiable. This is accepted because committing hundreds of megabytes of binary
into a repository that is otherwise text is a worse trade, and because some of
these artefacts carry terms that are better pointed at than vendored.

The input and output shapes in the manifest are load-bearing rather than
documentation. The pre- and post-processing code reads them, so a model exported
at a different input resolution does not silently produce boxes in the wrong
coordinate space — it either matches the manifest or fails.

CI checks that the manifest parses and that every entry is well formed. It cannot
check the hashes, because the artefacts are not in the repository; that check
happens at startup on the machine that actually has them.

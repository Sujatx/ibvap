# Architecture Decision Records

One file per decision — project, product, design, or architecture —
numbered sequentially in the order made, using the Nygard/MADR format
(`Status` / `Context` / `Decision` / `Consequences`). Supersedes the
per-stage decisions logs previously kept at `docs/00-project/decisions.md`
and `docs/03-design/decisions.md` (see
[0029](0029-decision-log-restructured-as-one-adr-per-file.md)); those files
no longer exist, their content lives here.

To add a new decision: create the next-numbered file below, following the
format any existing entry uses. Never append to an old entry or reopen a
running log — a change of mind gets a new file with `Status: Supersedes
NNNN`, and the old file gets `Status: Superseded by NNNN`.

| # | Title | Status | Date |
|---|---|---|---|
| [0001](0001-project-setup-and-documentation-structure.md) | Project setup and documentation structure established | Accepted | 2026-08-24 |
| [0002](0002-differentiate-on-deployment-not-benchmark-accuracy.md) | Differentiate on deployment, not benchmark accuracy leadership | Accepted | 2026-08-25 |
| [0003](0003-ssb-is-validation-context-not-product-boundary.md) | SSB is the validation context, not the product boundary | Accepted | 2026-08-25 |
| [0004](0004-function-without-remote-monitoring-layer.md) | Function correctly whether or not a remote monitoring layer is available | Accepted | 2026-08-25 |
| [0005](0005-core-workflows-modelled-around-artefacts-and-states.md) | Core workflows modelled around artefacts and their states | Accepted, narrowed by 0016 | 2026-08-25 |
| [0006](0006-c2-integration-via-generic-event-contract.md) | Satisfy C2 integration via a generic event contract, not a named adapter | Accepted | 2026-08-25 |
| [0007](0007-refuse-unsupported-capabilities-not-degrade.md) | Refuse unsupported capabilities, rather than degrade them | Accepted, narrowed by 0016 | 2026-08-25 |
| [0008](0008-face-detection-unconditional-gated-recognition.md) | Face detection unconditional; gated recognition specified | Accepted, narrowed by 0016, matching exercised by 0059 | 2026-08-25 |
| [0009](0009-all-eight-capabilities-with-declared-maturity.md) | All eight SIH capabilities addressed, with declared maturity | Accepted | 2026-08-25 |
| [0010](0010-support-posture-analytics-layer.md) | IBVAP as a support-posture analytics layer | Accepted, narrowed by 0016 | 2026-08-25 |
| [0011](0011-virtual-fence-plus-open-border-framing.md) | Virtual fence ships in full, plus an open-border framing | Accepted | 2026-08-25 |
| [0012](0012-suspicious-activity-as-operator-authored-rules.md) | Suspicious activity as an operator-authored rule engine | Accepted | 2026-08-25 |
| [0013](0013-night-time-movement-detection-as-explicit-capability.md) | Night-time movement detection as an explicit capability | Accepted | 2026-08-25 |
| [0014](0014-mvp-scoped-to-one-deployment-site.md) | MVP scoped to one deployment site, complete end-to-end | Accepted | 2026-08-25 |
| [0015](0015-mvp-validated-against-development-cctv-rig.md) | MVP validated against the development CCTV rig | Accepted | 2026-08-25 |
| [0016](0016-mvp-ui-cut-to-five-screens.md) | MVP UI cut to five screens | Accepted, the matching cut is narrowed by 0059 | 2026-08-26 |
| [0017](0017-cameras-site-sketch-not-a-map.md) | Cameras site sketch, not a map | Accepted, screen cut by 0016, narrowed by 0044 | 2026-08-26 |
| [0018](0018-operator-assigned-impact-grade.md) | Operator-assigned impact grade | Accepted | 2026-08-26 |
| [0019](0019-case-association-exempts-evidence-from-retention-clock.md) | Case-association exempts evidence from retention clock | Superseded by 0021 | 2026-08-26 |
| [0020](0020-egress-classification-field-deferred.md) | Egress classification field: considered, deferred | Accepted (deferred) | 2026-08-26 |
| [0021](0021-case-two-axis-state-model.md) | The Case gets a real two-axis state model | Accepted, screen cut by 0016 | 2026-08-26 |
| [0022](0022-measurement-rate-and-ranked-offender-views.md) | Measurement dashboard — rate + ranked-offender views | Accepted, screen cut by 0016 | 2026-08-26 |
| [0023](0023-dismissal-cause-captured-on-suppression.md) | Dismissal cause captured on suppression, not assessment | Accepted | 2026-08-26 |
| [0024](0024-session-lockout-and-recovery-for-one-person-site.md) | Session, lockout and recovery for a one-person site | Superseded by 0037 | 2026-08-26 |
| [0025](0025-suppression-auto-expiry-flagged-for-elevation.md) | Suppression auto-expiry, flagged for elevation | Superseded by 0026 | 2026-08-26 |
| [0026](0026-suppression-does-not-expire-visibility-replaces-timer.md) | Suppression does not expire; visibility replaces the timer | Superseded by 0027 | 2026-08-26 |
| [0027](0027-suppression-works-like-notification-snooze.md) | Suppression works like a notification snooze | Accepted | 2026-08-26 |
| [0028](0028-mvp-md-merged-into-prd-md.md) | MVP.md merged into PRD.md | Accepted | 2026-08-27 |
| [0029](0029-decision-log-restructured-as-one-adr-per-file.md) | Decision log restructured as one ADR per file | Accepted | 2026-08-27 |
| [0030](0030-dark-console-palette-no-severity-colour.md) | Dark console palette — colour marks category and attention, never severity | Accepted | 2026-08-29 |
| [0031](0031-component-grammar-chip-states-fact-segmented-control-chooses.md) | Component grammar — a chip states a fact, a segmented control makes a choice | Accepted | 2026-08-29 |
| [0032](0032-inference-runtime-decode-path-and-detector-licence.md) | Inference runtime, decode path, and detector licence | Accepted | 2026-09-01 |
| [0033](0033-backend-framework-packaging-and-auth.md) | Backend framework, packaging, and the authentication mechanism | Accepted | 2026-09-01 |
| [0034](0034-local-event-store-on-sqlite.md) | The local event store is SQLite, and the egress queue lives in it | Accepted | 2026-09-01 |
| [0035](0035-operator-console-stack-and-video-transport.md) | Operator console stack, and video reaches the browser separately from detections | Accepted, gateway settled by 0054 | 2026-09-01 |
| [0036](0036-wireframe-breakpoints-and-required-state-set.md) | Three console widths, and the state set a screen is not finished without | Superseded by 0039 | 2026-09-01 |
| [0037](0037-sign-in-follows-the-reference-username-password.md) | Sign in follows the reference — username and password, with a password reset | Accepted, supersedes 0024 | 2026-09-01 |
| [0038](0038-historical-timeline-on-the-focused-camera-view.md) | A historical timeline on the focused-camera view | Accepted, marker rule superseded by 0046 | 2026-09-02 |
| [0039](0039-state-coverage-evidenced-three-ways.md) | State coverage is evidenced three ways, not one frame per state | Accepted, supersedes 0036 | 2026-09-02 |
| [0040](0040-kit-gaps-built-out-for-hi-fi.md) | The kit gaps are built, and what building them settled | Accepted | 2026-09-02 |
| [0041](0041-hi-fi-assembled-from-an-appshell-component.md) | The hi-fi screens are assembled, and what assembling them settled | Accepted | 2026-09-02 |
| [0042](0042-sign-in-photograph-and-a-capability-icon-family.md) | The sign-in panel carries the photograph, and the icons become one family at two grids | Accepted | 2026-09-02 |
| [0043](0043-focused-camera-view-rebuilt-around-the-picture.md) | The focused camera view is rebuilt around the picture, and Live View gains an alerts rail | Accepted | 2026-09-03 |
| [0044](0044-site-sketch-returns-on-live-view.md) | The site sketch returns, on Live View, and stops short of being a map | Accepted, narrows 0017 | 2026-09-03 |
| [0045](0045-timeline-second-pass-controls-and-density.md) | The timeline's second pass — the controls it gains, and the hue it still refuses | Accepted, marker rule superseded by 0046 | 2026-09-03 |
| [0046](0046-timeline-markers-carry-class-colour.md) | Timeline markers carry class colour, and the axis is drawn as a band | Accepted, supersedes the marker rule in 0038 and 0045; store obligation settled by 0056 | 2026-09-03 |
| [0047](0047-rail-collapse-becomes-baked-frame-pairs.md) | The rail's collapsed state is baked frame pairs, not a runtime variant swap | Accepted, Figma-only, narrowed by 0057 | 2026-09-03 |
| [0048](0048-phase-2-closes-flow-frames-deferred.md) | Phase 2 closes here; the flow frames are deferred, not built | Accepted, narrows 0041 | 2026-09-03 |
| [0049](0049-four-homes-for-project-artefacts.md) | Four homes for project artefacts, decided by one question | Accepted | 2026-09-03 |
| [0050](0050-single-process-inference-placement.md) | Ingest, inference and rules run in one process on one node | Accepted | 2026-09-03 |
| [0051](0051-face-detection-model-and-refusal-threshold.md) | Face detection is YuNet, and it is refused below 24 pixels | Accepted, extended by 0059 | 2026-09-03 |
| [0052](0052-anpr-two-stage-chain-with-a-grammar-gate.md) | ANPR is a two-stage ONNX chain, and its grammar gate rejects but never repairs | Accepted | 2026-09-03 |
| [0053](0053-night-movement-as-a-detector-independent-primitive.md) | Night-time movement is a detector-independent primitive | Accepted | 2026-09-03 |
| [0054](0054-go2rtc-is-the-webrtc-gateway.md) | go2rtc is the WebRTC gateway | Accepted, settles the open choice in 0035 | 2026-09-03 |
| [0055](0055-offline-password-recovery-by-local-admin-reset.md) | Offline password recovery returns, as a local administrator reset | Accepted, settles the regression in 0037 | 2026-09-03 |
| [0056](0056-an-event-carries-one-primary-class.md) | An event carries exactly one primary class | Accepted, settles the store obligation in 0046 | 2026-09-03 |
| [0057](0057-hi-fi-frames-are-the-ui-specification.md) | The hi-fi frames are the UI specification, and rail collapse is runtime state | Accepted, narrows 0041 and 0047 | 2026-09-03 |
| [0058](0058-model-artefacts-are-versioned-files-with-a-manifest.md) | Model artefacts are versioned files with a manifest, not code | Accepted | 2026-09-03 |
| [0059](0059-face-recognition-ships-against-a-configured-watchlist.md) | Face recognition ships against a configured watchlist, using SFace, exactly as 0008 gated it | Accepted, narrows 0016; extends 0051 | 2026-09-03 |
| [0060](0060-file-backed-frame-source-for-testing.md) | A file-backed frame source, for testing and demonstration against footage the rig cannot produce | Accepted | 2026-09-03 |

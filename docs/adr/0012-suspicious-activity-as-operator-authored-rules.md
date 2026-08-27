# 12. Suspicious activity detection as an operator-authored rule engine, not a learned model

**Date:** 2026-08-25
**Status:** Accepted

## Context

Three independent, measured failures of learned video-anomaly detection
(scene overfitting, false-alarm explosion, contested ground truth) exist
against a capability whose definition nobody has supplied. The rule engine
is the only construction that can be honest about what it detects. This
decision must be revisited the moment the force supplies its own
definition of "suspicious" — no experiment substitutes for that answer.

## Decision

"Suspicious activity detection" is delivered as an operator-authored
composite rule engine over reliable primitives, plus a starter library
explicitly marked unvalidated. No learned anomaly model ships.

## Consequences

See [PRD.md](../02-product/PRD.md) §5.1, §9 (open questions).

# 1. Project setup and documentation structure established

**Date:** 2026-08-24
**Status:** Accepted

## Context

Per explicit project setup instructions: keep research, product, design,
architecture and implementation separate, and avoid premature technical or
product decisions.

## Decision

Adopt the workflow Research → Product → Design → Architecture → Engineering
→ Testing → Demo, with a corresponding `docs/` folder per stage, and treat
the official SIH problem statement (Problem Statement ID 26187), recorded
in [problem.md](../00-project/problem.md), as immutable. No tech stack,
architecture, or product features are chosen at this stage.

## Consequences

Every later decision must trace to a stage, and a stage does not begin
before the stage(s) before it are complete for the relevant feature or
decision. `problem.md` cannot be rewritten, simplified, or added to by any
later decision.
